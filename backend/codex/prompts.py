"""Prompt templates for Codex CLI requests."""

from __future__ import annotations

import json


def build_plan_prompt(question: str, schema_profile: dict) -> str:
    schema_json = json.dumps(schema_profile, ensure_ascii=False, indent=2)
    return f"""
You are an analysis planning assistant.
Return only valid JSON. Do not include markdown.

Question:
{question}

Schema profile:
{schema_json}

Output schema:
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


def build_summary_prompt(goal: str, result_summary: dict) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""
You are a data analysis explainer.
Return plain text summary in Chinese, 2-4 short sentences.

Goal:
{goal}

Result summary:
{result_json}
""".strip()


def build_followups_prompt(goal: str, result_summary: dict) -> str:
    result_json = json.dumps(result_summary, ensure_ascii=False, indent=2)
    return f"""
You are a data analysis assistant.
Generate exactly 3 short follow-up questions in Chinese.
Return JSON array only, e.g. ["问题1", "问题2", "问题3"].

Goal:
{goal}

Result summary:
{result_json}
""".strip()

