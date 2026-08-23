# Site architecture and UI cleanup Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task with review checkpoints.

**Goal:** Consolidate overlapping public pages, remove technical copy, fix the desktop header, make contact actions visibly interactive, and standardise closing-section alignment.

**Architecture:** New `work.html` and `about.html` become the only public destinations for the merged content. The four superseded URLs are removed in greenfield mode. Shared navigation, CSS and JavaScript provide the header, alignment and contact-route behaviour.

**Tech Stack:** Static HTML, shared CSS, vanilla JavaScript, existing Node QA and Playwright/axe browser QA.

**Spec:** `docs/superpowers/specs/2026-08-23-site-architecture-cleanup-design.md`

## Global Constraints

- Preserve the static architecture and visual identity; add no production dependencies.
- Do not add unsupported claims, metrics, client outcomes, current teaching claims, or a personal Century title.
- Keep LinkedIn as the functional contact route; do not invent a form endpoint or email address.
- Keep `qa/`, `site-improvement-pack/` and `reports/` out of the deployment artifact.
- Do not publish visible placeholders or implementation/audit labels.

### Task 1: Add failing regression guards

**Files:**
- Modify: `qa/check.mjs`
- Modify: `qa/browser/check.mjs`

- [ ] Assert that production HTML has no visible technical labels, superseded pages are absent, and new pages exist.
- [ ] Assert the contact route updates state without navigation in the browser suite.
- [ ] Run `node qa/check.mjs` and `npm test --prefix qa/browser`; observe the expected failures before implementation.

### Task 2: Build consolidated public destinations

**Files:**
- Create: `work.html`
- Create: `about.html`
- Modify: `sitemap.xml`, `sitemap-ai.xml`, `sitemap-images.xml`

- [ ] Build `work.html` with current role, Century recognition, public appearances and published Vaiti work, using plain-language headings and no technical labels.
- [ ] Build `about.html` with current role, BSUIR background, operating approach and a contact section with six route cards plus LinkedIn fallback.
- [ ] Give both pages complete metadata, JSON-LD, canonical URLs and the shared navigation.

### Task 3: Remove superseded page bodies

**Files:**
- Delete: `proof.html`, `writing.html`, `origin.html`, `contact.html`

- [ ] Replace duplicated bodies with accessible static redirect shells pointing to `work.html` or `about.html#contact`.
- [ ] Preserve canonical metadata for the destination and a visible fallback link for no-JS clients.

### Task 4: Repair shared header, alignment and copy system

**Files:**
- Modify: `assets/site.css`
- Modify: all production HTML navigation blocks and closing sections

- [ ] Make the desktop navigation single-row and switch to disclosure before collision.
- [ ] Remove visible `Checked`, `Scope`, `Status`, `Proof`, `Evidence map` and similar audit labels from every production page.
- [ ] Remove accidental `.center` use from closing sections that are not true split layouts.
- [ ] Point old and new internal links to `work.html` and `about.html` consistently.

### Task 5: Make contact actions real

**Files:**
- Modify: `assets/site.js`
- Modify: `about.html`

- [ ] Add a `data-route` map with human-readable route names and safe next-step copy.
- [ ] Intercept same-page route links, update the selected card and live region, push query state without reload, focus the response, and preserve no-JS navigation.
- [ ] Ensure the response contains a working LinkedIn link and no confidential-data instruction beyond the existing safe guidance.

### Task 6: Verify and review visually

- [ ] Run `node qa/check.mjs`.
- [ ] Run `node qa/test-regressions.mjs`.
- [ ] Run `npm test --prefix qa/browser`.
- [ ] Run `git diff --check`.
- [ ] Capture 1440px, 1024px, 768px, 390px and 320px screenshots for Home, Work, About and Contact route state; inspect header, closing sections, actions and no-overflow behaviour.
- [ ] Review all changed copy against claim safety and run a production scan for technical labels and placeholders.
