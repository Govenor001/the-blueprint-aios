#!/usr/bin/env python3
"""Idempotent, testable filesystem portion of the server installer."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Mapping, Any

try:
    from .bootstrap import bootstrap
    from .preflight import load_route, validate_environment
except ImportError:
    from bootstrap import bootstrap
    from preflight import load_route, validate_environment


def install_server(root: Path, env: Mapping[str, str] | None = None) -> dict[str, Any]:
    root = Path(root).resolve()
    environ = dict(env or os.environ)
    problems = validate_environment(load_route(root), environ)
    if problems:
        raise ValueError("; ".join(problems))
    bootstrap(root)
    return {"root": str(root), "idempotent": True, "services": ["dashboard", "bridge"], "schedules": "installed-disabled-until-owner-approval"}
