# Optional persistent Codex bootstrap

The archive is safe to extract into the repository root because all package files live under `qa/site-improvement-pack/`, which the audited deployment workflow excludes.

The instruction templates are intentionally not placed at repository root by default. The audited workflow excludes `qa/` but did not exclude root `AGENTS.md` or `.agents`; installing them without updating deployment could publish internal instructions.

## Default mode — safest

Do not copy anything. Start Codex with `MASTER_PROMPT.md`. It explicitly loads the nested instruction and skill templates.

## Optional persistent mode

Use only after inspecting the current workflow.

1. Confirm the Pages assembly excludes:
   - `qa`;
   - `AGENTS.md`;
   - `.agents`.
2. If `AGENTS.md` already exists, merge the template; never overwrite it.
3. Copy:
   - `qa/site-improvement-pack/install/AGENTS.md` → `AGENTS.md`
   - `qa/site-improvement-pack/install/.agents/` → `.agents/`
4. Assemble `_site` locally or inspect the workflow artefact.
5. Confirm neither file/directory appears in production output.
6. Commit the workflow exclusion and instruction installation together.

## Required workflow intent

The rsync assembly should contain exclusions equivalent to:

```text
--exclude='qa'
--exclude='AGENTS.md'
--exclude='.agents'
```

Do not assume the dated workflow is unchanged. Inspect first.
