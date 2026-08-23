# Recommended task order

Every task is self-contained and separately committable. Dependencies still matter because brand decisions change the content that technical work must encode.

## Phase 0 — Preflight

- inspect current branch and repository drift;
- run `node qa/check.mjs`;
- confirm `qa/` is excluded from production deployment;
- verify that the pack and root `AGENTS.md` do not overwrite newer project instructions.

## Phase 1 — Brand, evidence and content

1. **B00 — Establish the claim and source control layer** (`P0`)
2. **B01 — Repair all public expertise signals with primary links** (`P0`)
3. **B02 — Consolidate master positioning, roles and claim language** (`P1`)
4. **B03 — Rebuild the homepage narrative around authority and proof** (`P1`)
5. **B04 — Transform Proof into a verified Track Record** (`P1`)
6. **B05 — Reframe the Enterprise page for regulated organisations** (`P1`)
7. **B06 — Reframe Investors as AI technical diligence** (`P1`)
8. **B07 — Reframe Founders as a CTO-level diagnostic** (`P1`)
9. **B08 — Turn Century into the primary product proof** (`P1`)
10. **B09 — Build a verified media, speaking and insights system** (`P1`)
11. **B10 — Implement intent-specific conversion architecture** (`P1`)
12. **B11 — Produce and execute the external identity consistency plan** (`P1`)

## Brand Release Gate

Run the gate in `release-gates.md`. Do not proceed merely because all task files were touched. The site must have no P0 evidence risk and no visible unsupported placeholder.

## Phase 2 — Technical, UX, SEO and QA

1. **T01 — Implement the staged information architecture and navigation labels** (`P1`)
2. **T02 — Replace horizontal mobile navigation with an accessible disclosure menu** (`P1`)
3. **T03 — Fix contrast, typography, focus and motion accessibility** (`P1`)
4. **T04 — Unify metadata and the structured entity graph** (`P1`)
5. **T05 — Harden canonical, sitemap, robots and URL consistency** (`P1`)
6. **T06 — Implement the contact route safely on a static site** (`P1`)
7. **T07 — Extend dependency-free static QA for brand and SEO consistency** (`P1`)
8. **T08 — Add browser, responsive and accessibility regression tests** (`P2`)
9. **T09 — Measure and optimise performance and sharing assets** (`P2`)
10. **T10 — Synchronise machine-readable profiles and complete release regression** (`P1`)

## Final Release Gate

Run static QA, browser/a11y tests, machine-readable parity review, deployment-output review and live-link checks. Produce the final release report.

## Parallelisation guidance

Safe to parallelise for **research/review only**:

- B05, B06 and B07 page review after B02;
- external source re-checks;
- browser screenshots across different engines;
- independent final review.

Avoid concurrent edits to:

- global navigation;
- homepage;
- metadata;
- JSON-LD;
- `llms*`;
- `ai-profile.md`;
- `data/entity-graph.json`;
- shared CSS/JS.

The main agent must integrate and verify every parallel result.
