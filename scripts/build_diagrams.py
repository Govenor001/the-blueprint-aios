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


def _workflow_spec() -> dict[str, Any]:
    return {
        "schema_version": 2,
        "diagram_type": "workflow",
        "meta": {"title": "AIOS Agent Run", "quality_profile": "showcase", "views": [{"id": "main", "label": "Request to result", "focus": ["owner", "planner", "approval", "tool", "memory", "reply"]}]},
        "lanes": [{"id": "owner", "label": "Owner"}, {"id": "runtime", "label": "Agent Runtime"}, {"id": "safety", "label": "Safety & Recovery", "variant": "exception"}, {"id": "evidence", "label": "Tools & Evidence"}],
        "phases": [{"id": "intake", "label": "Intake", "fromCol": 0, "toCol": 1}, {"id": "work", "label": "Plan + execute", "fromCol": 2, "toCol": 4, "variant": "emphasis"}, {"id": "report", "label": "Record + report", "fromCol": 5, "toCol": 5, "variant": "dashed"}],
        "groups": [{"id": "safe-loop", "label": "Human approval loop", "lane": "safety", "fromCol": 3, "toCol": 5, "variant": "security"}],
        "mainPath": ["owner", "planner", "approval", "tool", "memory", "reply"],
        "nodes": [
            {"id": "owner", "lane": "owner", "col": 0, "type": "external", "label": "Owner", "sublabel": "request or approval", "width": 132},
            {"id": "planner", "lane": "runtime", "col": 1, "type": "backend", "label": "Scout / Operator", "sublabel": "understand + act", "width": 132},
            {"id": "approval", "lane": "safety", "col": 2, "type": "security", "label": "Approval Gate", "sublabel": "stop before risk", "tag": "human handoff", "width": 132},
            {"id": "blocked", "lane": "safety", "col": 3, "type": "security", "label": "Waiting", "sublabel": "needs owner input", "width": 132},
            {"id": "tool", "lane": "evidence", "col": 3, "type": "messagebus", "label": "Tool / MCP", "sublabel": "read or write", "width": 132},
            {"id": "memory", "lane": "evidence", "col": 4, "type": "database", "label": "Evidence + Memory", "sublabel": "trace the result", "width": 132},
            {"id": "reply", "lane": "owner", "col": 5, "type": "frontend", "label": "Dashboard / Telegram", "sublabel": "clear handoff", "width": 132}
        ],
        "edges": [
            {"id": "request-plan", "from": "owner", "to": "planner", "label": "intent", "variant": "emphasis"},
            {"id": "plan-approval", "from": "planner", "to": "approval", "label": "risk check", "variant": "security"},
            {"id": "approval-wait", "from": "approval", "to": "blocked", "label": "needs consent", "variant": "security", "role": "branch"},
            {"id": "approved-tool", "from": "approval", "to": "tool", "label": "approved", "variant": "emphasis"},
            {"id": "tool-memory", "from": "tool", "to": "memory", "label": "record evidence", "variant": "dashed"},
            {"id": "memory-reply", "from": "memory", "to": "reply", "label": "report", "variant": "emphasis"}
        ],
        "cards": [{"dot": "cyan", "title": "Safety contract", "items": ["Every risky action stops at a human gate", "Unavailable connections stay visible instead of becoming fake numbers"]}]
    }


def _dataflow_spec() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "diagram_type": "dataflow",
        "meta": {"title": "AIOS Evidence Flow", "quality_profile": "showcase", "views": [{"id": "data-path", "label": "From source to panel", "focus": ["source", "runtime", "memory", "panel"]}]},
        "stages": [{"label": "Sources"}, {"label": "Runtime"}, {"label": "Evidence"}, {"label": "Surfaces"}],
        "nodes": [
            {"id": "source", "type": "cloud", "label": "Connected Sources", "sublabel": "Gmail, APIs, files", "stage": 0, "row": 1, "tag": "owner linked"},
            {"id": "runtime", "type": "backend", "label": "Agents", "sublabel": "Scout / Operator / Advisor", "stage": 1, "row": 1, "tag": "approval aware"},
            {"id": "memory", "type": "database", "label": "Second Brain", "sublabel": "vault + activity", "stage": 2, "row": 0, "tag": "durable"},
            {"id": "metrics", "type": "database", "label": "Metric Store", "sublabel": "timestamped readings", "stage": 2, "row": 2, "tag": "source + age"},
            {"id": "panel", "type": "frontend", "label": "Mission Control", "sublabel": "panels + map", "stage": 3, "row": 1, "tag": "student view"}
        ],
        "flows": [
            {"id": "source-runtime", "from": "source", "to": "runtime", "label": "read / receive", "classification": "connected data", "variant": "emphasis"},
            {"id": "runtime-memory", "from": "runtime", "to": "memory", "label": "context + trace", "classification": "durable evidence", "variant": "default"},
            {"id": "runtime-metrics", "from": "runtime", "to": "metrics", "label": "collect", "classification": "timestamped", "variant": "dashed"},
            {"id": "memory-panel", "from": "memory", "to": "panel", "label": "map + activity", "classification": "read-only", "variant": "default"},
            {"id": "metrics-panel", "from": "metrics", "to": "panel", "label": "numbers + freshness", "classification": "read-only", "variant": "emphasis"}
        ],
        "cards": [{"dot": "emerald", "title": "Trust boundary", "items": ["Panels never invent values for unconnected services", "Every reading carries its source and collection time"]}]
    }


def _lifecycle_spec() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "diagram_type": "lifecycle",
        "meta": {"title": "AIOS Autonomy Ladder", "quality_profile": "showcase", "views": [{"id": "ladder", "label": "Manual to autonomous", "focus": ["manual", "assisted", "approved", "autonomous"]}, {"id": "recovery", "label": "Recovery", "focus": ["blocked", "failed"]}]},
        "lanes": [{"id": "main", "label": "Autonomy levels"}, {"id": "wait", "label": "Human wait"}, {"id": "error", "label": "Recovery"}],
        "states": [
            {"id": "manual", "type": "start", "label": "Manual", "sublabel": "owner runs each step", "lane": "main", "col": 0, "step": "01", "tag": "start"},
            {"id": "assisted", "type": "active", "label": "Assisted", "sublabel": "agent drafts, owner runs", "lane": "main", "col": 1, "step": "02", "tag": "review"},
            {"id": "approved", "type": "decision", "label": "Approved", "sublabel": "agent acts after consent", "lane": "main", "col": 2, "step": "03", "tag": "gate"},
            {"id": "autonomous", "type": "success", "label": "Autonomous", "sublabel": "bounded routine", "lane": "main", "col": 3, "step": "04", "tag": "bounded"},
            {"id": "blocked", "type": "waiting", "label": "Blocked", "sublabel": "missing input", "lane": "wait", "col": 1, "tag": "pause"},
            {"id": "failed", "type": "failure", "label": "Recoverable", "sublabel": "retry or hand back", "lane": "error", "col": 2, "tag": "safe stop"}
        ],
        "transitions": [
            {"id": "manual-assisted", "from": "manual", "to": "assisted", "variant": "default"},
            {"id": "assisted-approved", "from": "assisted", "to": "approved", "variant": "emphasis"},
            {"id": "approved-autonomous", "from": "approved", "to": "autonomous", "variant": "emphasis"},
            {"id": "approved-blocked", "from": "approved", "to": "blocked", "variant": "security", "fromSide": "bottom", "toSide": "top"},
            {"id": "approved-failed", "from": "approved", "to": "failed", "variant": "security", "fromSide": "bottom", "toSide": "top"}
        ],
        "cards": [{"dot": "rose", "title": "Promotion rule", "items": ["Students promote one agent only after its output is understood", "Blocked and failed are recoverable states, never silent success"]}]
    }


def _sequence_spec() -> dict[str, Any]:
    return {
        "schema_version": 1,
        "diagram_type": "sequence",
        "meta": {"title": "AIOS Request Sequence", "quality_profile": "showcase", "views": [{"id": "request", "label": "Request to handoff", "focus": ["owner", "dashboard", "agent", "policy", "source", "trace"]}]},
        "participants": [
            {"id": "owner", "type": "external", "label": "Owner", "sublabel": "request"},
            {"id": "dashboard", "type": "frontend", "label": "Dashboard", "sublabel": "Mission Control"},
            {"id": "agent", "type": "backend", "label": "Agent", "sublabel": "Scout / Operator"},
            {"id": "policy", "type": "security", "label": "Approval", "sublabel": "safety gate"},
            {"id": "source", "type": "cloud", "label": "Source / MCP", "sublabel": "connected tool"},
            {"id": "trace", "type": "database", "label": "Second Brain", "sublabel": "activity + memory"}
        ],
        "segments": [{"from": 140, "to": 300, "label": "Request"}, {"from": 320, "to": 500, "label": "Safety + work"}, {"from": 520, "to": 680, "label": "Evidence + reply"}],
        "messages": [
            {"id": "ask", "from": "owner", "to": "dashboard", "y": 180, "label": "ask for work", "variant": "default"},
            {"id": "dispatch", "from": "dashboard", "to": "agent", "y": 225, "label": "dispatch skill", "variant": "emphasis"},
            {"id": "check", "from": "agent", "to": "policy", "y": 270, "label": "check scope", "variant": "security"},
            {"id": "approved", "from": "policy", "to": "agent", "y": 315, "label": "approved / wait", "variant": "return"},
            {"id": "read", "from": "agent", "to": "source", "y": 370, "label": "read or act", "variant": "emphasis"},
            {"id": "result", "from": "source", "to": "agent", "y": 425, "label": "structured result", "variant": "return"},
            {"id": "record", "from": "agent", "to": "trace", "y": 480, "label": "record evidence", "variant": "dashed"},
            {"id": "reply", "from": "agent", "to": "dashboard", "y": 535, "label": "show result", "variant": "return"},
            {"id": "handoff", "from": "dashboard", "to": "owner", "y": 590, "label": "handoff", "variant": "return"}
        ],
        "activations": [{"participant": "dashboard", "from": 220, "to": 550, "type": "frontend"}, {"participant": "agent", "from": 225, "to": 500, "type": "backend"}, {"participant": "policy", "from": 265, "to": 325, "type": "security"}, {"participant": "source", "from": 365, "to": 435, "type": "cloud"}, {"participant": "trace", "from": 475, "to": 525, "type": "database"}],
        "cards": [{"dot": "orange", "title": "Observable handoff", "items": ["The owner sees where work pauses", "The result is recorded before it is reported"]}]
    }


def _fallback_html(spec: dict[str, Any]) -> str:
    nodes = []
    raw_nodes = spec.get("components") or spec.get("nodes") or spec.get("states") or spec.get("participants") or []
    for component in raw_nodes:
        label = html.escape(component["label"])
        sublabel = html.escape(component.get("sublabel", ""))
        nodes.append(f'<article><b>{label}</b><small>{sublabel}</small></article>')
    return """<!doctype html>
<html lang="en"><meta charset="utf-8"><title>AIOS Second Brain</title>
<style>body{margin:0;padding:32px;background:#f6f8f8;color:#17212b;font:16px system-ui}main{max-width:1100px;margin:auto}section{display:flex;flex-wrap:wrap;gap:14px;align-items:center;justify-content:center}article{min-width:150px;padding:18px;border:1px solid #dce3e3;border-radius:16px;background:#fff;box-shadow:0 8px 20px #23333c12}b,small{display:block}small{margin-top:7px;color:#667380;font-size:12px}</style>
<main><h1>AIOS Second Brain</h1><p>Plain map fallback. Install Node and run the diagram timer for the full Archify artifact.</p><section>""" + "".join(nodes) + "</section></main></html>"


def _deliver(root: Path, diagram_type: str, spec_path: Path, output_path: Path) -> bool:
    archify = root / "vendor" / "archify" / "bin" / "archify.mjs"
    node = shutil.which("node")
    if not node or not archify.exists():
        return False
    completed = subprocess.run(
        [node, str(archify), "deliver", diagram_type, str(spec_path), str(output_path), "--quality", "showcase", "--json"],
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
    specs = {
        "architecture": _architecture_spec(payload),
        "workflow": _workflow_spec(),
        "dataflow": _dataflow_spec(),
        "lifecycle": _lifecycle_spec(),
        "sequence": _sequence_spec(),
    }
    spec_dir = root / "var" / "diagrams"
    output_dir = root / "dashboard" / "static" / "diagrams"
    spec_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    results: dict[str, dict[str, Any]] = {}
    for diagram_type, spec in specs.items():
        spec_path = spec_dir / f"aios-{diagram_type}.json"
        output_path = output_dir / f"aios-{diagram_type}.html"
        spec_path.write_text(json.dumps(spec, indent=2), encoding="utf-8")
        delivered = _deliver(root, diagram_type, spec_path, output_path)
        if not delivered:
            output_path.write_text(_fallback_html(spec), encoding="utf-8")
        count_key = "components" if "components" in spec else "nodes" if "nodes" in spec else "states" if "states" in spec else "participants"
        results[diagram_type] = {count_key: len(spec.get(count_key, [])), "delivered": delivered, "output": str(output_path)}
    return results


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path.cwd())
    args = parser.parse_args(argv)
    print(json.dumps(build_diagrams(args.root)))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
