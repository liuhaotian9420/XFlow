#!/usr/bin/env python3
"""
**One Codex session** (``codex exec --json``) to orchestrate:

  ``$sql-generator`` → ``$sql-export-agent`` → ``$scorecardpy-duckdb-large-scale-scorecard``

using the **fixed path layout** in :mod:`backend.codex.full_integration_chain` (DuckDB under
``.agents/assets/``, SQL/Excel/scorecardpy under ``artifacts/full_integration_onego/``).

Default business request JSON: ``tests/full_itegration_case.json`` (filename spelling as in repo).

This script **only invokes Codex** and writes artifacts + a heuristic report. It does **not** re-run
dataworks/scorecardpy in Python after Codex (the agent should do that inside the same turn).

Examples::

    uv run python tests/e2e_codex_full_integration_onego.py
    uv run python tests/e2e_codex_full_integration_onego.py --timeout 900 --strict
    uv run python tests/e2e_codex_full_integration_onego.py --verify-after

``--verify-after`` checks that DuckDB + scorecardpy outputs exist at the **expected paths**
(Codex must have executed the commands successfully).
"""

from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

DEFAULT_CASE = REPO_ROOT / "tests" / "full_itegration_case.json"

_SQL_FENCE_RE = re.compile(r"```sql\s*\n(.*?)\n```", re.IGNORECASE | re.DOTALL)


def _log(msg: str, *, file=sys.stdout) -> None:
    """Print one line prefixed with a local timezone-aware ISO timestamp."""
    ts = datetime.now().astimezone().isoformat(timespec="seconds")
    print(f"[{ts}] {msg}", file=file, flush=True)


def _load_case(path: Path) -> tuple[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cid = raw.get("id")
    br = raw.get("business_request")
    if not isinstance(cid, str) or not isinstance(br, str):
        raise SystemExit(f"Invalid case JSON: {path}")
    return cid, br


def _extract_sql_from_last_message(last_message: str) -> str | None:
    """
    Best-effort extraction of a SQL script from Codex's last message.

    We intentionally accept SQL fenced blocks (```sql ... ```) since Codex may be blocked from
    writing files in its sandbox and will paste SQL into the response instead.
    """
    m = _SQL_FENCE_RE.search(last_message or "")
    if not m:
        return None
    sql = (m.group(1) or "").strip()
    return sql or None


def _run_step2_dataworks_export(*, sql_path: Path, excel_dir: Path, duckdb_path: Path, duckdb_table: str) -> None:
    cmd = [
        sys.executable,
        ".agents/skills/dataworks/scripts/run_sql_export.py",
        str(sql_path),
        "--save_path",
        str(excel_dir),
        "--duckdb-path",
        str(duckdb_path),
        "--duckdb-table",
        str(duckdb_table),
        "--lifecycle",
        "30",
    ]
    subprocess.run(cmd, cwd=str(REPO_ROOT), check=True)


def _run_step3_scorecardpy(*, duckdb_path: Path, duckdb_table: str, score_out: Path) -> None:
    cmd1 = [
        sys.executable,
        ".agents/skills/scorecardpy/scripts/run_scorecardpy.py",
        "--db-path",
        str(duckdb_path),
        "--table",
        str(duckdb_table),
        "--target",
        "target",
        "--id-col",
        "entity_id",
        "--out-dir",
        str(score_out),
        "--save-plots",
        "--plots-max",
        "30",
    ]
    subprocess.run(cmd1, cwd=str(REPO_ROOT), check=True)

    cmd2 = [
        sys.executable,
        ".agents/skills/scorecardpy/scripts/export_breaks.py",
        "--bins-pkl",
        str(score_out / "bins.pkl"),
        "--out-dir",
        str(score_out),
    ]
    subprocess.run(cmd2, cwd=str(REPO_ROOT), check=True)


def _verify_artifacts(layout_resolved: dict[str, Path], duck_table: str) -> tuple[bool, list[str]]:
    ok = True
    notes: list[str] = []
    db = layout_resolved["duckdb"]
    if not db.is_file():
        ok = False
        notes.append(f"Missing DuckDB file: {db}")
        return ok, notes
    try:
        import duckdb  # type: ignore

        con = duckdb.connect(str(db))
        try:
            rows = con.execute(
                f'SELECT COUNT(*) FROM "{duck_table}"',
            ).fetchone()
            cnt = int(rows[0]) if rows else 0
            notes.append(f"DuckDB table {duck_table!r} row_count={cnt}")
            if cnt == 0:
                ok = False
                notes.append("Table is empty.")
        except Exception as exc:
            ok = False
            notes.append(f"DuckDB read failed: {exc}")
        finally:
            con.close()
    except ImportError:
        notes.append("duckdb not installed; skipped row count.")

    score = layout_resolved["score_out"]
    for name in ("bins.pkl", "breaks_export.json", "selected_variables.json"):
        p = score / name
        if not p.is_file():
            ok = False
            notes.append(f"Missing scorecard artifact: {p}")
        else:
            notes.append(f"OK {p.name}")

    return ok, notes


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case-json", type=Path, default=DEFAULT_CASE)
    parser.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts/codex_full_integration_onego",
        help="Codex JSONL + stderr + report",
    )
    parser.add_argument("--timeout", type=int, default=900)
    parser.add_argument("--no-fix-shell-utf8", action="store_true")
    parser.add_argument(
        "--codex-sandbox",
        default="workspace-write",
        help="Codex CLI sandbox mode (read-only/workspace-write/danger-full-access)",
    )
    parser.add_argument(
        "--codex-approvals",
        default="never",
        help="Codex CLI approval policy (untrusted/on-request/never)",
    )
    parser.add_argument(
        "--codex-bypass-sandbox",
        action="store_true",
        help="Use Codex `--dangerously-bypass-approvals-and-sandbox` (EXTREMELY DANGEROUS).",
    )
    parser.add_argument(
        "--codex-disable-mcp",
        action="store_true",
        default=True,
        help=(
            "Disable external MCP servers (notion/linear/figma) to avoid OAuth stalls "
            "during unattended E2E runs. Enabled by default."
        ),
    )
    parser.add_argument(
        "--codex-enable-mcp",
        action="store_true",
        help="Override and keep MCP servers enabled.",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 if JSONL heuristics do not look like a full three-skill chain",
    )
    parser.add_argument(
        "--verify-after",
        action="store_true",
        help="After Codex, verify DuckDB + scorecardpy files at the layout paths",
    )
    parser.add_argument(
        "--host-exec-after",
        action="store_true",
        help="If Codex is blocked from running commands, execute Step2/3 on host after Codex using extracted SQL.",
    )
    args = parser.parse_args()

    sys.path.insert(0, str(REPO_ROOT))
    from backend.codex.full_integration_chain import (
        FullIntegrationLayout,
        analyze_full_integration_onego_jsonl,
        build_full_integration_onego_prompt,
    )
    from backend.codex.sql_generator_jsonl_runner import run_codex_json_stream_raw_prompt

    layout = FullIntegrationLayout.default_layout()
    paths = layout.resolve(REPO_ROOT)
    paths["sql_workdir"].mkdir(parents=True, exist_ok=True)
    paths["excel_dir"].mkdir(parents=True, exist_ok=True)
    paths["duckdb"].parent.mkdir(parents=True, exist_ok=True)
    paths["score_out"].mkdir(parents=True, exist_ok=True)

    case_id, business_request = _load_case(Path(args.case_json))
    prompt = build_full_integration_onego_prompt(business_request=business_request, layout=layout)
    disable_mcp = bool(args.codex_disable_mcp and not args.codex_enable_mcp)
    codex_config_overrides: list[str] = []
    if disable_mcp:
        codex_config_overrides = [
            "mcp_servers.notion.enabled=false",
            "mcp_servers.linear.enabled=false",
            "mcp_servers.figma.enabled=false",
        ]

    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    _log(f"[one-go] case={case_id} → starting Codex (timeout={args.timeout}s)")
    res = run_codex_json_stream_raw_prompt(
        repo_root=REPO_ROOT,
        run_id=case_id,
        prompt=prompt,
        mode="raw",
        timeout_s=int(args.timeout),
        out_dir=out_dir,
        fix_shell_utf8=not args.no_fix_shell_utf8,
        sandbox_mode=str(args.codex_sandbox or "").strip() or None,
        approval_policy=str(args.codex_approvals or "").strip() or None,
        bypass_sandbox=bool(args.codex_bypass_sandbox),
        codex_config_overrides=codex_config_overrides,
    )
    _log(
        f"[one-go] Codex finished (exit={res.returncode}, elapsed_s={res.elapsed_s:.1f})",
    )

    ev = analyze_full_integration_onego_jsonl(res.jsonl_text)
    report = {
        "case_id": case_id,
        "codex_exit": res.returncode,
        "elapsed_s": res.elapsed_s,
        "codex_argv": getattr(res, "argv", None),
        "codex_config_overrides": codex_config_overrides,
        "layout": {
            "duckdb_path_rel": layout.duckdb_path_rel,
            "duckdb_table": layout.duckdb_table,
            "score_out_rel": layout.score_out_rel,
        },
        "evidence": {
            "event_lines": ev.event_lines,
            "mentions_sql_generator": ev.mentions_sql_generator,
            "mentions_dataworks": ev.mentions_dataworks,
            "mentions_scorecardpy": ev.mentions_scorecardpy,
            "cmd_sql_generator_tree": ev.cmd_sql_generator_tree,
            "cmd_dataworks_export": ev.cmd_dataworks_export,
            "cmd_scorecardpy": ev.cmd_scorecardpy,
            "order_sg_dw_sc_ok": ev.order_sg_dw_sc_ok,
            "looks_like_full_chain": ev.looks_like_full_chain,
        },
        "artifacts": {
            "jsonl": str(res.jsonl_path) if res.jsonl_path else None,
            "last_message": str(res.last_message_path) if res.last_message_path else None,
        },
    }

    if res.returncode != 0:
        _log("[one-go] Codex stderr:", file=sys.stderr)
        print(res.stderr, file=sys.stderr)

    report_path = out_dir / f"{case_id}_onego_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    _log("[one-go] evidence (JSON):")
    print(json.dumps(report["evidence"], ensure_ascii=False, indent=2), flush=True)
    _log(f"[one-go] Report written: {report_path}")

    verify_ok = True
    verify_notes: list[str] = []
    if args.verify_after:
        _log("[one-go] Verifying artifacts…")
        verify_ok, verify_notes = _verify_artifacts(paths, layout.duckdb_table)
        if args.host_exec_after and not verify_ok:
            sql_path_guess = None
            extracted = _extract_sql_from_last_message(res.last_message)
            if extracted:
                # Prefer writing into the stable layout folder with a predictable filename.
                sql_path_guess = paths["sql_workdir"] / "full_integration_onego_extracted.sql"
                sql_path_guess.write_text(extracted, encoding="utf-8", newline="\n")
                try:
                    _log("[host-exec] Step 2: run_sql_export.py …")
                    _run_step2_dataworks_export(
                        sql_path=sql_path_guess,
                        excel_dir=paths["excel_dir"],
                        duckdb_path=paths["duckdb"],
                        duckdb_table=layout.duckdb_table,
                    )
                    _log("[host-exec] Step 3: run_scorecardpy.py + export_breaks.py …")
                    _run_step3_scorecardpy(
                        duckdb_path=paths["duckdb"],
                        duckdb_table=layout.duckdb_table,
                        score_out=paths["score_out"],
                    )
                except subprocess.CalledProcessError as exc:
                    verify_notes.append(f"[host-exec] failed: {exc}")
                else:
                    verify_ok, verify_notes = _verify_artifacts(paths, layout.duckdb_table)
                    if verify_ok:
                        verify_notes.append(f"[host-exec] OK (sql_path={sql_path_guess})")
            else:
                verify_notes.append("[host-exec] no ```sql fenced block``` found in Codex last message; cannot proceed.")
        report["verify"] = {"ok": verify_ok, "notes": verify_notes}
        report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
        for line in verify_notes:
            _log(f"  [verify] {line}")

    msg = res.last_message.strip()
    _log("--- last message (excerpt) ---")
    print((msg[:3000] + "\n…") if len(msg) > 3000 else msg or "(empty)", flush=True)

    if res.returncode != 0:
        return int(res.returncode if res.returncode <= 125 else 125)
    if args.strict and not ev.looks_like_full_chain:
        _log(
            "[strict] Heuristic: expected sql-generator → dataworks → scorecardpy in JSONL.",
            file=sys.stderr,
        )
        return 2
    if args.verify_after and not verify_ok:
        _log("[verify] Artifacts missing or empty.", file=sys.stderr)
        return 3

    _log("[one-go] OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
