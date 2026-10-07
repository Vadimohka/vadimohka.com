import { resolve } from 'node:path';

// Check element bounds as well as scrollWidth: overflow:hidden must not hide a regression.
export async function auditLayout(page, label) {
  const errors = await page.evaluate(() => {
    const failures = [];
    const width = document.documentElement.clientWidth;
    if (document.documentElement.scrollWidth > width + 1 || document.body.scrollWidth > width + 1) {
      failures.push('document overflows horizontally');
    }
    for (const node of document.querySelectorAll('header *, main *, footer *')) {
      const rect = node.getBoundingClientRect();
      if (!rect.width || !rect.height) continue;
      // Inline boxes have no clientWidth; Firefox may still report their scrollWidth.
      const clipped = node.clientWidth > 0 && node.scrollWidth > node.clientWidth + 2;
      if (rect.left < -1 || rect.right > width + 1 || clipped) {
        failures.push(`overflow/clipping: ${node.tagName}.${node.className} bounds=${rect.left}:${rect.right}, scroll/client=${node.scrollWidth}/${node.clientWidth}`);
      }
    }
    const containers = [...document.querySelectorAll('.nav, main > section > .container, .footer > .container')];
    const edges = new Set(containers.map(node => {
      const rect = node.getBoundingClientRect();
      return `${Math.round(rect.left)}:${Math.round(rect.width)}`;
    }));
    if (edges.size > 1) failures.push(`header/content/footer alignment: ${[...edges].join(', ')}`);
    for (const node of document.querySelectorAll('.hero-photo--portrait')) {
      const rect = node.getBoundingClientRect();
      if (Math.abs(rect.width / rect.height - 0.8) > 0.004) failures.push('portrait frame lost its 4:5 aspect ratio');
      if (getComputedStyle(node.querySelector('img')).objectFit !== 'contain') failures.push('portrait is cropped');
    }
    for (const node of document.querySelectorAll('.btn, .menu-toggle, .nav-links a')) {
      const rect = node.getBoundingClientRect();
      if (rect.width && rect.height && rect.height < 43.5) failures.push(`small touch target: ${node.className}`);
    }
    const hero = document.querySelector('.hero-photo img');
    if (hero && (!hero.complete || !hero.naturalWidth)) failures.push('hero image did not load');
    if (hero?.getAttribute('src').includes('vadim-home-720.webp')) {
      if (hero.naturalWidth !== 720 || hero.naturalHeight !== 900) failures.push('wrong homepage portrait dimensions');
      if (document.querySelector('link[rel="preload"][as="image"]')?.getAttribute('href') !== hero.getAttribute('src')) {
        failures.push('homepage preload does not match the visible portrait');
      }
    }
    return failures.slice(0, 12);
  });
  if (errors.length) throw new Error(`${label}: ${errors.join('; ')}`);
}

export async function checkResponsive({browser, page, BASE, ROOT, allPages}) {
  // A short landscape viewport must not strand the final navigation links below the screen.
  for (const viewport of [{width:568,height:320}, {width:844,height:390}, {width:320,height:568}]) {
    await page.setViewportSize(viewport);
    await page.goto(`${BASE}/index.html?browserqa=keyboard`, {waitUntil:'networkidle'});
    const button = page.locator('.menu-toggle');
    await button.focus();
    await page.keyboard.press('Enter');
    await page.waitForFunction(() => document.activeElement === document.querySelector('.nav-links a'));
    for (let i = 1; i < 7; i++) await page.keyboard.press('Tab');
    const lastVisible = await page.locator('.nav-links a').last().evaluate(node => {
      const link = node.getBoundingClientRect();
      const menu = node.parentElement.getBoundingClientRect();
      return document.activeElement === node && link.top >= menu.top && link.bottom <= menu.bottom + 1 && menu.bottom <= innerHeight;
    });
    if (!lastVisible) throw new Error(`${viewport.width}x${viewport.height}: last menu link is not keyboard-reachable within the viewport`);
    await page.screenshot({path:resolve(ROOT, `qa/screenshots/T08-menu-${viewport.width}x${viewport.height}.png`)});
    await page.keyboard.press('Escape');
    await page.waitForFunction(() => document.activeElement === document.querySelector('.menu-toggle') && document.querySelector('.nav-links').hidden);
    await page.keyboard.press('Space');
    await page.waitForFunction(() => !document.querySelector('.nav-links').hidden);
    await page.locator('main').focus();
    await page.waitForFunction(() => document.querySelector('.nav-links').hidden);
    await button.click();
    await page.mouse.click(1, viewport.height - 1);
    await page.waitForFunction(() => document.querySelector('.nav-links').hidden);
  }

  // Focus must never remain on the hidden toggle or a newly hidden navigation link after resize.
  await page.setViewportSize({width:390,height:844});
  await page.goto(`${BASE}/index.html?browserqa=resize`, {waitUntil:'networkidle'});
  await page.locator('.menu-toggle').focus();
  await page.setViewportSize({width:1440,height:1000});
  await page.waitForFunction(() => document.activeElement === document.querySelector('.nav-links a'));
  await page.setViewportSize({width:390,height:844});
  await page.waitForFunction(() => document.activeElement === document.querySelector('.menu-toggle') && document.querySelector('.nav-links').hidden);

  const noJs = await browser.newContext({javaScriptEnabled:false,viewport:{width:320,height:568}});
  const fallback = await noJs.newPage();
  for (const route of allPages) {
    await fallback.goto(`${BASE}/${route}?browserqa=nojs-content`, {waitUntil:'networkidle'});
    await auditLayout(fallback, `${route} without JavaScript`);
    const state = await fallback.evaluate(() => ({
      invisible: [...document.querySelectorAll('main .reveal')].some(node => getComputedStyle(node).opacity !== '1'),
      overlap: document.querySelector('.brand').getBoundingClientRect().bottom > document.querySelector('.nav-links').getBoundingClientRect().top,
      links: [...document.querySelectorAll('.nav-links a')].filter(node => node.getBoundingClientRect().height >= 44).length
    }));
    if (state.invisible || state.overlap || state.links !== 7) throw new Error(`${route}: no-JavaScript content/navigation is unusable (${JSON.stringify(state)})`);
  }
  await fallback.goto(`${BASE}/index.html?browserqa=nojs-screenshot`, {waitUntil:'networkidle'});
  await fallback.screenshot({path:resolve(ROOT, 'qa/screenshots/T08-home-nojs-320.png'),fullPage:true});
  await noJs.close();

  // Scroll each real reveal into view, rather than forcing opacity for screenshots.
  for (const width of [390,1440]) {
    await page.setViewportSize({width,height:width === 390 ? 844 : 1000});
    for (const route of allPages) {
      await page.goto(`${BASE}/${route}?browserqa=full-page`, {waitUntil:'networkidle'});
      await page.addStyleTag({content:'html{scroll-behavior:auto!important}'});
      for (const node of await page.locator('.reveal').all()) {
        await node.evaluate(el => el.scrollIntoView({block:'center',behavior:'instant'}));
        await page.waitForFunction(el => el.classList.contains('is-visible'), await node.elementHandle());
      }
      await page.evaluate(() => window.scrollTo({top:0,behavior:'instant'}));
      await page.waitForTimeout(700);
      const invisible = await page.locator('main .reveal').evaluateAll(nodes => nodes.some(node => getComputedStyle(node).opacity !== '1'));
      if (invisible) throw new Error(`${route} ${width}: content stayed transparent after scrolling`);
      await auditLayout(page, `${route} ${width} after scrolling`);
      await page.screenshot({path:resolve(ROOT, `qa/screenshots/T08-${route.replace('.html','')}-${width}-full.png`),fullPage:true});
    }
  }
  await page.goto(`${BASE}/index.html?browserqa=pointer`, {waitUntil:'networkidle'});
  await page.mouse.move(1439,999);
  await auditLayout(page, 'pointer at bottom-right edge');
}
