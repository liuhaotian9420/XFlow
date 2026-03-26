from __future__ import annotations

from typing import Any

import streamlit as st


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2.4rem;
            padding-bottom: 1.25rem;
        }
        h1 {
            line-height: 1.2;
            padding-top: 0.12em;
            overflow: visible;
        }
        .xyf-page-title {
            display: block;
            margin: 0 0 0.35rem 0;
            padding-top: 0.75rem;
            line-height: 1.22;
            overflow: visible;
        }
        .xyf-library-hero {
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 1rem;
            padding: 1rem 1.1rem;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, rgba(255, 247, 236, 0.98), rgba(245, 248, 255, 0.98));
        }
        .xyf-library-kicker {
            font-size: 0.76rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: rgba(49, 51, 63, 0.62);
            margin-bottom: 0.25rem;
        }
        .xyf-library-title {
            font-size: 1.35rem;
            font-weight: 700;
            line-height: 1.2;
            margin-bottom: 0.25rem;
        }
        .xyf-library-copy {
            font-size: 0.95rem;
            color: rgba(49, 51, 63, 0.76);
            max-width: 52rem;
        }
        .xyf-artifact-list-shell {
            border: 1px solid rgba(49, 51, 63, 0.10);
            border-radius: 1rem;
            background: rgba(255, 255, 255, 0.88);
            padding: 0.85rem 0.9rem 0.4rem 0.9rem;
        }
        .xyf-artifact-sidepanel {
            border: 1px solid rgba(49, 51, 63, 0.10);
            border-radius: 1rem;
            background: linear-gradient(180deg, rgba(250, 251, 253, 0.98), rgba(245, 247, 251, 0.98));
            padding: 0.9rem;
        }
        .xyf-page-chip {
            display: flex;
            align-items: center;
            justify-content: center;
            min-height: 2.55rem;
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 0.75rem;
            background: rgba(255, 255, 255, 0.84);
            font-size: 0.9rem;
            color: rgba(49, 51, 63, 0.78);
        }
        div[data-testid="stChatMessage"] {
            margin-bottom: 0.5rem;
        }
        .xyf-status-card {
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 0.9rem;
            padding: 0.7rem 0.85rem;
            background: linear-gradient(180deg, rgba(250, 250, 252, 0.98), rgba(245, 246, 250, 0.98));
            min-height: 5rem;
        }
        .xyf-status-label {
            font-size: 0.78rem;
            color: rgba(49, 51, 63, 0.68);
            margin-bottom: 0.2rem;
        }
        .xyf-status-value {
            font-size: 1rem;
            font-weight: 600;
            line-height: 1.35;
        }
        .xyf-muted {
            font-size: 0.82rem;
            color: rgba(49, 51, 63, 0.68);
        }
        .xyf-task-card {
            border: 1px solid rgba(49, 51, 63, 0.10);
            border-radius: 0.9rem;
            padding: 0.75rem 0.8rem 0.6rem 0.8rem;
            background: linear-gradient(180deg, rgba(251, 251, 253, 0.98), rgba(246, 247, 250, 0.98));
            margin: 0.2rem 0 0.75rem 0;
        }
        .xyf-task-title {
            font-size: 0.95rem;
            font-weight: 600;
            line-height: 1.35;
            color: rgb(30, 33, 44);
            margin-bottom: 0.3rem;
            display: -webkit-box;
            -webkit-line-clamp: 2;
            -webkit-box-orient: vertical;
            overflow: hidden;
        }
        .xyf-task-meta {
            font-size: 0.78rem;
            color: rgba(49, 51, 63, 0.66);
            margin-bottom: 0.65rem;
        }
        .xyf-sidebar-panel {
            border: 1px solid rgba(49, 51, 63, 0.12);
            border-radius: 1rem;
            padding: 0.9rem 0.9rem 0.85rem 0.9rem;
            background: linear-gradient(180deg, rgba(255, 250, 244, 0.98), rgba(247, 249, 253, 0.98));
            margin-bottom: 0.75rem;
        }
        .xyf-sidebar-kicker {
            font-size: 0.74rem;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: rgba(49, 51, 63, 0.58);
            margin-bottom: 0.28rem;
        }
        .xyf-sidebar-headline {
            font-size: 1.02rem;
            font-weight: 700;
            line-height: 1.25;
            color: rgb(28, 30, 39);
            margin-bottom: 0.75rem;
        }
        .xyf-sidebar-grid {
            display: grid;
            gap: 0.55rem;
            margin-bottom: 0.7rem;
        }
        .xyf-sidebar-cell {
            border: 1px solid rgba(49, 51, 63, 0.08);
            border-radius: 0.8rem;
            background: rgba(255, 255, 255, 0.66);
            padding: 0.68rem 0.72rem;
        }
        .xyf-sidebar-label {
            font-size: 0.74rem;
            color: rgba(49, 51, 63, 0.6);
            margin-bottom: 0.15rem;
        }
        .xyf-sidebar-value {
            font-size: 0.92rem;
            font-weight: 600;
            line-height: 1.3;
            color: rgb(30, 33, 44);
            margin-bottom: 0.18rem;
            word-break: break-word;
        }
        .xyf-sidebar-meta {
            font-size: 0.78rem;
            color: rgba(49, 51, 63, 0.66);
            line-height: 1.35;
        }
        .xyf-sidebar-system {
            margin-bottom: 0.65rem;
        }
        .xyf-sidebar-system-row {
            border: 1px solid rgba(49, 51, 63, 0.08);
            border-radius: 0.85rem;
            background: rgba(247, 248, 250, 0.92);
            padding: 0.65rem 0.75rem;
        }
        .xyf-sidebar-system-title {
            font-size: 0.74rem;
            color: rgba(49, 51, 63, 0.58);
            margin-bottom: 0.18rem;
        }
        .xyf-sidebar-system-copy {
            font-size: 0.79rem;
            color: rgba(49, 51, 63, 0.72);
            line-height: 1.35;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def _task_status_label() -> str:
    active_task_id = str(st.session_state.get("active_task_id") or "").strip()
    if not active_task_id:
        return "Idle"
    for msg in reversed(st.session_state.messages):
        if str(msg.get("task_id") or "").strip() != active_task_id:
            continue
        mtype = str(msg.get("type") or "").strip()
        if mtype == "thinking" and msg.get("action") == "confirm_task":
            return "Running"
        if mtype in ("task_done_confirm", "result"):
            return "Done"
        if mtype == "review_request" and not bool(msg.get("resolved")):
            return "Waiting for input"
        if mtype == "plan_review":
            return "Waiting for confirmation"
    return "In progress"


def render_status_panel() -> None:
    file_meta = st.session_state.get("file_meta") or {}
    file_name = str(file_meta.get("name") or "No file uploaded")
    mode_label = "Task" if st.session_state.get("mode") == "task" else "Chat"
    session_id = str(st.session_state.get("chat_session_id") or "")[:8]
    task_status = _task_status_label()
    active_task = str(st.session_state.get("active_task_id") or "").strip()

    cols = st.columns(3)
    items = [
        ("Current mode", mode_label, f"session `{session_id}...`" if session_id else "session not initialized"),
        ("Current file", file_name, "Supports CSV / Excel"),
        ("Task status", task_status, f"task `{active_task[:8]}...`" if active_task else "No active task"),
    ]
    for col, (label, value, sub) in zip(cols, items):
        with col:
            st.markdown(
                (
                    '<div class="xyf-status-card">'
                    f'<div class="xyf-status-label">{label}</div>'
                    f'<div class="xyf-status-value">{value}</div>'
                    f'<div class="xyf-muted">{sub}</div>'
                    "</div>"
                ),
                unsafe_allow_html=True,
            )


def summarize_plan(plan: dict[str, Any]) -> str:
    goal = str(plan.get("goal") or "").strip()
    metrics = plan.get("metrics") or []
    dims = plan.get("dimensions") or []
    out = plan.get("output") or {}
    metric_names = [
        str(item.get("name") or item.get("field") or "").strip()
        for item in metrics[:2]
        if isinstance(item, dict)
    ]
    dim_names = [
        str(item.get("name") or item.get("field") or "").strip()
        for item in dims[:2]
        if isinstance(item, dict)
    ]
    metric_text = ", ".join([x for x in metric_names if x]) or "key metrics"
    dim_text = ", ".join([x for x in dim_names if x]) or "main dimensions"
    chart_text = str(out.get("chart_type") or "chart").strip() or "chart"
    if goal:
        return f"The plan analyzes '{goal}' using {metric_text}, broken down by {dim_text}, and outputs a {chart_text}."
    return f"The plan analyzes {metric_text}, broken down by {dim_text}, and outputs a {chart_text}."


def result_summary_text(result: dict[str, Any]) -> str:
    summary = str(result.get("summary") or "").strip()
    if summary:
        return summary
    execution_summary = str(result.get("execution_summary") or "").strip()
    if execution_summary:
        return execution_summary
    table = result.get("table") or {}
    rows = table.get("rows") or []
    if rows:
        return f"Analysis finished with {len(rows)} rows."
    return "Analysis finished."
