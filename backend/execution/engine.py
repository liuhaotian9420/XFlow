"""Execution engine for running AnalysisPlan over pandas dataframes."""

from __future__ import annotations

from typing import Any

import pandas as pd

from backend.schemas.plan import AnalysisPlan, FilterOperator
from backend.schemas.result import ChartPayload, ResultPayload, TablePayload


def run_plan(df: pd.DataFrame, plan: AnalysisPlan) -> ResultPayload:
    """Execute a plan and convert the output to a stable payload."""
    work_df = df.copy()

    execution_steps: list[str] = []
    work_df, filter_summary = _apply_filters(work_df, plan)
    if filter_summary:
        execution_steps.extend(filter_summary)

    grouped_df, metric_aliases = _aggregate(work_df, plan, execution_steps)
    chart = _build_chart(grouped_df, plan)
    table = TablePayload(columns=list(grouped_df.columns), rows=grouped_df.to_dict("records"))

    if not execution_steps:
        execution_steps.append("No filters or aggregations were applied.")
    if metric_aliases:
        execution_steps.append(f"Output metrics: {', '.join(metric_aliases)}.")
    execution_summary = " ".join(execution_steps)

    return ResultPayload(chart=chart, table=table, execution_summary=execution_summary)


def _apply_filters(
    df: pd.DataFrame, plan: AnalysisPlan
) -> tuple[pd.DataFrame, list[str]]:
    steps: list[str] = []
    filtered = df
    for f in plan.filters:
        if f.column not in filtered.columns:
            continue
        before = len(filtered)
        series = filtered[f.column]
        value = f.value
        operator = f.operator
        if operator == FilterOperator.EQ:
            filtered = filtered[series == value]
        elif operator == FilterOperator.NEQ:
            filtered = filtered[series != value]
        elif operator == FilterOperator.GT:
            filtered = filtered[series > value]
        elif operator == FilterOperator.GTE:
            filtered = filtered[series >= value]
        elif operator == FilterOperator.LT:
            filtered = filtered[series < value]
        elif operator == FilterOperator.LTE:
            filtered = filtered[series <= value]
        elif operator == FilterOperator.IN:
            values = value if isinstance(value, list) else [value]
            filtered = filtered[series.isin(values)]
        elif operator == FilterOperator.NOT_IN:
            values = value if isinstance(value, list) else [value]
            filtered = filtered[~series.isin(values)]
        elif operator == FilterOperator.CONTAINS:
            filtered = filtered[series.astype(str).str.contains(str(value), na=False)]
        steps.append(
            f"Filter {f.column} {f.operator.value} {value}: {before} -> {len(filtered)} rows."
        )
    return filtered, steps


def _aggregate(
    df: pd.DataFrame, plan: AnalysisPlan, steps: list[str]
) -> tuple[pd.DataFrame, list[str]]:
    if not plan.metrics:
        return df.head(200), []

    metric_aliases: list[str] = []
    agg_map: dict[str, Any] = {}
    rename_map: dict[str, str] = {}
    for metric in plan.metrics:
        if metric.column not in df.columns:
            continue
        agg_map[metric.column] = metric.aggregation.value
        alias = metric.alias or f"{metric.column}_{metric.aggregation.value}"
        rename_map[metric.column] = alias
        metric_aliases.append(alias)

    if not agg_map:
        return df.head(200), metric_aliases

    dimension_cols = [d.column for d in plan.dimensions if d.column in df.columns]
    if dimension_cols:
        grouped_df = df.groupby(dimension_cols, dropna=False).agg(agg_map).reset_index()
        steps.append(f"Grouped by {', '.join(dimension_cols)}.")
    else:
        grouped_df = pd.DataFrame([df.agg(agg_map)])
        steps.append("Aggregated without grouping.")

    grouped_df = grouped_df.rename(columns=rename_map)
    grouped_df = grouped_df.head(500)
    return grouped_df, metric_aliases


def _build_chart(df: pd.DataFrame, plan: AnalysisPlan) -> ChartPayload:
    chart_type = plan.output.chart_type

    x_col = _pick_x_column(df, plan)
    y_col = _pick_y_column(df, plan, x_col)
    chart_df = df[[x_col, y_col]].copy() if x_col in df.columns and y_col in df.columns else df

    if chart_type.value == "histogram" and y_col in df.columns:
        histogram_df = df[y_col].value_counts().rename_axis(y_col).reset_index(name="count")
        return ChartPayload(
            chart_type=chart_type,
            x=y_col,
            y="count",
            data=histogram_df.to_dict("records"),
        )

    return ChartPayload(
        chart_type=chart_type,
        x=x_col,
        y=y_col,
        data=chart_df.to_dict("records"),
    )


def _pick_x_column(df: pd.DataFrame, plan: AnalysisPlan) -> str:
    for dim in plan.dimensions:
        if dim.column in df.columns:
            return dim.column
    return str(df.columns[0])


def _pick_y_column(df: pd.DataFrame, plan: AnalysisPlan, x_col: str) -> str:
    for metric in plan.metrics:
        alias = metric.alias or f"{metric.column}_{metric.aggregation.value}"
        if alias in df.columns:
            return alias
        if metric.column in df.columns and metric.column != x_col:
            return metric.column
    for col in df.columns:
        if col != x_col:
            return str(col)
    return x_col

