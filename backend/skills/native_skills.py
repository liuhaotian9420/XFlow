"""Detect whether the configured ACP agent loads Codex-native skills from ``cwd``."""

from __future__ import annotations

import os


def acp_agent_uses_native_skills() -> bool:
    """Return True when skill text should NOT be injected into prompts (agent discovers ``.agents/skills``).

    - ``ACP_AGENT_NATIVE_SKILLS=true|false`` overrides detection.
    - Otherwise, if ``ACP_AGENT_COMMAND`` contains ``codex`` (e.g. ``codex-acp``), assume native skills.
    """
    raw = os.getenv("ACP_AGENT_NATIVE_SKILLS", "").strip().lower()
    if raw in ("1", "true", "yes"):
        return True
    if raw in ("0", "false", "no"):
        return False
    cmd = os.getenv("ACP_AGENT_COMMAND", "codex-acp").strip().lower()
    return "codex" in cmd
