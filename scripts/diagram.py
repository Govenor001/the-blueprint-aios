#!/usr/bin/env python3
"""Compatibility entry point for the scheduled diagram builder."""

try:
    from .build_diagrams import build_diagrams
except ImportError:
    from build_diagrams import build_diagrams

__all__ = ["build_diagrams"]
