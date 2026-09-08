#!/usr/bin/env python3
"""Append redacted, bounded JSONL activity events."""

from __future__ import annotations

import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SECRET_PATTERNS = (
    re.compile(r"\bsk-[A-Za-z0-9_-]+"),
    re.compile(r"\bak_[A-Za-z0-9_-]+"),
    re.compile(r"\bxi-api[A-Za-z0-9_-]+"),
    re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.IGNORECASE),
)


def root_path() -> Path:
    return Path(os.environ.get("AIOS_ROOT", Path(__file__).resolve().parents[1]))


def redact(value: Any) -> Any:
    if not isinstance(value, str):
        return value
    result = value
    for pattern in SECRET_PATTERNS:
        result = pattern.sub("[redacted]", result)
    return result


def log(event: str, skill: str | None = None, detail: str | None = None, status: str = "ok", model: str | None = None) -> None:
    path = root_path() / "var" / "activity.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists() and path.stat().st_size > 10 * 1024 * 1024:
        rotated = path.with_name("activity.jsonl.1")
        if rotated.exists():
            rotated.unlink()
        path.replace(rotated)
    row = {
        "ts": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "event": redact(event),
        "skill": redact(skill),
        "model": redact(model),
        "detail": redact(detail)[:200] if isinstance(redact(detail), str) else redact(detail),
        "status": redact(status),
    }
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")
