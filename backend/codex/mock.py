"""Backward-compatible re-export of the mock analysis provider."""

from __future__ import annotations

from backend.acp.mock import MockAdapter, MockProvider

__all__ = ["MockAdapter", "MockProvider"]
