from __future__ import annotations

import uuid
from typing import Any

import requests
import streamlit as st

from app.api_client import (
    _api_url,
    _delete_all_chat_sessions,
    _delete_chat_session,
    _delete_task,
    _get_chat_session_turns,
    _get_chat_sessions,
    _get_result,
    _get_task,
    _get_task_history,
    _requests_error_message,
)
from app.streamlit_state import (
    _append_review_request_message,
    _format_ts_for_sidebar,
    _invalidate_schema_cache,
    _restore_chat_messages_from_turns,
)


def _load_runtime_status() -> dict[str, Any] | None:
    try:
        resp = requests.get(_api_url("/runtime/status"), timeout=5)
        resp.raise_for_status()
        return resp.json()
    except Exception:
        return None


def _task_card_title(question: Any) -> str:
    text = str(question or "").strip()
    return text or "Untitled task"


def _task_card_meta(item: dict[str, Any], task_id: str) -> str:
    updated = _format_ts_for_sidebar(item.get("updated_at"))
    short_id = task_id[:8] if task_id else "-"
    if updated != "-":
        return f"{updated} · task `{short_id}…`"
    return f"task `{short_id}…`"


def _runtime_summary(runtime_status: dict[str, Any] | None) -> tuple[str, list[str]]:
    if runtime_status is None:
        return "System status unavailable", []

    codex = runtime_status.get("codex") or {}
    odps = runtime_status.get("odps") or {}
    parts = [
        f"mode {runtime_status.get('app_mode', '-')}",
        f"codex {'ready' if codex.get('ready') else 'not ready'}",
        f"odps {'ready' if odps.get('ready') else 'not ready'}",
    ]
    issues: list[str] = []
    for issue in list(codex.get("issues") or []):
        message = str(issue.get("message") or "").strip()
        if message:
            issues.append(message)
    for issue in list(odps.get("issues") or []):
        message = str(issue.get("message") or "").strip()
        if message:
            issues.append(message)
    return " · ".join(parts), issues


def _render_workspace_summary() -> None:
    mode = st.session_state.get("mode", "chat")
    mode_label = "Task" if mode == "task" else "Chat"
    session_id = str(st.session_state.get("chat_session_id") or "")[:8]
    active_task_id = str(st.session_state.get("active_task_id") or "").strip()
    file_meta = st.session_state.get("file_meta")

    st.markdown('<div class="xyf-sidebar-panel">', unsafe_allow_html=True)
    st.markdown('<div class="xyf-sidebar-kicker">Workspace</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-sidebar-headline">{mode_label} mode</div>', unsafe_allow_html=True)

    st.markdown('<div class="xyf-sidebar-grid">', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="xyf-sidebar-cell">'
            '<div class="xyf-sidebar-label">Current file</div>'
            f'<div class="xyf-sidebar-value">{(file_meta or {}).get("name") or "No file uploaded"}</div>'
            '<div class="xyf-sidebar-meta">Upload CSV or Excel from the chat input below.</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    context_meta = f"session `{session_id}…`" if session_id else "session unavailable"
    if mode == "task" and active_task_id:
        context_meta = f"{context_meta} · active task `{active_task_id[:8]}…`"
    st.markdown(
        (
            '<div class="xyf-sidebar-cell">'
            '<div class="xyf-sidebar-label">Current context</div>'
            f'<div class="xyf-sidebar-value">{mode_label}</div>'
            f'<div class="xyf-sidebar-meta">{context_meta}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if file_meta:
        if st.button("Remove file", key="btn_remove_uploaded_file", use_container_width=True):
            st.session_state.file_meta = None
            _invalidate_schema_cache()
            st.session_state.pop("chat_prompt", None)
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


def _render_system_section(runtime_status: dict[str, Any] | None) -> None:
    summary, issues = _runtime_summary(runtime_status)

    st.markdown('<div class="xyf-sidebar-system">', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="xyf-sidebar-system-row">'
            '<div class="xyf-sidebar-system-title">System</div>'
            f'<div class="xyf-sidebar-system-copy">{summary}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    for issue in issues:
        st.warning(issue)

    with st.expander("Advanced settings", expanded=False):
        st.toggle("Enable MOCK", value=False, key="use_codex_mock")
        st.toggle("Show prompt debug", value=False, key="show_prompt_debug")
        st.toggle("Show chat event stream", value=True, key="show_chat_event_stream")
        st.toggle("Smart timeout", value=True, key="smart_timeout_enabled")
        if not bool(st.session_state.get("smart_timeout_enabled", True)):
            st.text_input(
                "Timeout (s)",
                key="chat_timeout_seconds",
                placeholder="e.g. 300",
                help="Used for chat requests when smart timeout is turned off.",
            )
        st.text_input(
            "Model override",
            key="codex_model_override",
            placeholder="e.g. gpt-5.4-mini",
            help="Recommended: gpt-5.4-mini",
        )
        st.text_input(
            "Reasoning effort",
            key="codex_reasoning_effort_override",
            placeholder="low / medium / high",
            help="Higher values may take longer.",
        )


def _render_recent_task_card(item: dict[str, Any]) -> None:
    task_id = str(item.get("task_id") or "").strip()
    title = _task_card_title(item.get("question"))
    meta = _task_card_meta(item, task_id)

    st.markdown('<div class="xyf-task-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-task-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-task-meta">{meta}</div>', unsafe_allow_html=True)

    primary_col, secondary_col = st.columns([1.6, 1])
    with primary_col:
        if st.button("View result", key=f"hist_res_{task_id}", use_container_width=True):
            try:
                res = _get_result(task_id)
                st.session_state.messages.append(
                    {"role": "assistant", "type": "result", "task_id": task_id, "result": res}
                )
                st.rerun()
            except requests.RequestException as exc:
                st.error(_requests_error_message(exc))
    with secondary_col:
        with st.popover("More", use_container_width=True):
            if st.button("Refresh status", key=f"hist_ref_{task_id}", use_container_width=True):
                try:
                    rec = _get_task(task_id)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "text",
                            "content": f"Task `{task_id}` status: `{rec.get('status')}`",
                        }
                    )
                    pending = rec.get("pending_review")
                    if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
                        _append_review_request_message(task_id, pending)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(_requests_error_message(exc))
            if st.button("Delete task", key=f"hist_del_{task_id}", use_container_width=True):
                try:
                    _delete_task(task_id)
                    st.session_state.task_history_cache = _get_task_history(limit=20)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(_requests_error_message(exc))
    st.markdown("</div>", unsafe_allow_html=True)


def render_sidebar() -> None:
    runtime_status = _load_runtime_status()
    with st.sidebar:
        _render_workspace_summary()
        _render_system_section(runtime_status)

        with st.expander("Session history", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                if st.button("Refresh list", key="refresh_chat_sessions", use_container_width=True, type="primary"):
                    try:
                        st.session_state.chat_sessions_cache = _get_chat_sessions(limit=50)
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))
            with c2:
                if st.button("Delete all", key="delete_all_chat_sessions", use_container_width=True):
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
                        updated = _format_ts_for_sidebar(item.get("updated_at"))
                        st.caption(f"`{sid[:8]}…` · {turn_count} turns · Last updated {updated}")
                    with col_load:
                        if st.button("Load", key=f"load_chat_session_{sid}", type="secondary", use_container_width=True):
                            try:
                                turns = _get_chat_session_turns(sid, limit=200)
                                st.session_state.messages = _restore_chat_messages_from_turns(turns)
                                st.session_state.chat_session_id = sid
                                st.session_state.mode = "chat"
                                st.rerun()
                            except requests.RequestException as exc:
                                st.error(_requests_error_message(exc))
                    with col_del:
                        if st.button("Delete", key=f"delete_chat_session_{sid}", type="tertiary", width="content"):
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
        header_col, action_col = st.columns([2.2, 1])
        with header_col:
            st.subheader("Recent tasks")
        with action_col:
            if st.button("Refresh", key="refresh_task_history", use_container_width=True):
                try:
                    st.session_state.task_history_cache = _get_task_history(limit=20)
                except requests.RequestException as exc:
                    st.error(_requests_error_message(exc))
        if not st.session_state.task_history_cache:
            try:
                st.session_state.task_history_cache = _get_task_history(limit=20)
            except requests.RequestException:
                st.caption("No recent tasks yet.")
        if not st.session_state.task_history_cache:
            st.caption("Recent tasks will appear here so you can reopen results or review status.")
        else:
            for item in st.session_state.task_history_cache[:5]:
                _render_recent_task_card(item)
