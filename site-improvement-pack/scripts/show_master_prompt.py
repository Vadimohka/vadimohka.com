#!/usr/bin/env python3
from pathlib import Path

path = Path(__file__).resolve().parents[1] / "MASTER_PROMPT.md"
print(path.read_text(encoding="utf-8"))
