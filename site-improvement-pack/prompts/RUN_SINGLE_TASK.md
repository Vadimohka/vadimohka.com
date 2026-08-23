# Run one independent task

Execute exactly one task: `<TASK_ID>`.

1. Read `AGENTS.md` and the local site-upgrade skill.
2. Read `qa/site-improvement-pack/manifest/tasks.json`.
3. Open the task file mapped to `<TASK_ID>`.
4. Inspect the current repository and report material drift from the task assumptions.
5. Check dependencies:
   - if a dependency is incomplete but a safe independent implementation is still possible, proceed conservatively and record the limitation;
   - if proceeding would encode an unsettled brand decision, stop before editing and report the exact blocker.
6. Run baseline `node qa/check.mjs`.
7. Implement only the task scope.
8. Never invent missing owner facts. Omit or narrow public claims.
9. Run all acceptance checks.
10. Review the diff for unrelated changes.
11. Write `qa/site-improvement-pack/results/<TASK_ID>.md` from the task-result template.
12. Return:
    - outcome;
    - files changed;
    - claims changed;
    - source IDs used;
    - tests and screenshots;
    - unresolved owner inputs;
    - next eligible task.

Do not start another task in the same turn.
