from __future__ import annotations

import base64
import json
import re
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


@dataclass
class BusinessThemeItem:
    id: str
    name: str
    summary: str
    category: str
    source_path: Path
    tags: list[str]
    detail_lines: list[str]
    prompt_hint: str


@dataclass
class BusinessTableItem:
    id: str
    name: str
    summary: str
    schema_name: str
    tags: list[str]
    referenced_by: list[str]
    detail_path: Path | None
    prompt_hint: str


@dataclass
class TopicTrackerItem:
    id: str
    name: str
    summary: str
    category: str
    folder_path: Path
    updated_at: datetime | None
    file_count: int
    subfolder_count: int
    sample_entries: list[str]
    prompt_hint: str


@st.cache_data(show_spinner=False, ttl=10)
def _cached_skill_items(repo_root_str: str) -> list[SkillGalleryItem]:
    return _collect_skill_items(Path(repo_root_str))


@st.cache_data(show_spinner=False, ttl=10)
def _cached_artifact_items(repo_root_str: str) -> list[ArtifactGalleryItem]:
    return _collect_artifact_items(Path(repo_root_str))


@st.cache_data(show_spinner=False, ttl=10)
def _cached_business_theme_items(repo_root_str: str) -> list[BusinessThemeItem]:
    return _collect_business_theme_items(Path(repo_root_str))


@st.cache_data(show_spinner=False, ttl=10)
def _cached_business_table_items(repo_root_str: str) -> list[BusinessTableItem]:
    return _collect_business_table_items(Path(repo_root_str))


@st.cache_data(show_spinner=False, ttl=10)
def _cached_topic_tracker_items(repo_root_str: str) -> list[TopicTrackerItem]:
    return _collect_topic_tracker_items(Path(repo_root_str))


@st.dialog("Sync GitLab")
def _show_sync_gitlab_dialog() -> None:
    st.info("敬请期待")
    st.caption("GitLab 同步入口已预留，后续会在这里接入实际同步流程。")


@st.dialog("导入本地 SKILL")
def _show_import_skill_dialog() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    template_content = """---
name: example-skill
description: Briefly describe what this skill does and when it should be used.
---

## Purpose

Describe the goal of the skill and the problem it solves.

## When to use

- Explain the trigger conditions.
- Mention the typical user request patterns.

## Inputs

- List required files, parameters, or assumptions.

## Workflow

1. Step one.
2. Step two.
3. Step three.

## Outputs

- Describe expected outputs or artifacts.
"""
    st.download_button(
        "下载 SKILL 模板",
        data=template_content.encode("utf-8"),
        file_name="SKILL.md",
        mime="text/markdown",
        key="download_skill_template",
        use_container_width=True,
    )
    uploaded = st.file_uploader("选择一个本地 `SKILL.md` 文件", type=["md"], key="import_skill_file")
    skill_name = st.text_input(
        "技能名称",
        key="import_skill_name",
        placeholder="例如：customer-segmentation",
        help="将写入到 `.agents/skills/<技能名称>/SKILL.md`。",
    )

    if st.button("开始导入", key="import_skill_submit", use_container_width=True, type="primary"):
        if uploaded is None:
            st.error("请先选择一个 `SKILL.md` 文件。")
            return
        if uploaded.name != "SKILL.md":
            st.error("文件名必须严格为 `SKILL.md`。")
            return
        normalized_name = _normalize_skill_directory_name(skill_name)
        if not normalized_name:
            st.error("技能名称不能为空，且只允许字母、数字、空格、`-`、`_`。")
            return
        try:
            content = uploaded.getvalue().decode("utf-8")
        except UnicodeDecodeError:
            st.error("文件必须使用 UTF-8 编码。")
            return
        validation_error = _validate_imported_skill_markdown(content)
        if validation_error:
            st.error(validation_error)
            return

        target_dir = repo_root / ".agents" / "skills" / normalized_name
        target_file = target_dir / "SKILL.md"
        if target_file.exists():
            st.error(f"目标目录已存在：`{target_dir.name}`。请更换技能名称。")
            return

        target_dir.mkdir(parents=True, exist_ok=True)
        target_file.write_text(content, encoding="utf-8")
        _cached_skill_items.clear()
        st.session_state["skills_import_notice"] = f"已导入到 `.agents/skills/{normalized_name}/SKILL.md`"
        st.rerun()


def render_skills_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    skill_items = _cached_skill_items(str(repo_root))
    import_notice = str(st.session_state.pop("skills_import_notice", "") or "").strip()
    if import_notice:
        st.success(import_notice)

    hero_col, action_col = st.columns([10, 0.1], gap="small", vertical_alignment="center")
    with hero_col:
        st.markdown(
            """
            <div class="xyf-library-hero">
                <div class="xyf-library-kicker">知识资产</div>
                <div class="xyf-library-title">技能库</div>
                <div class="xyf-library-copy">
                    浏览本地技能，查看用途说明，并在下一轮对话中直接复用。
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )


    _render_skill_section(skill_items)


def render_artifacts_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    artifact_items = _cached_artifact_items(str(repo_root))

    st.markdown(
        """
        <div class="xyf-library-hero">
            <div class="xyf-library-kicker">Workspace</div>
            <div class="xyf-library-title">分析产出</div>
            <div class="xyf-library-copy">
                以紧凑文件视图检索、筛选并查看历史任务沉淀下来的可复用产出。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not artifact_items:
        st.info("当前还没有分析产出。执行任务或将结果保存到 `artifacts/` 后，这里会自动展示。")
        return
    filter_col,list_col = st.columns([0.72,1.85,], gap="small")
    with filter_col:
        filtered = _render_artifact_filters(artifact_items)
        if not filtered:
            st.info("当前筛选条件下没有匹配的分析产出。")
            return
        _render_artifact_toolbar(filtered, artifact_items)

    paged_artifacts = _paginate_items(filtered, key_prefix="artifacts", page_size=6)
    if not paged_artifacts:
        st.info("当前页没有分析产出。")
        return

    selected_item = _resolve_selected_artifact(paged_artifacts)
    with list_col:
        _render_artifact_list(paged_artifacts, selected_item.id if selected_item else None)


def render_business_knowledge_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    theme_items = _cached_business_theme_items(str(repo_root))
    table_items = _cached_business_table_items(str(repo_root))

    st.markdown(
        """
        <div class="xyf-library-hero">
            <div class="xyf-library-kicker">Domain Intelligence</div>
            <div class="xyf-library-title">业务知识库</div>
            <div class="xyf-library-copy">
                汇总业务主题认知与 DataWorks 表资产，便于在提需求、拆分析口径、写 SQL 前先建立统一上下文。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    metric_cols = st.columns(4, gap="small")
    theme_count = len(theme_items)
    table_count = len(table_items)
    referenced_tables = sum(1 for item in table_items if item.referenced_by)
    detailed_tables = sum(1 for item in table_items if item.detail_path is not None)
    metrics = [
        ("主题文档", str(theme_count)),
        ("沉淀表数", str(table_count)),
        ("被引用表", str(referenced_tables)),
        ("详情表卡", str(detailed_tables)),
    ]
    for col, (label, value) in zip(metric_cols, metrics):
        with col:
            st.metric(label, value)

    theme_col, table_col = st.columns([1.05, 1.35], gap="large")
    with theme_col:
        _render_business_theme_section(theme_items)
    with table_col:
        _render_business_table_section(table_items)


def render_topics_tab() -> None:
    repo_root = Path(__file__).resolve().parent.parent
    topic_items = _cached_topic_tracker_items(str(repo_root))

    st.markdown(
        """
            <div class="xyf-library-hero xyf-topic-hero">
            <div class="xyf-library-kicker">Tracker</div>
            <div class="xyf-library-title">专题追踪</div>
            <div class="xyf-library-copy">
                基于 artifacts 目录中的专题文件夹追踪分析主题、产出沉淀和最新活动，快速定位当前在跑什么、积累了什么。
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not topic_items:
        st.info("`artifacts/` 下还没有可用于追踪的专题文件夹。")
        return

    m1, m2, m3, m4 = st.columns(4, gap="small")
    with m1:
        st.metric("专题数", str(len(topic_items)))
    with m2:
        st.metric("总文件数", str(sum(item.file_count for item in topic_items)))
    with m3:
        st.metric("含子目录专题", str(sum(1 for item in topic_items if item.subfolder_count > 0)))
    with m4:
        st.metric("最近更新专题", topic_items[0].name[:16] if topic_items else "-")

    search_col, category_col, sort_col = st.columns([1.2, 0.9, 0.9], gap="small", vertical_alignment="bottom")
    with search_col:
        search = st.text_input("搜索专题", key="topic_tracker_search_query", placeholder="scorecard、sql、complaint、analysis...")
    with category_col:
        categories = ["all"] + sorted({item.category for item in topic_items})
        selected_category = st.selectbox("分类", categories, key="topic_tracker_category")
    with sort_col:
        sort_key = st.selectbox("排序", ["最新优先", "文件数优先", "名称 A-Z"], key="topic_tracker_sort")

    query = search.strip().lower()
    filtered = [
        item
        for item in topic_items
        if (selected_category == "all" or item.category == selected_category)
        and (
            not query
            or query in item.name.lower()
            or query in item.summary.lower()
            or any(query in entry.lower() for entry in item.sample_entries)
        )
    ]
    if sort_key == "文件数优先":
        filtered.sort(key=lambda item: (item.file_count, item.updated_at or datetime.min), reverse=True)
    elif sort_key == "名称 A-Z":
        filtered.sort(key=lambda item: item.name.lower())
    else:
        filtered.sort(key=lambda item: item.updated_at or datetime.min, reverse=True)

    if not filtered:
        st.info("当前筛选条件下没有匹配的专题。")
        return

    paged_items = _paginate_items(filtered, key_prefix="topic_tracker", page_size=9, display_total=False)
    if not paged_items:
        st.info("当前页没有专题。")
        return

    cols = st.columns(3, gap="small")
    for idx, item in enumerate(paged_items):
        with cols[idx % 3]:
            _render_topic_tracker_card(item)

def _render_artifact_toolbar(filtered: list[ArtifactGalleryItem], all_items: list[ArtifactGalleryItem]) -> None:
    total_previewable = sum(1 for item in filtered if item.preview_mode != "none")
    m0,m1, m2, m3 = st.columns([0.1,0.3,0.3,0.3], gap="small",)
    with m1:
        st.metric("全部文件", str(len(all_items)))
    with m2:
        st.metric("筛选后", str(len(filtered)))
    with m3:
        st.metric("可预览", str(total_previewable))



def _render_artifact_filters(items: list[ArtifactGalleryItem]) -> list[ArtifactGalleryItem]:
    st.session_state.setdefault("artifacts_search_query", "")
    st.session_state.setdefault("artifacts_filter_kind", "all")
    st.session_state.setdefault("artifacts_filter_source", "all")
    st.session_state.setdefault("artifacts_filter_task", "all")
    st.session_state.setdefault("artifacts_sort_key", "最新优先")
    st.session_state.setdefault("artifacts_preview_only", False)

    layout_col, filter_col = st.columns([0.01, 0.99], gap="small")
    with filter_col:
        st.markdown("**搜索**")
        st.text_input(
            "搜索分析产出",
            key="artifacts_search_query",
            placeholder="文件名、任务 ID、摘要、路径...",
            label_visibility="collapsed",
        )
        # st.divider()
        st.markdown("**筛选**")
        kind_options = ["all"] + sorted({item.kind for item in items})
        source_options = ["all"] + sorted({item.source for item in items})
        task_values = sorted({item.task_id for item in items if item.task_id})
        task_options = ["all"] + task_values
        st.selectbox("类型", kind_options, key="artifacts_filter_kind")
        st.selectbox("来源", source_options, key="artifacts_filter_source")
        st.selectbox("任务", task_options, key="artifacts_filter_task")
        st.selectbox(
            "排序",
            ["最新优先", "最早优先", "名称 A-Z", "名称 Z-A"],
            key="artifacts_sort_key",
        )
        st.checkbox("仅看可预览", key="artifacts_preview_only")

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

    sort_key = str(st.session_state.get("artifacts_sort_key") or "最新优先")
    if sort_key == "最早优先":
        filtered.sort(key=lambda item: item.updated_at or datetime.min)
    elif sort_key == "名称 A-Z":
        filtered.sort(key=lambda item: item.name.lower())
    elif sort_key == "名称 Z-A":
        filtered.sort(key=lambda item: item.name.lower(), reverse=True)
    else:
        filtered.sort(key=lambda item: item.updated_at or datetime.min, reverse=True)

    with layout_col:
        return filtered


def _render_artifact_list(items: list[ArtifactGalleryItem], selected_id: str | None) -> None:
    st.markdown("**文件**")
    header = st.columns([4.7, 1, 1.1, 1.35, 0.9, 0.95, 3.75], gap="xxsmall")
    labels = ["名称", "类型", "来源", "更新时间", "大小", "任务", "操作"]
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
    st.markdown("**详情**")
    if item is None:
        st.info("请从列表中选择一个文件，以查看元信息和预览内容。")
        return

    with st.container(border=True):
        st.markdown(f"### {item.name}")
        info_rows = [
            ("类型", item.kind.upper()),
            ("来源", item.origin_label or item.source.replace("_", " ").title()),
            ("更新时间", item.updated_at.strftime("%Y-%m-%d %H:%M") if item.updated_at else "-"),
            ("大小", _format_size(item.size_bytes)),
            ("任务", item.task_id or "-"),
            ("路径", str(item.path.relative_to(Path(__file__).resolve().parent.parent)) if item.path is not None else "内嵌任务结果产出"),
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

    st.markdown("**预览**")
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
            st.info("图片预览不可用。")
        return
    if item.preview_mode == "html":
        html = item.html_payload
        if html is None and item.path is not None:
            html = item.path.read_text(encoding="utf-8", errors="replace")
        if html:
            components.html(html, height=320, scrolling=True)
        else:
            st.info("HTML 预览不可用。")
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
            st.info("表格预览不可用。")
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
            st.info("JSON 预览不可用。")
        return
    st.info("该类型文件暂不支持预览。")


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
        st.caption("-" if compact else "无可下载文件")
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
        st.info("`.agents/skills` 下还没有本地技能。")
        return

    search_col, category_col,pagination_col,action_col = st.columns([0.75, 0.3, 0.45, 0.6], gap="small",vertical_alignment = 'bottom')
    with search_col:
        search = st.text_input("搜索技能", key="skills_search_query", placeholder="planner、sql、verification...")
    with category_col:
        categories = ["all"] + sorted({item.category for item in items})
        selected_category = st.selectbox("分类", categories, key="skills_category")

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
        st.info("当前筛选条件下没有匹配的技能。")
        return
    with pagination_col:
        paged_skills = _paginate_items(filtered, key_prefix="skills", page_size=6,display_total= False)
        if not paged_skills:
            st.info("当前页没有技能。")
            return
    with action_col:
        import_col, sync_col = st.columns(2, gap="small")
        with import_col:
            if st.button("从本地导入", key="skills_import_local", type="secondary",width = 'stretch',help='上传本地的 SKILL 文件'):
                _show_import_skill_dialog()
        with sync_col:
            if st.button("同步远程", key="skills_sync_gitlab", type="primary",width = 'stretch',help='同步远程的 SKILL 文件'):
                _show_sync_gitlab_dialog()

    cols = st.columns(2)
    for idx, item in enumerate(paged_skills):
        with cols[idx % 2]:
            _render_skill_card(item)


def _render_skill_card(item: SkillGalleryItem) -> None:
    with st.container(border=True):
        st.markdown(f"**{item.name}**")
        st.write(_truncate_text(item.summary, 132))
        tag_text = " | ".join(item.tags[:3]) if item.tags else "技能"
        st.caption(tag_text)
        st.caption(f"`{item.skill_md.parent.name}`")

        c1, c2 = st.columns([1, 1])
        with c1:
            if st.button("用于对话", key=f"skill_use_{item.id}", use_container_width=True):
                st.session_state["_followup_q"] = {"text": item.prompt_hint, "mode": "chat"}
                st.session_state["mode"] = "chat"
                st.rerun()
        with c2:
            expand = st.toggle("详情", key=f"skill_detail_{item.id}", value=False)

        if expand:
            for line in item.detail_lines:
                st.write(f"- {_truncate_text(line, 140)}")


def _render_business_theme_section(items: list[BusinessThemeItem]) -> None:
    st.markdown("### 业务主题")
    if not items:
        st.info("`knowledge_base/theme` 下还没有业务主题文档。")
        return

    search_col, category_col, pagination_col = st.columns([0.75, 0.25, 0.72], gap="small", vertical_alignment="bottom")
    with search_col:
        search = st.text_input("搜索主题", key="business_theme_search_query", placeholder="新客、老客、监控、复盘...")
    with category_col:
        categories = ["all"] + sorted({item.category for item in items})
        selected_category = st.selectbox("分类", categories, key="business_theme_category")

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
            or any(query in line.lower() for line in item.detail_lines)
        )
    ]
    if not filtered:
        st.info("当前筛选条件下没有匹配的业务主题。")
        return

    with pagination_col:
        paged_items = _paginate_items(filtered, key_prefix="business_theme", page_size=4, display_total=False)
        if not paged_items:
            st.info("当前页没有业务主题。")
            return

    for item in paged_items:
        _render_business_theme_card(item)


def _render_business_theme_card(item: BusinessThemeItem) -> None:
    with st.container(border=True):
        st.markdown(f"**{item.name}**")
        st.write(_truncate_text(item.summary, 150))
        st.caption(" | ".join(item.tags[:4]) if item.tags else item.category)
        st.caption(f"`knowledge_base/theme/{item.source_path.name}`")

        action_col, detail_col = st.columns([1, 1], gap="small")
        with action_col:
            if st.button("用于对话", key=f"business_theme_use_{item.id}", use_container_width=True):
                st.session_state["_followup_q"] = {"text": item.prompt_hint, "mode": "chat"}
                st.session_state["mode"] = "chat"
                st.rerun()
        with detail_col:
            expand = st.toggle("详情", key=f"business_theme_detail_{item.id}", value=False)

        if expand:
            for line in item.detail_lines:
                st.write(f"- {_truncate_text(line, 160)}")


def _render_business_table_section(items: list[BusinessTableItem]) -> None:
    st.markdown("### 表资产")
    if not items:
        st.info("`knowledge_base/dataworks/tables.md` 中还没有可展示的 DataWorks 表知识。")
        return

    search_col, schema_col, detail_col, pagination_col = st.columns([1, 0.48, 0.68, 0.92], gap="small", vertical_alignment="bottom")
    with search_col:
        search = st.text_input("搜索表", key="business_table_search_query", placeholder="dws_inloan、risk、customer...")
    with schema_col:
        schemas = ["all"] + sorted({item.schema_name for item in items})
        selected_schema = st.selectbox("库/Schema", schemas, key="business_table_schema")
    with detail_col:
        detail_mode = st.selectbox("详情状态", ["全部", "已有详情", "缺少详情"], key="business_table_detail")

    query = search.strip().lower()
    filtered = [
        item
        for item in items
        if (selected_schema == "all" or item.schema_name == selected_schema)
        and (
            detail_mode == "全部"
            or (detail_mode == "已有详情" and item.detail_path is not None)
            or (detail_mode == "缺少详情" and item.detail_path is None)
        )
        and (
            not query
            or query in item.name.lower()
            or query in item.summary.lower()
            or any(query in tag.lower() for tag in item.tags)
            or any(query in ref.lower() for ref in item.referenced_by)
        )
    ]
    if not filtered:
        st.info("当前筛选条件下没有匹配的表。")
        return

    with pagination_col:
        paged_items = _paginate_items(filtered, key_prefix="business_table", page_size=6, display_total=False)
        if not paged_items:
            st.info("当前页没有表。")
            return

    cols = st.columns(2)
    for idx, item in enumerate(paged_items):
        with cols[idx % 2]:
            _render_business_table_card(item)


def _render_business_table_card(item: BusinessTableItem) -> None:
    with st.container(border=True):
        st.markdown(f"**{item.name}**")
        st.write(_truncate_text(item.summary, 152))
        st.caption(" | ".join(item.tags[:4]) if item.tags else item.schema_name)
        status = "已沉淀详情" if item.detail_path is not None else "仅索引"
        st.caption(f"`{item.schema_name}` | {status}")

        c1, c2 = st.columns([1, 1], gap="small")
        with c1:
            if st.button("用于对话", key=f"business_table_use_{item.id}", use_container_width=True):
                st.session_state["_followup_q"] = {"text": item.prompt_hint, "mode": "chat"}
                st.session_state["mode"] = "chat"
                st.rerun()
        with c2:
            expand = st.toggle("引用", key=f"business_table_detail_{item.id}", value=False)

        if expand:
            if item.referenced_by:
                st.write(f"- 被 {len(item.referenced_by)} 个脚本或分析文件引用")
                for ref in item.referenced_by[:5]:
                    st.write(f"- {ref}")
                if len(item.referenced_by) > 5:
                    st.caption(f"+ {len(item.referenced_by) - 5} more")
            else:
                st.write("- 当前未记录上游引用文件")
            if item.detail_path is not None:
                st.caption(f"`knowledge_base/dataworks/by_table/{item.detail_path.name}`")


def _render_topic_tracker_card(item: TopicTrackerItem) -> None:
    with st.container(border=True):
        timestamp = item.updated_at.strftime("%Y-%m-%d %H:%M:%S") if item.updated_at else "-"
        st.markdown(
            (
                "<div class='xyf-topic-card-head'>"
                f"<div class='xyf-topic-badge'>{item.category}</div>"
                f"<div class='xyf-topic-card-title'>{item.name}</div>"
                f"<div class='xyf-topic-card-copy'>{_truncate_text(item.summary, 180)}</div>"
                f"<div class='xyf-topic-card-time'>最新更新：{timestamp}</div>"
                "</div>"
            ),
            unsafe_allow_html=True,
        )

        meta_cols = st.columns([0.95, 0.95, 1.1], gap="small")
        with meta_cols[0]:
            st.caption(f"文件 `{item.file_count}`")
        with meta_cols[1]:
            st.caption(f"子目录 `{item.subfolder_count}`")
        with meta_cols[2]:
            if st.button("用于对话", key=f"topic_tracker_use_{item.id}", use_container_width=True):
                st.session_state["_followup_q"] = {"text": item.prompt_hint, "mode": "chat"}
                st.session_state["mode"] = "chat"
                st.rerun()

        with st.expander("展开专题内容", expanded=False):
            st.caption(f"`artifacts/{item.folder_path.name}`")
            if item.sample_entries:
                for entry in item.sample_entries:
                    st.write(f"- {entry}")
            else:
                st.write("- 该专题文件夹当前为空")


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


def _collect_business_theme_items(repo_root: Path) -> list[BusinessThemeItem]:
    theme_root = repo_root / "knowledge_base" / "theme"
    if not theme_root.exists():
        return []

    items: list[BusinessThemeItem] = []
    for path in sorted(theme_root.glob("*.md")):
        lines = path.read_text(encoding="utf-8", errors="replace").splitlines()
        title = _first_markdown_heading(lines) or path.stem.replace("_", " ").title()
        detail_lines = _extract_business_detail_lines(lines)
        summary = detail_lines[0] if detail_lines else "业务主题说明。"
        category = _categorize_business_theme(path.stem, title, summary)
        items.append(
            BusinessThemeItem(
                id=path.stem,
                name=title,
                summary=summary,
                category=category,
                source_path=path,
                tags=_business_theme_tags(path.stem, title, summary, category),
                detail_lines=detail_lines,
                prompt_hint=f"结合业务知识库主题《{title}》回答这个业务分析问题，并优先沿用该文档中的业务口径和拆分方式。",
            )
        )
    return items


def _collect_business_table_items(repo_root: Path) -> list[BusinessTableItem]:
    tables_md = repo_root / "knowledge_base" / "dataworks" / "tables.md"
    by_table_root = repo_root / "knowledge_base" / "dataworks" / "by_table"
    if not tables_md.exists():
        return []

    lines = tables_md.read_text(encoding="utf-8", errors="replace").splitlines()
    indexed_refs = _parse_table_reference_index(lines)
    items: list[BusinessTableItem] = []
    for table_name, referenced_by in indexed_refs.items():
        detail_path = by_table_root / f"{table_name}.md"
        schema_name = table_name.split(".", 1)[0] if "." in table_name else "other"
        ref_count = len(referenced_by)
        if referenced_by:
            summary = f"被 {ref_count} 个业务 SQL 或分析文件引用，可作为常用口径与宽表入口。"
        else:
            summary = "已登记表名，但暂未补充上游引用信息。"
        items.append(
            BusinessTableItem(
                id=table_name.replace(".", "_"),
                name=table_name,
                summary=summary,
                schema_name=schema_name,
                tags=_business_table_tags(table_name, schema_name, ref_count, detail_path.exists()),
                referenced_by=referenced_by,
                detail_path=detail_path if detail_path.exists() else None,
                prompt_hint=f"分析需求涉及表 `{table_name}`，请优先参考业务知识库中该表的上下文、引用场景和既有口径。",
            )
        )
    return items


def _collect_topic_tracker_items(repo_root: Path) -> list[TopicTrackerItem]:
    artifacts_root = repo_root / "artifacts"
    if not artifacts_root.exists():
        return []

    items: list[TopicTrackerItem] = []
    for folder in sorted(artifacts_root.iterdir()):
        if not folder.is_dir():
            continue
        child_entries = sorted(folder.iterdir(), key=lambda path: path.name.lower())
        file_count = sum(1 for entry in child_entries if entry.is_file())
        subfolder_count = sum(1 for entry in child_entries if entry.is_dir())
        updated_at = datetime.fromtimestamp(folder.stat().st_mtime) if folder.exists() else None
        sample_entries = []
        for entry in child_entries[:6]:
            prefix = "dir" if entry.is_dir() else "file"
            sample_entries.append(f"[{prefix}] {entry.name}")
        summary = _topic_tracker_summary(folder.name, file_count, subfolder_count, sample_entries)
        items.append(
            TopicTrackerItem(
                id=folder.name,
                name=folder.name.replace("_", " "),
                summary=summary,
                category=_categorize_topic_folder(folder.name),
                folder_path=folder,
                updated_at=updated_at,
                file_count=file_count,
                subfolder_count=subfolder_count,
                sample_entries=sample_entries,
                prompt_hint=f"围绕专题 `{folder.name}` 继续分析，优先参考该专题目录下已经沉淀的文件和产出脉络。",
            )
        )

    items.sort(key=lambda item: item.updated_at or datetime.min, reverse=True)
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


def _first_markdown_heading(lines: list[str]) -> str:
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("#"):
            return stripped.lstrip("#").strip()
    return ""


def _extract_business_detail_lines(lines: list[str]) -> list[str]:
    detail_lines: list[str] = []
    for line in lines:
        stripped = line.strip()
        if not stripped or stripped == "---" or stripped.startswith("#"):
            continue
        cleaned = stripped.lstrip("- ").strip()
        if cleaned:
            detail_lines.append(cleaned)
        if len(detail_lines) >= 5:
            break
    return detail_lines


def _categorize_business_theme(stem: str, title: str, summary: str) -> str:
    text = f"{stem} {title} {summary}".lower()
    if "monitor" in text:
        return "监控分析"
    if "new_customer" in text or "新客" in text:
        return "新客转化"
    if "existing_customer" in text or "老客" in text:
        return "老客经营"
    if "requirement" in text:
        return "需求模式"
    return "业务总览"


def _business_theme_tags(stem: str, title: str, summary: str, category: str) -> list[str]:
    text = f"{stem} {title} {summary}".lower()
    tags = [category]
    for label, token in (
        ("监控", "monitor"),
        ("新客", "new_customer"),
        ("老客", "existing_customer"),
        ("需求模板", "requirement"),
        ("概览", "overview"),
    ):
        if token in text and label not in tags:
            tags.append(label)
    return tags


def _parse_table_reference_index(lines: list[str]) -> dict[str, list[str]]:
    result: dict[str, list[str]] = {}
    current_table = ""
    in_index = False
    for line in lines:
        stripped = line.strip()
        if stripped.startswith("## ") and "By Table" in stripped:
            break
        if stripped.startswith("## "):
            in_index = "SQL" in stripped
            continue
        if not in_index:
            continue
        if stripped.startswith("### "):
            current_table = stripped[4:].strip()
            result.setdefault(current_table, [])
            continue
        if current_table and stripped.startswith("- "):
            ref = stripped[2:].strip()
            if ref and "未" not in ref:
                result[current_table].append(ref)
    return result


def _business_table_tags(table_name: str, schema_name: str, ref_count: int, has_detail: bool) -> list[str]:
    tags = [schema_name]
    if ref_count > 0:
        tags.append(f"{ref_count} refs")
    else:
        tags.append("unreferenced")
    tags.append("detail" if has_detail else "index")
    if "risk" in table_name.lower() and "risk" not in tags:
        tags.append("risk")
    if "loan" in table_name.lower() and "loan" not in tags:
        tags.append("loan")
    if "user" in table_name.lower() and "user" not in tags:
        tags.append("user")
    return tags


def _categorize_topic_folder(folder_name: str) -> str:
    text = folder_name.lower()
    if "scorecard" in text:
        return "评分卡"
    if "sql" in text:
        return "SQL专题"
    if "analysis" in text:
        return "分析复盘"
    if "task" in text:
        return "任务记录"
    if "export" in text or "duckdb" in text or "table" in text:
        return "数据资产"
    return "通用专题"


def _topic_tracker_summary(folder_name: str, file_count: int, subfolder_count: int, sample_entries: list[str]) -> str:
    if sample_entries:
        lead = sample_entries[0].split(" ", 1)[1]
        return f"该专题下有 {file_count} 个文件、{subfolder_count} 个子目录，当前可从 `{lead}` 等产出继续追踪。"
    return f"该专题下有 {file_count} 个文件、{subfolder_count} 个子目录。"


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
        return f"评分卡产出已保存至 `{parent}`。"
    if "codex_jsonl_streams" in rel_parts:
        return "已保存 Codex JSONL 流式产出。"
    if "excel" in rel_parts:
        return "已导出的表格产出。"
    if "plots" in rel_parts:
        return "已生成图表产出。"
    if len(rel_parts) >= 3 and rel_parts[0] == "artifacts" and rel_parts[1] == "tasks":
        return f"已保存任务 `{rel_parts[2][:8]}` 的产出。"
    return "已保存工作区产出。"


def _artifact_followup_prompt(item: ArtifactGalleryItem) -> str:
    parts = [f"使用产出 `{item.name}`"]
    if item.task_id:
        parts.append(f"来自任务 `{item.task_id[:8]}`")
    parts.append(f"作为下一步的上下文。产出类型：{item.kind}。")
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


def _normalize_skill_directory_name(name: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9 _-]+", "", (name or "").strip())
    cleaned = re.sub(r"[\s_]+", "-", cleaned).strip("-").lower()
    return cleaned


def _validate_imported_skill_markdown(content: str) -> str | None:
    lines = content.splitlines()
    if not lines or lines[0].strip() != "---":
        return "SKILL.md 必须以 YAML frontmatter 开头。"
    name, description = _parse_skill_front_matter(lines)
    if not name:
        return "frontmatter 缺少 `name` 字段。"
    if not description:
        return "frontmatter 缺少 `description` 字段。"
    required_sections = ("## Purpose",)
    for section in required_sections:
        if section not in content:
            return f"缺少必需章节：`{section}`。"
    return None


def _paginate_items[T](items: list[T], *, key_prefix: str, page_size: int, display_total = True) -> list[T]:
    total_pages = max(1, (len(items) + page_size - 1) // page_size)
    page_key = f"{key_prefix}_page"
    current_page = int(st.session_state.get(page_key, 1) or 1)
    current_page = min(max(1, current_page), total_pages)
    st.session_state[page_key] = current_page

    p1, p2, p3 = st.columns([1, 1.5, 1], gap="small")
    with p1:
        if st.button("上一页", key=f"{key_prefix}_prev", disabled=current_page <= 1, use_container_width=True):
            st.session_state[page_key] = current_page - 1
            st.rerun()
    with p2:
        st.markdown(
            f"<div class='xyf-page-chip'>第 <b>{current_page}</b> / {total_pages} 页</div>",
            unsafe_allow_html=True,
        )
    with p3:
        if st.button("下一页", key=f"{key_prefix}_next", disabled=current_page >= total_pages, use_container_width=True):
            st.session_state[page_key] = current_page + 1
            st.rerun()

    start_idx = (current_page - 1) * page_size
    end_idx = start_idx + page_size
    start_row = start_idx + 1 if items else 0
    end_row = min(len(items), end_idx)
    if display_total:
        st.caption(f"显示第 {start_row}-{end_row} 条，共 {len(items)} 条")
    return items[start_idx:end_idx]
