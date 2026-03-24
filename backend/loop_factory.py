"""Custom asyncio loop factory for uvicorn on Windows.

On Windows + ``--reload``, forcing a Proactor loop can trigger socket accept issues
in some environments (e.g. ``WinError 87``). For API serving stability we force a
Selector loop for uvicorn workers.

Codex subprocess execution still works because backend codex execution path has a
synchronous subprocess fallback when async subprocess is unavailable on Selector.

Usage::

    uv run uvicorn backend.main:app --reload --loop backend.loop_factory:proactor_loop_factory
"""

from __future__ import annotations

import asyncio
import sys


def proactor_loop_factory() -> asyncio.AbstractEventLoop:
    """Return an event-loop instance (required by asyncio.Runner(loop_factory=...))."""
    if sys.platform == "win32":
        return asyncio.SelectorEventLoop()
    return asyncio.new_event_loop()
