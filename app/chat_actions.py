from __future__ import annotations

from typing import Any

import requests
import streamlit as st

from app.api_client import (
    _ensure_schema_profile,
    _post_chat,
    _post_review_respond,
    _post_revise,
    _post_run_task,
    _post_task_bytes,
    _stream_chat,
    _requests_error_message,
)
from app.streamlit_state import (
    ERROR_KIND_CHAT,
    ERROR_KIND_CONFIRM_TASK,
    ERROR_KIND_CREATE_TASK,
    ERROR_KIND_REVIEW_RESPOND,
    ERROR_KIND_REVISE_PLAN,
    _append_review_request_message,
    _append_task_history,
    _assistant_error_dict,
    _chat_history_upto,
    _ensure_confirmation_review,
)


def _enqueue_task(question: str) -> None:
    meta = st.session_state.file_meta
    if not meta:
        st.session_state.messages.append(
            {
                "role": "assistant",
                "type": "text",
                "content": "Please attach a CSV or Excel file first using the paperclip in the chat bar.",
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
    st.session_state.messages.append(
        {
            "role": "assistant",
            "type": "thinking",
            "action": "chat_reply",
            "user_message": user_message.strip(),
        }
    )


def _enqueue_revise_plan(task_id: str, instruction: str) -> None:
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
    question = msg["question"]
    meta = st.session_state.file_meta
    if not meta:
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "text",
            "content": "The file was removed before the task could be created.",
        }
        return
    try:
        with st.spinner("Generating analysis plan..."):
            resp = _post_task_bytes(meta["name"], meta["data"], meta["type"], question)
        tid = resp["task_id"]
        plan = resp["plan"]
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "plan_review",
            "task_id": tid,
            "plan": plan,
        }
        pending = resp.get("pending_review")
        if isinstance(pending, dict) and str(pending.get("state") or "").lower() == "pending":
            _append_review_request_message(tid, pending)
        else:
            try:
                _ensure_confirmation_review(tid)
            except requests.RequestException:
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
    task_id = msg["task_id"]
    final_plan = msg.get("final_plan")
    try:
        with st.spinner("Running analysis..."):
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
                {"role": "assistant", "type": "task_done_confirm", "task_id": task_id}
            )
        else:
            st.session_state.messages[msg_index] = {
                "role": "assistant",
                "type": "text",
                "content": f"Run submitted but no result is on record yet (status={rec.get('status')}).",
            }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Execution failed",
            _requests_error_message(exc),
            kind=ERROR_KIND_CONFIRM_TASK,
        )
    st.rerun()


def _execute_chat_reply(msg: dict[str, Any], msg_index: int) -> None:
    user_text = msg.get("user_message", "")
    history = _chat_history_upto(msg_index)
    file_ctx = _ensure_schema_profile()
    try:
        stream_events: list[dict[str, Any]] = []
        latest_agent_text = ""
        latest_reasoning_text = ""
        latest_command: dict[str, Any] | None = None
        final_event: dict[str, Any] | None = None
        error_event: dict[str, Any] | None = None
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "chat_stream_debug",
            "content": "",
            "status_text": "Waiting for Codex events...",
            "stream_events": stream_events,
            "latest_agent_text": latest_agent_text,
            "latest_reasoning_text": latest_reasoning_text,
            "latest_command": latest_command,
        }
        with st.spinner("Thinking..."):
            for event in _stream_chat(user_text, history, file_ctx):
                stream_events.append(event)
                event_type = str(event.get("type") or "").strip().lower()
                if event_type == "agent.message.completed":
                    latest_agent_text = str(event.get("text") or "").strip()
                elif event_type == "reasoning.completed":
                    latest_reasoning_text = str(event.get("text") or "").strip()
                elif event_type == "command.completed":
                    latest_command = {
                        "command": event.get("command"),
                        "exit_code": event.get("exit_code"),
                        "output_preview": event.get("output_preview"),
                    }
                elif event_type == "final":
                    final_event = event
                elif event_type == "error":
                    error_event = event

                st.session_state.messages[msg_index] = {
                    "role": "assistant",
                    "type": "chat_stream_debug",
                    "content": latest_agent_text,
                    "status_text": (
                        "Final response received."
                        if final_event is not None
                        else f"Streaming event: {event_type or 'unknown'}"
                    ),
                    "stream_events": list(stream_events),
                    "latest_agent_text": latest_agent_text,
                    "latest_reasoning_text": latest_reasoning_text,
                    "latest_command": latest_command,
                }

        if final_event is None:
            detail = str((error_event or {}).get("error") or "Stream ended without a final reply.")
            st.session_state.messages[msg_index] = _assistant_error_dict(
                "Chat failed",
                detail,
                kind=ERROR_KIND_CHAT,
            )
            st.rerun()
            return

        session_id = final_event.get("session_id")
        if isinstance(session_id, str) and session_id.strip():
            st.session_state.chat_session_id = session_id.strip()
            st.session_state.chat_sessions_cache = []
        timing = final_event.get("timing") if isinstance(final_event.get("timing"), dict) else {}
        usage = final_event.get("usage") if isinstance(final_event.get("usage"), dict) else {}
        reply = str(final_event.get("reply") or "").strip() or "(empty reply)"
        st.session_state.messages[msg_index] = {
            "role": "assistant",
            "type": "chat_response",
            "content": reply,
            "debug_prompt": final_event.get("debug_prompt"),
            "prompt_chars": final_event.get("prompt_chars"),
            "history_turns_used": len(history[-20:]),
            "input_tokens": usage.get("input_tokens"),
            "output_tokens": usage.get("output_tokens"),
            "cached_input_tokens": usage.get("cached_input_tokens"),
            "codex_exec_elapsed_s": timing.get("codex_exec_elapsed_s"),
            "codex_spawn_elapsed_s": timing.get("codex_spawn_elapsed_s"),
            "codex_ttft_elapsed_s": timing.get("codex_ttft_elapsed_s"),
            "codex_generation_elapsed_s": timing.get("codex_generation_elapsed_s"),
            "codex_teardown_elapsed_s": timing.get("codex_teardown_elapsed_s"),
            "provider_elapsed_s": timing.get("provider_elapsed_s"),
            "provider_overhead_elapsed_s": timing.get("provider_overhead_elapsed_s"),
            "prompt_build_elapsed_s": timing.get("prompt_build_elapsed_s"),
            "api_elapsed_s": timing.get("api_elapsed_s") or final_event.get("_client_elapsed_s"),
            "runtime_vendor": final_event.get("runtime_vendor"),
            "runtime_binary": final_event.get("runtime_binary"),
            "stream_events": list(stream_events),
            "latest_reasoning_text": latest_reasoning_text,
            "latest_command": latest_command,
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Chat failed",
            _requests_error_message(exc),
            kind=ERROR_KIND_CHAT,
        )
    st.rerun()


def _execute_revise_plan(msg: dict[str, Any], msg_index: int) -> None:
    task_id = str(msg["task_id"])
    instruction = msg.get("instruction", "")
    try:
        with st.spinner("Revising plan..."):
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
            "content": "The plan has been updated from your feedback. Review the plan card above, or add more changes.",
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Could not revise plan",
            _requests_error_message(exc),
            kind=ERROR_KIND_REVISE_PLAN,
        )
    st.rerun()


def _execute_review_respond(msg: dict[str, Any], msg_index: int) -> None:
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
        with st.spinner("Submitting review response..."):
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
                "Your input has been applied to the current plan."
                if user_text
                else "Your review choice has been recorded."
            ),
        }
    except requests.RequestException as exc:
        st.session_state.messages[msg_index] = _assistant_error_dict(
            "Could not respond to review",
            _requests_error_message(exc),
            kind=ERROR_KIND_REVIEW_RESPOND,
        )
    st.rerun()
