from __future__ import annotations

import io
import json
import os
import sys
import time
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

from app.sql_generator_jsonl_panel import render_sql_generator_jsonl_panel

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

# Shown when the transcript is empty (excluded from /chat history). Keep in sync with page caption.
WELCOME_MESSAGE_MARKDOWN = (
    "**Hi — here is how to get started:**\n\n"
    "- **Chat**: ask questions about your data in normal language.\n"
    "- **Structured run**: type **`/task`** plus your analysis question to get a plan, review or revise it, "
    "then confirm to run.\n"
    "- **Data file**: attach **CSV / Excel** with the **paperclip** in the chat bar (or manage it in the sidebar).\n"
    "- **Mock Codex**: toggle in the sidebar for offline/built-in behavior vs real CLI.\n\n"
    "When you are ready, type a message or **`/task`** below."
)

# ``type: "error"`` message ``kind`` (optional); not shown to the model.
ERROR_KIND_CHAT = "chat"
ERROR_KIND_CREATE_TASK = "create_task"
ERROR_KIND_CONFIRM_TASK = "confirm_task"
ERROR_KIND_REVISE_PLAN = "revise_plan"
ERROR_KIND_REVIEW_RESPOND = "review_respond"

# Max user "turns" (each user text message starts one) fully expanded in the main column; older rows go in an expander.
MAX_VISIBLE_CHAT_TURNS = 40

st.set_page_config(page_title="xyf-competition-mvp", layout="wide")
st.title("xyf-competition-mvp")
st.caption(
    "Default: **chat** with the assistant about your data. Type **`/task`** + your question to generate a "
    "structured plan, review or revise it, confirm to run, then mark the task complete. "
    "Use the **SQL generator · Codex JSONL** tab to run the local JSONL smoke test without the CLI."
)


def _default_use_codex_mock() -> bool:
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("file_meta", None)
    st.session_state.setdefault("task_history", [])
    st.session_state.setdefault("chat_sessions_cache", [])
    st.session_state.setdefault("task_history_cache", [])
    st.session_state.setdefault("_followup_q", None)
    st.session_state.setdefault("mode", "chat")  # "chat" | "task"
    st.session_state.setdefault("chat_session_id", str(uuid.uuid4()))
    st.session_state.setdefault("active_task_id", None)
    st.session_state.setdefault("schema_profile", None)
    st.session_state.setdefault("schema_profile_for", None)
    st.session_state.setdefault("codex_model_override", "")
    st.session_state.setdefault("codex_reasoning_effort_override", "")
    st.session_state.setdefault("show_prompt_debug", False)
    if "use_codex_mock" not in st.session_state:
        st.session_state.use_codex_mock = _default_use_codex_mock()


def _ensure_welcome_if_empty() -> None:
    """If there is no transcript yet, show one assistant welcome card (not sent as /chat history)."""
    if st.session_state.messages:
        return
    st.session_state.messages = [
        {
            "role": "assistant",
            "type": "welcome",
            "content": WELCOME_MESSAGE_MARKDOWN,
        }
    ]


def _assistant_error_dict(
    title: str,
    detail: str,
    kind: str | None = None,
) -> dict[str, Any]:
    """Build a chat bubble that renders with ``st.error`` + optional detail expander."""
    msg: dict[str, Any] = {
        "role": "assistant",
        "type": "error",
        "title": (title or "Error").strip() or "Error",
        "detail": (detail or "").strip(),
    }
    if kind:
        msg["kind"] = kind
    return msg


def _render_assistant_error_message(msg: dict[str, Any], msg_index: int) -> None:
    """Render ``type: "error"`` with a callout and full text under Details."""
    title = str(msg.get("title") or "Something went wrong")
    detail = str(msg.get("detail") or "").strip()
    kind = msg.get("kind")
    st.error(f"**{title}**")
    if isinstance(kind, str) and kind.strip():
        st.caption(f"`kind:` {kind.strip()}")
    if detail:
        with st.expander("Details", key=f"assistant_err_details_{msg_index}"):
            st.code(detail, language="text")


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


def _pending_review_task_id() -> str | None:
    """Task id of the latest unresolved review_request card."""
    for m in reversed(st.session_state.messages):
        if m.get("type") != "review_request":
            continue
        if bool(m.get("resolved")):
            continue
        tid = m.get("task_id")
        if tid:
            return str(tid)
    return None


def _chat_history_upto(before_index: int) -> list[dict[str, str]]:
    """Build {role, content} history for POST /chat from prior transcript turns."""
    def _sanitize_assistant_content(text: str) -> str:
        lines = text.splitlines()
        kept: list[str] = []
        for line in lines:
            if "[Timing]" in line or "[Tokens]" in line:
                continue
            kept.append(line)
        return "\n".join(kept).strip()

    hist: list[dict[str, str]] = []
    for msg in st.session_state.messages[:before_index]:
        role = msg.get("role", "user")
        mtype = msg.get("type", "text")
        if role not in ("user", "assistant"):
            continue
        if mtype in ("welcome", "error"):
            continue
        if mtype == "text":
            content = (msg.get("content") or "").strip()
        elif mtype == "chat_response":
            content = _sanitize_assistant_content((msg.get("content") or "").strip())
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
    params: dict[str, str] = {"use_mock": "true" if use_mock else "false"}
    model = str(st.session_state.get("codex_model_override", "") or "").strip()
    reasoning = str(
        st.session_state.get("codex_reasoning_effort_override", "") or ""
    ).strip()
    if model:
        params["model"] = model
    if reasoning:
        params["reasoning_effort"] = reasoning
    return params


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


def _post_run_task(task_id: str, plan: dict[str, Any] | None) -> dict[str, Any]:
    params = _codex_mock_query_params()
    if bool(st.session_state.get("include_demo_artifacts", False)):
        params["include_demo_artifacts"] = "true"
    response = requests.post(
        _api_url(f"/tasks/{task_id}/run"),
        json={"plan": plan} if plan is not None else {},
        params=params,
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_review_respond(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review/respond"),
        json=payload,
        params=_codex_mock_query_params(),
        timeout=120,
    )
    response.raise_for_status()
    return response.json()


def _post_create_review_request(task_id: str, payload: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review"),
        json=payload,
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


def _get_chat_sessions(limit: int = 50) -> list[dict[str, Any]]:
    response = requests.get(_api_url("/chat/sessions"), params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return list(response.json() or [])


def _get_chat_session_turns(session_id: str, limit: int = 200) -> list[dict[str, Any]]:
    response = requests.get(
        _api_url(f"/chat/sessions/{session_id}/turns"),
        params={"limit": limit},
        timeout=30,
    )
    response.raise_for_status()
    return list(response.json() or [])


def _delete_chat_session(session_id: str) -> int:
    response = requests.delete(_api_url(f"/chat/sessions/{session_id}"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _delete_all_chat_sessions() -> int:
    response = requests.delete(_api_url("/chat/sessions"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _get_task_history(limit: int = 50) -> list[dict[str, Any]]:
    response = requests.get(_api_url("/tasks/history"), params={"limit": limit}, timeout=30)
    response.raise_for_status()
    return list(response.json() or [])


def _delete_task(task_id: str) -> int:
    response = requests.delete(_api_url(f"/tasks/{task_id}"), timeout=30)
    response.raise_for_status()
    body = response.json() or {}
    return int(body.get("deleted", 0) or 0)


def _post_chat(message: str, history: list[dict[str, str]], file_context: dict | None) -> dict[str, Any]:
    use_mock = bool(st.session_state.get("use_codex_mock", True))
    # Real Codex CLI cold start can exceed 120s.
    timeout_s = 120 if use_mock else int(os.getenv("STREAMLIT_CHAT_TIMEOUT_SECONDS", "300"))
    started = time.perf_counter()
    params = _codex_mock_query_params()
    if bool(st.session_state.get("show_prompt_debug", False)):
        params["include_prompt_debug"] = "true"
    response = requests.post(
        _api_url("/chat"),
        json={
            "message": message,
            "session_id": st.session_state.get("chat_session_id"),
            "history": history,
            "file_context": file_context,
        },
        params=params,
        timeout=timeout_s,
    )
    response.raise_for_status()
    payload = response.json()
    payload["_client_elapsed_s"] = time.perf_counter() - started
    return payload


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

    artifacts = result.get("artifacts") or []
    if artifacts:
        st.markdown("**Artifacts**")
        for idx, a in enumerate(artifacts):
            name = str(a.get("name") or f"artifact_{idx}")
            mime = str(a.get("mime") or "")
            width = a.get("display_width")
            height = a.get("display_height")
            if isinstance(width, int) and width > 0:
                width = min(width, 800)
            else:
                width = 640
            if mime.startswith("image/"):
                b64 = a.get("data_base64")
                if isinstance(b64, str) and b64.strip():
                    import base64 as _b64

                    raw = _b64.b64decode(b64)
                    st.image(raw, caption=name, width=width)
                else:
                    st.warning(f"Image artifact `{name}` missing data.")
            elif mime == "text/html":
                html = a.get("html")
                if isinstance(html, str) and html.strip():
                    h = height if isinstance(height, int) and height > 0 else 180
                    components.html(html, height=h, scrolling=True)
                else:
                    st.warning(f"HTML artifact `{name}` missing html.")
            else:
                st.caption(f"{name} ({mime})")
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


def _append_review_request_message(task_id: str, review: dict[str, Any]) -> None:
    """Append one pending review_request message if not already present."""
    review_id = str(review.get("review_id") or "").strip()
    if not review_id:
        return
    for m in reversed(st.session_state.messages):
        if m.get("type") != "review_request":
            continue
        if str(m.get("review_id") or "").strip() == review_id:
            return
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "review_request",
            "task_id": task_id,
            "review_id": review_id,
            "review_type": str(review.get("review_type") or "").strip(),
            "title": str(review.get("title") or "").strip(),
            "message": str(review.get("message") or "").strip(),
            "options": list(review.get("options") or []),
            "resolved": False,
        }
    )


def _ensure_confirmation_review(task_id: str) -> None:
    """Create one pending confirmation review on backend and mirror it in chat."""
    rec = _post_create_review_request(
        task_id,
        {
            "review_type": "confirmation",
            "title": "Confirm Execution",
            "message": "Review the current plan. Confirm to run, or type feedback to revise the plan first.",
            "options": ["Confirm and run"],
        },
    )
    pending = rec.get("pending_review")
    if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
        _append_review_request_message(task_id, pending)


def _restore_chat_messages_from_turns(turns: list[dict[str, Any]]) -> list[dict[str, Any]]:
    restored: list[dict[str, Any]] = []
    for turn in turns:
        user_message = str(turn.get("user_message") or "").strip()
        if user_message:
            restored.append({"role": "user", "type": "text", "content": user_message})
        reply_text = str(turn.get("reply_text") or "").strip()
        if reply_text:
            restored.append(
                {
                    "role": "assistant",
                    "type": "chat_response",
                    "content": reply_text,
                    "debug_prompt": turn.get("debug_prompt"),
                    "prompt_chars": turn.get("prompt_chars"),
                    "history_turns_used": turn.get("history_turns"),
                }
            )
        error_text = str(turn.get("error_text") or "").strip()
        if error_text and not reply_text:
            restored.append(
                _assistant_error_dict(
                    "Chat failed",
                    error_text,
                    kind=ERROR_KIND_CHAT,
                )
            )
    return restored


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


def _enqueue_review_respond(
    task_id: str,
    *,
    user_text: str | None = None,
    choice: str | None = None,
) -> None:
    """Queue response for pending task review; user_text has higher priority server-side."""
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "thinking",
            "action": "respond_review",
            "task_id": task_id,
            "user_text": (user_text or "").strip(),
            "choice": (choice or "").strip(),
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
        try:
            _ensure_confirmation_review(tid)
        except requests.RequestException:
            # Plan can still be shown even if review creation fails.
            pass
        st.session_state.active_task_id = tid
        _append_task_history(tid, question)
        st.session_state.task_history_cache = []
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
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Could not create task",
            f"The server said:\n\n{detail}{hint}",
            kind=ERROR_KIND_CREATE_TASK,
        )
    st.rerun()


def _execute_confirm_task(msg: dict[str, Any], msg_index: int) -> None:
    """Called during render when a 'thinking/confirm_task' message is encountered."""
    task_id = msg["task_id"]
    final_plan = msg.get("final_plan")
    try:
        with st.spinner("Running analysis…"):
            rec = _post_run_task(task_id, final_plan)
        st.session_state[f"review_done_{task_id}"] = True
        for j, m in enumerate(st.session_state.messages):
            if (
                m.get("type") == "review_request"
                and str(m.get("task_id")) == task_id
                and not bool(m.get("resolved"))
            ):
                updated = dict(m)
                updated["resolved"] = True
                updated["resolution"] = "confirm_and_run"
                st.session_state.messages[j] = updated
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
                "content": f"Run submitted but no result on record yet (status={rec.get('status')}).",
            }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Execution failed",
            _requests_error_message(exc),
            kind=ERROR_KIND_CONFIRM_TASK,
        )
    st.rerun()


def _execute_chat_reply(msg: dict[str, Any], msg_index: int) -> None:
    """POST /chat and replace the thinking placeholder with assistant text."""
    user_text = msg.get("user_message", "")
    history = _chat_history_upto(msg_index)
    file_ctx = _ensure_schema_profile()
    try:
        with st.spinner("Thinking…"):
            resp = _post_chat(user_text, history, file_ctx)
        session_id = resp.get("session_id")
        if isinstance(session_id, str) and session_id.strip():
            st.session_state.chat_session_id = session_id.strip()
            st.session_state.chat_sessions_cache = []
        reply = resp.get("reply", "").strip() or "(empty reply)"
        prompt_chars = resp.get("prompt_chars")
        history_turns_used = resp.get("history_turns_used")
        debug_prompt = resp.get("debug_prompt")
        codex_elapsed = resp.get("codex_exec_elapsed_s")
        codex_spawn_elapsed = resp.get("codex_spawn_elapsed_s")
        codex_ttft_elapsed = resp.get("codex_ttft_elapsed_s")
        codex_generation_elapsed = resp.get("codex_generation_elapsed_s")
        codex_teardown_elapsed = resp.get("codex_teardown_elapsed_s")
        provider_elapsed = resp.get("provider_elapsed_s")
        provider_overhead_elapsed = resp.get("provider_overhead_elapsed_s")
        prompt_build_elapsed = resp.get("prompt_build_elapsed_s")
        input_tokens = resp.get("input_tokens")
        output_tokens = resp.get("output_tokens")
        cached_input_tokens = resp.get("cached_input_tokens")
        api_elapsed = resp.get("api_elapsed_s")
        client_elapsed = resp.get("_client_elapsed_s")
        runtime_vendor = str(resp.get("runtime_vendor") or "").strip()
        runtime_binary = str(resp.get("runtime_binary") or "").strip()
        timing_parts: list[str] = []
        if isinstance(codex_elapsed, (int, float)):
            timing_parts.append(f"codex执行 {codex_elapsed:.2f}s")
        timing_parts.append(
            f"spawn {codex_spawn_elapsed:.2f}s"
            if isinstance(codex_spawn_elapsed, (int, float))
            else "spawn n/a"
        )
        timing_parts.append(
            f"首token {codex_ttft_elapsed:.2f}s"
            if isinstance(codex_ttft_elapsed, (int, float))
            else "首token n/a"
        )
        timing_parts.append(
            f"生成 {codex_generation_elapsed:.2f}s"
            if isinstance(codex_generation_elapsed, (int, float))
            else "生成 n/a"
        )
        timing_parts.append(
            f"收尾 {codex_teardown_elapsed:.2f}s"
            if isinstance(codex_teardown_elapsed, (int, float))
            else "收尾 n/a"
        )
        if isinstance(provider_overhead_elapsed, (int, float)):
            timing_parts.append(f"后端非Codex {provider_overhead_elapsed:.2f}s")
        if isinstance(prompt_build_elapsed, (int, float)):
            timing_parts.append(f"组Prompt {prompt_build_elapsed:.2f}s")
        if isinstance(provider_elapsed, (int, float)):
            timing_parts.append(f"后端总计 {provider_elapsed:.2f}s")
        if isinstance(client_elapsed, (int, float)):
            timing_parts.append(f"接口通讯 {client_elapsed:.2f}s")
        elif isinstance(api_elapsed, (int, float)):
            timing_parts.append(f"接口通讯 {api_elapsed:.2f}s")
        if timing_parts:
            reply = (
                f"{reply}\n\n"
                f"`[Timing] {' | '.join(timing_parts)}（后端总计与接口通讯包含 codex执行，勿相加）`"
            )
        token_parts: list[str] = []
        if isinstance(input_tokens, int):
            token_parts.append(f"in {input_tokens}")
        if isinstance(output_tokens, int):
            token_parts.append(f"out {output_tokens}")
        if isinstance(cached_input_tokens, int):
            token_parts.append(f"cached_in {cached_input_tokens}")
        if token_parts:
            reply = f"{reply}\n\n`[Tokens] {' | '.join(token_parts)}`"
        if runtime_vendor:
            runtime_text = f"[Runtime] {runtime_vendor}"
            if runtime_binary:
                runtime_text = f"{runtime_text} | {runtime_binary}"
            reply = f"{reply}\n\n`{runtime_text}`"
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "chat_response",
            "content": reply,
            "debug_prompt": debug_prompt,
            "prompt_chars": prompt_chars,
            "history_turns_used": history_turns_used,
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Chat failed",
            _requests_error_message(exc),
            kind=ERROR_KIND_CHAT,
        )
    st.rerun()


def _execute_revise_plan(msg: dict[str, Any], msg_index: int) -> None:
    """POST /tasks/{id}/revise and update the matching plan_review card."""
    task_id = str(msg["task_id"])
    instruction = msg.get("instruction", "")
    try:
        with st.spinner("Revising plan…"):
            resp = _post_revise(task_id, instruction)
        plan = resp["plan"]
        suffix = f"_{task_id}"
        for k in list(st.session_state.keys()):
            if isinstance(k, str) and k.startswith("plan_json_") and k.endswith(suffix):
                st.session_state.pop(k, None)
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
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Could not revise plan",
            _requests_error_message(exc),
            kind=ERROR_KIND_REVISE_PLAN,
        )
    st.rerun()


def _execute_review_respond(msg: dict[str, Any], msg_index: int) -> None:
    """POST /tasks/{id}/review/respond and apply returned task state into chat cards."""
    task_id = str(msg["task_id"])
    user_text = str(msg.get("user_text") or "").strip()
    choice = str(msg.get("choice") or "").strip()
    payload: dict[str, Any] = {}
    if user_text:
        payload["user_text"] = user_text
    if choice:
        payload["choice"] = choice
    if not payload:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": "No review response was sent.",
        }
        st.rerun()
        return
    try:
        with st.spinner("Submitting review response…"):
            rec = _post_review_respond(task_id, payload)
        for j, m in enumerate(st.session_state.messages):
            if (
                m.get("type") == "review_request"
                and str(m.get("task_id")) == task_id
                and not bool(m.get("resolved"))
            ):
                updated = dict(m)
                updated["resolved"] = True
                updated["resolution"] = user_text or choice or "resolved"
                st.session_state.messages[j] = updated
                break
        plan = rec.get("plan")
        if isinstance(plan, dict):
            suffix = f"_{task_id}"
            for k in list(st.session_state.keys()):
                if isinstance(k, str) and k.startswith("plan_json_") and k.endswith(suffix):
                    st.session_state.pop(k, None)
            plan_card_updated = False
            for j, m in enumerate(st.session_state.messages):
                if m.get("type") == "plan_review" and str(m.get("task_id")) == task_id:
                    st.session_state.messages[j] = {
                        "role": "assistant",
                        "type": "plan_review",
                        "task_id": task_id,
                        "plan": plan,
                    }
                    plan_card_updated = True
                    break
            if not plan_card_updated:
                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "type": "plan_review",
                        "task_id": task_id,
                        "plan": plan,
                    }
                )
        pending = rec.get("pending_review")
        if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
            _append_review_request_message(task_id, pending)
        elif user_text:
            try:
                _ensure_confirmation_review(task_id)
            except requests.RequestException:
                pass
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": (
                "你的文本反馈已应用到计划。"
                if user_text
                else "已记录你的选择。"
            ),
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Could not respond to review",
            _requests_error_message(exc),
            kind=ERROR_KIND_REVIEW_RESPOND,
        )
    st.rerun()


def _format_ts_for_sidebar(iso: str | None) -> str:
    """Format API ISO timestamps for a weak sidebar caption: output MM-DD HH:MM (local time when tz-aware)."""
    if iso is None or not str(iso).strip():
        return "—"
    s = str(iso).strip().replace("Z", "+00:00")
    try:
        dt = datetime.fromisoformat(s)
    except ValueError:
        return s[:16] if len(s) >= 16 else s
    if dt.tzinfo is not None:
        dt = dt.astimezone()
    return dt.strftime("%m-%d %H:%M")


def _user_text_message_indices(messages: list[dict[str, Any]]) -> list[int]:
    return [
        i
        for i, m in enumerate(messages)
        if m.get("role") == "user" and m.get("type") == "text"
    ]


def _transcript_cut_for_viewport(
    messages: list[dict[str, Any]],
    max_turns: int,
) -> int:
    """First index of the suffix shown outside the \"older\" expander; ``0`` means show everything."""
    user_idxs = _user_text_message_indices(messages)
    if len(user_idxs) <= max_turns:
        return 0
    return int(user_idxs[-max_turns])


def _render_chat_message(i: int, msg: dict[str, Any]) -> None:
    """Render one transcript row; ``i`` is the index in ``st.session_state.messages`` (required for thinking + unique keys)."""
    role = msg.get("role", "assistant")
    mtype = msg.get("type", "text")

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
            elif action == "respond_review":
                st.markdown("Applying your review response…")
                _execute_review_respond(msg, i)
            else:
                st.markdown("Processing…")
        return

    with st.chat_message(role):
        if mtype == "welcome":
            st.markdown(msg.get("content", ""))
        elif mtype == "error":
            _render_assistant_error_message(msg, i)
        elif mtype == "text":
            st.markdown(msg.get("content", ""))
        elif mtype == "chat_response":
            st.markdown(msg.get("content", ""))
            debug_prompt = msg.get("debug_prompt")
            if isinstance(debug_prompt, str) and debug_prompt.strip():
                with st.expander("Context sent to Codex", key=f"ctx_codex_{i}"):
                    pchars = msg.get("prompt_chars")
                    hturns = msg.get("history_turns_used")
                    meta_parts: list[str] = []
                    if isinstance(pchars, int):
                        meta_parts.append(f"prompt_chars={pchars}")
                    if isinstance(hturns, int):
                        meta_parts.append(f"history_turns={hturns}")
                    if meta_parts:
                        st.caption(" | ".join(meta_parts))
                    st.code(debug_prompt, language="markdown")
        elif mtype == "review_request":
            task_id = str(msg.get("task_id") or "")
            review_id = str(msg.get("review_id") or "")
            title = str(msg.get("title") or "Review")
            body = str(msg.get("message") or "")
            options = [str(x).strip() for x in (msg.get("options") or []) if str(x).strip()]
            resolved = bool(msg.get("resolved"))
            review_type = str(msg.get("review_type") or "").strip().lower()
            st.markdown(f"**{title}**")
            if body:
                st.markdown(body)
            if review_type:
                st.caption(f"type: `{review_type}`")
            if resolved:
                st.success(f"Handled: {str(msg.get('resolution') or 'resolved')}")
            elif review_type == "confirmation":
                if st.button(
                    "Confirm and run",
                    type="primary",
                    key=f"review_confirm_run_{i}_{task_id}_{review_id}",
                ):
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "thinking",
                            "action": "confirm_task",
                            "task_id": task_id,
                            "final_plan": None,
                        }
                    )
                    st.rerun()
            elif options:
                cols = st.columns(min(3, len(options)))
                for idx, opt in enumerate(options):
                    with cols[idx % len(cols)]:
                        if st.button(opt, key=f"review_opt_{i}_{task_id}_{review_id}_{idx}"):
                            _enqueue_review_respond(task_id, choice=opt)
                            st.rerun()
            st.caption("直接输入文本优先级更高，会覆盖按钮选择。")
        elif mtype == "plan_review":
            task_id = msg["task_id"]
            plan = msg["plan"]
            st.markdown(
                "Here is the proposed **analysis plan**. This is an informational message; "
                "execution decisions are handled in the review card."
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

            plan_key = f"plan_json_{i}_{task_id}"
            if plan_key not in st.session_state:
                st.session_state[plan_key] = json.dumps(plan, ensure_ascii=False, indent=2)

            with st.expander("Raw plan JSON (advanced)", key=f"raw_plan_exp_{i}_{task_id}"):
                st.text_area(
                    "Edit plan JSON",
                    key=plan_key,
                    height=260,
                    label_visibility="collapsed",
                )

            done_key = f"review_done_{task_id}"
            if st.session_state.get(done_key):
                st.success("Plan executed — see the result card below.")
            else:
                st.caption("Tip: use the review card below to confirm run or provide feedback.")

        elif mtype == "result":
            tid = msg["task_id"]
            st.markdown("**Results**")
            _render_result_block(msg["result"], tid, key_suffix=f"{i}_{tid[:8]}")
        elif mtype == "task_done_confirm":
            tid = msg["task_id"]
            st.markdown("**Task finished** — does this meet your goal?")
            note_key = f"replan_note_{i}_{tid}"
            st.text_area(
                "If not, describe what is missing (optional)",
                key=note_key,
                height=72,
            )
            b1, b2 = st.columns(2)
            with b1:
                if st.button("Mark complete", type="primary", key=f"done_ok_{i}_{tid}"):
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
                if st.button("Not done — replan", key=f"done_replan_{i}_{tid}"):
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
    st.caption(f"session `{str(st.session_state.get('chat_session_id', ''))[:8]}…`")

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
        value = False,
        key="use_codex_mock",
        help="When off, the API uses the real Codex CLI for plan / summary / follow-ups (same as CODEX_MOCK=false).",
    )
    st.toggle(
        "Show Prompt Debug",
        value = False,
        key="show_prompt_debug",
        help="Show a collapsed panel under each chat response with the exact prompt sent to Codex.",
    )
    st.toggle(
        "Include demo artifacts (PNG + HTML)",
        value=False,
        key="include_demo_artifacts",
        help="Attach a demo image (downloaded from the internet) + a demo HTML snippet in task results to test rendering.",
    )
    st.text_input(
        "Model Override",
        key="codex_model_override",
        placeholder="e.g. gpt-5.4-mini",
        help="Optional per-request model override sent to backend as query param `model`.",
    )
    st.text_input(
        "Reasoning Effort",
        key="codex_reasoning_effort_override",
        placeholder="low / medium / high",
        help="Optional per-request reasoning override sent as `reasoning_effort`.",
    )

    st.divider()
    st.subheader("Chat sessions")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("Refresh sessions", key="refresh_chat_sessions"):
            try:
                st.session_state.chat_sessions_cache = _get_chat_sessions(limit=50)
            except requests.RequestException as exc:
                st.error(_requests_error_message(exc))
    with c2:
        if st.button("Delete all sessions", key="delete_all_chat_sessions"):
            try:
                _delete_all_chat_sessions()
                st.session_state.chat_sessions_cache = []
                st.session_state.messages = []
                st.session_state.chat_session_id = str(uuid.uuid4())
                st.rerun()
            except requests.RequestException as exc:
                st.error(_requests_error_message(exc))
    if not st.session_state.chat_sessions_cache:
        try:
            st.session_state.chat_sessions_cache = _get_chat_sessions(limit=50)
        except requests.RequestException:
            st.caption("No session history yet.")
    if not st.session_state.chat_sessions_cache:
        st.caption("No session history yet.")
    else:
        for item in st.session_state.chat_sessions_cache:
            sid = str(item.get("session_id") or "")
            turn_count = int(item.get("turn_count") or 0)
            col_label, col_load, col_del = st.columns([3, 1, 1])
            with col_label:
                created = _format_ts_for_sidebar(item.get("created_at"))
                updated = _format_ts_for_sidebar(item.get("updated_at"))
                st.caption(f"`{sid[:8]}…` · {turn_count} turns · 最后更新 {updated}")
            with col_load:
                if st.button(
                    "Load",
                    key=f"load_chat_session_{sid}",
                    type="primary",
                    use_container_width=True,
                    help="Restore this server session into the chat area",
                ):
                    try:
                        turns = _get_chat_session_turns(sid, limit=200)
                        st.session_state.messages = _restore_chat_messages_from_turns(turns)
                        st.session_state.chat_session_id = sid
                        st.session_state.mode = "chat"
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))
            with col_del:
                if st.button(
                    "Delete",
                    key=f"delete_chat_session_{sid}",
                    type="tertiary",
                    width='content',
                    help="Remove this session from the server",
                ):
                    try:
                        _delete_chat_session(sid)
                        if st.session_state.get("chat_session_id") == sid:
                            st.session_state.chat_session_id = str(uuid.uuid4())
                            st.session_state.messages = []
                        st.session_state.chat_sessions_cache = _get_chat_sessions(limit=50)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))

    st.divider()
    st.subheader("Recent tasks")
    if st.button("Refresh tasks", key="refresh_task_history"):
        try:
            st.session_state.task_history_cache = _get_task_history(limit=50)
        except requests.RequestException as exc:
            st.error(_requests_error_message(exc))
    if not st.session_state.task_history_cache:
        try:
            st.session_state.task_history_cache = _get_task_history(limit=50)
        except requests.RequestException:
            st.caption("None yet.")
    if not st.session_state.task_history_cache:
        st.caption("None yet.")
    else:
        for item in st.session_state.task_history_cache:
            tid = str(item.get("task_id") or "")
            label = str(item.get("question") or "")
            label = label[:40] + ("…" if len(label) > 40 else "")
            st.caption(f"`{tid[:8]}…` {label}")
            c1, c2, c3 = st.columns(3)
            with c1:
                if st.button("Refresh", key=f"hist_ref_{tid}"):
                    try:
                        rec = _get_task(tid)
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "text",
                                "content": f"Task `{tid}` status: `{rec.get('status')}`",
                            }
                        )
                        pending = rec.get("pending_review")
                        if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
                            _append_review_request_message(tid, pending)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))
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
                        st.error(_requests_error_message(exc))
            with c3:
                if st.button("Delete", key=f"hist_del_{tid}"):
                    try:
                        _delete_task(tid)
                        st.session_state.task_history_cache = _get_task_history(limit=50)
                        st.rerun()
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))

    if st.button("Clear chat history"):
        st.session_state.messages = []
        st.session_state.mode = "chat"
        st.session_state.active_task_id = None
        st.session_state.chat_session_id = str(uuid.uuid4())
        st.rerun()

tab_chat, tab_sql_jsonl = st.tabs(["Chat & tasks", "SQL generator · Codex JSONL"])

with tab_chat:
    # --- Process follow-up click (before rendering chat) ---
    if st.session_state.get("_followup_q"):
        fq = st.session_state._followup_q
        st.session_state._followup_q = None
        st.session_state.messages.append({"role": "user", "type": "text", "content": fq})
        st.session_state.mode = "task"
        _enqueue_task(fq)
        st.rerun()

    _ensure_welcome_if_empty()

    # --- Render chat (40 user-turn viewport; older rows in expander) ---
    _messages = st.session_state.messages
    _cut = _transcript_cut_for_viewport(_messages, MAX_VISIBLE_CHAT_TURNS)
    _pin_welcome = (
        _cut > 0
        and bool(_messages)
        and _messages[0].get("type") == "welcome"
    )
    _exp_lo = 1 if _pin_welcome else 0
    _exp_hi = _cut

    if _pin_welcome:
        _render_chat_message(0, _messages[0])

    if _exp_lo < _exp_hi:
        _n_hidden = _exp_hi - _exp_lo
        with st.expander(f"加载更早的对话（{_n_hidden} 条消息）", key="viewport_older_messages"):
            for _j in range(_exp_lo, _exp_hi):
                _render_chat_message(_j, _messages[_j])

    for _i in range(_cut, len(_messages)):
        _render_chat_message(_i, _messages[_i])

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
                pending_review_tid = _pending_review_task_id()
                if pending_review_tid is not None:
                    _enqueue_review_respond(pending_review_tid, user_text=text)
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

with tab_sql_jsonl:
    render_sql_generator_jsonl_panel()

