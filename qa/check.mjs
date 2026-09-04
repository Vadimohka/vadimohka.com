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
const PAGES = ['index.html','enterprise.html','founders.html','investors.html',
  'century.html','expert.html','sources.html','404.html','work.html','about.html'];

let fails = 0;
const fail = (p, msg) => { console.error(`  ✗ ${p}: ${msg}`); fails++; };
const read = f => readFileSync(resolve(ROOT, f), 'utf8');
const matches = (re, s) => [...s.matchAll(re)];
const personCores = [];
const PRODUCTION_FILES = [...PAGES, 'assets/site.css', 'assets/site.js', 'ai-profile.md', 'llms.txt', 'llms-full.txt', 'data/entity-graph.json', 'sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml', 'robots.txt'];
const imageDimensions = file => {
  const bytes = readFileSync(resolve(ROOT, file));
  if (bytes.subarray(0, 8).toString('hex') === '89504e470d0a1a0a') return [bytes.readUInt32BE(16), bytes.readUInt32BE(20)];
  if (bytes[0] === 0xff && bytes[1] === 0xd8) {
    let offset = 2;
    while (offset + 9 < bytes.length) {
      if (bytes[offset] !== 0xff) { offset++; continue; }
      const marker = bytes[offset + 1];
      const length = bytes.readUInt16BE(offset + 2);
      if (marker >= 0xc0 && marker <= 0xc3) return [bytes.readUInt16BE(offset + 7), bytes.readUInt16BE(offset + 5)];
      offset += 2 + length;
    }
  }
  return null;
};

for (const page of PAGES) {
  if (!existsSync(resolve(ROOT, page))) { fail(page, 'file missing'); continue; }
  const html = read(page);
  // structured data: every block must parse and reuse the stable person identity
  const jsonld = matches(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g, html);
  if (!jsonld.length) fail(page, 'missing JSON-LD');
  for (const block of jsonld) {
    try {
      const node = JSON.parse(block[1]);
      if (node['@type'] === 'Person') {
        if (node['@id'] !== 'https://vadimohka.com/#person') fail(page, 'Person JSON-LD has unstable @id');
        const servedMarkets = (node.areaServed || []).map(area => area.name).sort();
        if (JSON.stringify(servedMarkets) !== JSON.stringify(['United Arab Emirates', 'United States'])) {
          fail(page, 'Person JSON-LD must identify United States and United Arab Emirates as areas served');
        }
        personCores.push(JSON.stringify({name:node.name,jobTitle:node.jobTitle,sameAs:node.sameAs,worksFor:node.worksFor,areaServed:servedMarkets}));
      }
      if (node['@type'] === 'WebPage' && node.inLanguage !== 'en') fail(page, 'WebPage JSON-LD missing inLanguage=en');
      if (page === 'century.html' && node['@type'] === 'SoftwareApplication' && node['@id'] !== 'https://vadimohka.com/#century') fail(page, 'Century schema has unstable @id');
    } catch (error) {
      fail(page, `invalid JSON-LD: ${error.message}`);
    }
  }

  const title = html.match(/<title>([^<]*)<\/title>/);
  if (!title || !title[1].trim()) fail(page, 'missing/empty <title>');

  const desc = html.match(/<meta name="description" content="([^"]*)"/);
  if (!desc || !desc[1].trim()) fail(page, 'missing/empty meta description');
  const ogTitle = html.match(/<meta property="og:title" content="([^"]*)"/);
  const twitterTitle = html.match(/<meta name="twitter:title" content="([^"]*)"/);
  const ogDesc = html.match(/<meta property="og:description" content="([^"]*)"/);
  const twitterDesc = html.match(/<meta name="twitter:description" content="([^"]*)"/);
  if (title && ogTitle && title[1] !== ogTitle[1]) fail(page, 'og:title differs from title');
  if (title && twitterTitle && title[1] !== twitterTitle[1]) fail(page, 'twitter:title differs from title');
  if (desc && ogDesc && desc[1] !== ogDesc[1]) fail(page, 'og:description differs from meta description');
  if (desc && twitterDesc && desc[1] !== twitterDesc[1]) fail(page, 'twitter:description differs from meta description');
  const ogImage = html.match(/<meta property="og:image" content="([^"]+)"/);
  const twitterImage = html.match(/<meta name="twitter:image" content="([^"]+)"/);
  if (ogImage && twitterImage && ogImage[1] !== twitterImage[1]) fail(page, 'twitter:image differs from og:image');
  for (const imageMeta of [ogImage, twitterImage]) {
    if (!imageMeta) continue;
    try {
      const url = new URL(imageMeta[1]);
      if (url.hostname === 'vadimohka.com') {
        const local = url.pathname.replace(/^\//, '');
        if (!existsSync(resolve(ROOT, local))) fail(page, `social image missing: ${local}`);
        else if (JSON.stringify(imageDimensions(local)) !== JSON.stringify([1200, 630])) fail(page, `social image is not 1200x630: ${local}`);
      }
    } catch { fail(page, 'invalid social image URL'); }
  }

  if (!/<html[^>]*\blang="[^"]+"/.test(html)) fail(page, 'missing <html lang>');

  const h1s = matches(/<h1\b/g, html).length;
  if (h1s !== 1) fail(page, `expected exactly one <h1>, found ${h1s}`);

  if (!/property="og:title"/.test(html)) fail(page, 'missing og:title');
  if (!/property="og:image"/.test(html)) fail(page, 'missing og:image');
  if (!/name="twitter:card"/.test(html)) fail(page, 'missing twitter:card');
  if (page !== '404.html' && !/rel="canonical"/.test(html)) fail(page, 'missing canonical');
  if (/vadimohka\.github\.io/.test(html)) fail(page, 'stale github.io domain (use vadimohka.com)');
  if (page !== '404.html' && !/<meta name="yandex-verification" content="c3fd18a00a5bf714"\s*\/>/.test(html)) {
    fail(page, 'missing Yandex site-verification meta tag');
  }
  if (!/<script\s+src="assets\/site\.js\?v=[^"]+"\s+defer><\/script>/.test(html)) fail(page, 'site script must load with defer');

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

  // Static contact pages must not ship a dead or placeholder form.
  for (const form of matches(/<form\b[^>]*>/g, html)) {
    const action = (form[0].match(/\baction="([^"]*)"/) || [])[1] || '';
    if (!action || /example\.com|placeholder|TODO|owner_input/i.test(action)) fail(page, 'form has missing or placeholder action');
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

// Keep every indexable destination reachable from another published page.
const incoming = Object.fromEntries(PAGES.map(page => [page, new Set()]));
for (const from of PAGES) {
  const html = read(from);
  for (const match of matches(/href="([^"]+)"/g, html)) {
    const target = match[1].split(/[?#]/)[0];
    if (incoming[target]) incoming[target].add(from);
  }
}
for (const page of PAGES.filter(page => page !== 'index.html' && page !== '404.html')) {
  if (!incoming[page].size) fail(page, 'published page has no incoming internal link');
}

if (new Set(personCores).size > 1) fail('JSON-LD', 'Person properties differ across pages');
try {
  const graph = JSON.parse(read('data/entity-graph.json'));
  const person = graph['@graph']?.find(node => node['@type'] === 'Person');
  const stacklevel = graph['@graph']?.find(node => node['@id'] === 'https://vadimohka.com/#stacklevel');
  if (!person || person['@id'] !== 'https://vadimohka.com/#person') fail('data/entity-graph.json', 'missing stable Person @id');
  if (!stacklevel || stacklevel['@type'] !== 'Organization' || stacklevel.url !== 'https://stacklevel.group/en/company') fail('data/entity-graph.json', 'StackLevel organisation node is not authoritative');
} catch (error) {
  fail('data/entity-graph.json', `invalid entity graph JSON: ${error.message}`);
}

// Global navigation must expose the same staged information architecture on every page.
const NAV_EXPECTED = [
  ['index.html', 'Home'], ['work.html', 'Work'], ['century.html', 'Century'],
  ['enterprise.html', 'Enterprise AI'], ['investors.html', 'AI Diligence'],
  ['founders.html', 'Founder Advisory'], ['about.html', 'About']
];
const normaliseHeader = html => (html.match(/<header class="site-header">([\s\S]*?)<\/header>/)?.[0] || '')
  .replace(/\saria-current="page"/g, '');
const headerTemplate = normaliseHeader(read('index.html'));
for (const page of PAGES) {
  const html = read(page);
  if (normaliseHeader(html) !== headerTemplate) fail(page, 'header differs from the shared site header');
  const menuButton = html.match(/<button class="menu-toggle"[^>]*>/);
  if (!menuButton || !/aria-expanded="false"/.test(menuButton[0]) || !/aria-controls="primary-menu"/.test(menuButton[0])) {
    fail(page, 'menu button is missing accessible disclosure attributes');
  }
  if (!/<a class="skip-link" href="#main-content">Skip to main content<\/a>/.test(html)) fail(page, 'missing skip-to-main-content link');
  if (!/<main id="main-content" tabindex="-1">/.test(html)) fail(page, 'main content target is missing or not focusable');
  const nav = html.match(/<div class="nav-links"(?: id="primary-menu")?>([\s\S]*?)<\/div>/);
  if (!nav) { fail(page, 'missing primary navigation'); continue; }
  const actual = matches(/<a\b([^>]*)>([^<]*)<\/a>/g, nav[1]).map(m => [
    (m[1].match(/href="([^"]+)"/) || [])[1]?.split(/[?#]/)[0],
    m[2].trim()
  ]);
  if (JSON.stringify(actual) !== JSON.stringify(NAV_EXPECTED)) fail(page, 'primary navigation destinations/labels differ from staged IA');
  const current = matches(/aria-current="page"/g, nav[1]).length;
  if (current > 1) fail(page, 'multiple aria-current="page" items in primary navigation');
  if (page !== '404.html' && NAV_EXPECTED.some(([path]) => path === page)) {
    const expected = page === 'index.html' ? 'index.html' : page;
    const currentTag = (nav[1].match(/<a\b(?=[^>]*aria-current="page")[^>]*>/) || [])[0] || '';
    const currentHref = ((currentTag.match(/href="([^"]+)"/) || [])[1] || '').split(/[?#]/)[0];
    if (currentHref !== expected) fail(page, `aria-current does not identify ${expected}`);
  }
}

// sitemap + robots — public pages only (bare-domain home, no sources/404)
const sm = existsSync(resolve(ROOT, 'sitemap.xml')) ? read('sitemap.xml') : '';
const SITEMAP = ['work.html','about.html','century.html','expert.html','enterprise.html','investors.html','founders.html'];
const CURRENT_LASTMOD = '2026-08-31';
if (!sm) fail('sitemap.xml', 'missing');
else {
  if (!/<loc>https:\/\/vadimohka\.com\/?<\/loc>/.test(sm)) fail('sitemap.xml', 'missing home (bare-domain) loc');
  for (const p of SITEMAP) if (!sm.includes('/' + p)) fail('sitemap.xml', `does not list ${p}`);
  if (sm.includes('/404.html')) fail('sitemap.xml', 'should not list 404.html');
  if (/vadimohka\.github\.io/.test(sm)) fail('sitemap.xml', 'stale github.io domain');
  for (const entry of matches(/<url>([\s\S]*?)<\/url>/g, sm)) {
    if (!new RegExp(`<lastmod>${CURRENT_LASTMOD}<\\/lastmod>`).test(entry[1])) fail('sitemap.xml', 'lastmod must match the current publication date');
  }
}
const robots = existsSync(resolve(ROOT, 'robots.txt')) ? read('robots.txt') : '';
if (!robots) fail('robots.txt', 'missing');
else if (!/Sitemap:/i.test(robots)) fail('robots.txt', 'missing Sitemap: reference');

// Canonical and sitemap exact-match rules. The AI sitemap intentionally lists
// machine-readable resources; the main sitemap must contain only canonical,
// indexable HTML URLs.
if (sm) {
  const sitemapLocs = matches(/<loc>([^<]+)<\/loc>/g, sm).map(m => m[1]);
  const canonicalPages = PAGES.filter(page => page !== '404.html')
    .map(page => {
      const canonical = read(page).match(/<link rel="canonical" href="([^"]+)"/);
      return canonical ? canonical[1] : null;
    }).filter(Boolean).sort();
  if (JSON.stringify(sitemapLocs.slice().sort()) !== JSON.stringify(canonicalPages)) fail('sitemap.xml', 'URLs do not exactly match indexable page canonicals');
  if (sitemapLocs.some(url => /index\.html|[?#]/.test(url))) fail('sitemap.xml', 'contains duplicate or parameterized URL');
}
for (const sitemap of ['sitemap-images.xml','sitemap-ai.xml']) {
  const file = resolve(ROOT, sitemap);
  if (!existsSync(file)) fail(sitemap, 'robots-referenced sitemap missing');
  else {
    const body = read(sitemap);
    if (!/<urlset\b/.test(body)) fail(sitemap, 'invalid sitemap root');
    for (const entry of matches(/<url>([\s\S]*?)<\/url>/g, body)) {
      if (!new RegExp(`<lastmod>${CURRENT_LASTMOD}<\\/lastmod>`).test(entry[1])) fail(sitemap, 'lastmod must match the current publication date');
    }
    if (sitemap === 'sitemap-images.xml') {
      for (const match of matches(/<image:loc>([^<]+)<\/image:loc>/g, body)) {
        try {
          const url = new URL(match[1]);
          const local = url.hostname === 'vadimohka.com' ? url.pathname.replace(/^\//, '') : '';
          if (!local || !existsSync(resolve(ROOT, local))) fail(sitemap, `image URL missing locally: ${match[1]}`);
        } catch { fail(sitemap, `invalid image URL: ${match[1]}`); }
      }
    }
  }
}

for (const profile of ['llms.txt', 'llms-full.txt', 'ai-profile.md']) {
  const body = read(profile);
  if (!/United States/.test(body) || !/United Arab Emirates/.test(body)) {
    fail(profile, 'must identify United States and United Arab Emirates as geographic focus');
  }
}

const home = read('index.html');
if (!/<link rel="preload"[^>]+fetchpriority="high"[^>]*>/.test(home)) fail('index.html', 'hero image preload must have fetchpriority=high');
for (const portrait of ['assets/portraits/vadim-boardroom-640.webp', 'assets/portraits/vadim-warm-640.webp']) {
  if (!existsSync(resolve(ROOT, portrait))) fail(portrait, 'missing 640px responsive portrait');
}
for (const page of PAGES) {
  const html = read(page);
  if (/portraits\/vadim-(?:boardroom|warm)-1536\.webp/.test(html) && !/portraits\/vadim-(?:boardroom|warm)-640\.webp 640w/.test(html)) {
    fail(page, 'portrait srcset is missing a 640w responsive candidate');
  }
}
if (robots) {
  for (const m of matches(/^Sitemap:\s*(\S+)/gmi, robots)) {
    const name = m[1].split('/').pop();
    if (!existsSync(resolve(ROOT, name))) fail('robots.txt', `referenced sitemap missing: ${name}`);
  }
}

// Production-safety and claim/source ledger invariants.
for (const file of PRODUCTION_FILES) {
  if (!existsSync(resolve(ROOT, file))) continue;
  const body = read(file);
  if (/\bTODO\b|\[OWNER_INPUT_REQUIRED\]|https?:\/\/example\.(?:com|org)|placeholder(?:\.com| endpoint)/i.test(body)) {
    fail(file, 'production TODO, owner placeholder or example endpoint found');
  }
}

// Public copy stays conversational; audit labels belong in the private ledger only.
for (const file of PRODUCTION_FILES) {
  if (!existsSync(resolve(ROOT, file))) continue;
  if (!file.endsWith('.html')) continue;
  const body = read(file);
  const visibleText = body.replace(/<script\b[\s\S]*?<\/script>/gi, ' ').replace(/<style\b[\s\S]*?<\/style>/gi, ' ').replace(/<[^>]+>/g, ' ');
  if (/\bChecked\b|\bScope:\s|\bStatus:\s|\bProof\b|\bEvidence map\b|\bVerified\b|\bVerify\b/i.test(visibleText)) {
    fail(file, 'visible audit/implementation label remains in production content');
  }
}

try {
  const claims = JSON.parse(read('qa/brand/claims.json'));
  const sources = JSON.parse(read('qa/brand/sources.json'));
  const sourceIds = new Set(sources.sources.map(source => source.source_id));
  const statuses = new Set(['verified','partially_verified','owner_confirmed','company_level_only','unverified','remove_or_clarify','low_authority']);
  const productionSet = new Set(PRODUCTION_FILES);
  for (const claim of claims.claims) {
    if (!/^C\d{3}$/.test(claim.id)) fail('qa/brand/claims.json', `invalid claim id: ${claim.id}`);
    if (!statuses.has(claim.status)) fail('qa/brand/claims.json', `${claim.id} has unknown status`);
    for (const sourceId of claim.sources || []) if (!sourceIds.has(sourceId)) fail('qa/brand/claims.json', `${claim.id} references missing ${sourceId}`);
    for (const surface of [...(claim.allowed_surfaces || []), ...(claim.surfaces || [])]) if (!productionSet.has(surface) && !surface.endsWith('.html')) fail('qa/brand/claims.json', `${claim.id} references unknown surface ${surface}`);
  }
  for (const source of sources.sources) {
    if (!/^S\d{3}$/.test(source.source_id)) fail('qa/brand/sources.json', `invalid source id: ${source.source_id}`);
    if (!/^https?:\/\/[^\s]+$/.test(source.url) || /example\.(?:com|org)|placeholder/i.test(source.url)) fail('qa/brand/sources.json', `${source.source_id} has invalid/placeholder URL`);
  }
} catch (error) {
  fail('qa/brand', `claim/source ledger JSON invalid: ${error.message}`);
}

// Public-signal cards must carry a date, role/format and direct external source.
const expert = read('expert.html');
for (const record of matches(/<article class="article">([\s\S]*?)<\/article>/g, expert)) {
  const body = record[1];
  if (!/\b20\d{2}\b/.test(body)) fail('expert.html', 'public-signal record missing date');
  if (!/class="proof-role"|class="card-label"/.test(body)) fail('expert.html', 'public-signal record missing descriptive record label');
  if (!/href="https?:\/\//.test(body)) fail('expert.html', 'public-signal record missing external source URL');
}

console.log(fails ? `\nFAIL — ${fails} issue(s)` : `\nPASS — ${PAGES.length} pages, all static checks green`);
process.exit(fails ? 1 : 0);
