import { readFileSync, mkdirSync } from 'node:fs';
import { resolve } from 'node:path';
import { chromium } from 'playwright';

const ROOT = resolve(new URL('../..', import.meta.url).pathname);
const portrait = readFileSync(resolve(ROOT, 'assets/portraits/vadim-boardroom-1536.webp')).toString('base64');
const variants = [
  ['og-home.png', 'Enterprise AI CTO · Product operator', 'Governed private AI for regulated organisations'],
  ['og-enterprise.png', 'Enterprise AI strategy & architecture', 'Private deployment · governance · controlled production'],
  ['og-diligence.png', 'AI technical due diligence', 'Product · data · architecture · deployment'],
  ['og-founder.png', 'CTO-level product & engineering support', 'For founders when delivery and architecture diverge'],
  ['og-century.png', 'Century AI Studio', 'Governed enterprise AI platform'],
  ['og-expert.png', 'Enterprise AI speaker & technical expert', 'Verified media, articles and programme work']
];
const escape = text => text.replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;');
const browser = await chromium.launch({headless:true});
try {
  const page = await browser.newPage({viewport:{width:1200,height:630}, deviceScaleFactor:1});
  for (const [file, title, subtitle] of variants) {
    const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="630" viewBox="0 0 1200 630">
      <defs><linearGradient id="shade" x1="0" x2="1"><stop offset="0" stop-color="#070708"/><stop offset=".56" stop-color="#070708" stop-opacity=".86"/><stop offset="1" stop-color="#070708" stop-opacity=".16"/></linearGradient></defs>
      <rect width="1200" height="630" fill="#070708"/><image href="data:image/webp;base64,${portrait}" x="600" y="0" width="600" height="630" preserveAspectRatio="xMidYMid slice"/><rect width="1200" height="630" fill="url(#shade)"/>
      <rect x="58" y="58" width="54" height="54" rx="14" fill="#10100f" stroke="#c7a45a" stroke-opacity=".55"/><text x="85" y="94" text-anchor="middle" font-family="Georgia,serif" font-size="22" fill="#f4efe3">VV</text>
      <text x="58" y="184" font-family="Arial,sans-serif" font-size="25" font-weight="700" letter-spacing="2" fill="#c7a45a">${escape(title)}</text>
      <text x="58" y="278" font-family="Georgia,serif" font-size="66" fill="#f4efe3">Vadim</text><text x="58" y="344" font-family="Georgia,serif" font-size="66" fill="#f4efe3">Vladymtsev</text>
      <text x="58" y="430" font-family="Arial,sans-serif" font-size="25" fill="#d2ccbf">${escape(subtitle)}</text>
      <text x="58" y="544" font-family="Arial,sans-serif" font-size="18" letter-spacing="1.8" fill="#a09b8e">VADIMOHKA.COM</text>
    </svg>`;
    await page.setContent(`<body style="margin:0;background:#070708">${svg}</body>`);
    await page.screenshot({path:resolve(ROOT, `assets/social/${file}`), type:'png'});
  }
} finally {
  await browser.close();
}
