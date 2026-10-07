import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium, firefox, webkit } from 'playwright';
import { auditLayout, checkResponsive } from './responsive.mjs';
import '../executive-content.mjs';
import {checkHealthInteractions} from '../health/browser.mjs';
import AxeBuilder from '@axe-core/playwright';

const ROOT = resolve(new URL('../..', import.meta.url).pathname);
const BASE = 'http://127.0.0.1:4173';
const viewports = [
  {width:375,height:812,name:'375'},
  {width:412,height:915,name:'412'},
  {width:414,height:896,name:'414'},
  {width:820,height:1180,name:'820'},
  {width:834,height:1194,name:'834'},
  {width:1920,height:1080,name:'1920'},
  {width:1440,height:1000,name:'1440'},
  {width:1280,height:800,name:'1280'},
  {width:1151,height:900,name:'1151'},
  {width:1150,height:900,name:'1150'},
  {width:1101,height:900,name:'1101'},
  {width:1100,height:900,name:'1100'},
  {width:1024,height:768,name:'1024'},
  {width:901,height:768,name:'901'},
  {width:900,height:768,name:'900'},
  {width:768,height:1024,name:'768'},
  {width:761,height:1024,name:'761'},
  {width:760,height:1024,name:'760'},
  {width:701,height:900,name:'701'},
  {width:700,height:900,name:'700'},
  {width:640,height:960,name:'640'},
  {width:480,height:800,name:'480'},
  {width:430,height:932,name:'430'},
  {width:390,height:844,name:'390'},
  {width:360,height:780,name:'360'},
  {width:320,height:568,name:'320'},
  {width:844,height:390,name:'landscape-844'},
  {width:568,height:320,name:'landscape-568'}
];
const allPages = ['index.html','about.html','work.html','century.html','enterprise.html','investors.html','founders.html','expert.html','sources.html','404.html'];

const server = spawn('python3', ['-m', 'http.server', '4173', '--bind', '127.0.0.1'], {cwd:ROOT, stdio:'ignore'});
server.unref();
const stopServer = () => server.kill('SIGTERM');
process.on('exit', stopServer);
await new Promise(resolveReady => setTimeout(resolveReady, 500));

const browserName = process.env.BROWSER || 'chromium';
const browserType = {chromium, firefox, webkit}[browserName];
if (!browserType) throw new Error(`Unsupported BROWSER: ${browserName}`);
const browser = await browserType.launch({headless:true});
mkdirSync(resolve(ROOT, 'qa/screenshots'), {recursive:true});
try {
  const page = await browser.newPage();
  for (const viewport of viewports) {
    await page.setViewportSize({width:viewport.width,height:viewport.height});
    await page.goto(`${BASE}/index.html?browserqa=${viewport.name}`, {waitUntil:'networkidle'});
    const overflow = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
    if (overflow) throw new Error(`${viewport.name}: document-level horizontal overflow`);
    if (viewport.width <= 1150) {
      const menu = page.getByRole('button', {name:'Menu'});
      await menu.click();
      if (await menu.getAttribute('aria-expanded') !== 'true') throw new Error(`${viewport.name}: menu did not open`);
      if (await page.locator('.nav-links[hidden]').count()) throw new Error(`${viewport.name}: menu links remain hidden after open`);
      await page.locator('.nav-links a').first().press('Escape');
      if (await menu.getAttribute('aria-expanded') !== 'false') throw new Error(`${viewport.name}: Escape did not close menu`);
      if (await page.evaluate(() => document.activeElement?.className) !== 'menu-toggle') throw new Error(`${viewport.name}: focus did not return to menu button`);
    } else if (await page.getByRole('button', {name:'Menu'}).isVisible()) {
      throw new Error(`${viewport.name}: mobile menu button visible on desktop`);
    }
    await page.evaluate(() => document.fonts.ready);
    const loadedFonts = await page.evaluate(() => [...document.fonts].filter(font => font.status === 'loaded').map(font => font.family.replace(/["']/g,'')));
    if (!['Playfair Display','DM Sans'].every(font => loadedFonts.includes(font))) throw new Error(`${viewport.name}: the specified web typography did not load`);
    await page.locator('main img').evaluateAll(images => Promise.all(images.filter(image => image.loading !== 'lazy').map(image => image.decode())));
    await page.screenshot({path:resolve(ROOT, `qa/screenshots/T08-home-${viewport.name}.png`), fullPage:false});
  }

  // Every published page must use the same container edge for its sections.
  // This catches a centered/narrow closing block that can look correct in isolation.
  for (const viewport of viewports) {
    await page.setViewportSize({width:viewport.width,height:viewport.height});
    for (const route of allPages) {
      await page.goto(`${BASE}/${route}?browserqa=alignment`, {waitUntil:'networkidle'});
      await auditLayout(page, `${route} ${viewport.name}`);
      if (route === 'index.html') {
        const caption = await page.locator('.product-stage figcaption').boundingBox();
        const front = await page.locator('.screen-front').boundingBox();
        if (front.y + front.height > caption.y - 4) throw new Error(`${viewport.name}: product illustration overlaps its disclosure`);
        await page.locator('.mandate-details').evaluate(node => { node.open = true; });
        await auditLayout(page, `${route} ${viewport.name} expanded mandate`);
        await page.locator('.mandate-details').evaluate(node => { node.open = false; });
      }
      const alignment = await page.evaluate(() => {
        const boxes = [...document.querySelectorAll('main > section > .container')].map(node => {
          const rect = node.getBoundingClientRect();
          return {x:Math.round(rect.x), width:Math.round(rect.width)};
        });
        return {
          overflow: document.documentElement.scrollWidth > window.innerWidth + 1,
          edges: [...new Set(boxes.map(box => `${box.x}:${box.width}`))],
          heroImage: document.querySelector('main > section .hero-photo img')?.getAttribute('src') || ''
        };
      });
      if (alignment.overflow) throw new Error(`${route} ${viewport.name}: horizontal overflow`);
      if (alignment.edges.length > 1) throw new Error(`${route} ${viewport.name}: section containers are misaligned (${alignment.edges.join(', ')})`);
      if (route === 'index.html') {
        if (!alignment.heroImage.includes('vadim-home-720.webp')) throw new Error('Homepage portrait changed');
        if (await page.locator('link[href="assets/internal.css"]').count()) throw new Error('Internal CSS leaked onto the homepage');
      } else {
        if (await page.locator('.inner-hero').count() !== 1) throw new Error(`${route}: missing internal-page composition`);
        if (await page.locator('.hero-photo').count()) throw new Error(`${route}: old repeated portrait layout returned`);
        if (route === 'about.html' && await page.locator('.profile-portrait img[src="assets/portraits/vadim-home-720.webp"]').count() !== 1) throw new Error('About portrait missing');
        const type = await page.locator('h1').evaluate(el => ({size:parseFloat(getComputedStyle(el).fontSize), family:getComputedStyle(el).fontFamily}));
        if (!type.family.includes('Playfair Display') || type.size < 37) throw new Error(`${route}: editorial headline hierarchy regressed`);
        const brokenNumbers = await page.locator('.page-index a span:first-child').evaluateAll(ns => ns.filter(n => n.offsetHeight > parseFloat(getComputedStyle(n).lineHeight) + 1).length);
        if (brokenNumbers) throw new Error(`${route} ${viewport.name}: chapter numbers wrap`);
        if (route === 'investors.html') {
          const inset = await page.locator('.review-page--front').evaluate(el => { const f=el.querySelector('.report-foot'); return el.clientHeight - f.offsetTop - f.offsetHeight; });
          if (inset < 8) throw new Error(`${route} ${viewport.name}: illustrated document content clips (${inset}px inset)`);
        }

        if (route === 'century.html' || route === 'work.html') {
          if (await page.locator('.studio-visual .studio-window').count() !== 2) throw new Error(`${route}: missing layered architectural illustration`);
          if (!(await page.locator('.studio-visual figcaption').innerText()).includes('not a product screenshot')) throw new Error('Illustration boundary missing');
        }

      }
      if (route === 'index.html' && viewport.name === '1440') {
        const sectionCount = await page.locator('main > section').count();
        const heroWidth = await page.locator('main > section.hero .hero-photo').evaluate(el => Math.round(el.getBoundingClientRect().width));
        if (sectionCount > 7) throw new Error(`index.html ${viewport.name}: homepage is too long (${sectionCount} sections)`);
        // The reference uses a larger, intentionally art-directed portrait; the original image file is retained.
        if (heroWidth < 500 || heroWidth > 560) throw new Error(`index.html ${viewport.name}: portrait scale is outside the executive layout (${heroWidth}px)`);
        if (await page.locator('main img[src*="vadim-home-"]').count() !== 1) throw new Error('index.html: duplicate portrait reintroduced');
        if (await page.locator('.insight img').count() !== 3) throw new Error('index.html: editorial image triptych is missing');
        const order = await page.locator('main > section').evaluateAll(nodes => nodes.map(n => n.getAttribute('aria-labelledby')));
        if (JSON.stringify(order) !== JSON.stringify([null, 'century-title', 'relevance-title', 'mandate-title', 'public-work-title', 'action-title'])) throw new Error('index.html: product-first section order changed');
        const recognitionCount = await page.getByText(/3rd place, AI Product Leader/i).count();
        if (recognitionCount > 1) throw new Error(`index.html ${viewport.name}: recognition is repeated ${recognitionCount} times`);
      }
      if (route === 'index.html' && await page.locator('section[aria-labelledby="outcomes-title"]').count()) {
        throw new Error('index.html: selected outcome block should be removed');
      }
      if (viewport.name === '1440') {
        const cardCount = await page.locator('.card').count();
        if (cardCount) {
          const cardStyle = await page.locator('.card').first().evaluate(el => {
            const style = getComputedStyle(el);
            return {padding: parseFloat(style.paddingTop), columnGap: parseFloat(getComputedStyle(el.parentElement).columnGap), rowGap: parseFloat(getComputedStyle(el.parentElement).rowGap)};
          });
          if (cardStyle.padding < 22) throw new Error(`${route} ${viewport.name}: card padding is too tight (${cardStyle.padding}px)`);
          if (cardStyle.columnGap < 16 || cardStyle.rowGap < 16) throw new Error(`${route} ${viewport.name}: card gap is too tight (${cardStyle.columnGap}px/${cardStyle.rowGap}px)`);
        }
        const articleCount = await page.locator('.article').count();
        if (articleCount) {
          const articleStyle = await page.locator('.article').first().evaluate(el => ({padding:parseFloat(getComputedStyle(el).paddingTop), gap:parseFloat(getComputedStyle(el).gap)}));
          if (articleStyle.padding < 22) throw new Error(`${route} ${viewport.name}: article card padding is too tight (${articleStyle.padding}px)`);
          if (articleStyle.gap < 16) throw new Error(`${route} ${viewport.name}: article card gap is too tight (${articleStyle.gap}px)`);
        }
        const tightGroups = await page.locator('.cards, .article-list').evaluateAll(elements => elements
          .filter(el => !el.closest('.split') && !el.matches('.advisory-grid'))
          .map(el => ({className: el.className, marginTop: parseFloat(getComputedStyle(el).marginTop)}))
          .filter(item => item.marginTop < 20));
        const advisoryGap = await page.locator('.advisory-grid').evaluateAll(groups => groups.map(group => group.getBoundingClientRect().top - group.previousElementSibling.getBoundingClientRect().bottom));
        if (advisoryGap.some(gap => gap < 20)) throw new Error(`${route}: advisory heading gap is too tight`);
        if (tightGroups.length) throw new Error(`${route} ${viewport.name}: heading-to-card/list spacing is too tight (${tightGroups.map(item => `${item.className}:${item.marginTop}px`).join(', ')})`);
      }
    }
  }

  await page.setViewportSize({width:390,height:844});
  await page.goto(`${BASE}/index.html?browserqa=skip`, {waitUntil:'networkidle'});
  await page.keyboard.press('Tab');
  if (await page.evaluate(() => document.activeElement?.className) !== 'skip-link') throw new Error('first Tab did not reveal skip link');
  await page.keyboard.press('Enter');
  if (await page.evaluate(() => document.activeElement?.id) !== 'main-content') throw new Error('skip link did not focus main content');

  const contactContext = await browser.newContext({viewport:{width:390,height:844}});
  const contact = await contactContext.newPage();
  await contact.goto(`${BASE}/about.html#contact?browserqa=contact`, {waitUntil:'networkidle'});
  if (await contact.locator('[data-route-response]').count() !== 1) throw new Error('about page missing contact route response');
  for (const intent of ['enterprise','diligence','founder','executive','media','speaking']) {
    await contact.goto(`${BASE}/about.html?intent=${intent}#contact`, {waitUntil:'networkidle'});
    const selected = await contact.locator('.intent-card.is-selected').getAttribute('data-intent');
    if (selected !== intent) throw new Error(`contact intent ${intent} selected ${selected}`);
    const before = await contact.url();
    await contact.locator(`[data-intent="${intent}"] a`).click();
    if (await contact.url() !== before) throw new Error(`contact intent ${intent} unexpectedly navigated`);
    if (await contact.locator('[data-route-response]').getAttribute('data-active-route') !== intent) throw new Error(`contact intent ${intent} did not update response`);
    if (await contact.locator('form').count()) throw new Error('contact page unexpectedly contains a form');
  }
  await contactContext.close();

  for (const width of [320, 768, 1440]) {
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

  const noJs = await browser.newContext({javaScriptEnabled:false, viewport:{width:320,height:568}});
  const noJsPage = await noJs.newPage();
  await noJsPage.goto(`${BASE}/index.html?browserqa=nojs`, {waitUntil:'networkidle'});
  if (await noJsPage.locator('.nav-links a').count() !== 7) throw new Error('JavaScript-disabled navigation lost links');
  if (await noJsPage.locator('.nav-links').getAttribute('hidden') !== null) throw new Error('JavaScript-disabled navigation is hidden');
  await noJs.close();

  const reduced = await browser.newContext({reducedMotion:'reduce', viewport:{width:390,height:844}});
  const reducedPage = await reduced.newPage();
  await reducedPage.goto(`${BASE}/index.html?browserqa=reduced`, {waitUntil:'networkidle'});
  const motion = await reducedPage.evaluate(() => getComputedStyle(document.querySelector('.btn')).transitionDuration);
  if (motion !== '0s') throw new Error(`reduced-motion button transition is ${motion}`);
  await reduced.close();

  const axeContext = await browser.newContext({viewport:{width:1440,height:1000}});
  const axePage = await axeContext.newPage();
  for (const route of allPages) {
    await axePage.goto(`${BASE}/${route}?browserqa=axe`, {waitUntil:'networkidle'});
    // Audit the final rendered content, not a transient opacity during a reveal.
    await axePage.addStyleTag({content:'html{scroll-behavior:auto!important}'});
    for (const node of await axePage.locator('.reveal').all()) {
      await node.evaluate(el => el.scrollIntoView({block:'center',behavior:'instant'}));
      await axePage.waitForFunction(el => getComputedStyle(el).opacity === '1', await node.elementHandle());
    }
    await axePage.evaluate(() => window.scrollTo({top:0,behavior:'instant'}));
    await axePage.waitForFunction(() => [...document.querySelectorAll('main .reveal')].every(node => getComputedStyle(node).opacity === '1'));
    const results = await new AxeBuilder({page:axePage}).withTags(['wcag2a','wcag2aa']).analyze();
    const serious = results.violations.filter(v => v.impact === 'serious' || v.impact === 'critical');
    if (serious.length) throw new Error(`${route}: axe serious/critical violations: ${JSON.stringify(serious.map(v => ({id:v.id,nodes:v.nodes.map(n => ({target:n.target,summary:n.failureSummary}))})))}`);
  }
  await axeContext.close();
  await checkHealthInteractions({page, browser, BASE});
  await checkResponsive({browser, page, BASE, ROOT, allPages, viewports});
  console.log(`PASS — ${browserName} browser QA covered ${viewports.length} viewports, menu/skip/no-JS/reduced-motion/contact routes and axe`);
} finally {
  await browser.close();
  stopServer();
}

