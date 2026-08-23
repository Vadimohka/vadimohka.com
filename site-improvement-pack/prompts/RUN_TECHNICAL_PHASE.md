# Run the technical phase

Execute T01 through T10 only after verifying that the Brand Release Gate passes.

## Preflight

1. Read the brand-gate report.
2. Re-run `node qa/check.mjs`.
3. Confirm current visible copy and machine-readable identity are stable.
4. Confirm the pack and all local/private inputs are excluded from deployment.

## Rules

- Preserve the static architecture and visual identity.
- Do not migrate frameworks.
- No production dependencies.
- Development-only browser/a11y dependencies must remain outside production output.
- Do not change brand claims merely to satisfy a technical implementation.
- Measure performance before setting targets.
- Do not call canonical or client-side navigation a true 301.
- Do not add a form without a real endpoint and privacy handling.
- Produce a result record after every task.

## Finish

Run the Final Release Gate and create the release report. Include exact commands, environment, results, known limitations, deployment-output review and post-deploy smoke test.
