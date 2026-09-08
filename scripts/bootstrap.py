#!/usr/bin/env python3
"""Prepare the AIOS filesystem without handling or printing secrets."""

from __future__ import annotations

import argparse
import os
import stat
import sys
from pathlib import Path

REQUIRED_DIRS = [
    "context",
    "vault/documents",
    "vault/context",
    "var",
    "config",
]


def check_environment() -> list[str]:
    problems = []
    if os.environ.get("ANTHROPIC_API_KEY"):
        problems.append("ANTHROPIC_API_KEY is set; AIOS requires subscription or Bedrock auth")
    return problems


def bootstrap(root: Path) -> None:
    root = Path(root).resolve()
    for relative in REQUIRED_DIRS:
        (root / relative).mkdir(parents=True, exist_ok=True)
    env_file = root / ".env"
    if env_file.exists():
        env_file.chmod(stat.S_IRUSR | stat.S_IWUSR)
    (root / "var" / "activity.jsonl").touch(exist_ok=True)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    problems = check_environment()
    if problems:
        for problem in problems:
            print(problem, file=sys.stderr)
        return 1
    bootstrap(args.root)
    print("AIOS filesystem ready.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
