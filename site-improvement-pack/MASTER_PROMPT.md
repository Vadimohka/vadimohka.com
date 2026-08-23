# Master prompt for Codex — vadimohka.com brand-first upgrade

You are the implementation owner for a staged improvement programme for the static website `vadimohka.com`.

## First actions

1. Confirm that the current working directory is the repository root.
2. Read, in this order:
   - `qa/site-improvement-pack/install/AGENTS.md` (or root `AGENTS.md` if the template has already been safely installed)
   - `qa/site-improvement-pack/install/.agents/skills/vadimohka-site-upgrade/SKILL.md` (or the root skill if installed)
   - `qa/site-improvement-pack/START_HERE_RU.md`
   - `qa/site-improvement-pack/context/current-state.md`
   - `qa/site-improvement-pack/context/non-negotiables.md`
   - `qa/site-improvement-pack/context/brand-strategy.md`
   - `qa/site-improvement-pack/evidence/claim-policy.md`
   - `qa/site-improvement-pack/manifest/tasks.json`
   - `qa/site-improvement-pack/manifest/task-order.md`
   - `qa/site-improvement-pack/manifest/release-gates.md`
3. Inspect the repository and compare it with the dated snapshot. Treat current code as authoritative when structure has changed, but preserve the pack’s strategy and safety rules.
4. Read `qa/site-improvement-pack/install/BOOTSTRAP.md`. Persistent root instructions are optional. Install them only after the deployment workflow excludes `AGENTS.md` and `.agents`, and never overwrite an existing instruction file without merging it.
5. Run the existing baseline QA before editing:
   ```bash
   node qa/check.mjs
   ```
6. Produce a short preflight note containing:
   - current branch and dirty/clean state;
   - current page inventory;
   - baseline QA result;
   - material drift from the pack snapshot;
   - the next eligible task.

## Execution objective

Execute the tasks in `manifest/tasks.json` in recommended order:

1. all `B*` brand/evidence/content tasks;
2. Brand Release Gate;
3. all `T*` technical/UX/SEO/QA tasks;
4. Final Release Gate.

Each task must remain independently reviewable and separately committable. Do not combine multiple tasks merely because they touch the same file. When the user requests the full programme, continue task by task and produce a result record after each task. When the environment supports independent subagents, they may research or review separate tasks, but they must not edit overlapping files concurrently and the main agent must integrate and verify every result.

## Decision policy

Make safe implementation decisions without repeatedly asking for clarification.

Ask or stop only when:
- a change would publish confidential information;
- a required external service, email address, form endpoint, or legal text is missing and there is no truthful fallback;
- a claim would materially change professional or legal meaning;
- the current repository contradicts a verified source in a way that cannot be resolved conservatively.

Otherwise:
- use the conservative copy supplied in the pack;
- omit unsupported claims;
- record missing owner input in the task result;
- never put a visible placeholder on the production site.

## Brand outcome

The site should position Vadim as:

> An enterprise AI CTO and product operator focused on governed private AI for regulated organisations, connecting product, architecture, security, adoption, and controlled production.

The strongest defensible archetype is operator / CTO / technical founder. Do not manufacture investor, board-level, global-leader, or thought-leader authority.

The homepage narrative must follow:

> Identity → Authority → Proof → Relevance → Depth → Trust → Action

## Claim discipline

Before adding or strengthening any claim:

1. Find it in `evidence/claim-register.csv`.
2. Check the supporting source IDs in `evidence/source-register.csv`.
3. Confirm whether the source proves:
   - the person;
   - the role;
   - the date;
   - the scope;
   - the outcome.
4. Keep company-level evidence separate from personal evidence.
5. If evidence is incomplete, narrow or omit the claim.
6. Synchronise all affected representations:
   - visible HTML;
   - title and meta description;
   - Open Graph and X metadata;
   - JSON-LD;
   - `ai-profile.md`;
   - `llms.txt`;
   - `llms-full.txt`;
   - `data/entity-graph.json`;
   - `sources.html`.

Never invent or infer numeric outcomes.

## Engineering outcome

Preserve the static architecture and visual identity. Improve:

- accessible mobile navigation;
- skip link, keyboard behavior, focus, contrast, and readable type;
- semantic page labels and navigation;
- metadata, structured data, canonical consistency, sitemaps, and OG assets;
- conversion routes without a fake or non-functional form;
- repeatable claim, HTML, schema, responsive, accessibility, and release QA;
- performance only after measuring a baseline.

Do not add production dependencies or migrate frameworks.

## Task loop

For each task:

1. Read the task file.
2. Inspect every listed target file.
3. Re-run source verification when network access is available; otherwise use the supplied evidence register and do not broaden claims.
4. Implement only the task scope.
5. Run:
   ```bash
   node qa/check.mjs
   ```
6. Run task-specific checks.
7. Review the diff against:
   - claim safety;
   - visual hierarchy;
   - mobile behavior;
   - metadata and machine-readable consistency;
   - internal and external links;
   - accidental private data;
   - unsupported adjectives or metrics.
8. Write a result using `templates/task-result.md`.
9. Update task status only when every acceptance criterion is verified.
10. Suggest the next eligible task.

## Completion

The programme is complete only when:

- all Brand Release Gate conditions pass;
- all technical tasks pass their acceptance criteria;
- baseline and enhanced QA pass;
- no production TODO or placeholder remains;
- no public signal lacks a working source;
- no machine-readable file overstates the visible/evidenced profile;
- responsive and keyboard checks are documented;
- a final release report is produced from `templates/release-report.md`.

Begin with preflight, then execute `B00`.
