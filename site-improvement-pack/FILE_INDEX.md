# Package index

**Snapshot:** 2026-08-22

## Entry points

- `START_HERE_RU.md` — Russian installation and operating guide.
- `MASTER_PROMPT.md` — Full Codex launcher for the complete programme.
- `install/AGENTS.md` — Optional persistent repository rules template.
- `install/.agents/skills/vadimohka-site-upgrade/SKILL.md` — Optional reusable Codex skill template.

## Manifest

- `manifest/tasks.json` — Machine-readable list of 22 independent tasks.
- `manifest/task-order.md` — Recommended brand-first order and parallelisation rules.
- `manifest/release-gates.md` — Brand and final release gates.
- `manifest/acceptance-matrix.csv` — 125 acceptance criteria ready for evidence/status tracking.
- `manifest/dependency-graph.mmd` — Mermaid dependency graph.

## Evidence

- `evidence/source-register.csv` — 27 public source records with scope and caveats.
- `evidence/claim-register.csv` — 24 claim records with risk and safe wording.
- `evidence/claim-policy.md` — Rules for proof, attribution, numbers, roles and machine parity.
- `evidence/owner-input.example.yaml` — Private owner facts required for stronger proof.
- `evidence/owner-questionnaire.md` — Interview for cases, metrics, roles and permissions.

## Brand and copy

- `context/brand-strategy.md` — Target positioning, ownable territory and message rules.
- `context/audience-strategy.md` — Decision/evidence model for each audience.
- `copy/homepage-v1.md` — Production-oriented homepage narrative and copy.
- `copy/metadata-map.csv` — Page-by-page titles, descriptions, H1s and canonicals.
- `copy/page-briefs/` — Briefs for all principal pages.
- `copy/microcopy-library.md` — CTA, labels, boundaries and prohibited generic wording.

## Design

- `design/homepage-wireframe.md` — Content hierarchy for desktop and mobile.
- `design/component-specs.md` — Evidence-card, public-work, CTA and menu specifications.
- `design/og-image-system.md` — Page-specific social-preview system.

## Tasks

- `tasks/brand/B00–B11.md` — 12 separately committable brand/evidence/content tasks.
- `tasks/technical/T01–T10.md` — 10 separately committable technical/UX/SEO/QA tasks.

## Prompts and templates

- `prompts/RUN_SINGLE_TASK.md` — Execute one task only.
- `prompts/RUN_BRAND_PHASE.md` — Execute brand phase and gate.
- `prompts/RUN_TECHNICAL_PHASE.md` — Execute technical phase after gate.
- `prompts/FINAL_REVIEW.md` — Independent release review.
- `templates/` — Task results, release report, evidence and case intake.

## Validation

- `scripts/validate_pack.py` — Offline package integrity check.
- `scripts/next_task.py` — Find next eligible task from result records.
- `scripts/check_source_links.py` — Optional online evidence-link checker.
- `research/suggested-test-matrix.md` — Browser, viewport, keyboard, accessibility, SEO and performance matrix.
