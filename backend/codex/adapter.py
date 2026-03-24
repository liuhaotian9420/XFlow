"""Backward-compatible re-exports for ``codex exec`` scripts and docs."""

from __future__ import annotations

from backend.acp.errors import CodexAdapterError
from backend.acp.json_util import extract_json_array_payload as _extract_json_array_payload
from backend.acp.json_util import extract_json_payload as _extract_json_payload
from backend.acp.legacy_codex import LegacyCodexProvider, get_legacy_codex_provider

# Historical name: always the legacy one-shot CLI adapter (see ``get_provider`` for ACP).
CodexAdapter = LegacyCodexProvider


def get_adapter() -> LegacyCodexProvider:
    """Return the process-wide legacy Codex CLI adapter (``codex exec``)."""
    return get_legacy_codex_provider()


__all__ = [
    "CodexAdapter",
    "CodexAdapterError",
    "get_adapter",
    "_extract_json_array_payload",
    "_extract_json_payload",
]
