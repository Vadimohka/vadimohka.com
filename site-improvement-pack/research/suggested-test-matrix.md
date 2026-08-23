# Suggested test matrix

## Viewports

- 1440 × 1000 — desktop.
- 1024 × 768 — small desktop/tablet landscape.
- 768 × 1024 — tablet portrait.
- 390 × 844 — common mobile.
- 320 × 568 — compact mobile.

## Browsers

Minimum manual or automated coverage:

- Chromium.
- Firefox.
- WebKit/Safari engine.

Physical-device checks are still useful for:

- iOS Safari sticky header and menu;
- Android Chrome focus/touch targets;
- text resizing;
- reduced motion.

## Keyboard scenarios

1. First Tab reveals Skip to main content.
2. Header navigation follows visual order.
3. Mobile menu opens with Enter and Space.
4. Focus moves into the open menu or remains predictably controlled.
5. Escape closes the menu.
6. Focus returns to the menu button.
7. All CTAs and source links are reachable.
8. No focus trap.
9. Visible focus meets contrast requirements.

## Accessibility checks

- one H1;
- logical heading order;
- landmark structure;
- descriptive link text;
- non-decorative images have meaningful alt;
- decorative images have empty alt;
- controls have accessible names;
- normal text contrast ≥ 4.5:1;
- large text contrast ≥ 3:1;
- focus indicator visible;
- content usable at 200% zoom;
- no horizontal page overflow;
- reduced-motion behavior;
- no serious/critical axe violations.

## SEO checks

- title and description present/unique;
- canonical exact;
- OG and X tags;
- OG image resolves and has dimensions;
- valid JSON-LD;
- stable Person `@id`;
- no unsupported Person properties;
- sitemap only contains indexable canonical URLs;
- `robots.txt` references valid sitemaps;
- no conflicting slash variants;
- no accidental indexation of dev pack.

## Claim checks

- no production `TODO`;
- no `[OWNER_INPUT_REQUIRED]`;
- no public-signal card without `href`;
- all visible dates match sources;
- no personal claim sourced only from company logos;
- machine-readable role matches visible current role;
- MIPT absent unless exact credential is supplied;
- no invented metrics.

## Performance checks

Measure before setting targets:

- Lighthouse mobile and desktop;
- LCP element;
- CLS causes;
- main-thread work;
- total asset weight;
- image dimensions/format;
- unused CSS;
- cache behavior.

Do not record a score in marketing copy.
