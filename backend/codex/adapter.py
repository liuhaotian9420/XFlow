"""Backward-compatible re-exports for ``codex exec`` scripts and docs."""

from __future__ import annotations

from backend.codex.errors import CodexAdapterError
from backend.codex.json_util import extract_json_array_payload as _extract_json_array_payload
from backend.codex.json_util import extract_json_payload as _extract_json_payload
from backend.codex.legacy import LegacyCodexProvider, get_legacy_codex_provider

# Historical name: one-shot CLI adapter.
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
