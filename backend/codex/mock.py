"""Mock adapter for development and testing."""

from __future__ import annotations

from backend.schemas.plan import (
    Aggregation,
    AnalysisPlan,
    ChartType,
    DimensionRole,
    DimensionSpec,
    FilterOperator,
    FilterSpec,
    MetricSpec,
    OutputSpec,
)


class MockAdapter:
    """Return deterministic plans/summaries without invoking Codex CLI."""

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "mock"
    ) -> AnalysisPlan:
        columns = {col["name"] for col in schema_profile.get("columns", [])}
        metric_col = self._pick_metric_column(columns)
        time_col = self._pick_time_column(columns)
        category_col = self._pick_category_column(columns, fallback=time_col)

        metrics = [
            MetricSpec(
                column=metric_col,
                aggregation=Aggregation.SUM,
                alias=f"{metric_col}_sum",
            )
        ]
        dimensions = []
        if time_col:
            dimensions.append(DimensionSpec(column=time_col, role=DimensionRole.TIME))
        if category_col and category_col != time_col:
            dimensions.append(
                DimensionSpec(column=category_col, role=DimensionRole.CATEGORY)
            )

        filters: list[FilterSpec] = []
        lower_question = question.lower()
        if "华东" in question and "region" in columns:
            filters.append(
                FilterSpec(column="region", operator=FilterOperator.EQ, value="华东")
            )
        if "最近" in question and time_col:
            filters.append(
                FilterSpec(
                    column=time_col,
                    operator=FilterOperator.CONTAINS,
                    value="2025",
                )
            )

        chart_type = ChartType.LINE if time_col else ChartType.BAR
        if "分布" in question or "distribution" in lower_question:
            chart_type = ChartType.HISTOGRAM

        return AnalysisPlan(
            goal=question.strip() or "Analyze uploaded data",
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            output=OutputSpec(chart_type=chart_type, show_table=True),
        )

    async def generate_summary(
        self,
        goal: str,
        result_df_summary: dict,
        plan: AnalysisPlan | None = None,
        task_id: str = "mock",
    ) -> str:
        used_goal = goal if goal else (plan.goal if plan else "Analyze uploaded data")
        return (
            f"Executed plan for goal '{used_goal}'. "
            f"Returned {result_df_summary.get('row_count', 0)} rows."
        )

    async def generate_followups(
        self, goal: str, result_df_summary: dict, task_id: str = "mock"
    ) -> list[str]:
        return [
            f"是否需要按时间趋势继续分析：{goal}？",
            "是否需要按区域或部门做对比？",
            "是否需要定位异常峰值对应的明细记录？",
        ]

    @staticmethod
    def _pick_metric_column(columns: set[str]) -> str:
        for candidate in ("amount", "sales_amount", "score", "visits", "y", "value"):
            if candidate in columns:
                return candidate
        for col in columns:
            if col not in {"date", "month", "region", "dept", "product", "source"}:
                return col
        return next(iter(columns), "value")

    @staticmethod
    def _pick_time_column(columns: set[str]) -> str | None:
        for candidate in ("date", "month", "order_date", "created_at"):
            if candidate in columns:
                return candidate
        return None

    @staticmethod
    def _pick_category_column(columns: set[str], fallback: str | None) -> str | None:
        for candidate in ("region", "dept", "product", "source", "page"):
            if candidate in columns:
                return candidate
        for col in columns:
            if col != fallback:
                return col
        return fallback

