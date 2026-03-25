#!/usr/bin/env python3
"""Evaluate `sql-generator` skill effectiveness via Codex CLI.

This test suite runs the same set of business requests in two modes:
1) Skill-hinted: prompt includes `Skill hint: $sql-generator`
2) Raw: no skill hint

For each case, it compares the generated SQL to a "ground truth" SQL file from
`.agents/skills/sql-generator/references/sql代码/` and reports:
- latency (end-to-end, and best-effort phase metrics when available)
- simple structural accuracy metrics (tables, join count, key keywords)

Usage (from repo root):
  uv run python tests/eval_sql_generator_skill.py --mode both

Prerequisites (real run):
  - `codex` CLI on PATH (or set `CODEX_CLI_COMMAND`)
  - `codex login` completed
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import io
import platform
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

# Repo root on sys.path (same pattern as tests/run_regression.py)
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.codex.factory import get_provider
from backend.codex.errors import CodexAdapterError


Mode = Literal["hint", "raw"]


_TABLE_RE = re.compile(r"\b([A-Za-z_][\w$]*\.[A-Za-z_][\w$]*)\b")
_JOIN_RE = re.compile(r"(?i)\b(left\s+join|right\s+join|full\s+join|inner\s+join|cross\s+join|join)\b")


def _read_text(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")


def extract_physical_tables(sql: str) -> set[str]:
    """Extract `db.table`-like tokens used in SQL."""
    return {m.group(1).lower() for m in _TABLE_RE.finditer(sql)}


def extract_join_types(sql: str) -> list[str]:
    return [m.group(1).lower() for m in _JOIN_RE.finditer(sql)]


def keyword_flags(sql: str) -> dict[str, bool]:
    low = sql.lower()
    keys = [
        "with",
        "union all",
        "max_pt",
        "insert overwrite",
        "create table",
        "partition",
        "group by",
        "row_number",
        "qualify",
        "date_add",
        "current_date",
    ]
    return {k: (k in low) for k in keys}


def jaccard(a: set[str], b: set[str]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / float(len(a | b))


def f1(p: float, r: float) -> float:
    if p <= 0 or r <= 0:
        return 0.0
    return 2 * p * r / (p + r)


def score_case(generated_sql: str, truth_sql: str) -> dict[str, Any]:
    gen_tables = extract_physical_tables(generated_sql)
    tru_tables = extract_physical_tables(truth_sql)
    table_j = jaccard(gen_tables, tru_tables)

    gen_joins = extract_join_types(generated_sql)
    tru_joins = extract_join_types(truth_sql)
    join_count_delta = abs(len(gen_joins) - len(tru_joins))

    gen_kw = keyword_flags(generated_sql)
    tru_kw = keyword_flags(truth_sql)
    kw_tp = sum(1 for k, v in gen_kw.items() if v and tru_kw.get(k, False))
    kw_fp = sum(1 for k, v in gen_kw.items() if v and not tru_kw.get(k, False))
    kw_fn = sum(1 for k, v in tru_kw.items() if v and not gen_kw.get(k, False))
    kw_prec = kw_tp / float(kw_tp + kw_fp) if (kw_tp + kw_fp) else 1.0
    kw_rec = kw_tp / float(kw_tp + kw_fn) if (kw_tp + kw_fn) else 1.0
    kw_f1 = f1(kw_prec, kw_rec)

    # Heuristic overall: tables matter most; keywords approximate "shape".
    overall = 0.65 * table_j + 0.30 * kw_f1 + 0.05 * max(0.0, 1.0 - (join_count_delta / 20.0))

    return {
        "table_jaccard": round(table_j, 4),
        "generated_table_count": len(gen_tables),
        "truth_table_count": len(tru_tables),
        "join_count_generated": len(gen_joins),
        "join_count_truth": len(tru_joins),
        "join_count_delta": join_count_delta,
        "keyword_f1": round(kw_f1, 4),
        "overall_score": round(overall, 4),
    }


def build_prompt(*, business_request: str, mode: Mode) -> str:
    """Build a minimal prompt that forces SQL-only output."""
    hint_line = "Skill hint: $sql-generator\n\n" if mode == "hint" else ""
    return (
        "You are a senior data analyst writing ODPS SQL.\n"
        f"{hint_line}"
        "CRITICAL OUTPUT RULES:\n"
        "- Output ONLY the SQL script.\n"
        "- No markdown, no code fences, no explanations.\n"
        "- Use ODPS-compatible SQL style.\n"
        "- Use placeholders like ${bizdate} when date partition is required.\n"
        "- If you need MAX_PT(...) per local convention, include it.\n"
        "\n"
        "Business request (written by a stakeholder):\n"
        f"{business_request.strip()}\n"
    ).strip()


@dataclass(frozen=True)
class Case:
    id: str
    difficulty: str
    truth_path: str
    business_request: str


def load_cases(repo_root: Path, cases_path: Path) -> list[Case]:
    payload = json.loads(_read_text(cases_path))
    out: list[Case] = []
    for item in payload:
        out.append(
            Case(
                id=str(item["id"]),
                difficulty=str(item.get("difficulty", "unknown")),
                truth_path=str(item["truth_path"]),
                business_request=str(item["business_request"]),
            )
        )
    # Ensure truth files exist.
    for c in out:
        p = repo_root / c.truth_path
        if not p.is_file():
            raise FileNotFoundError(f"truth_path not found: {c.truth_path}")
    return out


async def run_one(
    *,
    provider: Any,
    repo_root: Path,
    case: Case,
    mode: Mode,
    timeout_s: int | None,
) -> dict[str, Any]:
    if timeout_s is not None and hasattr(provider, "timeout_seconds"):
        provider.timeout_seconds = int(timeout_s)

    prompt = build_prompt(business_request=case.business_request, mode=mode)
    truth_sql = _read_text(repo_root / case.truth_path)

    # Configure Codex CLI behavior per-run via env vars (process-wide provider).
    if args_model := os.getenv("CODEX_MODEL"):
        pass  # external override

    # Mock provider path: keep the suite runnable offline, but clearly mark
    # that no real Codex execution occurred (latency/usage are meaningless).
    if provider.__class__.__name__ == "MockProvider":
        return {
            "case_id": case.id,
            "difficulty": case.difficulty,
            "mode": mode,
            "elapsed_s": 0.0,
            "provider_exec_elapsed_s": None,
            "provider_ttft_elapsed_s": None,
            "provider_generation_elapsed_s": None,
            "usage": {},
            "score": score_case(truth_sql, truth_sql),
            "generated_sql": truth_sql.strip(),
            "note": "mock_provider_returned_truth_sql",
        }

    started = time.perf_counter()
    # We intentionally use the "legacy" provider private API because this suite
    # is explicitly evaluating `codex exec` behavior + skill hints.
    try:
        # Persist JSONL event stream for this run when enabled.
        jsonl_dir = os.getenv("CODEX_JSONL_OUT_DIR", "").strip()
        if jsonl_dir:
            safe_tag = f"{case.id}__{mode}"
            os.environ["CODEX_JSONL_TAG"] = safe_tag
        raw, usage = await provider._run_prompt_with_usage(prompt)  # type: ignore[attr-defined]
        elapsed_s = time.perf_counter() - started
        gen_sql = raw.strip()
    except CodexAdapterError as exc:
        elapsed_s = time.perf_counter() - started
        return {
            "case_id": case.id,
            "difficulty": case.difficulty,
            "mode": mode,
            "elapsed_s": round(elapsed_s, 3),
            "error": str(exc),
            "hint": (
                "If you see auth/config errors like `unknown variant enterprise_sso`, "
                "your PATH `codex` is likely the wrong CLI. Set `CODEX_CLI_COMMAND` to the "
                "Xinfei enterprise `codex.exe` and re-run (see backend/codex/xinfei_sso.py)."
            ),
        }

    return {
        "case_id": case.id,
        "difficulty": case.difficulty,
        "mode": mode,
        "elapsed_s": round(elapsed_s, 3),
        "provider_exec_elapsed_s": getattr(provider, "last_exec_elapsed_s", None),
        "provider_ttft_elapsed_s": getattr(provider, "last_ttft_elapsed_s", None),
        "provider_generation_elapsed_s": getattr(provider, "last_generation_elapsed_s", None),
        "usage": usage or {},
        "score": score_case(gen_sql, truth_sql),
        "generated_sql": gen_sql,
    }


async def main_async(args: argparse.Namespace) -> int:
    repo_root = Path(__file__).resolve().parent.parent
    cases_path = repo_root / args.cases
    cases = load_cases(repo_root, cases_path)
    if args.case_id:
        wanted = set(args.case_id)
        cases = [c for c in cases if c.id in wanted]
        missing = wanted - {c.id for c in cases}
        if missing:
            raise SystemExit(f"Unknown --case-id: {sorted(missing)}")

    if args.use_mock:
        os.environ["CODEX_MOCK"] = "true"
    else:
        os.environ["CODEX_MOCK"] = "false"

    if args.model:
        os.environ["CODEX_MODEL"] = args.model
    if args.reasoning_effort:
        os.environ["CODEX_REASONING_EFFORT"] = args.reasoning_effort
    os.environ["CODEX_USE_JSON_EVENTS"] = "true" if args.json_events else "false"
    if args.jsonl_dir:
        os.environ["CODEX_JSONL_OUT_DIR"] = str((repo_root / args.jsonl_dir).resolve())
        os.environ["CODEX_JSONL_REPO_ROOT"] = str(repo_root.resolve())

    # On Windows, the async JSONL reader path in the legacy provider can hit the
    # StreamReader line-length limit if the CLI emits very large JSON events.
    # Prefer the proven sync subprocess path for stability in eval runs.
    if platform.system().lower().startswith("win"):
        os.environ.setdefault("CODEX_ASYNC_SUBPROCESS", "false")

    provider = get_provider(use_mock=args.use_mock)

    modes: list[Mode]
    if args.mode == "both":
        modes = ["raw", "hint"]
    else:
        modes = [args.mode]

    results: list[dict[str, Any]] = []
    for case in cases:
        for mode in modes:
            results.append(
                await run_one(
                    provider=provider,
                    repo_root=repo_root,
                    case=case,
                    mode=mode,
                    timeout_s=args.timeout,
                )
            )

    # Aggregate
    by_mode: dict[str, list[dict[str, Any]]] = {"raw": [], "hint": []}
    for r in results:
        by_mode[r["mode"]].append(r)

    def _avg(nums: list[float]) -> float:
        return sum(nums) / float(len(nums)) if nums else 0.0

    summary = {}
    for m in modes:
        rs = by_mode[m]
        ok = [x for x in rs if isinstance(x.get("score"), dict)]
        err = [x for x in rs if "error" in x]
        summary[m] = {
            "case_count": len(rs),
            "ok_count": len(ok),
            "error_count": len(err),
            "avg_elapsed_s": round(_avg([float(x["elapsed_s"]) for x in rs]), 3),
            "avg_overall_score": round(
                _avg([float(x["score"]["overall_score"]) for x in ok]), 4
            ),
            "avg_table_jaccard": round(
                _avg([float(x["score"]["table_jaccard"]) for x in ok]), 4
            ),
            "avg_keyword_f1": round(_avg([float(x["score"]["keyword_f1"]) for x in ok]), 4),
        }

    report = {
        "meta": {
            "cases_path": str(args.cases),
            "mode": args.mode,
            "use_mock": bool(args.use_mock),
            "timeout_s": args.timeout,
        },
        "summary": summary,
        "results": results,
    }

    out = json.dumps(report, ensure_ascii=False, indent=2)
    if args.output:
        (repo_root / args.output).write_text(out + "\n", encoding="utf-8")
    # Windows terminals may default to GBK; ensure UTF-8 output to avoid crashes
    # when the report contains non-ASCII (Chinese) text.
    try:
        sys.stdout.reconfigure(encoding="utf-8")  # type: ignore[attr-defined]
    except Exception:
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    print(out)
    return 0


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--cases",
        default="tests/sql_generator_eval_cases.json",
        help="Path to evaluation cases JSON (relative to repo root)",
    )
    p.add_argument(
        "--mode",
        choices=["hint", "raw", "both"],
        default="both",
        help="Run skill-hinted vs raw prompts",
    )
    p.add_argument(
        "--case-id",
        action="append",
        default=[],
        help="Run only specific case id(s). Repeatable.",
    )
    p.add_argument(
        "--timeout",
        type=int,
        default=None,
        help="Override CODEX_TIMEOUT_SECONDS for this run only",
    )
    p.add_argument(
        "--model",
        default="",
        help="Codex model override (sets CODEX_MODEL)",
    )
    p.add_argument(
        "--reasoning-effort",
        default="",
        help="Reasoning effort override (sets CODEX_REASONING_EFFORT), e.g. low",
    )
    p.add_argument(
        "--json-events",
        action="store_true",
        help="Enable codex exec --json event stream (usage + timings).",
    )
    p.add_argument(
        "--jsonl-dir",
        default="artifacts/sql_generator_eval_jsonl",
        help="Directory to write per-run codex JSONL streams (relative to repo root).",
    )
    p.add_argument(
        "--use-mock",
        action="store_true",
        help="Use the mock provider (no Codex CLI calls).",
    )
    p.add_argument(
        "--output",
        default="",
        help="Optional output path (relative to repo root) to write JSON report.",
    )
    return p


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main_async(build_parser().parse_args())))

