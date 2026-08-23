# Repository inventory and implementation implications

**Dated snapshot:** 22 August 2026.

## Architecture

- Static HTML pages in repository root.
- Shared CSS in `assets/site.css`.
- Small shared JavaScript in `assets/site.js`.
- GitHub Pages deployment.
- No build step.
- No production dependencies.
- Pure Node QA at `qa/check.mjs`.
- Machine-readable files are committed, not generated at runtime.

## Key implementation implications

### Content changes are duplicated

A role or positioning statement may exist in:

- visible page copy;
- title;
- meta description;
- Open Graph;
- X metadata;
- JSON-LD;
- `ai-profile.md`;
- `llms.txt`;
- `llms-full.txt`;
- `data/entity-graph.json`;
- `sources.html`.

Every claim task must search all representations.

### The deployment may publish unexpected files

The current workflow excludes dev-only paths such as `qa/`. Codex must confirm the exact rsync/exclusion behavior after this pack is added.

### Navigation is repeated

The static header/footer appears across multiple HTML files. A navigation task must update every page and QA consistency.

### No backend exists

A contact form requires:

- a real external endpoint/service;
- a serverless function;
- or a changed hosting architecture.

Until then, use direct links/email and do not pretend a form submits.

### Redirect limitations

GitHub Pages supports limited redirect behavior. A canonical tag is not a true HTTP 301. Do not claim `/index.html` has been permanently redirected unless an edge/hosting rule has been added and verified.

### QA opportunity

Because the site is small and static, meaningful checks can remain fast:

- metadata consistency;
- JSON-LD parse;
- claim/source rules;
- public TODO detection;
- nav consistency;
- local links/assets;
- browser screenshots;
- axe scans;
- Lighthouse baseline.

## Existing likely hotspots

- `index.html`: positioning and first-screen proof.
- `proof.html`: evidence architecture.
- `expert.html`: unresolved public-signal links.
- `contact.html`: conversion.
- `assets/site.css`: mobile navigation, small labels, low-opacity text.
- `data/entity-graph.json`: role/education consistency.
- `llms*.txt` and `ai-profile.md`: risk of broader machine-readable claims.
