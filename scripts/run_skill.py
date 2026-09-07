#!/usr/bin/env python3
"""Run one allow-listed skill through Claude Code."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from activity import log


def main(argv: list[str] | None = None) -> int:
    args = argv or sys.argv[1:]
    if len(args) != 1:
        print("usage: run_skill.py SKILL_NAME", file=sys.stderr)
        return 2
    root = Path(__file__).resolve().parents[1]
    map_path = root / "dashboard" / "static" / "map.json"
    if not map_path.exists():
        print("map.json is missing; run scripts/build_map.py first", file=sys.stderr)
        return 1
    data = json.loads(map_path.read_text(encoding="utf-8"))
    names = {
        agent["name"]
        for wing in data.get("wings", [])
        for department in wing.get("departments", [])
        for function in department.get("functions", [])
        for agent in function.get("agents", [])
    }
    if args[0] not in names:
        print("skill is not allow-listed", file=sys.stderr)
        return 1
    log("skill_started", skill=args[0])
    try:
        result = subprocess.run(
            ["claude", "-p", f"Use the /{args[0]} skill for the owner's request."],
            cwd=root,
            text=True,
            capture_output=True,
            timeout=300,
            check=False,
        )
        log("skill_finished", skill=args[0], detail=result.stdout[-1000:], status="ok" if result.returncode == 0 else "error")
        return result.returncode
    except Exception as exc:
        log("skill_error", skill=args[0], detail=str(exc), status="error")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
