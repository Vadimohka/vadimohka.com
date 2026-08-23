# Independent claim verification review

Review the current repository without changing production files.

## Scope

- all visible HTML;
- titles/descriptions;
- Open Graph and X metadata;
- JSON-LD;
- `data/entity-graph.json`;
- `ai-profile.md`;
- `llms.txt`;
- `llms-full.txt`;
- `sources.html`.

## Method

1. Extract every substantive claim.
2. Map it to `qa/brand/claims.json` or the pack claim register.
3. Verify source IDs and exact wording.
4. Classify each occurrence:
   - safe;
   - too broad;
   - outdated;
   - company-level misattribution;
   - unverified;
   - inconsistent;
   - low-authority but true.
5. Check dates, current/former roles and product/person attribution.
6. Re-check external URLs when network access exists.
7. Do not accept the website itself as independent proof.

## Output

Create `qa/site-improvement-pack/reports/claim-review.md` with:

- P0/P1/P2 findings;
- exact file and excerpt;
- claim ID;
- source IDs;
- why the wording is unsafe;
- exact safe replacement or removal;
- cross-file mirrors that must change.

Do not implement changes in this review.
