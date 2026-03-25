#!/usr/bin/env python3
"""
End-to-end: natural language (minimal case) → Codex → save ``.sql`` → dataworks export.

Uses ``tests/e2e_simple_case.json`` so the model request stays short for faster runs.

**Codex** must be available locally (same as ``tests/run_codex_json_stream.py``).

ODPS behavior:
- Default ``--mock-odps``: patches ``run_sql_export.py`` so no real MaxCompute call; still runs
  Excel (and optional DuckDB) logic — proves the handoff path.
- With ``--real-odps``: runs ``run_sql_export.py`` as a subprocess; requires ODPS env vars.

Examples::

    uv run python tests/e2e_codex_sql_to_dataworks.py
    uv run python tests/e2e_codex_sql_to_dataworks.py --mode hint --timeout 120
    uv run python tests/e2e_codex_sql_to_dataworks.py --real-odps --save-path ./files
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


def _load_simple_case(path: Path) -> tuple[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cid = raw.get("id")
    br = raw.get("business_request")
    if not isinstance(cid, str) or not isinstance(br, str):
        raise SystemExit(f"Invalid E2E case JSON: {path}")
    return cid, br


def normalize_codex_sql_output(text: str) -> str:
    """Strip optional markdown fences if the model ignores output rules."""
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
    spec = importlib.util.spec_from_file_location("dataworks_run_sql_export_e2e", str(path))
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Failed to load dataworks from {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _run_dataworks_mocked(sql_path: Path, save_path: Path, duckdb_args: list[str]) -> None:
    import pandas as pd

    mod = _import_dataworks_module()
    mock_df = pd.DataFrame(
        {
            "id": [1],
            "label": ["ok"],
        }
    )
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
        str(save_path),
        *duckdb_args,
    ]
    old = sys.argv[:]
    sys.argv = argv
    try:
        mod.main()
    finally:
        sys.argv = old


def _run_dataworks_subprocess(sql_path: Path, save_path: Path, duckdb_args: list[str]) -> None:
    script = REPO_ROOT / ".agents/skills/dataworks/scripts/run_sql_export.py"
    cmd = [
        sys.executable,
        str(script),
        str(sql_path),
        "--save_path",
        str(save_path),
        *duckdb_args,
    ]
    proc = subprocess.run(cmd, cwd=str(REPO_ROOT), capture_output=True, text=True)
    if proc.returncode != 0:
        raise SystemExit(
            f"run_sql_export.py failed (exit {proc.returncode})\nSTDERR:\n{proc.stderr}\nSTDOUT:\n{proc.stdout}"
        )


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--case-json",
        type=Path,
        default=REPO_ROOT / "tests/e2e_simple_case.json",
        help="Path to NL case JSON (id + business_request)",
    )
    p.add_argument("--mode", choices=("raw", "hint"), default="raw")
    p.add_argument("--timeout", type=int, default=180, help="Codex subprocess timeout seconds")
    p.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts/e2e_sql_generator_dataworks",
        help="Directory for Codex JSONL + generated .sql + Excel",
    )
    p.add_argument(
        "--save-path",
        type=Path,
        default=None,
        help="Directory for Excel output (default: <out-dir>/excel)",
    )
    p.add_argument(
        "--mock-odps",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="Patch ODPS inside run_sql_export (default: true)",
    )
    p.add_argument(
        "--real-odps",
        action="store_true",
        help="Shorthand: run real run_sql_export.py (implies --no-mock-odps)",
    )
    p.add_argument("--duckdb-path", type=Path, default=None, help="If set, pass --duckdb-path")
    p.add_argument("--duckdb-table", type=str, default=None, help="If set, pass --duckdb-table")
    p.add_argument("--lifecycle", type=int, default=7, help="DuckDB lifecycle days")
    p.add_argument("--no-fix-shell-utf8", action="store_true", help="Disable JSONL UTF-8 repair")
    args = p.parse_args()

    if args.real_odps:
        args.mock_odps = False

    sys.path.insert(0, str(REPO_ROOT))
    from backend.codex.sql_generator_jsonl_runner import run_sql_generator_json_stream_inline

    case_id, business_request = _load_simple_case(Path(args.case_json))

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[e2e] Codex case={case_id} mode={args.mode} (timeout={args.timeout}s)…", flush=True)
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
        raise SystemExit(f"Codex failed with exit code {codex_res.returncode}")

    sql_body = normalize_codex_sql_output(codex_res.last_message)
    if not sql_body:
        raise SystemExit("Codex returned an empty last message; check JSONL in out-dir.")
    sql_path = out_dir / f"{case_id}.sql"
    sql_path.write_text(sql_body + "\n", encoding="utf-8")
    print(f"[e2e] Wrote SQL: {sql_path}", flush=True)

    excel_dir = Path(args.save_path).resolve() if args.save_path else (out_dir / "excel")
    excel_dir.mkdir(parents=True, exist_ok=True)

    duck_parts: list[str] = []
    if args.duckdb_path is not None and args.duckdb_table:
        duck_parts.extend(
            [
                "--duckdb-path",
                str(Path(args.duckdb_path).resolve()),
                "--duckdb-table",
                str(args.duckdb_table),
                "--lifecycle",
                str(int(args.lifecycle)),
            ]
        )
    elif args.duckdb_path is not None or args.duckdb_table:
        raise SystemExit("Use both --duckdb-path and --duckdb-table or neither.")

    print(
        f"[e2e] Dataworks (mock_odps={args.mock_odps}) → Excel under {excel_dir}…",
        flush=True,
    )
    if args.mock_odps:
        _run_dataworks_mocked(sql_path, excel_dir, duck_parts)
    else:
        _run_dataworks_subprocess(sql_path, excel_dir, duck_parts)

    xlsx = excel_dir / f"{sql_path.stem}.xlsx"
    if not xlsx.is_file():
        candidates = list(excel_dir.glob("*.xlsx"))
        raise SystemExit(f"Expected Excel at {xlsx}; found {candidates!r}")
    print(f"[e2e] OK — Excel: {xlsx}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
