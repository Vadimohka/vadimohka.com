# Run the brand phase

Execute the Brand phase only: B00 through B11.

## Rules

- Work sequentially unless independent research is delegated without overlapping edits.
- Produce a result file after every task.
- Re-run baseline QA after every task.
- Do not perform technical enhancement tasks except a minimal fix that is strictly required to complete a brand task.
- Use conservative copy when owner input is missing.
- Do not treat company-level evidence as personal proof.
- Do not publish visible placeholders.
- After B11, run the Brand Release Gate and create:
  `qa/site-improvement-pack/reports/brand-gate-report.md`.

## Stop condition

Stop the phase if:

- a P0 claim cannot be safely removed or verified;
- a current role is materially disputed;
- implementation would publish confidential information;
- the owner must choose between legally or commercially different statements.

Otherwise continue with safe defaults.

## Final response

Summarise:

- tasks completed;
- claim risks removed;
- pages materially changed;
- owner inputs still missing;
- Brand Release Gate result;
- whether the technical phase is eligible to start.
