"""Free-form chat with the assistant (no structured task plan)."""

from __future__ import annotations

import logging
import os
import time
import uuid

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.chat_store import (
    delete_all_sessions,
    delete_session,
    list_session_turns,
    list_sessions,
    save_chat_turn,
)
from backend.codex.errors import CodexAdapterError
from backend.codex.factory import get_provider
from backend.codex.mock import MockProvider
from backend.codex.xinfei_sso import is_xinfei_enterprise_binary, resolve_codex_executable
from backend.observability import log_event

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _effective_reasoning_effort(
    reasoning_effort: str | None,
    think_level: str | None,
) -> str | None:
    value = (reasoning_effort or "").strip() or (think_level or "").strip()
    return value or None


def _auth_hint_for_chat_error(detail: str, *, codex_bin: str) -> str | None:
    low = detail.lower()
    auth_like = any(
        token in low
        for token in (
            "not logged in",
            "enterprise sso",
            "expired",
            "refresh token",
            "access token",
            "unauthorized",
            "401",
            "forbidden",
            "403",
            "stream disconnected",
            "no last agent message",
        )
    )
    if not auth_like:
        return None
    if is_xinfei_enterprise_binary(codex_bin):
        return (
            "Likely Xinfei Codex auth issue (not logged in or session expired). "
            "Run `codex login status` and, if needed, "
            "`codex login --enterprise-sso` (use the same CODEX_HOME as backend)."
        )
    return (
        "Likely Codex auth/session issue. Run `codex login status` and re-login if needed."
    )


class ChatMessage(BaseModel):
    """One turn in the client-supplied history."""

    role: str = Field(..., description="Typically 'user' or 'assistant'.")
    content: str = ""


class ChatRequest(BaseModel):
    message: str
    session_id: str | None = None
    history: list[ChatMessage] = Field(default_factory=list)
    file_context: dict | None = None
    use_mock: bool | None = None


class ChatResponse(BaseModel):
    session_id: str
    turn_id: str
    reply: str
    prompt_chars: int | None = None
    history_turns_used: int | None = None
    debug_prompt: str | None = None
    codex_exec_elapsed_s: float | None = None
    codex_spawn_elapsed_s: float | None = None
    codex_ttft_elapsed_s: float | None = None
    codex_generation_elapsed_s: float | None = None
    codex_teardown_elapsed_s: float | None = None
    provider_elapsed_s: float | None = None
    provider_overhead_elapsed_s: float | None = None
    prompt_build_elapsed_s: float | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_input_tokens: int | None = None
    skill_hints: list[str] | None = None
    api_elapsed_s: float | None = None
    runtime_vendor: str | None = None
    runtime_binary: str | None = None


@router.post("/chat", response_model=ChatResponse)
async def chat_message(
    payload: ChatRequest,
    use_mock: bool | None = Query(
        default=None,
        description="If set, overrides body use_mock / CODEX_MOCK for this request.",
    ),
    model: str | None = Query(
        default=None,
        description="Optional per-request Codex model override (e.g. gpt-5.4-mini).",
    ),
    reasoning_effort: str | None = Query(
        default=None,
        description="Optional per-request reasoning effort override (low/medium/high).",
    ),
    think_level: str | None = Query(
        default=None,
        description="Alias of reasoning_effort.",
    ),
    include_prompt_debug: bool = Query(
        default=False,
        description="When true, include full rendered chat prompt in response for debugging.",
    ),
) -> ChatResponse:
    """Plain-text assistant reply using the same Codex/Mock stack as planning."""
    text = payload.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="message must not be empty")

    chat_id = str(uuid.uuid4())
    session_id = (payload.session_id or "").strip() or str(uuid.uuid4())
    turn_id = str(uuid.uuid4())
    history = [m.model_dump() for m in payload.history]
    explicit = use_mock if use_mock is not None else payload.use_mock
    use_mock_flag = _effective_use_mock(explicit)
    effective_reasoning = _effective_reasoning_effort(reasoning_effort, think_level)
    adapter = get_provider(
        use_mock_flag,
        model=model,
        reasoning_effort=effective_reasoning,
    )

    resolved_codex = resolve_codex_executable()
    adapter_command = str(getattr(adapter, "command", "") or "").strip() or resolved_codex
    provider_name = type(adapter).__name__
    extra = ""
    if hasattr(adapter, "command"):
        extra = f" codex_cli={adapter.command!r}"
    logger.info(
        "CHAT begin chat_id=%s provider=%s resolved_codex=%s model=%r reasoning=%r history_turns=%d msg_chars=%d%s",
        chat_id,
        provider_name,
        resolved_codex,
        (model or "").strip() or None,
        effective_reasoning,
        len(history),
        len(text),
        extra,
    )
    t0 = time.perf_counter()
    provider_elapsed_s: float | None = None
    codex_exec_elapsed_s: float | None = None
    is_fallback = False
    error_text: str | None = None
    try:
        p0 = time.perf_counter()
        reply = await adapter.chat(
            message=text,
            history=history,
            file_context=payload.file_context,
            task_id=chat_id,
        )
        provider_elapsed_s = time.perf_counter() - p0
        codex_exec_elapsed_s = getattr(adapter, "last_exec_elapsed_s", None)
        prompt_build_elapsed_s = getattr(adapter, "last_chat_prompt_build_elapsed_s", None)
        provider_overhead_elapsed_s: float | None = None
        if (
            isinstance(provider_elapsed_s, (int, float))
            and isinstance(codex_exec_elapsed_s, (int, float))
        ):
            provider_overhead_elapsed_s = max(
                0.0, float(provider_elapsed_s) - float(codex_exec_elapsed_s)
            )
        log_event(chat_id, "chat", "chat_ok", {"use_mock": use_mock_flag})
        logger.info(
            "CHAT done chat_id=%s provider=%s elapsed_s=%.2f provider_elapsed_s=%.2f codex_exec_elapsed_s=%s prompt_build_elapsed_s=%s provider_overhead_elapsed_s=%s reply_chars=%d",
            chat_id,
            provider_name,
            time.perf_counter() - t0,
            provider_elapsed_s or -1.0,
            f"{codex_exec_elapsed_s:.2f}" if codex_exec_elapsed_s is not None else "n/a",
            f"{prompt_build_elapsed_s:.2f}" if prompt_build_elapsed_s is not None else "n/a",
            (
                f"{provider_overhead_elapsed_s:.2f}"
                if provider_overhead_elapsed_s is not None
                else "n/a"
            ),
            len(reply or ""),
        )
    except (CodexAdapterError, Exception) as exc:
        error_text = f"{type(exc).__name__}: {exc!s}"
        logger.exception(
            "CHAT failed chat_id=%s after %.2fs use_mock=%s explicit_query=%s provider=%s resolved_codex=%s",
            chat_id,
            time.perf_counter() - t0,
            use_mock_flag,
            explicit,
            provider_name,
            resolved_codex,
        )
        if not use_mock_flag and explicit is False:
            hint = _auth_hint_for_chat_error(error_text or "", codex_bin=adapter_command)
            save_chat_turn(
                {
                    "turn_id": turn_id,
                    "session_id": session_id,
                    "chat_id": chat_id,
                    "user_message": text,
                    "history_turns": len(history),
                    "use_mock": use_mock_flag,
                    "model": (model or "").strip() or None,
                    "reasoning_effort": effective_reasoning,
                    "provider_name": provider_name,
                    "reply_text": None,
                    "is_fallback": False,
                    "error_text": error_text,
                    "prompt_chars": getattr(adapter, "last_prompt_chars", None),
                    "input_tokens": getattr(adapter, "last_input_tokens", None),
                    "output_tokens": getattr(adapter, "last_output_tokens", None),
                    "cached_input_tokens": getattr(
                        adapter, "last_cached_input_tokens", None
                    ),
                    "codex_exec_elapsed_s": getattr(adapter, "last_exec_elapsed_s", None),
                    "codex_spawn_elapsed_s": getattr(adapter, "last_spawn_elapsed_s", None),
                    "codex_ttft_elapsed_s": getattr(adapter, "last_ttft_elapsed_s", None),
                    "codex_generation_elapsed_s": getattr(
                        adapter, "last_generation_elapsed_s", None
                    ),
                    "codex_teardown_elapsed_s": getattr(
                        adapter, "last_teardown_elapsed_s", None
                    ),
                    "provider_elapsed_s": provider_elapsed_s,
                    "provider_overhead_elapsed_s": None,
                    "prompt_build_elapsed_s": getattr(
                        adapter, "last_chat_prompt_build_elapsed_s", None
                    ),
                    "api_elapsed_s": time.perf_counter() - t0,
                    "debug_prompt": (
                        getattr(adapter, "last_chat_prompt_text", None)
                        if include_prompt_debug
                        else None
                    ),
                }
            )
            raise HTTPException(
                status_code=502,
                detail=(
                    "Chat generation failed (mock fallback disabled). "
                    f"{type(exc).__name__}: {exc!s}. "
                    "Check server logs for the full traceback, verify Codex CLI auth/config, "
                    "or re-enable mock in the UI."
                    + (f" Hint: {hint}" if hint else "")
                ),
            ) from exc
        reply = await MockProvider().chat(
            message=text,
            history=history,
            file_context=payload.file_context,
            task_id=chat_id,
        )
        codex_exec_elapsed_s = None
        is_fallback = True
        log_event(
            chat_id,
            "chat",
            "chat_fallback",
            {"error": str(exc), "use_mock": True},
        )

    provider_overhead_elapsed_s_out: float | None = None
    if (
        isinstance(provider_elapsed_s, (int, float))
        and isinstance(codex_exec_elapsed_s, (int, float))
    ):
        provider_overhead_elapsed_s_out = max(
            0.0, float(provider_elapsed_s) - float(codex_exec_elapsed_s)
        )
    runtime_vendor: str | None = None
    runtime_binary: str | None = None
    if is_fallback:
        runtime_vendor = "mock-fallback"
    elif use_mock_flag:
        runtime_vendor = "mock"
    else:
        runtime_vendor = (
            "xinfei-codex"
            if is_xinfei_enterprise_binary(adapter_command)
            else "native-codex"
        )
        runtime_binary = adapter_command

    response = ChatResponse(
        session_id=session_id,
        turn_id=turn_id,
        reply=reply,
        prompt_chars=getattr(adapter, "last_prompt_chars", None),
        history_turns_used=len(history[-20:]),
        debug_prompt=(
            getattr(adapter, "last_chat_prompt_text", None)
            if include_prompt_debug
            else None
        ),
        codex_exec_elapsed_s=codex_exec_elapsed_s,
        codex_spawn_elapsed_s=getattr(adapter, "last_spawn_elapsed_s", None),
        codex_ttft_elapsed_s=getattr(adapter, "last_ttft_elapsed_s", None),
        codex_generation_elapsed_s=getattr(adapter, "last_generation_elapsed_s", None),
        codex_teardown_elapsed_s=getattr(adapter, "last_teardown_elapsed_s", None),
        provider_elapsed_s=provider_elapsed_s,
        provider_overhead_elapsed_s=provider_overhead_elapsed_s_out,
        prompt_build_elapsed_s=getattr(adapter, "last_chat_prompt_build_elapsed_s", None),
        input_tokens=getattr(adapter, "last_input_tokens", None),
        output_tokens=getattr(adapter, "last_output_tokens", None),
        cached_input_tokens=getattr(adapter, "last_cached_input_tokens", None),
        skill_hints=getattr(adapter, "last_skill_hints", None),
        api_elapsed_s=time.perf_counter() - t0,
        runtime_vendor=runtime_vendor,
        runtime_binary=runtime_binary,
    )
    save_chat_turn(
        {
            "turn_id": turn_id,
            "session_id": session_id,
            "chat_id": chat_id,
            "user_message": text,
            "history_turns": len(history),
            "use_mock": use_mock_flag,
            "model": (model or "").strip() or None,
            "reasoning_effort": effective_reasoning,
            "provider_name": provider_name,
            "reply_text": response.reply,
            "is_fallback": is_fallback,
            "error_text": error_text,
            "prompt_chars": response.prompt_chars,
            "input_tokens": response.input_tokens,
            "output_tokens": response.output_tokens,
            "cached_input_tokens": response.cached_input_tokens,
            "codex_exec_elapsed_s": response.codex_exec_elapsed_s,
            "codex_spawn_elapsed_s": response.codex_spawn_elapsed_s,
            "codex_ttft_elapsed_s": response.codex_ttft_elapsed_s,
            "codex_generation_elapsed_s": response.codex_generation_elapsed_s,
            "codex_teardown_elapsed_s": response.codex_teardown_elapsed_s,
            "provider_elapsed_s": response.provider_elapsed_s,
            "provider_overhead_elapsed_s": response.provider_overhead_elapsed_s,
            "prompt_build_elapsed_s": response.prompt_build_elapsed_s,
            "api_elapsed_s": response.api_elapsed_s,
            "debug_prompt": response.debug_prompt,
        }
    )
    return response


class ChatSessionMeta(BaseModel):
    session_id: str
    created_at: str
    updated_at: str
    turn_count: int


class ChatTurnRecord(BaseModel):
    turn_id: str
    session_id: str
    chat_id: str
    created_at: str
    user_message: str
    history_turns: int
    use_mock: int
    model: str | None = None
    reasoning_effort: str | None = None
    provider_name: str | None = None
    reply_text: str | None = None
    is_fallback: int
    error_text: str | None = None
    prompt_chars: int | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None
    cached_input_tokens: int | None = None
    codex_exec_elapsed_s: float | None = None
    codex_spawn_elapsed_s: float | None = None
    codex_ttft_elapsed_s: float | None = None
    codex_generation_elapsed_s: float | None = None
    codex_teardown_elapsed_s: float | None = None
    provider_elapsed_s: float | None = None
    provider_overhead_elapsed_s: float | None = None
    prompt_build_elapsed_s: float | None = None
    api_elapsed_s: float | None = None
    debug_prompt: str | None = None


@router.get("/chat/sessions", response_model=list[ChatSessionMeta])
async def get_chat_sessions(
    limit: int = Query(default=50, ge=1, le=500),
) -> list[ChatSessionMeta]:
    rows = list_sessions(limit=limit)
    return [ChatSessionMeta.model_validate(r) for r in rows]


@router.get("/chat/sessions/{session_id}/turns", response_model=list[ChatTurnRecord])
async def get_chat_session_turns(
    session_id: str,
    limit: int = Query(default=200, ge=1, le=2000),
) -> list[ChatTurnRecord]:
    rows = list_session_turns(session_id=session_id, limit=limit)
    return [ChatTurnRecord.model_validate(r) for r in rows]


@router.delete("/chat/sessions/{session_id}")
async def delete_chat_session(session_id: str) -> dict[str, int]:
    deleted = delete_session(session_id=session_id)
    return {"deleted": deleted}


@router.delete("/chat/sessions")
async def delete_chat_sessions() -> dict[str, int]:
    deleted = delete_all_sessions()
    return {"deleted": deleted}
