# Independent final review

Act as a sceptical institutional reviewer and senior frontend/SEO engineer. Do not assume the implementing agent completed the work correctly.

## Review lenses

1. Investor.
2. Bank / financial institution.
3. Enterprise / FinTech executive.
4. Founder.
5. C-level / board reader.
6. Accessibility reviewer.
7. Technical SEO/entity reviewer.
8. Static-site maintainer.

## Required checks

- Read the release report and every task result.
- Inspect the complete diff from the pre-programme baseline.
- Re-run all documented checks.
- Re-extract substantive claims and compare to evidence.
- Review first-screen screenshots at desktop and mobile.
- Keyboard-test navigation and CTAs.
- Check responsive overflow.
- Validate JSON-LD and metadata.
- Inspect deployment output for dev/private files.
- Open all proof links.
- Confirm no task has marked an unverified acceptance criterion as complete.
- Confirm performance claims are measurements, not assumptions.

## Output

Create `qa/site-improvement-pack/reports/independent-final-review.md`.

Classify findings:

- Block release.
- Fix before release.
- Follow-up.
- Accepted limitation.

End with one of:

- `APPROVE`
- `APPROVE WITH DOCUMENTED LIMITATIONS`
- `DO NOT RELEASE`

Do not make production edits during this review.
