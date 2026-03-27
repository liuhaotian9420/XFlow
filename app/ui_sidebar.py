from __future__ import annotations

import time
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
    cached = st.session_state.get("_runtime_status_cache")
    expires_at = float(st.session_state.get("_runtime_status_cache_expires_at") or 0.0)
    now = time.time()
    if isinstance(cached, dict) and now < expires_at:
        return cached
    try:
        resp = requests.get(_api_url("/runtime/status"), timeout=5)
        resp.raise_for_status()
        payload = resp.json()
        st.session_state["_runtime_status_cache"] = payload
        st.session_state["_runtime_status_cache_expires_at"] = now + 10.0
        return payload
    except Exception:
        return None


def _task_card_title(question: Any) -> str:
    text = str(question or "").strip()
    return text or "未命名任务"


def _task_card_meta(item: dict[str, Any], task_id: str) -> str:
    updated = _format_ts_for_sidebar(item.get("updated_at"))
    short_id = task_id[:8] if task_id else "-"
    if updated != "-":
        return f"{updated} · 任务 `{short_id}…`"
    return f"任务 `{short_id}…`"


def _runtime_summary(runtime_status: dict[str, Any] | None) -> tuple[str, list[str]]:
    if runtime_status is None:
        return "系统状态暂时不可用", []

    codex = runtime_status.get("codex") or {}
    odps = runtime_status.get("odps") or {}
    parts = [
        f"模式 {runtime_status.get('app_mode', '-')}",
        f"Codex {'已就绪' if codex.get('ready') else '未就绪'}",
        f"ODPS {'已就绪' if odps.get('ready') else '未就绪'}",
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
    mode_label = "任务模式" if mode == "task" else "对话模式"
    session_id = str(st.session_state.get("chat_session_id") or "")[:8]
    active_task_id = str(st.session_state.get("active_task_id") or "").strip()
    file_meta = st.session_state.get("file_meta")

    st.markdown('<div class="xyf-sidebar-panel">', unsafe_allow_html=True)
    st.markdown('<div class="xyf-sidebar-kicker">工作区概览</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-sidebar-headline">{mode_label}</div>', unsafe_allow_html=True)

    st.markdown('<div class="xyf-sidebar-grid">', unsafe_allow_html=True)
    st.markdown(
        (
            '<div class="xyf-sidebar-cell">'
            '<div class="xyf-sidebar-label">当前文件</div>'
            f'<div class="xyf-sidebar-value">{(file_meta or {}).get("name") or "尚未上传文件"}</div>'
            '<div class="xyf-sidebar-meta">请在下方对话输入框上传 CSV 或 Excel 文件。</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )

    context_meta = f"会话 `{session_id}…`" if session_id else "会话暂不可用"
    if mode == "task" and active_task_id:
        context_meta = f"{context_meta} · 当前任务 `{active_task_id[:8]}…`"
    st.markdown(
        (
            '<div class="xyf-sidebar-cell">'
            '<div class="xyf-sidebar-label">当前上下文</div>'
            f'<div class="xyf-sidebar-value">{mode_label}</div>'
            f'<div class="xyf-sidebar-meta">{context_meta}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    if file_meta:
        if st.button("移除文件", key="btn_remove_uploaded_file", use_container_width=True):
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
            f'<div class="xyf-sidebar-system-title">系统状态{"🟢" if len(issues) == 0 else "🟡" if len(issues) < 2 else "🔴"}</div>'
            f'<div class="xyf-sidebar-system-copy">{summary}</div>'
            "</div>"
        ),
        unsafe_allow_html=True,
    )
    st.markdown("</div>", unsafe_allow_html=True)

    for issue in issues:
        st.warning(issue)

    with st.expander("高级设置", expanded=False):
        st.toggle("启用 MOCK（本地模拟）", value=False, key="use_codex_mock")
        st.toggle("显示提示词调试信息", value=False, key="show_prompt_debug")
        st.toggle("显示对话事件流", value=True, key="show_chat_event_stream")
        st.toggle("智能控时", value=True, key="smart_timeout_enabled")
        if not bool(st.session_state.get("smart_timeout_enabled", True)):
            st.text_input(
                "超时时间（秒）",
                key="chat_timeout_seconds",
                placeholder="例如 300",
                help="关闭智能超时后，聊天请求将使用这里填写的秒数。",
            )
        st.text_input(
            "模型覆盖",
            key="codex_model_override",
            placeholder="e.g. gpt-5.4-mini",
            help="推荐填写 gpt-5.4-mini。",
        )
        st.text_input(
            "推理强度",
            key="codex_reasoning_effort_override",
            placeholder="low / medium / high",
            help="可选 low / medium / high，强度越高通常越耗时。",
        )


def _render_recent_task_card(item: dict[str, Any]) -> None:
    task_id = str(item.get("task_id") or "").strip()
    title = _task_card_title(item.get("question"))
    meta = _task_card_meta(item, task_id)

    # st.markdown('<div class="xyf-task-card">', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-task-title">{title}</div>', unsafe_allow_html=True)
    st.markdown(f'<div class="xyf-task-meta">{meta}</div>', unsafe_allow_html=True)

    primary_col, secondary_col = st.columns([1.6, 1])
    with primary_col:
        if st.button("查看结果", key=f"hist_res_{task_id}", use_container_width=True):
            try:
                res = _get_result(task_id)
                st.session_state.messages.append(
                    {"role": "assistant", "type": "result", "task_id": task_id, "result": res}
                )
                st.rerun()
            except requests.RequestException as exc:
                st.error(_requests_error_message(exc))
    with secondary_col:
        with st.popover("更多", use_container_width=True):
            if st.button("刷新状态", key=f"hist_ref_{task_id}", use_container_width=True):
                try:
                    rec = _get_task(task_id)
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "text",
                            "content": f"任务 `{task_id}` 当前状态：`{rec.get('status')}`",
                        }
                    )
                    pending = rec.get("pending_review")
                    if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
                        _append_review_request_message(task_id, pending)
                    st.rerun()
                except requests.RequestException as exc:
                    st.error(_requests_error_message(exc))
            if st.button("删除任务", key=f"hist_del_{task_id}", use_container_width=True):
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
        # _render_workspace_summary()
        _render_system_section(runtime_status)

        with st.expander("会话历史", expanded=False):
            c1, c2 = st.columns(2)
            with c1:
                if st.button("刷新列表", key="refresh_chat_sessions", use_container_width=True, type="primary"):
                    try:
                        st.session_state.chat_sessions_cache = _get_chat_sessions(limit=50)
                    except requests.RequestException as exc:
                        st.error(_requests_error_message(exc))
            with c2:
                if st.button("删除全部", key="delete_all_chat_sessions", use_container_width=True):
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
                    st.caption("暂无会话历史。")
            if not st.session_state.chat_sessions_cache:
                st.caption("暂无会话历史。")
            else:
                for item in st.session_state.chat_sessions_cache:
                    sid = str(item.get("session_id") or "")
                    turn_count = int(item.get("turn_count") or 0)
                    col_label, col_load, col_del = st.columns([3, 1, 1])
                    with col_label:
                        updated = _format_ts_for_sidebar(item.get("updated_at"))
                        st.caption(f"`{sid[:8]}…` · {turn_count} 轮对话 · 最近更新 {updated}")
                    with col_load:
                        if st.button("加载", key=f"load_chat_session_{sid}", type="secondary", use_container_width=True):
                            try:
                                turns = _get_chat_session_turns(sid, limit=200)
                                st.session_state.messages = _restore_chat_messages_from_turns(turns)
                                st.session_state.chat_session_id = sid
                                st.session_state.mode = "chat"
                                st.rerun()
                            except requests.RequestException as exc:
                                st.error(_requests_error_message(exc))
                    with col_del:
                        if st.button("删除", key=f"delete_chat_session_{sid}", type="tertiary", width="content"):
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
            st.subheader("最近任务")
        with action_col:
            if st.button("刷新", key="refresh_task_history", use_container_width=True):
                try:
                    st.session_state.task_history_cache = _get_task_history(limit=20)
                except requests.RequestException as exc:
                    st.error(_requests_error_message(exc))
        if not st.session_state.task_history_cache:
            try:
                st.session_state.task_history_cache = _get_task_history(limit=20)
            except requests.RequestException:
                st.caption("暂无最近任务。")
        if not st.session_state.task_history_cache:
            st.caption("这里会显示最近执行过的任务，方便继续查看结果或回看状态。")
        else:
            for item in st.session_state.task_history_cache[:5]:
                _render_recent_task_card(item)
