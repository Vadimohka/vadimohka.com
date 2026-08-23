# Safe subagent delegation prompt

Use subagents for independent analysis or review, not overlapping edits.

## Suggested reviewers

### Evidence reviewer

Read the claim/source registers and target task. Return:

- unsupported or overbroad claims;
- exact source mismatch;
- safe replacement;
- missing owner input.

Do not edit files.

### Institutional reader

Review the rendered page as a banker, investor, founder or C-level executive. Return:

- first 30-second interpretation;
- trust blockers;
- proof missing;
- CTA clarity;
- exact copy that caused concern.

Do not edit files.

### Accessibility reviewer

Review HTML/CSS/JS and browser behavior. Return:

- keyboard sequence;
- focus bugs;
- accessible names;
- contrast/type risks;
- mobile overflow;
- reduced-motion issues.

Do not edit files.

### SEO/entity reviewer

Review metadata, canonical, JSON-LD, sitemap and AI-readable files. Return:

- inconsistencies;
- unsupported structured claims;
- entity fragmentation;
- exact fixes.

Do not edit files.

## Integration rule

The main agent:

1. receives all reports;
2. resolves conflicts using the evidence policy;
3. performs the edits;
4. runs complete QA;
5. remains accountable for the final diff.
