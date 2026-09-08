#!/usr/bin/env python3
"""Install and normalize the curated Business OS skill set."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml

try:
    from .validate_skills import ALLOWED_TOP_LEVEL, parse_frontmatter
except ImportError:  # direct script execution
    from validate_skills import ALLOWED_TOP_LEVEL, parse_frontmatter

DEFAULT_MANIFEST = Path(__file__).resolve().parents[1] / "business-os-150" / "skills-manifest.json"
CATEGORY_WINGS = {
    "business-growth": "growth",
    "c-level": "command",
    "engineering": "build",
    "finance": "back-office",
    "legal": "back-office",
    "marketing": "content",
    "product": "build",
    "project-management": "command",
}


def load_manifest(path: Path = DEFAULT_MANIFEST) -> dict[str, Any]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    skills = payload.get("skills")
    if payload.get("skill_count") != 150 or not isinstance(skills, list) or len(skills) != 150:
        raise ValueError("Business OS manifest must declare exactly 150 skills")
    names = [item.get("name") for item in skills]
    paths = [item.get("path") for item in skills]
    if len(set(names)) != 150 or len(set(paths)) != 150:
        raise ValueError("Business OS manifest contains duplicate names or paths")
    for item in skills:
        if item.get("repo") != "borghei/Claude-Skills" or not item.get("category"):
            raise ValueError(f"Invalid manifest entry: {item!r}")
    return payload


def install_command(manifest: dict[str, Any], app: str = "claude-code") -> list[str]:
    command = ["npx", "skills", "add", "borghei/Claude-Skills"]
    for item in manifest["skills"]:
        command.extend(["--skill", item["name"]])
    command.extend(["-a", app, "-y"])
    return command


def _frontmatter_text(data: dict[str, Any], body: str) -> str:
    clean = {key: data[key] for key in data if key in ALLOWED_TOP_LEVEL}
    return "---\n" + yaml.safe_dump(clean, sort_keys=False, allow_unicode=True).strip() + "\n---\n\n" + body.lstrip()


def normalize_skill(source: Path, target: Path, category: str) -> None:
    source_text = source.read_text(encoding="utf-8")
    data = parse_frontmatter(source)
    name = str(data.get("name") or source.parent.name)
    description = str(data.get("description") or f"Business OS skill: {name.replace('-', ' ')}.")
    metadata = data.get("metadata") if isinstance(data.get("metadata"), dict) else {}
    metadata = dict(metadata)
    metadata.setdefault("wing", CATEGORY_WINGS.get(category, "build"))
    metadata.setdefault("department", category.replace("-", " ").title())
    metadata.setdefault("function", name.replace("-", " ").title())
    metadata.setdefault("replaces", f"Manual {name.replace('-', ' ')} work.")
    metadata.setdefault("the-human", "The owner approves consequential actions.")
    metadata.setdefault("ladder", {
        "manual": "Run only when the owner asks.",
        "assisted": "Prepare work for owner review.",
        "autonomous": "Run on a schedule after approval.",
    })
    metadata.setdefault("trigger", f"Use when {name.replace('-', ' ')} is needed.")
    metadata.setdefault("outputs", ["A structured result"])
    metadata.setdefault("kpis", ["Useful output delivered"])
    metadata.setdefault("tools", ["claude"])
    metadata.setdefault("model", "smart")
    metadata.setdefault("autonomy", "assisted")
    metadata.setdefault("scaffolding-phase", 3)
    data["name"] = name
    data["description"] = description
    data["metadata"] = metadata
    lines = source_text.splitlines()
    end = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    body = "\n".join(lines[end + 1:]) if end is not None else source_text
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(_frontmatter_text(data, body), encoding="utf-8")


def sync_installed_skills(root: Path, manifest: dict[str, Any]) -> int:
    root = root.resolve()
    source_roots = [
        root / ".claude" / "skills",
        root / ".agents" / "skills",
    ]
    imported = 0
    by_name = {item["name"]: item for item in manifest["skills"]}
    for name, item in by_name.items():
        source = next((candidate / name / "SKILL.md" for candidate in source_roots if (candidate / name / "SKILL.md").exists()), None)
        if source is None:
            continue
        target_dir = root / "skill-vault" / name
        if target_dir.exists():
            shutil.rmtree(target_dir)
        shutil.copytree(source.parent, target_dir)
        normalize_skill(target_dir / "SKILL.md", target_dir / "SKILL.md", item["category"])
        imported += 1
    return imported


def run_install(manifest: dict[str, Any], root: Path, app: str = "claude-code", dry_run: bool = False) -> int:
    command = install_command(manifest, app)
    print(" ".join(command))
    if not dry_run:
        subprocess.run(command, cwd=root, check=True)
    return sync_installed_skills(root, manifest) if not dry_run else 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument("--app", default="claude-code")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args(argv)
    try:
        manifest = load_manifest(args.manifest)
        imported = run_install(manifest, args.root, args.app, args.dry_run)
    except (OSError, ValueError, subprocess.CalledProcessError, yaml.YAMLError) as exc:
        print(f"business-os: {exc}", file=sys.stderr)
        return 1
    if not args.dry_run:
        print(f"Imported and normalized {imported} installed skills.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
