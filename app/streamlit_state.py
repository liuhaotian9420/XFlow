from __future__ import annotations

import os
import uuid
from datetime import datetime
from typing import Any

import streamlit as st

from app.api_client import _post_create_review_request

WELCOME_MESSAGE_MARKDOWN = (
    "**你好呀，欢迎和我对话，你可以**\n\n"
    "- 1. 直接提问，先用自然语言和数据对话。\n"
    "- 2. 可以通过聊天框上传 **CSV / Excel** 文件。\n\n"
    "准备好后，直接在下方输入问题。"
)

ERROR_KIND_CHAT = "chat"
ERROR_KIND_CREATE_TASK = "create_task"
ERROR_KIND_CONFIRM_TASK = "confirm_task"
ERROR_KIND_REVISE_PLAN = "revise_plan"
ERROR_KIND_REVIEW_RESPOND = "review_respond"

MAX_VISIBLE_CHAT_TURNS = 40


def _default_use_codex_mock() -> bool:
    app_mode = os.getenv("APP_MODE", "").strip().lower()
    if app_mode == "mock":
        return False
    if app_mode == "real":
        return False
    return os.getenv("CODEX_MOCK", "false").lower() == "true"


def _init_state() -> None:
    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("file_meta", None)
    st.session_state.setdefault("task_history", [])
    st.session_state.setdefault("chat_sessions_cache", [])
    st.session_state.setdefault("task_history_cache", [])
    st.session_state.setdefault("_followup_q", None)
    st.session_state.setdefault("mode", "chat")
    st.session_state.setdefault("chat_session_id", str(uuid.uuid4()))
    st.session_state.setdefault("active_task_id", None)
    st.session_state.setdefault("schema_profile", None)
    st.session_state.setdefault("schema_profile_for", None)
    st.session_state.setdefault("codex_model_override", "")
    st.session_state.setdefault("codex_reasoning_effort_override", "")
    st.session_state.setdefault("show_prompt_debug", False)
    st.session_state.setdefault("show_chat_event_stream", True)
    st.session_state.setdefault("smart_timeout_enabled", True)
    st.session_state.setdefault("chat_timeout_seconds", "")
    if "use_codex_mock" not in st.session_state:
        st.session_state.use_codex_mock = _default_use_codex_mock()


def _ensure_welcome_if_empty() -> None:
    if st.session_state.messages:
        return
    st.session_state.messages = [
        {"role": "assistant", "type": "welcome", "content": WELCOME_MESSAGE_MARKDOWN}
    ]


def _assistant_error_dict(
    title: str,
    detail: str,
    kind: str | None = None,
) -> dict[str, Any]:
    msg: dict[str, Any] = {
        "role": "assistant",
        "type": "error",
        "title": (title or "Error").strip() or "Error",
        "detail": (detail or "").strip(),
    }
    if kind:
        msg["kind"] = kind
    return msg


def _invalidate_schema_cache() -> None:
    st.session_state.pop("schema_profile", None)
    st.session_state.pop("schema_profile_for", None)


def _parse_task_command(text: str) -> tuple[bool, str]:
    stripped = text.strip()
    lower = stripped.lower()
    if lower.startswith("/task"):
        rest = stripped[5:].lstrip()
        return True, rest
    return False, stripped


def _pending_plan_task_id() -> str | None:
    for m in reversed(st.session_state.messages):
        if m.get("type") != "plan_review":
            continue
        tid = m.get("task_id")
        if tid and not st.session_state.get(f"review_done_{tid}"):
            return str(tid)
    return None


def _pending_review_task_id() -> str | None:
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


def _append_task_history(task_id: str, question: str) -> None:
    hist = st.session_state.task_history
    hist.append({"task_id": task_id, "question": question[:120]})
    st.session_state.task_history = hist[-20:]


def _extract_review_plan_fields(review: dict[str, Any]) -> tuple[str | None, str | None, list[dict[str, Any]]]:
    suggested_plan = review.get("suggested_plan")
    if not isinstance(suggested_plan, dict):
        return None, None, []
    completeness = suggested_plan.get("completeness") or {}
    recommended_action = completeness.get("recommended_action")
    completeness_status = completeness.get("status")
    ambiguities = list(suggested_plan.get("ambiguities") or [])
    return (
        str(recommended_action).strip() if recommended_action is not None else None,
        str(completeness_status).strip() if completeness_status is not None else None,
        ambiguities,
    )


def _append_review_request_message(task_id: str, review: dict[str, Any]) -> None:
    review_id = str(review.get("review_id") or "").strip()
    if not review_id:
        return
    for m in reversed(st.session_state.messages):
        if m.get("type") != "review_request":
            continue
        if str(m.get("review_id") or "").strip() == review_id:
            return
    recommended_action, completeness_status, ambiguities = _extract_review_plan_fields(review)
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
            "suggested_plan": review.get("suggested_plan"),
            "recommended_action": recommended_action,
            "completeness_status": completeness_status,
            "ambiguities": ambiguities,
            "resolved": False,
        }
    )


def _ensure_confirmation_review(task_id: str) -> None:
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
                    "input_tokens": turn.get("input_tokens"),
                    "output_tokens": turn.get("output_tokens"),
                    "cached_input_tokens": turn.get("cached_input_tokens"),
                    "codex_exec_elapsed_s": turn.get("codex_exec_elapsed_s"),
                    "codex_spawn_elapsed_s": turn.get("codex_spawn_elapsed_s"),
                    "codex_ttft_elapsed_s": turn.get("codex_ttft_elapsed_s"),
                    "codex_generation_elapsed_s": turn.get("codex_generation_elapsed_s"),
                    "codex_teardown_elapsed_s": turn.get("codex_teardown_elapsed_s"),
                    "provider_elapsed_s": turn.get("provider_elapsed_s"),
                    "provider_overhead_elapsed_s": turn.get("provider_overhead_elapsed_s"),
                    "prompt_build_elapsed_s": turn.get("prompt_build_elapsed_s"),
                    "api_elapsed_s": turn.get("api_elapsed_s"),
                    "stream_events": [],
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


def _format_ts_for_sidebar(iso: str | None) -> str:
    if iso is None or not str(iso).strip():
        return "-"
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
    user_idxs = _user_text_message_indices(messages)
    if len(user_idxs) <= max_turns:
        return 0
    return int(user_idxs[-max_turns])
