# Executive Focus redesign

Base: `main` at `1044094debad7145cb9d923ea2100d54c56f2848`.

## Presentation

Concept 03: graphite surfaces, restrained champagne actions, serif editorial
headlines and clear sans-serif body copy. No client logos, fabricated metrics,
stock skylines or unverified product screenshots are added. The original supplied
720 × 900 portrait is unchanged; CSS fades its edges into the first-screen horizon.

The homepage is reorganized as introduction → Century → relevance/advisory →
operating approach → public work → contact. All original headings, substantive
paragraphs, recognition, source destinations and anchor IDs are retained. The
second homepage portrait and its standalone introductory composition are removed;
the original mandate copy is retained in a compact editorial split. Four public
records share a two-column desktop grid and a mobile stack. No content carousel or
autoplay is introduced.

The Century visual is a labelled HTML architecture overview, NOT a screenshot of
a shipping interface. Its labels are already described in `century.html`.

`assets/site.css` is replaced with the shared design system, not appended overrides.
The other nine HTML pages are unchanged. Compact shared hero, cards, split layouts,
source records and closing sections bring the direction to the entire site.
Navigation still exposes the same seven destinations. Inquiry routes, focus,
keyboard and no-JavaScript behavior remain available. The unused pointer-light
handler is removed; no new runtime dependencies, fonts or tracking are introduced.

## Preservation and QA

`node qa/executive-content.mjs` checks nine unchanged HTML pages and the existing
identity/discovery/deployment assets byte-for-byte, and checks every original
homepage heading/paragraph, link destination and anchor after reordering. Its
baseline is a review fixture; update it deliberately when future content changes
are approved, not to silence a failed redesign check.

Existing static and browser checks remain. Browser QA additionally verifies the
single homepage image, product-first order, compact portrait scale and content
integrity; axe now covers all 10 pages rather than three. Chromium, Firefox and
WebKit execute the same 16-width matrix in the existing PR workflow.

Local rendering uses system Chromium with source HTML/CSS/JS inlined because the
local browser cannot navigate to the preview server. It is visual/geometry QA, not
a substitute for the unmodified network-served site and navigation tests in CI.

## Publication

Changes are developed on `design/executive-focus` and reviewed through a PR.
The main-branch deployment workflow, canonical URLs, sitemaps, metadata and factual
role statements are untouched. Merging the PR triggers the existing Pages workflow.
