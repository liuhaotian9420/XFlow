---
name: plan-reviser
description: Trigger when user asks to revise an existing AnalysisPlan using feedback and the same schema profile.
---

## Watermark
- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `plan-reviser`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Do this before the final answer for the skill, and overwrite rather than append.

## Goal
Revise an existing AnalysisPlan and return the full updated JSON.

## Inputs expected
- Current plan JSON
- Revision instruction
- Schema profile JSON

## Output constraints
- Return exactly one JSON object, no markdown.
- Preserve AnalysisPlan shape: goal, metrics, dimensions, filters, output, ambiguities, confidence.
- Use only columns from schema profile.
- Allowed values:
  - aggregation: sum, mean, count, max, min, median
  - operator: eq, neq, gt, gte, lt, lte, in, not_in, contains
  - role: time, category, geo
  - chart_type: line, bar, histogram

## Failure handling
- If instruction is partially ambiguous, apply best-effort revision and record remaining ambiguity.

## Boundaries
- Do not return partial patches; always return full revised plan object.
