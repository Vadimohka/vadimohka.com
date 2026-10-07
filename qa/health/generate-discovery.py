#!/usr/bin/env python3
"""Generate search metadata and discovery documents. No network or runtime dependency.
Use --write after editing search-config.json; CI uses --check to detect drift.
Dates are editorial inputs, never the current clock or an automatic deployment date.
"""
import argparse, copy, html, json, re
from html.parser import HTMLParser
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
CFG=json.loads((ROOT/'qa/health/search-config.json').read_text())
DOMAIN=CFG['baseURL']; DATE=CFG['modified']
class Blocks(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True);self.inside=False;self.depth=0;self.kind=None;self.parts=[];self.blocks=[];self.skip=0
    def handle_starttag(self,tag,attrs):
        if tag=='main':self.inside=True
        if not self.inside:return
        if tag in ('svg','script','style'):self.skip+=1
        if tag in ('h1','h2','h3','p','li','summary') and not self.skip and self.kind is None:self.kind=tag;self.parts=[]
        if tag=='br' and self.kind:self.parts.append(' ')
    def handle_endtag(self,tag):
        if tag=='main':self.inside=False
        if tag in ('svg','script','style') and self.skip:self.skip-=1
        if self.kind==tag:
            text=re.sub(r'\s+',' ',' '.join(self.parts)).strip()
            if text:self.blocks.append((tag,text))
            self.kind=None
    def handle_data(self,data):
        if self.inside and self.kind and not self.skip:self.parts.append(data)
def dump(data):return json.dumps(data,ensure_ascii=False,separators=(',',':')).replace('</','<\\/')
def url(name):return DOMAIN+('' if name=='index.html' else name)
def metadata(name,cfg):
    canonical=url(name);escape=lambda v:html.escape(v,quote=True)
    lines=['<meta charset="utf-8" />','<meta name="viewport" content="width=device-width, initial-scale=1" />',
        '<meta name="yandex-verification" content="c3fd18a00a5bf714" />',
        '<script>document.documentElement.classList.add("js");</script>',
        '<link rel="preload" href="assets/executive/PlayfairDisplay.woff2" as="font" type="font/woff2" crossorigin />',
        '<link rel="preload" href="assets/executive/DMSans.woff2" as="font" type="font/woff2" crossorigin />']
    if name in ('index.html','about.html'):
        lines+=['<link rel="preload" as="image" href="assets/portraits/vadim-home-720.webp" type="image/webp" fetchpriority="high" />',
                '<link rel="preload" as="image" href="assets/executive/horizon.webp" type="image/webp" fetchpriority="high" />']
    if name=='404.html':lines.insert(1,'<base href="/" />')
    lines+=['<link rel="stylesheet" href="assets/site.css" />']
    if name!='index.html':lines+=['<link rel="stylesheet" href="assets/internal.css" />']
    lines+=[f'<title>{escape(cfg["title"])}</title>',f'<meta name="description" content="{escape(cfg["description"])}" />',
        '<meta name="author" content="Vadim Vladymtsev" />','<meta name="theme-color" content="#080c0e" />',
        '<meta name="robots" content="'+('noindex,follow' if name=='404.html' else 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1')+'" />']
    if name!='404.html':
        lines += [f'<link rel="canonical" href="{canonical}" />',f'<link rel="alternate" hreflang="en" href="{canonical}" />',f'<link rel="alternate" hreflang="x-default" href="{canonical}" />']
    lines += ['<meta property="og:type" content="website" />','<meta property="og:site_name" content="Vadim Vladymtsev" />','<meta property="og:locale" content="en_US" />']
    for prop,val in [('title',cfg['title']),('description',cfg['description']),('url',canonical),('image',cfg['socialImage']),('image:type','image/jpeg' if cfg['socialImage'].endswith('.jpg') else 'image/png'),('image:width','1200'),('image:height','630'),('image:alt',cfg['label']+' — Vadim Vladymtsev')]:lines.append(f'<meta property="og:{prop}" content="{escape(val)}" />')
    for prop,val in [('card','summary_large_image'),('title',cfg['title']),('description',cfg['description']),('image',cfg['socialImage']),('image:alt',cfg['label']+' — Vadim Vladymtsev')]:lines.append(f'<meta name="twitter:{prop}" content="{escape(val)}" />')
    lines+=['<link rel="icon" href="assets/favicon.svg" type="image/svg+xml" />','<link rel="icon" href="assets/favicon-32.png" sizes="32x32" type="image/png" />','<link rel="apple-touch-icon" href="assets/favicon-180.png" />','<link rel="describedby" href="llms.txt" type="text/plain" />','<link rel="describedby" href="data/entity-graph.json" type="application/ld+json" />']
    graph=copy.deepcopy(CFG['core'])
    page={'@type':cfg['schemaType'],'@id':canonical+'#webpage','url':canonical,'name':cfg['title'],'description':cfg['description'],'inLanguage':'en','dateModified':DATE,'isPartOf':{'@id':DOMAIN+'#website'},'about':{'@id':DOMAIN+'#person'}}
    if name=='about.html':page['mainEntity']={'@id':DOMAIN+'#person'}
    if 'service' in cfg:graph.append(cfg['service']);page['mainEntity']={'@id':cfg['service']['@id']}
    if name=='century.html':graph.append(CFG['century']);page['mainEntity']={'@id':DOMAIN+'#century'}
    if name=='sources.html':page['citation']=[x['url'] for x in CFG['person'].get('subjectOf',[])]
    graph.append(page)
    lines.append('<script type="application/ld+json">'+dump({'@context':'https://schema.org','@graph':graph})+'</script>')
    return '<head>\n'+'\n'.join(lines)+'\n</head>'
def outputs():
    out={};full=['# Vadim Vladymtsev — public site text','',f'Canonical website: {DOMAIN}',f'Content updated: {DATE}','', 'This document is generated from the visible English site. Links and the human-readable pages are authoritative. It does not establish offices, client engagements or personal presence in a country.','']
    for name,cfg in CFG['pages'].items():
        text=(ROOT/name).read_text();out[name]=re.sub(r'<head>[\s\S]*?</head>',lambda m:metadata(name,cfg),text,count=1)
        if name=='404.html':continue
        parser=Blocks();parser.feed(text)
        full += [f'## {cfg["label"]}',url(name),'']
        for tag,block in parser.blocks:
            if tag in ('h1','h2','h3'):full+=['### '+block,'']
            elif tag=='li':full+=['- '+block]
            elif tag!='summary':full+=[block,'']
    core=copy.deepcopy(CFG['core']);core.append(CFG['century']);core += [cfg['service'] for cfg in CFG['pages'].values() if 'service' in cfg]
    out['data/entity-graph.json']=json.dumps({'@context':'https://schema.org','@graph':core},ensure_ascii=False,indent=2)+'\n'
    intro='# Vadim Vladymtsev\n\n> Enterprise AI CTO and product operator. CTO at StackLevel Group.\n\nEnglish-language enterprise AI, technical due diligence and CTO advisory for audiences in the United States and the United Arab Emirates (UAE). Geographic focus is not a claim of offices or residence.\n\n'
    index=intro+'## Canonical pages\n\n'
    for name,cfg in CFG['pages'].items():
        if name!='404.html':index+=f'- [{cfg["label"]}]({url(name)}): {cfg["description"]}\n'
    index+='\n## Public profiles and product\n\n- [Russian-language personal profile](https://vadimohka.ru/)\n- [LinkedIn](https://www.linkedin.com/in/vadimohka/)\n- [Century AI Studio](https://century-ai.by/)\n\n## Supporting documents\n\n- [Profile summary]('+DOMAIN+'ai-profile.md)\n- [Full public site text]('+DOMAIN+'llms-full.txt)\n- [Structured entity graph]('+DOMAIN+'data/entity-graph.json)\n'
    out['llms.txt']=index
    profile=intro+'## Work and inquiry types\n\n'
    for name,cfg in CFG['pages'].items():
        if 'service' in cfg:profile+=f'### {cfg["service"]["name"]}\n\n{cfg["description"]}\n\n{url(name)}\n\n'
    profile+='## Product context\n\n'+CFG['century']['description']+'\n\n'+DOMAIN+'century.html\n\n## Public record\n\n'
    for record in CFG['person'].get('subjectOf',[]):profile+='- '+record['name']+' — '+record.get('datePublished',record.get('startDate',''))+' — '+record['url']+'\n'
    profile+='\n## Identity and contact\n\n'+DOMAIN+'about.html#contact\n\nRussian-language profile: https://vadimohka.ru/\n\nTechnical assessments are not investment, legal or financial advice. Public product recognition is not a personal award.\n'
    out['ai-profile.md']=profile;out['llms-full.txt']='\n'.join(full).rstrip()+'\n'
    pre='<?xml version="1.0" encoding="UTF-8"?>\n';esc=lambda s:html.escape(s,quote=False)
    entries=[f'  <url><loc>{url(name)}</loc><lastmod>{DATE}</lastmod></url>' for name in CFG['pages'] if name!='404.html']
    out['sitemap.xml']=pre+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+'\n'.join(entries)+'\n</urlset>\n'
    entries=[]
    for name,cfg in CFG['pages'].items():
        if name=='404.html':continue
        imgs=[cfg['socialImage']]
        if name in ('index.html','about.html'):imgs.append(DOMAIN+'assets/portraits/vadim-home-720.webp')
        entries.append(f'  <url><loc>{url(name)}</loc><lastmod>{DATE}</lastmod>'+''.join('<image:image><image:loc>'+esc(image)+'</image:loc></image:image>' for image in imgs)+'</url>')
    out['sitemap-images.xml']=pre+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">\n'+'\n'.join(entries)+'\n</urlset>\n'
    out['sitemap-ai.xml']=pre+'<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'  <url><loc>{DOMAIN}{name}</loc><lastmod>{DATE}</lastmod></url>\n' for name in ['llms.txt','llms-full.txt','ai-profile.md','data/entity-graph.json'])+'</urlset>\n'
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser();g=p.add_mutually_exclusive_group(required=True);g.add_argument('--check',action='store_true');g.add_argument('--write',action='store_true');args=p.parse_args()
    changed=[]
    for name,text in outputs().items():
        path=ROOT/name
        if not path.exists() or path.read_text()!=text:
            changed.append(name)
            if args.write:path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text)
    if args.check and changed:raise SystemExit('Discovery output is stale: '+', '.join(changed))
    print(('Updated' if args.write else 'PASS — generated discovery:')+' '+str(len(changed) if args.write else len(outputs()))+' files')
