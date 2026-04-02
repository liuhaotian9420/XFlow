"""Free-form chat with the assistant (no structured task plan)."""

from __future__ import annotations

import json
import logging
import os
import time
import uuid
from collections.abc import AsyncIterator
from typing import Any

from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

from backend.chat_jobs import CHAT_JOBS
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
from backend.mock_scenarios import next_stream_events
from backend.codex.xinfei_sso import is_xinfei_enterprise_binary, resolve_codex_executable
from backend.observability import log_event
from backend.runtime_config import default_use_mock
from backend.runtime_timeout import resolve_timeout_seconds

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return default_use_mock()


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


class ChatExecutionContext(BaseModel):
    payload: ChatRequest
    use_mock: bool | None = None
    model: str | None = None
    reasoning_effort: str | None = None
    think_level: str | None = None
    timeout_seconds: int | None = None
    auto_timeout: bool = False
    include_prompt_debug: bool = False
    chat_id: str
    session_id: str
    turn_id: str
    history: list[dict[str, str]]
    explicit: bool | None = None
    use_mock_flag: bool
    effective_reasoning: str | None = None
    provider_name: str
    adapter_command: str
    resolved_codex: str
    adapter: Any


class ChatJobSnapshot(BaseModel):
    job_id: str
    status: str
    created_at: float
    updated_at: float
    session_id: str
    turn_id: str
    chat_id: str
    latest_text: str = ""
    latest_reasoning_text: str = ""
    latest_command: dict[str, Any] | None = None
    stream_events: list[dict[str, Any]] = Field(default_factory=list)
    final_reply: str | None = None
    timing: dict[str, Any] = Field(default_factory=dict)
    usage: dict[str, Any] = Field(default_factory=dict)
    runtime_vendor: str | None = None
    runtime_binary: str | None = None
    error: str | None = None


def _chat_runtime_fields(
    *,
    adapter: object,
    is_fallback: bool,
    use_mock_flag: bool,
) -> tuple[str | None, str | None]:
    resolved_codex = resolve_codex_executable()
    adapter_command = str(getattr(adapter, "command", "") or "").strip() or resolved_codex
    if is_fallback:
        return "mock-fallback", None
    if use_mock_flag:
        return "mock", None
    return (
        "xinfei-codex" if is_xinfei_enterprise_binary(adapter_command) else "native-codex",
        adapter_command,
    )


def _sse_json(event: dict[str, object]) -> str:
    return f"data: {json.dumps(event, ensure_ascii=False)}\n\n"


def _reply_debug_summary(reply: str) -> str:
    text = (reply or "").strip()
    if not text:
        return "reply=empty"
    if not (text.startswith("{") and text.endswith("}")):
        return f"reply=plain chars={len(text)}"
    try:
        obj = json.loads(text)
    except json.JSONDecodeError:
        return f"reply=json_like_but_invalid chars={len(text)}"
    if not isinstance(obj, dict):
        return f"reply=json_non_object type={type(obj).__name__}"
    result = obj.get("result")
    if not isinstance(result, dict):
        return "reply=json_object result=none"
    artifacts = result.get("artifacts")
    artifacts_n = len(artifacts) if isinstance(artifacts, list) else 0
    html_n = 0
    path_n = 0
    if isinstance(artifacts, list):
        for a in artifacts:
            if not isinstance(a, dict):
                continue
            mime = str(a.get("mime") or "").strip().lower()
            if mime == "text/html":
                html_n += 1
            if isinstance(a.get("path"), str) and a.get("path", "").strip():
                path_n += 1
    return (
        "reply=json_object "
        f"result_keys={sorted(result.keys())} artifacts={artifacts_n} "
        f"html_artifacts={html_n} artifacts_with_path={path_n}"
    )


def _save_chat_turn_record(
    *,
    turn_id: str,
    session_id: str,
    chat_id: str,
    user_message: str,
    history: list[dict],
    use_mock_flag: bool,
    model: str | None,
    effective_reasoning: str | None,
    provider_name: str,
    reply_text: str | None,
    is_fallback: bool,
    error_text: str | None,
    adapter: object,
    provider_elapsed_s: float | None,
    provider_overhead_elapsed_s: float | None,
    api_elapsed_s: float,
    include_prompt_debug: bool,
) -> None:
    save_chat_turn(
        {
            "turn_id": turn_id,
            "session_id": session_id,
            "chat_id": chat_id,
            "user_message": user_message,
            "history_turns": len(history),
            "use_mock": use_mock_flag,
            "model": (model or "").strip() or None,
            "reasoning_effort": effective_reasoning,
            "provider_name": provider_name,
            "reply_text": reply_text,
            "is_fallback": is_fallback,
            "error_text": error_text,
            "prompt_chars": getattr(adapter, "last_prompt_chars", None),
            "input_tokens": getattr(adapter, "last_input_tokens", None),
            "output_tokens": getattr(adapter, "last_output_tokens", None),
            "cached_input_tokens": getattr(adapter, "last_cached_input_tokens", None),
            "codex_exec_elapsed_s": getattr(adapter, "last_exec_elapsed_s", None),
            "codex_spawn_elapsed_s": getattr(adapter, "last_spawn_elapsed_s", None),
            "codex_ttft_elapsed_s": getattr(adapter, "last_ttft_elapsed_s", None),
            "codex_generation_elapsed_s": getattr(
                adapter, "last_generation_elapsed_s", None
            ),
            "codex_teardown_elapsed_s": getattr(adapter, "last_teardown_elapsed_s", None),
            "provider_elapsed_s": provider_elapsed_s,
            "provider_overhead_elapsed_s": provider_overhead_elapsed_s,
            "prompt_build_elapsed_s": getattr(
                adapter, "last_chat_prompt_build_elapsed_s", None
            ),
            "api_elapsed_s": api_elapsed_s,
            "debug_prompt": (
                getattr(adapter, "last_chat_prompt_text", None)
                if include_prompt_debug
                else None
            ),
        }
    )


def _build_chat_context(
    *,
    payload: ChatRequest,
    use_mock: bool | None,
    model: str | None,
    reasoning_effort: str | None,
    think_level: str | None,
    timeout_seconds: int | None,
    auto_timeout: bool,
    include_prompt_debug: bool,
) -> ChatExecutionContext:
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
    effective_timeout_seconds = resolve_timeout_seconds(
        auto_timeout=auto_timeout,
        explicit_timeout_seconds=timeout_seconds,
        route_kind="chat",
        model=model,
        reasoning_effort=effective_reasoning,
        env_default_timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "180")),
    )
    adapter = get_provider(
        use_mock_flag,
        model=model,
        reasoning_effort=effective_reasoning,
        timeout_seconds=effective_timeout_seconds,
    )
    resolved_codex = resolve_codex_executable()
    adapter_command = str(getattr(adapter, "command", "") or "").strip() or resolved_codex
    provider_name = type(adapter).__name__
    return ChatExecutionContext(
        payload=payload,
        use_mock=use_mock,
        model=model,
        reasoning_effort=reasoning_effort,
        think_level=think_level,
        timeout_seconds=timeout_seconds,
        auto_timeout=auto_timeout,
        include_prompt_debug=include_prompt_debug,
        chat_id=chat_id,
        session_id=session_id,
        turn_id=turn_id,
        history=history,
        explicit=explicit,
        use_mock_flag=use_mock_flag,
        effective_reasoning=effective_reasoning,
        provider_name=provider_name,
        adapter_command=adapter_command,
        resolved_codex=resolved_codex,
        adapter=adapter,
    )


async def _iter_chat_events(ctx: ChatExecutionContext) -> AsyncIterator[dict[str, Any]]:
    text = ctx.payload.message.strip()
    provider_elapsed_s: float | None = None
    provider_overhead_elapsed_s: float | None = None
    error_text: str | None = None
    is_fallback = False
    final_reply: str | None = None
    final_emitted = False
    error_emitted = False
    saved = False
    t0 = time.perf_counter()
    try:
        p0 = time.perf_counter()
        if isinstance(ctx.adapter, MockProvider):
            scripted_events = next_stream_events(ctx.session_id)
            provider_elapsed_s = time.perf_counter() - p0
            runtime_vendor, runtime_binary = _chat_runtime_fields(
                adapter=ctx.adapter,
                is_fallback=False,
                use_mock_flag=ctx.use_mock_flag,
            )
            if scripted_events:
                for raw_event in scripted_events:
                    event = dict(raw_event)
                    event["chat_id"] = ctx.chat_id
                    event["session_id"] = ctx.session_id
                    event["turn_id"] = ctx.turn_id
                    if str(event.get("type") or "").strip().lower() == "final":
                        final_reply = str(event.get("reply") or "").strip() or None
                        final_emitted = True
                        event["runtime_vendor"] = runtime_vendor
                        event["runtime_binary"] = runtime_binary
                        event.setdefault("timing", {})
                        if isinstance(event["timing"], dict):
                            event["timing"]["provider_elapsed_s"] = provider_elapsed_s
                            event["timing"]["api_elapsed_s"] = time.perf_counter() - t0
                    yield event
                if final_emitted:
                    return
            reply = await ctx.adapter.chat(
                message=text,
                history=ctx.history,
                file_context=ctx.payload.file_context,
                task_id=ctx.session_id,
            )
            final_event = {
                "type": "final",
                "chat_id": ctx.chat_id,
                "session_id": ctx.session_id,
                "turn_id": ctx.turn_id,
                "reply": reply,
                "timing": {
                    "provider_elapsed_s": provider_elapsed_s,
                    "api_elapsed_s": time.perf_counter() - t0,
                },
                "runtime_vendor": runtime_vendor,
                "runtime_binary": runtime_binary,
            }
            logger.info(
                "[CHATDBG][backend][stream_final][mock] chat_id=%s turn_id=%s %s",
                ctx.chat_id,
                ctx.turn_id,
                _reply_debug_summary(reply),
            )
            final_reply = reply
            final_emitted = True
            yield final_event
            return

        async for event in ctx.adapter.stream_chat(
            message=text,
            history=ctx.history,
            file_context=ctx.payload.file_context,
            chat_id=ctx.chat_id,
        ):
            event_type = str(event.get("type") or "").strip().lower()
            if event_type == "error":
                error_text = str(event.get("error") or "").strip() or error_text
                error_emitted = True
            if event_type == "final":
                provider_elapsed_s = time.perf_counter() - p0
                codex_exec_elapsed_s = getattr(ctx.adapter, "last_exec_elapsed_s", None)
                if (
                    isinstance(provider_elapsed_s, (int, float))
                    and isinstance(codex_exec_elapsed_s, (int, float))
                ):
                    provider_overhead_elapsed_s = max(
                        0.0, float(provider_elapsed_s) - float(codex_exec_elapsed_s)
                    )
                runtime_vendor, runtime_binary = _chat_runtime_fields(
                    adapter=ctx.adapter,
                    is_fallback=False,
                    use_mock_flag=ctx.use_mock_flag,
                )
                final_reply = str(event.get("reply") or "").strip() or None
                event["session_id"] = ctx.session_id
                event["turn_id"] = ctx.turn_id
                event["runtime_vendor"] = runtime_vendor
                event["runtime_binary"] = runtime_binary
                event.setdefault("timing", {})
                if isinstance(event["timing"], dict):
                    event["timing"]["provider_elapsed_s"] = provider_elapsed_s
                    event["timing"]["provider_overhead_elapsed_s"] = provider_overhead_elapsed_s
                    event["timing"]["api_elapsed_s"] = time.perf_counter() - t0
                logger.info(
                    "[CHATDBG][backend][stream_final] chat_id=%s turn_id=%s %s",
                    ctx.chat_id,
                    ctx.turn_id,
                    _reply_debug_summary(str(event.get("reply") or "")),
                )
                final_emitted = True
            yield event

        if final_reply is None and error_text is None:
            error_text = "Stream ended without a final reply."
            yield {
                "type": "error",
                "chat_id": ctx.chat_id,
                "session_id": ctx.session_id,
                "turn_id": ctx.turn_id,
                "error": error_text,
            }
            error_emitted = True
    except (CodexAdapterError, Exception) as exc:
        error_text = f"{type(exc).__name__}: {exc!s}"
        logger.exception(
            "CHAT stream failed chat_id=%s after %.2fs use_mock=%s explicit_query=%s provider=%s resolved_codex=%s",
            ctx.chat_id,
            time.perf_counter() - t0,
            ctx.use_mock_flag,
            ctx.explicit,
            ctx.provider_name,
            ctx.resolved_codex,
        )
        if not final_emitted and not ctx.use_mock_flag and ctx.explicit is not False:
            is_fallback = True
            mock_provider = MockProvider()
            reply = await mock_provider.chat(
                message=text,
                history=ctx.history,
                file_context=ctx.payload.file_context,
                task_id=ctx.chat_id,
            )
            final_reply = reply
            runtime_vendor, runtime_binary = _chat_runtime_fields(
                adapter=ctx.adapter,
                is_fallback=True,
                use_mock_flag=ctx.use_mock_flag,
            )
            fallback_event = {
                "type": "final",
                "chat_id": ctx.chat_id,
                "session_id": ctx.session_id,
                "turn_id": ctx.turn_id,
                "reply": reply,
                "runtime_vendor": runtime_vendor,
                "runtime_binary": runtime_binary,
                "error": error_text,
                "timing": {
                    "provider_elapsed_s": provider_elapsed_s,
                    "api_elapsed_s": time.perf_counter() - t0,
                },
            }
            logger.info(
                "[CHATDBG][backend][stream_final][fallback] chat_id=%s turn_id=%s %s",
                ctx.chat_id,
                ctx.turn_id,
                _reply_debug_summary(reply),
            )
            final_emitted = True
            yield fallback_event
            return
        if not final_emitted and not error_emitted:
            yield {
                "type": "error",
                "chat_id": ctx.chat_id,
                "session_id": ctx.session_id,
                "turn_id": ctx.turn_id,
                "error": error_text,
                "runtime_vendor": (
                    "xinfei-codex"
                    if is_xinfei_enterprise_binary(ctx.adapter_command)
                    else "native-codex"
                )
                if not ctx.use_mock_flag
                else "mock",
                "runtime_binary": ctx.adapter_command if not ctx.use_mock_flag else None,
            }
            error_emitted = True
    finally:
        if not saved:
            _save_chat_turn_record(
                turn_id=ctx.turn_id,
                session_id=ctx.session_id,
                chat_id=ctx.chat_id,
                user_message=text,
                history=ctx.history,
                use_mock_flag=ctx.use_mock_flag,
                model=ctx.model,
                effective_reasoning=ctx.effective_reasoning,
                provider_name=ctx.provider_name,
                reply_text=final_reply,
                is_fallback=is_fallback,
                error_text=error_text,
                adapter=ctx.adapter,
                provider_elapsed_s=provider_elapsed_s,
                provider_overhead_elapsed_s=provider_overhead_elapsed_s,
                api_elapsed_s=time.perf_counter() - t0,
                include_prompt_debug=ctx.include_prompt_debug,
            )
            saved = True


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
    timeout_seconds: int | None = Query(
        default=None,
        ge=1,
        le=3600,
        description="Optional per-request Codex subprocess timeout in seconds.",
    ),
    auto_timeout: bool = Query(
        default=False,
        alias="autoTimeout",
        description="If true, ignore timeout_seconds and estimate timeout from historical Codex runtimes.",
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
    effective_timeout_seconds = resolve_timeout_seconds(
        auto_timeout=auto_timeout,
        explicit_timeout_seconds=timeout_seconds,
        route_kind="chat",
        model=model,
        reasoning_effort=effective_reasoning,
        env_default_timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "180")),
    )
    adapter = get_provider(
        use_mock_flag,
        model=model,
        reasoning_effort=effective_reasoning,
        timeout_seconds=effective_timeout_seconds,
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
            _save_chat_turn_record(
                turn_id=turn_id,
                session_id=session_id,
                chat_id=chat_id,
                user_message=text,
                history=history,
                use_mock_flag=use_mock_flag,
                model=model,
                effective_reasoning=effective_reasoning,
                provider_name=provider_name,
                reply_text=None,
                is_fallback=False,
                error_text=error_text,
                adapter=adapter,
                provider_elapsed_s=provider_elapsed_s,
                provider_overhead_elapsed_s=None,
                api_elapsed_s=time.perf_counter() - t0,
                include_prompt_debug=include_prompt_debug,
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
    _save_chat_turn_record(
        turn_id=turn_id,
        session_id=session_id,
        chat_id=chat_id,
        user_message=text,
        history=history,
        use_mock_flag=use_mock_flag,
        model=model,
        effective_reasoning=effective_reasoning,
        provider_name=provider_name,
        reply_text=response.reply,
        is_fallback=is_fallback,
        error_text=error_text,
        adapter=adapter,
        provider_elapsed_s=response.provider_elapsed_s,
        provider_overhead_elapsed_s=response.provider_overhead_elapsed_s,
        api_elapsed_s=response.api_elapsed_s or 0.0,
        include_prompt_debug=include_prompt_debug,
    )
    return response


@router.post("/chat/stream")
async def chat_message_stream(
    payload: ChatRequest,
    use_mock: bool | None = Query(default=None),
    model: str | None = Query(default=None),
    reasoning_effort: str | None = Query(default=None),
    think_level: str | None = Query(default=None),
    timeout_seconds: int | None = Query(default=None, ge=1, le=3600),
    auto_timeout: bool = Query(default=False, alias="autoTimeout"),
    include_prompt_debug: bool = Query(default=False),
) -> StreamingResponse:
    ctx = _build_chat_context(
        payload=payload,
        use_mock=use_mock,
        model=model,
        reasoning_effort=reasoning_effort,
        think_level=think_level,
        timeout_seconds=timeout_seconds,
        auto_timeout=auto_timeout,
        include_prompt_debug=include_prompt_debug,
    )

    async def _event_gen():
        async for event in _iter_chat_events(ctx):
            yield _sse_json(event)

    return StreamingResponse(_event_gen(), media_type="text/event-stream")


@router.post("/chat/jobs", response_model=ChatJobSnapshot)
async def create_chat_job(
    payload: ChatRequest,
    use_mock: bool | None = Query(default=None),
    model: str | None = Query(default=None),
    reasoning_effort: str | None = Query(default=None),
    think_level: str | None = Query(default=None),
    timeout_seconds: int | None = Query(default=None, ge=1, le=3600),
    auto_timeout: bool = Query(default=False, alias="autoTimeout"),
    include_prompt_debug: bool = Query(default=False),
) -> ChatJobSnapshot:
    ctx = _build_chat_context(
        payload=payload,
        use_mock=use_mock,
        model=model,
        reasoning_effort=reasoning_effort,
        think_level=think_level,
        timeout_seconds=timeout_seconds,
        auto_timeout=auto_timeout,
        include_prompt_debug=include_prompt_debug,
    )

    # We need the id before constructing the async runner closure.
    job_id = str(uuid.uuid4())

    async def _runner() -> None:
        async for event in _iter_chat_events(ctx):
            CHAT_JOBS.append_event(job_id, event)

    snapshot = CHAT_JOBS.create_job(
        session_id=ctx.session_id,
        turn_id=ctx.turn_id,
        chat_id=ctx.chat_id,
        runner=_runner,
        job_id=job_id,
    )
    CHAT_JOBS.append_event(
        job_id,
        {
            "type": "job.created",
            "session_id": ctx.session_id,
            "turn_id": ctx.turn_id,
            "chat_id": ctx.chat_id,
        },
    )
    out = CHAT_JOBS.get_snapshot(job_id)
    if out is None:
        raise HTTPException(status_code=500, detail="Failed to create chat job")
    return ChatJobSnapshot.model_validate(out)


@router.get("/chat/jobs/{job_id}", response_model=ChatJobSnapshot)
async def get_chat_job(job_id: str) -> ChatJobSnapshot:
    snapshot = CHAT_JOBS.get_snapshot(job_id)
    if snapshot is None:
        raise HTTPException(status_code=404, detail="Chat job not found")
    return ChatJobSnapshot.model_validate(snapshot)


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
