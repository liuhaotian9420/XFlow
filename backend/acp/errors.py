"""Shared errors for analysis providers (legacy Codex CLI and ACP)."""

from __future__ import annotations


class CodexAdapterError(RuntimeError):
    """Raised when an LLM / agent provider interaction fails."""
