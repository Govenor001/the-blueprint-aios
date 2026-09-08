#!/usr/bin/env python3
"""Make the installed skill vault available to Claude Code at runtime."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path


def sync_runtime_skills(root: Path) -> list[str]:
    """Copy vault skills into Claude's runtime directory without touching core skills."""
    root = Path(root).resolve()
    source_root = root / "skill-vault"
    runtime_root = root / ".claude" / "skills"
    runtime_root.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for source_dir in sorted(source_root.iterdir() if source_root.exists() else []):
        source_file = source_dir / "SKILL.md"
        if not source_dir.is_dir() or not source_file.is_file():
            continue
        target_file = runtime_root / source_dir.name / "SKILL.md"
        if target_file.exists():
            continue
        target_file.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source_file, target_file)
        copied.append(source_dir.name)
    return copied


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    copied = sync_runtime_skills(args.root)
    print(f"Runtime skills ready: {len(copied)} copied, existing skills preserved.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
