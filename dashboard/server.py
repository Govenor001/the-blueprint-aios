#!/usr/bin/env python3
"""Small authenticated FastAPI server for the static Mission Control UI."""

from __future__ import annotations

import base64
import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles

from scripts.activity import log
from scripts.build_map import build_map


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


def create_app(root: Path | str | None = None, password: str | None = None) -> FastAPI:
    root_path = Path(root or os.environ.get("AIOS_ROOT", Path.cwd())).resolve()
    dashboard_password = password if password is not None else os.environ.get("DASHBOARD_PASSWORD")
    if not dashboard_password:
        raise RuntimeError("DASHBOARD_PASSWORD is required before the dashboard can start")

    app = FastAPI(title="AIOS Mission Control", docs_url=None, redoc_url=None)
    static_dir = root_path / "dashboard" / "static"

    async def auth(request: Request) -> JSONResponse | None:
        if not _authorized(request, dashboard_password):
            return JSONResponse(
                {"detail": "Authentication required"},
                status_code=401,
                headers={"WWW-Authenticate": 'Basic realm="AIOS"'},
            )
        return None

    @app.get("/api/health")
    async def health(request: Request) -> JSONResponse:
        denied = await auth(request)
        if denied:
            return denied
        return JSONResponse({"status": "ok", "dashboard": "ready"})

    @app.get("/api/map")
    async def map_endpoint(request: Request) -> JSONResponse:
        denied = await auth(request)
        if denied:
            return denied
        map_path = static_dir / "map.json"
        if not map_path.exists():
            try:
                build_map(root_path)
            except (OSError, ValueError, KeyError) as exc:
                return JSONResponse({"detail": str(exc)}, status_code=500)
        return JSONResponse(json.loads(map_path.read_text(encoding="utf-8")))

    @app.get("/api/skill/{name}")
    async def skill_endpoint(name: str, request: Request) -> JSONResponse:
        denied = await auth(request)
        if denied:
            return denied
        map_path = static_dir / "map.json"
        if not map_path.exists():
            build_map(root_path)
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        for wing in payload["wings"]:
            for department in wing["departments"]:
                for agent in department["agents"]:
                    if agent["name"] == name:
                        return JSONResponse(agent)
        return JSONResponse({"detail": "Unknown skill"}, status_code=404)

    @app.get("/api/activity")
    async def activity_endpoint(request: Request, limit: int = 50) -> JSONResponse:
        denied = await auth(request)
        if denied:
            return denied
        limit = max(1, min(limit, 500))
        path = root_path / "var" / "activity.jsonl"
        rows: list[dict[str, Any]] = []
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines()[-limit:]:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:
                    continue
        return JSONResponse({"items": rows})

    @app.post("/api/run")
    async def run_endpoint(request: Request) -> JSONResponse:
        denied = await auth(request)
        if denied:
            return denied
        body = await request.json()
        name = body.get("skill") if isinstance(body, dict) else None
        map_path = static_dir / "map.json"
        if not map_path.exists():
            build_map(root_path)
        payload = json.loads(map_path.read_text(encoding="utf-8"))
        allowlist = {
            agent["name"]
            for wing in payload["wings"]
            for department in wing["departments"]
            for agent in department["agents"]
        }
        if not isinstance(name, str) or name not in allowlist:
            return JSONResponse({"detail": "Skill is not allowlisted"}, status_code=400)
        command = [sys.executable, str(root_path / "scripts" / "run_skill.py"), name]
        try:
            process = subprocess.Popen(command, cwd=root_path, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        except OSError as exc:
            log("skill_start_failed", name, str(exc), "error")
            return JSONResponse({"detail": "Unable to start skill"}, status_code=500)
        log("skill_started", name, f"pid={process.pid}")
        return JSONResponse({"accepted": True, "skill": name, "pid": process.pid}, status_code=202)

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(static_dir / "index.html")

    app.mount("/static", StaticFiles(directory=static_dir), name="static")
    return app


def main() -> int:
    import uvicorn

    root = Path(os.environ.get("AIOS_ROOT", Path.cwd()))
    create_app(root)
    uvicorn.run("dashboard.server:create_app", host="127.0.0.1", port=int(os.environ.get("PORT", "8787")), factory=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
