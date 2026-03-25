#!/usr/bin/env python3
"""Run `codex exec --json` and persist the full JSONL event stream (stdout).

This is intentionally a thin wrapper to capture the *entire* event stream for
inspection (e.g., to verify whether prompt-based "Skill hint" is taking effect).

Example:
  uv run python tests/run_codex_json_stream.py --case-id monitor_screen_daily_current_month --mode raw
  uv run python tests/run_codex_json_stream.py --case-id monitor_screen_daily_current_month --mode hint
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.sql_generator_jsonl_runner import (  # noqa: E402
    run_sql_generator_json_stream,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--case-id",
        required=True,
        help="Case id from tests/sql_generator_eval_cases.json",
    )
    p.add_argument("--mode", choices=["raw", "hint"], required=True)
    p.add_argument(
        "--cases",
        default="tests/sql_generator_eval_cases.json",
        help="Cases JSON path (relative to repo root)",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=300,
        help="Subprocess timeout seconds",
    )
    p.add_argument(
        "--out-dir",
        default="artifacts/codex_jsonl_streams",
        help="Output directory (relative to repo root)",
    )
    p.add_argument(
        "--no-fix-shell-utf8",
        action="store_true",
        help=(
            "Skip rewriting PowerShell Get-Content outputs as UTF-8 from disk "
            "(Windows default is to fix mojibake in aggregated_output)."
        ),
    )
    args = p.parse_args()

    repo_root = Path(__file__).resolve().parent.parent
    out_dir = repo_root / args.out_dir

    result = run_sql_generator_json_stream(
        repo_root=repo_root,
        case_id=args.case_id,
        mode=args.mode,  # type: ignore[arg-type]
        cases_relative=args.cases,
        timeout_s=int(args.timeout),
        out_dir=out_dir,
        fix_shell_utf8=not args.no_fix_shell_utf8,
    )

    if result.returncode != 0:
        raise SystemExit(
            f"codex exec failed (exit={result.returncode}). See {out_dir / f'codex_stderr__{args.case_id}__{args.mode}.txt'}"
        )

    print(str(result.jsonl_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
