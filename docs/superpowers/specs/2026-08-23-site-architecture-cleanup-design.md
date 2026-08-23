# Site architecture and UI cleanup design

## Goal

Make the public site feel like one coherent operator profile: a clean header, plain-language content, visible actions that produce a result, and two consolidated destination pages instead of four overlapping pages.

## Decisions

- `work.html` becomes the public destination for current role, selected work, public appearances and published writing.
- `about.html` becomes the public destination for current role, background, working approach and contact routes.
- `proof.html`, `writing.html`, `origin.html` and `contact.html` are removed in greenfield mode; no duplicate bodies or compatibility aliases remain.
- Primary navigation is reduced to Home, Work, Century, Enterprise AI, AI Diligence, Founder Advisory and About. Contact is a strong in-page action in `about.html`, not a second top-level destination.
- Visible copy removes audit/implementation labels such as `Checked`, `Scope`, `Status`, `Proof`, `Evidence map`, and `Methodology`. The evidence ledger remains in non-public QA files.
- Existing claims stay narrow: no new outcomes, clients, metrics, personal Century title, or current teaching claim is introduced.
- Every action either navigates to a meaningful destination, opens a verified external source, or updates the contact route in place and exposes a LinkedIn next step.
- Section content uses the same left-aligned container; only genuine two-column compositions use a centered split alignment.

## Interaction model

Contact route buttons use progressive enhancement. With JavaScript, selecting a route updates the selected card, changes the URL with `history.pushState`, reveals a focused next-step panel, and does not reload the page. Without JavaScript, the existing query URL still renders the selected route and remains usable.

## Visual model

The header stays single-row at desktop widths with tighter, non-wrapping links and switches to the existing disclosure menu before the links can collide. New pages reuse the existing dark editorial system, but use fewer cards, fewer labels, and a consistent left edge for closing sections.

## Acceptance criteria

1. No production HTML contains the visible strings `Checked`, `Scope:`, `Status:`, `Proof`, or `Evidence map`.
2. Desktop header never wraps or places Contact on a second line at 1440px; mobile menu remains keyboard accessible.
3. `work.html` and `about.html` contain the consolidated content; the four superseded HTML routes are absent.
4. Contact route selection changes visible state without a page reload when JavaScript is enabled and remains usable with JavaScript disabled.
5. Final sections align to the shared container edge unless they are intentionally a two-column split.
6. Static QA, regression QA, axe, responsive browser checks and screenshot review pass.
