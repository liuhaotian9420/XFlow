#!/usr/bin/env python3
"""Rewrite Codex JSONL files: fix mojibake in Get-Content command outputs via UTF-8 re-read."""

from __future__ import annotations

import argparse
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.jsonl_encoding_fix import repair_jsonl_file  # noqa: E402


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "jsonl_files",
        nargs="+",
        type=Path,
        help="Paths to .jsonl files (relative or absolute)",
    )
    p.add_argument(
        "--repo-root",
        type=Path,
        default=None,
        help="Repository root for resolving Get-Content paths (default: parent of tests/)",
    )
    args = p.parse_args()
    repo = (
        args.repo_root.resolve()
        if args.repo_root
        else Path(__file__).resolve().parent.parent
    )
    for f in args.jsonl_files:
        fp = f.resolve()
        repair_jsonl_file(fp, repo_root=repo)
        print(f"repaired {fp}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
