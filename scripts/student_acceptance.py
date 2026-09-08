#!/usr/bin/env python3
"""Static acceptance checks for the student-facing seven-day setup."""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any


def validate_curriculum_links(root: Path) -> list[str]:
    root = Path(root).resolve()
    errors: list[str] = []
    curriculum = root / "curriculum"
    for day in range(8):
        path = curriculum / "days" / f"day-{day}.md"
        if not path.exists():
            errors.append(f"missing curriculum day: {path.name}")
    for path in sorted(curriculum.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(r"\]\(([^)]+)\)", text):
            target = match.group(1).split("#", 1)[0]
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            target_path = (path.parent / target).resolve()
            if not target_path.exists():
                errors.append(f"broken link in {path.name}: {target}")
    return errors


def run_acceptance(root: Path) -> dict[str, Any]:
    root = Path(root).resolve()
    curriculum_text = "\n".join(path.read_text(encoding="utf-8") for path in (root / "curriculum").rglob("*.md"))
    checks = {
        "curriculum_days": not validate_curriculum_links(root),
        "dashboard": (root / "dashboard" / "static" / "index.html").exists(),
        "map_builder": (root / "scripts" / "build_map.py").exists(),
        "all_panels": len(list((root / "config" / "panels").glob("*.yaml"))) == 7,
        "core_roles": all((root / "skill-vault" / name / "SKILL.md").exists() for name in ("scout", "operator", "advisor")),
        "no_platform_install_on_days": not bool(re.search(r"cp -r skill-vault|git clone|install an agent", curriculum_text, re.I)),
        "no_laptop_first_flow": not bool(re.search(r"your laptop|on your machine|your terminal", curriculum_text, re.I)),
        "no_anthropic_api_key_in_curriculum": "ANTHROPIC_API_KEY" not in curriculum_text,
        "systemd_schedules": len(list((root / "deploy" / "timers").glob("*.timer"))) >= 5,
    }
    return {"passed": all(checks.values()), "checks": checks, "link_errors": validate_curriculum_links(root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    result = run_acceptance(args.root)
    print(json.dumps(result, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
