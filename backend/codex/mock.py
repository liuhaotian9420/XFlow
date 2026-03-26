"""Mock provider for development and testing (no CLI)."""

from __future__ import annotations

from backend.planning.adapters import parse_plan_payload
from backend.schemas.plan import (
    Aggregation,
    AmbiguitySpec,
    AnalysisPlan,
    ChartType,
    DimensionRole,
    DimensionSpec,
    ExplorationPriority,
    ExplorationTaskSpec,
    FilterOperator,
    FilterSpec,
    MetricSpec,
    OutputSpec,
    PlanAssumptionSpec,
    PlanCompletenessSpec,
    PlanCompletenessStatus,
    PlanQuestionSpec,
)


class MockProvider:
    """Return deterministic plans and summaries without invoking an external agent."""

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "mock"
    ) -> AnalysisPlan:
        self.last_raw_skill_plan: dict | None = None
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
        dimensions: list[DimensionSpec] = []
        if time_col:
            dimensions.append(DimensionSpec(column=time_col, role=DimensionRole.TIME))
        if category_col and category_col != time_col:
            dimensions.append(
                DimensionSpec(column=category_col, role=DimensionRole.CATEGORY)
            )

        filters: list[FilterSpec] = []
        lower_question = question.lower()
        if ("east" in lower_question or "east china" in lower_question) and "region" in columns:
            filters.append(
                FilterSpec(column="region", operator=FilterOperator.EQ, value="east")
            )
        if any(token in lower_question for token in ("latest", "recent", "2025")) and time_col:
            filters.append(
                FilterSpec(
                    column=time_col,
                    operator=FilterOperator.CONTAINS,
                    value="2025",
                )
            )

        chart_type = ChartType.LINE if time_col else ChartType.BAR
        if "distribution" in lower_question:
            chart_type = ChartType.HISTOGRAM
        elif "compare" in lower_question:
            chart_type = ChartType.BAR

        confidence, ambiguities = self._assess_confidence(
            question=question,
            columns=columns,
            metric_col=metric_col,
            time_col=time_col,
            category_col=category_col,
            filters=filters,
        )
        completeness = self._build_completeness(
            question=question,
            ambiguities=ambiguities,
            time_col=time_col,
            category_col=category_col,
        )

        plan = AnalysisPlan(
            goal=question.strip() or "Analyze uploaded data",
            metrics=metrics,
            dimensions=dimensions,
            filters=filters,
            output=OutputSpec(chart_type=chart_type, show_table=True),
            assumptions=self._build_assumptions(
                metric_col=metric_col,
                time_col=time_col,
            ),
            confidence=confidence,
            ambiguities=ambiguities,
            completeness=completeness,
        )
        parsed, raw_skill = parse_plan_payload(plan.model_dump(mode="json"))
        self.last_raw_skill_plan = raw_skill
        return parsed

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
            f"Do you want to continue with a time trend analysis for '{goal}'?",
            "Do you want a category or region comparison next?",
            "Do you want to inspect the detailed rows behind outliers?",
        ]

    async def chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        task_id: str = "mock",
    ) -> str:
        if file_context:
            filename = file_context.get("filename", "unknown")
            rows = file_context.get("row_count", "?")
            cols = file_context.get("column_count", "?")
            col_names = [
                c.get("name")
                for c in (file_context.get("columns") or [])
                if isinstance(c, dict) and c.get("name")
            ]
            col_hint = ", ".join(col_names[:12]) if col_names else "no column names available"
            return (
                f"[Mock chat]\nLoaded file: {filename} ({rows} rows, {cols} columns).\n"
                f"Columns: {col_hint}\n\n"
                f"Question: {message.strip()[:500]}\n\n"
                "If you want an executable analysis, use `/task` followed by the analysis request."
            )
        return (
            "[Mock chat]\nNo tabular file schema is loaded yet.\n\n"
            f"Question: {message.strip()[:500]}\n\n"
            "Attach a CSV or Excel file first, then use `/task` to generate a structured plan."
        )

    async def revise_plan(
        self,
        current_plan: AnalysisPlan,
        instruction: str,
        schema_profile: dict,
        task_id: str = "mock",
    ) -> AnalysisPlan:
        self.last_raw_skill_plan = None
        data = current_plan.model_dump()
        short = instruction.strip()[:300] or "user revision"
        data["goal"] = f"{data.get('goal', '')} | revised: {short}"

        ambiguities = list(data.get("ambiguities") or [])
        ambiguities.append({"field": "revision", "issue": short})
        data["ambiguities"] = ambiguities

        completeness = dict(data.get("completeness") or {})
        completeness["status"] = PlanCompletenessStatus.NEEDS_EXPLORATION.value
        completeness["rationale"] = (
            "Plan was revised from user feedback and should be re-checked for completeness."
        )
        completeness["score"] = round(
            max(0.0, min(1.0, float(completeness.get("score", 0.8)) - 0.05)),
            2,
        )
        open_questions = list(completeness.get("open_questions") or [])
        open_questions.append(
            {
                "question": f"Does the revision '{short}' change metric, filter, or grouping semantics?",
                "reason": "User feedback changed the plan and may invalidate prior assumptions.",
                "blocking": False,
                "priority": ExplorationPriority.MEDIUM.value,
                "related_fields": ["goal", "metrics", "dimensions", "filters"],
            }
        )
        completeness["open_questions"] = open_questions
        missing_information = list(completeness.get("missing_information") or [])
        missing_information.extend(ambiguities[-1:])
        completeness["missing_information"] = missing_information
        data["completeness"] = completeness

        confidence = data.get("confidence")
        if confidence is not None:
            data["confidence"] = round(
                max(0.0, min(1.0, float(confidence) - 0.05)),
                2,
            )
        parsed, raw_skill = parse_plan_payload(data)
        self.last_raw_skill_plan = raw_skill
        return parsed

    @staticmethod
    def _build_assumptions(
        metric_col: str,
        time_col: str | None,
    ) -> list[PlanAssumptionSpec]:
        assumptions = [
            PlanAssumptionSpec(
                statement=f"Use '{metric_col}' as the primary metric.",
                impact="If this metric is not intended, aggregate results will not answer the real question.",
            )
        ]
        if time_col:
            assumptions.append(
                PlanAssumptionSpec(
                    statement=f"Use '{time_col}' as the primary time axis.",
                    impact="Trend and recency analysis depend on this column representing business time.",
                )
            )
        return assumptions

    @staticmethod
    def _build_completeness(
        question: str,
        ambiguities: list[AmbiguitySpec],
        time_col: str | None,
        category_col: str | None,
    ) -> PlanCompletenessSpec:
        if not ambiguities:
            return PlanCompletenessSpec()

        status = PlanCompletenessStatus.NEEDS_EXPLORATION
        score = 0.75
        open_questions: list[PlanQuestionSpec] = []
        exploration_tasks: list[ExplorationTaskSpec] = []

        if not time_col and any(
            kw in question.lower() for kw in ("trend", "recent", "time", "latest")
        ):
            status = PlanCompletenessStatus.BLOCKED
            score = 0.45
            open_questions.append(
                PlanQuestionSpec(
                    question="Which column should be used as the time dimension?",
                    reason="The request implies time-based analysis but no time column was confidently detected.",
                    blocking=True,
                    priority=ExplorationPriority.HIGH,
                    related_fields=["dimensions"],
                )
            )

        if not category_col:
            open_questions.append(
                PlanQuestionSpec(
                    question="Is a categorical split needed, or is a single aggregate acceptable?",
                    reason="No obvious category dimension was identified.",
                    blocking=False,
                    priority=ExplorationPriority.MEDIUM,
                    related_fields=["dimensions", "output"],
                )
            )

        exploration_tasks.append(
            ExplorationTaskSpec(
                goal="Validate whether the chosen metric and dimensions match the user's business intent.",
                rationale="Fallback selections were used for part of the draft plan.",
                priority=ExplorationPriority.MEDIUM,
                inputs=["question", "schema_profile", "current plan draft"],
                success_criteria=[
                    "Primary metric is confirmed",
                    "Grouping dimensions are confirmed or adjusted",
                ],
            )
        )

        return PlanCompletenessSpec(
            status=status,
            score=score,
            rationale=(
                "The draft plan is executable, but some fields were inferred and should be explored "
                "before autonomous task execution."
            ),
            missing_information=ambiguities,
            open_questions=open_questions,
            exploration_tasks=exploration_tasks,
        )

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

        has_time_keyword = any(
            kw in question.lower() for kw in ("trend", "change", "recent", "latest", "time")
        )
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
        elif any(kw in question.lower() for kw in ("east", "west", "north", "south", "only", "exclude")):
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
