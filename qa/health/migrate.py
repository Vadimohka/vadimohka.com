#!/usr/bin/env python3
"""One-time, explicit migration from the reviewed a5fd47a source snapshot.
Development-only; no network requests and no generated-code execution.
The original content baselines are retained. All public assets and outputs
are verified by independent static/content/browser checks before publication.
"""
from pathlib import Path
from bs4 import BeautifulSoup
from PIL import Image
import copy,csv,hashlib,html,json,re,shutil,subprocess
R=Path(__file__).resolve().parents[2]; D='https://vadimohka.com/'
H=lambda b:hashlib.sha256(b.encode() if isinstance(b,str) else b).hexdigest()
BASE='a5fd47a74aefa09336194202b312298b21dc8cbf'
# Refuse to overwrite concurrent source changes. QA staging files are excluded.
for f in [*R.glob('*.html'),R/'assets/site.css',R/'assets/internal.css',R/'assets/site.js',R/'data/entity-graph.json']:
    original=subprocess.check_output(['git','show',BASE+':'+str(f.relative_to(R))])
    assert original==f.read_bytes(),f'Concurrent source change: {f}'
oldgraph=json.loads((R/'data/entity-graph.json').read_text())['@graph']
with (R/'site-improvement-pack/evidence/source-register.csv').open() as stream:
    originals={row['source_id']:row['url'] for row in csv.DictReader(stream)}
for name in ['architecture','workspace','dubai']:
    image=Image.open(R/f'assets/executive/{name}.webp')
    for width in ([640,960] if name=='dubai' else [640]):
        image.resize((width,round(image.height*width/image.width)),Image.Resampling.LANCZOS).save(R/f'assets/executive/{name}-{width}.webp',quality=82,method=6)
oldgeo='He frequently works from the United States and the United Arab Emirates.'
newgeo='His international focus is enterprise AI conversations with organizations in the United States and the United Arab Emirates.'
focus={
 'enterprise.html':'Enterprise AI strategy and architecture inquiries from organizations in the United States and the United Arab Emirates (UAE) are welcome.',
 'investors.html':'AI technical due diligence inquiries from investors and investment teams in the United States and the United Arab Emirates (UAE) are welcome.',
 'founders.html':'CTO advisory inquiries from founders and executive teams in the United States and the United Arab Emirates (UAE) are welcome.'}
for f in R.glob('*.html'):
    text=f.read_text().replace('<div class="noise"></div><div class="cursor-light"></div>','')
    def backdrop(m):
        cls='section-backdrop'+(' section-backdrop--inner' if 'inner-closing' in m[0] else '')
        return m[0]+f'<img class="{cls}" src="assets/executive/dubai.webp" srcset="assets/executive/dubai-640.webp 640w, assets/executive/dubai-960.webp 960w, assets/executive/dubai.webp 1500w" sizes="100vw" width="1500" height="1000" alt="" loading="lazy" decoding="async" />'
    text=re.sub(r'<section\b(?=[^>]*class="[^"]*\b(?:closing|inner-closing)\b)[^>]*>',backdrop,text)
    def images(m):
        tag=m[0]
        if 'section-backdrop' in tag:return tag
        src=re.search(r'src="assets/executive/(architecture|workspace|dubai)\.webp"',tag)
        if src and 'srcset=' not in tag:
            name=src[1];w=1500 if name=='dubai' else 1000
            sizes='(max-width: 760px) calc(100vw - 40px), (max-width: 1100px) 45vw, 600px' if any(c in tag for c in ['editorial-photo','editorial-image']) else '(max-width: 700px) 160px, (max-width: 1100px) 33vw, 370px'
            if 'loading="eager"' in tag:sizes='(max-width: 760px) calc(100vw - 40px), (max-width: 1100px) 45vw, 600px'
            tag=tag.replace(src[0],src[0]+f' srcset="assets/executive/{name}-640.webp 640w, assets/executive/{name}.webp {w}w" sizes="{sizes}"')
            if 'loading="eager"' in tag and 'fetchpriority=' not in tag:tag=tag.replace('loading="eager"','loading="eager" fetchpriority="high"')
        if 'src="assets/portraits/vadim-home-720.webp"' in tag and 'fetchpriority=' not in tag:tag=tag.replace('loading="eager"','loading="eager" fetchpriority="high"')
        return tag
    text=re.sub(r'<img\b[^>]*>',images,text)
    if f.name=='sources.html':
        for key,sid in [('finance-mail','S003'),('vaiti','S005'),('it-security','S010')]:
            old=f'href="{D}sources.html#{key}"';assert text.count(old)==1
            text=text.replace(old,f'id="{key}" href="{html.escape(originals[sid],quote=True)}"')
    text=text.replace(oldgeo,newgeo)
    if f.name in focus:
        start=text.index('inner-closing');pos=text.index('<div class="hero-actions"',start)
        text=text[:pos]+f'<p class="small market-focus">{focus[f.name]}</p>'+text[pos:]
    if f.name=='about.html':text=re.sub(r'aria-label="Choose the ([^"]+) route"',r'aria-label="Choose this route: \1"',text)
    f.write_text(text)
css=(R/'assets/site.css').read_text().replace("background:var(--bg) url('executive/dubai.webp') right 56%/cover no-repeat",'background:var(--bg)').replace('.noise,.cursor-light{display:none}','')
css+='\n/* Native lazy backgrounds preserve the approved closing composition. */\n.section-backdrop{position:absolute;inset:0;z-index:-2;width:100%;height:100%;max-width:none;object-fit:cover;object-position:right 56%;pointer-events:none}\n.section-backdrop--inner{object-position:70% 48%}\n.market-focus{margin-top:14px;max-width:620px}\n@media print{.section-backdrop{display:none}}\n'
css+='\n@media(max-width:1150px){html.js .nav:not(.is-open) .nav-links{display:none}}\n'
(R/'assets/site.css').write_text(css)
p=R/'assets/internal.css';p.write_text(p.read_text().replace("background:url('executive/dubai.webp') 70% 48%/cover no-repeat",'background:var(--bg)'))
p=R/'assets/site.js';js=p.read_text();a=js.index('const reveals =');b=js.index('const intentCards =',a);js=js[:a]+js[b:]
js=js.replace("link.addEventListener('click', event => {\n      const intent", "link.addEventListener('click', event => {\n      if(event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;\n      const intent");p.write_text(js)
history=json.loads((R/'qa/executive-content-baseline.json').read_text());internal=json.loads((R/'qa/internal-content-baseline.json').read_text())
mappings=json.loads((R/'qa/editorial-titles.json').read_text());oldblock=next(x for x in internal['pages']['about.html']['text'] if oldgeo in x)
mappings.setdefault('about.html',{})[oldblock]=oldblock.replace(oldgeo,newgeo)
(R/'qa/editorial-titles.json').write_text(json.dumps(mappings,indent=2,ensure_ascii=False)+'\n')
sources=json.loads((R/'qa/brand/sources.json').read_text())
for src in sources['sources']:
    if src['source_id'] in ['S003','S005','S006','S010']:
        src['url']=originals[src['source_id']]
        src['maintenance_note']='Original publisher/program URL restored from the source register on 2026-10-07; not a new claim or event.'
(R/'qa/brand/sources.json').write_text(json.dumps(sources,indent=2,ensure_ascii=False)+'\n')
(R/'docs/archive').mkdir(parents=True,exist_ok=True)
for name in ['source-register.csv','claim-register.csv','claim-policy.md']:shutil.copy2(R/'site-improvement-pack/evidence'/name,R/'docs/archive'/name)
shutil.rmtree(R/'site-improvement-pack')
active='\n'.join(p.read_text() for p in [*R.glob('*.html'),*R.glob('*.xml'),*R.glob('*.txt'),R/'ai-profile.md',R/'data/entity-graph.json',R/'assets/site.css',R/'assets/internal.css',R/'assets/site.js'])
removed=[]
for p in sorted((R/'assets').rglob('*')):
    if not p.is_file() or p.suffix not in ['.png','.webp','.jpg']:continue
    if p.parent.name in ['executive','social'] or p.name=='favicon-32.png':continue
    if p.name not in active:removed.append({'path':str(p.relative_to(R)),'bytes':p.stat().st_size,'sha256':H(p.read_bytes())});p.unlink()
assert len(removed)==22 and sum(x['bytes'] for x in removed)==6848925,'Unexpected asset cleanup'
(R/'qa/health/removed-assets.json').write_text(json.dumps(removed,indent=2)+'\n')
meta={
 'index.html':('Vadim Vladymtsev | Enterprise AI CTO & Advisory','Vadim Vladymtsev, CTO at StackLevel Group. Enterprise AI strategy, product architecture, technical due diligence and CTO advisory for USA and UAE audiences.'),
 'about.html':('Vadim Vladymtsev | About & Contact — USA & UAE','Meet Vadim Vladymtsev, CTO at StackLevel Group. Product architecture, enterprise AI and technical judgment. Contact routes for USA and UAE business inquiries.'),
 'century.html':('Century AI Studio | Governed Enterprise AI Platform','Explore Century AI Studio: assistants, workflows, protected data access, private deployment and operational controls for enterprise AI. Product context and sources.'),
 'enterprise.html':('Enterprise AI Strategy & Architecture | USA & UAE','Enterprise AI strategy and architecture with Vadim Vladymtsev. Use-case selection, data boundaries, governance and production planning for USA and UAE organizations.'),
 'investors.html':('AI Technical Due Diligence | USA & UAE | Vadim Vladymtsev','AI technical due diligence for investors in the USA and UAE. Assess product, data, architecture, security, team and deployment risks with Vadim Vladymtsev.'),
 'founders.html':('CTO Advisory for Founders | USA & UAE | Vadim Vladymtsev','CTO advisory for founders and executive teams in the USA and UAE. Align product, architecture, ownership and engineering delivery with a focused technical diagnostic.'),
 'expert.html':('Enterprise AI Speaker & Expert | Vadim Vladymtsev','Enterprise AI speaker and technical expert Vadim Vladymtsev. Topics, published articles, public appearances and contact routes for media and conference organizers.'),
 'work.html':('Enterprise AI Work & Public Record | Vadim Vladymtsev','Explore Vadim Vladymtsev’s enterprise AI work: Century product context, published expertise, engineering experience and source-linked public records.'),
 'sources.html':('Sources & Public References | Vadim Vladymtsev','Original publications, product references, conference records and professional profiles supporting Vadim Vladymtsev’s enterprise AI work and background.'),
 '404.html':('Page Not Found | Vadim Vladymtsev','This page could not be found. Return to Vadim Vladymtsev’s enterprise AI work, advisory services or contact page.')}
person=copy.deepcopy(next(n for n in oldgraph if n['@type']=='Person'));person.pop('areaServed',None)
person['image']=D+'assets/portraits/vadim-home-720.webp';person['mainEntityOfPage']={'@id':D+'about.html#webpage'}
person['sameAs']=['https://vadimohka.ru/','https://www.linkedin.com/in/vadimohka/','https://github.com/Vadimohka','https://codeforces.com/profile/Vadimohka','https://scholar.google.com/citations?user=ccabRDYAAAAJ&hl=ru'];person['knowsLanguage']=['en','ru']
for node in person.get('subjectOf',[]):
    for frag,sid in [('finance-mail','S003'),('vaiti','S005'),('it-security','S010')]:
        if '#'+frag in node.get('url',''):node['url']=originals[sid]
core=[person,*[copy.deepcopy(n) for n in oldgraph if n['@type'] in ['Organization','WebSite']]]
century=copy.deepcopy(next(n for n in oldgraph if n['@type']=='SoftwareApplication'))
services={
 'enterprise.html':('Enterprise AI strategy and architecture','Enterprise AI strategy, product architecture, deployment planning and governance','Organizations and executive teams'),
 'investors.html':('AI technical due diligence','Technical assessment of AI product, data, architecture, deployment and team claims; not investment, legal or financial advice','Investors and investment teams'),
 'founders.html':('CTO advisory for founders','CTO-level diagnosis of product, architecture, engineering ownership and delivery decisions','Founders and executive teams')}
config={'baseURL':D,'modified':'2026-10-07','person':person,'core':core,'century':century,'pages':{}}
for name,(title,desc) in meta.items():
    source=BeautifulSoup((R/name).read_text(),'html.parser');image=source.find('meta',property='og:image')['content']
    config['pages'][name]={'title':title,'description':desc,'socialImage':image,'schemaType':'ProfilePage' if name=='about.html' else ('CollectionPage' if name in ['work.html','expert.html','sources.html'] else 'WebPage'),'label':{'index.html':'Home','about.html':'About & Contact','century.html':'Century AI Studio','enterprise.html':'Enterprise AI','investors.html':'AI Technical Due Diligence','founders.html':'CTO Advisory','expert.html':'Media & Speaking','work.html':'Selected Work','sources.html':'Sources','404.html':'Not Found'}[name]}
    if name in services:
        sname,stype,audience=services[name];config['pages'][name]['service']={'@type':'Service','@id':D+name+'#service','name':sname,'serviceType':stype,'url':D+name,'provider':{'@id':D+'#person'},'description':desc,'areaServed':[{'@type':'Country','name':'United States'},{'@type':'Country','name':'United Arab Emirates'}],'audience':{'@type':'BusinessAudience','audienceType':audience},'availableChannel':{'@type':'ServiceChannel','serviceUrl':D+'about.html#contact','availableLanguage':'en'}}
(R/'qa/health/search-config.json').write_text(json.dumps(config,indent=2,ensure_ascii=False)+'\n')
(R/'robots.txt').write_text('# Public search and retrieval access. Existing allow-all policy is preserved.\nUser-agent: *\nAllow: /\n\nSitemap: '+D+'sitemap.xml\nSitemap: '+D+'sitemap-images.xml\nSitemap: '+D+'sitemap-ai.xml\n')
# Teach static validation the schema graph and the real editorial date.
p=R/'qa/check.mjs';s=p.read_text();s=s.replace('const node = JSON.parse(block[1]);','const parsed = JSON.parse(block[1]);\n      for (const node of parsed["@graph"] || [parsed]) {')
a=s.index('        const servedMarkets =');b=s.index('\n      }',a)
s=s[:a]+'''        if ('areaServed' in node) fail(page, 'areaServed belongs on Service, not Person');
        personCores.push(JSON.stringify({name:node.name,jobTitle:node.jobTitle,sameAs:node.sameAs,worksFor:node.worksFor,image:node.image}));'''+s[b:]
s=s.replace("node['@type'] === 'WebPage' &&", "['WebPage','ProfilePage','CollectionPage'].includes(node['@type']) &&")
s=s.replace("fail(page, 'Century schema has unstable @id');", "fail(page, 'Century schema has unstable @id');\n      }")
s=s.replace("const CURRENT_LASTMOD = '2026-08-31';","const CURRENT_LASTMOD = JSON.parse(read('qa/health/search-config.json')).modified;")
a=s.index("for (const portrait of ['assets/portraits/vadim-boardroom-640.webp'");b=s.index('for (const page of PAGES)',a);s=s[:a]+s[b:]
s=s.replace("if (href.startsWith('/')) { fail", "if (page === '404.html' && href === '/') continue;\n    if (href.startsWith('/')) { fail");p.write_text(s)
p=R/'qa/executive-content.mjs';s=p.read_text().replace('import { internalPages }',"import { approvedHash } from './health/approved-changes.mjs';\nimport { internalPages }")
s=s.replace('expected, `${file}: protected content changed`',"approvedHash('protected:'+file, expected), `${file}: protected content changed`")
s=s.replace("baseline.home.head, 'Homepage metadata/preload changed'", "approvedHash('home-head', baseline.home.head), 'Homepage metadata/preload changed'");p.write_text(s)
p=R/'qa/internal-content.mjs';s=p.read_text().replace('import {readFileSync}',"import { approvedHash, restoredSource } from './health/approved-changes.mjs';\nimport {readFileSync}")
s=s.replace('expected,`${file}: homepage/shared production file changed`',"approvedHash('locked:'+file,expected),`${file}: homepage/shared production file changed`")
s=s.replace('before.head,`${file}: metadata/structured data changed`',"approvedHash('internal-head:'+file,before.head),`${file}: metadata/structured data changed`")
s=s.replace('assert.ok(hrefs.has(href),`${file}: destination lost: ${href}`)','assert.ok(hrefs.has(restoredSource(file,href)),`${file}: destination lost: ${href}`)')
s=s.replace('9 metadata/header/footer snapshots, all destinations/anchors; homepage, shared CSS and JS unchanged','9 metadata/header/footer snapshots, all destinations/anchors; explicit SEO/performance changes authorized');p.write_text(s)
p=R/'qa/browser/check.mjs';s=p.read_text().replace('const viewports = [',"const viewports = [\n  {width:375,height:812,name:'375'},\n  {width:412,height:915,name:'412'},\n  {width:414,height:896,name:'414'},\n  {width:820,height:1180,name:'820'},\n  {width:834,height:1194,name:'834'},")
s=s.replace('await checkResponsive({','await checkHealthInteractions({page, browser, BASE});\n  await checkResponsive({')
s=s.replace("import '../executive-content.mjs';","import '../executive-content.mjs';\nimport {checkHealthInteractions} from '../health/browser.mjs';")
s=s.replace("el.classList.contains('is-visible')","getComputedStyle(el).opacity === '1'");p.write_text(s)
p=R/'qa/browser/responsive.mjs';p.write_text(p.read_text().replace("el.classList.contains('is-visible')","getComputedStyle(el).opacity === '1'"))
p=R/'.github/workflows/browser-qa.yml';s=p.read_text().replace('      - run: npx playwright install --with-deps ${{ matrix.browser }}', '''      - name: Install Chromium without unrelated OS upgrades
        if: matrix.browser == 'chromium'
        run: npx playwright install --only-shell chromium
      - name: Install Firefox or WebKit with required system libraries
        if: matrix.browser != 'chromium'
        run: npx playwright install --with-deps ${{ matrix.browser }}''')
s=s.replace('node qa/check.mjs && node qa/test-regressions.mjs','node qa/check.mjs && node qa/test-regressions.mjs && python3 qa/health/check.py');p.write_text(s)
p=R/'.github/workflows/deploy.yml';s=p.read_text().replace('run: node qa/check.mjs','run: node qa/check.mjs && node qa/test-regressions.mjs && node qa/executive-content.mjs && python3 qa/health/check.py')
a=s.index('        run: |\n          rsync');b=s.index('\n      - uses: actions/configure-pages',a);s=s[:a]+'        run: node qa/health/build.mjs\n'+s[b:];p.write_text(s)
p=R/'.gitignore';p.write_text(p.read_text()+'\n# Generated audit and preview output\nqa/health/results/\n__pycache__/\n*.pyc\n')
p=R/'qa/performance/baseline.md';p.write_text('> Historical pre-redesign measurement. Superseded for the current site by the Site health workflow and its raw Lighthouse artifacts; do not use these scores as current results.\n\n'+p.read_text())
p=R/'assets/executive/credits.json';credits=json.loads(p.read_text());credits['responsive_variants']='The -640.webp and dubai-960.webp files are proportionally resized from the corresponding credited originals, encoded as WebP at quality 82. Original media remains unchanged.';p.write_text(json.dumps(credits,indent=2)+'\n')
subprocess.run(['python3','qa/health/generate-discovery.py','--write'],check=True)
# Record exact authorized changes, not a replacement historical baseline.
changes={'sourceCommit':BASE,'purpose':'Owner-requested SEO/GEO, responsive startup and resource optimization. Keep historical baselines intact.','hashes':{},'sourceRepairs':{}}
for f,old in history['unchanged'].items():
    if f in internal['pages']:continue
    new=H((R/f).read_bytes())
    if new!=old:changes['hashes']['protected:'+f]={'before':old,'after':new}
new=H(re.search(r'<head>[\s\S]*?</head>',(R/'index.html').read_text())[0]);changes['hashes']['home-head']={'before':history['home']['head'],'after':new}
for f,old in internal['locked'].items():
    new=H((R/f).read_bytes())
    if new!=old:changes['hashes']['locked:'+f]={'before':old,'after':new}
for f,record in internal['pages'].items():
    new=H(re.search(r'<head>[\s\S]*?</head>',(R/f).read_text())[0].replace('<link rel="stylesheet" href="assets/internal.css" />',''))
    if new!=record['head']:changes['hashes']['internal-head:'+f]={'before':record['head'],'after':new}
for key in ['finance-mail','vaiti','it-security']:changes['sourceRepairs'][D+'sources.html#'+key]=re.search('id="'+key+'" href="([^"]+)"',(R/'sources.html').read_text())[1]
(R/'qa/health/approved-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print('Migration prepared. Independent QA and browser checks must pass before publication.')
