#!/usr/bin/env python3
"""Collect panel cards without making the dashboard call external APIs."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


def _card_id(panel: str, card: dict[str, Any]) -> str:
    value = card.get("id") or f"{panel}-{card.get('title', 'card')}"
    return re.sub(r"[^a-z0-9-]+", "-", str(value).lower()).strip("-")


def collect(root: Path) -> int:
    root = Path(root).resolve()
    panels = root / "config" / "panels"
    metric_dir = root / "var" / "metrics"
    metric_dir.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(panels.glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for card in payload.get("cards", []):
            card_id = _card_id(path.stem, card)
            now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
            source = card.get("source", {})
            row: dict[str, Any] = {"retrieved_at": now, "card_id": card_id, "source": source, "status": "unavailable"}
            if isinstance(source, dict) and "local" in source:
                local = root / str(source["local"])
                row["status"] = "available" if local.exists() else "unavailable"
                row["value"] = len(list(local.glob("*"))) if local.exists() else None
            else:
                row["error"] = "connection not configured"
            with (metric_dir / f"{card_id}.jsonl").open("a", encoding="utf-8") as handle:
                handle.write(json.dumps(row, ensure_ascii=False) + "\n")
            count += 1
    return count


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(collect(args.root))
