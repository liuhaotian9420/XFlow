"""Free-form chat with the assistant (no structured task plan)."""

from __future__ import annotations

import logging
import os
import time
import uuid

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.acp.errors import CodexAdapterError
from backend.acp.factory import get_provider
from backend.acp.mock import MockProvider
from backend.acp.provider import AcpProvider
from backend.acp.xinfei_sso import resolve_codex_executable
from backend.observability import log_event

router = APIRouter(tags=["chat"])
logger = logging.getLogger(__name__)


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


class ChatMessage(BaseModel):
    """One turn in the client-supplied history."""

    role: str = Field(..., description="Typically 'user' or 'assistant'.")
    content: str = ""


class ChatRequest(BaseModel):
    message: str
    history: list[ChatMessage] = Field(default_factory=list)
    file_context: dict | None = None
    use_mock: bool | None = None


class ChatResponse(BaseModel):
    reply: str


@router.post("/chat", response_model=ChatResponse)
async def chat_message(
    payload: ChatRequest,
    use_mock: bool | None = Query(
        default=None,
        description="If set, overrides body use_mock / CODEX_MOCK for this request.",
    ),
) -> ChatResponse:
    """Plain-text assistant reply using the same Codex/Mock stack as planning."""
    text = payload.message.strip()
    if not text:
        raise HTTPException(status_code=400, detail="message must not be empty")

    chat_id = str(uuid.uuid4())
    history = [m.model_dump() for m in payload.history]
    explicit = use_mock if use_mock is not None else payload.use_mock
    use_mock_flag = _effective_use_mock(explicit)
    adapter = get_provider(use_mock_flag)

    resolved_codex = resolve_codex_executable()
    provider_name = type(adapter).__name__
    extra = ""
    if isinstance(adapter, AcpProvider):
        extra = f" acp_spawn_argv={adapter.acp_spawn_argv!r}"
    elif hasattr(adapter, "command"):
        extra = f" legacy_cli={adapter.command!r}"
    logger.info(
        "CHAT begin chat_id=%s provider=%s resolved_codex=%s history_turns=%d msg_chars=%d%s",
        chat_id,
        provider_name,
        resolved_codex,
        len(history),
        len(text),
        extra,
    )
    t0 = time.perf_counter()
    try:
        reply = await adapter.chat(
            message=text,
            history=history,
            file_context=payload.file_context,
            task_id=chat_id,
        )
        log_event(chat_id, "chat", "chat_ok", {"use_mock": use_mock_flag})
        logger.info(
            "CHAT done chat_id=%s provider=%s elapsed_s=%.2f reply_chars=%d",
            chat_id,
            provider_name,
            time.perf_counter() - t0,
            len(reply or ""),
        )
    except (CodexAdapterError, Exception) as exc:
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
            raise HTTPException(
                status_code=502,
                detail=(
                    "Chat generation failed (mock fallback disabled). "
                    f"{type(exc).__name__}: {exc!s}. "
                    "Check server logs for the full traceback; try ACP_AGENT_INHERIT_FULL_ENV=true "
                    "(default), ACP_BACKEND=legacy, or re-enable mock in the UI."
                ),
            ) from exc
        reply = await MockProvider().chat(
            message=text,
            history=history,
            file_context=payload.file_context,
            task_id=chat_id,
        )
        log_event(
            chat_id,
            "chat",
            "chat_fallback",
            {"error": str(exc), "use_mock": True},
        )

    return ChatResponse(reply=reply)
