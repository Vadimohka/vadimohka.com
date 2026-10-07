# Executive Focus redesign

Base: `main` at `1044094debad7145cb9d923ea2100d54c56f2848`.

## Presentation

The revised Concept 03 implementation is a photographic, editorial composition:
near-black surfaces, restrained champagne actions, Playfair Display headlines and
DM Sans body/UI text. The supplied 720 × 900 image file remains unchanged. An SVG
silhouette mask and a responsive chest-up crop integrate the portrait into a
photographic Earth-at-night horizon. Tablet framing centers the image inside its
container, rather than reusing a fixed desktop offset.

The homepage order is introduction → Century → advisory → practical approach →
public work → contact. Duplicate introductory composition and the second portrait
are removed. All factual paragraphs, recognition, source destinations and anchor
IDs are retained. The full original biography and mandate are available in a
native details disclosure that works without JavaScript. Editorial headings and
short UI labels are intentionally revised; the content checker records those
specific mappings instead of regenerating the original baseline.

Century is represented by layered HTML architectural panels with an explicit
illustration caption, NOT a screenshot of a shipping interface. Labels are based
on capabilities already described in `century.html`; no customer data, metrics or
endorsements are invented. Three public records use decorative editorial images;
the fourth speaking record remains in a compact linked row. No carousel/autoplay.

The skyline in the contact section and the article thumbnails are decorative,
not photographs of the author's offices or claims about event locations. Image
sources and font licenses are recorded in `assets/executive/credits.json` and
adjacent OFL files. Assets and subset WOFF2 fonts are self-hosted; there are no
third-party runtime requests, new JavaScript dependencies or tracking additions.
The temporary branch-only asset preparation workflow is removed from the final tree.

`assets/site.css` contains the shared design system. The other nine HTML pages are
unchanged. Shared typography, hero proportions, cards, split layouts and closing
sections apply the direction across the site. Navigation still exposes the same
seven destinations. Inquiry routes, keyboard focus, no-JavaScript navigation and
reduced-motion behavior remain available. The unused pointer-light handler is removed.

## Preservation and QA

`node qa/executive-content.mjs` pins 21 original files, including nine unchanged
HTML pages, identity/discovery/deployment assets and the supplied portrait. It also
checks the homepage metadata, 33 original text units (with explicit editorial
mappings), link destinations and anchor IDs. Do not change the baseline merely to
silence a failed redesign check.

Browser QA tests all 10 routes at 19 viewport sizes from 320 to 1920px, including
navigation/hero breakpoint boundaries and short landscape screens. It checks
container alignment, text/control clipping, portrait framing, touch targets,
expanded mandate content, illustration/caption separation, font loading, keyboard
navigation, resize focus, six inquiry routes, reduced motion and no-JavaScript use.
Axe serious/critical checks cover all ten pages. Full-page screenshots cover all
routes at 390 and 1440px in Chromium, Firefox and WebKit.

Full-page capture scrolls each real image into view, waits for its native lazy
request and successful decoding, and then returns to the top. It does not suppress
load errors or force visibility as a substitute for testing actual content.

Local rendering uses system Chromium with source HTML/CSS/JS inlined because the
local browser cannot navigate to the preview server. Local visual/geometry review
is not a substitute for the network-served site and navigation tests in CI.

## Publication

Changes are developed on `design/executive-focus` and reviewed through PR #5.
The main-branch deployment workflow, canonical URLs, sitemaps, metadata and factual
role statements are untouched. No production deployment is performed by this work.
Merging the PR triggers the existing Pages workflow.
