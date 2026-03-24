"""Select mock vs ACP vs legacy ``codex exec`` provider; manage shared ACP subprocess."""

from __future__ import annotations

import logging
import os
import shlex
import shutil
from pathlib import Path

from backend.acp.client import AcpSessionManager
from backend.acp.legacy_codex import LegacyCodexProvider
from backend.acp.mock import MockProvider
from backend.acp.provider import AcpProvider
from backend.acp.xinfei_sso import (
    codex_parent_dir_for_path_prepend,
    ensure_xinfei_sso_gate,
    resolve_codex_executable,
)
from backend.skills.registry import default_project_root

logger = logging.getLogger(__name__)

AnalysisProvider = MockProvider | AcpProvider | LegacyCodexProvider

_shared_acp_manager: AcpSessionManager | None = None


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def _parse_acp_argv() -> tuple[str, tuple[str, ...]]:
    """Resolve ACP agent argv; default to ``codex-acp``, or ``npx`` if the binary is missing."""
    raw = os.getenv("ACP_AGENT_COMMAND", "").strip()
    extra = os.getenv("ACP_AGENT_ARGS", "").strip()
    posix = os.name != "nt"
    if not raw:
        if shutil.which("codex-acp"):
            raw = "codex-acp"
        elif shutil.which("npx"):
            raw = "npx -y @zed-industries/codex-acp"
        else:
            raw = "codex-acp"
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
    """Use ACP when the agent launcher exists and backend is not forced to legacy exec."""
    forced = os.getenv("ACP_BACKEND", "").strip().lower()
    if forced in ("legacy", "exec", "codex-exec"):
        return False
    cmd, _ = _parse_acp_argv()
    if cmd == "npx":
        return shutil.which("npx") is not None
    return shutil.which(cmd) is not None


def _acp_agent_inherit_full_env() -> bool:
    """When True, pass the parent process env into the ACP agent (matches a normal shell)."""
    raw = os.getenv("ACP_AGENT_INHERIT_FULL_ENV", "true").strip().lower()
    return raw not in ("0", "false", "no", "off")


def _acp_agent_extra_env() -> dict[str, str]:
    """Env for ``codex-acp`` / ``npx``: optional full inherit + prepend Xinfei ``codex.exe`` dir on ``PATH``.

    The ACP SDK starts from a *trimmed* env then applies this mapping. Passing only ``PATH`` often
    drops variables your interactive terminal has (proxy, Node, auth helpers), which breaks
    ``npx`` or enterprise Codex — so we default to inheriting ``os.environ``.
    """
    prepend_off = os.getenv("ACP_AGENT_PATH_PREPEND", "").strip().lower() in (
        "0",
        "false",
        "no",
        "off",
    )
    codex_bin = resolve_codex_executable()
    parent: str | None = None
    if not prepend_off:
        parent = codex_parent_dir_for_path_prepend(codex_bin)
        if parent:
            logger.debug("ACP agent PATH prepend: %s", parent)

    def _apply_path_prepend(target: dict[str, str]) -> None:
        if not parent:
            return
        base_path = target.get("PATH", "")
        target["PATH"] = (
            f"{parent}{os.pathsep}{base_path}" if base_path else parent
        )

    if _acp_agent_inherit_full_env():
        # Only str values — ``os.environ`` is str on supported platforms.
        out = {k: v for k, v in os.environ.items() if isinstance(v, str)}
        _apply_path_prepend(out)
        return out

    if not parent:
        return {}
    base_path = os.environ.get("PATH", "")
    merged = f"{parent}{os.pathsep}{base_path}" if base_path else parent
    return {"PATH": merged}


def get_acp_session_manager_singleton() -> AcpSessionManager:
    """Lazily construct the process-wide ACP agent connection (stdio JSON-RPC)."""
    global _shared_acp_manager
    if _shared_acp_manager is None:
        cmd, args = _parse_acp_argv()
        timeout = int(os.getenv("CODEX_TIMEOUT_SECONDS", "120"))
        codex_bin = resolve_codex_executable()
        logger.info(
            "ACP singleton create argv=%s timeout_s=%s session_cwd=%s resolved_codex=%s",
            (cmd, *args),
            timeout,
            _acp_session_cwd(),
            codex_bin,
        )
        _shared_acp_manager = AcpSessionManager(
            cmd,
            args,
            timeout_seconds=timeout,
            session_cwd=_acp_session_cwd(),
            extra_env=_acp_agent_extra_env(),
        )
    return _shared_acp_manager


def get_provider(use_mock: bool | None = None) -> AnalysisProvider:
    """Return the analysis provider for this request (mock, ACP, or legacy Codex exec)."""
    if _effective_use_mock(use_mock):
        return MockProvider()
    codex_bin = resolve_codex_executable()
    ensure_xinfei_sso_gate(codex_bin)
    if _should_use_acp():
        retry = int(os.getenv("CODEX_RETRY_COUNT", "1"))
        return AcpProvider(
            _mgr=get_acp_session_manager_singleton(),
            retry_count=retry,
        )
    return LegacyCodexProvider(
        command=codex_bin,
        timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "60")),
        retry_count=int(os.getenv("CODEX_RETRY_COUNT", "1")),
    )


async def shutdown_providers() -> None:
    """Close shared ACP subprocess on FastAPI shutdown."""
    global _shared_acp_manager
    if _shared_acp_manager is not None:
        await _shared_acp_manager.aclose()
        _shared_acp_manager = None
