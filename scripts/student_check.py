#!/usr/bin/env python3
"""Check that a student setup is ready for the seven-day challenge."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path

try:
    from scripts.install_business_os import load_manifest
except ModuleNotFoundError:  # direct `python scripts/student_check.py` execution
    from install_business_os import load_manifest


WINGS = {"intelligence", "content", "growth", "comms", "command", "back-office", "build"}


def _password_present(root: Path) -> bool:
    if os.environ.get("DASHBOARD_PASSWORD"):
        return True
    for env_file in (root / ".env", root.parent / ".env"):
        if env_file.exists() and any(line.startswith("DASHBOARD_PASSWORD=") and line.split("=", 1)[1].strip() for line in env_file.read_text(encoding="utf-8").splitlines()):
            return True
    return False


def check(root: Path) -> dict:
    root = Path(root).resolve()
    map_path = root / "dashboard" / "static" / "map.json"
    try:
        map_payload = json.loads(map_path.read_text(encoding="utf-8"))
        seven_wings = {item.get("wing") for item in map_payload.get("wings", [])} == WINGS
    except (OSError, json.JSONDecodeError, AttributeError):
        seven_wings = False
    try:
        business_os_manifest = load_manifest(root / "business-os-150" / "skills-manifest.json")["skill_count"] == 150
    except (OSError, ValueError, json.JSONDecodeError):
        business_os_manifest = False
    checks = {
        "models_config": (root / "config" / "models.yaml").exists(),
        "core_roles": (root / "config" / "core-roles.yaml").exists(),
        "dashboard": (root / "dashboard" / "static" / "index.html").exists(),
        "map": (root / "dashboard" / "static" / "map.json").exists(),
        "seven_wings": seven_wings,
        "diagram_builder": (root / "scripts" / "build_diagrams.py").exists() and (root / "vendor" / "archify" / "bin" / "archify.mjs").exists(),
        "panel_definitions": len(list((root / "config" / "panels").glob("*.yaml"))) == 7,
        "metric_collector": (root / "scripts" / "collect.py").exists() and (root / "deploy" / "timers" / "aios-collect.timer").exists(),
        "activity_log": (root / "var" / "activity.jsonl").exists(),
        "business_os_manifest": business_os_manifest,
        "dashboard_password": _password_present(root),
        "no_anthropic_api_key": not bool(os.environ.get("ANTHROPIC_API_KEY")),
    }
    return {"passed": all(checks.values()), "checks": checks}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    result = check(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
