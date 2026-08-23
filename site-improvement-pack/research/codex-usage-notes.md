# Codex usage notes

This package supplies two optional repository-native mechanisms:

1. an `AGENTS.md` template for durable repository guidance;
2. a `.agents/skills/vadimohka-site-upgrade/SKILL.md` template for the reusable workflow.

They remain nested under `qa/site-improvement-pack/install/` by default so internal instructions are not accidentally deployed. The master prompt loads them explicitly and is the programme launcher. `install/BOOTSTRAP.md` explains safe root installation.

## Why the instructions are split

The supplied `AGENTS.md` template stays concise and contains rules that apply to every task:

- architecture;
- brand safety;
- work order;
- testing;
- completion.

Detailed research stays under `qa/site-improvement-pack/`, so it is loaded only when relevant.

## Recommended interaction patterns

### Full programme

Paste `MASTER_PROMPT.md`. Codex should preflight and begin at B00.

### One task

Use `prompts/RUN_SINGLE_TASK.md` with a task ID.

### Brand only

Use `prompts/RUN_BRAND_PHASE.md`.

### Technical only

Use `prompts/RUN_TECHNICAL_PHASE.md` only after the Brand Release Gate passes.

### Independent review

Use `prompts/FINAL_REVIEW.md` in a separate Codex thread or after implementation.

## Parallel work

Parallel research/review is safe only when agents do not edit overlapping files. The main agent must integrate and run the complete checks. Brand tasks often touch shared metadata and machine-readable files, so concurrent editing is usually more expensive than sequential work.

## Context discipline

A task file is intentionally self-contained. Codex should load:

- the task;
- referenced evidence rows;
- relevant page brief;
- current target files.

It should not load the entire pack for every small task.

## Security

Never paste private client details into a cloud environment unless the owner has approved the environment and data handling. `owner-input.local.yaml` should remain local and uncommitted.
