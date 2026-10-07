from pathlib import Path
from bs4 import BeautifulSoup
import json, hashlib, re, tempfile, shutil
ROOT=Path(__file__).resolve().parents[1]
BASE=Path(tempfile.mkdtemp(prefix='inner-original-'))
PAGES=['work','century','enterprise','investors','founders','about','expert','sources','404']
original_guard=json.loads((ROOT/'qa/executive-content-baseline.json').read_text())
for file in [f'{p}.html' for p in PAGES]+['index.html','assets/site.css','assets/site.js']:
 data=(ROOT/file).read_bytes()
 if file in original_guard['unchanged']:
  assert hashlib.sha256(data).hexdigest()==original_guard['unchanged'][file],f'{file}: not the expected original'
 (BASE/file).parent.mkdir(parents=True,exist_ok=True)
 (BASE/file).write_bytes(data)
def fragment(html):return BeautifulSoup(html,'html.parser')
def node(html):return fragment(html).find()
def addclass(n,*names):n['class']=list(dict.fromkeys(n.get('class',[])+list(names)))
def removeclass(n,*names):n['class']=[c for c in n.get('class',[]) if c not in names]
def norm(t):return ' '.join(t.split())
def photo(name,caption=''):
 return node(f'<figure class="editorial-visual"><img src="assets/executive/{name}.webp" width="1200" height="800" alt="" decoding="async" loading="eager"><figcaption>{caption}</figcaption></figure>')
def platform():
 return node('''<figure class="platform-visual" aria-label="Century architecture overview">
 <div class="platform-frame"><div class="platform-top"><span class="platform-wordmark">◎ Century</span><span>Architecture overview</span></div>
 <div class="platform-body"><p class="visual-eyebrow">Private enterprise AI</p><p class="visual-title">One operating<br>boundary.</p><div class="platform-inputs"><span>Assistants</span><span>Workflows</span><span>APIs</span></div><div class="flow-line" aria-hidden="true">↓</div><div class="platform-core"><span>Governed access</span><small>Policies · Roles · Audit</small></div><div class="flow-line" aria-hidden="true">↓</div><div class="platform-inputs platform-bottom"><span>Models</span><span>Company data</span><span>Infrastructure</span></div><div class="platform-foot">Private deployment boundary</div></div></div>
 <figcaption>Illustrative architecture, based on the published product capabilities. Not a product screenshot.</figcaption></figure>''')
def memo():
 return node('''<figure class="memo-visual" aria-label="Technical diligence review framework"><div class="memo-sheet"><div class="memo-heading"><span>Technical diligence</span><span>Review framework</span></div><p class="visual-title">Evidence before<br>commitment.</p><div class="memo-row"><span>01</span><span>Product reality</span><span aria-hidden="true">↗</span></div><div class="memo-row"><span>02</span><span>Data &amp; models</span><span aria-hidden="true">↗</span></div><div class="memo-row"><span>03</span><span>Architecture</span><span aria-hidden="true">↗</span></div><div class="memo-row"><span>04</span><span>Team execution</span><span aria-hidden="true">↗</span></div><p class="memo-footer">Known. Open. At risk.</p></div><figcaption>Illustrative review structure — not a completed assessment.</figcaption></figure>''')
def portrait():
 return node('''<figure class="profile-portrait"><img src="assets/portraits/vadim-home-720.webp" width="720" height="900" alt="Vadim Vladymtsev" loading="eager" decoding="async"><figcaption>Vadim Vladymtsev<span>CTO · StackLevel Group</span></figcaption></figure>''')
for name in PAGES:
 raw=(BASE/f'{name}.html').read_text();s=fragment(raw);main=s.select_one('main')
 sections=main.select(':scope > section');hero=sections[0];grid=hero.select_one('.hero-grid');copy=hero.select_one('.hero-copy')
 hero['class']=['inner-hero',f'inner-hero--{name}'];grid['class']=['container','inner-hero-grid'];copy['class']=['inner-hero-copy']
 for img in grid.select(':scope > .hero-photo'):img.decompose()
 if name=='century':grid.append(platform())
 elif name=='investors':grid.append(memo())
 elif name=='about':grid.append(portrait())
 elif name=='enterprise':grid.append(photo('architecture','Architecture. Governance. Operations.'))
 elif name=='founders':grid.append(photo('workspace','Product. Architecture. Engineering.'))
 elif name=='expert':grid.append(photo('workspace','Writing · Commentary · Speaking'))
 elif name=='work':grid.append(node('''<div class="work-hero-index"><p class="visual-eyebrow">The public record</p><a href="#role-title"><span>01</span>Product &amp; architecture<span>↗</span></a><a href="#public-title"><span>02</span>Writing &amp; appearances<span>↗</span></a><a href="#background-title"><span>03</span>Engineering foundation<span>↗</span></a></div>'''))
 elif name=='sources':grid.append(node('<div class="archive-mark" aria-hidden="true">11<span>Public references</span></div>'))
 elif name=='404':grid.append(node('<div class="error-mark" aria-hidden="true">404</div>'))
 breaks={'work':['Selected work','and public record.'],'century':['A corporate AI platform','for controlled work.'],'enterprise':['Private AI systems','for regulated organisations.'],'investors':['AI Technical','Due Diligence.'],'founders':['When product, architecture','and engineering diverge.'],'about':['Enterprise AI CTO','and product operator.'],'expert':['Public expertise on','governed enterprise AI.'],'404':['This page is','off the map.']}
 h=copy.select_one('h1');h['class']=['inner-title']
 if name in breaks:
  assert norm(h.get_text())==norm(' '.join(breaks[name])),name
  h.clear()
  for t in breaks[name]:h.append(node('<span>'+t+'</span>'))
 jumps={'century':[('problem-title','Context'),('surface-title','Capabilities'),('deployment-title','Deployment'),('relationship-title','Product record')],'enterprise':[('decisions-title','Decisions'),('path-title','Process'),('deliverables-title','Deliverables'),('proof-title','Track record')],'investors':[('decision-title','Assessment'),('process-title','Process'),('deliverables-title','Deliverables'),('boundaries-title','Boundaries')],'founders':[('triggers-title','When to engage'),('process-title','Process'),('deliverables-title','Deliverables'),('builder-title','Background')],'about':[('approach-title','Approach'),('background-title','Background'),('contact','Contact')],'expert':[('records-title','Public records'),('topics-title','Topics'),('bios-title','Biographies'),('kit-title','Media enquiries')]}
 if name in jumps:
  nav=node('<nav class="page-index" aria-label="On this page"></nav>')
  for i,(ref,label) in enumerate(jumps[name]):nav.append(node(f'<a href="#{ref}"><span>0{i+1}</span>{label}<span aria-hidden="true">↗</span></a>'))
  w=node('<div class="container"></div>');w.append(nav);hero.append(w)
 for sec in sections[1:]:
  addclass(sec,'inner-section');removeclass(sec,'section','section-tight')
  con=sec.select_one(':scope > .container')
  if con is None:continue
  removeclass(con,'split','center')
  for ch in list(con.find_all(recursive=False)):
   if ch.name=='div' and ch.select_one('h2') and not ch.select_one('.card'):ch.unwrap()
  intro=node('<div class="section-intro"></div>')
  for ch in list(con.find_all(recursive=False)):
   if ch.name=='h2' or (ch.name=='p' and ('kicker' in ch.get('class',[]) or 'lead' in ch.get('class',[]))):intro.append(ch.extract())
  if intro.contents:con.insert(0,intro)
  for p in sec.select('[style]'):
   if p.name in ['p','div']:del p['style']
  for group in sec.select('.cards'):
   classes=group.get('class',[]);columns=4 if 'four' in classes else 2 if 'two' in classes else 3
   group['class']=['editorial-grid',f'editorial-grid--{columns}']
   for card in group.find_all(recursive=False):removeclass(card,'card');addclass(card,'editorial-item')
  for group in sec.select('.article-list'):
   group['class']=(['container'] if 'container' in group.get('class',[]) else [])+['record-list']
   for rec in group.find_all(recursive=False):removeclass(rec,'article');addclass(rec,'record-row')
  for ul in sec.select('.clean-list'):
   ul['class']=['operating-list']
   for i,li in enumerate(ul.find_all('li',recursive=False)):li.insert(0,node(f'<span class="step-number" aria-hidden="true">0{i+1}</span>'))
  for r in sec.select('.reveal'):removeclass(r,'reveal')
  if 'section-cta' in sec.get('class',[]):removeclass(sec,'section-cta');addclass(sec,'inner-closing')
 def section(label):return main.select_one(f'section[aria-labelledby="{label}"]')
 if name=='work':
  addclass(section('role-title'),'work-feature-section')
  group=section('role-title').select_one('.editorial-grid');group['class']=['work-feature-grid']
  items=group.select(':scope > .editorial-item');items[0]['class']=['role-note'];items[1]['class']=['flagship-work']
  feature_copy=node('<div class="flagship-copy"></div>')
  for ch in list(items[1].contents):feature_copy.append(ch.extract())
  items[1].append(feature_copy);items[1].append(platform())
  pub=section('public-title');g=pub.select_one('.editorial-grid');g['class']=['publication-grid']
  for i,item in enumerate(g.find_all(recursive=False)):
   item['class']=['publication-item'];content=node('<div class="publication-copy"></div>')
   for child in list(item.contents):content.append(child.extract())
   item.append(photo(['workspace','architecture','dubai','workspace'][i]));item.append(content)
   for im in item.select('img'):im['loading']='lazy'
  addclass(section('background-title'),'timeline-section')
 if name in ['enterprise','investors','founders']:
  label='path-title' if name=='enterprise' else 'process-title'
  sec=section(label);addclass(sec,'process-section','tinted-section')
  g=sec.select_one('.editorial-grid')
  if g:g['class']=['process-grid']
  deliver=section('deliverables-title');addclass(deliver,'deliverables-section')
  for i,item in enumerate(deliver.select('.editorial-item')):
   if not item.select_one('.num'):item.insert(0,node(f'<span class="num" aria-hidden="true">0{i+1}</span>'))
  first=section('decisions-title' if name=='enterprise' else 'decision-title' if name=='investors' else 'triggers-title')
  addclass(first,'assessment-section')
  if name=='founders':
   g=first.select_one('.editorial-grid');g['class']=['diagnostic-grid']
   for i,item in enumerate(g.find_all(recursive=False)):item.insert(0,node(f'<span class="diagnostic-number" aria-hidden="true">0{i+1}</span>'))
  if name=='enterprise':
   sec=section('controls-title');addclass(sec,'controls-section','tinted-section')
   frame=sec.select_one('.panel.frame')
   if frame:
    ul=sec.select_one('.operating-list')
    frame.replace_with(ul.extract()) if ul else frame.decompose()
 if name=='century':
  addclass(section('problem-title'),'context-section')
  addclass(section('surface-title'),'capabilities-section','tinted-section')
  addclass(section('deployment-title'),'deployment-section')
  for pan in section('deployment-title').select('.panel.frame'):pan['class']=['deployment-note']
  addclass(section('governance-title'),'assurance-section','tinted-section')
  addclass(section('relationship-title'),'record-section')
 if name=='about':
  addclass(section('approach-title'),'profile-approach','tinted-section')
  addclass(section('background-title'),'timeline-section')
  contact=section('contact-title');addclass(contact,'contact-section')
  group=contact.select_one('.editorial-grid');group['class']=['contact-routes']
  for card in group.find_all(recursive=False):
   addclass(card,'contact-route');link=card.select_one('a.route-link');link['class']=['route-link','text-action']
   link.append(node('<span aria-hidden="true">↗</span>'))
  response=contact.select_one('[data-route-response]');response['class']=['route-response','contact-next']
 if name=='expert':
  addclass(section('records-title'),'press-section')
  recs=section('records-title').select('.record-row')
  for i,rec in enumerate(recs):rec.insert(0,node(f'<span class="record-number" aria-hidden="true">0{i+1}</span>'))
  addclass(section('topics-title'),'topics-section','tinted-section')
  bios=section('bios-title');addclass(bios,'bios-section')
  g=bios.select_one('.editorial-grid')
  if g:
   g['class']=['bio-library']
   for i,old in enumerate(list(g.find_all(recursive=False))):
    details=node('<details class="bio-variant"></details>')
    if i==0:details['open']=''
    title=old.select_one('h3, .card-label');summ=node('<summary></summary>')
    if title and title.name!='h3':title.name='span';title['class']=['bio-label']
    if title:summ.append(title.extract())
    summ.append(node('<span class="disclosure-sign" aria-hidden="true">+</span>'));details.append(summ)
    body=node('<div class="bio-copy"></div>')
    for child in list(old.contents):body.append(child.extract())
    details.append(body);old.replace_with(details)
  addclass(section('kit-title'),'media-kit-section')
 if name=='sources':
  sec=sections[1];addclass(sec,'source-library');con=sec.select_one('.container')
  g=con if 'record-list' in con.get('class',[]) else con.select_one('.record-list');g['class']=['container','source-list']
  for i,row in enumerate(g.find_all(recursive=False)):
   row['class']=['source-entry','external-link'];row.insert(0,node(f'<span class="record-number" aria-hidden="true">{i+1:02}</span>'))
  addclass(section('methodology-title'),'methodology-section','tinted-section')
 if name=='404':
  addclass(sections[1],'error-routes')
  for group in sections[1].select('.door-grid'):group['class']=['error-grid']
  for a in sections[1].select('.door'):a['class']=['error-route']
 for sec in sections[1:]:
  for fr in sec.select('.panel.frame'):
   if not norm(fr.get_text()):fr.decompose()
 dimensions={'assets/executive/architecture.webp':(1000,667),'assets/executive/workspace.webp':(1000,668),'assets/executive/dubai.webp':(1500,1000),'assets/portraits/vadim-home-720.webp':(720,900)}
 for img in main.select('img'):
  if img['src'] in dimensions:
   w,h=dimensions[img['src']];img['width']=str(w);img['height']=str(h)
 newmain=str(main)
 start=raw.index('<main');end=raw.index('</main>')+len('</main>')
 out=raw[:start]+newmain+raw[end:]
 out=out.replace('</head>','<link rel="stylesheet" href="assets/internal.css" /></head>',1)
 out=out.replace('<body>',f'<body class="inner-page page-{name}">',1)
 (ROOT/f'{name}.html').write_text(out)
# Snapshot original content, never edited output; every source hash is independently anchored.
b=BASE;r=ROOT
norm=lambda x:' '.join(x.split())
hash=lambda x:hashlib.sha256(x if isinstance(x,bytes) else x.encode()).hexdigest()
m={'baseCommit':'6be190366a6966464b44875d1af31250072811f3','locked':{f:hash((b/f).read_bytes()) for f in ['index.html','assets/site.css','assets/site.js']},'pages':{}}
for f in sorted(b.glob('*.html')):
 if f.stem=='index':continue
 raw=f.read_text();s=BeautifulSoup(raw,'html.parser')
 m['pages'][f.name]={'sourceHash':hash(raw),'head':hash(re.search(r'<head>[\s\S]*?</head>',raw)[0]),'header':hash(re.search(r'<header\b[\s\S]*?</header>',raw)[0]),'footer':hash(re.search(r'<footer\b[\s\S]*?</footer>',raw)[0]),'text':[norm(x.get_text(' ',strip=True)) for x in s.select('main h1,main h2,main h3,main p,main li')],'hrefs':sorted(set(x['href'] for x in s.select('[href]'))),'ids':sorted(set(x['id'] for x in s.select('[id]')))}
(r/'qa/internal-content-baseline.json').write_text(json.dumps(m,ensure_ascii=False,separators=(',',':'))+'\n')
file=ROOT/'qa/executive-content.mjs';text=file.read_text()
text=text.replace("import assert from 'node:assert/strict';","import assert from 'node:assert/strict';\nimport { internalPages } from './internal-content.mjs';")
text=text.replace('  assert.equal(hash(readFileSync(resolve(ROOT, file))), expected, `${file}: protected content changed`);','  // Internal HTML now has a semantic + metadata guard anchored to this original hash.\n  if (!internalPages.has(file)) assert.equal(hash(readFileSync(resolve(ROOT, file))), expected, `${file}: protected content changed`);')
file.write_text(text)
file=ROOT/'qa/browser/check.mjs';text=file.read_text()
start=text.index('      const expectedHero =');end=text.index("      if (route === 'index.html' && viewport.name",start)
text=text[:start]+'''      if (route === 'index.html') {
        if (!alignment.heroImage.includes('vadim-home-720.webp')) throw new Error('Homepage portrait changed');
        if (await page.locator('link[href="assets/internal.css"]').count()) throw new Error('Internal CSS leaked onto the homepage');
      } else {
        if (await page.locator('.inner-hero').count() !== 1) throw new Error(`${route}: missing internal-page composition`);
        if (await page.locator('.hero-photo').count()) throw new Error(`${route}: old repeated portrait layout returned`);
        if (route === 'about.html' && await page.locator('.profile-portrait img[src="assets/portraits/vadim-home-720.webp"]').count() !== 1) throw new Error('About portrait missing');
      }
'''+text[end:]
pos=text.index('  const noJs = await browser.newContext(')
text=text[:pos]+'''  for (const width of [320, 768, 1440]) {
    await page.setViewportSize({width,height:900});
    await page.goto(`${BASE}/expert.html?browserqa=bios`, {waitUntil:'networkidle'});
    for (const disclosure of await page.locator('.bio-variant').all()) {
      await disclosure.locator('summary').focus();
      if (await disclosure.getAttribute('open') === null) await page.keyboard.press('Enter');
      if (!(await disclosure.locator('.bio-copy').isVisible())) throw new Error('Bio disclosure inaccessible');
      await auditLayout(page, `expert expanded biography ${width}`);
    }
    await page.goto(`${BASE}/century.html?browserqa=chapter-navigation`, {waitUntil:'networkidle'});
    const chapter = page.locator('.page-index a[href="#deployment-title"]');
    await chapter.click();
    await page.waitForFunction(() => Math.abs(document.querySelector('#deployment-title').getBoundingClientRect().top - document.querySelector('.site-header').getBoundingClientRect().height) < 100);
    await auditLayout(page, `century chapter navigation ${width}`);
  }

'''+text[pos:]
file.write_text(text)
print('Rebuilt 9 internal pages; source-anchored preservation guard covers',sum(len(p['text']) for p in m['pages'].values()),'text blocks.')
shutil.rmtree(BASE)
