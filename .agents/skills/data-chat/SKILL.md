---
name: data-chat
description: Use when the user wants practical guidance for data analysis in plain chat, optionally using attached table schema and/or summary statistics.
---

## Watermark
- Every time this skill is used, overwrite `water.json` in this skill directory.
- Use `../_common/scripts/write_watermark.py` to write the file.
- Required JSON shape:
  - `skill`: `data-chat`
  - `version`: watermark version, default `v1`
  - `input_files`: input file names/paths used for this run, or `[]`
  - `actions`: concise completed actions for this run
- Do this before the final answer for the skill, and overwrite rather than append.

# Data Chat

## Goal
Provide concise, practical data-analysis guidance in normal chat.

## Inputs expected
- Latest user message
- Recent conversation turns
- Optional file context (schema/statistics)

## Output constraints
- Reply in the user's language when possible.
- Keep response concise unless user requests depth.
- Use plain text/markdown; do not output raw analysis-plan JSON unless user explicitly asks.
- If user wants executable analysis, suggest using `/task`.

## Failure handling
- If file context is missing or sparse, state what is known and what needs upload/analysis.

## Boundaries
- Do not fabricate specific column stats when context is absent.
