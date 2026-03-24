"""Mock provider for development and testing (no CLI)."""

from __future__ import annotations

from backend.schemas.plan import (
    Aggregation,
    AmbiguitySpec,
    AnalysisPlan,
    ChartType,
    DimensionRole,
    DimensionSpec,
    FilterOperator,
    FilterSpec,
    MetricSpec,
    OutputSpec,
)


class MockProvider:
    """Return deterministic plans/summaries without invoking an external agent."""

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
        elif "对比" in question or "比较" in question or "compare" in lower_question:
            chart_type = ChartType.BAR

        confidence, ambiguities = self._assess_confidence(
            question=question,
            columns=columns,
            metric_col=metric_col,
            time_col=time_col,
            category_col=category_col,
            filters=filters,
        )

        return AnalysisPlan(
            goal=question.strip() or "Analyze uploaded data",
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            output=OutputSpec(chart_type=chart_type, show_table=True),
            confidence=confidence,
            ambiguities=ambiguities,
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

    async def chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        task_id: str = "mock",
    ) -> str:
        fname = None
        rows = None
        cols = None
        if file_context:
            fname = file_context.get("filename")
            rows = file_context.get("row_count")
            cols = file_context.get("column_count")
            col_names = [
                c.get("name")
                for c in (file_context.get("columns") or [])
                if isinstance(c, dict) and c.get("name")
            ]
            col_hint = (
                f"主要字段包括：{', '.join(col_names[:12])}"
                + ("…" if len(col_names) > 12 else "")
                if col_names
                else "字段列表可在后续分析步骤中确认。"
            )
            ctx = (
                f"当前已加载数据文件 `{fname or 'unknown'}`"
                f"（约 {rows} 行、{cols} 列）。{col_hint}"
            )
        else:
            ctx = "目前还没有可用的表格结构信息；如需针对数据提问，请先通过回形针上传 CSV/Excel。"

        return (
            f"（Mock 对话）{ctx}\n\n"
            f"关于你的问题：{message.strip()[:500]}\n\n"
            "建议：若要进行可执行的分析，请在聊天中输入 **`/task`** 加上你的分析需求，"
            "系统会生成结构化计划供你确认后再运行。"
        )

    async def revise_plan(
        self,
        current_plan: AnalysisPlan,
        instruction: str,
        schema_profile: dict,
        task_id: str = "mock",
    ) -> AnalysisPlan:
        data = current_plan.model_dump()
        short = instruction.strip()[:300] or "用户修订"
        data["goal"] = f"{data.get('goal', '')} · 修订：{short}"
        amb = list(data.get("ambiguities") or [])
        amb.append({"field": "revision", "issue": short})
        data["ambiguities"] = amb
        conf = data.get("confidence")
        if conf is not None:
            data["confidence"] = round(max(0.0, min(1.0, float(conf) - 0.05)), 2)
        return AnalysisPlan.model_validate(data)

    @staticmethod
    def _assess_confidence(
        question: str,
        columns: set[str],
        metric_col: str,
        time_col: str | None,
        category_col: str | None,
        filters: list[FilterSpec],
    ) -> tuple[float, list[AmbiguitySpec]]:
        score = 0.7
        ambiguities: list[AmbiguitySpec] = []

        well_known_metrics = {"amount", "sales_amount", "score", "visits", "value"}
        if metric_col in well_known_metrics:
            score += 0.1
        else:
            ambiguities.append(
                AmbiguitySpec(
                    field="metrics[0].column",
                    issue=f"'{metric_col}' was chosen as metric by fallback; verify it is the correct numeric column",
                )
            )
            score -= 0.1

        if not time_col and not category_col:
            ambiguities.append(
                AmbiguitySpec(
                    field="dimensions",
                    issue="No time or category column detected; result will be a single aggregate row",
                )
            )
            score -= 0.1

        has_time_keyword = any(kw in question for kw in ("趋势", "变化", "trend", "月", "季"))
        if has_time_keyword and not time_col:
            ambiguities.append(
                AmbiguitySpec(
                    field="dimensions",
                    issue="Question mentions time analysis but no date column was found in the data",
                )
            )
            score -= 0.15

        if filters:
            score += 0.05
        elif any(kw in question for kw in ("华东", "华南", "华北", "只看", "排除")):
            ambiguities.append(
                AmbiguitySpec(
                    field="filters",
                    issue="Question mentions a filter condition but no matching column was found",
                )
            )
            score -= 0.1

        return round(max(0.0, min(1.0, score)), 2), ambiguities

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


MockAdapter = MockProvider

__all__ = ["MockAdapter", "MockProvider"]
