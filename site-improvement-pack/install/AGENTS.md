# AGENTS.md — vadimohka.com

## Repository model

- This is a static GitHub Pages site.
- Preserve the no-build, no-production-dependency architecture unless a task explicitly proves that a change is necessary.
- Local preview: `python3 -m http.server 4173`
- Required baseline QA: `node qa/check.mjs`
- The execution pack is in `qa/site-improvement-pack/`.
- The reusable workflow skill template is in `qa/site-improvement-pack/install/.agents/skills/vadimohka-site-upgrade/`. If installed at repository root, it is in `.agents/skills/vadimohka-site-upgrade/`.

## Work order

1. Complete brand and evidence tasks before technical enhancement tasks.
2. Work on one manifest task at a time unless the user explicitly requests a multi-task batch.
3. Treat every task as a separately reviewable change.
4. Do not start the technical phase until the Brand Release Gate in `qa/site-improvement-pack/manifest/release-gates.md` passes.

## Claim safety

- Never invent clients, deployments, transaction volume, revenue, funding, exits, team size, users, AUM, mandates, testimonials, certifications, awards, dates, or external profile changes.
- Distinguish personal evidence from company-level evidence.
- A company client logo or company metric does not prove Vadim's personal role.
- Do not publish placeholders, internal TODO comments, or `[OWNER_INPUT_REQUIRED]`.
- When evidence is missing, use conservative wording or omit the claim.
- Update visible copy, metadata, JSON-LD, `ai-profile.md`, `llms.txt`, `llms-full.txt`, `data/entity-graph.json`, and `sources.html` together when a claim changes.
- Use `qa/site-improvement-pack/evidence/claim-register.csv` and `source-register.csv` as the starting evidence ledger, but re-check the current repository before editing.

## Brand rules

- Primary positioning: enterprise AI CTO and product operator focused on governed private AI for regulated organisations.
- Strongest current archetype: operator / CTO / technical founder.
- Do not position Vadim as an investor, global industry leader, board-level authority, or established thought leader without new verified evidence.
- Prefer proof over adjectives.
- Replace vague status language such as “serious environments” and “high stakes” with concrete conditions such as regulated, private, audited, governed, production, or decision-specific language.
- The homepage narrative must follow: Identity → Authority → Proof → Relevance → Depth → Trust → Action.
- Keep English as the production language of the `.com` site until a complete multilingual plan is approved.

## Engineering rules

- Preserve the current visual identity unless a task requires a specific component change.
- Do not migrate to a framework merely to simplify editing.
- Do not add production JavaScript libraries.
- Development-only dependencies are allowed only when they materially improve repeatable QA and are documented.
- Use semantic HTML, progressive enhancement, visible keyboard focus, reduced-motion support, and accessible mobile navigation.
- Keep all URLs and legacy inbound links working. Do not claim a true 301 redirect is implemented on GitHub Pages unless the hosting layer actually supports it.
- Do not report Lighthouse, Core Web Vitals, rankings, traffic, or conversion numbers unless they were measured in the current task.

## Completion rules

For every task:

1. Read the task file and all referenced pack files.
2. Inspect current files before making changes; the pack is a dated specification, not a blind patch.
3. Make the smallest coherent change that satisfies the task.
4. Run `node qa/check.mjs`.
5. Run any task-specific checks.
6. Review the diff for claim inflation, broken links, metadata drift, responsive regressions, and accidental publication of private inputs.
7. Write a concise result using `qa/site-improvement-pack/templates/task-result.md`.
8. Do not mark a task complete when an acceptance criterion is unverified.
