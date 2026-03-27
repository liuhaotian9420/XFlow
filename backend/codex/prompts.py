"""Prompt templates for Codex CLI requests."""

from __future__ import annotations

import json


def build_plan_prompt(
    question: str,
    schema_profile: dict,
    *,
    skill_hint: str = "$analysis-planner",
) -> str:
    schema_json = json.dumps(schema_profile, ensure_ascii=False, indent=2)
    return f"""You are an analysis planning assistant for tabular data.
Skill hint: {skill_hint}

CRITICAL output rules:
- Respond with ONE JSON object only.
- No markdown, no code fences, no explanation before or after the JSON.
- Use only column names that appear in the schema profile below.
- Output MUST follow the skill-native AnalysisPlan contract (goal/scope/grain/methods/validation/etc.).
- "aggregation" must be one of: sum, mean, count, max, min, median.
- "operator" must be one of: eq, neq, gt, gte, lt, lte, in, not_in, contains.
- "analysis_type" must be one of: descriptive, diagnostic, trend, comparison, distribution, segmentation, ranking.
- "method.type" must be one of: aggregate, timeseries, top_n, distribution, group_compare, period_compare.
- "null_policy" must be one of: include, exclude, separate_bucket (or null).
- "role" must be one of: time, category, geo (or null when uncertain).
- "output.chart_type" may be: line, bar, histogram, table.
- "completion_state" must be one of: needs_clarification, minimally_completed, reviewed.
- Set "confidence" between 0.0 and 1.0 and record real uncertainty in "ambiguities".
- "metrics" must contain at least one item.
- "methods" must contain at least one item.
- "output.table_fields" must contain at least one item.

Question:
{question}

Schema profile:
{schema_json}

Output JSON must match this shape (field names and types):
{{
  "goal": {{
    "question": "string",
    "decision_context": "string|null",
    "success_criteria": "string|null"
  }},
  "scope": {{
    "entity": "string|null",
    "population": "string",
    "assumptions": ["string"]
  }},
  "analysis_type": "descriptive|diagnostic|trend|comparison|distribution|segmentation|ranking",
  "grain": {{
    "primary_key": ["string"],
    "answer_unit": "string",
    "aggregation_level": "string|null"
  }},
  "metrics": [
    {{
      "name": "string",
      "column": "string",
      "aggregation": "sum|mean|count|max|min|median",
      "definition": "string|null",
      "format": "string|null",
      "constraints": ["string"]
    }}
  ],
  "dimensions": [
    {{
      "column": "string",
      "role": "time|category|geo|null",
      "label": "string|null",
      "reason": "string|null"
    }}
  ],
  "filters": [
    {{
      "column": "string",
      "operator": "eq|neq|gt|gte|lt|lte|in|not_in|contains",
      "value": "any",
      "required": "boolean|null"
    }}
  ],
  "segments": [
    {{
      "name": "string|null",
      "column": "string|null",
      "definition": "string|null"
    }}
  ],
  "time": {{
    "time_column": "string|null",
    "grain": "string|null",
    "window": "string|null",
    "comparison_window": "string|null"
  }},
  "derived_fields": [
    {{
      "name": "string",
      "expression_logic": "string",
      "source_columns": ["string"]
    }}
  ],
  "comparisons": [
    {{
      "type": "string",
      "left": "string|null",
      "right": "string|null",
      "metric_names": ["string"],
      "expected_signal": "string|null"
    }}
  ],
  "methods": [
    {{
      "name": "string",
      "type": "aggregate|timeseries|top_n|distribution|group_compare|period_compare",
      "inputs": ["string"],
      "description": "string",
      "null_policy": "include|exclude|separate_bucket|null"
    }}
  ],
  "validation": {{
    "data_quality_checks": ["string"],
    "metric_sanity_checks": ["string"],
    "coverage_checks": ["string"]
  }},
  "output": {{
    "table_fields": ["string"],
    "chart_type": "line|bar|histogram|table|null",
    "title": "string|null",
    "sort": "string|null",
    "limit": "integer|null",
    "narrative_focus": "string|null"
  }},
  "ambiguities": [
    {{
      "field": "string|null",
      "issue": "string",
      "severity": "string|null",
      "blocks_minimal_completion": "boolean|null"
    }}
  ],
  "confidence": 0.0,
  "completion_state": "needs_clarification|minimally_completed|reviewed"
}}
""".strip()


def build_summary_prompt(
    goal: str,
    result_summary: dict,
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""You are a data analysis explainer.
Return plain text summary in Chinese, 2-4 short sentences.

If the result mentions artifacts, describe them briefly at a high level only.
Do not generate machine-readable result JSON, base64 payloads, binary content, or raw HTML bodies.

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
    skill_hint: str = "$data-chat",
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

    return f"""You are a helpful data-analysis assistant in a workbench app.
Skill hint: {skill_hint}

Rules:
- Reply in the user’s latest language when possible (Chinese or English).
- Keep responses concise unless the user asks for depth.
- Use plain text or markdown in normal chat. Do not output raw JSON plans unless explicitly requested.
- For structured analysis, mention that the user can type `/task` followed by their question.
- The final output must always satisfy the chat output schema and include both `reply` and `result`.
- `result` is only for structured render metadata of existing outputs, not for source code or prose.
- Only include artifacts that already exist as concrete generated local files/results.
- Each entry in `result.artifacts` must contain exactly: `name`, `mime`, `path`.
- `path` must be a controlled repo-relative artifact path, or `null` if no local file exists. Never use absolute paths or invented paths.
- Use stable MIME types only, such as: `text/html`, `image/png`, `image/jpeg`, `image/gif`, `image/webp`, `text/plain`, `text/csv`, `application/json`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `application/vnd.ms-excel`, `application/octet-stream`.
- If generating a renderable artifact, save it to a controlled local artifact path before referencing it.
- Prefer referencing saved local files over inlining content.
- Never include `data_base64`, raw binary data, or full HTML bodies in chat content or structured metadata.
- Keep machine-readable fields strictly structured and free of explanatory prose.

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
    skill_hint: str = "$plan-reviser",
) -> str:
    """Ask the model to return a full revised AnalysisPlan JSON."""
    plan_json = json.dumps(current_plan, ensure_ascii=False, indent=2)
    schema_json = json.dumps(schema_profile, ensure_ascii=False, indent=2)
    return f"""You are an analysis planning assistant. The user asked to REVISE an existing analysis plan based on their feedback.
Skill hint: {skill_hint}

CRITICAL output rules:
- Respond with ONE JSON object only (the full revised plan).
- No markdown, no code fences, no explanation before or after the JSON.
- Use only column names that appear in the schema profile below.
- Preserve the same skill-native JSON shape as the current plan.
- Apply the user's instruction faithfully; adjust metrics, dimensions, filters, chart type, or goal text as needed.
- "aggregation" must be one of: sum, mean, count, max, min, median.
- "operator" must be one of: eq, neq, gt, gte, lt, lte, in, not_in, contains.
- "role" must be one of: time, category, geo (or null when uncertain).
- "output.chart_type" may be: line, bar, histogram, table, or null.
- "completion_state" must be one of: needs_clarification, minimally_completed, reviewed.
- Update "ambiguities", "confidence", and "completion_state" to reflect any remaining uncertainty after the revision.
- "metrics" must contain at least one item.
- "methods" must contain at least one item.
- "output.table_fields" must contain at least one item.

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
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""You are a data analysis assistant.

Generate exactly 3 short follow-up questions in Chinese.

Output rules:
- Return ONE JSON array of 3 strings only.
- No markdown, no code fences, no other text.
- Keep the questions user-facing and concise.
- Do not include raw JSON objects, base64 payloads, or HTML in the questions.
Example: ["接下来要按时间趋势继续看吗？", "要不要按渠道或区域做对比？", "要不要下钻查看明细样本？"]

Goal:
{goal}

Result summary:
{result_json}
""".strip()
