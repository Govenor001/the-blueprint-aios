"""Answer metric questions from append-only local history only."""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import yaml

try:
    from .chart import render
except ImportError:  # direct script execution through the Telegram bridge
    from chart import render


def answer(root: Path, question: str) -> dict[str, Any]:
    root = Path(root).resolve()
    words = set(re.findall(r"[a-z0-9]+", question.lower()))
    candidates: list[tuple[int, str, dict[str, Any]]] = []
    for path in sorted((root / "config" / "panels").glob("*.yaml")):
        payload = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for card in payload.get("cards", []):
            card_id = str(card.get("id") or card.get("title", "card")).lower().replace(" ", "-")
            searchable = set(re.findall(r"[a-z0-9]+", f"{path.stem} {card_id} {card.get('title', '')}".lower()))
            score = len(words & searchable)
            if score:
                candidates.append((score, card_id, card))
    if not candidates:
        return {"message": "I do not have a collected card that answers that question yet. Connect the relevant service and run the collector first.", "chart_url": None}
    _, card_id, card = max(candidates, key=lambda item: item[0])
    metric = root / "var" / "metrics" / f"{card_id}.jsonl"
    rows: list[dict[str, Any]] = []
    if metric.exists():
        for line in metric.read_text(encoding="utf-8").splitlines()[-30:]:
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            if row.get("status") == "available":
                rows.append(row)
    if not rows:
        source = card.get("source", {})
        connection = source.get("connection") if isinstance(source, dict) else None
        suffix = f" Connect {connection} and run the collector." if connection else " Run the collector after adding the source."
        return {"message": f"{card.get('title', card_id)} is not connected yet.{suffix}", "chart_url": None, "card_id": card_id}
    latest = rows[-1]
    shape = card.get("shape", "table")
    spec: dict[str, Any] = {"shape": shape, "title": card.get("title", card_id), "source": latest.get("source_label", "UNAVAILABLE"), "collected_at": latest.get("retrieved_at", "UNAVAILABLE")}
    values = [(row.get("retrieved_at", ""), row.get("value")) for row in rows if isinstance(row.get("value"), (int, float))]
    if shape in {"line", "bar"}:
        spec["series"] = [{"label": card.get("title", card_id), "points": values}]
    elif shape == "table":
        spec["rows"] = [row.get("value") for row in rows[-7:]]
    elif shape == "donut":
        spec["value"] = latest.get("value", 0) if isinstance(latest.get("value", 0), (int, float)) else 0
    else:
        spec["value"] = latest.get("value", "UNAVAILABLE")
    return {"message": f"{card.get('title', card_id)} has {len(rows)} collected reading(s), latest from {latest.get('source_label', 'UNAVAILABLE')} at {latest.get('retrieved_at', 'UNAVAILABLE')}.", "chart_url": f"/api/chart/{card_id}", "card_id": card_id, "svg": render(spec)}
