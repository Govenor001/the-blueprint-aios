#!/usr/bin/env python3
"""Authenticated FastAPI server for the static Mission Control dashboard."""

from __future__ import annotations

import base64
import asyncio
import json
import os
import re
import shutil
import subprocess
import sys
import uuid
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from fastapi.staticfiles import StaticFiles
import yaml

from scripts.activity import log
from scripts.build_map import build_map
from scripts.model_for import model_for
from scripts.mcp_connections import configured_servers
from scripts.chart import render as render_chart


def _authorized(request: Request, password: str) -> bool:
    header = request.headers.get("Authorization", "")
    if not header.startswith("Basic "):
        return False
    try:
        decoded = base64.b64decode(header[6:], validate=True).decode("utf-8")
        username, supplied = decoded.split(":", 1)
    except (ValueError, UnicodeDecodeError):
        return False
    return username == "owner" and supplied == password


def _deny() -> JSONResponse:
    return JSONResponse(
        {"detail": "Authentication required"},
        status_code=401,
        headers={"WWW-Authenticate": 'Basic realm="AIOS"'},
    )


def _agents(payload: dict[str, Any]) -> list[dict[str, Any]]:
    return [
        agent
        for wing in payload.get("wings", [])
        for department in wing.get("departments", [])
        for function in department.get("functions", [])
        for agent in function.get("agents", [])
    ]


def create_app(root: Path | str | None = None, password: str | None = None) -> FastAPI:
    root_path = Path(root or os.environ.get("AIOS_ROOT", Path.cwd())).resolve()
    dashboard_password = password if password is not None else os.environ.get("DASHBOARD_PASSWORD")
    if not dashboard_password:
        raise RuntimeError("DASHBOARD_PASSWORD is not set. Refusing to start.")

    app = FastAPI(title="AIOS Mission Control", docs_url=None, redoc_url=None)
    static_dir = root_path / "dashboard" / "static"

    def authorized(request: Request) -> bool:
        return _authorized(request, dashboard_password)

    @app.get("/api/health")
    async def health(request: Request) -> JSONResponse:
        if not authorized(request):
            return _deny()
        disk = shutil.disk_usage(root_path)
        return JSONResponse({
            "bridge": (root_path / "var" / "bridge.pid").exists(),
            "claude": shutil.which("claude") is not None,
            "disk_free_mb": disk.free // (1024 * 1024),
        })

    @app.get("/api/map")
    async def map_endpoint(request: Request) -> JSONResponse:
        if not authorized(request):
            return _deny()
        map_path = static_dir / "map.json"
        if not map_path.exists():
            try:
                build_map(root_path)
            except (OSError, ValueError, KeyError) as exc:
                return JSONResponse({"detail": str(exc)}, status_code=500)
        return JSONResponse(json.loads(map_path.read_text(encoding="utf-8")))

    @app.get("/api/skill/{name}")
    async def skill_endpoint(name: str, request: Request) -> JSONResponse:
        if not authorized(request):
            return _deny()
        map_path = static_dir / "map.json"
        if not map_path.exists():
            build_map(root_path)
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        for agent in _agents(payload):
            if agent["name"] == name:
                return JSONResponse(agent)
        return JSONResponse({"detail": "Unknown skill"}, status_code=404)

    @app.get("/api/activity")
    async def activity_endpoint(request: Request, limit: int = 50) -> JSONResponse:
        if not authorized(request):
            return _deny()
        limit = max(1, min(limit, 500))
        path = root_path / "var" / "activity.jsonl"
        rows: list[dict[str, Any]] = []
        if path.exists():
            for line in reversed(path.read_text(encoding="utf-8").splitlines()):
                if len(rows) >= limit:
                    break
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return JSONResponse({"items": rows})

    @app.get("/api/connections")
    async def connections_endpoint(request: Request) -> JSONResponse:
        """Report integration readiness without ever returning credential values."""
        if not authorized(request):
            return _deny()
        bedrock_route = os.environ.get("CLAUDE_CODE_USE_BEDROCK") == "1" or os.environ.get("AIOS_MODEL_ROUTE") == "bedrock"
        definitions = (
            (("Claude via Bedrock", ("AWS_REGION",)) if bedrock_route else ("Claude", ("CLAUDE_CODE_OAUTH_TOKEN",))),
            ("Telegram", ("TELEGRAM_BOT_TOKEN", "TELEGRAM_CHAT_ID")),
            ("Composio", ("COMPOSIO_API_KEY",)),
            ("ElevenLabs", ("ELEVEN_API_KEY", "ELEVENLABS_API_KEY")),
            ("Blotato", ("BLOTATO_API_KEY",)),
            ("Local model", ("AIOS_LOCAL_MODEL_URL",)),
        )
        connections = []
        for name, variables in definitions:
            present = [key for key in variables if os.environ.get(key)]
            # ElevenLabs supports both the current and legacy variable spelling.
            satisfied = bool(present) if name == "ElevenLabs" else len(present) == len(variables)
            if name == "Claude via Bedrock":
                satisfied = bedrock_route and bool(os.environ.get("AWS_REGION"))
            connections.append({
                "name": name,
                "status": "connected" if satisfied else "needs_setup",
                "configured": len(present),
                "required": 1 if name == "ElevenLabs" else len(variables),
            })
        for server in configured_servers(root_path):
            cached_accounts = []
            if server["name"] == "blotato":
                cache = root_path / "var" / "connections" / "blotato.json"
                if cache.exists():
                    try:
                        cached_accounts = json.loads(cache.read_text(encoding="utf-8")).get("accounts", [])
                    except (OSError, json.JSONDecodeError):
                        cached_accounts = []
            connections.append({
                "name": f"MCP: {server['name']}",
                "status": server["status"],
                "configured": 0 if server["missing"] else 1,
                "required": 1,
                "tier": server["tier"],
                "missing": server["missing"],
                "tools": server["tools"],
                "accounts": cached_accounts,
            })
        return JSONResponse({"connections": connections})

    @app.get("/api/panels")
    async def panels_endpoint(request: Request) -> JSONResponse:
        if not authorized(request):
            return _deny()
        panels = []
        panel_dir = root_path / "config" / "panels"
        for config_path in sorted(panel_dir.glob("*.yaml")):
            payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            cards = []
            for card in payload.get("cards", []):
                card_id = str(card.get("id") or card.get("title", "card")).lower().replace(" ", "-")
                metric = root_path / "var" / "metrics" / f"{card_id}.jsonl"
                latest = None
                if metric.exists():
                    for line in reversed(metric.read_text(encoding="utf-8").splitlines()):
                        try:
                            latest = json.loads(line)
                            break
                        except json.JSONDecodeError:
                            continue
                cards.append({"id": card_id, "title": card.get("title", card_id), "shape": card.get("shape", "table"), "latest": latest})
            panels.append({"name": config_path.stem, "cards": cards})
        return JSONResponse({"panels": panels})

    @app.get("/api/chart/{card_id}")
    async def chart_endpoint(card_id: str, request: Request) -> Response:
        """Render a chart from append-only local history; never call a connector here."""
        if not authorized(request):
            return _deny()
        if not re.fullmatch(r"[a-z0-9-]+", card_id):
            return JSONResponse({"detail": "Invalid card"}, status_code=400)
        card_config = None
        for config_path in sorted((root_path / "config" / "panels").glob("*.yaml")):
            payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            for card in payload.get("cards", []):
                value = str(card.get("id") or card.get("title", "card")).lower().replace(" ", "-")
                if value == card_id:
                    card_config = card
                    break
            if card_config:
                break
        if not card_config:
            return JSONResponse({"detail": "Unknown card"}, status_code=404)
        metric = root_path / "var" / "metrics" / f"{card_id}.jsonl"
        rows: list[dict[str, Any]] = []
        if metric.exists():
            for line in metric.read_text(encoding="utf-8").splitlines()[-30:]:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("status") == "available":
                    rows.append(row)
        latest = rows[-1] if rows else {}
        shape = card_config.get("shape", "table")
        spec: dict[str, Any] = {
            "shape": shape,
            "title": card_config.get("title", card_id),
            "source": latest.get("source_label", "UNAVAILABLE"),
            "collected_at": latest.get("retrieved_at", "UNAVAILABLE"),
        }
        values = [(row.get("retrieved_at", ""), row.get("value")) for row in rows if isinstance(row.get("value"), (int, float))]
        if shape in {"line", "bar"}:
            spec["series"] = [{"label": card_config.get("title", card_id), "points": values}]
        elif shape == "table":
            spec["rows"] = [row.get("value") for row in rows[-7:]] or ["UNAVAILABLE"]
        elif shape == "donut":
            spec["value"] = latest.get("value", 0) if isinstance(latest.get("value", 0), (int, float)) else 0
        else:
            spec["value"] = latest.get("value", "UNAVAILABLE")
        return Response(content=render_chart(spec), media_type="image/svg+xml")

    @app.post("/api/ask")
    async def ask_endpoint(request: Request) -> JSONResponse:
        """Answer a metric question from local history and point to its SVG chart."""
        if not authorized(request):
            return _deny()
        body = await request.json()
        question = body.get("question", "") if isinstance(body, dict) else ""
        if not isinstance(question, str) or not question.strip():
            return JSONResponse({"detail": "A metric question is required"}, status_code=400)
        question = question.strip()[:500]
        question_words = set(re.findall(r"[a-z0-9]+", question.lower()))
        candidates: list[tuple[int, str, dict[str, Any], str]] = []
        for config_path in sorted((root_path / "config" / "panels").glob("*.yaml")):
            payload = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
            for card in payload.get("cards", []):
                card_id = str(card.get("id") or card.get("title", "card")).lower().replace(" ", "-")
                searchable = set(re.findall(r"[a-z0-9]+", f"{config_path.stem} {card_id} {card.get('title', '')}".lower()))
                score = len(question_words & searchable)
                if score:
                    candidates.append((score, card_id, card, config_path.stem))
        if not candidates:
            return JSONResponse({"message": "I do not have a collected card that answers that question yet. Connect the relevant service and run the collector first.", "chart_url": None})
        _, card_id, card_config, panel_name = max(candidates, key=lambda item: item[0])
        metric = root_path / "var" / "metrics" / f"{card_id}.jsonl"
        rows: list[dict[str, Any]] = []
        if metric.exists():
            for line in metric.read_text(encoding="utf-8").splitlines()[-30:]:
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if row.get("status") == "available":
                    rows.append(row)
        if not rows:
            source = card_config.get("source", {})
            connection = source.get("connection") if isinstance(source, dict) else None
            missing = f" Connect {connection} and run the collector." if connection else " Run the collector after adding the source."
            return JSONResponse({"message": f"{card_config.get('title', card_id)} is not connected yet.{missing}", "chart_url": None, "card_id": card_id})
        latest = rows[-1]
        shape = card_config.get("shape", "table")
        spec: dict[str, Any] = {"shape": shape, "title": card_config.get("title", card_id), "source": latest.get("source_label", "UNAVAILABLE"), "collected_at": latest.get("retrieved_at", "UNAVAILABLE")}
        values = [(row.get("retrieved_at", ""), row.get("value")) for row in rows if isinstance(row.get("value"), (int, float))]
        if shape in {"line", "bar"}:
            spec["series"] = [{"label": card_config.get("title", card_id), "points": values}]
        elif shape == "table":
            spec["rows"] = [row.get("value") for row in rows[-7:]]
        elif shape == "donut":
            spec["value"] = latest.get("value", 0) if isinstance(latest.get("value", 0), (int, float)) else 0
        else:
            spec["value"] = latest.get("value", "UNAVAILABLE")
        explanation = f"{card_config.get('title', card_id)} has {len(rows)} collected reading(s), latest from {latest.get('source_label', 'UNAVAILABLE')} at {latest.get('retrieved_at', 'UNAVAILABLE')}. The chart is evidence only; decide what action it supports."
        return JSONResponse({"message": explanation, "chart_url": f"/api/chart/{card_id}", "card_id": card_id, "panel": panel_name})

    @app.post("/api/run")
    async def run_endpoint(request: Request) -> JSONResponse:
        if not authorized(request):
            return _deny()
        body = await request.json()
        name = body.get("skill") if isinstance(body, dict) else None
        owner_input = body.get("input", "") if isinstance(body, dict) else ""
        if not isinstance(owner_input, str):
            owner_input = ""
        owner_input = owner_input.strip()[:5000]
        map_path = static_dir / "map.json"
        if not map_path.exists():
            build_map(root_path)
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        allowed = {agent["name"] for agent in _agents(payload)}
        if not isinstance(name, str) or name not in allowed:
            return JSONResponse({"detail": "Skill is not allowlisted"}, status_code=400)
        try:
            resolved_model = model_for(root_path, skill=name)
            run_id = uuid.uuid4().hex
            command = [sys.executable, str(root_path / "scripts" / "run_skill.py"), name]
            if owner_input:
                command.append(owner_input)
            subprocess.Popen(
                command,
                cwd=root_path,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        except (OSError, KeyError, ValueError) as exc:
            log("skill_start_failed", name, str(exc), "error")
            return JSONResponse({"detail": "Unable to start skill"}, status_code=500)
        log("skill_accepted", name, f"run_id={run_id}; model={resolved_model}")
        return JSONResponse({"run_id": run_id}, status_code=202)

    @app.post("/api/chat")
    async def chat_endpoint(request: Request) -> JSONResponse:
        """Run a focused agent or whole-brain conversation and return its reply."""
        if not authorized(request):
            return _deny()
        body = await request.json()
        scope = body.get("scope", "brain") if isinstance(body, dict) else "brain"
        message = body.get("message", "") if isinstance(body, dict) else ""
        if not isinstance(scope, str) or not isinstance(message, str):
            return JSONResponse({"detail": "A conversation scope and message are required"}, status_code=400)
        message = message.strip()[:8000]
        if not message:
            return JSONResponse({"detail": "A message is required"}, status_code=400)
        map_path = static_dir / "map.json"
        if not map_path.exists():
            build_map(root_path)
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        allowed = {agent["name"] for agent in _agents(payload)}
        if scope != "brain" and scope not in allowed:
            return JSONResponse({"detail": "Agent is not allowlisted"}, status_code=400)
        try:
            resolved_model = model_for(root_path, tier="smart") if scope == "brain" else model_for(root_path, skill=scope)
            if scope == "brain":
                prompt = (
                    "You are the whole AIOS operating brain. Coordinate the right internal "
                    "departments and explain your answer clearly. Do not claim an action was "
                    "completed unless you actually completed it.\n\nOwner message:\n" + message
                )
            else:
                prompt = f"Use the /{scope} skill as the focused AIOS agent.\n\nOwner message:\n{message}"
            log("chat_started", skill=None if scope == "brain" else scope, model=resolved_model)
            result = await asyncio.to_thread(
                subprocess.run,
                ["claude", "--model", resolved_model, "-p", prompt],
                cwd=root_path,
                capture_output=True,
                text=True,
                timeout=300,
                check=False,
            )
            output = result.stdout.strip() or result.stderr.strip() or "No response was returned."
            log("chat_finished", skill=None if scope == "brain" else scope, model=resolved_model, detail=output[-1000:], status="ok" if result.returncode == 0 else "error")
            return JSONResponse({"message": output, "model": resolved_model, "scope": scope})
        except subprocess.TimeoutExpired:
            log("chat_error", skill=None if scope == "brain" else scope, detail="chat timed out", status="error")
            return JSONResponse({"detail": "That conversation took too long. Try a smaller request."}, status_code=504)
        except (OSError, KeyError, ValueError) as exc:
            log("chat_error", skill=None if scope == "brain" else scope, detail=str(exc), status="error")
            return JSONResponse({"detail": "This conversation is not ready yet"}, status_code=503)

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    return app


def main() -> int:
    import uvicorn

    root = Path(os.environ.get("AIOS_ROOT", Path.cwd()))
    if not os.environ.get("DASHBOARD_PASSWORD"):
        print("DASHBOARD_PASSWORD is not set. Refusing to start.", file=sys.stderr)
        return 1
    uvicorn.run(create_app(root), host="127.0.0.1", port=int(os.environ.get("PORT", "8787")))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
