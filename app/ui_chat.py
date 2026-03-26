from __future__ import annotations

import json
import uuid
from typing import Any

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

from app.api_client import _get_task
from app.chat_actions import (
    _enqueue_review_respond,
    _execute_chat_reply,
    _execute_confirm_task,
    _execute_create_task,
    _execute_review_respond,
    _execute_revise_plan,
)
from app.ui_status import result_summary_text, summarize_plan


def clear_current_chat() -> None:
    st.session_state.messages = []
    st.session_state.mode = "chat"
    st.session_state.active_task_id = None
    st.session_state.chat_session_id = str(uuid.uuid4())


def render_chat_toolbar() -> None:
    left_col, right_col = st.columns([4, 1])
    with left_col:
        st.caption("当前会话")
    with right_col:
        if st.button("清空当前聊天", key="clear_current_chat", use_container_width=True):
            clear_current_chat()
            st.rerun()


def _review_action_from_message(msg: dict[str, Any]) -> str:
    action = str(msg.get("recommended_action") or "").strip().lower()
    if action:
        return action
    status = str(msg.get("completeness_status") or "").strip().lower()
    if status == "blocked":
        return "revise_required"
    if status == "needs_exploration":
        return "clarify"
    return "confirm"


def _render_assistant_error_message(msg: dict[str, Any], msg_index: int) -> None:
    title = str(msg.get("title") or "Something went wrong")
    detail = str(msg.get("detail") or "").strip()
    kind = msg.get("kind")
    st.error(f"**{title}**")
    if isinstance(kind, str) and kind.strip():
        st.caption(f"`kind:` {kind.strip()}")
    if detail:
        with st.expander("Details", key=f"assistant_err_details_{msg_index}"):
            st.code(detail, language="text")


def _render_chat_stream_event_panel(msg: dict[str, Any], msg_index: int) -> None:
    if not bool(st.session_state.get("show_chat_event_stream", True)):
        return
    events = msg.get("stream_events")
    if not isinstance(events, list) or not events:
        return
    latest_reasoning = str(msg.get("latest_reasoning_text") or "").strip()
    latest_command = msg.get("latest_command") if isinstance(msg.get("latest_command"), dict) else None
    title = f"Live event stream ({len(events)} events)"
    with st.expander(title, expanded=False):
        if latest_reasoning:
            st.caption("Latest reasoning")
            st.code(latest_reasoning, language="text")
        if latest_command:
            command = str(latest_command.get("command") or "").strip()
            exit_code = latest_command.get("exit_code")
            if command:
                meta = f"exit_code={exit_code}" if exit_code is not None else "exit_code=?"
                st.caption(f"Latest command | {meta}")
                st.code(command, language="powershell")
            output_preview = str(latest_command.get("output_preview") or "").strip()
            if output_preview:
                st.code(output_preview, language="text")

        rows: list[dict[str, Any]] = []
        for idx, event in enumerate(events, start=1):
            if not isinstance(event, dict):
                continue
            note = ""
            event_type = str(event.get("type") or "")
            if event_type in {"agent.message.completed", "reasoning.completed"}:
                note = str(event.get("text") or "")[:120]
            elif event_type == "command.completed":
                note = str(event.get("command") or "")[:120]
            elif event_type == "error":
                note = str(event.get("error") or "")[:120]
            rows.append({"#": idx, "type": event_type, "note": note})
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        with st.expander("Raw events", expanded=False):
            st.text_area(
                "events_json",
                value=json.dumps(events, ensure_ascii=False, indent=2),
                height=320,
                key=f"chat_stream_events_{msg_index}",
                label_visibility="collapsed",
            )


def _draw_chart(chart: dict[str, Any]) -> None:
    chart_df = pd.DataFrame(chart.get("data", []))
    x_col = chart.get("x")
    y_col = chart.get("y")
    chart_type = chart.get("chart_type")
    if chart_df.empty or not x_col or not y_col or x_col not in chart_df.columns:
        st.info("No chart data yet.")
        return
    if chart_type == "line":
        st.line_chart(chart_df.set_index(x_col)[y_col])
    elif chart_type == "bar":
        st.bar_chart(chart_df.set_index(x_col)[y_col])
    elif chart_type == "histogram":
        st.bar_chart(chart_df[y_col].value_counts())
    else:
        st.dataframe(chart_df, use_container_width=True)


def _render_plan_tables(plan: dict[str, Any]) -> None:
    st.markdown(f"**分析目标**: {plan.get('goal', '')}")
    out = plan.get("output") or {}
    st.caption(f"图表: `{out.get('chart_type', '')}` | 展示表格: `{out.get('show_table', True)}`")

    metrics = plan.get("metrics") or []
    if metrics:
        st.markdown("**指标**")
        st.dataframe(pd.DataFrame(metrics), use_container_width=True)

    dims = plan.get("dimensions") or []
    if dims:
        st.markdown("**维度**")
        st.dataframe(pd.DataFrame(dims), use_container_width=True)

    filters = plan.get("filters") or []
    if filters:
        st.markdown("**筛选条件**")
        st.dataframe(pd.DataFrame(filters), use_container_width=True)


def _render_result_block(result: dict[str, Any], task_id: str, key_suffix: str) -> None:
    if "chart" not in result:
        st.warning(result.get("message", "结果中没有可展示的图表。"))
        with st.expander("查看原始结果", key=f"raw_result_{key_suffix}"):
            st.json(result)
        return
    st.markdown("**结论摘要**")
    st.write(result_summary_text(result))
    if result.get("execution_summary"):
        st.caption(result["execution_summary"])
    st.markdown("**图表结果**")
    _draw_chart(result["chart"])
    table = result.get("table") or {}
    rows = table.get("rows") or []
    table_df = pd.DataFrame(rows)
    st.markdown("**结果明细**")
    st.dataframe(table_df, use_container_width=True)
    if not table_df.empty:
        st.download_button(
            "下载结果 CSV",
            data=table_df.to_csv(index=False).encode("utf-8"),
            file_name=f"{task_id}_result.csv",
            mime="text/csv",
            key=f"dl_{key_suffix}",
        )

    artifacts = result.get("artifacts") or []
    if artifacts:
        with st.expander("附加产物", key=f"artifacts_{key_suffix}"):
            for idx, artifact in enumerate(artifacts):
                name = str(artifact.get("name") or f"artifact_{idx}")
                mime = str(artifact.get("mime") or "")
                width = artifact.get("display_width")
                height = artifact.get("display_height")
                if isinstance(width, int) and width > 0:
                    width = min(width, 800)
                else:
                    width = 640
                if mime.startswith("image/"):
                    b64 = artifact.get("data_base64")
                    if isinstance(b64, str) and b64.strip():
                        import base64 as _b64

                        raw = _b64.b64decode(b64)
                        st.image(raw, caption=name, width=width)
                    else:
                        st.warning(f"Image artifact `{name}` missing data.")
                elif mime == "text/html":
                    html = artifact.get("html")
                    if isinstance(html, str) and html.strip():
                        h = height if isinstance(height, int) and height > 0 else 180
                        components.html(html, height=h, scrolling=True)
                    else:
                        st.warning(f"HTML artifact `{name}` missing html.")
                else:
                    st.caption(f"{name} ({mime})")
    follow = result.get("follow_ups") or []
    if follow:
        st.markdown("**建议下一步**")
        for idx, item in enumerate(follow):
            label = item[:80] + ("..." if len(item) > 80 else "")
            if st.button(label, key=f"fu_{key_suffix}_{idx}"):
                st.session_state["_followup_q"] = item
                st.rerun()


def render_chat_message(i: int, msg: dict[str, Any]) -> None:
    role = msg.get("role", "assistant")
    mtype = msg.get("type", "text")

    if mtype == "thinking":
        action = msg.get("action")
        with st.chat_message("assistant"):
            if action == "create_task":
                st.markdown("💡Analyzing your question...")
                _execute_create_task(msg, i)
            elif action == "confirm_task":
                st.markdown("🚀Running the analysis plan...")
                _execute_confirm_task(msg, i)
            elif action == "chat_reply":
                st.markdown("⌛Thinking...")
                _execute_chat_reply(msg, i)
            elif action == "revise_plan":
                st.markdown("🔄Updating the plan...")
                _execute_revise_plan(msg, i)
            elif action == "respond_review":
                st.markdown("🔄Applying your review response...")
                _execute_review_respond(msg, i)
            else:
                st.markdown("Processing...")
        return

    with st.chat_message(role):
        if mtype == "welcome":
            with st.container(border=True):
                st.markdown(msg.get("content", ""))
        elif mtype == "error":
            _render_assistant_error_message(msg, i)
        elif mtype == "text":
            st.markdown(msg.get("content", ""))
        elif mtype == "chat_stream_debug":
            content = str(msg.get("content") or "").strip()
            status_text = str(msg.get("status_text") or "Streaming...").strip()
            if content:
                st.markdown(content)
            else:
                st.caption(status_text)
            _render_chat_stream_event_panel(msg, i)
        elif mtype == "chat_response":
            st.markdown(msg.get("content", ""))
            total_elapsed = None
            for key in ("api_elapsed_s", "codex_exec_elapsed_s", "provider_elapsed_s"):
                value = msg.get(key)
                if isinstance(value, (int, float)):
                    total_elapsed = float(value)
                    break
            if total_elapsed is not None:
                st.caption(f"总耗时: {total_elapsed:.2f}s")

            if bool(st.session_state.get("show_prompt_debug", False)):
                token_parts: list[str] = []
                in_tok = msg.get("input_tokens")
                out_tok = msg.get("output_tokens")
                cached_in_tok = msg.get("cached_input_tokens")
                if isinstance(in_tok, int):
                    token_parts.append(f"in={in_tok}")
                if isinstance(out_tok, int):
                    token_parts.append(f"out={out_tok}")
                if isinstance(cached_in_tok, int):
                    token_parts.append(f"cached_in={cached_in_tok}")
                if token_parts:
                    st.caption("[Tokens] " + " | ".join(token_parts))

                timing_parts: list[str] = []
                for key, label in (
                    ("api_elapsed_s", "api"),
                    ("provider_elapsed_s", "provider"),
                    ("codex_exec_elapsed_s", "codex_exec"),
                    ("prompt_build_elapsed_s", "prompt_build"),
                    ("codex_spawn_elapsed_s", "spawn"),
                    ("codex_ttft_elapsed_s", "ttft"),
                    ("codex_generation_elapsed_s", "generation"),
                    ("codex_teardown_elapsed_s", "teardown"),
                    ("provider_overhead_elapsed_s", "overhead"),
                ):
                    value = msg.get(key)
                    if isinstance(value, (int, float)):
                        timing_parts.append(f"{label}={float(value):.2f}s")
                if timing_parts:
                    st.caption("[Timing] " + " | ".join(timing_parts))

                vendor = str(msg.get("runtime_vendor") or "").strip()
                binary = str(msg.get("runtime_binary") or "").strip()
                if vendor:
                    runtime_text = f"[Runtime] vendor={vendor}"
                    if binary:
                        runtime_text += f" | bin={binary}"
                    st.caption(runtime_text)

                debug_prompt = msg.get("debug_prompt")
                if isinstance(debug_prompt, str) and debug_prompt.strip():
                    with st.expander("Context sent to Codex", key=f"ctx_codex_{i}"):
                        pchars = msg.get("prompt_chars")
                        hturns = msg.get("history_turns_used")
                        meta_parts: list[str] = []
                        if isinstance(pchars, int):
                            meta_parts.append(f"prompt_chars={pchars}")
                        if isinstance(hturns, int):
                            meta_parts.append(f"history_turns={hturns}")
                        if meta_parts:
                            st.caption(" | ".join(meta_parts))
                        st.code(debug_prompt, language="markdown")
            _render_chat_stream_event_panel(msg, i)
        elif mtype == "review_request":
            task_id = str(msg.get("task_id") or "")
            review_id = str(msg.get("review_id") or "")
            title = str(msg.get("title") or "Review")
            body = str(msg.get("message") or "")
            options = [str(x).strip() for x in (msg.get("options") or []) if str(x).strip()]
            resolved = bool(msg.get("resolved"))
            review_type = str(msg.get("review_type") or "").strip().lower()
            suggested_plan = msg.get("suggested_plan")
            completeness_status = str(msg.get("completeness_status") or "").strip().lower()
            recommended_action = _review_action_from_message(msg)
            ambiguities = list(msg.get("ambiguities") or [])

            with st.container(border=True):
                if recommended_action == "confirm" or review_type == "confirmation":
                    st.markdown(f"**待确认执行** | {title}")
                elif recommended_action == "revise_required":
                    st.markdown(f"**需要修订计划** | {title}")
                elif recommended_action == "clarify":
                    st.markdown(f"**需要补充或澄清** | {title}")
                else:
                    st.markdown(f"**需要处理** | {title}")

                if review_type:
                    st.caption(f"type: `{review_type}`")
                if completeness_status:
                    st.caption(f"completeness: `{completeness_status}`")
                st.caption(f"recommended action: `{recommended_action}`")

                if resolved:
                    st.success(f"Handled: {str(msg.get('resolution') or 'resolved')}")
                elif recommended_action == "confirm" or review_type == "confirmation":
                    if st.button(
                        "Confirm and run",
                        type="primary",
                        key=f"review_confirm_run_{i}_{task_id}_{review_id}",
                    ):
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "thinking",
                                "action": "confirm_task",
                                "task_id": task_id,
                                "final_plan": None,
                            }
                        )
                        st.rerun()
                elif options and recommended_action == "confirm":
                    cols = st.columns(min(3, len(options)))
                    for idx, opt in enumerate(options):
                        with cols[idx % len(cols)]:
                            if st.button(opt, key=f"review_opt_{i}_{task_id}_{review_id}_{idx}"):
                                _enqueue_review_respond(task_id, choice=opt)
                                st.rerun()

                if body:
                    st.markdown(body)

                if review_type == "suggestion" or recommended_action in {"clarify", "revise_required"}:
                    if recommended_action == "revise_required":
                        st.error(
                            "This plan has material gaps. Revise the plan before treating it as a normal execution candidate."
                        )
                    else:
                        st.warning(
                            "This plan is not fully complete yet. Clarify the gaps below before deciding whether to continue."
                        )

                    if isinstance(suggested_plan, dict):
                        completeness = suggested_plan.get("completeness") or {}
                        open_questions = completeness.get("open_questions") or []
                        exploration_tasks = completeness.get("exploration_tasks") or []
                        missing_information = completeness.get("missing_information") or []

                        if open_questions:
                            st.markdown("**Open questions**")
                            for item in open_questions[:5]:
                                if isinstance(item, dict):
                                    question = str(item.get("question") or "").strip()
                                    if question:
                                        st.write(f"- {question}")

                        if exploration_tasks:
                            st.markdown("**Suggested next steps**")
                            for item in exploration_tasks[:5]:
                                if isinstance(item, dict):
                                    goal = str(item.get("goal") or "").strip()
                                    if goal:
                                        st.write(f"- {goal}")

                        if missing_information:
                            st.markdown("**Missing or unstable information**")
                            for item in missing_information[:5]:
                                if isinstance(item, dict):
                                    field = str(item.get("field") or "").strip()
                                    issue = str(item.get("issue") or "").strip()
                                    if field or issue:
                                        if field and issue:
                                            st.write(f"- {field}: {issue}")
                                        else:
                                            st.write(f"- {field or issue}")

                    if ambiguities:
                        st.markdown("**Plan ambiguities**")
                        for item in ambiguities[:5]:
                            if isinstance(item, dict):
                                field = str(item.get("field") or "").strip()
                                issue = str(item.get("issue") or "").strip()
                                if field or issue:
                                    if field and issue:
                                        st.write(f"- {field}: {issue}")
                                    else:
                                        st.write(f"- {field or issue}")

                    if recommended_action == "revise_required":
                        st.info(
                            "Reply in the chat input below with the changes or missing information needed to revise the current plan."
                        )
                    else:
                        st.info(
                            "Reply in the chat input below to supplement, clarify, or revise the current plan."
                        )

                st.caption(
                    "While a plan review is pending, your next text input will be consumed as input to supplement or revise the current plan."
                )

        elif mtype == "plan_review":
            task_id = msg["task_id"]
            plan = msg["plan"]
            with st.container(border=True):
                st.markdown("**分析计划**")
                st.write(summarize_plan(plan))
                _render_plan_tables(plan)
                conf = plan.get("confidence")
                if conf is not None:
                    if conf < 0.6:
                        st.warning(f"置信度偏低: **{conf:.2f}**，建议重点检查筛选条件和字段映射。")
                    else:
                        st.info(f"当前计划置信度: **{conf:.2f}**")
                for amb in plan.get("ambiguities") or []:
                    st.warning(f"`{amb.get('field', '?')}`: {amb.get('issue', '')}")
                plan_key = f"plan_json_{i}_{task_id}"
                if plan_key not in st.session_state:
                    st.session_state[plan_key] = json.dumps(plan, ensure_ascii=False, indent=2)
                with st.expander("查看原始计划 JSON（高级）", key=f"raw_plan_exp_{i}_{task_id}"):
                    st.text_area("Edit plan JSON", key=plan_key, height=260, label_visibility="collapsed")
                done_key = f"review_done_{task_id}"
                if st.session_state.get(done_key):
                    st.success("计划已执行，结果见下方结果卡片。")
                else:
                    st.caption("如需执行，请在下方 review 卡中确认；如需调整，请直接在聊天框补充说明。")

        elif mtype == "result":
            tid = msg["task_id"]
            with st.container(border=True):
                st.markdown("**分析结果**")
                _render_result_block(msg["result"], tid, key_suffix=f"{i}_{tid[:8]}")

        elif mtype == "task_done_confirm":
            tid = msg["task_id"]
            with st.container(border=True):
                st.markdown("**执行结果回顾**")
                st.write("如果这次执行结果还不满足目标，可以提交结果反馈并再次规划。")
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("满足，标记完成", type="primary", key=f"done_ok_{i}_{tid}"):
                        st.session_state.mode = "chat"
                        st.session_state.active_task_id = None
                        st.session_state.messages[i] = {
                            "role": "assistant",
                            "type": "text",
                            "content": "已标记完成。你可以继续追问，也可以重新发起新的 **`/task`** 任务。",
                        }
                        st.rerun()
                with b2:
                    note_key = f"replan_note_{i}_{tid}"
                    st.text_area("如果结果仍不满足，请补充缺失点", key=note_key, height=72)
                    if st.button("结果不满足，重新规划", key=f"done_replan_{i}_{tid}"):
                        note = (st.session_state.get(note_key) or "").strip() or "Needs a different analysis."
                        try:
                            rec = _get_task(tid)
                            orig_q = (rec.get("input") or {}).get("question", "")
                        except requests.RequestException:
                            orig_q = ""
                        combined = (
                            f"{orig_q}\n\nUser feedback (result not sufficient): {note}"
                            if orig_q
                            else f"User feedback (result not sufficient): {note}"
                        )
                        st.session_state.mode = "task"
                        st.session_state.messages[i] = {
                            "role": "assistant",
                            "type": "text",
                            "content": "正在根据你的结果反馈重新生成计划...",
                        }
                        st.session_state.messages.append(
                            {
                                "role": "assistant",
                                "type": "thinking",
                                "action": "create_task",
                                "question": combined.strip(),
                            }
                        )
                        st.rerun()
