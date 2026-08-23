# Release report — vadimohka.com

## Release identity

- Date: 2026-08-22
- Branch: `main`
- Commit: `7795240` (working tree intentionally contains the staged programme changes)
- Environment: static GitHub Pages repository; local Chromium/Lighthouse verification
- Reviewer: Codex implementation owner; owner-gated inputs remain explicitly listed

## Programme summary

- Brand tasks: B00–B11 complete.
- Technical tasks: T01–T10 complete.
- Deliberately deferred tasks: exact Century personal title/relationship; exact MIPT credential; private metrics/cases; direct email/form/privacy endpoint/calendar; external-profile owner actions; true `/index.html` 301 hosting rule.

## Brand Release Gate

| Condition group | Result | Evidence |
|---|---|---|
| Identity | pass | Current CTO role sourced; Century personal role omitted; unsupported investor/board/global/thought-leader identity and MIPT removed. |
| Evidence | pass | Work separates personal role/public work from Century product recognition; no aggregate metrics or production TODOs remain. |
| Homepage and audience pages | pass | Homepage follows Identity → Authority → Proof → Relevance → Depth → Trust → Action; enterprise, diligence, founder, Century and contact routes use bounded copy. |
| Machine parity | pass | HTML metadata, JSON-LD, AI profiles, entity graph, sitemap and sources page share the same conservative identity. |

## Final Release Gate

| Condition group | Result | Evidence |
|---|---|---|
| Static quality | pass | `node qa/check.mjs`; 10 pages, links/assets, metadata, JSON-LD, claims/sources, sitemap and deploy-safe checks green. |
| Responsive and accessibility | pass | Playwright/axe suite: five viewports, menu/skip/no-JS/reduced motion; no serious/critical findings. |
| SEO and entity | pass | Canonical set equals main sitemap; root slash consistent; stable `#person`; page WebPage nodes; noindex 404/sources handling documented. |
| Performance | pass | Lighthouse lab baseline recorded; LCP/preload intentional; 1200×630 OG cards validated. |
| Deployment evidence | pass with limitation | Rsync artifact excludes QA, pack, reports, instructions and local paths; post-change production deploy remains pending. |

## Claims added, changed or removed

| Claim ID | Action | Final wording | Source IDs |
|---|---|---|---|
| C001 | retained/synchronised | Enterprise AI CTO and product operator; CTO at StackLevel Group | S001 |
| C002 | retained/narrowed | Century received third place in the AI Product Leader category at IT-Akademgrad 2025; product recognition, not a personal award | S002 |
| C003 | omitted | Exact Century personal title/relationship remains unpublished | S021, S027 |
| C004–C007 | omitted/narrowed | Regulated-private-AI focus and specific BSUIR records only; no sector or aggregate metrics | S015–S021 |
| C008 | retained/narrowed | University teaching and competitive-programming coaching at BSUIR, with event-specific records | S015–S020 |
| C011–C014 | retained | Dated public-work records with exact source role/date | S003–S011 |
| C015–C017 | omitted | No completed diligence mandate, MIPT credential or unsupported education authority | — |
| C018 | secondary only | Claude Foundations certificate appears only as low-authority supporting proof | S025 |
| C020 | product-only | Century capability descriptions remain company/product-level | S021 |

## Commands run

```text
node qa/check.mjs
node qa/test-regressions.mjs
cd qa/browser && npm ci && npx playwright install chromium && npm test
npx --yes lighthouse ... (mobile and desktop; raw JSON ignored, summary in qa/performance/baseline.md)
git diff --check
```

All commands passed. The browser regression was intentionally broken once (focus return) and failed as expected before restoration.

## Browser matrix

| Browser | Viewport | Result | Screenshot |
|---|---:|---|---|
| Chromium | 1440×1000 | pass | `qa/screenshots/T08-home-1440.png` |
| Chromium | 1024×768 | pass | `qa/screenshots/T08-home-1024.png` |
| Chromium | 768×1024 | pass | `qa/screenshots/T08-home-768.png` |
| Chromium | 390×844 | pass | `qa/screenshots/T08-home-390.png` |
| Chromium | 320×568 | pass | `qa/screenshots/T08-home-320.png` |

## Accessibility

- Automated scanner/version: axe-core via `@axe-core/playwright` 4.11.0; Playwright Chromium.
- Serious/critical findings: none on index, about/contact routes or Work.
- Manual keyboard result: skip link first, menu click/Enter/Space/Escape, focus return, no focus trap; links remain available with JavaScript disabled.
- Contrast review: muted token 7.26:1, paper 17.55:1, gold 8.52:1 against the dark background; meaningful labels target 12px.
- Known limitations: Firefox/WebKit and physical-device checks remain optional follow-up coverage.

## SEO and structured data

- Canonical/sitemap: exact match; root uses `https://vadimohka.com/`.
- JSON-LD validation: all 10 published pages and entity graph parse; stable `https://vadimohka.com/#person`.
- sameAs: LinkedIn, Codeforces and Google Scholar only; Stepik/Claude remain supporting references.
- index/noindex: sources remains an evidence utility; 404 is noindex; neither is in the main sitemap.
- redirect limitations: live `/index.html` is HTTP 200; HTTP/HTTPS and www canonicalize to HTTPS root, but no arbitrary GitHub Pages 301 is claimed.

## Performance

- Tool/version: Lighthouse 13.4.1, Chromium headless.
- Date/environment: 2026-08-22, local Python static server.
- LCP element: preloaded boardroom portrait; mobile request selects the 960px WebP.
- Findings: mobile 100 / desktop 96 lab performance, 1.1–1.2s LCP, ~90KiB transfer; shared CSS is the only notable render-blocking request.
- Changes: corrected legacy OG claims; added six 1200×630 page-intent cards; retained explicit image dimensions/srcsets.
- No field-data claim was made.

## Deployment-output review

- Pack excluded: yes (`site-improvement-pack/`).
- Owner-input excluded: yes (`owner-input.local.*`, private evidence paths).
- QA excluded: yes (`qa/`).
- Secrets scan: no tokens, passwords, endpoints or owner placeholders found in production surfaces.
- Published file list: static HTML, assets, public machine-readable profiles, sitemaps, robots, CNAME and license; internal reports are excluded.

## External source check

| Source ID | Result | Checked date |
|---|---|---|
| S001 | 200 — StackLevel company page | 2026-08-22 |
| S002 | 200 — HTP/IT-Akademgrad recognition | 2026-08-22 |
| S003 | 200 — Finance Mail.ru quotation | 2026-08-22 |
| S005 | retained; curl timed out in this run, prior page re-check supports the article record | 2026-08-22 |
| S007 | 200 — M.AI.N organiser record | 2026-08-22 |
| S010 | 200 — IT-Security official programme | 2026-08-22 |
| S013 | 403 to automated fetch; public profile was accessible in browser audit | 2026-08-22 |
| S021 | 200 — Century product site | 2026-08-22 |

The full source ledger remains linked from `sources.html`; inaccessible secondary links were not silently deleted.

## Unresolved owner inputs

- Exact Century personal title, legal/product relationship and start date.
- Exact MIPT programme/credential, dates and permission.
- Approved professional email, form endpoint, privacy contact entity, calendar URL and response-time text.
- Permitted private case studies, diligence mandate count, team/user/education metrics and sector-specific personal evidence.
- External profile actions for LinkedIn, legacy `.ru`, Setka and related mirrors.
- Hosting/edge decision for a true `/index.html` 301.

## Post-deploy smoke test

- URL: `https://vadimohka.com/` and host variants
- Date: 2026-08-22
- Key pages: root, `/about.html#contact`, `/century.html`
- Status codes: root 200; `/index.html` 200; HTTP root 301 → HTTPS; www 301 → non-www HTTPS.
- Share previews: local 1200×630 assets validated; post-deploy preview refresh remains pending until this working tree is deployed.
- Contact actions: local six-intent browser matrix passes; post-deploy route smoke remains pending deployment.

## Release decision

`APPROVE WITH DOCUMENTED LIMITATIONS`

Reason: the release candidate passes all offline/static/browser/performance gates and excludes private development material. Deployment and owner-gated profile/contact decisions remain external follow-up actions; no unsupported claim is published while those inputs are absent.

## Follow-up architecture and interaction cleanup — 2026-08-23

- Working branch: `codex/site-cleanup` (not pushed).
- Consolidated `proof.html` + `writing.html` into `work.html`; consolidated `origin.html` + `contact.html` into `about.html` with `#contact` routes. The four superseded HTML routes were removed in greenfield mode.
- Reduced the primary navigation to Home, Work, Century, Enterprise AI, AI Diligence, Founder Advisory and About. The disclosure menu now engages through tablet widths before header collision.
- Replaced visible audit vocabulary with plain-language labels and kept source/claim detail in the QA ledger and Sources page.
- Contact intent cards now update an in-page next-step panel without a document reload; links remain usable without JavaScript.
- Closing sections use the shared container alignment; the BSUIR senior lecturer / ICPC coach record links to the supplied university article without a historical date label.
- Added responsive portraits to the opening hero of every published page: the home and Enterprise AI pages use the boardroom portrait, Founder Advisory uses the educator portrait, and the remaining pages use the warm portrait.
- Tightened the home page for faster scanning: the hero portrait now fills its grid column, the Century teaser keeps one route instead of repeating the recognition claim, and the duplicate biography bridge was removed.
- Corrected the singleton outcome card so it uses a readable desktop width instead of occupying only one third of the grid.
- Removed the redundant Selected outcome block from the home page and increased card padding/gaps across the site for clearer text-to-edge and card-to-card spacing.
- Added a shared 24px heading-to-card/list rhythm, enlarged article-list cards, and removed legacy CSS for unused manifesto, ledger, matrix, marquee, timeline and investor-only components. The remaining `is-selected` rule is intentionally driven by the contact-route JavaScript.
- Incoming-link audit confirms every published destination except the intentional standalone `404.html` has at least one internal route; no published page is orphaned.
- Verification: `node qa/check.mjs`, `node qa/test-regressions.mjs`, `npm test --prefix qa/browser`, custom Pages-artifact viewport checks (1440, 1150, 1024, 768, 390, 320), route no-reload check, and `git diff --check` all pass.
- Pages-equivalent artifact is available locally at `http://127.0.0.1:4173/`; deployment and push remain intentionally pending.
