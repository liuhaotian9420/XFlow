"""xyf-competition-mvp backend package.

On Windows, force ``ProactorEventLoop`` so that ``asyncio.create_subprocess_exec`` (used by
the Codex CLI subprocess path) is available. This ``set_event_loop_policy`` runs at import time,
but **uvicorn >= 0.36** creates its own loop via a loop factory, which may override us.

Therefore always start with one of:

    uv run uvicorn backend.main:app --reload --loop backend.loop_factory:proactor_loop_factory

or:

    uv run python scripts/run_uvicorn_windows.py --reload
"""

from __future__ import annotations

import asyncio
import sys

if sys.platform == "win32":
    try:
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
    except AttributeError:
        pass
