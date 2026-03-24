"""Select mock vs ACP vs legacy ``codex exec`` provider; manage shared ACP subprocess."""

from __future__ import annotations

import os
import shlex
import shutil
from pathlib import Path

from backend.acp.client import AcpSessionManager
from backend.skills.registry import default_project_root
from backend.acp.legacy_codex import LegacyCodexProvider
from backend.acp.mock import MockProvider
from backend.acp.provider import AcpProvider

AnalysisProvider = MockProvider | AcpProvider | LegacyCodexProvider

_shared_acp_manager: AcpSessionManager | None = None


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _parse_acp_argv() -> tuple[str, tuple[str, ...]]:
    raw = os.getenv("ACP_AGENT_COMMAND", "codex-acp").strip()
    extra = os.getenv("ACP_AGENT_ARGS", "").strip()
    posix = os.name != "nt"
    parts = shlex.split(raw, posix=posix) if raw else []
    if not parts:
        parts = ["codex-acp"]
    cmd = parts[0]
    more = shlex.split(extra, posix=posix) if extra else []
    args = tuple(parts[1:] + more)
    return cmd, args


def _acp_session_cwd() -> str:
    """Absolute cwd for ``session/new`` so agents (e.g. Codex) discover ``.agents/skills``."""
    raw = os.getenv("ACP_SESSION_CWD", "").strip()
    if raw:
        return str(Path(raw).expanduser().resolve())
    return str(default_project_root().resolve())


def _should_use_acp() -> bool:
    """Use ACP when the agent binary exists and backend is not forced to legacy exec."""
    forced = os.getenv("ACP_BACKEND", "").strip().lower()
    if forced in ("legacy", "exec", "codex-exec"):
        return False
    cmd, _ = _parse_acp_argv()
    resolved = shutil.which(cmd)
    return resolved is not None


def get_acp_session_manager_singleton() -> AcpSessionManager:
    """Lazily construct the process-wide ACP agent connection (stdio JSON-RPC)."""
    global _shared_acp_manager
    if _shared_acp_manager is None:
        cmd, args = _parse_acp_argv()
        timeout = int(os.getenv("CODEX_TIMEOUT_SECONDS", "120"))
        _shared_acp_manager = AcpSessionManager(
            cmd,
            args,
            timeout_seconds=timeout,
            session_cwd=_acp_session_cwd(),
        )
    return _shared_acp_manager


def get_provider(use_mock: bool | None = None) -> AnalysisProvider:
    """Return the analysis provider for this request (mock, ACP, or legacy Codex exec)."""
    if _effective_use_mock(use_mock):
        return MockProvider()
    if _should_use_acp():
        retry = int(os.getenv("CODEX_RETRY_COUNT", "1"))
        return AcpProvider(
            _mgr=get_acp_session_manager_singleton(),
            retry_count=retry,
        )
    return LegacyCodexProvider(
        command=os.getenv("CODEX_CLI_COMMAND", "codex"),
        timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "60")),
        retry_count=int(os.getenv("CODEX_RETRY_COUNT", "1")),
    )


async def shutdown_providers() -> None:
    """Close shared ACP subprocess on FastAPI shutdown."""
    global _shared_acp_manager
    if _shared_acp_manager is not None:
        await _shared_acp_manager.aclose()
        _shared_acp_manager = None
