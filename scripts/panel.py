#!/usr/bin/env python3
"""Pure helpers for rendering fixture-backed Mission Control payloads."""

from __future__ import annotations

from typing import Any


def render_panel(panel: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    cards = []
    for card in panel.get("cards", []):
        card_id = str(card.get("id") or card.get("title", "card"))
        latest = metrics.get(card_id)
        cards.append({"id": card_id, "title": card.get("title", card_id), "shape": card.get("shape", "table"), "latest": latest, "empty_state": latest is None or latest.get("status") != "available" if isinstance(latest, dict) else latest is None})
    return {"name": panel.get("name", "panel"), "cards": cards}


def build_mission_control(scout: dict[str, Any], operator: dict[str, Any], advisor: dict[str, Any], metrics: dict[str, Any]) -> dict[str, Any]:
    return {"roles": {"scout": scout, "operator": operator, "advisor": advisor}, "metrics": metrics}
