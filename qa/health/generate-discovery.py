#!/usr/bin/env python3
"""Generate search metadata and discovery documents without network dependencies.

Use --write after editing HTML or search-config.json; --check detects drift.
Publication and modification dates are editorial inputs, never the build clock.
"""
import argparse
import copy
import html
import json
import re
import xml.etree.ElementTree as ET
from datetime import date
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / 'qa/health/search-config.json').read_text())
DOMAIN = CFG['baseURL']
DATE = CFG['modified']
ARCHIVE = 'essays/index.html'
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}


class Blocks(HTMLParser):
    """Existing full-site text extraction, outside the stricter essay body."""
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.inside = False
        self.kind = None
        self.parts = []
        self.blocks = []
        self.skip = 0

    def handle_starttag(self, tag, attrs):
        if tag == 'main':
            self.inside = True
        if not self.inside:
            return
        if tag in ('svg', 'script', 'style'):
            self.skip += 1
        if tag in ('h1', 'h2', 'h3', 'p', 'li', 'summary') and not self.skip and self.kind is None:
            self.kind, self.parts = tag, []
        if tag == 'br' and self.kind:
            self.parts.append(' ')

    def handle_endtag(self, tag):
        if tag == 'main':
            self.inside = False
        if tag in ('svg', 'script', 'style') and self.skip:
            self.skip -= 1
        if self.kind == tag:
            text = re.sub(r'\s+', ' ', ' '.join(self.parts)).strip()
            if text:
                self.blocks.append((tag, text))
            self.kind = None

    def handle_data(self, data):
        if self.inside and self.kind and not self.skip:
            self.parts.append(data)


class EssaySource(HTMLParser):
    """Read H1 and the visible thesis/prose, excluding navigation and related links."""
    def __init__(self, source):
        super().__init__(convert_charrefs=True)
        self.stack, self.frames, self.blocks, self.headlines = [], [], [], []
        self.body_count = self.thesis_count = 0
        self.feed(source)
        self.close()
        if self.body_count != 1 or self.thesis_count != 1 or len(self.headlines) != 1 or not self.blocks:
            raise ValueError('Each essay needs one H1, one #essay-body and one thesis paragraph')

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if tag == 'br':
            for _, _, parts in self.frames:
                parts.append(' ')
        if tag in VOID:
            return
        self.stack.append((tag, attrs))
        in_main = any(t == 'main' for t, _ in self.stack)
        in_body = any(a.get('id') == 'essay-body' for _, a in self.stack)
        if attrs.get('id') == 'essay-body':
            self.body_count += 1
        if in_body and tag == 'p' and 'essay-thesis' in attrs.get('class', '').split():
            self.thesis_count += 1
        if in_main and tag == 'h1':
            self.frames.append((len(self.stack), 'h1', []))
        elif in_body and tag in ('p', 'h2', 'h3', 'li', 'pre'):
            self.frames.append((len(self.stack), tag, []))

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if index is None:
            return
        for depth, kind, parts in self.frames:
            if depth > index:
                text = ' '.join(''.join(parts).split())
                if kind == 'h1':
                    self.headlines.append(text)
                elif text:
                    self.blocks.append((kind, text))
        self.frames = [frame for frame in self.frames if frame[0] <= index]
        del self.stack[index:]

    def handle_data(self, data):
        for _, _, parts in self.frames:
            parts.append(data)

    @property
    def body(self):
        return '\n\n'.join(text for _, text in self.blocks)


def dump(data):
    return json.dumps(data, ensure_ascii=False, separators=(',', ':')).replace('</', '<\\/')


def url(name):
    if name == 'index.html':
        return DOMAIN
    return DOMAIN + (name[:-len('index.html')] if name.endswith('/index.html') else name)


def markdown_path(name):
    return name[:-len('index.html')] + 'index.md'


def modified(cfg):
    return cfg.get('modified', cfg.get('article', {}).get('modified', DATE))


def checked_date(value):
    if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
        raise ValueError('Editorial dates must have YYYY-MM-DD precision')
    date.fromisoformat(value)
    return value


def essay_order():
    names = [name for name, cfg in CFG['pages'].items() if 'article' in cfg]
    for name in names:
        article = CFG['pages'][name]['article']
        if checked_date(article['published']) > checked_date(article['modified']):
            raise ValueError(name + ': modification precedes publication')
        if modified(CFG['pages'][name]) != article['modified']:
            raise ValueError(name + ': page and article modification dates differ')
    return sorted(names, key=lambda name: CFG['pages'][name]['article']['published'], reverse=True)


def breadcrumbs(name, cfg):
    entries = [('Home', DOMAIN)]
    if name == ARCHIVE:
        entries.append(('Essays', url(ARCHIVE)))
    elif 'article' in cfg:
        entries += [('Essays', url(ARCHIVE)), (cfg['label'], url(name))]
    else:
        return None
    return {'@type': 'BreadcrumbList', '@id': url(name) + '#breadcrumbs',
            'itemListElement': [{'@type': 'ListItem', 'position': i, 'name': label, 'item': target}
                                for i, (label, target) in enumerate(entries, 1)]}


def page_nodes(name, cfg, essays, order):
    canonical = url(name)
    page = {'@type': cfg['schemaType'], '@id': canonical + '#webpage', 'url': canonical,
            'name': cfg['title'], 'description': cfg['description'], 'inLanguage': 'en',
            'dateModified': checked_date(modified(cfg)), 'isPartOf': {'@id': DOMAIN + '#website'},
            'about': {'@id': DOMAIN + '#person'}}
    nodes = [page]
    if name == 'about.html':
        page['mainEntity'] = {'@id': DOMAIN + '#person'}
    if 'service' in cfg:
        nodes.append(copy.deepcopy(cfg['service']))
        page['mainEntity'] = {'@id': cfg['service']['@id']}
    if name == 'century.html':
        nodes.append(copy.deepcopy(CFG['century']))
        page['mainEntity'] = {'@id': CFG['century']['@id']}
    if name == 'sources.html':
        page['citation'] = [record['url'] for record in CFG['person'].get('subjectOf', [])]
    crumb = breadcrumbs(name, cfg)
    if crumb:
        page['breadcrumb'] = {'@id': crumb['@id']}
        nodes.append(crumb)
    if name == ARCHIVE:
        page['mainEntity'] = {'@id': canonical + '#articles'}
        page['hasPart'] = [{'@id': url(path) + '#article'} for path in order]
        nodes.append({'@type': 'ItemList', '@id': canonical + '#articles',
                      'numberOfItems': len(order), 'itemListOrder': 'https://schema.org/ItemListOrderDescending',
                      'itemListElement': [{'@type': 'ListItem', 'position': i,
                                           'name': essays[path].headlines[0], 'url': url(path)}
                                          for i, path in enumerate(order, 1)]})
    if 'article' in cfg:
        source, article = essays[name], cfg['article']
        if source.headlines[0] != cfg['label']:
            raise ValueError(name + ': visible H1 differs from the configured article title')
        page['mainEntity'] = {'@id': canonical + '#article'}
        page['isPartOf'] = {'@id': url(ARCHIVE) + '#webpage'}
        page['datePublished'] = article['published']
        nodes.append({'@type': 'Article', '@id': canonical + '#article', 'url': canonical,
                      'headline': source.headlines[0], 'description': cfg['description'],
                      'image': cfg['socialImage'], 'inLanguage': 'en',
                      'datePublished': article['published'], 'dateModified': article['modified'],
                      'author': {'@id': DOMAIN + '#person'}, 'publisher': {'@id': DOMAIN + '#person'},
                      'mainEntityOfPage': {'@id': canonical + '#webpage'},
                      'isPartOf': {'@id': url(ARCHIVE) + '#webpage'}, 'keywords': article.get('keywords', []),
                      'articleBody': source.body,
                      'wordCount': len(re.findall(r"\b\w+(?:[-’']\w+)*\b", source.body))})
    return nodes


def metadata(name, cfg, nodes, archive_nodes):
    canonical = url(name)
    escape = lambda value: html.escape(value, quote=True)
    prefix = '/' if '/' in name else ''
    asset = lambda path: prefix + 'assets/' + path
    root_link = lambda path: prefix + path
    lines = ['<meta charset="utf-8" />', '<meta name="viewport" content="width=device-width, initial-scale=1" />',
             '<meta name="yandex-verification" content="c3fd18a00a5bf714" />',
             '<script>document.documentElement.classList.add("js");</script>',
             f'<link rel="preload" href="{asset("executive/PlayfairDisplay.woff2")}" as="font" type="font/woff2" crossorigin />',
             f'<link rel="preload" href="{asset("executive/DMSans.woff2")}" as="font" type="font/woff2" crossorigin />']
    if name in ('index.html', 'about.html'):
        lines += ['<link rel="preload" as="image" href="assets/portraits/vadim-home-720.webp" type="image/webp" fetchpriority="high" />',
                  '<link rel="preload" as="image" href="assets/executive/horizon.webp" type="image/webp" fetchpriority="high" />']
    hero_photos = {'work.html': 'architecture', 'enterprise.html': 'architecture',
                   'founders.html': 'workspace', 'expert.html': 'workspace'}
    if name in hero_photos:
        photo = hero_photos[name]
        lines.append(f'<link rel="preload" as="image" href="assets/executive/{photo}.webp" imagesrcset="assets/executive/{photo}-640.webp 640w, assets/executive/{photo}-768.webp 768w, assets/executive/{photo}.webp 1000w" imagesizes="(max-width: 760px) calc(100vw - 40px), (max-width: 1100px) 45vw, 600px" type="image/webp" fetchpriority="high" />')
    if name == '404.html':
        lines.insert(1, '<base href="/" />')
    stylesheet = asset('site.css') + '?v=' + CFG['assetsVersion']
    lines.append(f'<link rel="stylesheet" href="{stylesheet}" />')
    if name != 'index.html':
        lines.append(f'<link rel="stylesheet" href="{asset("internal.css")}" />')
    if name == ARCHIVE or 'article' in cfg:
        lines.append('<link rel="stylesheet" href="/assets/essays.css" />')
    lines += [f'<title>{escape(cfg["title"])}</title>',
              f'<meta name="description" content="{escape(cfg["description"])}" />',
              '<meta name="author" content="Vadim Vladymtsev" />', '<meta name="theme-color" content="#080c0e" />',
              '<meta name="robots" content="' + ('noindex,follow' if name == '404.html' else 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1') + '" />']
    if name != '404.html':
        lines += [f'<link rel="canonical" href="{canonical}" />',
                  f'<link rel="alternate" hreflang="en" href="{canonical}" />',
                  f'<link rel="alternate" hreflang="x-default" href="{canonical}" />']
    lines += [f'<meta property="og:type" content="{"article" if "article" in cfg else "website"}" />',
              '<meta property="og:site_name" content="Vadim Vladymtsev" />', '<meta property="og:locale" content="en_US" />']
    for prop, value in [('title', cfg['title']), ('description', cfg['description']), ('url', canonical),
                        ('image', cfg['socialImage']), ('image:type', 'image/jpeg' if cfg['socialImage'].endswith('.jpg') else 'image/png'),
                        ('image:width', '1200'), ('image:height', '630'), ('image:alt', cfg['label'] + ' — Vadim Vladymtsev')]:
        lines.append(f'<meta property="og:{prop}" content="{escape(value)}" />')
    if 'article' in cfg:
        for prop, value in [('published_time', cfg['article']['published']),
                            ('modified_time', cfg['article']['modified']), ('author', DOMAIN + 'about.html')]:
            lines.append(f'<meta property="article:{prop}" content="{escape(value)}" />')
        lines.append('<link rel="author" href="/about.html" />')
    for prop, value in [('card', 'summary_large_image'), ('title', cfg['title']), ('description', cfg['description']),
                        ('image', cfg['socialImage']), ('image:alt', cfg['label'] + ' — Vadim Vladymtsev')]:
        lines.append(f'<meta name="twitter:{prop}" content="{escape(value)}" />')
    lines += [f'<link rel="icon" href="{asset("favicon.svg")}" type="image/svg+xml" />',
              f'<link rel="icon" href="{asset("favicon-32.png")}" sizes="32x32" type="image/png" />',
              f'<link rel="apple-touch-icon" href="{asset("favicon-180.png")}" />',
              f'<link rel="describedby" href="{root_link("llms.txt")}" type="text/plain" />',
              f'<link rel="describedby" href="{root_link("data/entity-graph.json")}" type="application/ld+json" />',
              f'<link rel="describedby" href="{root_link("ai.json")}" type="application/json" />']
    if name == ARCHIVE or 'article' in cfg:
        lines += [f'<link rel="alternate" type="text/markdown" href="/{markdown_path(name)}" />',
                  '<link rel="describedby" type="text/plain" href="/essays/llms.txt" />',
                  '<link rel="alternate" type="application/rss+xml" title="Essays — Vadim Vladymtsev" href="/essays/feed.xml" />']
    graph = copy.deepcopy(CFG['core'])
    if 'article' in cfg:
        graph += copy.deepcopy(archive_nodes)
    graph += copy.deepcopy(nodes)
    lines.append('<script type="application/ld+json">' + dump({'@context': 'https://schema.org', '@graph': graph}) + '</script>')
    return '<head>\n' + '\n'.join(lines) + '\n</head>'


def feed(order, essays):
    atom, dc = 'http://www.w3.org/2005/Atom', 'http://purl.org/dc/elements/1.1/'
    ET.register_namespace('atom', atom)
    ET.register_namespace('dc', dc)
    rss = ET.Element('rss', {'version': '2.0'})
    channel = ET.SubElement(rss, 'channel')
    for key, value in [('title', 'Essays — Vadim Vladymtsev'), ('link', url(ARCHIVE)),
                       ('description', CFG['pages'][ARCHIVE]['description']), ('language', 'en')]:
        ET.SubElement(channel, key).text = value
    ET.SubElement(channel, '{' + atom + '}link',
                  {'href': DOMAIN + 'essays/feed.xml', 'rel': 'self', 'type': 'application/rss+xml'})
    for name in order:
        cfg = CFG['pages'][name]
        item = ET.SubElement(channel, 'item')
        for key, value in [('title', essays[name].headlines[0]), ('link', url(name)), ('description', cfg['description'])]:
            ET.SubElement(item, key).text = value
        ET.SubElement(item, 'guid', {'isPermaLink': 'true'}).text = url(name)
        ET.SubElement(item, '{' + dc + '}date').text = cfg['article']['published']
    ET.indent(rss, space='  ')
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + ET.tostring(rss, encoding='unicode') + '\n'


def public_profiles():
    # sameAs is the approved identity list in the editorial configuration.
    return [(urlsplit(target).hostname.removeprefix('www.'), target)
            for target in CFG['person'].get('sameAs', [])]


def outputs():
    sources = {name: (ROOT / name).read_text() for name in CFG['pages']}
    order = essay_order()
    essays = {name: EssaySource(sources[name]) for name in order}
    nodes = {name: page_nodes(name, cfg, essays, order) for name, cfg in CFG['pages'].items()}
    out = {}
    full = ['# Vadim Vladymtsev — public site text', '', f'Canonical website: {DOMAIN}',
            f'Content updated: {DATE}', '',
            'This document is generated from the visible English site. Links and the human-readable pages are authoritative. It does not establish offices, client engagements or personal presence in a country.', '']
    for name, cfg in CFG['pages'].items():
        text = sources[name]
        out[name] = re.sub(r'<head>[\s\S]*?</head>', lambda match: metadata(name, cfg, nodes[name], nodes.get(ARCHIVE, [])), text, count=1)
        if name == '404.html':
            continue
        full += [f'## {cfg["label"]}', url(name), '']
        if name in essays:
            source, article = essays[name], cfg['article']
            full += ['Author: Vadim Vladymtsev', 'Published: ' + article['published'],
                     'Updated: ' + article['modified'], '', source.body, '']
            md = ['# ' + source.headlines[0], '', 'Author: [Vadim Vladymtsev](' + DOMAIN + 'about.html)',
                  'Published: ' + article['published'], 'Updated: ' + article['modified'],
                  'Canonical: ' + url(name), '']
            for tag, block in source.blocks:
                md += [(('## ' if tag == 'h2' else '### ') + block) if tag in ('h2', 'h3')
                       else ('- ' + block if tag == 'li' else block), '']
            out[markdown_path(name)] = '\n'.join(md).rstrip() + '\n'
        else:
            parser = Blocks()
            parser.feed(text)
            for tag, block in parser.blocks:
                if tag in ('h1', 'h2', 'h3'):
                    full += ['### ' + block, '']
                elif tag == 'li':
                    full += ['- ' + block]
                elif tag != 'summary':
                    full += [block, '']
    core = copy.deepcopy(CFG['core'])
    core.append(copy.deepcopy(CFG['century']))
    for name, graph in nodes.items():
        if name != '404.html':
            core += graph
    # Century and other referenced nodes retain one authoritative definition.
    unique = {node['@id']: node for node in core}
    out['data/entity-graph.json'] = json.dumps({'@context': 'https://schema.org', '@graph': list(unique.values())}, ensure_ascii=False, indent=2) + '\n'
    intro = '# Vadim Vladymtsev\n\n> Enterprise AI CTO and product operator. CTO at StackLevel Group.\n\nEnglish-language enterprise AI, technical due diligence and CTO advisory for audiences in the United States and the United Arab Emirates (UAE). Geographic focus is not a claim of offices or residence.\n\n'
    index = intro + '## Canonical pages\n\n'
    for name, cfg in CFG['pages'].items():
        if name != '404.html':
            index += f'- [{cfg["label"]}]({url(name)}): {cfg["description"]}\n'
    index += '\n## Public profiles and product\n\n'
    for label, target in public_profiles():
        index += f'- [{label}]({target})\n'
    index += f'- [{CFG["century"]["name"]}]({CFG["century"]["url"]})\n'
    supporting = [('Profile summary', 'ai-profile.md'), ('Full public site text', 'llms-full.txt'),
                  ('Structured entity graph', 'data/entity-graph.json'), ('Discovery catalog', 'ai.json')]
    if order:
        supporting += [('Essays reading index', 'essays/llms.txt'), ('Essays RSS feed', 'essays/feed.xml')]
        archive_md = ['# Essays', '', CFG['pages'][ARCHIVE]['description'], '', 'Canonical: ' + url(ARCHIVE), '']
        scoped = ['# Essays by Vadim Vladymtsev', '', '- [Archive](' + url(ARCHIVE) + ')',
                  '- [Archive Markdown](' + DOMAIN + markdown_path(ARCHIVE) + ')',
                  '- [RSS feed](' + DOMAIN + 'essays/feed.xml)',
                  '- [Discovery catalog](' + DOMAIN + 'ai.json)', '']
        for name in order:
            cfg = CFG['pages'][name]
            archive_md += ['## [' + cfg['label'] + '](' + url(name) + ')', '',
                           'Published: ' + cfg['article']['published'], '', cfg['description'], '',
                           '[Full text in Markdown](' + DOMAIN + markdown_path(name) + ')', '']
            scoped.append(f'- [{cfg["label"]}]({DOMAIN}{markdown_path(name)}): {cfg["article"]["published"]}. {cfg["description"]}')
        out[markdown_path(ARCHIVE)] = '\n'.join(archive_md).rstrip() + '\n'
        out['essays/llms.txt'] = '\n'.join(scoped).rstrip() + '\n'
        out['essays/feed.xml'] = feed(order, essays)
    index += '\n## Supporting documents\n\n'
    for label, path in supporting:
        index += f'- [{label}]({DOMAIN}{path})\n'
    out['llms.txt'] = index
    profile = intro + '## Work and inquiry types\n\n'
    for name, cfg in CFG['pages'].items():
        if 'service' in cfg:
            profile += f'### {cfg["service"]["name"]}\n\n{cfg["description"]}\n\n{url(name)}\n\n'
    profile += '## Product context\n\n' + CFG['century']['description'] + '\n\n' + DOMAIN + 'century.html\n\n## Public record\n\n'
    for record in CFG['person'].get('subjectOf', []):
        profile += '- ' + record['name'] + ' — ' + record.get('datePublished', record.get('startDate', '')) + ' — ' + record['url'] + '\n'
    profile += '\n## Identity and contact\n\n' + DOMAIN + 'about.html#contact\n\n'
    for label, target in public_profiles():
        profile += f'- [{label}]({target})\n'
    profile += '\nTechnical assessments are not investment, legal or financial advice. Public product recognition is not a personal award.\n'
    out['ai-profile.md'], out['llms-full.txt'] = profile, '\n'.join(full).rstrip() + '\n'
    catalog = {'schemaVersion': 1, 'site': DOMAIN, 'name': 'Vadim Vladymtsev', 'inLanguage': 'en',
               'documents': [], 'discovery': {path: DOMAIN + path for _, path in supporting if path != 'ai.json'}}
    catalog['discovery']['llms.txt'] = DOMAIN + 'llms.txt'
    for name, cfg in CFG['pages'].items():
        if name == '404.html':
            continue
        entry = {'url': url(name), 'title': cfg['label'], 'description': cfg['description'],
                 'type': 'Article' if name in essays else cfg['schemaType'], 'dateModified': modified(cfg)}
        if name in essays:
            entry['datePublished'] = cfg['article']['published']
        if name == ARCHIVE or name in essays:
            entry['markdown'] = DOMAIN + markdown_path(name)
        catalog['documents'].append(entry)
    out['ai.json'] = json.dumps(catalog, ensure_ascii=False, indent=2) + '\n'
    pre = '<?xml version="1.0" encoding="UTF-8"?>\n'
    esc = lambda value: html.escape(value, quote=False)
    entries = [f'  <url><loc>{url(name)}</loc><lastmod>{modified(cfg)}</lastmod></url>'
               for name, cfg in CFG['pages'].items() if name != '404.html']
    out['sitemap.xml'] = pre + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + '\n'.join(entries) + '\n</urlset>\n'
    entries = []
    for name, cfg in CFG['pages'].items():
        if name == '404.html':
            continue
        images = [cfg['socialImage']]
        if name in ('index.html', 'about.html'):
            images.append(DOMAIN + 'assets/portraits/vadim-home-720.webp')
        entries.append(f'  <url><loc>{url(name)}</loc><lastmod>{modified(cfg)}</lastmod>'
                       + ''.join('<image:image><image:loc>' + esc(image) + '</image:loc></image:image>' for image in images) + '</url>')
    out['sitemap-images.xml'] = pre + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n' + '\n'.join(entries) + '\n</urlset>\n'
    ai_paths = {path: DATE for path in ['llms.txt', 'llms-full.txt', 'ai-profile.md', 'data/entity-graph.json', 'ai.json']}
    if order:
        ai_paths.update({path: modified(CFG['pages'][ARCHIVE]) for path in ['essays/llms.txt', 'essays/feed.xml', markdown_path(ARCHIVE)]})
        ai_paths.update({markdown_path(name): modified(CFG['pages'][name]) for name in order})
    out['sitemap-ai.xml'] = pre + '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + ''.join(
        f'  <url><loc>{DOMAIN}{path}</loc><lastmod>{stamp}</lastmod></url>\n' for path, stamp in ai_paths.items()) + '</urlset>\n'
    return out


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--check', action='store_true')
    group.add_argument('--write', action='store_true')
    args = parser.parse_args()
    generated, changed = outputs(), []
    for name, text in generated.items():
        path = ROOT / name
        if not path.exists() or path.read_text() != text:
            changed.append(name)
            if args.write:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
    if args.check and changed:
        raise SystemExit('Discovery output is stale: ' + ', '.join(changed))
    print(('Updated' if args.write else 'PASS — generated discovery:') + ' '
          + str(len(changed) if args.write else len(generated)) + ' files')
