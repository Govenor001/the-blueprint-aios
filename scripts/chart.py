#!/usr/bin/env python3
"""Render the five approved AIOS chart shapes as self-contained SVG."""

from __future__ import annotations

import html
import math
from typing import Any

WIDTH, HEIGHT = 700, 260
ACCENT = "#76e0c2"
MUTED = "#9aa5b5"
BG = "#181d27"


def _text(value: Any) -> str:
    return html.escape(str(value))


def _frame(title: str, note: str) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img">',
        f'<rect width="{WIDTH}" height="{HEIGHT}" rx="14" fill="{BG}"/>',
        f'<text x="24" y="32" fill="#f5f7fb" font-family="system-ui" font-size="17">{_text(title)}</text>',
        f'<text x="24" y="242" fill="{MUTED}" font-family="system-ui" font-size="11">{_text(note)}</text>',
    ]


def _finish(lines: list[str]) -> str:
    lines.append("</svg>")
    return "".join(lines)


def render(spec: dict[str, Any]) -> str:
    shape = spec.get("shape")
    title = spec.get("title", "")
    note = spec.get("note") or f"from {spec.get('source', 'UNAVAILABLE')}, collected {spec.get('collected_at', 'UNAVAILABLE')}"
    lines = _frame(title, note)
    if shape == "kpi":
        value = spec.get("value", "UNAVAILABLE")
        change = spec.get("change", "")
        lines.append(f'<text x="40" y="142" fill="{ACCENT}" font-family="system-ui" font-weight="700" font-size="64">{_text(value)}</text>')
        lines.append(f'<text x="42" y="174" fill="{MUTED}" font-family="system-ui" font-size="15">{_text(change)}</text>')
    elif shape in {"line", "bar"}:
        series = spec.get("series", [])
        values = [float(point[1]) for row in series for point in row.get("points", [])]
        max_value = max(values or [1])
        baseline = 205
        lines.append(f'<line x1="40" y1="{baseline}" x2="660" y2="{baseline}" stroke="#2b3443"/>')
        for series_index, row in enumerate(series):
            points = row.get("points", [])
            if shape == "line":
                coords = []
                for index, point in enumerate(points):
                    x = 50 + (index * 590 / max(1, len(points) - 1))
                    y = baseline - (float(point[1]) / max_value * 145)
                    coords.append(f"{x:.1f},{y:.1f}")
                if coords:
                    lines.append(f'<polyline points="{" ".join(coords)}" fill="none" stroke="{ACCENT}" stroke-width="3"/>')
            else:
                bar_width = 540 / max(1, len(points))
                for index, point in enumerate(points):
                    x = 70 + index * bar_width
                    height = float(point[1]) / max_value * 145
                    y = baseline - height
                    lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_width * .65:.1f}" height="{height:.1f}" fill="{ACCENT}" opacity="{1 - series_index * .15:.2f}"/>')
            lines.append(f'<text x="{50 + series_index * 100}" y="72" fill="{ACCENT}" font-family="system-ui" font-size="12">{_text(row.get("label", ""))}</text>')
    elif shape == "table":
        for index, row in enumerate(spec.get("rows", [])[:7]):
            y = 72 + index * 22
            lines.append(f'<text x="32" y="{y}" fill="#f5f7fb" font-family="system-ui" font-size="13">{_text(row)}</text>')
    elif shape == "donut":
        value = float(spec.get("value", 0))
        radius = 62
        lines.append(f'<circle cx="350" cy="132" r="{radius}" fill="none" stroke="#2b3443" stroke-width="22"/>')
        circumference = 2 * math.pi * radius
        lines.append(f'<circle cx="350" cy="132" r="{radius}" fill="none" stroke="{ACCENT}" stroke-width="22" stroke-dasharray="{circumference * value / 100:.1f} {circumference:.1f}" transform="rotate(-90 350 132)"/>')
        lines.append(f'<text x="350" y="140" text-anchor="middle" fill="#f5f7fb" font-family="system-ui" font-size="24">{_text(value)}%</text>')
    else:
        raise ValueError("shape must be one of kpi, line, bar, table, donut")
    return _finish(lines)


def to_png(svg: str, output: str) -> bool:
    try:
        import cairosvg
        cairosvg.svg2png(bytestring=svg.encode("utf-8"), write_to=output)
        return True
    except Exception:
        return False
