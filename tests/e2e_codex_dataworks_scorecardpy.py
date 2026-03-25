#!/usr/bin/env python3
"""
E2E chain: **Codex (NL)** → **sql-generator style .sql** → **dataworks** (Excel + **DuckDB under `.agents/assets/`**)
→ **scorecardpy** (reads DuckDB).

- **Default** uses mocked ODPS that returns a scorecardpy-friendly wide table (same shape as
  ``tests/test_integration_dataworks_to_scorecardpy.py``), so the generated SQL file is only the handoff artifact.
- **``--real-odps``** runs true MaxCompute; you must ensure the SQL result matches scorecardpy columns
  (``entity_id``, ``target``, features) or scorecardpy will fail.

DuckDB lives under ``.agents/assets/`` by default (see ``--duckdb-path``).

Examples::

    uv run python tests/e2e_codex_dataworks_scorecardpy.py
    uv run python tests/e2e_codex_dataworks_scorecardpy.py --mode hint --timeout 180
    uv run python tests/e2e_codex_dataworks_scorecardpy.py --real-odps
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
AGENTS_ASSETS = REPO_ROOT / ".agents" / "assets"


def _make_scorecard_ready_mock_df(n: int = 400, seed: int = 42) -> Any:
    """Same schema as ``_make_mock_df`` in ``test_integration_dataworks_to_scorecardpy`` (smaller default n)."""
    import numpy as np
    import pandas as pd

    rng = np.random.default_rng(seed)
    entity_id = np.arange(n, dtype=int)
    target = (rng.random(n) < 0.25).astype(int)
    feature_num_1 = (target * 2.0 + rng.normal(0, 1.0, n)).astype(float)
    feature_num_2 = (rng.lognormal(mean=1.0 + target * 0.2, sigma=0.5, size=n)).astype(float)
    feature_num_3 = (rng.normal(loc=0.0, scale=1.0, size=n) + target * -0.8).astype(float)
    miss_mask = rng.random(n) < 0.05
    feature_num_3[miss_mask] = np.nan
    cats1 = np.array(["A", "B", "C"], dtype=object)
    cat1 = np.empty(n, dtype=object)
    for i in range(n):
        probs = [0.2, 0.6, 0.2] if target[i] == 1 else [0.5, 0.3, 0.2]
        cat1[i] = rng.choice(cats1, p=probs)
    cats2 = np.array(["X", "Y"], dtype=object)
    cat2 = np.empty(n, dtype=object)
    for i in range(n):
        probs = [0.7, 0.3] if target[i] == 1 else [0.3, 0.7]
        cat2[i] = rng.choice(cats2, p=probs)
    return pd.DataFrame(
        {
            "entity_id": entity_id,
            "target": target,
            "feature_num_1": feature_num_1,
            "feature_num_2": feature_num_2,
            "feature_num_3": feature_num_3,
            "feature_cat_1": cat1,
            "feature_cat_2": cat2,
        }
    )


def _load_simple_case(path: Path) -> tuple[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cid = raw.get("id")
    br = raw.get("business_request")
    if not isinstance(cid, str) or not isinstance(br, str):
        raise SystemExit(f"Invalid case JSON: {path}")
    return cid, br


def normalize_codex_sql_output(text: str) -> str:
    t = (text or "").strip()
    if not t:
        return t
    if not t.startswith("```"):
        return t
    lines = t.splitlines()
    if lines:
        lines = lines[1:]
    while lines and lines[-1].strip() == "```":
        lines = lines[:-1]
    return "\n".join(lines).strip()


def _import_dataworks_module() -> Any:
    path = REPO_ROOT / ".agents/skills/dataworks/scripts/run_sql_export.py"
    spec = importlib.util.spec_from_file_location("dataworks_run_sql_export_e2e_sc", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load dataworks from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_dataworks(
    *,
    sql_path: Path,
    excel_dir: Path,
    duckdb_path: Path,
    duckdb_table: str,
    lifecycle: int,
    mock_odps: bool,
    mock_df: Any,
) -> None:
    mod = _import_dataworks_module()
    if mock_odps:
        mod.resolve_odps_config = lambda _args: (  # type: ignore[method-assign]
            "dummy_id",
            "dummy_key",
            "dummy_project",
            "dummy_endpoint",
        )
        mod.run_odps_sql = lambda *_a, **_k: mock_df.copy()  # type: ignore[method-assign]

    argv = [
        "run_sql_export.py",
        str(sql_path),
        "--save_path",
        str(excel_dir),
        "--duckdb-path",
        str(duckdb_path),
        "--duckdb-table",
        duckdb_table,
        "--lifecycle",
        str(int(lifecycle)),
    ]
    old = sys.argv[:]
    sys.argv = argv
    try:
        mod.main()
    finally:
        sys.argv = old


def _run_dataworks_subprocess(
    sql_path: Path,
    excel_dir: Path,
    duckdb_path: Path,
    duckdb_table: str,
    lifecycle: int,
) -> None:
    script = REPO_ROOT / ".agents/skills/dataworks/scripts/run_sql_export.py"
    cmd = [
        sys.executable,
        str(script),
        str(sql_path),
        "--save_path",
        str(excel_dir),
        "--duckdb-path",
        str(duckdb_path),
        "--duckdb-table",
        duckdb_table,
        "--lifecycle",
        str(int(lifecycle)),
    ]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            f"run_sql_export.py failed (exit {proc.returncode})\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}"
        )


def _run_scorecardpy_and_export(*, db_path: Path, table: str, out_dir: Path, plots_max: int) -> None:
    run_script = REPO_ROOT / ".agents/skills/scorecardpy/scripts/run_scorecardpy.py"
    export_script = REPO_ROOT / ".agents/skills/scorecardpy/scripts/export_breaks.py"

    cmd = [
        sys.executable,
        str(run_script),
        "--db-path",
        str(db_path),
        "--table",
        table,
        "--target",
        "target",
        "--id-col",
        "entity_id",
        "--out-dir",
        str(out_dir),
        "--save-plots",
        "--plots-max",
        str(plots_max),
    ]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            f"run_scorecardpy failed (exit {proc.returncode})\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}"
        )

    bins_pkl = out_dir / "bins.pkl"
    if not bins_pkl.is_file():
        raise SystemExit(f"Missing {bins_pkl}")

    proc2 = subprocess.run(
        [
            sys.executable,
            str(export_script),
            "--bins-pkl",
            str(bins_pkl),
            "--out-dir",
            str(out_dir),
        ],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
    )
    if proc2.returncode != 0:
        raise SystemExit(
            f"export_breaks failed (exit {proc2.returncode})\nSTDERR:\n{proc2.stderr}\nSTDOUT:\n{proc2.stdout}"
        )
    for name in ("breaks_export.json", "selected_variables.json"):
        p = out_dir / name
        if not p.is_file():
            raise SystemExit(f"Missing {p}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--case-json",
        type=Path,
        default=REPO_ROOT / "tests/e2e_simple_case.json",
    )
    p.add_argument("--mode", choices=("raw", "hint"), default="raw")
    p.add_argument("--timeout", type=int, default=180)
    p.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts/e2e_codex_dataworks_scorecardpy",
        help="Codex logs + generated .sql + Excel export",
    )
    p.add_argument(
        "--duckdb-path",
        type=Path,
        default=AGENTS_ASSETS / "e2e_scorecard_chain.duckdb",
        help="DuckDB file under .agents/assets/ by default",
    )
    p.add_argument("--duckdb-table", type=str, default="e2e_scorecard_sample")
    p.add_argument("--lifecycle", type=int, default=30)
    p.add_argument(
        "--score-out-dir",
        type=Path,
        default=None,
        help="scorecardpy output (default: <out-dir>/scorecardpy)",
    )
    p.add_argument("--mock-rows", type=int, default=400, help="Rows in mocked ODPS frame (mock ODPS only)")
    p.add_argument("--plots-max", type=int, default=30)
    p.add_argument(
        "--mock-odps",
        action=argparse.BooleanOptionalAction,
        default=True,
    )
    p.add_argument("--real-odps", action="store_true", help="implies --no-mock-odps")
    p.add_argument("--no-fix-shell-utf8", action="store_true")
    args = p.parse_args()

    if args.real_odps:
        args.mock_odps = False

    AGENTS_ASSETS.mkdir(parents=True, exist_ok=True)

    sys.path.insert(0, str(REPO_ROOT))
    from backend.codex.sql_generator_jsonl_runner import run_sql_generator_json_stream_inline

    case_id, business_request = _load_simple_case(Path(args.case_json))
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[e2e] Codex case={case_id} mode={args.mode}…", flush=True)
    codex_res = run_sql_generator_json_stream_inline(
        repo_root=REPO_ROOT,
        case_id=case_id,
        business_request=business_request,
        mode=args.mode,  # type: ignore[arg-type]
        timeout_s=int(args.timeout),
        out_dir=out_dir,
        fix_shell_utf8=not args.no_fix_shell_utf8,
    )
    if codex_res.returncode != 0:
        print(codex_res.stderr, file=sys.stderr)
        raise SystemExit(f"Codex failed (exit={codex_res.returncode})")

    sql_body = normalize_codex_sql_output(codex_res.last_message)
    if not sql_body:
        raise SystemExit("Codex returned empty last message.")
    sql_path = out_dir / f"{case_id}.sql"
    sql_path.write_text(sql_body + "\n", encoding="utf-8")
    print(f"[e2e] SQL file: {sql_path}", flush=True)

    excel_dir = out_dir / "excel"
    excel_dir.mkdir(parents=True, exist_ok=True)
    db_path = Path(args.duckdb_path).resolve()
    db_path.parent.mkdir(parents=True, exist_ok=True)

    mock_df = _make_scorecard_ready_mock_df(n=max(200, int(args.mock_rows)))

    print(
        f"[e2e] dataworks → Excel + DuckDB `{db_path}` table `{args.duckdb_table}` "
        f"(mock_odps={args.mock_odps})…",
        flush=True,
    )
    if args.mock_odps:
        _run_dataworks(
            sql_path=sql_path,
            excel_dir=excel_dir,
            duckdb_path=db_path,
            duckdb_table=args.duckdb_table,
            lifecycle=args.lifecycle,
            mock_odps=True,
            mock_df=mock_df,
        )
    else:
        _run_dataworks_subprocess(
            sql_path=sql_path,
            excel_dir=excel_dir,
            duckdb_path=db_path,
            duckdb_table=args.duckdb_table,
            lifecycle=args.lifecycle,
        )

    xlsx = excel_dir / f"{sql_path.stem}.xlsx"
    if not xlsx.is_file():
        raise SystemExit(f"Missing Excel: {xlsx}")

    score_out = (
        Path(args.score_out_dir).resolve()
        if args.score_out_dir
        else (out_dir / "scorecardpy")
    )
    score_out.mkdir(parents=True, exist_ok=True)
    print(f"[e2e] scorecardpy → {score_out}…", flush=True)
    _run_scorecardpy_and_export(
        db_path=db_path,
        table=args.duckdb_table,
        out_dir=score_out,
        plots_max=int(args.plots_max),
    )

    print("[e2e] OK", flush=True)
    print(f"  DuckDB:  {db_path}", flush=True)
    print(f"  Table:   {args.duckdb_table}", flush=True)
    print(f"  Excel:   {xlsx}", flush=True)
    print(f"  Scores:  {score_out} (bins.pkl, breaks_export.json, …)", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
