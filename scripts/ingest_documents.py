#!/usr/bin/env python3
"""Extract supported documents into vault/context without overwriting owner files."""

from __future__ import annotations

import argparse
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from xml.etree import ElementTree


def extract(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix in {".md", ".txt", ".csv"}:
        return path.read_text(encoding="utf-8", errors="replace")
    if suffix == ".pdf":
        from pypdf import PdfReader

        return "\n\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
    if suffix == ".docx":
        with zipfile.ZipFile(path) as archive:
            xml = archive.read("word/document.xml")
        root = ElementTree.fromstring(xml)
        return "\n".join(
            "".join(node.itertext()).strip()
            for node in root.iter()
            if node.tag.endswith("}p")
        )
    raise ValueError(f"unsupported file type: {path.name}")


def ingest(root: Path) -> dict[str, int]:
    root = Path(root).resolve()
    incoming = root / "vault" / "documents"
    processed = incoming / "processed"
    context = root / "vault" / "context"
    processed.mkdir(parents=True, exist_ok=True)
    context.mkdir(parents=True, exist_ok=True)
    result = {"processed": 0, "proposed": 0, "unreadable": 0}
    for path in sorted(incoming.iterdir()):
        if not path.is_file() or path.suffix.lower() not in {".md", ".txt", ".pdf", ".csv", ".docx"}:
            continue
        try:
            text = extract(path).strip()
        except Exception as exc:
            text = f"UNAVAILABLE: could not read {path.name}: {exc}"
            result["unreadable"] += 1
        if not text:
            text = f"UNAVAILABLE: {path.name} contained no readable text."
            result["unreadable"] += 1
        destination = context / f"{path.stem}.md"
        if destination.exists():
            stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
            destination = context / f"{path.stem}.{stamp}.proposed.md"
            result["proposed"] += 1
        else:
            result["processed"] += 1
        destination.write_text(f"# Source: {path.name}\n\n{text}\n", encoding="utf-8")
        shutil.move(str(path), processed / path.name)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(ingest(args.root))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
