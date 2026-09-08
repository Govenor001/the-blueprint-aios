#!/usr/bin/env python3
"""Search the private vault without invoking Claude."""

from __future__ import annotations

import argparse
import json
import math
import re
from pathlib import Path

from local_model import embed


def _cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right))
    norm_left = math.sqrt(sum(a * a for a in left))
    norm_right = math.sqrt(sum(b * b for b in right))
    return dot / (norm_left * norm_right) if norm_left and norm_right else 0.0


def search(root: Path, query: str, limit: int = 5) -> list[dict]:
    path = Path(root).resolve() / "vault" / "index.jsonl"
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8").splitlines():
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        row["score"] = 0.0
        rows.append(row)
    query_vector = embed([query])
    if query_vector and query_vector[0]:
        for row in rows:
            if row.get("vector"):
                row["score"] = _cosine(query_vector[0], row["vector"])
    else:
        words = set(re.findall(r"[a-z0-9]+", query.lower()))
        for row in rows:
            haystack = row.get("passage", "").lower()
            row["score"] = sum(haystack.count(word) for word in words)
    return sorted(rows, key=lambda row: row["score"], reverse=True)[:limit]


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--root", type=Path, default=Path.cwd())
    parser.add_argument("--limit", type=int, default=5)
    args = parser.parse_args()
    print(json.dumps(search(args.root, args.query, args.limit), ensure_ascii=False, indent=2))
