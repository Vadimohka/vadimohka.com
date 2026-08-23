#!/usr/bin/env python3
"""Validate the structure and internal references of the site-improvement pack."""

from __future__ import annotations

import csv
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

PACK = Path(__file__).resolve().parents[1]
ROOT = PACK.parents[1]


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)


def main() -> int:
    errors: list[str] = []

    manifest_path = PACK / "manifest" / "tasks.json"
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail(f"Cannot parse {manifest_path}: {exc}")
        return 1

    tasks = manifest.get("tasks", [])
    ids = [task.get("id") for task in tasks]
    if len(ids) != len(set(ids)):
        errors.append("Task IDs are not unique.")

    id_set = set(ids)
    phase_seen_technical = False
    for task in sorted(tasks, key=lambda item: item.get("order", 9999)):
        task_id = task.get("id")
        phase = task.get("phase")
        if phase == "Technical":
            phase_seen_technical = True
        if phase == "Brand" and phase_seen_technical:
            errors.append(f"Brand task {task_id} appears after a technical task.")
        for dep in task.get("dependencies", []):
            if dep not in id_set:
                errors.append(f"{task_id} depends on missing task {dep}.")
        task_file = PACK / task.get("file", "")
        if not task_file.is_file():
            errors.append(f"Missing task file for {task_id}: {task_file}")
        else:
            text = task_file.read_text(encoding="utf-8")
            if f"# {task_id} " not in text and f"# {task_id} —" not in text:
                errors.append(f"Task heading mismatch in {task_file}.")

    source_path = PACK / "evidence" / "source-register.csv"
    claim_path = PACK / "evidence" / "claim-register.csv"

    with source_path.open(encoding="utf-8", newline="") as handle:
        sources = list(csv.DictReader(handle))
    source_ids = [row["source_id"] for row in sources]
    if len(source_ids) != len(set(source_ids)):
        errors.append("Source IDs are not unique.")
    source_set = set(source_ids)

    for row in sources:
        url = row.get("url", "").strip()
        parsed = urlparse(url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            errors.append(f"Invalid source URL for {row.get('source_id')}: {url}")

    with claim_path.open(encoding="utf-8", newline="") as handle:
        claims = list(csv.DictReader(handle))
    claim_ids = [row["claim_id"] for row in claims]
    if len(claim_ids) != len(set(claim_ids)):
        errors.append("Claim IDs are not unique.")

    for row in claims:
        for source_id in filter(None, (part.strip() for part in row.get("evidence_ids", "").split(","))):
            if source_id not in source_set:
                errors.append(
                    f"Claim {row.get('claim_id')} references missing source {source_id}."
                )

    required = [
        PACK / "install" / "AGENTS.md",
        PACK / "install" / ".agents" / "skills" / "vadimohka-site-upgrade" / "SKILL.md",
        PACK / "MASTER_PROMPT.md",
        PACK / "manifest" / "release-gates.md",
        PACK / "evidence" / "claim-policy.md",
        PACK / "copy" / "homepage-v1.md",
    ]
    for path in required:
        if not path.is_file():
            errors.append(f"Missing required file: {path}")

    owner_local = list(ROOT.rglob("owner-input.local.yaml"))
    if owner_local:
        errors.append(
            "A private owner-input.local.yaml exists in the overlay. It must not be distributed."
        )

    if errors:
        for message in errors:
            fail(message)
        print(f"Pack validation failed with {len(errors)} error(s).", file=sys.stderr)
        return 1

    brand_count = sum(1 for task in tasks if task["phase"] == "Brand")
    technical_count = sum(1 for task in tasks if task["phase"] == "Technical")
    print(
        f"Pack valid: {len(tasks)} tasks "
        f"({brand_count} brand, {technical_count} technical), "
        f"{len(claims)} claims, {len(sources)} sources."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
