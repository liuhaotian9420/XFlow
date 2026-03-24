"""List repository skills (Codex-style ``SKILL.md`` under ``.agents/skills``)."""

from __future__ import annotations

from fastapi import APIRouter
from pydantic import BaseModel, Field

from backend.skills import get_registry

router = APIRouter(prefix="/skills", tags=["skills"])


class SkillMetaResponse(BaseModel):
    """Serializable skill metadata (no body — progressive disclosure)."""

    name: str = Field(description="Skill id from SKILL.md frontmatter")
    description: str = Field(default="", description="When the skill should trigger")
    path: str = Field(description="Absolute path to SKILL.md")


@router.get("", response_model=list[SkillMetaResponse])
def list_skills() -> list[SkillMetaResponse]:
    """Return all discovered skills under ``.agents/skills``."""
    reg = get_registry()
    return [
        SkillMetaResponse(
            name=m.name,
            description=m.description,
            path=str(m.path.resolve()),
        )
        for m in reg.list_skills()
    ]
