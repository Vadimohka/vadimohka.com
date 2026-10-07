from pathlib import Path
from bs4 import BeautifulSoup
import base64, gzip, hashlib, json, re
ROOT=Path(__file__).resolve().parents[1]
# This preparation runs only on the isolated editorial-refinement branch.
# Preserve factual paragraphs, source destinations, route attributes and global assets.
payload=(ROOT/'qa/editorial-css.b64').read_text().strip().replace('ZQfq7//UTTq6j5M474','ZQfq7//UTq6j5M474')
css=gzip.decompress(base64.b64decode(payload))
assert hashlib.sha256(css).hexdigest()=='e49b026275bcf47e84873fb1b21b232264db1169761c1738d42fd19ed767cc15', 'CSS transport hash mismatch'
TITLES={
'work': {'Selected work and public record.':'Product. Practice. Perspective.','Product, architecture and controlled production.':'Selected work.','Writing, commentary and appearances.':'Ideas in the open.','An engineering foundation built through teaching and competition.':'Built on engineering.','Have a decision that needs a clearer technical frame?':'Let’s find the next move.'},
'century':{'A corporate AI platform for controlled work.':'Private AI. Under your control.','Models are only one part of the operating system.':'More than a model.','Capabilities currently described by the product source.':'One platform. Connected capabilities.','A protected contour around models, data and work.':'Your infrastructure. Your boundary.','The system is reviewable because activity leaves a trace.':'Control, built in.','Product context, not an invented personal title.':'Product record & relationship.','Start with the current product surface.':'Explore what comes next.'},
'enterprise':{'Private AI systems for regulated organisations.':'From AI pilot to real operations.','The decisions an enterprise AI initiative has to survive.':'The decisions that matter.','From a priority decision to a controlled production boundary.':'A clear path forward.','Controls belong in the product and operating model.':'Governance by design.','A useful engagement leaves decisions, owners and next checks behind.':'Clarity you can act on.','Product context and a public insight.':'Product meets practice.','Scope a governed AI deployment.':'Let’s define the next step.'},
'investors':{'AI Technical Due Diligence.':'Clarity before commitment.','Does the technical story hold together?':'Look beyond the demo.','Questions, not implied outcomes.':'Ask the harder questions.','A bounded technical review.':'A focused review.','A written view of what is known, open and risky.':'Evidence. Not assumptions.','Technical assessment, not investment advice.':'A technical view. A better-informed decision.'},
'founders':{'When product, architecture and engineering diverge.':'Product. Architecture. Aligned.','You may need a diagnostic when…':'Find the real constraint.','Start with the decision, then inspect the system around it.':'Turn complexity into a plan.','Concrete outputs for the next operating decision.':'A direction. And a next step.','Product-building context, stated narrowly.':'Grounded in the work.','A diagnostic is not fundraising or a growth promise.':'Start with a CTO diagnostic.'},
'about':{'Enterprise AI CTO and product operator.':'Vadim Vladymtsev.','Connect the product decision to the system that has to carry it.':'Product thinking. Engineering depth.','An engineering foundation built through teaching and competition.':'An engineering foundation.','Start with the decision that needs to be made.':'Let’s talk about your next decision.'},
'expert':{'Public expertise on governed enterprise AI.':'Ideas for real-world AI.','Every record has a format, date, role and direct source.':'Selected appearances.','Practical topics for enterprise audiences.':'Conversations that matter.','Reusable introductions using the current role.':'A few words about Vadim.','A clear route for editors and organisers.':'For editors & organisers.','Need a clear technical voice on enterprise AI?':'Bring the conversation forward.'},
'sources':{'Public sources':'The public record.','How to read these links.':'Context matters.'},
'404':{'This page is off the map.':'A different way forward.'}
}
LINES={'work':['Product.','Practice.','Perspective.'],'century':['Private AI.','Under your','control.'],'enterprise':['From AI pilot','to real','operations.'],'investors':['Clarity before','commitment.'],'founders':['Product.','Architecture.','Aligned.'],'about':['Vadim','Vladymtsev.'],'expert':['Ideas for','real-world AI.'],'sources':['The public','record.'],'404':['A different','way forward.']}
ICONS=[
'<rect x="4" y="4" width="6" height="6" rx="1"/><rect x="22" y="4" width="6" height="6" rx="1"/><rect x="13" y="23" width="6" height="6" rx="1"/><path d="M7 10v6h18v-6M16 16v7"/>',
'<path d="M16 3l11 5v8c0 6-7 11-11 13C12 27 5 22 5 16V8z"/><path d="M11 16l3 3 7-7"/>',
'<rect x="4" y="5" width="24" height="22" rx="3"/><path d="M4 12h24M11 12v15M17 18h6M17 22h4"/>',
'<path d="M10 9L3 16l7 7M22 9l7 7-7 7M19 5l-6 22"/>'
]
def icon(i):return '<svg class="edition-icon" viewBox="0 0 32 32" fill="none" stroke="currentColor" stroke-width="1.3" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">'+ICONS[i%4]+'</svg>'
def frag(h):return BeautifulSoup(h,'html.parser').find()
def addclass(n,*cl):n['class']=list(dict.fromkeys(n.get('class',[])+list(cl)))
def photo(src,cls='section-photograph'):
 return frag(f'<figure class="{cls}"><img src="assets/{src}" alt="" loading="lazy" decoding="async" width="1000" height="668" /></figure>')
def studio():
 return frag('''<figure class="studio-visual"><div class="studio-stage" aria-hidden="true">
 <div class="studio-halo"></div><div class="studio-window studio-window--rear"><div class="studio-toolbar"><span>◎ Century</span><span>Workflow architecture</span></div><div class="studio-flow"><div>Source</div><i>↓</i><div>Policy check</div><i>↓</i><div>Model / retrieval</div><i>↓</i><div>Human review</div></div></div>
 <div class="studio-window studio-window--front"><div class="studio-toolbar"><span>◎ Century</span><span>Private enterprise AI</span></div><div class="studio-layout"><div class="studio-sidebar"><span>Workspace</span><b>Overview</b><span>Assistants</span><span>Workflows</span><span>Data sources</span><span>Access &amp; audit</span><small>Architecture illustration</small></div><div class="studio-content"><div class="studio-heading">One operating boundary.<span>Models, data and work. Connected.</span></div><div class="studio-modules"><div><i>◇</i>Assistants<small>Source-grounded context</small></div><div><i>⌘</i>Workflows<small>Review &amp; escalation</small></div></div><div class="studio-system"><span>ACCESS BOUNDARY</span><div><b>Sources</b><i>→</i><b>Policies</b><i>→</i><b>Models</b></div></div><div class="studio-audit"><span>Operational control</span><div>Roles &amp; permissions<i>Defined access</i></div><div>Logs &amp; traces<i>Reviewable activity</i></div><div>Deployment<i>Private infrastructure</i></div></div></div></div></div></div><figcaption>Illustrative architecture · not a product screenshot.</figcaption></figure>''')
def memo():
 return frag('''<figure class="review-visual"><div class="review-stage" aria-hidden="true"><div class="review-glow"></div><div class="review-page review-page--rear"><span>TECHNICAL REVIEW</span><h3>Product.<br/>Data.<br/>Architecture.</h3><div class="report-lines"></div></div><div class="review-page review-page--front"><div class="report-head"><span>AI TECHNICAL DILIGENCE</span><span>01 / FRAMEWORK</span></div><h3>What holds up.<br/>What remains open.</h3><p>Evidence before the next commitment.</p><div class="report-list"><div><b>01</b>Product reality<span>↗</span></div><div><b>02</b>Data &amp; models<span>↗</span></div><div><b>03</b>Architecture<span>↗</span></div><div><b>04</b>Team execution<span>↗</span></div></div><div class="report-foot">Known <span>·</span> Open <span>·</span> At risk</div></div></div><figcaption>Illustrative review framework · not a completed assessment.</figcaption></figure>''')
for name,mapping in TITLES.items():
 file=ROOT/(name+'.html'); original=file.read_text(); main_html=re.search(r'<main\b[\s\S]*?</main>',original).group()
 soup=BeautifulSoup(main_html,'html.parser'); main=soup.main
 for h in main.select('h1,h2'):
  old=h.get_text(' ',strip=True)
  if old in mapping: h.clear();h.append(mapping[old])
 h1=main.h1;h1.clear()
 for line in LINES[name]:
  h1.append(frag('<span>'+line+'</span>'));h1.append(' ')
 hero=main.select_one('.inner-hero'); copy=hero.select_one('.inner-hero-copy')
 if name=='about': h1.insert_after(frag('<p class="hero-role">Enterprise AI CTO and product operator.</p>'))
 if name=='investors': h1.insert_before(frag('<p class="hero-role">AI Technical Due Diligence.</p>'))
 for v in main.select('.platform-visual'):v.replace_with(studio())
 for v in main.select('.memo-visual'):v.replace_with(memo())
 if name=='work':
  idx=hero.select_one('.work-hero-index');idx['class']=['page-index'];idx.name='nav';idx['aria-label']='On this page'
  idx.select_one('.visual-eyebrow').decompose(); idx.extract()
  wrap=frag('<div class="container"></div>');wrap.append(idx);hero.append(wrap)
  hero.select_one('.inner-hero-grid').append(photo('executive/architecture.webp','editorial-visual work-photograph'))
 for img in hero.select('.editorial-visual img'):img['loading']='eager'
 if name=='work':
  note=main.select_one('.role-note'); flagship=main.select_one('.flagship-work')
  if note and flagship: note.extract();flagship.insert_after(note)
  addclass(main.select_one('.work-feature-section'),'flagship-section')
 for sec in main.select('.assessment-section,.capabilities-section,.assurance-section,.deliverables-section,.topics-section'):
  for i,item in enumerate(sec.select('.editorial-item')):
   addclass(item,'edition-card');item.insert(0,frag(icon(i)))
  if 'capabilities-section' in sec.get('class',[]):
   for i,item in enumerate(sec.select('.editorial-item')):
    visual=['<div class="mini-chat"><i></i><i></i><i></i><span>Sources · Context · Response</span></div>', '<div class="mini-workflow"><i></i><b>→</b><i></i><b>→</b><i></i></div>', '<div class="mini-data"><i></i><i></i><i></i><i></i><i></i></div>', '<div class="mini-connect"><i>API</i><b>↔</b><i>Data</i></div>'][i%4]
    item.insert(0,frag('<div class="capability-art" aria-hidden="true">'+visual+'</div>'))
 for sec in main.select('.process-section'):addclass(sec,'edition-process')
 if name in ['about','work']:
  timeline=main.select_one('.timeline-section');tcontainer=timeline.select_one('.container')
  visual=photo('portraits/vadim-educator-720.webp','foundation-photo')
  tcontainer.append(visual)
 if name=='expert':
  for i,row in enumerate(main.select('.press-section .record-row')):
   addclass(row,'press-card');row.insert(0,photo(['executive/workspace.webp','executive/architecture.webp','executive/dubai.webp','executive/horizon.webp'][i],'press-cover'))
 if name=='century':addclass(main.select_one('.record-section'),'product-record')
 if name=='sources':
  for i,source in enumerate(main.select('.source-entry')):source.insert(0,frag(icon(i)))
 out=original[:original.index(main_html)]+str(main)+original[original.index(main_html)+len(main_html):]
 file.write_text(out)
(ROOT/'qa/editorial-titles.json').write_text(json.dumps({k+'.html':v for k,v in TITLES.items()},ensure_ascii=False,indent=2)+'\n')
f=ROOT/'qa/internal-content.mjs';t=f.read_text();t=t.replace("const original=JSON.parse(read('qa/executive-content-baseline.json'));", "const original=JSON.parse(read('qa/executive-content-baseline.json'));\nconst editorial=JSON.parse(read('qa/editorial-titles.json'));")
t=t.replace("for(const unit of before.text){assert.ok(text.includes(unit),`${file}: original content lost: ${unit}`);blocks++;}", "for(const [oldTitle,newTitle] of Object.entries(editorial[file]||{})){assert.ok(before.text.includes(oldTitle), `${file}: unknown editorial source heading`);assert.ok(text.includes(newTitle), `${file}: replacement heading missing: ${newTitle}`);}\n for(const unit of before.text){assert.ok(text.includes(editorial[file]?.[unit]||unit),`${file}: original content lost: ${unit}`);blocks++;}")
f.write_text(t)
(ROOT/'assets/internal.css').write_bytes(css)
f=ROOT/'qa/browser/check.mjs';t=f.read_text()
t=t.replace("{width:1024,height:900,name:'1024'},", "{width:1101,height:900,name:'1101'},\n  {width:1100,height:900,name:'1100'},\n  {width:1024,height:900,name:'1024'},")
t=t.replace("{width:768,height:1024,name:'768'},", "{width:768,height:1024,name:'768'},\n  {width:761,height:1024,name:'761'},\n  {width:760,height:1024,name:'760'},")
needle="if (route === 'about.html' && await page.locator('.profile-portrait img[src=\"assets/portraits/vadim-home-720.webp\"]').count() !== 1) throw new Error('About portrait missing');"
assert needle in t, 'Browser test anchor changed'
t=t.replace(needle, needle+'''
        const type = await page.locator('h1').evaluate(el => ({size:parseFloat(getComputedStyle(el).fontSize), family:getComputedStyle(el).fontFamily}));
        if (!type.family.includes('Playfair Display') || type.size < 37) throw new Error(`${route}: editorial headline hierarchy regressed`);
        if (route === 'century.html' || route === 'work.html') {
          if (await page.locator('.studio-visual .studio-window').count() !== 2) throw new Error(`${route}: missing layered architectural illustration`);
          if (!(await page.locator('.studio-visual figcaption').innerText()).includes('not a product screenshot')) throw new Error('Illustration boundary missing');
        }
''')
f.write_text(t)
print('Prepared reviewed editorial compositions; homepage and shared assets not modified.')
