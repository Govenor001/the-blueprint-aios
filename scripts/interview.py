#!/usr/bin/env python3
"""Small, file-backed interview helper for Day 1 context setup."""

from __future__ import annotations

from pathlib import Path
from typing import Mapping


QUESTIONS = ("business_name", "offer", "customer", "voice", "priority", "boundary", "aios_name")


def save_interview(root: Path, answers: Mapping[str, str]) -> Path:
    root = Path(root).resolve()
    output = root / "context" / "interview.md"
    output.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Owner interview", ""]
    for key in QUESTIONS:
        lines.extend([f"## {key.replace('_', ' ').title()}", str(answers.get(key, "UNAVAILABLE")), ""])
    output.write_text("\n".join(lines), encoding="utf-8")
    return output
