# Vadim Vladymtsev — personal site

Static English-language Executive 03 website for enterprise AI, technical due diligence and CTO advisory. USA and UAE are intended audiences, not implied office locations. No production runtime dependencies or third-party font requests.

## Preview and checks

```sh
python3 -m http.server 4173
node qa/check.mjs
node qa/test-regressions.mjs
node qa/executive-content.mjs
python3 qa/health/check.py
```

## Publish

The GitHub Pages workflow publishes `main` in one job: checkout, package static files, configure Pages, upload the public artifact and deploy. It runs no QA gates, tests, generators, browser checks or post-deployment checks. Browser QA and Site health are separate workflows for pull requests or manual use.

`scripts/package-site.mjs` copies the ready-to-publish files into `_site` using the public allowlist. It uses only Node.js built-ins and does not install dependencies or invoke validation. Documentation, source notes, QA, old installation packs and reports are excluded from publication. Sixteen HTML routes are published, including the essay collection and five essays. All six contact intents are retained.

To prepare the same artifact locally:

```sh
node scripts/package-site.mjs
```

## Search and AI discovery

`qa/health/search-config.json` is the editorial source for titles, descriptions, consistent identity/service metadata and actual modification dates. Run:

```sh
python3 qa/health/generate-discovery.py --write
python3 qa/health/generate-discovery.py --check
```

The generator synchronizes page heads, the entity graph, XML sitemaps and AI-readable documents with visible content. It does not invent clients, offices, residence, reviews or regional clones. Service nodes, not Person, specify `areaServed`. All published pages are in English and use their own canonical URLs.

`/essays/` is a `CollectionPage` with a dated `ItemList`. Each article has an `Article` node, author identity, breadcrumbs and full `articleBody` extracted from its visible `#essay-body`. To edit an essay, change that HTML and its editorial metadata in `search-config.json`, then regenerate discovery. Keep the thesis first and explain the full context in the article. Publication dates follow the owner-selected October–November 2026 schedule; modification dates record editorial changes.

Generated essay resources include per-essay `index.md`, the collection Markdown, `/essays/llms.txt`, and `/essays/feed.xml`. The feed uses date-only `dc:date` because the editorial source does not claim a publication time. `/ai.json` is this site's discovery catalog, linking the canonical pages, article dates, Markdown and the existing entity graph; it is not presented as an external standard. `llms-full.txt` includes every essay in full.

`llms.txt` supplements crawlable HTML; it is not a ranking guarantee. Sitemap dates are explicit editorial dates, never refreshed merely by deployment. Original source and claim registers remain in `docs/archive/`, with current ledgers in `qa/brand/`.

Public links exclude CIS source destinations at the owner's request. Century links use `https://century-ai.eu/`. The current editorial configuration is the source for identity and product links; historical evidence ledgers are excluded from the Pages artifact. Codeforces remains an international profile: its current terms identify its operator as a UAE company. A verification meta tag is an ownership marker, not an external source link.

Historical content baselines stay intact. `qa/health/approved-changes.json` records specific old/new hashes and the exact text, destinations and source anchors changed by authorized releases; semantic content checks remain active. Future changes must update those explicit exceptions deliberately, not replace historical baselines.

## Browser and performance checks

```sh
cd qa/browser
npm ci
npx playwright install chromium
npm test
# BROWSER=firefox or BROWSER=webkit after installing that engine
```

The browser suite uses the same route registry as discovery and checks responsive layouts, fonts/images, keyboard/menu/resize behavior, no-JavaScript content, reduced motion, current source anchors, English US/UAE locale contexts, nested 404 assets and axe findings.

The Site health workflow compares the pre-maintenance `a5fd47a` snapshot and candidate using pinned Lighthouse 13.4.1, with three home-mobile runs and spot checks on other pages. Raw reports distinguish lab measurements from real-user Core Web Vitals and from real HTTPS availability checks. A single runner does not measure geographic USA/UAE latency. Missing field data is reported as unavailable.

## Assets

The supplied portrait, approved font files and their licenses remain unchanged. Responsive WebP versions are derivatives of the credited original photographs. Closing photographs are native lazy-loaded images; decorative imagery does not imply offices or customer relationships. Provenance is recorded in `assets/executive/credits.json`.

Unused historical exports and obsolete installation/prompt packs are removed; Git history retains recovery copies. GH Pages controls cache and compression headers; changing CDN policy or adding Search Console/Bing verification requires the relevant service access.
