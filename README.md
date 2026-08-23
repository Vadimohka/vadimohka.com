# Vadim Vladymtsev — Ultra Personal Site

Static GitHub Pages site. No build step, no dependencies.

## Deploy

1. Create a GitHub repository.
2. Upload all files from this folder to the repository root.
3. Go to Settings → Pages.
4. Select Deploy from branch → main → root.
5. Open the published GitHub Pages URL.

## Preview locally

    python3 -m http.server 4173

Then open http://localhost:4173/

## Pages

- `index.html` — main positioning.
- `enterprise.html` — governed private AI for regulated organisations.
- `founders.html` — founders / chaos to product.
- `investors.html` — AI technical diligence / technical judgment.
- `about.html` — current role, working approach, background and contact routes.
- `century.html` — product proof.
- `work.html` — selected work, product context and engineering background.
- `sources.html` — public source map.
- `404.html` — styled not-found page.

## QA

Dependency-free static checks (pure Node, no browser, no install). Verifies every
page has a title, meta description, canonical/OG/Twitter tags, a `lang` attribute and
exactly one `<h1>`; every image has `alt` + `width`/`height`; internal links and assets
resolve; and there are no empty hrefs, absolute local paths, duplicate ids,
production TODOs or placeholder form actions. It also checks claim/source ledger
references, stable Person JSON-LD, navigation parity, public-signal source records,
canonical/sitemap equality, and robots sitemap references.

    node qa/check.mjs        # from the repo root
    node qa/test-regressions.mjs

Optional browser QA uses development-only Playwright and axe-core tooling:

    cd qa/browser && npm ci && npx playwright install chromium && npm test

It covers 1440, 1024, 768, 390 and 320px viewports, mobile menu/skip-link
behavior, contact intents, no-JavaScript navigation, reduced motion, overflow,
screenshots and serious/critical axe findings. A manual GitHub Actions workflow
(`Browser QA (manual)`) runs the same suite and uploads screenshots.

When network access is available, re-check the key public proof links with:

    node qa/external-link-check.mjs

This reports inaccessible sources for review without silently removing evidence.

`qa/` is dev-only and is not needed by the published site.

The Pages workflow assembles a clean `_site/` artifact and excludes `qa/`,
`site-improvement-pack/`, `reports/`, `.agents/`, `AGENTS.md`, and other local/development
paths. GitHub Pages does not provide an arbitrary `/index.html` HTTP 301 in this
repository; the canonical tag and root sitemap URL use `https://vadimohka.com/`.
A true redirect requires a hosting or edge rule and must be verified separately.

The contact section is intentionally form-free until an approved endpoint and
privacy owner exist. Its functional routes are direct LinkedIn/company links;
the six intent query parameters (`enterprise`, `diligence`, `founder`,
`executive`, `media`, `speaking`) preselect the route when JavaScript is
available and remain ordinary links when it is not.

## Notes

No build step. No dependencies. Works on GitHub Pages. Canonical / Open Graph /
sitemap URLs use the `vadimohka.com` domain — update them if you deploy to a
custom domain.
