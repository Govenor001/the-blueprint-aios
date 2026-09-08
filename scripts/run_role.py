#!/usr/bin/env python3
"""Deterministic Scout, Operator, and Advisor orchestration helpers."""

from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


def _now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_scout(inputs: dict[str, Any]) -> dict[str, Any]:
    """Normalize sourced observations without advice or invented values."""
    observations: list[dict[str, Any]] = []
    for item in inputs.get("sources", []) if isinstance(inputs, dict) else []:
        if not isinstance(item, dict):
            continue
        source = str(item.get("source") or "UNAVAILABLE")
        timestamp = str(item.get("retrieved_at") or item.get("timestamp") or "UNAVAILABLE")
        value = item.get("value")
        status = str(item.get("status") or ("available" if source != "UNAVAILABLE" else "unavailable"))
        observations.append({"source": source, "retrieved_at": timestamp, "status": status, "value": value})
    return {"role": "scout", "generated_at": _now(), "status": "available" if observations else "unavailable", "observations": observations}


def run_operator(request: dict[str, Any], context: dict[str, Any]) -> dict[str, Any]:
    """Prepare a draft and stop before consequential actions."""
    request = request if isinstance(request, dict) else {}
    text = str(request.get("request") or request.get("text") or "").strip()
    faq = context.get("faq") if isinstance(context, dict) else None
    risky_words = ("send", "publish", "spend", "pay", "delete", "refund", "legal", "password")
    approval_required = any(word in text.lower() for word in risky_words)
    if not text:
        return {"role": "operator", "generated_at": _now(), "status": "needs_input", "draft": None, "approval_required": False}
    return {"role": "operator", "generated_at": _now(), "status": "draft", "draft": text, "approval_required": approval_required or not bool(faq), "required_approval_for": ["send", "spend", "publish", "delete", "external_write"], "context_note": "FAQ context loaded." if faq else "FAQ context unavailable; owner review required."}


def run_advisor(scout: dict[str, Any], operator: dict[str, Any]) -> dict[str, Any]:
    """Return exactly three ranked, evidence-backed options."""
    evidence = [row for row in scout.get("observations", []) if row.get("status") == "available"] if isinstance(scout, dict) else []
    evidence_text = f"{evidence[0].get('source')} at {evidence[0].get('retrieved_at')}" if evidence else "UNAVAILABLE: connect a source before acting."
    draft_state = operator.get("status", "unavailable") if isinstance(operator, dict) else "unavailable"
    labels = ["Resolve the highest-confidence signal", "Review the next owner decision", "Keep the system bounded"]
    recommendations = [{"rank": index, "recommendation": label, "evidence": evidence_text, "consequence_of_waiting": "The decision remains unverified." if not evidence else f"The {draft_state} work remains pending owner review."} for index, label in enumerate(labels, 1)]
    return {"role": "advisor", "generated_at": _now(), "status": "available", "recommendations": recommendations}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("role", choices=("scout", "operator", "advisor"))
    parser.add_argument("input", type=Path, help="JSON fixture input")
    args = parser.parse_args(argv)
    payload = json.loads(args.input.read_text(encoding="utf-8"))
    if args.role == "scout":
        result = run_scout(payload)
    elif args.role == "operator":
        result = run_operator(payload.get("request", {}), payload.get("context", {}))
    else:
        result = run_advisor(payload.get("scout", {}), payload.get("operator", {}))
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
