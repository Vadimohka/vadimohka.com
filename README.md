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
- `enterprise.html` — big business / boardroom.
- `founders.html` — founders / chaos to product.
- `investors.html` — investor vision / technical judgment.
- `origin.html` — teacher, ICPC, BSUIR, work ethic.
- `century.html` — product proof.
- `proof.html` — evidence ledger.
- `writing.html` — VK articles and essays.
- `contact.html` — conversion.
- `sources.html` — public source map.
- `404.html` — styled not-found page.

## QA

Dependency-free static checks (pure Node, no browser, no install). Verifies every
page has a title, meta description, canonical/OG/Twitter tags, a `lang` attribute and
exactly one `<h1>`; every image has `alt` + `width`/`height`; internal links and assets
resolve; and there are no empty hrefs, absolute local paths, or duplicate ids. Also
checks sitemap + robots consistency.

    node qa/check.mjs        # from the repo root

`qa/` is dev-only and is not needed by the published site.

## Notes

No build step. No dependencies. Works on GitHub Pages. Canonical / Open Graph /
sitemap URLs use the `vadimohka.com` domain — update them if you deploy to a
custom domain.
