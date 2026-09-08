#!/usr/bin/env python3
"""Generate systemd timer definitions without enabling them implicitly."""

from __future__ import annotations

from pathlib import Path
from typing import Any


def schedule_jobs(root: Path, jobs: list[dict[str, Any]]) -> None:
    output = Path(root) / "var" / "generated-systemd"
    output.mkdir(parents=True, exist_ok=True)
    for job in jobs:
        name = str(job["name"])
        command = str(job["command"])
        interval = str(job.get("interval", "hourly"))
        (output / f"aios-{name}.service").write_text(
            "[Unit]\nDescription=AIOS %s\n\n[Service]\nType=oneshot\nExecStart=%s\n" % (name, command), encoding="utf-8"
        )
        (output / f"aios-{name}.timer").write_text(
            "[Unit]\nDescription=AIOS schedule %s\n\n[Timer]\nOnCalendar=%s\nPersistent=true\n\n[Install]\nWantedBy=timers.target\n" % (name, interval), encoding="utf-8"
        )
