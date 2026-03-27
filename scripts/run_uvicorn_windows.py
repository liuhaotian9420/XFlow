"""Start the API on Windows with Proactor policy applied before uvicorn imports the app.

Use from repo root::

    uv run python scripts/run_uvicorn_windows.py          # default: host=127.0.0.1, port=8000
    uv run python scripts/run_uvicorn_windows.py --reload  # with hot-reload

This avoids ``NotImplementedError`` from ``asyncio.create_subprocess_exec`` when running
the Codex CLI subprocess (SelectorEventLoop on Windows does not support subprocess pipes).
"""

from __future__ import annotations

import argparse
import asyncio
import os
import sys
from pathlib import Path


_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run xyf backend (Windows-friendly asyncio).")
    parser.add_argument("--host", default=os.getenv("UVICORN_HOST", "127.0.0.1"))
    parser.add_argument("--port", type=int, default=int(os.getenv("UVICORN_PORT", "8000")))
    parser.add_argument("--reload", action="store_true")
    parser.add_argument("--log-level", default=os.getenv("UVICORN_LOG_LEVEL", "info"))
    args = parser.parse_args()

    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

    import uvicorn

    uvicorn.run(
        "backend.main:app",
        host=args.host,
        port=args.port,
        reload=args.reload,
        log_level=args.log_level,
        loop="backend.loop_factory:proactor_loop_factory",
    )


if __name__ == "__main__":
    main()
