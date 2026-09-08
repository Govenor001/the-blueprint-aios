#!/usr/bin/env python3
"""Validate every AIOS skill against the frontmatter contract."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from typing import Any

import yaml

ALLOWED_TOP_LEVEL = {
    "name",
    "description",
    "argument-hint",
    "compatibility",
    "license",
    "metadata",
    "disable-model-invocation",
    "user-invocable",
}
WINGS = {"intelligence", "content", "growth", "comms", "command", "back-office", "build"}
AUTONOMY = {"manual", "assisted", "autonomous"}
MODELS = {"fast", "smart", "deep"}
REQUIRED_METADATA = {
    "wing",
    "department",
    "function",
    "replaces",
    "the-human",
    "ladder",
    "trigger",
    "outputs",
    "kpis",
    "tools",
    "autonomy",
    "scaffolding-phase",
}


def parse_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("frontmatter must start with ---")
    try:
        end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    except StopIteration as exc:
        raise ValueError("frontmatter has no closing ---") from exc
    parsed = yaml.safe_load("\n".join(lines[1:end]))
    if not isinstance(parsed, dict):
        raise ValueError("frontmatter must be a mapping")
    return parsed


def load_tool_keys(root: Path) -> set[str]:
    registry = root / "references" / "tool-registry.md"
    if not registry.exists():
        return set()
    keys: set[str] = set()
    for line in registry.read_text(encoding="utf-8").splitlines():
        parts = [part.strip() for part in line.strip().strip("|").split("|")]
        if len(parts) >= 3 and parts[0] not in {"key", "---"} and parts[0]:
            keys.add(parts[0])
    return keys


def _nonempty(metadata: dict[str, Any], key: str, errors: list[str]) -> None:
    value = metadata.get(key)
    if value is None or value == "" or value == []:
        errors.append(f"metadata.{key}: is empty")


def validate_skill(path: Path, tool_keys: set[str] | None = None) -> list[str]:
    errors: list[str] = []
    try:
        data = parse_frontmatter(path)
    except (OSError, ValueError, yaml.YAMLError) as exc:
        return [f"frontmatter: {exc}"]

    unknown = set(data) - ALLOWED_TOP_LEVEL
    errors.extend(f"top-level key not allowed: {key}" for key in sorted(unknown))
    for key in ("name", "description", "metadata"):
        if key not in data:
            errors.append(f"{key}: missing")

    metadata = data.get("metadata")
    if not isinstance(metadata, dict):
        errors.append("metadata: must be a mapping")
        return errors

    for key in sorted(REQUIRED_METADATA):
        if key not in metadata:
            errors.append(f"metadata.{key}: missing")
        else:
            _nonempty(metadata, key, errors)

    ladder = metadata.get("ladder")
    if isinstance(ladder, dict):
        if set(ladder) != AUTONOMY:
            errors.append("metadata.ladder: must contain exactly manual, assisted, autonomous")
    else:
        errors.append("metadata.ladder: must be a mapping")

    if metadata.get("wing") not in WINGS:
        errors.append(f"metadata.wing: invalid value {metadata.get('wing')!r}")
    if metadata.get("autonomy") not in AUTONOMY:
        errors.append(f"metadata.autonomy: invalid value {metadata.get('autonomy')!r}")
    if metadata.get("model", "smart") not in MODELS:
        errors.append(f"metadata.model: invalid value {metadata.get('model')!r}")

    for list_key in ("outputs", "kpis", "tools"):
        if not isinstance(metadata.get(list_key), list):
            errors.append(f"metadata.{list_key}: must be a list")
    if metadata.get("requires-context") is not None and not isinstance(metadata["requires-context"], list):
        errors.append("metadata.requires-context: must be a list")

    if isinstance(metadata.get("tools"), list) and tool_keys is not None:
        for tool in metadata["tools"]:
            if tool not in tool_keys:
                errors.append(f"metadata.tools: unknown tool {tool!r}")

    if "name" in data and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", str(data["name"])):
        errors.append("name: must use lowercase letters, numbers, and hyphens")
    return errors


def iter_skill_files(root: Path) -> list[Path]:
    return sorted((root / "skill-vault").rglob("SKILL.md"))


def validate_all(root: Path) -> dict[Path, list[str]]:
    tool_keys = load_tool_keys(root)
    return {path: validate_skill(path, tool_keys) for path in iter_skill_files(root)}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=None)
    args = parser.parse_args(argv)
    root = (args.root or Path.cwd()).resolve()
    results = validate_all(root)
    failed = False
    for path, errors in results.items():
        name = path.parent.name
        if errors:
            failed = True
            for error in errors:
                print(f"{name}: {error}")
        else:
            print(f"{name}: PASS")
    if not results:
        print("No skills found under skill-vault/")
        return 1
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
