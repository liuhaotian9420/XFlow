"""Load Codex-style ``SKILL.md`` files from ``.agents/skills`` for prompt injection."""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path

logger = logging.getLogger(__name__)

# Logical ids (must match ``name`` in each SKILL.md frontmatter).
SKILL_ANALYSIS_PLANNER = "analysis-planner"
SKILL_DATA_CHAT = "data-chat"
SKILL_PLAN_REVISER = "plan-reviser"


def default_project_root() -> Path:
    """Repository root (``xyf-competition-mvp/``): three parents up from this file."""
    return Path(__file__).resolve().parent.parent.parent


def default_skills_root() -> Path:
    return default_project_root() / ".agents" / "skills"


@dataclass(frozen=True)
class SkillMeta:
    """Skill discovery metadata (progressive disclosure: no body)."""

    name: str
    description: str
    path: Path


@dataclass(frozen=True)
class SkillContent:
    """Full skill: metadata plus instruction body after YAML frontmatter."""

    meta: SkillMeta
    body: str


def _parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split leading ``---`` YAML-like frontmatter from markdown body."""
    stripped = text.lstrip("\ufeff")
    if not stripped.startswith("---"):
        return {}, stripped
    parts = stripped.split("---", 2)
    if len(parts) < 3:
        return {}, stripped
    front = parts[1]
    body = parts[2].lstrip("\n")
    meta: dict[str, str] = {}
    for line in front.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            meta[key.strip()] = val.strip().strip('"').strip("'")
    return meta, body


class SkillRegistry:
    """Scan ``skills_root`` for ``*/SKILL.md``; lazy-load bodies per name."""

    def __init__(self, skills_root: Path) -> None:
        self._root = skills_root
        self._by_name: dict[str, SkillMeta] = {}
        self._body_cache: dict[str, str] = {}
        self._scan()

    def _scan(self) -> None:
        self._by_name.clear()
        self._body_cache.clear()
        if not self._root.is_dir():
            logger.debug("Skills root missing or not a directory: %s", self._root)
            return
        for child in sorted(self._root.iterdir()):
            if not child.is_dir():
                continue
            skill_file = child / "SKILL.md"
            if not skill_file.is_file():
                continue
            try:
                text = skill_file.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                logger.warning("Could not read skill file %s: %s", skill_file, exc)
                continue
            meta_dict, _body_preview = _parse_frontmatter(text)
            name = meta_dict.get("name", child.name)
            description = meta_dict.get("description", "")
            self._by_name[name] = SkillMeta(
                name=name, description=description, path=skill_file
            )

    def list_skills(self) -> list[SkillMeta]:
        return sorted(self._by_name.values(), key=lambda m: m.name)

    def get_skill(self, name: str) -> SkillContent | None:
        meta = self._by_name.get(name)
        if meta is None:
            return None
        if name not in self._body_cache:
            try:
                text = meta.path.read_text(encoding="utf-8", errors="replace")
            except OSError as exc:
                logger.warning("Could not load skill %s: %s", name, exc)
                return None
            _fm, body = _parse_frontmatter(text)
            self._body_cache[name] = body.strip()
        return SkillContent(meta=meta, body=self._body_cache[name])


_registry_singleton: SkillRegistry | None = None


def get_registry(skills_root: Path | None = None) -> SkillRegistry:
    """Process-wide registry rooted at ``.agents/skills`` under the project."""
    global _registry_singleton
    if _registry_singleton is None:
        root = skills_root if skills_root is not None else default_skills_root()
        _registry_singleton = SkillRegistry(root)
    return _registry_singleton


def reset_registry_for_tests() -> None:
    """Clear singleton (tests only)."""
    global _registry_singleton
    _registry_singleton = None
