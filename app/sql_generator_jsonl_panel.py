"""Streamlit panel: run sql-generator Codex JSONL smoke test."""

from __future__ import annotations

import json
import subprocess
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st

from backend.codex import sql_generator_jsonl_runner as jsonl_runner

_STREAM_KEY = "sql_jsonl_stream_result"
_ERROR_KEY = "sql_jsonl_stream_error"
_UI_NONCE_KEY = "sql_jsonl_ui_nonce"


def _repo_root() -> Path:
    return Path(__file__).resolve().parent.parent


def _default_out_dir(repo: Path) -> Path:
    return repo / "artifacts" / "codex_jsonl_streams"


def render_sql_generator_jsonl_panel() -> None:
    SqlGeneratorJsonStreamResult = jsonl_runner.SqlGeneratorJsonStreamResult
    load_cases_dicts = jsonl_runner.load_cases_dicts
    run_sql_generator_json_stream = jsonl_runner.run_sql_generator_json_stream
    run_sql_generator_json_stream_inline = getattr(
        jsonl_runner,
        "run_sql_generator_json_stream_inline",
        None,
    )

    repo = _repo_root()
    cases_path = repo / "tests" / "sql_generator_eval_cases.json"
    e2e_path = repo / "tests" / "e2e_simple_case.json"

    st.markdown(
        "Run **`codex exec --json`** (same CLI as `tests/run_codex_json_stream.py`). "
        "Requires a working **Codex CLI** on the machine that runs Streamlit (not the FastAPI mock). "
        "Full handoff to dataworks + mocked ODPS: `uv run python tests/e2e_codex_sql_to_dataworks.py`. "
        "**Serial two skills** in one Codex run (sql-generator -> sql-export-agent): "
        "`uv run python tests/e2e_codex_two_skills_serial.py`. "
        "**Full chain** (DuckDB under `.agents/assets/` + scorecardpy, scripted steps): "
        "`uv run python tests/e2e_codex_dataworks_scorecardpy.py`. "
        "**One Codex turn** (three skill hints + `tests/full_itegration_case.json`): "
        "`uv run python tests/e2e_codex_full_integration_onego.py`."
    )

    source = st.radio(
        "Case source",
        ("Benchmark (eval suite)", "E2E minimal (short NL)"),
        horizontal=True,
        key="sql_jsonl_case_source",
        help="E2E minimal uses tests/e2e_simple_case.json for faster Codex runs.",
    )

    case_id: str
    use_inline = False
    business_request_inline: str | None = None

    if source.startswith("E2E"):
        if not e2e_path.is_file():
            st.warning(f"E2E case file not found: `{e2e_path}`")
            return
        payload = json.loads(e2e_path.read_text(encoding="utf-8"))
        case_id = str(payload.get("id") or "e2e")
        business_request_inline = str(payload.get("business_request") or "")
        if not business_request_inline.strip():
            st.warning("e2e_simple_case.json has no business_request.")
            return
    else:
        if not cases_path.is_file():
            st.warning(f"Cases file not found: `{cases_path}` (open repo root when running Streamlit).")
            return
        cases = load_cases_dicts(cases_path)
        id_list = [str(c.get("id", "")) for c in cases if c.get("id")]
        if not id_list:
            st.warning("No cases in JSON.")
            return
        case_id = st.selectbox("Case", id_list, key="sql_jsonl_case_id")
        case = next(c for c in cases if c.get("id") == case_id)
        with st.expander("Business request for this case", expanded=False):
            st.text(case.get("business_request", ""))

    if source.startswith("E2E"):
        use_inline = True
        with st.expander("E2E business request", expanded=False):
            st.text(business_request_inline or "")

    c2, c3 = st.columns(2)
    with c2:
        mode = st.radio(
            "Mode",
            ("hint", "raw"),
            horizontal=True,
            key="sql_jsonl_mode",
            help="hint = Skill hint: $sql-generator",
        )
    with c3:
        default_timeout = 180 if use_inline else 300
        timeout_s = st.number_input(
            "Timeout (s)",
            min_value=30,
            value=default_timeout,
            step=30,
            key="sql_jsonl_timeout",
        )

    fix_utf8 = st.checkbox(
        "Fix PowerShell Get-Content UTF-8 (recommended on Windows)",
        value=True,
        key="sql_jsonl_fix_utf8",
    )
    persist = st.checkbox(
        "Also write files under artifacts/codex_jsonl_streams",
        value=True,
        key="sql_jsonl_persist",
        help="Matches CLI default out-dir; disable to only show output in the browser.",
    )

    run = st.button("Run Codex JSONL", type="primary", key="sql_jsonl_run_btn")

    if run:
        st.session_state.pop(_STREAM_KEY, None)
        st.session_state.pop(_ERROR_KEY, None)
        st.session_state[_UI_NONCE_KEY] = int(st.session_state.get(_UI_NONCE_KEY, 0)) + 1
        out_dir = _default_out_dir(repo) if persist else None
        try:
            with st.spinner(f"Running codex (case={case_id}, mode={mode})..."):
                if use_inline and business_request_inline:
                    if run_sql_generator_json_stream_inline is None:
                        raise RuntimeError(
                            "run_sql_generator_json_stream_inline is unavailable in "
                            "backend.codex.sql_generator_jsonl_runner"
                        )
                    result = run_sql_generator_json_stream_inline(
                        repo_root=repo,
                        case_id=case_id,
                        business_request=business_request_inline,
                        mode=mode,  # type: ignore[arg-type]
                        timeout_s=int(timeout_s),
                        out_dir=out_dir,
                        fix_shell_utf8=bool(fix_utf8),
                    )
                else:
                    result = run_sql_generator_json_stream(
                        repo_root=repo,
                        case_id=case_id,
                        mode=mode,  # type: ignore[arg-type]
                        timeout_s=int(timeout_s),
                        out_dir=out_dir,
                        fix_shell_utf8=bool(fix_utf8),
                    )
            st.session_state[_STREAM_KEY] = result
        except subprocess.TimeoutExpired:
            st.session_state[_ERROR_KEY] = f"Timed out after {timeout_s}s."
        except Exception as exc:
            st.session_state[_ERROR_KEY] = str(exc)

    err = st.session_state.get(_ERROR_KEY)
    if isinstance(err, str) and err.strip():
        st.error(err)

    result = st.session_state.get(_STREAM_KEY)
    if not isinstance(result, SqlGeneratorJsonStreamResult):
        return

    if result.returncode != 0:
        st.warning(f"Codex exited with code **{result.returncode}**; check stderr below.")

    m1, m2, m3 = st.columns(3)
    with m1:
        st.metric("Elapsed (s)", f"{result.elapsed_s:.2f}")
    with m2:
        st.metric("Exit code", str(result.returncode))
    with m3:
        if result.jsonl_path:
            st.caption(f"Saved: `{result.jsonl_path.name}`")

    st.subheader("Codex last message (`-o`)")
    if result.last_message.strip():
        st.code(result.last_message, language="sql")
    else:
        st.caption("(empty)")

    st.subheader("JSONL stream (stdout)")
    jtext = result.jsonl_text
    nonce = int(st.session_state.get(_UI_NONCE_KEY, 0))
    if len(jtext) > 1_200_000:
        st.caption("Output very large; use download or on-disk file.")
        st.text_area(
            "jsonl (truncated)",
            value=jtext[:500_000] + "\n\n... [truncated for UI]",
            height=400,
            key=f"sql_jsonl_ta_trunc_{nonce}",
        )
    else:
        st.text_area(
            "jsonl",
            value=jtext,
            height=480,
            key=f"sql_jsonl_ta_{nonce}",
            help="Line-delimited JSON events from `codex exec --json`.",
        )

    st.download_button(
        "Download .jsonl",
        data=jtext.encode("utf-8"),
        file_name=f"codex_exec__{result.case_id}__{result.mode}.jsonl",
        mime="application/x-ndjson",
        key=f"sql_jsonl_dl_{nonce}",
    )

    st.subheader("Event index")
    rows = _jsonl_event_summary(jtext)
    if rows:
        st.dataframe(pd.DataFrame(rows), use_container_width=True, height=min(320, 28 + 24 * len(rows)))

    with st.expander("Stderr"):
        st.code(result.stderr or "(empty)", language="text")

    with st.expander("Inspect one line as JSON", expanded=False):
        line_n = st.number_input(
            "Line number (1-based)",
            min_value=1,
            value=1,
            key="sql_jsonl_inspect_line",
        )
        lines = jtext.splitlines()
        if line_n <= len(lines):
            raw = lines[line_n - 1]
            try:
                st.json(json.loads(raw))
            except json.JSONDecodeError:
                st.code(raw, language="text")
        else:
            st.caption("Line out of range.")


def _jsonl_event_summary(jtext: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for i, line in enumerate(jtext.splitlines(), 1):
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            rows.append({"line": i, "type": "parse_error", "item": "", "note": line[:80]})
            continue
        item = o.get("item")
        item_t = ""
        if isinstance(item, dict):
            item_t = str(item.get("type", ""))
        note = ""
        if isinstance(item, dict) and item.get("type") == "agent_message":
            tx = item.get("text")
            if isinstance(tx, str):
                note = tx[:100] + ("..." if len(tx) > 100 else "")
        rows.append(
            {
                "line": i,
                "type": str(o.get("type", "")),
                "item": item_t,
                "note": note,
            }
        )
    return rows
