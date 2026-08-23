# Final Release Gate — 2026-08-22

## Status

`pass with documented limitations`

## Static quality

- `node qa/check.mjs` passes: 12 pages, all static checks green.
- No broken internal links/assets, empty hrefs, placeholder form actions, duplicate IDs, production TODOs or owner placeholders.
- All HTML JSON-LD blocks and `data/entity-graph.json` parse.

## Responsive and accessibility

- Playwright Chromium suite passes at 1440×1000, 1024×768, 768×1024, 390×844 and 320×568.
- Mobile menu is discoverable, keyboard-operable, Escape-closing and focus-restoring; hidden links are not tabbable.
- Skip link focuses `#main-content`; no-JavaScript navigation remains visible and usable.
- Contrast/token and 12px label audit passes; reduced motion disables nonessential transitions.
- axe-core reports no serious/critical findings on index, contact or Track Record.

## SEO and entity

- Titles/descriptions/OG/X metadata are synchronized with visible page purpose.
- Main sitemap URLs exactly match indexable canonical URLs; root slash is consistent.
- Stable Person `https://vadimohka.com/#person` and connected WebPage/Organisation/Product nodes are present.
- Sources/404 are not in the main sitemap; 404 is noindex.
- `/index.html` behavior is documented as HTTP 200; no false 301 claim is made.

## Performance and sharing

- Lighthouse baseline is dated and reproducible in `qa/performance/baseline.md`.
- Hero LCP preload/srcset and explicit image dimensions are intentional.
- All referenced social cards are 1200×630; page-specific cards are in `assets/social/`.

## Deployment

- Rsync artifact review confirms `qa/`, `site-improvement-pack/`, `reports/`, `.agents/`, `AGENTS.md` and local/private paths are excluded.
- No secrets or confidential owner-input files are included.

## Remaining limitations

- Owner input is still required for exact Century role/relationship, MIPT details, direct contact endpoint/email/privacy owner/calendar, private metrics/cases and external-profile cleanup.
- Firefox/WebKit and physical-device checks are not available in this environment.
- Post-deploy live smoke/share-preview verification must be repeated after the working tree is deployed.

## Decision

The release candidate passes the technical and evidence gates with the limitations above explicitly recorded. Release report: [`reports/release-report.md`](../../reports/release-report.md).
