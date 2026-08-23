#!/usr/bin/env python3
"""Optional online source-link checker. Not part of the offline baseline."""

from __future__ import annotations

import csv
import ssl
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
REGISTER = PACK / "evidence" / "source-register.csv"

USER_AGENT = (
    "Mozilla/5.0 (compatible; vadimohka-site-source-check/1.0; "
    "+https://vadimohka.com/)"
)


def main() -> int:
    with REGISTER.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    failures = 0
    context = ssl.create_default_context()
    for row in rows:
        source_id = row["source_id"]
        url = row["url"]
        request = urllib.request.Request(
            url,
            headers={"User-Agent": USER_AGENT, "Accept": "text/html,*/*;q=0.8"},
            method="GET",
        )
        try:
            with urllib.request.urlopen(request, timeout=20, context=context) as response:
                status = response.status
                final_url = response.geturl()
                ok = 200 <= status < 400
                print(f"{source_id}\t{status}\t{'OK' if ok else 'FAIL'}\t{final_url}")
                failures += 0 if ok else 1
        except (urllib.error.URLError, TimeoutError, ValueError) as exc:
            failures += 1
            print(f"{source_id}\tERROR\tFAIL\t{exc}")
        time.sleep(0.25)

    if failures:
        print(f"{failures} source(s) failed or were inaccessible.", file=sys.stderr)
        return 1
    print("All sources returned a successful HTTP status.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
