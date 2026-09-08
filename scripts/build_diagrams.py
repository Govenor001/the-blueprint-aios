#!/usr/bin/env python3
"""Build static AIOS structure diagrams without making page-load network calls."""

from __future__ import annotations

import argparse
import html
import json
import shutil
import subprocess
from pathlib import Path
from typing import Any


WING_COLORS = {
    "intelligence": "#bff4d6",
    "content": "#cceafb",
    "growth": "#e5dcff",
    "comms": "#fff1b8",
    "back-office": "#ffd7c8",
    "command": "#d9f0e8",
    "build": "#dce7ff",
}


def _architecture_spec(payload: dict[str, Any]) -> dict[str, Any]:
    wings = payload.get("wings", [])
    components = [
        {
            "id": "second-brain",
            "type": "backend",
            "label": "Second Brain",
            "sublabel": "Mission Control",
            "pos": [520, 330],
            "size": [180, 76],
        }
    ]
    connections = []
    positions = [(60, 80), (350, 80), (640, 80), (930, 80), (205, 560), (495, 560), (785, 560)]
    for index, wing in enumerate(wings[:7]):
        name = str(wing.get("wing", f"wing-{index}"))
        component_id = f"wing-{index}"
        x, y = positions[index]
        components.append({
            "id": component_id,
            "type": "backend",
            "label": name.replace("-", " ").title(),
            "sublabel": f"{len(wing.get('departments', []))} departments",
            "pos": [x, y],
            "size": [180, 76],
            "tag": "manual / assisted",
        })
        if y < 330:
            connections.append({
                "id": f"brain-to-{component_id}",
                "from": "second-brain",
                "to": component_id,
                "fromSide": "top",
                "toSide": "bottom",
                "via": [[610, 280], [x + 90, 280]],
            })
        else:
            connections.append({
                "id": f"brain-to-{component_id}",
                "from": "second-brain",
                "to": component_id,
                "fromSide": "bottom",
                "toSide": "top",
                "via": [[610, 480], [x + 90, 480]],
            })
    return {
        "schema_version": 1,
        "diagram_type": "architecture",
        "meta": {
            "title": "AIOS Second Brain",
            "quality_profile": "showcase",
            "views": [{"id": "all-wings", "label": "All seven wings", "focus": [component["id"] for component in components]}],
        },
        "components": components,
        "connections": connections,
        "cards": [{"dot": "cyan", "title": "Safety", "items": ["Every agent has a human handoff", "Source and freshness are shown"]}],
    }


def _fallback_html(spec: dict[str, Any]) -> str:
    nodes = []
    for component in spec["components"]:
        label = html.escape(component["label"])
        sublabel = html.escape(component.get("sublabel", ""))
        nodes.append(f'<article><b>{label}</b><small>{sublabel}</small></article>')
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><title>AIOS Second Brain</title>
<style>body{margin:0;padding:32px;background:#f6f8f8;color:#17212b;font:16px system-ui}main{max-width:1100px;margin:auto}section{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center}article{min-width:150px;padding:18px;border:1px solid #dce3e3;border-radius:16px;background:#fff;box-shadow:0 8px 20px #23333c12}b,small{display:block}small{margin-top:7px;color:#667380;font-size:12px}</style>
<main><h1>AIOS Second Brain</h1><p>Plain map fallback. Install Node and run the diagram timer for the full Archify artifact.</p><section>""" + "".join(nodes) + "</section></main></html>"


def _deliver(root: Path, spec_path: Path, output_path: Path) -> bool:
    archify = root / "vendor" / "archify" / "bin" / "archify.mjs"
    node = shutil.which("node")
    if not node or not archify.exists():
        return False
    completed = subprocess.run(
        [node, str(archify), "deliver", "architecture", str(spec_path), str(output_path), "--quality", "showcase", "--json"],
        cwd=root,
        capture_output=True,
        text=True,
        check=False,
    )
    return completed.returncode == 0 and output_path.exists()


def build_diagrams(root: Path) -> dict[str, dict[str, Any]]:
    root = Path(root).resolve()
    map_path = root / "dashboard" / "static" / "map.json"
    if not map_path.exists():
        raise FileNotFoundError(f"map is missing: {map_path}")
    payload = json.loads(map_path.read_text(encoding="utf-8"))
    spec = _architecture_spec(payload)
    spec_dir = root / "var" / "diagrams"
    output_dir = root / "dashboard" / "static" / "diagrams"
    spec_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    spec_path = spec_dir / "aios-architecture.json"
    output_path = output_dir / "aios-architecture.html"
    spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
    delivered = _deliver(root, spec_path, output_path)
    if not delivered:
        output_path.write_text(_fallback_html(spec), encoding="utf-8")
    return {"architecture": {"components": len(spec["components"]), "delivered": delivered, "output": str(output_path)}}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    print(json.dumps(build_diagrams(args.root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
