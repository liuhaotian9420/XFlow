#!/usr/bin/env python3
"""Smoke-test real Codex CLI: plan -> pandas execution -> summary -> follow-ups.

Prerequisites:
  - `codex` on PATH (or set CODEX_CLI_COMMAND)
  - `codex login` completed
  - Network reachability to Codex / OpenAI backend
  - Run from repo root:  uv run python scripts/validate_codex.py

This script forces CODEX_MOCK=false for the adapter it uses. It does not start FastAPI.

By default the backend adapter sets CODEX_HTTP_TRANSPORT_ONLY=true (HTTPS/SSE instead of WSS).
Set CODEX_HTTP_TRANSPORT_ONLY=false to test WebSocket transport.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

# Repo root on sys.path (same pattern as tests/run_regression.py)
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from backend.codex.adapter import CodexAdapter, CodexAdapterError, get_adapter
from backend.execution.engine import run_plan
from backend.observability import save_snapshot


def build_profile(df: pd.DataFrame, filename: str) -> dict:
    return {
        "filename": filename,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": [{"name": str(col), "dtype": str(df[col].dtype)} for col in df.columns],
    }


async def main_async(args: argparse.Namespace) -> int:
    os.environ["CODEX_MOCK"] = "false"

    fixtures = Path(args.fixtures_dir)
    csv_path = fixtures / args.csv
    if not csv_path.is_file():
        print(f"ERROR: fixture not found: {csv_path}", file=sys.stderr)
        return 2

    df = pd.read_csv(csv_path)
    profile = build_profile(df, args.csv)
    task_id = "validate-codex-smoke"

    adapter: CodexAdapter = get_adapter()
    if args.timeout is not None:
        adapter.timeout_seconds = args.timeout

    print("=== Codex full-loop validation ===")
    print(f"CSV: {csv_path}")
    print(f"Question: {args.question}")
    print(f"CLI: {adapter.command!r}, timeout={adapter.timeout_seconds}s")
    print()

    try:
        plan = await adapter.generate_plan(
            question=args.question,
            schema_profile=profile,
            task_id=task_id,
        )
    except CodexAdapterError as exc:
        print(f"FAIL generate_plan: {exc}", file=sys.stderr)
        return 1

    print("--- AnalysisPlan (parsed) ---")
    print(json.dumps(plan.model_dump(), ensure_ascii=False, indent=2))
    save_snapshot(task_id, "validate_plan", plan.model_dump())

    try:
        result = run_plan(df=df, plan=plan)
    except Exception as exc:  # pragma: no cover
        print(f"FAIL run_plan: {exc}", file=sys.stderr)
        return 1

    result_summary = {
        "row_count": len(result.table.rows),
        "columns": result.table.columns,
        "chart_type": result.chart.chart_type.value,
    }
    print()
    print("--- Execution summary ---")
    print(json.dumps(result_summary, ensure_ascii=False, indent=2))
    save_snapshot(task_id, "validate_exec_summary", result_summary)

    try:
        summary_text = await adapter.generate_summary(
            goal=plan.goal,
            result_df_summary=result_summary,
            task_id=task_id,
        )
    except CodexAdapterError as exc:
        print(f"FAIL generate_summary: {exc}", file=sys.stderr)
        return 1

    print()
    print("--- Summary (text) ---")
    print(summary_text)

    try:
        followups = await adapter.generate_followups(
            goal=plan.goal,
            result_df_summary=result_summary,
            task_id=task_id,
        )
    except CodexAdapterError as exc:
        print(f"FAIL generate_followups: {exc}", file=sys.stderr)
        return 1

    print()
    print("--- Follow-ups ---")
    print(json.dumps(followups, ensure_ascii=False, indent=2))

    if len(followups) < 3:
        print(
            "\nWARN: fewer than 3 follow-ups returned; check codex_followups_call snapshot.",
            file=sys.stderr,
        )

    print()
    print("OK: full Codex loop completed. See artifacts/tasks/validate-codex-smoke/")
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    default_fixtures = Path(__file__).resolve().parent.parent / "tests" / "fixtures"
    p.add_argument(
        "--fixtures-dir",
        default=str(default_fixtures),
        help="Directory containing CSV fixtures",
    )
    p.add_argument(
        "--csv",
        default="sales_data.csv",
        help="Fixture CSV filename under fixtures dir",
    )
    p.add_argument(
        "--question",
        default="华东区最近3个月销售趋势",
        help="Natural language question for plan generation",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Override CODEX_TIMEOUT_SECONDS for this run only",
    )
    return p


if __name__ == "__main__":
    parser = build_parser()
    ns = parser.parse_args()
    raise SystemExit(asyncio.run(main_async(ns)))
