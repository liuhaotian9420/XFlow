#!/usr/bin/env python3
"""Preflight checks for mock/real runtime modes."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from backend.runtime_config import APP_MODE_MOCK, APP_MODE_REAL, get_runtime_status


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check local runtime readiness.")
    parser.add_argument(
        "--mode",
        choices=[APP_MODE_MOCK, APP_MODE_REAL],
        default=None,
        help="Optional expected app mode.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Print machine-readable JSON.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    status = get_runtime_status()
    mode = str(status["app_mode"])
    codex_ready = bool(status["codex"]["ready"])
    odps_ready = bool(status["odps"]["ready"])
    if args.mode == APP_MODE_REAL:
        ok = mode == APP_MODE_REAL and codex_ready and odps_ready
    elif args.mode == APP_MODE_MOCK:
        ok = mode == APP_MODE_MOCK
    else:
        ok = mode == APP_MODE_MOCK or (codex_ready and odps_ready)

    if args.json:
        print(json.dumps({"ok": ok, **status}, ensure_ascii=False, indent=2))
        return 0 if ok else 1

    print(f"APP_MODE: {mode}")
    if args.mode and args.mode != mode:
        print(f"Expected mode: {args.mode}")
    print(f"Codex: {'ready' if codex_ready else 'not ready'}")
    for issue in status["codex"]["issues"]:
        print(f"  - {issue['message']}")
    print(f"ODPS: {'ready' if odps_ready else 'not ready'}")
    for issue in status["odps"]["issues"]:
        print(f"  - {issue['message']}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
