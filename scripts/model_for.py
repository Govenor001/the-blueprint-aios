#!/usr/bin/env python3
"""Resolve AIOS skill model tiers without hardcoding provider model names."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

import yaml


def _find_agent(payload: dict[str, Any], skill: str) -> dict[str, Any]:
    for wing in payload.get("wings", []):
        for department in wing.get("departments", []):
            for function in department.get("functions", []):
                for agent in function.get("agents", []):
                    if agent.get("name") == skill:
                        return agent
    raise KeyError(f"Unknown skill: {skill}")


def model_for(root: Path, skill: str | None = None, tier: str | None = None) -> str:
    root = Path(root).resolve()
    config = yaml.safe_load((root / "config" / "models.yaml").read_text(encoding="utf-8"))
    route = config["route"]
    selected_tier = tier or "smart"
    if skill:
        map_path = root / "dashboard" / "static" / "map.json"
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        selected_tier = _find_agent(payload, skill).get("model", "smart")
    try:
        return str(config["tiers"][route][selected_tier])
    except KeyError as exc:
        raise ValueError(f"No model configured for route={route!r}, tier={selected_tier!r}") from exc


if __name__ == "__main__":
    if len(sys.argv) not in {2, 3}:
        raise SystemExit("usage: model_for.py SKILL [ROOT]")
    root = Path(sys.argv[2]) if len(sys.argv) == 3 else Path.cwd()
    print(model_for(root, skill=sys.argv[1]))
