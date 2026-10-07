# Vadim Vladymtsev — personal site

Static English-language Executive 03 website for enterprise AI, technical due diligence and CTO advisory. USA and UAE are intended audiences, not implied office locations. No production runtime dependencies or third-party font requests.

## Preview, check and publish

```sh
python3 -m http.server 4173
node qa/check.mjs
node qa/test-regressions.mjs
node qa/executive-content.mjs
python3 qa/health/check.py
node qa/health/build.mjs
```

GitHub Actions publishes `main` using the public allowlist in `qa/health/build.mjs`. Documentation, source notes, QA, old installation packs and reports are not published. A failed gate prevents deployment. The ten public routes and all six contact intents are retained.

## Search and AI discovery

`qa/health/search-config.json` is the editorial source for titles, descriptions, consistent identity/service metadata and actual modification dates. Run:

```sh
python3 qa/health/generate-discovery.py --write
python3 qa/health/generate-discovery.py --check
```

The generator synchronizes page heads, the entity graph, XML sitemaps and AI-readable documents with visible content. It does not invent clients, offices, residence, reviews or regional clones. Service nodes, not Person, specify `areaServed`. There is one English version; the Russian profile is related but not a page-for-page translation.

`llms.txt` supplements crawlable HTML; it is not a ranking guarantee. Sitemap dates are explicit editorial dates, never refreshed merely by deployment. Original source and claim registers remain in `docs/archive/`, with current ledgers in `qa/brand/`.

Historical content baselines stay intact. `qa/health/approved-changes.json` records specific old/new hashes for authorized maintenance changes; semantic content checks remain active. Future changes must update those explicit exceptions deliberately, not replace historical baselines.

## Browser and performance checks

```sh
cd qa/browser
npm ci
npx playwright install chromium
npm test
# BROWSER=firefox or BROWSER=webkit after installing that engine
```

The browser suite checks 28 viewports, all ten routes, fonts/images, keyboard/menu/resize behavior, no-JavaScript content, reduced motion, source anchors, English US/UAE locale contexts, nested 404 assets and axe findings.

The Site health workflow compares the pre-maintenance `a5fd47a` snapshot and candidate using pinned Lighthouse 13.4.1, with three home-mobile runs and spot checks on other pages. Raw reports distinguish lab measurements from real-user Core Web Vitals and from real HTTPS availability checks. A single runner does not measure geographic USA/UAE latency. Missing field data is reported as unavailable.

## Assets

The supplied portrait, approved font files and their licenses remain unchanged. Responsive WebP versions are derivatives of the credited original photographs. Closing photographs are native lazy-loaded images; decorative imagery does not imply offices or customer relationships. Provenance is recorded in `assets/executive/credits.json`.

Unused historical exports and obsolete installation/prompt packs are removed; Git history retains recovery copies. GH Pages controls cache and compression headers; changing CDN policy or adding Search Console/Bing verification requires the relevant service access.
