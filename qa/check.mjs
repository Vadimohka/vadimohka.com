// Static QA for the site — pure Node, no browser, no dependencies.
// Run from repo root:  node qa/check.mjs
// Checks: pages exist, internal links + assets resolve, one <h1>, title +
// meta description, canonical/OG/Twitter, lang, alt + width/height on images,
// duplicate ids, empty href, nested and root-relative links, stylesheet present,
// rough <div> nesting balance, sitemap + robots.
import { readFileSync, existsSync, statSync } from 'node:fs';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const ROOT = resolve(dirname(fileURLToPath(import.meta.url)), '..');
const read = f => readFileSync(resolve(ROOT, f), 'utf8');
const CONFIG = JSON.parse(read('qa/health/search-config.json'));
const PAGES = Object.keys(CONFIG.pages);
const SITE = new URL(CONFIG.baseURL);
const canonicalURL = page => new URL(page.replace(/(^|\/)index\.html$/, '$1'), SITE).href;
const localTarget = (href, page = 'index.html') => {
  const url = new URL(href.replace(/&amp;/g, '&'), canonicalURL(page));
  if (url.origin !== SITE.origin) return null;
  const path = decodeURIComponent(url.pathname).replace(/^\//, '');
  return {url, file: path.endsWith('/') || !path ? path + 'index.html' : path};
};
const fileExists = file => existsSync(resolve(ROOT, file)) && statSync(resolve(ROOT, file)).isFile();
const modified = page => CONFIG.pages[page]?.modified || CONFIG.pages[page]?.article?.modified || CONFIG.modified;

let fails = 0;
const fail = (p, msg) => { console.error(`  ✗ ${p}: ${msg}`); fails++; };
const matches = (re, s) => [...s.matchAll(re)];
const personCores = [];
const PRODUCTION_FILES = [...PAGES, 'assets/site.css', 'assets/internal.css', 'assets/essays.css', 'assets/site.js', 'ai-profile.md', 'llms.txt', 'llms-full.txt', 'data/entity-graph.json', 'sitemap.xml', 'sitemap-images.xml', 'sitemap-ai.xml', 'robots.txt',
  ...['ai.json', 'ai-catalog.json', '.well-known/ai.json', '.well-known/ai-catalog.json'].filter(fileExists)];
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
      const parsed = JSON.parse(block[1]);
      for (const node of parsed["@graph"] || [parsed]) {
      if (node['@type'] === 'Person') {
        if (node['@id'] !== 'https://vadimohka.com/#person') fail(page, 'Person JSON-LD has unstable @id');
        if ('areaServed' in node) fail(page, 'areaServed belongs on Service, not Person');
        personCores.push(JSON.stringify({name:node.name,jobTitle:node.jobTitle,sameAs:node.sameAs,worksFor:node.worksFor,image:node.image}));
      }
      if (['WebPage','ProfilePage','CollectionPage'].includes(node['@type']) && node.inLanguage !== 'en') fail(page, 'WebPage JSON-LD missing inLanguage=en');
      if (page === 'century.html' && node['@type'] === 'SoftwareApplication' && node['@id'] !== 'https://vadimohka.com/#century') fail(page, 'Century schema has unstable @id');
      }
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
  if (page !== '404.html' && html.match(/<link rel="canonical" href="([^"]+)"/)?.[1] !== canonicalURL(page)) fail(page, 'canonical does not match the public route');
  if (/vadimohka\.github\.io/.test(html)) fail(page, 'stale github.io domain (use vadimohka.com)');
  if (page !== '404.html' && !/<meta name="yandex-verification" content="c3fd18a00a5bf714"\s*\/>/.test(html)) {
    fail(page, 'missing Yandex site-verification meta tag');
  }
  if (!/<script\s+src="\/?assets\/site\.js\?v=[^"]+"\s+defer><\/script>/.test(html)) fail(page, 'site script must load with defer');

  // images: alt + intrinsic dimensions + resolvable src
  for (const m of matches(/<img\b[^>]*>/g, html)) {
    const tag = m[0];
    const src = (tag.match(/\bsrc="([^"]*)"/) || [])[1] || '(no src)';
    if (!/\balt=/.test(tag)) fail(page, `img missing alt: ${src}`);
    if (!/\bwidth=/.test(tag) || !/\bheight=/.test(tag)) fail(page, `img missing width/height: ${src}`);
    try {
      const target = localTarget(src, page);
      if (target && !fileExists(target.file)) fail(page, `img src not found: ${src}`);
    } catch { fail(page, `invalid img src: ${src}`); }
  }

  // Resolve local URLs from each public route, including directory indexes.
  for (const m of matches(/\bhref="([^"]*)"/g, html)) {
    const href = m[1];
    if (href.trim() === '') { fail(page, 'empty href'); continue; }
    if (/^(mailto:|tel:|data:)/.test(href)) continue;
    try {
      const target = localTarget(href, page);
      if (target && !fileExists(target.file)) fail(page, `internal link not found: ${href}`);
    } catch { fail(page, `invalid link URL: ${href}`); }
  }

  // Static contact pages must not ship a dead or placeholder form.
  for (const form of matches(/<form\b[^>]*>/g, html)) {
    const action = (form[0].match(/\baction="([^"]*)"/) || [])[1] || '';
    if (!action || /example\.com|placeholder|TODO|owner_input/i.test(action)) fail(page, 'form has missing or placeholder action');
  }

  // stylesheet target exists
  for (const m of matches(/<link[^>]+rel="stylesheet"[^>]+href="([^"]+)"/g, html)) {
    try {
      const target = localTarget(m[1], page);
      if (target && !fileExists(target.file)) fail(page, `stylesheet not found: ${m[1]}`);
    } catch { fail(page, `invalid stylesheet URL: ${m[1]}`); }
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
  for (const match of matches(/<a\b[^>]*href="([^"]+)"/g, html)) {
    try {
      const target = localTarget(match[1], from)?.file;
      if (target !== from && incoming[target]) incoming[target].add(from);
    } catch { /* Invalid URLs are reported by the page checks above. */ }
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
  if (!stacklevel || stacklevel['@type'] !== 'Organization' || stacklevel.name !== 'StackLevel Group' || stacklevel.employee?.['@id'] !== 'https://vadimohka.com/#person' || 'url' in stacklevel) fail('data/entity-graph.json', 'StackLevel organisation identity must remain without an outbound URL');
} catch (error) {
  fail('data/entity-graph.json', `invalid entity graph JSON: ${error.message}`);
}

// Global navigation must expose the same staged information architecture on every page.
const NAV_EXPECTED = [
  ['/', 'Home'], ['/work.html', 'Work'], ['/essays/', 'Essays'], ['/century.html', 'Century'],
  ['/enterprise.html', 'Enterprise AI'], ['/investors.html', 'AI Diligence'],
  ['/founders.html', 'Founder Advisory'], ['/about.html', 'About']
];
const normaliseHeader = html => (html.match(/<header class="site-header">([\s\S]*?)<\/header>/)?.[0] || '')
  .replace(/\saria-current="(?:page|location)"/g, '');
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
  const currentTags = matches(/<a\b(?=[^>]*aria-current="(?:page|location)")[^>]*>/g, nav[1]);
  if (currentTags.length > 1) fail(page, 'multiple current items in primary navigation');
  const route = new URL(canonicalURL(page)).pathname;
  const essayArticle = Boolean(CONFIG.pages[page].article);
  const expected = essayArticle ? '/essays/' : route;
  if (page !== '404.html' && NAV_EXPECTED.some(([path]) => path === expected)) {
    const currentTag = currentTags[0]?.[0] || '';
    const currentHref = currentTag.match(/href="([^"]+)"/)?.[1];
    const currentValue = currentTag.match(/aria-current="([^"]+)"/)?.[1];
    if (currentHref !== expected || currentValue !== (essayArticle ? 'location' : 'page')) fail(page, `aria-current does not identify ${expected}`);
  }
}

// sitemap + robots — canonical public pages, excluding the 404 document.
const sm = existsSync(resolve(ROOT, 'sitemap.xml')) ? read('sitemap.xml') : '';
const SITEMAP = PAGES.filter(page => page !== '404.html');
const LASTMOD_BY_URL = new Map(SITEMAP.map(page => [canonicalURL(page), modified(page)]));
for (const page of PAGES.filter(page => page.startsWith('essays/'))) {
  LASTMOD_BY_URL.set(new URL(page.replace(/\.html$/, '.md'), SITE).href, modified(page));
}
for (const file of ['essays/llms.txt', 'essays/feed.xml']) {
  LASTMOD_BY_URL.set(new URL(file, SITE).href, modified('essays/index.html'));
}
const checkLastmod = (entry, sitemap) => {
  const url = entry.match(/<loc>([^<]+)<\/loc>/)?.[1];
  const expected = LASTMOD_BY_URL.get(url) || CONFIG.modified;
  if (entry.match(/<lastmod>([^<]+)<\/lastmod>/)?.[1] !== expected) fail(sitemap, 'lastmod must match the configured content modification date');
};
if (!sm) fail('sitemap.xml', 'missing');
else {
  if (!/<loc>https:\/\/vadimohka\.com\/?<\/loc>/.test(sm)) fail('sitemap.xml', 'missing home (bare-domain) loc');
  for (const p of SITEMAP) if (!sm.includes(`<loc>${canonicalURL(p)}</loc>`)) fail('sitemap.xml', `does not list ${p}`);
  if (sm.includes('/404.html')) fail('sitemap.xml', 'should not list 404.html');
  if (/vadimohka\.github\.io/.test(sm)) fail('sitemap.xml', 'stale github.io domain');
  for (const entry of matches(/<url>([\s\S]*?)<\/url>/g, sm)) {
    checkLastmod(entry[1], 'sitemap.xml');
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
      checkLastmod(entry[1], sitemap);
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
  const visible = body.replace(/<script\b[\s\S]*?<\/script>/gi, ' ').replace(/<style\b[\s\S]*?<\/style>/gi, ' ');
  const labels = matches(/<(h[1-6]|summary|dt|button|span|a|p)\b[^>]*>([\s\S]*?)<\/\1>/gi, visible)
    .map(match => match[2].replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim());
  if (labels.some(label => /^(?:(?:Checked|Scope|Status|Proof|Verified)\s*:|Evidence map(?:\s*:|$)|(?:Checked|Proof|Verified|Verify)$)/i.test(label))) {
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

// Publication cards carry a date, format and a direct source or authored essay.
const expert = read('expert.html');
for (const record of matches(/<article class="(?:article|editorial-item)">([\s\S]*?)<\/article>/g, expert)) {
  const body = record[1];
  if (!/\b20\d{2}\b/.test(body)) fail('expert.html', 'public-signal record missing date');
  if (!/class="proof-role"|class="card-label"/.test(body)) fail('expert.html', 'public-signal record missing descriptive record label');
  const href = body.match(/<a\b[^>]*href="([^"]+)"/)?.[1];
  try {
    const target = href && localTarget(href, 'expert.html');
    if (!href || (target ? !CONFIG.pages[target.file]?.article : !/^https:\/\//.test(href))) fail('expert.html', 'publication record missing a direct source or authored essay');
  } catch { fail('expert.html', 'publication record has an invalid source URL'); }
}

console.log(fails ? `\nFAIL — ${fails} issue(s)` : `\nPASS — ${PAGES.length} pages, all static checks green`);
process.exit(fails ? 1 : 0);
