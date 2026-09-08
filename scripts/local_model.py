#!/usr/bin/env python3
"""Optional Tier 1 local model adapter.

The adapter is deliberately optional: when AIOS_LOCAL_MODEL_URL is unset or the
endpoint is unavailable, callers receive None and can use keyword matching.
"""

from __future__ import annotations

import json
import os
import urllib.request
from typing import Any


def _post(path: str, payload: dict[str, Any]) -> Any:
    base = os.environ.get("AIOS_LOCAL_MODEL_URL", "").rstrip("/")
    if not base:
        return None
    url = base + "/" + path.lstrip("/")
    request = urllib.request.Request(
        url,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except Exception:
        return None


def embed(texts: list[str]) -> list[list[float]] | None:
    """Return embeddings from the optional local endpoint, or None."""
    if not texts:
        return []
    result = _post("/embed", {"texts": texts})
    if isinstance(result, dict):
        result = result.get("embeddings")
    if not isinstance(result, list) or not all(isinstance(row, list) for row in result):
        return None
    return result


def classify(text: str, labels: list[str]) -> str | None:
    """Return one local classification label, or None when unavailable."""
    if not labels:
        return None
    result = _post("/classify", {"text": text, "labels": labels})
    if isinstance(result, dict):
        result = result.get("label")
    return result if result in labels else None
