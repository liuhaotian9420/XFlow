"""Run regression checks for mock/real Codex modes."""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from pathlib import Path

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
    errors: list[str] = []
    chart_type = ""
    try:
        plan = await adapter.generate_plan(
            question=case["question"], schema_profile=profile, task_id=f"reg-{case['name']}"
        )
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
    except Exception as exc:  # pragma: no cover
        ok = False
        errors.append(f"unexpected_error: {exc}")

    return {"case": case["name"], "mode": mode, "ok": ok, "chart_type": chart_type, "errors": errors}


async def run_all(fixtures_dir: Path, mode: str) -> dict:
    cases = load_cases(fixtures_dir)
    results = []
    for case in cases:
        result = await run_case(case=case, fixtures_dir=fixtures_dir, mode=mode)
        results.append(result)

    passed = sum(1 for item in results if item["ok"])
    total = len(results)
    report = {
        "mode": mode,
        "passed": passed,
        "total": total,
        "success_rate": round((passed / total) * 100, 2) if total else 0.0,
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

