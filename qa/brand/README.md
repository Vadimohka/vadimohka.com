# Brand claim and source ledger

This directory is the maintainable control layer for public claims used by
vadimohka.com. It is deliberately kept under qa/ so it remains development
only and is excluded by the GitHub Pages deployment workflow.

## Files

- claims.json maps each substantive public claim to a stable C### ID,
  evidence status, scope, exact text variants, public surfaces, and source IDs.
- sources.json maps each S### ID to the URL, date, authority, exact support,
  allowed use, and caveat recorded in the supplied evidence register.

The 2026-08-22 pack registers are the import baseline. Current repository copy
remains authoritative when it has drifted from the dated snapshot; add a new
claim or source record rather than reusing an ID for a materially different
statement.

## Update procedure

1. Search all production HTML, ai-profile.md, llms.txt, llms-full.txt,
   data/entity-graph.json, and sources.html for the wording or its variants.
2. Re-check the supporting URL when network access is available. Confirm the
   person, role, date, scope, and outcome separately; keep company and product
   evidence distinct from personal evidence.
3. Update the existing stable claim record, or add the next unused C### ID.
   Record the exact wording variants and every affected public surface.
4. Add or update the source record with what it proves and the caveat that
   limits its use. Keep last_checked current.
5. Synchronise every affected visible and machine-readable mirror in the same
   task. Do not use this ledger to publish owner-only evidence.
6. Run node qa/check.mjs and the task-specific checks, then write the task
   result under the pack's current results directory.

## Status and scope rules

verified means the source supports the exact wording. partially_verified means
only a narrower statement is safe. owner_confirmed is personal information
supplied by the owner without independent publication. company_level_only is a
company or product fact and is never a personal outcome. unverified and
remove_or_clarify are retained for audit history but are not publishable proof.

Claims marked unverified, remove_or_clarify, or company_level_only cannot be
used as personal hero proof. Method, opinion, navigation, CTA, and
product-description copy without a personal outcome are explicitly classified
as non-claim copy in claims.json until evidence makes them a claim.

Local owner input is intentionally ignored by Git. Do not commit
owner-input.local.yaml, private evidence directories, or screenshots that
contain private data.
