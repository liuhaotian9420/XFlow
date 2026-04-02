from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))
_BRAND_LOGO_PATH = _REPO_ROOT / "xflow.png"

from app.chat_actions import _enqueue_chat, _enqueue_review_respond, _enqueue_task
from app.streamlit_state import (
    MAX_VISIBLE_CHAT_TURNS,
    _ensure_welcome_if_empty,
    _init_state,
    _invalidate_schema_cache,
    _parse_task_command,
    _pending_review_task_id,
    _transcript_cut_for_viewport,
)
from app.ui_chat import clear_current_chat, render_chat_message
from app.ui_library import render_artifacts_tab, render_business_knowledge_tab, render_skills_tab, render_topics_tab
from app.ui_sidebar import render_sidebar
from app.ui_status import inject_global_styles, render_status_panel

st.set_page_config(
    page_title="XFlow",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":bar_chart:",
)
brand_col, title_col = st.columns([1, 10], vertical_alignment="center")
with brand_col:
    if _BRAND_LOGO_PATH.is_file():
        st.image(str(_BRAND_LOGO_PATH), width=288)
with title_col:
    st.markdown(
        """
        <h1 class="xyf-page-title">
        你的一站式 AI 数据分析工作台
        </h1>
        """,
        unsafe_allow_html=True,
    )
st.caption("面向数据分析场景的轻量工作台，支持对话分析、任务规划、执行确认、技能调用与结果沉淀。")
inject_global_styles()

_init_state()
render_sidebar()

tab_chat, tab_skills, tab_artifacts, bussiness_theme, topics = st.tabs(
    ["AI助手", "技能库", "分析产出", "业务知识库", "专题追踪"]
)

with tab_chat:
    if st.session_state.get("_followup_q"):
        queued = st.session_state._followup_q
        st.session_state._followup_q = None
        if isinstance(queued, dict):
            fq = str(queued.get("text") or "").strip()
            target_mode = str(queued.get("mode") or "chat").strip().lower()
        else:
            fq = str(queued or "").strip()
            target_mode = "chat"
        if fq:
            existing_draft = str(st.session_state.get("chat_composer_draft_value") or "").strip()
            next_draft = f"{existing_draft}\n\n{fq}".strip() if existing_draft else fq
            st.session_state["chat_composer_draft_value"] = next_draft
            st.session_state["chat_composer_draft_version"] = int(st.session_state.get("chat_composer_draft_version") or 0) + 1
            st.session_state[f"chat_composer_draft_input_{st.session_state['chat_composer_draft_version']}"] = next_draft
            st.session_state.mode = "chat" if target_mode == "chat" else target_mode
        st.rerun()

    _ensure_welcome_if_empty()
    st.session_state.setdefault("chat_composer_draft_value", "")
    st.session_state.setdefault("chat_composer_draft_version", 0)
    cur_status, reset_status = st.columns([10, 1])
    with cur_status:
        with st.expander("当前会话状态", expanded=False):
            render_status_panel()
            st.markdown("")
    with reset_status:
        if st.button(
            "重置",
            key="reset_chat",
            use_container_width=True,
            type="primary",
            help="重置当前会话，历史记录仍可在侧边栏中查看。",
        ):
            clear_current_chat()
            st.rerun()

    messages = st.session_state.messages
    cut = _transcript_cut_for_viewport(messages, MAX_VISIBLE_CHAT_TURNS)
    pin_welcome = cut > 0 and bool(messages) and messages[0].get("type") == "welcome"
    exp_lo = 1 if pin_welcome else 0
    exp_hi = cut

    if pin_welcome:
        render_chat_message(0, messages[0])

    if exp_lo < exp_hi:
        hidden_count = exp_hi - exp_lo
        with st.expander(f"加载更早消息（{hidden_count} 条）", key="viewport_older_messages"):
            for idx in range(exp_lo, exp_hi):
                render_chat_message(idx, messages[idx])

    for idx in range(cut, len(messages)):
        render_chat_message(idx, messages[idx])

    draft_text = str(st.session_state.get("chat_composer_draft_value") or "")
    if draft_text.strip():
        draft_version = int(st.session_state.get("chat_composer_draft_version") or 0)
        draft_input_key = f"chat_composer_draft_input_{draft_version}"
        st.session_state.setdefault(draft_input_key, draft_text)
        st.markdown("**对话草稿**")
        st.text_area(
            "对话草稿",
            key=draft_input_key,
            height=140,
            placeholder="从技能库、业务知识库、专题追踪带入的内容会先出现在这里，确认后再发送。",
            label_visibility="collapsed",
        )
        draft_send_col, draft_clear_col = st.columns([1, 1], gap="small")
        with draft_send_col:
            if st.button("发送草稿", key="send_chat_composer_draft", use_container_width=True, type="primary"):
                st.session_state["chat_composer_draft_value"] = str(st.session_state.get(draft_input_key) or "")
                draft_to_send = str(st.session_state.get("chat_composer_draft_value") or "").strip()
                if draft_to_send:
                    st.session_state.messages.append({"role": "user", "type": "text", "content": draft_to_send})
                    st.session_state.mode = "chat"
                    st.session_state["chat_composer_draft_value"] = ""
                    st.session_state["chat_composer_draft_version"] = draft_version + 1
                    _enqueue_chat(draft_to_send)
                    st.rerun()
        with draft_clear_col:
            if st.button("清空草稿", key="clear_chat_composer_draft", use_container_width=True):
                st.session_state["chat_composer_draft_value"] = ""
                st.session_state["chat_composer_draft_version"] = draft_version + 1
                st.rerun()

    chat_val = st.chat_input(
        "直接提问，也可以附带 CSV 或 Excel 文件。",
        accept_file=True,
        file_type=["csv", "xlsx", "xls"],
        key="chat_prompt",
    )
    if chat_val is not None:
        text = chat_val.text.strip() if not isinstance(chat_val, str) else chat_val.strip()
        file_list = [] if isinstance(chat_val, str) else list(chat_val.files)
        if file_list:
            f0 = file_list[0]
            prev_name = (st.session_state.file_meta or {}).get("name")
            st.session_state.file_meta = {
                "name": f0.name,
                "type": f0.type or "application/octet-stream",
                "data": f0.getvalue(),
            }
            if prev_name != f0.name:
                _invalidate_schema_cache()
            st.session_state.messages.append(
                {"role": "assistant", "type": "text", "content": f"已加载文件 **`{f0.name}`**。"}
            )
        if text:
            st.session_state.messages.append({"role": "user", "type": "text", "content": text})
            is_task_cmd, task_body = _parse_task_command(text)
            if is_task_cmd:
                if not task_body:
                    st.session_state.messages.append(
                        {
                            "role": "assistant",
                            "type": "text",
                            "content": "请在 **`/task`** 后补充分析需求，例如 `/task 比较各区域销售额`。",
                        }
                    )
                else:
                    st.session_state.mode = "task"
                    _enqueue_task(task_body)
            elif st.session_state.get("mode") == "task":
                pending_review_tid = _pending_review_task_id()
                if pending_review_tid is not None:
                    _enqueue_review_respond(pending_review_tid, user_text=text)
                else:
                    st.session_state.mode = "chat"
                    _enqueue_chat(text)
            else:
                st.session_state.mode = "chat"
                _enqueue_chat(text)
        elif file_list and not text:
            st.session_state.messages.append(
                {"role": "assistant", "type": "text", "content": "文件已附加，可以开始提问了。"}
            )
        st.rerun()

with tab_skills:
    render_skills_tab()

with tab_artifacts:
    render_artifacts_tab()

with bussiness_theme:
    render_business_knowledge_tab()

with topics:
    render_topics_tab()

