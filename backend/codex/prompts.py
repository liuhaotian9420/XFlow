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
- "aggregation" must be one of: sum, mean, count, max, min, median.
- "operator" must be one of: eq, neq, gt, gte, lt, lte, in, not_in, contains.
- "role" must be one of: time, category, geo.
- "chart_type" must be one of: line, bar, histogram.
- Set "confidence" between 0.0 and 1.0. List real uncertainties in "ambiguities".

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
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""You are a data analysis explainer.
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
) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""You are a data analysis assistant.

Generate exactly 3 short follow-up questions in Chinese.

Output rules:
- Return ONE JSON array of 3 strings only.
- No markdown, no code fences, no other text.
Example: ["鏄惁闇€瑕佹寜鏈堜唤缁х画涓嬮捇锛?, "鏄惁瑕佸姣斿叾浠栧尯鍩燂紵", "鏄惁闇€瑕佸鍑烘槑缁嗭紵"]

Goal:
{goal}

Result summary:
{result_json}
""".strip()
