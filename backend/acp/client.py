"""ACP client callbacks and a shared session manager (JSON-RPC stdio to an ACP agent)."""

from __future__ import annotations

import asyncio
import logging
import os
import sys
import tempfile
import time
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


def _acp_stderr_transport_kwargs() -> dict[str, Any]:
    """Map ``ACP_AGENT_STDERR`` to ``spawn_stdio_transport`` kwargs.

    The SDK defaults to ``stderr=PIPE``. If the agent is chatty on stderr and nothing
    drains the pipe, the child **blocks** and the client looks stuck on "Thinking…".
    """
    raw = os.getenv("ACP_AGENT_STDERR", "inherit").strip().lower()
    if raw in ("pipe", "1", "true", "yes"):
        return {}
    if raw in ("null", "none", "discard", "devnull"):
        return {"stderr": asyncio.subprocess.DEVNULL}
    # inherit parent's stderr → logs appear next to uvicorn; avoids pipe deadlock
    return {"stderr": None}


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
        else:
            logger.debug(
                "ACP session_update session_id=%s type=%s",
                session_id[:16] if session_id else "",
                type(update).__name__,
            )

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

    @property
    def spawn_argv(self) -> tuple[str, ...]:
        """ACP launcher argv (for logs): e.g. ``npx``, ``-y``, ``@zed-industries/codex-acp``."""
        return (self._agent_command, *self._agent_args)

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
                argv = (self._agent_command, *self._agent_args)
                tk = _acp_stderr_transport_kwargs()
                logger.info(
                    "ACP spawning agent argv=%s cwd=%s stderr_mode=%s",
                    argv,
                    self._subprocess_cwd,
                    "pipe(default-sdk)"
                    if not tk
                    else ("inherit" if tk.get("stderr") is None else "DEVNULL"),
                )
                t0 = time.perf_counter()
                cm = a.spawn_agent_process(
                    self._client,
                    self._agent_command,
                    *self._agent_args,
                    env=self._extra_env if self._extra_env else None,
                    cwd=self._subprocess_cwd,
                    transport_kwargs=tk or None,
                )
                self._conn, _proc = await self._stack.enter_async_context(cm)
                await self._conn.initialize(protocol_version=a.PROTOCOL_VERSION)
                dt = time.perf_counter() - t0
                pid = getattr(_proc, "pid", None)
                logger.info(
                    "ACP agent ready pid=%s initialize_ok in %.2fs",
                    pid,
                    dt,
                )
            except NotImplementedError as exc:
                await self._stack.aclose()
                self._stack = None
                self._conn = None
                if sys.platform == "win32":
                    loop = asyncio.get_running_loop()
                    raise CodexAdapterError(
                        "ACP cannot spawn a subprocess on this Windows asyncio loop "
                        f"({type(loop).__name__}). asyncio.create_subprocess_exec is only "
                        "implemented on WindowsProactorEventLoop. Ensure the backend package "
                        "is imported as ``backend`` (so ``backend/__init__.py`` sets "
                        "WindowsProactorEventLoopPolicy before the loop starts), restart "
                        "uvicorn without an alternate entry that skips that import, or set "
                        "ACP_BACKEND=legacy to use ``codex exec`` instead."
                    ) from exc
                raise
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
                logger.info(
                    "ACP new_session logical_key=%r cwd=%s",
                    logical_session_key,
                    self._session_cwd,
                )
                t_ns = time.perf_counter()
                resp = await self._conn.new_session(cwd=self._session_cwd, mcp_servers=[])
                self._sessions[logical_session_key] = resp.session_id
                logger.info(
                    "ACP new_session done session_id=%s in %.2fs",
                    resp.session_id[:16] if resp.session_id else "",
                    time.perf_counter() - t_ns,
                )
            sid = self._sessions[logical_session_key]
            logger.info(
                "ACP prompt start session=%s… prompt_chars=%s timeout_s=%s",
                sid[:16] if sid else "",
                len(user_text),
                self._timeout,
            )
            t_prompt = time.perf_counter()
            try:
                await asyncio.wait_for(
                    self._conn.prompt(
                        session_id=sid,
                        prompt=[a.text_block(user_text)],
                    ),
                    timeout=self._timeout,
                )
            except asyncio.TimeoutError as exc:
                logger.error(
                    "ACP prompt TIMEOUT after %ss session=%s…",
                    self._timeout,
                    sid[:16] if sid else "",
                )
                raise CodexAdapterError(
                    f"ACP prompt timed out after {self._timeout}s"
                ) from exc
            dt = time.perf_counter() - t_prompt
            text = self._client.get_turn_text().strip()
            logger.info(
                "ACP prompt end session=%s… wall_s=%.2f reply_chars=%s",
                sid[:16] if sid else "",
                dt,
                len(text),
            )
            if not text:
                raise CodexAdapterError(
                    "ACP agent returned no streamed text for this turn. "
                    "Ensure the agent speaks via agent_message_chunk updates."
                )
            return text
