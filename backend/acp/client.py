"""ACP client callbacks and a shared session manager (JSON-RPC stdio to an ACP agent)."""

from __future__ import annotations

import asyncio
import logging
import tempfile
from contextlib import AsyncExitStack
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any

from backend.acp.errors import CodexAdapterError

if TYPE_CHECKING:
    from acp.client.connection import ClientSideConnection

logger = logging.getLogger(__name__)

_ACP_INSTALL_HINT = (
    "Install the Agent Client Protocol SDK: uv sync  (or pip install 'agent-client-protocol>=0.8.1')."
)


@dataclass(frozen=True)
class _AcpRuntime:
    """Lazily loaded symbols from the ``acp`` package (``agent-client-protocol`` on PyPI)."""

    PROTOCOL_VERSION: Any
    spawn_agent_process: Any
    text_block: Any
    ClientSideConnection: type
    AgentMessageChunk: type
    AgentThoughtChunk: type
    AllowedOutcome: type
    PermissionOption: type
    ReadTextFileResponse: type
    RequestPermissionResponse: type
    ToolCallUpdate: type
    WriteTextFileResponse: type


_acp_cached: _AcpRuntime | None = None


def _load_acp() -> _AcpRuntime:
    """Import ``acp`` on first use so mock-only runs do not require the SDK."""
    global _acp_cached
    if _acp_cached is not None:
        return _acp_cached
    try:
        from acp import PROTOCOL_VERSION, spawn_agent_process, text_block
        from acp.client.connection import ClientSideConnection
        from acp.schema import (
            AgentMessageChunk,
            AgentThoughtChunk,
            AllowedOutcome,
            PermissionOption,
            ReadTextFileResponse,
            RequestPermissionResponse,
            ToolCallUpdate,
            WriteTextFileResponse,
        )
    except ImportError as exc:
        raise ImportError(
            f"ACP mode requires the 'agent-client-protocol' package. {_ACP_INSTALL_HINT}"
        ) from exc
    _acp_cached = _AcpRuntime(
        PROTOCOL_VERSION=PROTOCOL_VERSION,
        spawn_agent_process=spawn_agent_process,
        text_block=text_block,
        ClientSideConnection=ClientSideConnection,
        AgentMessageChunk=AgentMessageChunk,
        AgentThoughtChunk=AgentThoughtChunk,
        AllowedOutcome=AllowedOutcome,
        PermissionOption=PermissionOption,
        ReadTextFileResponse=ReadTextFileResponse,
        RequestPermissionResponse=RequestPermissionResponse,
        ToolCallUpdate=ToolCallUpdate,
        WriteTextFileResponse=WriteTextFileResponse,
    )
    return _acp_cached


class AnalysisAcpClient:
    """Minimal ACP client: auto-approve permissions, accumulate streamed agent text."""

    def __init__(self) -> None:
        self._chunks: list[str] = []

    def reset_turn_buffer(self) -> None:
        self._chunks.clear()

    def get_turn_text(self) -> str:
        return "".join(self._chunks)

    def on_connect(self, conn: Any) -> None:
        return None

    async def request_permission(
        self,
        options: list[Any],
        session_id: str,
        tool_call: Any,
        **kwargs: Any,
    ) -> Any:
        a = _load_acp()
        for opt in options:
            if opt.kind in ("allow_once", "allow_always"):
                return a.RequestPermissionResponse(
                    outcome=a.AllowedOutcome(option_id=opt.option_id)
                )
        if options:
            return a.RequestPermissionResponse(
                outcome=a.AllowedOutcome(option_id=options[0].option_id)
            )
        return a.RequestPermissionResponse(
            outcome=a.AllowedOutcome(option_id="__implicit_allow__")
        )

    async def session_update(
        self,
        session_id: str,
        update: Any,
        **kwargs: Any,
    ) -> None:
        a = _load_acp()
        if isinstance(update, (a.AgentMessageChunk, a.AgentThoughtChunk)):
            content = update.content
            if hasattr(content, "text") and isinstance(content.text, str):
                self._chunks.append(content.text)

    async def read_text_file(
        self,
        path: str,
        session_id: str,
        limit: int | None = None,
        line: int | None = None,
        **kwargs: Any,
    ) -> Any:
        a = _load_acp()
        try:
            p = Path(path)
            if p.is_file():
                text = p.read_text(encoding="utf-8", errors="replace")
                if limit is not None:
                    text = text[:limit]
                return a.ReadTextFileResponse(content=text)
        except OSError as exc:
            logger.debug("read_text_file failed for %s: %s", path, exc)
        return a.ReadTextFileResponse(content="")

    async def write_text_file(
        self, content: str, path: str, session_id: str, **kwargs: Any
    ) -> Any:
        return _load_acp().WriteTextFileResponse()

    async def ext_method(self, method: str, params: dict[str, Any]) -> dict[str, Any]:
        return {}

    async def ext_notification(self, method: str, params: dict[str, Any]) -> None:
        return None


class AcpSessionManager:
    """One long-lived ACP agent subprocess; one ACP session per logical key (e.g. task_id)."""

    def __init__(
        self,
        agent_command: str,
        agent_args: tuple[str, ...],
        *,
        subprocess_cwd: str | None = None,
        session_cwd: str | None = None,
        timeout_seconds: int = 120,
        extra_env: dict[str, str] | None = None,
    ) -> None:
        self._agent_command = agent_command
        self._agent_args = agent_args
        self._subprocess_cwd = subprocess_cwd
        self._session_cwd = session_cwd or str(Path(tempfile.gettempdir()).resolve())
        self._timeout = timeout_seconds
        self._extra_env = extra_env or {}

        self._stack: AsyncExitStack | None = None
        self._conn: ClientSideConnection | None = None  # type: ignore[valid-type]
        self._client = AnalysisAcpClient()
        self._sessions: dict[str, str] = {}
        self._ensure_lock = asyncio.Lock()
        self._prompt_lock = asyncio.Lock()

    async def aclose(self) -> None:
        """Close JSON-RPC connection and terminate the agent subprocess."""
        self._sessions.clear()
        if self._stack is not None:
            try:
                await self._stack.aclose()
            except Exception as exc:  # pragma: no cover
                logger.warning("ACP shutdown: %s", exc)
            finally:
                self._stack = None
                self._conn = None

    async def _ensure(self) -> None:
        async with self._ensure_lock:
            if self._conn is not None:
                return
            a = _load_acp()
            self._stack = AsyncExitStack()
            assert self._stack is not None
            try:
                cm = a.spawn_agent_process(
                    self._client,
                    self._agent_command,
                    *self._agent_args,
                    env=self._extra_env if self._extra_env else None,
                    cwd=self._subprocess_cwd,
                )
                self._conn, _proc = await self._stack.enter_async_context(cm)
                await self._conn.initialize(protocol_version=a.PROTOCOL_VERSION)
            except Exception:
                await self._stack.aclose()
                self._stack = None
                self._conn = None
                raise

    async def prompt_for(self, logical_session_key: str, user_text: str) -> str:
        """Send one user turn on the logical session; return concatenated agent text."""
        await self._ensure()
        a = _load_acp()
        async with self._prompt_lock:
            self._client.reset_turn_buffer()
            assert self._conn is not None
            if logical_session_key not in self._sessions:
                resp = await self._conn.new_session(cwd=self._session_cwd, mcp_servers=[])
                self._sessions[logical_session_key] = resp.session_id
            sid = self._sessions[logical_session_key]
            try:
                await asyncio.wait_for(
                    self._conn.prompt(
                        session_id=sid,
                        prompt=[a.text_block(user_text)],
                    ),
                    timeout=self._timeout,
                )
            except asyncio.TimeoutError as exc:
                raise CodexAdapterError(
                    f"ACP prompt timed out after {self._timeout}s"
                ) from exc
            text = self._client.get_turn_text().strip()
            if not text:
                raise CodexAdapterError(
                    "ACP agent returned no streamed text for this turn. "
                    "Ensure the agent speaks via agent_message_chunk updates."
                )
            return text
