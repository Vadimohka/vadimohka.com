#!/usr/bin/env python3
"""Offline regression guards for canonical URLs, local anchors, image candidates and schema."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urljoin,urlsplit,unquote
from datetime import date
import json,re,subprocess,sys,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[2];DOMAIN='https://vadimohka.com/'
class Page(HTMLParser):
 def __init__(self,text):
  super().__init__(convert_charrefs=True);self.ids=set();self.links=[];self.images=[];self.metas={};self.hreflang={};self.preloads=[];self.canonical=None;self.base=None;self.headings=[];self.feed(text)
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if a.get('id'):self.ids.add(a['id'])
  if tag=='a' and a.get('href'):self.links.append(a['href'])
  if tag=='img':self.images.append(a)
  if tag=='meta':self.metas[a.get('name',a.get('property'))]=a.get('content')
  if tag=='base':self.base=a.get('href')
  if tag=='link':
   if a.get('rel')=='canonical':self.canonical=a.get('href')
   if a.get('hreflang'):self.hreflang[a['hreflang']]=a['href']
   if a.get('rel')=='preload':self.preloads.append(a)
  if tag in ['h1','h2','h3','h4']:self.headings.append(tag)
errors=[]
def check(ok,message):
 if not ok:errors.append(message)
pages={p.name:Page(p.read_text()) for p in ROOT.glob('*.html')};persons=[];titles=[];descriptions=[]
for name,p in pages.items():
 text=(ROOT/name).read_text();canonical=DOMAIN+('' if name=='index.html' else name)
 titles.append(re.search(r'<title>(.*?)</title>',text).group(1));descriptions.append(p.metas.get('description'))
 check(p.headings.count('h1')==1,name+': exactly one H1 required')
 check(p.metas.get('og:locale')=='en_US',name+': English social locale')
 if name=='404.html':check('noindex' in p.metas.get('robots','') and p.base=='/',name+': noindex + root base required')
 else:
  check(p.canonical==canonical,name+': canonical mismatch')
  check(p.hreflang=={'en':canonical,'x-default':canonical},name+': invalid/nonexistent locale alternates')
  check('max-image-preview:large' in p.metas.get('robots',''),name+': preview visibility')
 for link in p.links:
  target=urlsplit(urljoin(canonical,link));path=unquote(target.path).lstrip('/') or 'index.html'
  if target.netloc!='vadimohka.com':continue
  check((ROOT/path).is_file(),f'{name}: broken local destination {link}')
  if target.fragment and path in pages:check(unquote(target.fragment) in pages[path].ids,f'{name}: missing anchor {link}')
 for image in p.images:
  check('alt' in image and int(image.get('width',0))>0 and int(image.get('height',0))>0,name+': image semantics/dimensions missing')
  check((ROOT/image['src']).is_file(),name+': image missing '+image['src'])
  if image.get('srcset'):
   check(bool(image.get('sizes')),name+': srcset without sizes')
   for candidate in image['srcset'].split(','):
    src,w=candidate.strip().split();check((ROOT/src).is_file() and re.fullmatch(r'\d+w',w),name+': invalid image candidate '+candidate)
  if 'section-backdrop' in image.get('class',''):check(image.get('loading')=='lazy',name+': below-fold backdrop loaded eagerly')
 check(sum(x.get('as')=='font' for x in p.preloads)==2,name+': fonts not discoverable in head')
 for raw in re.findall(r'<script type="application/ld\+json">([\s\S]*?)</script>',text):
  data=json.loads(raw);graph=data.get('@graph',[data]);localids={n['@id'] for n in graph if '@id' in n}
  person=next(n for n in graph if n.get('@type')=='Person');persons.append(person)
  check('areaServed' not in person and 'address' not in person and 'location' not in person,name+': unsupported Person geography')
  check(person['image']==DOMAIN+'assets/portraits/vadim-home-720.webp',name+': inconsistent identity photograph')
  check('&amp;' not in raw,name+': HTML escaping inside JSON-LD URL')
  for node in graph:
   check(not any(k in node for k in ['aggregateRating','review','priceRange']),name+': unsupported reputation/price claim')
   if node['@type']=='Service':check({v['name'] for v in node['areaServed']}=={'United States','United Arab Emirates'},name+': service markets mismatch')
   for rel in ['provider','isPartOf','publisher','worksFor','about','mainEntity']:
    if isinstance(node.get(rel),dict) and '@id' in node[rel]:check(node[rel]['@id'] in localids,name+': dangling '+rel+' reference')
   if node['@type']=='ProfilePage':check(node.get('mainEntity',{}).get('@id')==DOMAIN+'#person',name+': invalid profile identity')
check(len(set(titles))==len(titles),'duplicate titles');check(len(set(descriptions))==len(descriptions),'duplicate descriptions')
check(all(x==persons[0] for x in persons),'Person facts drift across pages')
check(json.loads((ROOT/'data/entity-graph.json').read_text())['@graph'][0]==persons[0],'external entity graph differs')
for name in ['about.html','llms.txt','llms-full.txt','ai-profile.md','data/entity-graph.json']:
 check('frequently works from' not in (ROOT/name).read_text(),name+': unconfirmed physical-presence claim')
for name in ['enterprise.html','investors.html','founders.html']:check('United Arab Emirates (UAE)' in (ROOT/name).read_text(),name+': market context is only hidden in metadata')
for fragment in ['finance-mail','vaiti','it-security']:check(fragment in pages['sources.html'].ids,'missing legacy source anchor '+fragment)
for entry in re.findall(r'<a\b[^>]*class="source-entry[^>]*>',(ROOT/'sources.html').read_text()):check('href="https://vadimohka.com/sources.html#' not in entry,'source self-reference loop')
ns={'s':'http://www.sitemaps.org/schemas/sitemap/0.9'}
for name in ['sitemap.xml','sitemap-images.xml','sitemap-ai.xml']:
 doc=ET.fromstring((ROOT/name).read_text())
 for entry in doc.findall('s:url',ns):
  modified=entry.find('s:lastmod',ns).text;check(date.fromisoformat(modified)<=date.today(),name+': future lastmod')
  url=entry.find('s:loc',ns).text;path=unquote(urlsplit(url).path).lstrip('/') or 'index.html';check((ROOT/path).is_file(),name+': missing URL '+url)
 check('image:title' not in (ROOT/name).read_text(),name+': deprecated image sitemap field')
robots=(ROOT/'robots.txt').read_text()
for name in ['sitemap.xml','sitemap-images.xml','sitemap-ai.xml']:check('Sitemap: '+DOMAIN+name in robots,'robots missing '+name)
active='\n'.join((ROOT/p).read_text() for p in [*pages,'assets/site.css','assets/internal.css','assets/site.js','sitemap-images.xml'])
for item in json.loads((ROOT/'qa/health/removed-assets.json').read_text()):check(not (ROOT/item['path']).exists() and item['path'] not in active,'unused asset still present/referenced: '+item['path'])
subprocess.run([sys.executable,str(ROOT/'qa/health/generate-discovery.py'),'--check'],check=True)
if errors:raise SystemExit('\n'.join(errors))
print(f'PASS — search/resource health: {len(pages)} routes, complete local anchors, consistent schema, image candidates and generated discovery')
