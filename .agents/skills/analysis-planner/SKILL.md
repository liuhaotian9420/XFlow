---
name: analysis-planner
description: Trigger when user asks to create a structured analysis plan from a question plus schema profile.
---

## Watermark
- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `analysis-planner`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Do this before the final answer for the skill, and overwrite rather than append.

## Goal
Return a complete AnalysisPlan JSON for tabular analysis tasks.

## Inputs expected
- User question (intent)
- Schema profile JSON (columns, row_count, dtypes)

## Output constraints
- Return exactly one JSON object, no markdown.
- Use only columns that exist in schema profile.
- Keep JSON shape: goal, metrics, dimensions, filters, output, ambiguities, confidence.
- Allowed values:
  - aggregation: sum, mean, count, max, min, median
  - operator: eq, neq, gt, gte, lt, lte, in, not_in, contains
  - role: time, category, geo
  - chart_type: line, bar, histogram

## Failure handling
- If intent is ambiguous, still return best-effort plan and record ambiguity in `ambiguities`.
- Keep `confidence` aligned with uncertainty.

## Boundaries
- Do not return prose around JSON.
- Do not invent columns that are absent from schema.
