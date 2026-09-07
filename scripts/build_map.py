#!/usr/bin/env python3
"""Build the static Mission Control skill map from validated frontmatter."""

from __future__ import annotations

import argparse
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from validate_skills import iter_skill_files, load_tool_keys, parse_frontmatter, validate_skill


def _skill_record(root: Path, path: Path, tool_keys: set[str]) -> dict[str, Any]:
    data = parse_frontmatter(path)
    metadata = data["metadata"]
    errors = validate_skill(path, tool_keys)
    if errors:
        raise ValueError(f"{path}: " + "; ".join(errors))
    relative = path.relative_to(root).as_posix()
    return {
        "name": str(data["name"]),
        "description": str(data["description"]),
        "path": relative,
        "metadata": metadata,
    }


def build_map(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    tool_keys = load_tool_keys(root)
    records = [_skill_record(root, path, tool_keys) for path in iter_skill_files(root)]
    records.sort(key=lambda item: (item["metadata"]["wing"], item["metadata"]["department"].lower(), item["name"]))

    grouped: dict[str, dict[str, list[dict[str, Any]]]] = defaultdict(lambda: defaultdict(list))
    for record in records:
        metadata = record["metadata"]
        grouped[metadata["wing"]][metadata["department"]].append(record)

    wings = []
    for wing in sorted(grouped):
        departments = []
        for department in sorted(grouped[wing]):
            agents = sorted(grouped[wing][department], key=lambda item: item["name"])
            departments.append({"department": department, "agents": agents})
        wings.append({"wing": wing, "departments": departments})

    autonomy = Counter(record["metadata"]["autonomy"] for record in records)
    models = Counter(record["metadata"].get("model", "smart") for record in records)
    result = {
        "version": 1,
        "generated_at": None,
        "counts": {
            "total": len(records),
            "manual": autonomy["manual"],
            "assisted": autonomy["assisted"],
            "autonomous": autonomy["autonomous"],
            "fast": models["fast"],
            "smart": models["smart"],
            "deep": models["deep"],
        },
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
