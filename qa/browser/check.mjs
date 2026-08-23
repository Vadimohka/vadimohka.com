import { spawn } from 'node:child_process';
import { mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';
import AxeBuilder from '@axe-core/playwright';

const ROOT = resolve(new URL('../..', import.meta.url).pathname);
const BASE = 'http://127.0.0.1:4173';
const viewports = [
  {width:1440,height:1000,name:'1440'},
  {width:1024,height:768,name:'1024'},
  {width:768,height:1024,name:'768'},
  {width:390,height:844,name:'390'},
  {width:320,height:568,name:'320'}
];
const allPages = ['index.html','about.html','work.html','century.html','enterprise.html','investors.html','founders.html','expert.html','sources.html','404.html'];

const server = spawn('python3', ['-m', 'http.server', '4173', '--bind', '127.0.0.1'], {cwd:ROOT, stdio:'ignore'});
server.unref();
const stopServer = () => server.kill('SIGTERM');
process.on('exit', stopServer);
await new Promise(resolveReady => setTimeout(resolveReady, 500));

const browser = await chromium.launch({headless:true});
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
    await page.screenshot({path:resolve(ROOT, `qa/screenshots/T08-home-${viewport.name}.png`), fullPage:false});
  }

  // Every published page must use the same container edge for its sections.
  // This catches a centered/narrow closing block that can look correct in isolation.
  for (const viewport of viewports) {
    await page.setViewportSize({width:viewport.width,height:viewport.height});
    for (const route of allPages) {
      await page.goto(`${BASE}/${route}?browserqa=alignment`, {waitUntil:'networkidle'});
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
      const expectedHero = route === 'founders.html'
        ? 'vadim-educator-1122.webp'
        : (route === 'index.html' || route === 'enterprise.html' ? 'vadim-boardroom-1536.webp' : 'vadim-warm-1536.webp');
      if (!alignment.heroImage.includes(expectedHero)) throw new Error(`${route} ${viewport.name}: expected hero portrait is missing`);
      if (route === 'index.html' && viewport.name === '1440') {
        const sectionCount = await page.locator('main > section').count();
        const heroWidth = await page.locator('main > section.hero .hero-photo').evaluate(el => Math.round(el.getBoundingClientRect().width));
        if (sectionCount > 7) throw new Error(`index.html ${viewport.name}: homepage is too long (${sectionCount} sections)`);
        if (heroWidth < 470) throw new Error(`index.html ${viewport.name}: hero portrait is too narrow (${heroWidth}px)`);
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
          .filter(el => !el.closest('.split'))
          .map(el => ({className: el.className, marginTop: parseFloat(getComputedStyle(el).marginTop)}))
          .filter(item => item.marginTop < 20));
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

  const noJs = await browser.newContext({javaScriptEnabled:false, viewport:{width:320,height:568}});
  const noJsPage = await noJs.newPage();
  await noJsPage.goto(`${BASE}/index.html?browserqa=nojs`, {waitUntil:'networkidle'});
  if (await noJsPage.locator('.nav-links a').count() !== 7) throw new Error('JavaScript-disabled navigation lost links');
  if (await noJsPage.locator('.nav-links').getAttribute('hidden') !== null) throw new Error('JavaScript-disabled navigation is hidden');
  await noJs.close();

  const reduced = await browser.newContext({reducedMotion:'reduce', viewport:{width:390,height:844}});
  const reducedPage = await reduced.newPage();
  await reducedPage.goto(`${BASE}/index.html?browserqa=reduced`, {waitUntil:'networkidle'});
  const motion = await reducedPage.evaluate(() => getComputedStyle(document.querySelector('.reveal')).transitionDuration);
  if (motion !== '0s') throw new Error(`reduced-motion reveal transition is ${motion}`);
  await reduced.close();

  const axeContext = await browser.newContext({viewport:{width:1440,height:1000}});
  const axePage = await axeContext.newPage();
  for (const route of ['index.html','about.html','work.html']) {
    await axePage.goto(`${BASE}/${route}?browserqa=axe`, {waitUntil:'networkidle'});
    const results = await new AxeBuilder({page:axePage}).withTags(['wcag2a','wcag2aa']).analyze();
    const serious = results.violations.filter(v => v.impact === 'serious' || v.impact === 'critical');
    if (serious.length) throw new Error(`${route}: axe serious/critical violations: ${serious.map(v => v.id).join(', ')}`);
  }
  await axeContext.close();
  console.log(`PASS — browser QA covered ${viewports.length} viewports, menu/skip/no-JS/reduced-motion/contact routes and axe`);
} finally {
  await browser.close();
}
