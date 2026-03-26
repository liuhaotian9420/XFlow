from __future__ import annotations

import base64
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

import pandas as pd
import streamlit as st
import streamlit.components.v1 as components


@dataclass
class ArtifactGalleryItem:
    id: str
    name: str
    kind: str
    source: str
    task_id: str
    path: Path | None
    mime: str
    summary: str
    updated_at: datetime | None
    size_bytes: int | None
    preview_mode: str
    text_payload: str | None = None
    html_payload: str | None = None
    image_bytes: bytes | None = None
    table_rows: list[dict[str, Any]] | None = None
    origin_label: str | None = None


@dataclass
class SkillGalleryItem:
    id: str
    name: str
    summary: str
    category: str
    skill_dir: Path
    skill_md: Path
    tags: list[str]
    detail_lines: list[str]
    prompt_hint: str


def render_skills_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    skill_items = _collect_skill_items(repo_root)

    st.markdown(
        """
        <div class="xyf-library-hero">
            <div class="xyf-library-kicker">Knowledge Base</div>
            <div class="xyf-library-title">Skills</div>
            <div class="xyf-library-copy">
                Browse local skills, inspect their purpose, and reuse them in the next conversation turn.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    _render_skill_section(skill_items)


def render_artifacts_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    artifact_items = _collect_artifact_items(repo_root)

    st.markdown(
        """
        <div class="xyf-library-hero">
            <div class="xyf-library-kicker">Workspace Files</div>
            <div class="xyf-library-title">Saved Artifacts</div>
            <div class="xyf-library-copy">
                Search, filter, and inspect reusable outputs from prior runs in a compact file-style view.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not artifact_items:
        st.info("No artifacts available yet. Run a task or save outputs under `artifacts/` to populate this page.")
        return
    filter_col,list_col = st.columns([0.72,1.85,], gap="small")
    with filter_col:
        filtered = _render_artifact_filters(artifact_items)
        if not filtered:
            st.info("No artifacts match the current filters.")
            return
        _render_artifact_toolbar(filtered, artifact_items)

    paged_artifacts = _paginate_items(filtered, key_prefix="artifacts", page_size=6)
    if not paged_artifacts:
        st.info("No artifacts on this page.")
        return

    selected_item = _resolve_selected_artifact(paged_artifacts)
    with list_col:
        _render_artifact_list(paged_artifacts, selected_item.id if selected_item else None)

def _render_artifact_toolbar(filtered: list[ArtifactGalleryItem], all_items: list[ArtifactGalleryItem]) -> None:
    total_previewable = sum(1 for item in filtered if item.preview_mode != "none")
    m0,m1, m2, m3 = st.columns([0.1,0.3,0.3,0.3], gap="small",)
    with m1:
        st.metric("All files", str(len(all_items)))
    with m2:
        st.metric("Filtered", str(len(filtered)))
    with m3:
        st.metric("Previewable", str(total_previewable))



def _render_artifact_filters(items: list[ArtifactGalleryItem]) -> list[ArtifactGalleryItem]:
    st.session_state.setdefault("artifacts_search_query", "")
    st.session_state.setdefault("artifacts_filter_kind", "all")
    st.session_state.setdefault("artifacts_filter_source", "all")
    st.session_state.setdefault("artifacts_filter_task", "all")
    st.session_state.setdefault("artifacts_sort_key", "Newest first")
    st.session_state.setdefault("artifacts_preview_only", False)

    layout_col, filter_col = st.columns([0.01, 0.99], gap="small")
    with filter_col:
        st.markdown("**Search**")
        st.text_input(
            "Search artifacts",
            key="artifacts_search_query",
            placeholder="name, task id, summary, path...",
            label_visibility="collapsed",
        )
        # st.divider()
        st.markdown("**Filters**")
        kind_options = ["all"] + sorted({item.kind for item in items})
        source_options = ["all"] + sorted({item.source for item in items})
        task_values = sorted({item.task_id for item in items if item.task_id})
        task_options = ["all"] + task_values
        st.selectbox("Type", kind_options, key="artifacts_filter_kind")
        st.selectbox("Source", source_options, key="artifacts_filter_source")
        st.selectbox("Task", task_options, key="artifacts_filter_task")
        st.selectbox(
            "Sort",
            ["Newest first", "Oldest first", "Name A-Z", "Name Z-A"],
            key="artifacts_sort_key",
        )
        st.checkbox("Previewable only", key="artifacts_preview_only")

    query = str(st.session_state.get("artifacts_search_query") or "").strip().lower()
    kind = str(st.session_state.get("artifacts_filter_kind") or "all")
    source = str(st.session_state.get("artifacts_filter_source") or "all")
    task_id = str(st.session_state.get("artifacts_filter_task") or "all")
    preview_only = bool(st.session_state.get("artifacts_preview_only"))

    filtered = [
        item
        for item in items
        if (kind == "all" or item.kind == kind)
        and (source == "all" or item.source == source)
        and (task_id == "all" or item.task_id == task_id)
        and (not preview_only or item.preview_mode != "none")
        and (
            not query
            or query in item.name.lower()
            or query in item.summary.lower()
            or query in item.task_id.lower()
            or (item.path is not None and query in str(item.path).lower())
        )
    ]

    sort_key = str(st.session_state.get("artifacts_sort_key") or "Newest first")
    if sort_key == "Oldest first":
        filtered.sort(key=lambda item: item.updated_at or datetime.min)
    elif sort_key == "Name A-Z":
        filtered.sort(key=lambda item: item.name.lower())
    elif sort_key == "Name Z-A":
        filtered.sort(key=lambda item: item.name.lower(), reverse=True)
    else:
        filtered.sort(key=lambda item: item.updated_at or datetime.min, reverse=True)

    with layout_col:
        return filtered


def _render_artifact_list(items: list[ArtifactGalleryItem], selected_id: str | None) -> None:
    st.markdown("**Files**")
    header = st.columns([4.7, 1, 1.1, 1.35, 0.9, 0.95, 3.75], gap="xxsmall")
    labels = ["Name", "Type", "Source", "Updated", "Size", "Task", "Actions"]
    for col, label in zip(header, labels):
        col.caption(label)

    for item in items:
        row = st.columns([4.7, 1, 1.1, 1.35, 0.9, 0.95, 3.75], gap="xxsmall",vertical_alignment="top")
        is_selected = item.id == selected_id
        name_label = item.name + ("  •" if is_selected else "")
        with row[0]:
            st.markdown(f"**{name_label}**")
            # if st.button(name_label, key=f"artifact_row_select_{item.id}", use_container_width=True, type="secondary" if is_selected else "tertiary"):
            #     st.session_state["selected_artifact_id"] = item.id
            #     st.rerun()
            # st.caption(_truncate_text(item.summary, 72))
        with row[1]:
            st.caption(item.kind.upper())
        with row[2]:
            st.caption(item.origin_label or item.source.replace("_", " ").title())
        with row[3]:
            st.caption(item.updated_at.strftime("%Y-%m-%d %H:%M") if item.updated_at else "-")
        with row[4]:
            st.caption(_format_size(item.size_bytes))
        with row[5]:
            st.caption(item.task_id[:8] if item.task_id else "-")
        with row[6]:
            a1, a2, a3 = st.columns([2,3,3], gap="xxsmall")
            # with a1:
            #     preview_disabled = item.preview_mode == "none"
            #     if st.button("🔍查看", key=f"artifact_preview_select_{item.id}", disabled=preview_disabled, width ='content', help="Preview"):
            #         st.session_state["selected_artifact_id"] = item.id
            #         st.rerun()
            with a1:
                _render_artifact_download(item, compact=True)
            with a2:
                if st.button("在对话中使用", key=f"artifact_use_{item.id}", width = 'content', help="Use in chat",icon='💬',type = 'tertiary'):
                    st.session_state["_followup_q"] = {"text": _artifact_followup_prompt(item), "mode": "chat"}
                    st.session_state["mode"] = "chat"
                    st.rerun()
            with a3:
                with st.popover("查看详情", width = 'stretch',type = 'secondary',icon = '🔍',disabled = item.preview_mode == "none"):
                    _render_artifact_detail_panel(item)
        # with st.expander("Details", expanded=False):
        #     _render_artifact_detail_panel(item)
        st.divider()


def _render_artifact_detail_panel(item: ArtifactGalleryItem | None) -> None:
    st.markdown("**Details**")
    if item is None:
        st.info("Select a file from the list to inspect its metadata and preview.")
        return

    with st.container(border=True):
        st.markdown(f"### {item.name}")
        info_rows = [
            ("Type", item.kind.upper()),
            ("Source", item.origin_label or item.source.replace("_", " ").title()),
            ("Updated", item.updated_at.strftime("%Y-%m-%d %H:%M") if item.updated_at else "-"),
            ("Size", _format_size(item.size_bytes)),
            ("Task", item.task_id or "-"),
            ("Path", str(item.path.relative_to(Path(__file__).resolve().parent.parent)) if item.path is not None else "embedded result artifact"),
        ]
        for label, value in info_rows:
            st.caption(f"{label}: {value}")
        st.write(item.summary)

        # action_col_1, action_col_2 = st.columns(2, gap="small")
        # with action_col_1:
        #     _render_artifact_download(item, compact=False)
        # with action_col_2:
        #     if st.button("Use in chat", key=f"artifact_detail_use_{item.id}", use_container_width=True):
        #         st.session_state["_followup_q"] = {"text": _artifact_followup_prompt(item), "mode": "chat"}
        #         st.session_state["mode"] = "chat"
        #         st.rerun()

    st.markdown("**Preview**")
    with st.container(border=True):
        _render_artifact_preview(item)


def _resolve_selected_artifact(items: list[ArtifactGalleryItem]) -> ArtifactGalleryItem | None:
    if not items:
        return None
    selected_id = str(st.session_state.get("selected_artifact_id") or "").strip()
    if selected_id:
        for item in items:
            if item.id == selected_id:
                return item
    st.session_state["selected_artifact_id"] = items[0].id
    return items[0]


def _render_artifact_preview(item: ArtifactGalleryItem) -> None:
    if item.preview_mode == "image":
        if item.image_bytes is not None:
            st.image(item.image_bytes, caption=item.name, use_container_width=True)
        elif item.path is not None:
            st.image(str(item.path), caption=item.name, use_container_width=True)
        else:
            st.info("Image preview unavailable.")
        return
    if item.preview_mode == "html":
        html = item.html_payload
        if html is None and item.path is not None:
            html = item.path.read_text(encoding="utf-8", errors="replace")
        if html:
            components.html(html, height=320, scrolling=True)
        else:
            st.info("HTML preview unavailable.")
        return
    if item.preview_mode == "table":
        rows = item.table_rows
        if rows is None and item.path is not None and item.path.suffix.lower() == ".csv":
            try:
                rows = pd.read_csv(item.path).head(50).to_dict(orient="records")
            except Exception:
                rows = None
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, height=360)
        else:
            st.info("Table preview unavailable.")
        return
    if item.preview_mode == "json":
        payload = item.text_payload
        if payload is None and item.path is not None:
            payload = item.path.read_text(encoding="utf-8", errors="replace")
        if payload:
            try:
                st.json(json.loads(payload))
            except json.JSONDecodeError:
                st.code(payload[:4000], language="json")
        else:
            st.info("JSON preview unavailable.")
        return
    st.info("Preview not available for this artifact type.")


def _render_artifact_download(item: ArtifactGalleryItem, *, compact: bool) -> None:
    payload: bytes | None = None
    file_name: str | None = None
    mime = item.mime or "application/octet-stream"
    label = "💾下载" if compact else "💾"

    if item.path is not None and item.path.is_file():
        payload = item.path.read_bytes()
        file_name = item.path.name
    elif item.image_bytes is not None:
        payload = item.image_bytes
        file_name = item.name
    elif item.html_payload is not None:
        payload = item.html_payload.encode("utf-8")
        file_name = f"{item.name}.html"
        mime = "text/html"
    elif item.text_payload is not None:
        payload = item.text_payload.encode("utf-8")
        file_name = f"{item.name}.txt"
        mime = "text/plain"

    if payload is None or file_name is None:
        st.caption("-" if compact else "No file")
        return

    st.download_button(
        label,
        data=payload,
        file_name=file_name,
        mime=mime,
        key=f"artifact_dl_{item.id}_{'compact' if compact else 'full'}",
        width='content',
        type = 'primary' 
    )


def _render_skill_section(items: list[SkillGalleryItem]) -> None:
    # st.markdown("### Skills")
    if not items:
        st.info("No local skills found under `.agents/skills`.")
        return

    search_col, category_col,pagination_col = st.columns([1.4, 1, 0.6], gap="small",vertical_alignment = 'bottom')
    with search_col:
        search = st.text_input("Search skills", key="skills_search_query", placeholder="planner, sql, verification...")
    with category_col:
        categories = ["all"] + sorted({item.category for item in items})
        selected_category = st.selectbox("Category", categories, key="skills_category")

    query = search.strip().lower()
    filtered = [
        item
        for item in items
        if (selected_category == "all" or item.category == selected_category)
        and (
            not query
            or query in item.name.lower()
            or query in item.summary.lower()
            or any(query in tag.lower() for tag in item.tags)
        )
    ]
    if not filtered:
        st.info("No skills match the current filters.")
        return
    with pagination_col:
        paged_skills = _paginate_items(filtered, key_prefix="skills", page_size=6,display_total= False)
        if not paged_skills:
            st.info("No skills on this page.")
            return

    # st.markdown(
    #     """
    #     <div class="xyf-library-hero">
    #         <div class="xyf-library-kicker">Filtered results</div>
    #         <div class="xyf-library-title">Skills</div>
    #     </div>
    #     """,
    #     unsafe_allow_html=True,
    # )
    cols = st.columns(2)
    for idx, item in enumerate(paged_skills):
        with cols[idx % 2]:
            _render_skill_card(item)


def _render_skill_card(item: SkillGalleryItem) -> None:
    with st.container(border=True):
        st.markdown(f"**{item.name}**")
        st.write(_truncate_text(item.summary, 132))
        tag_text = " | ".join(item.tags[:3]) if item.tags else "Skill"
        st.caption(tag_text)
        st.caption(f"`{item.skill_md.parent.name}`")

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("Use this skill", key=f"skill_use_{item.id}", use_container_width=True):
                st.session_state["_followup_q"] = {"text": item.prompt_hint, "mode": "chat"}
                st.session_state["mode"] = "chat"
                st.rerun()
        with c2:
            expand = st.toggle("Details", key=f"skill_detail_{item.id}", value=False)

        if expand:
            for line in item.detail_lines:
                st.write(f"- {_truncate_text(line, 140)}")


def _collect_artifact_items(repo_root: Path) -> list[ArtifactGalleryItem]:
    items: list[ArtifactGalleryItem] = []
    items.extend(_collect_task_result_artifacts(repo_root))

    artifacts_root = repo_root / "artifacts"
    if artifacts_root.exists():
        for path in sorted(artifacts_root.rglob("*")):
            if not path.is_file():
                continue
            if path.name.endswith((".sqlite3", ".sqlite3-shm", ".sqlite3-wal", ".log")):
                continue
            items.append(_artifact_item_from_file(path, repo_root))

    deduped: dict[str, ArtifactGalleryItem] = {}
    for item in items:
        deduped[item.id] = item
    ordered = list(deduped.values())
    ordered.sort(key=lambda item: item.updated_at or datetime.min, reverse=True)
    return ordered


def _collect_task_result_artifacts(repo_root: Path) -> list[ArtifactGalleryItem]:
    task_root = repo_root / "artifacts" / "tasks"
    if not task_root.exists():
        return []

    items: list[ArtifactGalleryItem] = []
    for result_path in sorted(task_root.glob("*/result.json")):
        try:
            payload = json.loads(result_path.read_text(encoding="utf-8"))
        except Exception:
            continue
        task_id = result_path.parent.name
        artifacts = payload.get("artifacts") or []
        if not isinstance(artifacts, list):
            continue
        updated_at = datetime.fromtimestamp(result_path.stat().st_mtime)
        for idx, artifact in enumerate(artifacts):
            if not isinstance(artifact, dict):
                continue
            name = str(artifact.get("name") or f"artifact_{idx}")
            mime = str(artifact.get("mime") or "")
            preview_mode = "none"
            image_bytes = None
            html_payload = None
            if mime.startswith("image/"):
                preview_mode = "image"
                b64 = artifact.get("data_base64")
                if isinstance(b64, str) and b64.strip():
                    try:
                        image_bytes = base64.b64decode(b64)
                    except Exception:
                        image_bytes = None
            elif mime == "text/html":
                preview_mode = "html"
                html_payload = str(artifact.get("html") or "").strip() or None
            items.append(
                ArtifactGalleryItem(
                    id=f"task_result_{task_id}_{idx}",
                    name=name,
                    kind=_classify_artifact_kind(name, mime, None),
                    source="task_result",
                    task_id=task_id,
                    path=None,
                    mime=mime,
                    summary=f"Generated in task result `{task_id[:8]}`.",
                    updated_at=updated_at,
                    size_bytes=len(image_bytes) if image_bytes is not None else (len(html_payload.encode('utf-8')) if html_payload else None),
                    preview_mode=preview_mode,
                    html_payload=html_payload,
                    image_bytes=image_bytes,
                    origin_label="Task result",
                )
            )
    return items


def _artifact_item_from_file(path: Path, repo_root: Path) -> ArtifactGalleryItem:
    rel_parts = path.relative_to(repo_root).parts
    task_id = ""
    if len(rel_parts) >= 3 and rel_parts[0] == "artifacts" and rel_parts[1] == "tasks":
        task_id = rel_parts[2]

    suffix = path.suffix.lower()
    mime = _guess_mime(path)
    return ArtifactGalleryItem(
        id=str(path.relative_to(repo_root)).replace("\\", "_").replace("/", "_"),
        name=path.name,
        kind=_classify_artifact_kind(path.name, mime, suffix),
        source="saved_file",
        task_id=task_id,
        path=path,
        mime=mime,
        summary=_artifact_summary_from_path(path, rel_parts),
        updated_at=datetime.fromtimestamp(path.stat().st_mtime),
        size_bytes=path.stat().st_size,
        preview_mode=_preview_mode_for_path(path, mime, suffix),
        origin_label="Saved file",
    )


def _collect_skill_items(repo_root: Path) -> list[SkillGalleryItem]:
    skill_root = repo_root / ".agents" / "skills"
    if not skill_root.exists():
        return []

    items: list[SkillGalleryItem] = []
    for skill_md in sorted(skill_root.glob("*/SKILL.md")):
        lines = skill_md.read_text(encoding="utf-8", errors="replace").splitlines()
        name, description = _parse_skill_front_matter(lines)
        if not name:
            name = skill_md.parent.name
        if not description:
            description = _first_nonempty_markdown_line(lines[3:]) or "No description available."
        items.append(
            SkillGalleryItem(
                id=name.replace(" ", "_"),
                name=name,
                summary=description,
                category=_categorize_skill(name, description),
                skill_dir=skill_md.parent,
                skill_md=skill_md,
                tags=_skill_tags(name, description, _categorize_skill(name, description)),
                detail_lines=_extract_skill_detail_lines(lines),
                prompt_hint=f"Use the `{name}` skill for this task. {description}",
            )
        )
    return items


def _parse_skill_front_matter(lines: list[str]) -> tuple[str, str]:
    if not lines or lines[0].strip() != "---":
        return "", ""
    name = ""
    description = ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("name:"):
            name = line.split(":", 1)[1].strip()
        elif line.startswith("description:"):
            description = line.split(":", 1)[1].strip()
    return name, description


def _extract_skill_detail_lines(lines: list[str]) -> list[str]:
    detail_lines: list[str] = []
    capture = False
    for line in lines:
        stripped = line.strip()
        if stripped == "## Purpose":
            capture = True
            continue
        if capture and stripped.startswith("## "):
            break
        if capture and stripped and not stripped.startswith("#"):
            detail_lines.append(stripped.lstrip("- ").strip())
        if len(detail_lines) >= 4:
            break
    if detail_lines:
        return detail_lines
    fallback = _first_nonempty_markdown_line(lines)
    return [fallback] if fallback else []


def _first_nonempty_markdown_line(lines: list[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped and not stripped.startswith("#") and stripped != "---":
            return stripped.lstrip("- ").strip()
    return ""


def _categorize_skill(name: str, description: str) -> str:
    text = f"{name} {description}".lower()
    if "plan" in text:
        return "Planning"
    if "sql" in text or "export" in text:
        return "SQL / Export"
    if "verification" in text or "scorecard" in text:
        return "Verification / Modeling"
    return "Data Analysis"


def _skill_tags(name: str, description: str, category: str) -> list[str]:
    tags = [category]
    text = f"{name} {description}".lower()
    for token in ("planning", "sql", "export", "analysis", "verification", "modeling", "duckdb"):
        if token in text and token.title() not in tags:
            tags.append(token.title())
    return tags


def _classify_artifact_kind(name: str, mime: str, suffix: str | None) -> str:
    suffix = (suffix or "").lower()
    if mime.startswith("image/") or suffix in {".png", ".jpg", ".jpeg", ".gif", ".webp"}:
        return "image"
    if mime == "text/html" or suffix == ".html":
        return "html"
    if suffix in {".csv", ".xlsx", ".xls"}:
        return "table"
    if suffix in {".json", ".jsonl"}:
        return "json"
    if suffix in {".sql", ".txt", ".md"}:
        return "text"
    return "file"


def _guess_mime(path: Path) -> str:
    suffix = path.suffix.lower()
    return {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
        ".html": "text/html",
        ".csv": "text/csv",
        ".json": "application/json",
        ".jsonl": "application/x-ndjson",
        ".sql": "text/plain",
        ".txt": "text/plain",
        ".md": "text/markdown",
        ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        ".xls": "application/vnd.ms-excel",
        ".pkl": "application/octet-stream",
    }.get(suffix, "application/octet-stream")


def _preview_mode_for_path(path: Path, mime: str, suffix: str) -> str:
    kind = _classify_artifact_kind(path.name, mime, suffix)
    if kind in {"image", "html", "json"}:
        return kind
    if kind == "table" and suffix == ".csv":
        return "table"
    return "none"


def _artifact_summary_from_path(path: Path, rel_parts: tuple[str, ...]) -> str:
    parent = path.parent.name
    if "scorecardpy" in rel_parts:
        return f"Scorecard output saved under `{parent}`."
    if "codex_jsonl_streams" in rel_parts:
        return "Saved Codex JSONL stream artifact."
    if "excel" in rel_parts:
        return "Exported spreadsheet artifact."
    if "plots" in rel_parts:
        return "Generated plot artifact."
    if len(rel_parts) >= 3 and rel_parts[0] == "artifacts" and rel_parts[1] == "tasks":
        return f"Saved task artifact from `{rel_parts[2][:8]}`."
    return "Saved workspace artifact."


def _artifact_followup_prompt(item: ArtifactGalleryItem) -> str:
    parts = [f"Use the artifact `{item.name}`"]
    if item.task_id:
        parts.append(f"from task `{item.task_id[:8]}`")
    parts.append(f"as context for the next step. Artifact type: {item.kind}.")
    return " ".join(parts)


def _format_size(size_bytes: int | None) -> str:
    if size_bytes is None:
        return "-"
    units = ["B", "KB", "MB", "GB"]
    size = float(size_bytes)
    for unit in units:
        if size < 1024 or unit == units[-1]:
            if unit == "B":
                return f"{int(size)} {unit}"
            return f"{size:.1f} {unit}"
        size /= 1024
    return f"{int(size_bytes)} B"


def _truncate_text(text: str, limit: int) -> str:
    text = (text or "").strip()
    if len(text) <= limit:
        return text
    return text[: max(0, limit - 3)].rstrip() + "..."


def _paginate_items[T](items: list[T], *, key_prefix: str, page_size: int, display_total = True) -> list[T]:
    total_pages = max(1, (len(items) + page_size - 1) // page_size)
    page_key = f"{key_prefix}_page"
    current_page = int(st.session_state.get(page_key, 1) or 1)
    current_page = min(max(1, current_page), total_pages)
    st.session_state[page_key] = current_page

    p1, p2, p3 = st.columns([1, 2, 1], gap="small")
    with p1:
        if st.button("Prev", key=f"{key_prefix}_prev", disabled=current_page <= 1, use_container_width=True):
            st.session_state[page_key] = current_page - 1
            st.rerun()
    with p2:
        st.markdown(
            f"<div class='xyf-page-chip'>Page <b>{current_page}</b> / {total_pages}</div>",
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("Next", key=f"{key_prefix}_next", disabled=current_page >= total_pages, use_container_width=True):
            st.session_state[page_key] = current_page + 1
            st.rerun()

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    start_row = start_idx + 1 if items else 0
    end_row = min(len(items), end_idx)
    if display_total:
        st.caption(f"Showing {start_row}-{end_row} of {len(items)}")
    return items[start_idx:end_idx]
