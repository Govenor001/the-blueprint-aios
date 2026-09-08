#!/usr/bin/env python3
"""Stable entry point for document ingestion."""

try:
    from .ingest_documents import ingest
except ImportError:
    from ingest_documents import ingest

__all__ = ["ingest"]


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args()
    print(ingest(args.root))
