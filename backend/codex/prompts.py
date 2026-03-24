"""Prompt templates for Codex CLI requests."""

from __future__ import annotations

import json


def _skill_context_block(skill_instructions: str | None) -> str:
    """Optional prefix from ``SKILL.md`` body (injected for non-native agents)."""
    if not skill_instructions or not str(skill_instructions).strip():
        return ""
    return f"## Skill Context\n\n{skill_instructions.strip()}\n\n---\n\n"


def build_plan_prompt(
    question: str,
    schema_profile: dict,
    *,
    skill_instructions: str | None = None,
) -> str:
    schema_json = json.dumps(schema_profile, ensure_ascii=False, indent=2)
    example = """
{
  "goal": "Compare sales by region last quarter",
  "metrics": [{"column": "amount", "aggregation": "sum", "alias": "amount_sum"}],
  "dimensions": [
    {"column": "date", "role": "time"},
    {"column": "region", "role": "category"}
  ],
  "filters": [{"column": "region", "operator": "eq", "value": "华东"}],
  "output": {"chart_type": "line", "show_table": true},
  "ambiguities": [{"field": "date", "issue": "Assuming column date is parseable as time"}],
  "confidence": 0.75
}
""".strip()
    prefix = _skill_context_block(skill_instructions)
    return f"""{prefix}You are an analysis planning assistant for tabular data.

CRITICAL output rules:
- Respond with ONE JSON object only.
- No markdown, no code fences, no explanation before or after the JSON.
- Use only column names that appear in the schema profile below.
- "aggregation" must be one of: sum, mean, count, max, min, median.
- "operator" must be one of: eq, neq, gt, gte, lt, lte, in, not_in, contains.
- "role" must be one of: time, category, geo.
- "chart_type" must be one of: line, bar, histogram.
- Chart selection (match the user's intent):
  - Use "line" for time trends: words like 趋势, 变化, 走势, 增长, 按月, 按日, trend, over time.
  - Use "bar" for category comparison: 对比, 比较, 各部门, 各区域, 排名, compare.
  - Use "histogram" when the user asks for 分布, distribution, 频率分布, or per-category share of a single numeric measure (e.g. 各渠道流量分布): set chart_type to "histogram", not "bar".
  - Use "bar" only for explicit side-by-side comparison of metrics across categories (对比/比较), not for 分布 wording.
- Filters on date/time columns: use operators gt, gte, lt, lte, eq with concrete values (e.g. ISO dates "2025-01-01") when possible. Do NOT use operator "contains" on date columns with vague Chinese phrases — that usually filters out all rows.
- If row_count in the schema is small (under ~20), keep filters minimal so the result is not empty unless the user clearly requires a strict slice.
- Set "confidence" between 0.0 and 1.0. List real uncertainties in "ambiguities".

Example of valid output (structure only; adapt columns to the real schema):
{example}

Question:
{question}

Schema profile:
{schema_json}

Output JSON must match this shape (field names and types):
{{
  "goal": "string",
  "metrics": [
    {{"column": "string", "aggregation": "sum|mean|count|max|min|median", "alias": "string|null"}}
  ],
  "dimensions": [
    {{"column": "string", "role": "time|category|geo"}}
  ],
  "filters": [
    {{"column": "string", "operator": "eq|neq|gt|gte|lt|lte|in|not_in|contains", "value": "any"}}
  ],
  "output": {{
    "chart_type": "line|bar|histogram",
    "show_table": true
  }},
  "ambiguities": [{{"field": "string", "issue": "string"}}],
  "confidence": 0.0
}}
""".strip()


def build_summary_prompt(
    goal: str,
    result_summary: dict,
    *,
    skill_instructions: str | None = None,
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    prefix = _skill_context_block(skill_instructions)
    return f"""{prefix}You are a data analysis explainer.
Return plain text summary in Chinese, 2-4 short sentences.

Goal:
{goal}

Result summary:
{result_json}
""".strip()


def build_chat_prompt(
    message: str,
    history: list[dict],
    file_context: dict | None,
    *,
    skill_instructions: str | None = None,
) -> str:
    """Build a conversational prompt (plain-text reply, not JSON)."""
    history_lines: list[str] = []
    for turn in history[-20:]:
        role = turn.get("role", "user")
        content = (turn.get("content") or "").strip()
        if not content:
            continue
        history_lines.append(f"{role}: {content}")
    history_block = "\n".join(history_lines) if history_lines else "(no prior turns)"

    if file_context:
        ctx_json = json.dumps(file_context, ensure_ascii=False, indent=2)
        context_block = f"""
The user has a tabular data file in context (schema / stats below). Use it to answer questions about columns,
data shape, and reasonable analysis approaches. If schema is missing or sparse, say what you can infer and what
would require running an analysis task.

Data context (JSON):
{ctx_json}
""".strip()
    else:
        context_block = """
No file schema is loaded yet. You may answer general questions. For questions that need the actual columns or
row statistics, briefly ask the user to attach CSV/Excel (paperclip) and optionally use /task to run a structured plan.
""".strip()

    prefix = _skill_context_block(skill_instructions)
    return f"""{prefix}You are a helpful data-analysis assistant in a workbench app.

Rules:
- Reply in the same language as the user's latest message when possible (Chinese or English).
- Be concise (a few short paragraphs or bullets unless the user asks for depth).
- Do not output raw JSON analysis plans unless the user explicitly asks for a plan skeleton; normal chat should be plain text / markdown.
- If the user wants to run a structured analysis, mention they can type `/task` followed by their question.

{context_block}

Recent conversation:
{history_block}

User message:
{message}
""".strip()


def build_revise_plan_prompt(
    current_plan: dict,
    instruction: str,
    schema_profile: dict,
    *,
    skill_instructions: str | None = None,
) -> str:
    """Ask the model to return a full revised AnalysisPlan JSON."""
    plan_json = json.dumps(current_plan, ensure_ascii=False, indent=2)
    schema_json = json.dumps(schema_profile, ensure_ascii=False, indent=2)
    prefix = _skill_context_block(skill_instructions)
    return f"""{prefix}You are an analysis planning assistant. The user asked to REVISE an existing analysis plan based on their feedback.

CRITICAL output rules:
- Respond with ONE JSON object only (the full revised plan).
- No markdown, no code fences, no explanation before or after the JSON.
- Use only column names that appear in the schema profile below.
- Preserve the same JSON shape as the current plan (goal, metrics, dimensions, filters, output, ambiguities, confidence).
- Apply the user's instruction faithfully; adjust metrics, dimensions, filters, chart type, or goal text as needed.
- "aggregation" must be one of: sum, mean, count, max, min, median.
- "operator" must be one of: eq, neq, gt, gte, lt, lte, in, not_in, contains.
- "role" must be one of: time, category, geo.
- "chart_type" must be one of: line, bar, histogram.
- Update "ambiguities" and "confidence" to reflect any remaining uncertainty after the revision.

Current plan:
{plan_json}

Schema profile:
{schema_json}

User revision instruction:
{instruction}

Output: one JSON object matching the AnalysisPlan shape.
""".strip()


def build_followups_prompt(
    goal: str,
    result_summary: dict,
    *,
    skill_instructions: str | None = None,
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    prefix = _skill_context_block(skill_instructions)
    return f"""{prefix}You are a data analysis assistant.

Generate exactly 3 short follow-up questions in Chinese.

Output rules:
- Return ONE JSON array of 3 strings only.
- No markdown, no code fences, no other text.
Example: ["是否需要按月份继续下钻？", "是否要对比其他区域？", "是否需要导出明细？"]

Goal:
{goal}

Result summary:
{result_json}
""".strip()
