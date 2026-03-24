"""Map logical skill ids to optional prompt injection bodies."""

from __future__ import annotations

from backend.skills.registry import get_registry


def skill_instructions_for_prompt(skill_name: str, *, inject: bool) -> str | None:
    """Return ``SKILL.md`` body for prepending to prompts, or ``None`` when injection is off."""
    if not inject:
        return None
    content = get_registry().get_skill(skill_name)
    return content.body if content else None
