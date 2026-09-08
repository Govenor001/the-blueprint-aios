#!/usr/bin/env python3
"""Index vault passages with optional local embeddings."""

from __future__ import annotations

import argparse
import json
import re
from datetime import datetime, timezone
from pathlib import Path

from local_model import embed


def passages(path: Path, words: int = 240) -> list[dict]:
    text = path.read_text(encoding="utf-8", errors="replace")
    tokens = text.split()
    rows = []
    for offset in range(0, len(tokens), words):
        chunk = " ".join(tokens[offset:offset + words]).strip()
        if chunk:
            rows.append({"file": str(path), "offset": offset, "passage": chunk})
    return rows


def index_vault(root: Path) -> int:
    root = Path(root).resolve()
    source_dirs = [root / "vault" / "documents" / "processed", root / "vault" / "context"]
    rows = []
    for directory in source_dirs:
        if directory.exists():
            rows.extend(passages(path) for path in sorted(directory.rglob("*")) if path.is_file() and path.suffix.lower() in {".md", ".txt", ".csv"})
    flat = [row for group in rows for row in group]
    vectors = embed([row["passage"] for row in flat])
    now = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    index_path = root / "vault" / "index.jsonl"
    index_path.parent.mkdir(parents=True, exist_ok=True)
    with index_path.open("a", encoding="utf-8") as handle:
        for index, row in enumerate(flat):
            row = dict(row)
            row["indexed_at"] = now
            row["vector"] = vectors[index] if vectors is not None and index < len(vectors) else None
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    return len(flat)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(index_vault(args.root))
