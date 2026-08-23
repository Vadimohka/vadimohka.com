#!/usr/bin/env python3
"""Show the next eligible task based on result records."""

from __future__ import annotations

import json
import re
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]


def result_status(task_id: str) -> str:
    path = PACK / "results" / f"{task_id}.md"
    if not path.exists():
        return "not_started"
    text = path.read_text(encoding="utf-8")
    match = re.search(r"`(complete|blocked|partially complete)`", text, re.I)
    return match.group(1).lower().replace(" ", "_") if match else "unknown"


def main() -> int:
    manifest = json.loads((PACK / "manifest" / "tasks.json").read_text(encoding="utf-8"))
    tasks = sorted(manifest["tasks"], key=lambda item: item["order"])
    status = {task["id"]: result_status(task["id"]) for task in tasks}

    for task in tasks:
        task_id = task["id"]
        if status[task_id] == "complete":
            continue
        incomplete_deps = [
            dep for dep in task.get("dependencies", []) if status.get(dep) != "complete"
        ]
        if incomplete_deps:
            continue
        print(f"{task_id}: {task['title']}")
        print(f"Phase: {task['phase']} | Priority: {task['priority']}")
        print(f"File: qa/site-improvement-pack/{task['file']}")
        print(f"Status: {status[task_id]}")
        return 0

    unfinished = [task["id"] for task in tasks if status[task["id"]] != "complete"]
    if unfinished:
        print("No task is currently eligible. Unfinished tasks:", ", ".join(unfinished))
        print("Check blocked or incomplete dependencies.")
        return 2

    print("All tasks are recorded as complete. Run the Final Release Gate.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
