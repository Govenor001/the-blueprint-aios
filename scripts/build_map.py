#!/usr/bin/env python3
"""Build deterministic Mission Control map data from validated skill frontmatter."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

try:
    from .validate_skills import iter_skill_files, load_tool_keys, parse_frontmatter, validate_skill
except ImportError:  # direct script execution
    from validate_skills import iter_skill_files, load_tool_keys, parse_frontmatter, validate_skill

WING_ORDER = ["intelligence", "content", "growth", "comms", "command", "back-office", "build"]


def load_tools(root: Path) -> dict[str, dict[str, str]]:
    registry = root / "references" / "tool-registry.md"
    tools: dict[str, dict[str, str]] = {}
    if not registry.exists():
        return tools
    for line in registry.read_text(encoding="utf-8").splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 3 and parts[0] not in {"key", "---"} and parts[0]:
            tools[parts[0]] = {"name": parts[1], "hex": parts[2]}
    return tools


def _skill_record(root: Path, path: Path, tool_keys: set[str]) -> tuple[str, str, str, dict[str, Any]]:
    data = parse_frontmatter(path)
    metadata = data["metadata"]
    errors = validate_skill(path, tool_keys)
    if errors:
        raise ValueError(f"{path}: " + "; ".join(errors))
    record = {
        "name": str(data["name"]),
        "description": str(data["description"]),
        "path": path.relative_to(root).as_posix(),
        "replaces": metadata["replaces"],
        "the-human": metadata["the-human"],
        "ladder": metadata["ladder"],
        "trigger": metadata["trigger"],
        "outputs": metadata["outputs"],
        "kpis": metadata["kpis"],
        "tools": metadata["tools"],
        "autonomy": metadata["autonomy"],
        "model": metadata.get("model", "smart"),
        "phase": metadata["scaffolding-phase"],
    }
    return metadata["wing"], metadata["department"], metadata["function"], record


def build_map(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    tool_keys = load_tool_keys(root)
    grouped: dict[str, dict[str, dict[str, list[dict[str, Any]]]]] = defaultdict(
        lambda: defaultdict(lambda: defaultdict(list))
    )
    records = []
    for path in iter_skill_files(root):
        wing, department, function, record = _skill_record(root, path, tool_keys)
        grouped[wing][department][function].append(record)
        records.append(record)

    wings = []
    for wing in WING_ORDER:
        if wing not in grouped:
            continue
        departments = []
        for department in sorted(grouped[wing], key=str.casefold):
            functions = []
            for function in sorted(grouped[wing][department], key=str.casefold):
                agents = sorted(
                    grouped[wing][department][function],
                    key=lambda item: (int(item["phase"]), item["name"]),
                )
                functions.append({"function": function, "agents": agents})
            departments.append({"department": department, "functions": functions})
        wings.append({"wing": wing, "departments": departments})

    autonomy = Counter(record["autonomy"] for record in records)
    result = {
        "generated": datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "counts": {
            "total": len(records),
            "manual": autonomy["manual"],
            "assisted": autonomy["assisted"],
            "autonomous": autonomy["autonomous"],
        },
        "tools": load_tools(root),
        "wings": wings,
    }
    output = root / "dashboard" / "static" / "map.json"
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return result


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    try:
        result = build_map(args.root)
    except (OSError, ValueError, KeyError) as exc:
        print(f"build-map: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result["counts"], sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
