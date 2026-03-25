#!/usr/bin/env python3
"""
E2E-style harness: **one** ``codex exec --json`` session with **two** skill hints in **serial** order:

1. ``$sql-generator`` — write one ``.sql`` under ``artifacts/two_skill_chain/``
2. ``$sql-export-agent`` — emit the ``run_sql_export.py`` command for that file

This does **not** enforce that Codex actually loaded both skill packages; use the printed **evidence**
and saved JSONL to inspect behavior.

Usage::

    uv run python tests/e2e_codex_two_skills_serial.py
    uv run python tests/e2e_codex_two_skills_serial.py --timeout 240 --strict

``--strict`` exits non-zero if JSONL heuristics say the run did not look like a serial two-skill flow.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


def _load_case(path: Path) -> tuple[str, str]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    cid = raw.get("id")
    br = raw.get("business_request")
    if not isinstance(cid, str) or not isinstance(br, str):
        raise SystemExit(f"Invalid case JSON: {path}")
    return cid, br


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument(
        "--case-json",
        type=Path,
        default=REPO_ROOT / "tests/two_skill_serial_case.json",
    )
    p.add_argument(
        "--out-dir",
        type=Path,
        default=REPO_ROOT / "artifacts/codex_two_skill_serial",
        help="Codex JSONL + last message + stderr",
    )
    p.add_argument("--timeout", type=int, default=300)
    p.add_argument("--no-fix-shell-utf8", action="store_true")
    p.add_argument(
        "--strict",
        action="store_true",
        help="Exit 2 if heuristic two-skill serial evidence fails",
    )
    args = p.parse_args()

    sys.path.insert(0, str(REPO_ROOT))
    from backend.codex.sql_generator_jsonl_runner import run_codex_json_stream_raw_prompt
    from backend.codex.two_skill_chain import (
        analyze_two_skill_serial_jsonl,
        build_serial_two_skill_prompt,
    )

    case_id, business_request = _load_case(Path(args.case_json))
    prompt = build_serial_two_skill_prompt(business_request=business_request)
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"[two-skill] case={case_id} → Codex (timeout={args.timeout}s)…", flush=True)
    res = run_codex_json_stream_raw_prompt(
        repo_root=REPO_ROOT,
        run_id=case_id,
        prompt=prompt,
        mode="raw",
        timeout_s=int(args.timeout),
        out_dir=out_dir,
        fix_shell_utf8=not args.no_fix_shell_utf8,
    )
    if res.returncode != 0:
        print(res.stderr, file=sys.stderr)
        raise SystemExit(f"Codex failed (exit={res.returncode})")

    ev = analyze_two_skill_serial_jsonl(res.jsonl_text)
    report = {
        "case_id": case_id,
        "codex_exit": res.returncode,
        "elapsed_s": res.elapsed_s,
        "evidence": {
            "event_lines": ev.event_lines,
            "mentions_sql_generator_hint": ev.mentions_sql_generator_hint,
            "mentions_sql_export_or_dataworks": ev.mentions_sql_export_or_dataworks,
            "command_touches_sql_generator_tree": ev.command_touches_sql_generator_tree,
            "command_touches_dataworks_run_sql_export": ev.command_touches_dataworks_run_sql_export,
            "step1_before_step2_order_ok": ev.step1_before_step2_order_ok,
            "looks_like_serial_two_skill": ev.looks_like_serial_two_skill,
        },
        "artifacts": {
            "jsonl": str(res.jsonl_path) if res.jsonl_path else None,
            "last_message": str(res.last_message_path) if res.last_message_path else None,
        },
    }
    report_path = out_dir / f"{case_id}_two_skill_report.json"
    report_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report["evidence"], ensure_ascii=False, indent=2), flush=True)
    print(f"[two-skill] Report: {report_path}", flush=True)
    print("\n--- last message (excerpt) ---", flush=True)
    msg = res.last_message.strip()
    print((msg[:2000] + "\n…") if len(msg) > 2000 else msg or "(empty)", flush=True)

    if args.strict and not ev.looks_like_serial_two_skill:
        print(
            "\n[strict] Heuristic failed: expected both skill areas with step1 ≤ step2 ordering in JSONL.",
            file=sys.stderr,
        )
        return 2
    print("[two-skill] OK", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
