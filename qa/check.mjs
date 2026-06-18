// Static QA for the site — pure Node, no browser, no dependencies.
// Run from repo root:  node qa/check.mjs
// Checks: pages exist, internal links + assets resolve, one <h1>, title +
// meta description, canonical/OG/Twitter, lang, alt + width/height on images,
// duplicate ids, empty href, absolute local paths, stylesheet present,
// rough <div> nesting balance, sitemap + robots.
import { readFileSync, existsSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const PAGES = ['index.html','enterprise.html','founders.html','investors.html','origin.html',
  'century.html','proof.html','writing.html','contact.html','sources.html','404.html'];

let fails = 0;
const fail = (p, msg) => { console.error(`  ✗ ${p}: ${msg}`); fails++; };
const read = f => readFileSync(resolve(ROOT, f), 'utf8');
const matches = (re, s) => [...s.matchAll(re)];

for (const page of PAGES) {
  if (!existsSync(resolve(ROOT, page))) { fail(page, 'file missing'); continue; }
  const html = read(page);

  const title = html.match(/<title>([^<]*)<\/title>/);
  if (!title || !title[1].trim()) fail(page, 'missing/empty <title>');

  const desc = html.match(/<meta name="description" content="([^"]*)"/);
  if (!desc || !desc[1].trim()) fail(page, 'missing/empty meta description');

  if (!/<html[^>]*\blang="[^"]+"/.test(html)) fail(page, 'missing <html lang>');

  const h1s = matches(/<h1\b/g, html).length;
  if (h1s !== 1) fail(page, `expected exactly one <h1>, found ${h1s}`);

  if (!/property="og:title"/.test(html)) fail(page, 'missing og:title');
  if (!/property="og:image"/.test(html)) fail(page, 'missing og:image');
  if (!/name="twitter:card"/.test(html)) fail(page, 'missing twitter:card');
  if (page !== '404.html' && !/rel="canonical"/.test(html)) fail(page, 'missing canonical');

  // images: alt + intrinsic dimensions + resolvable src
  for (const m of matches(/<img\b[^>]*>/g, html)) {
    const tag = m[0];
    const src = (tag.match(/\bsrc="([^"]*)"/) || [])[1] || '(no src)';
    if (!/\balt=/.test(tag)) fail(page, `img missing alt: ${src}`);
    if (!/\bwidth=/.test(tag) || !/\bheight=/.test(tag)) fail(page, `img missing width/height: ${src}`);
    if (src && !/^https?:/.test(src) && !existsSync(resolve(ROOT, src))) fail(page, `img src not found: ${src}`);
  }

  // links: resolve internal, flag empty + absolute-local
  for (const m of matches(/\bhref="([^"]*)"/g, html)) {
    const href = m[1];
    if (href.trim() === '') { fail(page, 'empty href'); continue; }
    if (/^(https?:|mailto:|tel:|#|data:)/.test(href)) continue;
    if (href.startsWith('//')) continue;
    if (href.startsWith('/')) { fail(page, `absolute local path (breaks project pages): ${href}`); continue; }
    const path = href.split(/[?#]/)[0];
    if (path && !existsSync(resolve(ROOT, path))) fail(page, `internal link not found: ${href}`);
  }

  // stylesheet target exists
  for (const m of matches(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g, html)) {
    if (!/^https?:/.test(m[1]) && !existsSync(resolve(ROOT, m[1]))) fail(page, `stylesheet not found: ${m[1]}`);
  }

  // duplicate ids
  const ids = matches(/\bid="([^"]+)"/g, html).map(m => m[1]);
  const dup = ids.filter((id, i) => ids.indexOf(id) !== i);
  if (dup.length) fail(page, `duplicate id(s): ${[...new Set(dup)].join(', ')}`);

  // rough nesting sanity
  const opens = matches(/<div\b/g, html).length, closes = matches(/<\/div>/g, html).length;
  if (opens !== closes) fail(page, `<div> imbalance: ${opens} open vs ${closes} close`);
}

// sitemap + robots
const sm = existsSync(resolve(ROOT, 'sitemap.xml')) ? read('sitemap.xml') : '';
if (!sm) fail('sitemap.xml', 'missing');
else for (const p of PAGES.filter(p => p !== '404.html'))
  if (!sm.includes(p)) fail('sitemap.xml', `does not list ${p}`);
const robots = existsSync(resolve(ROOT, 'robots.txt')) ? read('robots.txt') : '';
if (!robots) fail('robots.txt', 'missing');
else if (!/Sitemap:/i.test(robots)) fail('robots.txt', 'missing Sitemap: reference');

console.log(fails ? `\nFAIL — ${fails} issue(s)` : `\nPASS — ${PAGES.length} pages, all static checks green`);
process.exit(fails ? 1 : 0);
