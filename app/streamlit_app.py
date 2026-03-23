from __future__ import annotations

import json
import os
from typing import Any

import pandas as pd
import requests
import streamlit as st

API_BASE_URL = os.getenv("API_BASE_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="xyf-competition-mvp", layout="wide")
st.title("xyf-competition-mvp")
st.caption("Ask -> Plan -> Review -> Results")


def _init_state() -> None:
    st.session_state.setdefault("task_id", None)
    st.session_state.setdefault("plan", None)
    st.session_state.setdefault("task_status", None)
    st.session_state.setdefault("result", None)


def _api_url(path: str) -> str:
    return f"{API_BASE_URL.rstrip('/')}{path}"


def _post_task(file_obj, question: str) -> dict[str, Any]:
    payload = {"question": question}
    files = {"file": (file_obj.name, file_obj.getvalue(), file_obj.type)}
    response = requests.post(_api_url("/tasks"), data=payload, files=files, timeout=90)
    response.raise_for_status()
    return response.json()


def _post_review(task_id: str, final_plan: dict[str, Any]) -> dict[str, Any]:
    response = requests.post(
        _api_url(f"/tasks/{task_id}/review"),
        json={"final_plan": final_plan},
        timeout=90,
    )
    response.raise_for_status()
    return response.json()


def _get_task(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}"), timeout=30)
    response.raise_for_status()
    return response.json()


def _get_result(task_id: str) -> dict[str, Any]:
    response = requests.get(_api_url(f"/tasks/{task_id}/result"), timeout=90)
    response.raise_for_status()
    return response.json()


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


_init_state()

tab_ask, tab_plan, tab_review, tab_results = st.tabs(
    ["Ask", "Plan", "Review", "Results"]
)

with tab_ask:
    st.subheader("Ask")
    question = st.text_area(
        "Describe your analysis question",
        placeholder="例如：帮我看华东区最近三个月销售趋势",
    )
    uploaded = st.file_uploader("Upload CSV/Excel", type=["csv", "xlsx", "xls"])
    if uploaded is not None:
        try:
            preview_df = (
                pd.read_csv(uploaded)
                if uploaded.name.endswith(".csv")
                else pd.read_excel(uploaded)
            )
            st.write("Preview (top 10 rows)")
            st.dataframe(preview_df.head(10), use_container_width=True)
            st.write("Schema")
            schema_view = pd.DataFrame(
                {"column": preview_df.columns, "dtype": preview_df.dtypes.astype(str)}
            )
            st.dataframe(schema_view, use_container_width=True)
        except Exception as exc:
            st.warning(f"Local preview failed: {exc}")

    if st.button("Create Task", type="primary"):
        if not question.strip():
            st.error("Question is required.")
        elif uploaded is None:
            st.error("Please upload a file.")
        else:
            try:
                result = _post_task(uploaded, question.strip())
                st.session_state.task_id = result["task_id"]
                st.session_state.plan = result["plan"]
                st.session_state.task_status = result["status"]
                st.success(f"Task created: {result['task_id']}")
            except requests.RequestException as exc:
                st.error(f"Failed to create task: {exc}")

with tab_plan:
    st.subheader("Plan")
    task_id = st.session_state.task_id
    if not task_id:
        st.info("Create a task in Ask tab first.")
    else:
        if st.button("Refresh Plan from Backend"):
            try:
                task_payload = _get_task(task_id)
                st.session_state.plan = task_payload.get("plan")
                st.session_state.task_status = task_payload.get("status")
            except requests.RequestException as exc:
                st.error(f"Failed to refresh task: {exc}")
        st.write(f"Task ID: `{task_id}`")
        st.write(f"Status: `{st.session_state.task_status}`")
        st.json(st.session_state.plan or {}, expanded=True)

with tab_review:
    st.subheader("Review")
    plan = st.session_state.plan
    task_id = st.session_state.task_id
    if not task_id or not plan:
        st.info("No plan available yet.")
    else:
        confidence = plan.get("confidence")
        if confidence is not None:
            if confidence < 0.6:
                st.warning(f"Low confidence plan: {confidence:.2f}. Please review carefully.")
            else:
                st.info(f"Plan confidence: {confidence:.2f}")
        ambiguities = plan.get("ambiguities", [])
        if ambiguities:
            st.markdown("**Ambiguities detected**")
            for item in ambiguities:
                st.markdown(
                    f"- `{item.get('field', 'unknown')}`: {item.get('issue', '')}"
                )

        editable = st.text_area(
            "Edit final plan JSON",
            value=json.dumps(plan, ensure_ascii=False, indent=2),
            height=360,
        )
        if st.button("Submit Review and Run", type="primary"):
            try:
                final_plan = json.loads(editable)
                payload = _post_review(task_id, final_plan)
                st.session_state.task_status = payload.get("status")
                st.success("Review submitted.")
            except json.JSONDecodeError as exc:
                st.error(f"Invalid JSON: {exc}")
            except requests.RequestException as exc:
                st.error(f"Failed to submit review: {exc}")

with tab_results:
    st.subheader("Results")
    task_id = st.session_state.task_id
    if not task_id:
        st.info("No task found.")
    else:
        if st.button("Fetch Result", type="primary"):
            try:
                payload = _get_result(task_id)
                st.session_state.result = payload
                task_payload = _get_task(task_id)
                st.session_state.task_status = task_payload.get("status")
            except requests.RequestException as exc:
                st.error(f"Failed to get result: {exc}")

        result = st.session_state.result
        if not result:
            st.info("Result not loaded yet.")
        elif "chart" not in result:
            status = st.session_state.task_status or "unknown"
            message = result.get("message", "")
            if status == "failed":
                st.error("System execution failed. Please check plan fields and retry.")
            elif "not ready" in message.lower():
                st.info("Task is still running. Try again in a few seconds.")
            else:
                st.warning("Please refine your question and review plan fields.")
            st.write(result)
        else:
            _draw_chart(result["chart"])
            table_df = pd.DataFrame(result["table"]["rows"])
            st.dataframe(table_df, use_container_width=True)
            if not table_df.empty:
                st.download_button(
                    "Download table CSV",
                    data=table_df.to_csv(index=False).encode("utf-8"),
                    file_name=f"{task_id}_result.csv",
                    mime="text/csv",
                )
            st.caption(result.get("execution_summary", ""))
            if result.get("summary"):
                st.write(result["summary"])
            if result.get("follow_ups"):
                st.write("Follow-ups")
                for item in result["follow_ups"]:
                    st.markdown(f"- {item}")
