#!/usr/bin/env python3
"""Summarize local activity records without pretending to know provider cost."""

from __future__ import annotations

from collections import Counter
from typing import Iterable, Any


def usage_report(records: Iterable[dict[str, Any]]) -> dict[str, Any]:
    rows = [record for record in records if isinstance(record, dict)]
    statuses = Counter(str(row.get("status", "unknown")) for row in rows)
    models = Counter(str(row.get("model", "unknown")) for row in rows if row.get("model"))
    return {"runs": len(rows), "statuses": dict(statuses), "models": dict(models), "cost": "UNAVAILABLE unless the provider supplies billing data"}
