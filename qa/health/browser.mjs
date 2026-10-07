import assert from 'node:assert/strict';
import {readFileSync} from 'node:fs';
export async function checkHealthInteractions({page,browser,BASE}){
  await page.setViewportSize({width:390,height:844});
  await page.goto(`${BASE}/about.html`,{waitUntil:'networkidle'});
  for(const link of await page.locator('.route-link').all())assert.match(await link.getAttribute('aria-label'),/^Choose this route:/);
  for(const id of ['finance-mail','vaiti','it-security']){
    await page.goto(`${BASE}/sources.html#${id}`,{waitUntil:'networkidle'});
    const link=page.locator(`#${id}`);assert.equal(await link.count(),1);
    const destination=await link.getAttribute('href');assert.ok(destination.startsWith('https://')&&!destination.includes('vadimohka.com/sources.html'));
  }
  for(const locale of ['en-US','en-AE']){
    const ctx=await browser.newContext({locale,viewport:{width:412,height:915},deviceScaleFactor:2});
    const p=await ctx.newPage();await p.goto(`${BASE}/enterprise.html`,{waitUntil:'networkidle'});
    assert.ok((await p.locator('.market-focus').innerText()).includes('United Arab Emirates'));
    assert.equal(await p.locator('html').getAttribute('lang'),'en');
    assert.ok((await p.locator('.editorial-visual img').first().evaluate(e=>e.complete&&e.naturalWidth>0)));
    await ctx.close();
  }
  const html=readFileSync(new URL('../../404.html',import.meta.url),'utf8');
  await page.route('**/missing/nested/page',route=>route.fulfill({status:404,contentType:'text/html',body:html}));
  await page.goto(`${BASE}/missing/nested/page`,{waitUntil:'networkidle'});
  assert.equal(await page.evaluate(()=>new URL(document.querySelector('link[rel="stylesheet"]').href).pathname),'/assets/site.css');
  assert.ok(await page.evaluate(()=>document.fonts.check('20px "Playfair Display"')));
  await page.unroute('**/missing/nested/page');
  console.log('PASS — market locales, source anchors, accessible inquiry labels and nested 404 assets');
}
