"""Custom asyncio loop factory for uvicorn on Windows.

``uvicorn.loops.asyncio`` deliberately returns ``SelectorEventLoop`` when
``use_subprocess=True`` (i.e. ``--reload``), but ``SelectorEventLoop`` does **not**
implement ``asyncio.create_subprocess_exec`` on Windows. Our ACP layer needs that.

Usage::

    uv run uvicorn backend.main:app --reload --loop backend.loop_factory.proactor_loop_factory

Or via the helper script ``scripts/run_uvicorn_windows.py`` which sets the policy before
uvicorn starts.
"""

from __future__ import annotations

import asyncio
import sys
from collections.abc import Callable


def proactor_loop_factory(
    use_subprocess: bool = False,  # noqa: ARG001
) -> Callable[[], asyncio.AbstractEventLoop]:
    """Always return ``ProactorEventLoop`` on Windows regardless of ``use_subprocess``."""
    if sys.platform == "win32":
        return asyncio.ProactorEventLoop
    return asyncio.SelectorEventLoop
