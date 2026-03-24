from __future__ import annotations

import io
import json
import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="xyf-competition-mvp", layout="wide")
st.title("xyf-competition-mvp")
st.caption(
    "Default: **chat** with the assistant about your data. Type **`/task`** + your question to generate a "
    "structured plan, review or revise it, confirm to run, then mark the task complete."
)


def _default_use_codex_mock() -> bool:
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("file_meta", None)
    st.session_state.setdefault("task_history", [])
    st.session_state.setdefault("_followup_q", None)
    st.session_state.setdefault("mode", "chat")  # "chat" | "task"
    st.session_state.setdefault("active_task_id", None)
    st.session_state.setdefault("schema_profile", None)
    st.session_state.setdefault("schema_profile_for", None)
    if "use_codex_mock" not in st.session_state:
        st.session_state.use_codex_mock = _default_use_codex_mock()


def _invalidate_schema_cache() -> None:
    """Clear cached schema when the uploaded file changes or is removed."""
    st.session_state.pop("schema_profile", None)
    st.session_state.pop("schema_profile_for", None)


def _ensure_schema_profile() -> dict | None:
    """Fetch and cache schema profile for the active upload (for /chat context)."""
    meta = st.session_state.file_meta
    if not meta:
        return None
    name = meta["name"]
    if (
        st.session_state.get("schema_profile_for") == name
        and st.session_state.get("schema_profile") is not None
    ):
        return st.session_state.schema_profile  # type: ignore[return-value]
    try:
        files = {
            "file": (
                name,
                io.BytesIO(meta["data"]),
                meta.get("type") or "application/octet-stream",
            )
        }
        response = requests.post(_api_url("/data/profile"), files=files, timeout=120)
        response.raise_for_status()
        profile = response.json()
        st.session_state.schema_profile = profile
        st.session_state.schema_profile_for = name
        return profile
    except requests.RequestException:
        return {
            "filename": name,
            "note": "Could not load schema preview; chat may be limited until the server is reachable.",
        }


def _parse_task_command(text: str) -> tuple[bool, str]:
    """Return (is_task_command, remainder_after_prefix)."""
    stripped = text.strip()
    lower = stripped.lower()
    if lower.startswith("/task"):
        rest = stripped[5:].lstrip()
        return True, rest
    return False, stripped


def _pending_plan_task_id() -> str | None:
    """Task id of the latest plan card that has not been confirmed/run yet."""
    for m in reversed(st.session_state.messages):
        if m.get("type") != "plan_review":
            continue
        tid = m.get("task_id")
        if tid and not st.session_state.get(f"review_done_{tid}"):
            return str(tid)
    return None


def _chat_history_upto(before_index: int) -> list[dict[str, str]]:
    """Build {role, content} history for POST /chat from prior transcript turns."""
    hist: list[dict[str, str]] = []
    for msg in st.session_state.messages[:before_index]:
        role = msg.get("role", "user")
        mtype = msg.get("type", "text")
        if role not in ("user", "assistant"):
            continue
        if mtype == "text":
            content = (msg.get("content") or "").strip()
        elif mtype == "chat_response":
            content = (msg.get("content") or "").strip()
        else:
            continue
        if content:
            hist.append({"role": role, "content": content})
    return hist[-20:]


def _api_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}{path}"


def _requests_error_message(exc: requests.RequestException) -> str:
    """Surface FastAPI ``detail`` instead of only '502 Server Error: Bad Gateway'."""
    if isinstance(exc, requests.HTTPError):
        resp = exc.response
        if resp is not None:
            try:
                body = resp.json()
                detail = body.get("detail")
                if isinstance(detail, str):
                    return detail
                if isinstance(detail, list):
                    parts: list[str] = []
                    for item in detail:
                        if isinstance(item, dict):
                            loc = item.get("loc", ())
                            msg = item.get("msg", "")
                            parts.append(f"{loc}: {msg}".strip() if loc else str(msg))
                        else:
                            parts.append(str(item))
                    return "; ".join(parts) if parts else str(body)
            except (ValueError, TypeError):
                pass
            raw = (resp.text or "").strip()
            if raw:
                return raw[:8000]
    return str(exc)


def _codex_mock_query_params() -> dict[str, str]:
    """Query string survives multipart POST reliably; form fields beside file uploads may not."""
    use_mock = bool(st.session_state.get("use_codex_mock", True))
    return {"use_mock": "true" if use_mock else "false"}


def _post_task_bytes(
    filename: str,
    file_bytes: bytes,
    mime: str,
    question: str,
) -> dict[str, Any]:
    payload = {"question": question}
    files = {"file": (filename, io.BytesIO(file_bytes), mime or "application/octet-stream")}
    response = requests.post(
        _api_url("/tasks"),
        data=payload,
        files=files,
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_review(task_id: str, final_plan: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review"),
        json={"final_plan": final_plan},
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _get_task(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}"), timeout=30)
    response.raise_for_status()
    return response.json()


def _get_result(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}/result"), timeout=120)
    response.raise_for_status()
    return response.json()


def _post_chat(message: str, history: list[dict[str, str]], file_context: dict | None) -> dict[str, Any]:
    response = requests.post(
        _api_url("/chat"),
        json={
            "message": message,
            "history": history,
            "file_context": file_context,
        },
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_revise(task_id: str, instruction: str) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/revise"),
        json={"instruction": instruction},
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _draw_chart(chart: dict[str, Any]) -> None:
    chart_df = pd.DataFrame(chart.get("data", []))
    x_col = chart.get("x")
    y_col = chart.get("y")
    chart_type = chart.get("chart_type")
    if chart_df.empty or not x_col or not y_col or x_col not in chart_df.columns:
        st.info("No chart data yet.")
        return
    if chart_type == "line":
        st.line_chart(chart_df.set_index(x_col)[y_col])
    elif chart_type == "bar":
        st.bar_chart(chart_df.set_index(x_col)[y_col])
    elif chart_type == "histogram":
        st.bar_chart(chart_df[y_col].value_counts())
    else:
        st.dataframe(chart_df, use_container_width=True)


def _render_plan_tables(plan: dict[str, Any]) -> None:
    st.markdown(f"**Goal:** {plan.get('goal', '')}")
    out = plan.get("output") or {}
    st.caption(f"Chart: `{out.get('chart_type', '')}` · show_table: `{out.get('show_table', True)}`")

    metrics = plan.get("metrics") or []
    if metrics:
        st.markdown("**Metrics**")
        st.dataframe(pd.DataFrame(metrics), use_container_width=True)

    dims = plan.get("dimensions") or []
    if dims:
        st.markdown("**Dimensions**")
        st.dataframe(pd.DataFrame(dims), use_container_width=True)

    filters = plan.get("filters") or []
    if filters:
        st.markdown("**Filters**")
        st.dataframe(pd.DataFrame(filters), use_container_width=True)


def _render_result_block(result: dict[str, Any], task_id: str, key_suffix: str) -> None:
    if "chart" not in result:
        st.warning(result.get("message", "No chart in result."))
        st.json(result)
        return
    _draw_chart(result["chart"])
    table = result.get("table") or {}
    rows = table.get("rows") or []
    table_df = pd.DataFrame(rows)
    st.dataframe(table_df, use_container_width=True)
    if not table_df.empty:
        st.download_button(
            "Download table CSV",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{task_id}_result.csv",
            mime="text/csv",
            key=f"dl_{key_suffix}",
        )
    if result.get("execution_summary"):
        st.caption(result["execution_summary"])
    if result.get("summary"):
        st.markdown(result["summary"])
    follow = result.get("follow_ups") or []
    if follow:
        st.markdown("**Suggested follow-ups**")
        for idx, item in enumerate(follow):
            if st.button(
                item[:80] + ("…" if len(item) > 80 else ""),
                key=f"fu_{key_suffix}_{idx}",
            ):
                st.session_state["_followup_q"] = item
                st.rerun()


def _append_task_history(task_id: str, question: str) -> None:
    hist = st.session_state.task_history
    hist.append({"task_id": task_id, "question": question[:120]})
    st.session_state.task_history = hist[-20:]


def _enqueue_task(question: str) -> None:
    """Append a 'thinking' placeholder; actual API call happens on next render."""
    meta = st.session_state.file_meta
    if not meta:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "type": "text",
                "content": "Please attach a CSV or Excel file first (paperclip in the chat bar).",
            }
        )
        return
    st.session_state.mode = "task"
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "thinking",
            "action": "create_task",
            "question": question.strip(),
        }
    )


def _enqueue_chat(user_message: str) -> None:
    """Queue a free-form chat reply (no analysis plan)."""
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "thinking",
            "action": "chat_reply",
            "user_message": user_message.strip(),
        }
    )


def _enqueue_revise_plan(task_id: str, instruction: str) -> None:
    """Queue server-side plan revision from natural-language feedback."""
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "thinking",
            "action": "revise_plan",
            "task_id": task_id,
            "instruction": instruction.strip(),
        }
    )


def _execute_create_task(msg: dict[str, Any], msg_index: int) -> None:
    """Called during render when a 'thinking/create_task' message is encountered."""
    question = msg["question"]
    meta = st.session_state.file_meta
    if not meta:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": "File was removed before the task could be created.",
        }
        return
    try:
        with st.spinner("Generating analysis plan…"):
            resp = _post_task_bytes(
                meta["name"], meta["data"], meta["type"], question,
            )
        tid = resp["task_id"]
        plan = resp["plan"]
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "plan_review",
            "task_id": tid,
            "plan": plan,
        }
        st.session_state.active_task_id = tid
        _append_task_history(tid, question)
    except requests.RequestException as exc:
        detail = _requests_error_message(exc)
        use_mock = bool(st.session_state.get("use_codex_mock", True))
        hint = (
            ""
            if use_mock
            else (
                "\n\nTurn on **Mock Codex** in the sidebar to use the built-in planner, "
                "or fix the CLI / auth / network issue above and retry."
            )
        )
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": f"**Could not create task.** The server said:\n\n{detail}{hint}",
        }
    st.rerun()


def _execute_confirm_task(msg: dict[str, Any], msg_index: int) -> None:
    """Called during render when a 'thinking/confirm_task' message is encountered."""
    task_id = msg["task_id"]
    final_plan = msg["final_plan"]
    try:
        with st.spinner("Running analysis…"):
            rec = _post_review(task_id, final_plan)
        st.session_state[f"review_done_{task_id}"] = True
        res = rec.get("result")
        if res is not None:
            st.session_state.messages[msg_index] = {
                "role": "assistant",
                "type": "result",
                "task_id": task_id,
                "result": res,
            }
            st.session_state.messages.append(
                {
                    "role": "assistant",
                    "type": "task_done_confirm",
                    "task_id": task_id,
                }
            )
        else:
            st.session_state.messages[msg_index] = {
                "role": "assistant",
                "type": "text",
                "content": f"Review submitted but no result on record (status={rec.get('status')}).",
            }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": f"**Execution failed:** {_requests_error_message(exc)}",
        }
    st.rerun()


def _execute_chat_reply(msg: dict[str, Any], msg_index: int) -> None:
    """POST /chat and replace the thinking placeholder with assistant text."""
    user_text = msg.get("user_message", "")
    history = _chat_history_upto(msg_index)
    file_ctx = _ensure_schema_profile()
    try:
        with st.spinner("Thinking…"):
            resp = _post_chat(user_text, history, file_ctx)
        reply = resp.get("reply", "").strip() or "(empty reply)"
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "chat_response",
            "content": reply,
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": f"**Chat failed:** {_requests_error_message(exc)}",
        }
    st.rerun()


def _execute_revise_plan(msg: dict[str, Any], msg_index: int) -> None:
    """POST /tasks/{id}/revise and update the matching plan_review card."""
    task_id = str(msg["task_id"])
    instruction = msg.get("instruction", "")
    try:
        with st.spinner("Revising plan…"):
            resp = _post_revise(task_id, instruction)
        plan = resp["plan"]
        st.session_state.pop(f"plan_json_{task_id}", None)
        for j, m in enumerate(st.session_state.messages):
            if m.get("type") == "plan_review" and m.get("task_id") == task_id:
                st.session_state.messages[j] = {
                    "role": "assistant",
                    "type": "plan_review",
                    "task_id": task_id,
                    "plan": plan,
                }
                break
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": "Plan updated from your feedback — review the card above, or describe more changes.",
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": f"**Could not revise plan:** {_requests_error_message(exc)}",
        }
    st.rerun()


_init_state()

# --- Sidebar: session + history (upload via chat bar paperclip — avoids sidebar file_uploader + chat_input issues) ---
with st.sidebar:
    mode = st.session_state.get("mode", "chat")
    st.subheader("Mode")
    st.caption(
        f"**{'Task' if mode == 'task' else 'Chat'}**"
        + (
            f" · active task `{str(st.session_state.get('active_task_id', ''))[:8]}…`"
            if mode == "task" and st.session_state.get("active_task_id")
            else ""
        )
    )

    st.subheader("Data file")
    if st.session_state.file_meta:
        st.caption(f"Active: `{st.session_state.file_meta['name']}`")
        if st.button("Remove file", key="btn_remove_uploaded_file"):
            st.session_state.file_meta = None
            _invalidate_schema_cache()
            st.session_state.pop("chat_prompt", None)
            st.rerun()
    else:
        st.caption("Attach CSV/Excel with the **paperclip** in the chat bar below.")

    st.toggle(
        "Mock Codex (no CLI)",
        key="use_codex_mock",
        help="When off, the API uses the real Codex CLI for plan / summary / follow-ups (same as CODEX_MOCK=false).",
    )

    st.divider()
    st.subheader("Recent tasks")
    if not st.session_state.task_history:
        st.caption("None yet.")
    else:
        for i, item in enumerate(reversed(st.session_state.task_history)):
            tid = item["task_id"]
            label = item["question"][:40] + ("…" if len(item["question"]) > 40 else "")
            st.caption(f"`{tid[:8]}…` {label}")
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Refresh", key=f"hist_ref_{tid}"):
                    try:
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "text",
                                "content": f"Task `{tid}` status: `{_get_task(tid).get('status')}`",
                            }
                        )
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(str(exc))
            with c2:
                if st.button("Result", key=f"hist_res_{tid}"):
                    try:
                        res = _get_result(tid)
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "result",
                                "task_id": tid,
                                "result": res,
                            }
                        )
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(str(exc))

    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.session_state.mode = "chat"
        st.session_state.active_task_id = None
        st.rerun()

# --- Process follow-up click (before rendering chat) ---
if st.session_state.get("_followup_q"):
    fq = st.session_state._followup_q
    st.session_state._followup_q = None
    st.session_state.messages.append({"role": "user", "type": "text", "content": fq})
    st.session_state.mode = "task"
    _enqueue_task(fq)
    st.rerun()

# --- Render chat ---
for i, msg in enumerate(st.session_state.messages):
    role = msg.get("role", "assistant")
    mtype = msg.get("type", "text")

    # --- Deferred execution: "thinking" placeholders trigger API calls during render ---
    if mtype == "thinking":
        action = msg.get("action")
        with st.chat_message("assistant"):
            if action == "create_task":
                st.markdown("Analyzing your question…")
                _execute_create_task(msg, i)
            elif action == "confirm_task":
                st.markdown("Running the analysis plan…")
                _execute_confirm_task(msg, i)
            elif action == "chat_reply":
                st.markdown("Thinking…")
                _execute_chat_reply(msg, i)
            elif action == "revise_plan":
                st.markdown("Updating the plan…")
                _execute_revise_plan(msg, i)
            else:
                st.markdown("Processing…")
        continue

    with st.chat_message(role):
        if mtype == "text":
            st.markdown(msg.get("content", ""))
        elif mtype == "chat_response":
            st.markdown(msg.get("content", ""))
        elif mtype == "plan_review":
            task_id = msg["task_id"]
            plan = msg["plan"]
            st.markdown(
                "Here is the proposed **analysis plan**. Review the JSON if needed, then confirm to run. "
                "While this card is open, you can **type revision feedback in chat** (no `/task` prefix) to update the plan."
            )
            _render_plan_tables(plan)

            conf = plan.get("confidence")
            if conf is not None:
                if conf < 0.6:
                    st.warning(f"Low confidence: **{conf:.2f}** — check filters and columns.")
                else:
                    st.info(f"Confidence: **{conf:.2f}**")

            for amb in plan.get("ambiguities") or []:
                st.warning(f"`{amb.get('field', '?')}`: {amb.get('issue', '')}")

            plan_key = f"plan_json_{task_id}"
            if plan_key not in st.session_state:
                st.session_state[plan_key] = json.dumps(plan, ensure_ascii=False, indent=2)

            with st.expander("Raw plan JSON (advanced)"):
                st.text_area(
                    "Edit plan JSON",
                    key=plan_key,
                    height=260,
                    label_visibility="collapsed",
                )

            done_key = f"review_done_{task_id}"
            if st.session_state.get(done_key):
                st.success("Plan submitted — scroll down for the result card.")
            else:
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("Confirm and run", type="primary", key=f"confirm_{task_id}"):
                        try:
                            final_plan = json.loads(st.session_state[plan_key])
                        except json.JSONDecodeError as exc:
                            st.error(str(exc))
                        else:
                            st.session_state.messages.append(
                                {
                                    "role": "assistant",
                                    "type": "thinking",
                                    "action": "confirm_task",
                                    "task_id": task_id,
                                    "final_plan": final_plan,
                                }
                            )
                            st.rerun()
                with b2:
                    st.caption("Edit the JSON in the expander above before confirming.")

        elif mtype == "result":
            tid = msg["task_id"]
            st.markdown("**Results**")
            _render_result_block(msg["result"], tid, key_suffix=f"{i}_{tid[:8]}")
        elif mtype == "task_done_confirm":
            tid = msg["task_id"]
            st.markdown("**Task finished** — does this meet your goal?")
            note_key = f"replan_note_{tid}"
            st.text_area(
                "If not, describe what is missing (optional)",
                key=note_key,
                height=72,
            )
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Mark complete", type="primary", key=f"done_ok_{tid}"):
                    st.session_state.mode = "chat"
                    st.session_state.active_task_id = None
                    st.session_state.messages[i] = {
                        "role": "assistant",
                        "type": "text",
                        "content": (
                            "Marked complete. You can keep chatting, or start a structured run with **`/task`** "
                            "+ your question."
                        ),
                    }
                    st.rerun()
            with b2:
                if st.button("Not done — replan", key=f"done_replan_{tid}"):
                    note = (st.session_state.get(note_key) or "").strip() or "Needs a different analysis."
                    try:
                        rec = _get_task(tid)
                        orig_q = (rec.get("input") or {}).get("question", "")
                    except requests.RequestException:
                        orig_q = ""
                    combined = (
                        f"{orig_q}\n\nUser feedback (result not sufficient): {note}"
                        if orig_q
                        else f"User feedback (result not sufficient): {note}"
                    )
                    st.session_state.mode = "task"
                    st.session_state.messages[i] = {
                        "role": "assistant",
                        "type": "text",
                        "content": "Generating a new plan from your feedback…",
                    }
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "thinking",
                            "action": "create_task",
                            "question": combined.strip(),
                        }
                    )
                    st.rerun()

# --- Chat input (CSV/Excel via paperclip) ---
chat_val = st.chat_input(
    "Chat freely, or type /task + your analysis question — attach CSV/Excel via paperclip…",
    accept_file=True,
    file_type=["csv", "xlsx", "xls"],
    key="chat_prompt",
)
if chat_val is not None:
    text = chat_val.text.strip() if not isinstance(chat_val, str) else chat_val.strip()
    file_list = [] if isinstance(chat_val, str) else list(chat_val.files)
    if file_list:
        f0 = file_list[0]
        prev_name = (st.session_state.file_meta or {}).get("name")
        st.session_state.file_meta = {
            "name": f0.name,
            "type": f0.type or "application/octet-stream",
            "data": f0.getvalue(),
        }
        if prev_name != f0.name:
            _invalidate_schema_cache()
        st.session_state.messages.append(
            {
                "role": "assistant",
                "type": "text",
                "content": f"Loaded **`{f0.name}`**.",
            }
        )
    if text:
        st.session_state.messages.append({"role": "user", "type": "text", "content": text})
        is_task_cmd, task_body = _parse_task_command(text)
        if is_task_cmd:
            if not task_body:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "text",
                        "content": "Use **`/task`** followed by your analysis request (e.g. `/task compare sales by region`).",
                    }
                )
            else:
                st.session_state.mode = "task"
                _enqueue_task(task_body)
        elif st.session_state.get("mode") == "task":
            pending_tid = _pending_plan_task_id()
            if pending_tid is not None:
                _enqueue_revise_plan(pending_tid, text)
            else:
                st.session_state.mode = "chat"
                _enqueue_chat(text)
        else:
            st.session_state.mode = "chat"
            _enqueue_chat(text)
    elif file_list and not text:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "type": "text",
                "content": "File ready. Ask a question in the chat box.",
            }
        )
    st.rerun()

