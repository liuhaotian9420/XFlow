"""Select mock vs real ``codex exec`` provider."""

from __future__ import annotations

import os

from backend.codex.legacy import LegacyCodexProvider
from backend.codex.mock import MockProvider
from backend.codex.xinfei_sso import ensure_xinfei_sso_gate, resolve_codex_executable

AnalysisProvider = MockProvider | LegacyCodexProvider


def _effective_use_mock(explicit: bool | None) -> bool:
    if explicit is not None:
        return explicit
    return os.getenv("CODEX_MOCK", "true").lower() == "true"


def get_provider(
    use_mock: bool | None = None,
    *,
    model: str | None = None,
    reasoning_effort: str | None = None,
) -> AnalysisProvider:
    """Return the analysis provider for this request (mock or codex exec)."""
    if _effective_use_mock(use_mock):
        return MockProvider()
    codex_bin = resolve_codex_executable()
    ensure_xinfei_sso_gate(codex_bin)
    return LegacyCodexProvider(
        command=codex_bin,
        timeout_seconds=int(os.getenv("CODEX_TIMEOUT_SECONDS", "180")),
        retry_count=int(os.getenv("CODEX_RETRY_COUNT", "1")),
        model=(model or "").strip() or None,
        reasoning_effort=(reasoning_effort or "").strip() or None,
    )


async def shutdown_providers() -> None:
    """Compatibility hook for FastAPI lifespan."""
    return None
