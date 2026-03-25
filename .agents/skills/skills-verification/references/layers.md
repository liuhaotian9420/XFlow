# Verification Layers

This file indexes the layer-oriented guidance already described in `SKILL.md`.

## Verification model

Always validate in **layers**, from cheapest to most behaviorally meaningful.

### Layer 1 - Structural validation
Check the target skill for:

- valid YAML frontmatter
- required frontmatter keys:
  - `name`
  - `description`
- presence of `SKILL.md`
- valid directory shape
- section completeness
- all indexed files under `references/` and `scripts/` actually exist
- all example paths and local file references are resolvable

This layer should be fast and non-destructive.

### Layer 2 - Smoke validation
Run the target skill's minimal execution path, if one exists.

Typical checks:
- a help command works
- an example script starts successfully
- dependencies import correctly
- a smallest happy path completes without immediate crash

If the environment is missing dependencies, try the most local and reproducible runner available, for example:

```bash
python ...
uv run python ...
```

Do not silently skip smoke checks without reporting why.

### Layer 3 - Contract validation
Test whether the skill actually does what it claims.

Examples:
- if a skill claims to support CSV input, feed it a minimal CSV
- if it claims to export Excel, verify an Excel file is produced
- if it claims to write DuckDB tables, verify the table exists afterward
- if it claims to reject invalid inputs, verify that the rejection is clear and intentional

This is the most important layer.

### Layer 4 - Negative-path validation
Test at least one invalid input path when feasible.

Examples:
- missing required columns
- empty query or empty dataset
- invalid file type
- malformed config
- impossible table name
- absent environment variable

A good skill should fail **clearly**, not just crash.

## Core principle

A skill is **not** considered fully verified merely because:
- its markdown is valid
- its example command starts
- its script does not crash immediately

A skill is only meaningfully verified when the verifier can establish a minimal executable contract between:

- declared inputs
- expected behavior
- produced outputs
- understandable failure modes

If that contract cannot be tested because the skill is too vague, report the skill as **insufficiently testable**.
