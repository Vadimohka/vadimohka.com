# Current state snapshot

**Observed:** 22 August 2026  
**Repository:** `Vadimohka/vadimohka.com`  
**Deployment model:** static GitHub Pages, no build step, no production dependencies.

## Current repository shape

Public pages:

- `index.html`
- `enterprise.html`
- `founders.html`
- `investors.html`
- `origin.html`
- `century.html`
- `proof.html`
- `expert.html`
- `writing.html`
- `contact.html`
- `sources.html`
- `404.html`

Supporting files:

- `assets/site.css`
- `assets/site.js`
- portrait and Open Graph images under `assets/`
- `data/entity-graph.json`
- `ai-profile.md`
- `llms.txt`
- `llms-full.txt`
- `robots.txt`
- `sitemap.xml`
- `sitemap-images.xml`
- `sitemap-ai.xml`
- `qa/check.mjs`
- GitHub Pages deployment workflow.

## Existing strengths

- Static architecture and very small JavaScript surface.
- System font stacks; no external font requests.
- Semantic landmarks are already used.
- One H1 per page.
- Canonical, Open Graph, X metadata, robots, sitemaps, and JSON-LD exist.
- Images generally have alt text and explicit dimensions.
- Responsive grids work without general document overflow in source-based checks.
- Existing pure-Node QA catches common static-site errors.
- Visual identity is coherent: dark editorial palette, restrained animation, executive photography.

## Material weaknesses

### Brand and evidence

- The visual level is stronger than the published commercial proof.
- Homepage H1 is only the name; the role is outside the H1.
- The repeated phrase “serious environments” signals status but not a concrete operating condition or outcome.
- Hero proof points are mostly roles, sectors, or reach metrics rather than business outcomes.
- `proof.html` mixes responsibilities, beliefs, and evidence.
- `expert.html` contains four public-signal cards that were published without working source links; source comments explicitly indicated that verified URLs were still required.
- Banks, fintech, investment-company, international-corporation, investor-diligence, and team-scale claims are broader than the public personal evidence.
- `writing.html` is too thin to substantiate strong thought-leadership positioning.
- Several current and legacy profiles use different primary titles.

### Conversion

- Contact routes mainly to LinkedIn, Century, or another internal page.
- No direct professional email is visible.
- No intent-specific inquiry path exists.
- A functional form cannot be added safely until an endpoint and privacy approach are known.

### UX and accessibility

- On narrow screens, primary navigation becomes a horizontally scrollable row.
- Some meaningful labels are 9–10 px on compact mobile.
- Some secondary text uses low opacity and may fail WCAG AA contrast.
- No skip-to-content link was observed.
- Full keyboard, screen-reader, physical-device, and browser-matrix testing has not yet been performed.

### Technical SEO and entity consistency

- `/index.html` remains reachable; canonical points to `/`, but GitHub Pages alone does not provide arbitrary true 301 rules.
- Root URL formatting is not fully consistent across sitemap and canonical representations.
- Schema nodes do not use a fully unified stable `@id` graph.
- Person properties differ between pages.
- Some organisation relations and exact credentials are unclear.
- One shared OG image is used for pages with materially different intents.
- The old `.ru` site and external profiles create message fragmentation.

## Existing commands

```bash
python3 -m http.server 4173
node qa/check.mjs
```

## Snapshot limitation

This document is a dated audit snapshot. Codex must inspect the current repository before editing and must not overwrite newer work merely to match this file.
