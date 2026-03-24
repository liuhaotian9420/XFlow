"""Free-form chat with the assistant (no structured task plan)."""

from __future__ import annotations

import os
import uuid

from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel, Field

from backend.acp.errors import CodexAdapterError
from backend.acp.factory import get_provider
from backend.acp.mock import MockProvider
from backend.observability import log_event

router = APIRouter(tags=["chat"])


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

    try:
        reply = await adapter.chat(
            message=text,
            history=history,
            file_context=payload.file_context,
            task_id=chat_id,
        )
        log_event(chat_id, "chat", "chat_ok", {"use_mock": use_mock_flag})
    except (CodexAdapterError, Exception) as exc:
        if not use_mock_flag and explicit is False:
            raise HTTPException(
                status_code=502,
                detail=f"Chat generation failed (mock fallback disabled): {exc}",
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
