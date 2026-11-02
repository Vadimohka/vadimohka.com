#!/usr/bin/env python3
"""Offline health checks for configured pages, essays and public discovery files."""
import argparse
import html
import json
import re
import subprocess
import sys
import xml.etree.ElementTree as ET
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urljoin, urlsplit
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
CFG = json.loads((ROOT / 'qa/health/search-config.json').read_text())
DOMAIN = CFG['baseURL']
HOST = urlsplit(DOMAIN).hostname
ARCHIVE = 'essays/index.html'
TODAY = datetime.now(ZoneInfo('Europe/Minsk')).date()
VOID = {'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 'link', 'meta', 'param', 'source', 'track', 'wbr'}
errors = []


def check(ok, message):
    if not ok:
        errors.append(message)


def canonical(name):
    if name == 'index.html':
        return DOMAIN
    return DOMAIN + (name[:-10] if name.endswith('/index.html') else name)


def md_path(name):
    return name[:-10] + 'index.md'


def modified(cfg):
    return cfg.get('modified', cfg.get('article', {}).get('modified', CFG['modified']))


def local_path(value, base=DOMAIN):
    target = urlsplit(urljoin(base, value))
    if target.scheme not in ('http', 'https') or target.hostname != HOST:
        return None, target
    path = unquote(target.path).lstrip('/')
    if not path or path.endswith('/'):
        path += 'index.html'
    return path, target


def date_value(value, label):
    from datetime import date
    try:
        if not isinstance(value, str) or not re.fullmatch(r'\d{4}-\d{2}-\d{2}', value):
            raise ValueError('Expected YYYY-MM-DD')
        stamp = date.fromisoformat(value)
        check(stamp <= TODAY, label + ': future editorial date in Europe/Minsk')
        return stamp
    except ValueError:
        check(False, label + ': invalid date')
        return None


def date_label(value):
    from datetime import date
    stamp = date.fromisoformat(value)
    months = ('January', 'February', 'March', 'April', 'May', 'June',
              'July', 'August', 'September', 'October', 'November', 'December')
    return f'{stamp.day} {months[stamp.month - 1]} {stamp.year}'


class Page(HTMLParser):
    """Independent extraction of visible text, dates, cards and HTML relations."""
    def __init__(self, text):
        super().__init__(convert_charrefs=True)
        self.ids, self.links, self.references, self.images = set(), [], [], []
        self.metas, self.hreflang = {}, {}
        self.preloads, self.head_links, self.headings = [], [], []
        self.canonical = self.base = None
        self.stack, self.captures, self.card_frames = [], [], []
        self.h1, self.body_blocks, self.body_links, self.times, self.cards = [], [], [], [], []
        self.modified_times = []
        self.body_count = self.thesis_count = 0
        self.raw_graphs = re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>', text)
        self.graph = []
        for raw in self.raw_graphs:
            data = json.loads(raw)
            self.graph.extend(data.get('@graph', [data]))
        title = re.search(r'<title>(.*?)</title>', text, re.S)
        self.title = html.unescape(title[1]) if title else None
        self.feed(text)
        self.close()

    def handle_starttag(self, tag, pairs):
        attrs = dict(pairs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag == 'a' and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag == 'img':
            self.images.append(attrs)
        if tag == 'meta':
            self.metas[attrs.get('name', attrs.get('property'))] = attrs.get('content')
        if tag == 'base':
            self.base = attrs.get('href')
        if tag == 'link':
            self.head_links.append(attrs)
            if attrs.get('rel') == 'canonical':
                self.canonical = attrs.get('href')
            if attrs.get('hreflang'):
                self.hreflang[attrs['hreflang']] = attrs['href']
            if attrs.get('rel') == 'preload':
                self.preloads.append(attrs)
        for key in ('href', 'src', 'poster'):
            if attrs.get(key) and tag != 'base':
                self.references.append(attrs[key])
        if tag in ('h1', 'h2', 'h3', 'h4'):
            self.headings.append(tag)
        if tag == 'br':
            for _, _, _, parts in self.captures:
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
        if in_main and tag == 'article' and 'essay-card' in attrs.get('class', '').split():
            self.card_frames.append((len(self.stack), {'links': [], 'times': []}))
        card = self.card_frames[-1][1] if self.card_frames else None
        if in_main and tag == 'h1':
            self.captures.append((len(self.stack), 'h1', None, []))
        elif in_body and tag in ('p', 'h2', 'h3', 'li', 'pre'):
            self.captures.append((len(self.stack), 'body', None, []))
        if in_body and tag == 'a' and attrs.get('href'):
            self.body_links.append(attrs['href'])
        if in_main and tag == 'time' and (card is not None or 'essay-date' in attrs.get('class', '').split()):
            self.captures.append((len(self.stack), 'time', (attrs.get('datetime'), card), []))
        elif in_main and tag == 'time' and any('essay-updated' in a.get('class', '').split() for _, a in self.stack):
            self.captures.append((len(self.stack), 'modified-time', attrs.get('datetime'), []))
        if card is not None and tag == 'a' and attrs.get('href') and any(t == 'h2' for t, _ in self.stack):
            self.captures.append((len(self.stack), 'card-link', (attrs['href'], card), []))

    def handle_endtag(self, tag):
        index = next((i for i in range(len(self.stack) - 1, -1, -1) if self.stack[i][0] == tag), None)
        if index is None:
            return
        for depth, kind, owner, parts in self.captures:
            if depth <= index:
                continue
            text = ' '.join(''.join(parts).split())
            if kind == 'h1':
                self.h1.append(text)
            elif kind == 'body' and text:
                self.body_blocks.append(text)
            elif kind == 'time':
                stamp, card = owner
                (self.times if card is None else card['times']).append((stamp, text))
            elif kind == 'modified-time':
                self.modified_times.append((owner, text))
            elif kind == 'card-link':
                target, card = owner
                card['links'].append((target, text))
        self.captures = [capture for capture in self.captures if capture[0] <= index]
        for depth, card in self.card_frames:
            if depth > index:
                self.cards.append(card)
        self.card_frames = [frame for frame in self.card_frames if frame[0] <= index]
        del self.stack[index:]

    def handle_data(self, text):
        for _, _, _, parts in self.captures:
            parts.append(text)


def node(graph, identifier, kind, label):
    matches = [entry for entry in graph if entry.get('@id') == identifier]
    check(len(matches) == 1 and matches[0].get('@type') == kind, label + ': missing, duplicated or mistyped ' + identifier)
    return matches[0] if len(matches) == 1 else {}


def relation(page, rel, media, target, base):
    return sum(entry.get('rel') == rel and entry.get('type') == media
               and urljoin(base, entry.get('href', '')) == target for entry in page.head_links) == 1


def public_documents():
    names = set(CFG['pages']) | {'robots.txt', 'humans.txt', 'llms.txt', 'llms-full.txt', 'ai-profile.md',
                                'ai.json', 'sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml'}
    for folder in ('assets', 'data', 'essays'):
        names.update(path.relative_to(ROOT).as_posix() for path in (ROOT / folder).rglob('*') if path.is_file())
    return [ROOT / name for name in names if (ROOT / name).suffix.lower()
            in {'.html', '.md', '.txt', '.json', '.jsonld', '.xml', '.css', '.js', '.svg'}]


def check_public_urls(paths):
    blocked = {'vaiti.io', 'stepik.org', 'stacklevel.group'}
    for path in paths:
        if not path.is_file():
            check(False, str(path.relative_to(ROOT)) + ': missing public document')
            continue
        source = html.unescape(path.read_text()).replace('\\/', '/')
        for value in re.findall(r'(?:https?:)?//[^\s<>"\'()\\]+', source):
            target = urlsplit('https:' + value if value.startswith('//') else value)
            host = (target.hostname or '').lower()
            denied = host.endswith(('.ru', '.by', '.su', '.xn--p1ai')) or any(
                host == domain or host.endswith('.' + domain) for domain in blocked)
            denied |= host in ('instagram.com', 'www.instagram.com') and target.path.rstrip('/') == '/p/DW7GULsDNwq'
            check(not denied, str(path.relative_to(ROOT)) + ': removed regional source URL remains: ' + value)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--published-dir', type=Path, help='Also inspect the actual packaged public documents')
    args = parser.parse_args()
    pages = {name: Page((ROOT / name).read_text()) for name in CFG['pages']}
    actual_html = {path.relative_to(ROOT).as_posix() for path in ROOT.glob('*.html')}
    actual_html.update(path.relative_to(ROOT).as_posix() for path in (ROOT / 'essays').rglob('*.html'))
    check(actual_html == set(pages), 'Configured routes do not cover every published HTML page')
    global_graph = json.loads((ROOT / 'data/entity-graph.json').read_text())['@graph']
    global_ids = {entry.get('@id') for entry in global_graph}
    check(len(global_ids) == len(global_graph), 'Entity graph contains duplicate IDs')
    persons, titles, descriptions = [], [], []
    for name, page in pages.items():
        cfg, target = CFG['pages'][name], canonical(name)
        base = urljoin(target, page.base) if page.base else target
        titles.append(page.title)
        descriptions.append(page.metas.get('description'))
        check(page.headings.count('h1') == 1, name + ': exactly one H1 required')
        check(page.title == cfg['title'] and page.metas.get('description') == cfg['description'], name + ': editorial metadata differs')
        check(page.metas.get('og:locale') == 'en_US', name + ': English social locale')
        if name == '404.html':
            check('noindex' in page.metas.get('robots', '') and page.base == '/', name + ': noindex + root base required')
        else:
            check(page.canonical == target, name + ': canonical mismatch')
            check(page.hreflang == {'en': target, 'x-default': target}, name + ': invalid/nonexistent locale alternates')
            check('max-image-preview:large' in page.metas.get('robots', ''), name + ': preview visibility')
        check(page.metas.get('og:url') == target and page.metas.get('og:image') == cfg['socialImage'], name + ': social URL/image mismatch')
        check(relation(page, 'describedby', 'application/json', DOMAIN + 'ai.json', base), name + ': ai.json is not discoverable')
        for link in page.references:
            path, resolved = local_path(link, base)
            if path is None:
                continue
            check((ROOT / path).is_file(), f'{name}: broken local destination {link}')
            if resolved.fragment and path in pages:
                check(unquote(resolved.fragment) in pages[path].ids, f'{name}: missing anchor {link}')
        for image in page.images:
            check('alt' in image and int(image.get('width', 0)) > 0 and int(image.get('height', 0)) > 0,
                  name + ': image semantics/dimensions missing')
            if image.get('srcset'):
                check(bool(image.get('sizes')), name + ': srcset without sizes')
                for candidate in image['srcset'].split(','):
                    src, width = candidate.strip().split()
                    path, _ = local_path(src, base)
                    check(path is not None and (ROOT / path).is_file() and re.fullmatch(r'\d+w', width),
                          name + ': invalid image candidate ' + candidate)
            if 'section-backdrop' in image.get('class', ''):
                check(image.get('loading') == 'lazy', name + ': below-fold backdrop loaded eagerly')
        check(sum(entry.get('as') == 'font' for entry in page.preloads) == 2, name + ': fonts not discoverable in head')
        local_ids = {entry.get('@id') for entry in page.graph}
        check(len(local_ids) == len(page.graph), name + ': duplicate schema IDs')
        person = node(page.graph, DOMAIN + '#person', 'Person', name)
        persons.append(person)
        check(person == CFG['person'], name + ': Person differs from editorial configuration')
        check(not any(key in person for key in ('areaServed', 'address', 'location')), name + ': unsupported Person geography')
        check(person.get('image') == DOMAIN + 'assets/portraits/vadim-home-720.webp', name + ': inconsistent identity photograph')
        check(not any('&amp;' in raw for raw in page.raw_graphs), name + ': HTML escaping inside JSON-LD URL')
        for entry in page.graph:
            check(not any(key in entry for key in ('aggregateRating', 'review', 'priceRange')), name + ': unsupported reputation/price claim')
            if entry.get('@type') == 'Service':
                check({market['name'] for market in entry['areaServed']} == {'United States', 'United Arab Emirates'},
                      name + ': service markets mismatch')
            for rel in ('provider', 'isPartOf', 'publisher', 'worksFor', 'about', 'mainEntity', 'mainEntityOfPage', 'author', 'breadcrumb'):
                value = entry.get(rel)
                if isinstance(value, dict) and '@id' in value:
                    check(value['@id'] in local_ids | global_ids, name + ': dangling ' + rel + ' reference')
            if entry.get('@type') == 'ProfilePage':
                check(entry.get('mainEntity', {}).get('@id') == DOMAIN + '#person', name + ': invalid profile identity')
        webpage = node(page.graph, target + '#webpage', cfg['schemaType'], name)
        check(webpage.get('dateModified') == modified(cfg), name + ': WebPage modification date differs')
        date_value(webpage.get('dateModified'), name)
        if name != '404.html':
            check(node(global_graph, target + '#webpage', cfg['schemaType'], name) == webpage,
                  name + ': entity graph page differs from inline schema')
    check(len(set(titles)) == len(titles), 'duplicate titles')
    check(len(set(descriptions)) == len(descriptions), 'duplicate descriptions')
    check(all(person == persons[0] for person in persons), 'Person facts drift across pages')
    check(node(global_graph, DOMAIN + '#person', 'Person', 'entity graph') == persons[0], 'external entity graph differs')

    essays = [name for name, cfg in CFG['pages'].items() if 'article' in cfg]
    ordered = sorted(essays, key=lambda name: CFG['pages'][name]['article']['published'], reverse=True)
    full = (ROOT / 'llms-full.txt').read_text()
    for name in essays:
        cfg, page, target = CFG['pages'][name], pages[name], canonical(name)
        article_cfg = cfg['article']
        article = node(page.graph, target + '#article', 'Article', name)
        webpage = node(page.graph, target + '#webpage', 'WebPage', name)
        body = '\n\n'.join(page.body_blocks)
        check(page.body_count == 1 and page.thesis_count == 1 and bool(body), name + ': missing thesis/prose container')
        check(page.h1 == [cfg['label']] and article.get('headline') == cfg['label'], name + ': essay headline mismatch')
        check(article.get('articleBody') == body, name + ': Article differs from visible thesis and prose')
        check(article.get('wordCount') == len(re.findall(r"\b\w+(?:[-’']\w+)*\b", body)), name + ': Article word count differs')
        check(article.get('author') == {'@id': DOMAIN + '#person'} and article.get('publisher') == {'@id': DOMAIN + '#person'},
              name + ': incorrect article attribution')
        check(article.get('mainEntityOfPage') == {'@id': target + '#webpage'}
              and webpage.get('mainEntity') == {'@id': target + '#article'}
              and article.get('isPartOf') == {'@id': canonical(ARCHIVE) + '#webpage'}
              and webpage.get('isPartOf') == {'@id': canonical(ARCHIVE) + '#webpage'}, name + ': article/page/archive relationships differ')
        for field, config_key in (('datePublished', 'published'), ('dateModified', 'modified')):
            check(article.get(field) == webpage.get(field) == article_cfg[config_key], name + ': article dates differ')
            date_value(article.get(field), name + ' ' + field)
        check(article_cfg['published'] <= article_cfg['modified'], name + ': invalid publication chronology')
        check(page.times == [(article_cfg['published'], date_label(article_cfg['published']))], name + ': visible essay date/label differs')
        check(page.modified_times == [(article_cfg['modified'], date_label(article_cfg['modified']))], name + ': visible updated date/label differs')
        check(page.metas.get('og:type') == 'article'
              and page.metas.get('article:published_time') == article_cfg['published']
              and page.metas.get('article:modified_time') == article_cfg['modified']
              and page.metas.get('article:author') == DOMAIN + 'about.html', name + ': article social metadata differs')
        expected_crumbs = [{'@type': 'ListItem', 'position': position, 'name': label, 'item': link}
                           for position, (label, link) in enumerate(
                               [('Home', DOMAIN), ('Essays', canonical(ARCHIVE)), (cfg['label'], target)], 1)]
        crumb = node(page.graph, target + '#breadcrumbs', 'BreadcrumbList', name)
        check(crumb.get('itemListElement') == expected_crumbs, name + ': essay breadcrumbs differ')
        check(node(global_graph, target + '#article', 'Article', name) == article, name + ': global Article differs')
        check('citation' not in article and not any(local_path(link, target)[0] is None for link in page.body_links),
              name + ': external source/citation inside essay prose')
        check(relation(page, 'alternate', 'text/markdown', DOMAIN + md_path(name), target), name + ': missing Markdown relation')
        check(relation(page, 'alternate', 'application/rss+xml', DOMAIN + 'essays/feed.xml', target), name + ': missing RSS relation')
        check(relation(page, 'describedby', 'text/plain', DOMAIN + 'essays/llms.txt', target), name + ': missing scoped index')
        markdown = (ROOT / md_path(name)).read_text()
        check(markdown.startswith('# ' + cfg['label'] + '\n') and body + '\n' in markdown, name + ': Markdown loses essay text')
        for required in ('Author: [Vadim Vladymtsev](' + DOMAIN + 'about.html)',
                         'Published: ' + article_cfg['published'], 'Updated: ' + article_cfg['modified'], 'Canonical: ' + target):
            check(required in markdown, name + ': Markdown metadata differs')
        check(target in full and body in full, name + ': full LLM corpus loses essay text')

    if essays:
        archive, archive_url = pages[ARCHIVE], canonical(ARCHIVE)
        expected_urls = [canonical(name) for name in ordered]
        cards = archive.cards
        check(len(cards) == len(ordered) and all(len(card['links']) == 1 for card in cards), 'Archive needs one linked card per essay')
        card_urls = [urljoin(archive_url, card['links'][0][0]) for card in cards if len(card['links']) == 1]
        check(card_urls == expected_urls, 'Archive is not in publication-date order or has missing/duplicate essays')
        by_url = {canonical(name): name for name in essays}
        for card in cards:
            if len(card['links']) != 1:
                continue
            href, title = card['links'][0]
            name = by_url.get(urljoin(archive_url, href))
            if name is None:
                continue
            cfg = CFG['pages'][name]
            stamp = cfg['article']['published']
            check(title == cfg['label'] and card['times'] == [(stamp, date_label(stamp))], name + ': archive card title/date differs')
        listing = node(archive.graph, archive_url + '#articles', 'ItemList', ARCHIVE)
        expected_items = [{'@type': 'ListItem', 'position': index, 'name': CFG['pages'][name]['label'], 'url': canonical(name)}
                          for index, name in enumerate(ordered, 1)]
        check(listing.get('numberOfItems') == len(ordered) and listing.get('itemListElement') == expected_items, 'Archive ItemList differs')
        collection = node(archive.graph, archive_url + '#webpage', 'CollectionPage', ARCHIVE)
        check(collection.get('mainEntity') == {'@id': archive_url + '#articles'}
              and collection.get('hasPart') == [{'@id': target + '#article'} for target in expected_urls], 'Archive collection relationships differ')
        archive_crumb = node(archive.graph, archive_url + '#breadcrumbs', 'BreadcrumbList', ARCHIVE)
        check(archive_crumb.get('itemListElement') == [
            {'@type': 'ListItem', 'position': 1, 'name': 'Home', 'item': DOMAIN},
            {'@type': 'ListItem', 'position': 2, 'name': 'Essays', 'item': archive_url}], 'Archive breadcrumbs differ')
        check(node(global_graph, archive_url + '#articles', 'ItemList', ARCHIVE) == listing, 'Global archive ItemList differs')
        check(relation(archive, 'alternate', 'text/markdown', DOMAIN + md_path(ARCHIVE), archive_url), 'Archive missing Markdown relation')
        check(relation(archive, 'alternate', 'application/rss+xml', DOMAIN + 'essays/feed.xml', archive_url), 'Archive missing RSS relation')
        feed = ET.parse(ROOT / 'essays/feed.xml').getroot()
        channel = feed.find('channel')
        check(feed.tag == 'rss' and feed.attrib == {'version': '2.0'} and channel is not None, 'Expected RSS 2.0 essay feed')
        if channel is not None:
            check(channel.findtext('link') == archive_url and channel.findtext('language') == 'en'
                  and channel.findtext('title') == 'Essays — Vadim Vladymtsev'
                  and channel.findtext('description') == CFG['pages'][ARCHIVE]['description'], 'RSS archive metadata differs')
            self_link = channel.find('{http://www.w3.org/2005/Atom}link')
            check(self_link is not None and self_link.get('href') == DOMAIN + 'essays/feed.xml'
                  and self_link.get('rel') == 'self', 'RSS missing canonical self link')
            items = channel.findall('item')
            check([item.findtext('link') for item in items] == expected_urls, 'RSS order/inventory differs')
            for item in items:
                name = by_url.get(item.findtext('link'))
                if name is None:
                    continue
                cfg = CFG['pages'][name]
                stamp = item.findall('{http://purl.org/dc/elements/1.1/}date')
                guid = item.find('guid')
                check(item.findtext('title') == cfg['label'] and item.findtext('description') == cfg['description'], name + ': RSS editorial metadata differs')
                check(guid is not None and guid.text == canonical(name) and guid.get('isPermaLink') == 'true', name + ': RSS GUID differs')
                check(len(stamp) == 1 and stamp[0].text == cfg['article']['published'] and item.find('pubDate') is None,
                      name + ': RSS loses date precision or invents a time')

    expected_documents = {canonical(name): name for name in CFG['pages'] if name != '404.html'}
    catalog = json.loads((ROOT / 'ai.json').read_text())
    documents = catalog.get('documents', [])
    check(catalog.get('schemaVersion') == 1 and catalog.get('site') == DOMAIN and catalog.get('inLanguage') == 'en', 'ai.json header differs')
    check(len(documents) == len(expected_documents) and {entry.get('url') for entry in documents} == set(expected_documents),
          'ai.json canonical inventory differs')
    for entry in documents:
        name = expected_documents.get(entry.get('url'))
        if name is None:
            continue
        cfg = CFG['pages'][name]
        check(entry.get('title') == cfg['label'] and entry.get('description') == cfg['description']
              and entry.get('dateModified') == modified(cfg)
              and entry.get('type') == ('Article' if 'article' in cfg else cfg['schemaType']), name + ': ai.json metadata differs')
        if 'article' in cfg:
            check(entry.get('datePublished') == cfg['article']['published'], name + ': ai.json publication date differs')
        if name == ARCHIVE or 'article' in cfg:
            check(entry.get('markdown') == DOMAIN + md_path(name), name + ': ai.json Markdown target differs')
    supporting = ['llms.txt', 'llms-full.txt', 'ai-profile.md', 'data/entity-graph.json']
    if essays:
        supporting += ['essays/llms.txt', 'essays/feed.xml']
    check(catalog.get('discovery') == {path: DOMAIN + path for path in supporting}, 'ai.json supporting discovery links differ')
    reading_paths = ['llms.txt', 'ai-profile.md']
    if essays:
        reading_paths += ['essays/llms.txt', md_path(ARCHIVE), *(md_path(name) for name in essays)]
    for name in reading_paths:
        text = (ROOT / name).read_text()
        for target in re.findall(r'\[[^\]]+\]\(([^)\s]+)\)', text):
            path, _ = local_path(target)
            if path is not None:
                check((ROOT / path).is_file(), name + ': broken Markdown discovery link ' + target)
    root_index = (ROOT / 'llms.txt').read_text()
    for target in [*expected_documents, *(DOMAIN + path for path in supporting if path != 'llms.txt'), DOMAIN + 'ai.json']:
        check('(' + target + ')' in root_index, 'Root llms index misses ' + target)
    if essays:
        scoped = (ROOT / 'essays/llms.txt').read_text()
        for name in essays:
            check('(' + DOMAIN + md_path(name) + ')' in scoped, 'Scoped essays index misses ' + name)

    ns = {'s': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    ai_expected = {DOMAIN + path for path in ['llms.txt', 'llms-full.txt', 'ai-profile.md', 'data/entity-graph.json', 'ai.json']}
    if essays:
        ai_expected |= {DOMAIN + path for path in ['essays/llms.txt', 'essays/feed.xml', md_path(ARCHIVE), *(md_path(name) for name in essays)]}
    for name in ('sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml'):
        text = (ROOT / name).read_text()
        entries = ET.fromstring(text).findall('s:url', ns)
        urls = [entry.findtext('s:loc', namespaces=ns) for entry in entries]
        expected = ai_expected if name == 'sitemap-ai.xml' else set(expected_documents)
        check(len(urls) == len(expected) and set(urls) == expected, name + ': URL inventory differs')
        for entry in entries:
            target = entry.findtext('s:loc', namespaces=ns)
            stamp = entry.findtext('s:lastmod', namespaces=ns)
            date_value(stamp, name)
            path, _ = local_path(target)
            check(path is not None and (ROOT / path).is_file(), name + ': missing URL ' + str(target))
            if target in expected_documents:
                check(stamp == modified(CFG['pages'][expected_documents[target]]), name + ': modification date differs')
        check('image:title' not in text, name + ': deprecated image sitemap field')
    robots = (ROOT / 'robots.txt').read_text()
    for name in ('sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml'):
        check('Sitemap: ' + DOMAIN + name in robots, 'robots missing ' + name)
    for name in ('about.html', 'llms.txt', 'llms-full.txt', 'ai-profile.md', 'data/entity-graph.json'):
        check('frequently works from' not in (ROOT / name).read_text(), name + ': unconfirmed physical-presence claim')
    for name in ('enterprise.html', 'investors.html', 'founders.html'):
        check('United Arab Emirates (UAE)' in (ROOT / name).read_text(), name + ': market context is only hidden in metadata')
    for entry in re.findall(r'<a\b[^>]*class="source-entry[^>]*>', (ROOT / 'sources.html').read_text()):
        check('href="https://vadimohka.com/sources.html#' not in entry, 'source self-reference loop')
    active_paths = [*pages, 'assets/site.css', 'assets/internal.css', 'assets/site.js', 'sitemap-images.xml']
    if (ROOT / 'assets/essays.css').is_file():
        active_paths.append('assets/essays.css')
    active = '\n'.join((ROOT / path).read_text() for path in active_paths)
    for item in json.loads((ROOT / 'qa/health/removed-assets.json').read_text()):
        check(not (ROOT / item['path']).exists() and item['path'] not in active, 'unused asset still present/referenced: ' + item['path'])
    check_public_urls(public_documents())
    if args.published_dir:
        published = (ROOT / args.published_dir).resolve()
        check(published.is_dir(), 'Packaged public directory is missing')
        check_public_urls([path for path in published.rglob('*') if path.is_file() and path.suffix.lower()
                           in {'.html', '.md', '.txt', '.json', '.jsonld', '.xml', '.css', '.js', '.svg'}])
        for name in [*CFG['pages'], 'ai.json', 'data/entity-graph.json']:
            check((published / name).is_file(), 'Packaged artifact misses ' + name)
    generated = subprocess.run([sys.executable, str(ROOT / 'qa/health/generate-discovery.py'), '--check'],
                               capture_output=True, text=True)
    check(generated.returncode == 0, (generated.stdout + generated.stderr).strip())
    if errors:
        raise SystemExit('\n'.join(errors))
    print(generated.stdout.strip())
    print(f'PASS — search/resource health: {len(pages)} configured routes, {len(essays)} full essays, '
          'canonical/Markdown/schema/date parity, discovery catalog, feeds and public URLs')


if __name__ == '__main__':
    main()
