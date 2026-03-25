"""Run regression checks for mock/real Codex modes."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import pandas as pd

from backend.codex.adapter import CodexAdapterError, get_adapter
from backend.codex.mock import MockAdapter
from backend.execution.engine import run_plan


def load_cases(fixtures_dir: Path) -> list[dict]:
    payload = json.loads((fixtures_dir / "cases.json").read_text(encoding="utf-8"))
    return payload


def build_profile(df: pd.DataFrame, filename: str) -> dict:
    return {
        "filename": filename,
        "row_count": int(df.shape[0]),
        "column_count": int(df.shape[1]),
        "columns": [{"name": str(col), "dtype": str(df[col].dtype)} for col in df.columns],
    }


async def run_case(case: dict, fixtures_dir: Path, mode: str) -> dict:
    file_path = fixtures_dir / case["file"]
    df = pd.read_csv(file_path)
    profile = build_profile(df, case["file"])

    if mode == "mock":
        adapter = MockAdapter()
    else:
        adapter = get_adapter()

    ok = True
    parse_success = False
    errors: list[str] = []
    chart_type = ""
    skill_hints: list[str] | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_input_tokens: int | None = None
    try:
        plan = await adapter.generate_plan(
            question=case["question"], schema_profile=profile, task_id=f"reg-{case['name']}"
        )
        parse_success = True
        skill_hints = getattr(adapter, "last_skill_hints", None)
        input_tokens = getattr(adapter, "last_input_tokens", None)
        output_tokens = getattr(adapter, "last_output_tokens", None)
        cached_input_tokens = getattr(adapter, "last_cached_input_tokens", None)
        result = run_plan(df=df, plan=plan)
        chart_type = result.chart.chart_type.value
        if chart_type != case["expected_chart_type"]:
            ok = False
            errors.append(
                f"expected chart={case['expected_chart_type']} got={chart_type}"
            )
    except CodexAdapterError as exc:
        ok = False
        errors.append(f"codex_error: {exc}")
        skill_hints = getattr(adapter, "last_skill_hints", None)
        input_tokens = getattr(adapter, "last_input_tokens", None)
        output_tokens = getattr(adapter, "last_output_tokens", None)
        cached_input_tokens = getattr(adapter, "last_cached_input_tokens", None)
    except Exception as exc:  # pragma: no cover
        ok = False
        errors.append(f"unexpected_error: {exc}")
        skill_hints = getattr(adapter, "last_skill_hints", None)
        input_tokens = getattr(adapter, "last_input_tokens", None)
        output_tokens = getattr(adapter, "last_output_tokens", None)
        cached_input_tokens = getattr(adapter, "last_cached_input_tokens", None)

    return {
        "case": case["name"],
        "mode": mode,
        "ok": ok,
        "parse_success": parse_success,
        "chart_type": chart_type,
        "skill_hints": skill_hints,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "cached_input_tokens": cached_input_tokens,
        "errors": errors,
    }


async def run_all(fixtures_dir: Path, mode: str) -> dict:
    cases = load_cases(fixtures_dir)
    results = []
    for case in cases:
        result = await run_case(case=case, fixtures_dir=fixtures_dir, mode=mode)
        results.append(result)

    passed = sum(1 for item in results if item["ok"])
    parse_passed = sum(1 for item in results if item.get("parse_success"))
    total = len(results)
    token_cases = [
        item for item in results if isinstance(item.get("input_tokens"), int)
    ]
    total_input_tokens = sum(int(item.get("input_tokens") or 0) for item in token_cases)
    total_output_tokens = sum(int(item.get("output_tokens") or 0) for item in token_cases)
    total_cached_input_tokens = sum(
        int(item.get("cached_input_tokens") or 0) for item in token_cases
    )
    report = {
        "mode": mode,
        "passed": passed,
        "parse_passed": parse_passed,
        "total": total,
        "success_rate": round((passed / total) * 100, 2) if total else 0.0,
        "parse_success_rate": round((parse_passed / total) * 100, 2) if total else 0.0,
        "token_summary": {
            "cases_with_usage": len(token_cases),
            "total_input_tokens": total_input_tokens,
            "total_output_tokens": total_output_tokens,
            "total_cached_input_tokens": total_cached_input_tokens,
            "avg_input_tokens_per_case": (
                round(total_input_tokens / len(token_cases), 2) if token_cases else None
            ),
        },
        "results": results,
    }
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run regression suite.")
    parser.add_argument("--mode", choices=["mock", "real"], default="mock")
    parser.add_argument(
        "--fixtures-dir",
        default=str(Path(__file__).resolve().parent / "fixtures"),
    )
    args = parser.parse_args()

    if args.mode == "real":
        os.environ["CODEX_MOCK"] = "false"
    else:
        os.environ["CODEX_MOCK"] = "true"

    report = asyncio.run(run_all(Path(args.fixtures_dir), mode=args.mode))
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

