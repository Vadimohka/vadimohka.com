---
name: vadimohka-site-upgrade
description: Plan, implement, verify, or review brand-first improvements to vadimohka.com. Use for positioning, evidence, homepage, track record, audience pages, conversion, accessibility, SEO, schema, responsive UX, QA, and release work governed by qa/site-improvement-pack.
---

# Vadimohka site upgrade workflow

Use this skill only for the `vadimohka.com` repository or a working copy of it.

## Start

1. Read root `AGENTS.md` if installed; otherwise read `qa/site-improvement-pack/install/AGENTS.md`.
2. Read `qa/site-improvement-pack/MASTER_PROMPT.md`.
3. Read `qa/site-improvement-pack/manifest/tasks.json`.
4. Inspect the current repository and note any drift from the dated snapshot.
5. Select exactly one task unless the user explicitly requests a phase or batch.

## Task execution

- Open the selected task file.
- Load only the referenced context, evidence, and copy files.
- Resolve safe implementation details yourself.
- Do not ask for owner input when a conservative, truthful fallback exists.
- If a required fact cannot be safely inferred, omit the public claim and record the missing input in the task result.
- Keep each task independently reviewable.
- Never mix unrelated technical cleanup into a brand task.

## Brand-first gate

Do not execute `T*` tasks until the Brand Release Gate passes, except for a narrowly necessary fix that blocks a brand task. If such a fix is needed, keep it minimal and document why.

## Verification

Always run:

```bash
node qa/check.mjs
```

Then run the checks named in the task. Review all changed claims across HTML, metadata, structured data, AI-readable files, and sources.

## Output

Use `qa/site-improvement-pack/templates/task-result.md`. Include:

- task ID;
- changed files;
- claims added, changed, or removed;
- source IDs used;
- tests run and outcomes;
- screenshots or manual checks performed;
- unresolved owner inputs;
- rollback notes.
