#!/usr/bin/env python3
"""Validate the non-secret environment before services are started."""

from __future__ import annotations

import argparse
import os
from pathlib import Path
from typing import Mapping, Any

import yaml


def load_route(root: Path) -> dict[str, Any]:
    path = Path(root) / "config" / "route.yaml"
    if not path.exists():
        path = Path(root) / "config" / "models.yaml"
    return yaml.safe_load(path.read_text(encoding="utf-8")) or {}


def validate_environment(route: dict[str, Any], environ: Mapping[str, str]) -> list[str]:
    problems: list[str] = []
    if environ.get("ANTHROPIC_API_KEY"):
        problems.append("ANTHROPIC_API_KEY is forbidden; use Claude subscription or Bedrock auth")
    if not environ.get("DASHBOARD_PASSWORD"):
        problems.append("DASHBOARD_PASSWORD is required")
    selected = environ.get("AIOS_MODEL_ROUTE") or route.get("route")
    allowed = set(route.get("allowed_routes", [])) or set((route.get("tiers") or {}).keys())
    if selected not in allowed:
        problems.append(f"unsupported AIOS_MODEL_ROUTE: {selected}")
    if selected == "bedrock" and not environ.get("AWS_REGION"):
        problems.append("AWS_REGION is required for the Bedrock route")
    return problems


def bootstrap_install(root: Path) -> None:
    try:
        from .bootstrap import bootstrap
    except ImportError:
        from bootstrap import bootstrap
    bootstrap(Path(root))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    problems = validate_environment(load_route(args.root), os.environ)
    for problem in problems:
        print(problem)
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
