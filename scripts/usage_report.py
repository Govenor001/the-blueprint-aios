#!/usr/bin/env python3
"""Summarize local activity records without pretending to know provider cost."""

from __future__ import annotations

from collections import Counter
import argparse
import json
from pathlib import Path
from typing import Iterable, Any


def usage_report(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [record for record in records if isinstance(record, dict)]
    statuses = Counter(str(row.get("status", "unknown")) for row in rows)
    models = Counter(str(row.get("model", "unknown")) for row in rows if row.get("model"))
    return {"runs": len(rows), "statuses": dict(statuses), "models": dict(models), "cost": "UNAVAILABLE unless the provider supplies billing data"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", default="var/activity.jsonl")
    args = parser.parse_args(argv)
    path = Path(args.path)
    records = []
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                value = json.loads(line)
            except json.JSONDecodeError:
                continue
            if isinstance(value, dict):
                records.append(value)
    print(json.dumps(usage_report(records), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
