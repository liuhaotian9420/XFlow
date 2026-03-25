# Contract Testing

This file indexes the contract-oriented guidance already described in `SKILL.md`.

## Contract validation

Test whether the skill actually does what it claims.

Examples:
- if a skill claims to support CSV input, feed it a minimal CSV
- if it claims to export Excel, verify an Excel file is produced
- if it claims to write DuckDB tables, verify the table exists afterward
- if it claims to reject invalid inputs, verify that the rejection is clear and intentional

This is the most important layer.

## Negative-path validation

Test at least one invalid input path when feasible.

Examples:
- missing required columns
- empty query or empty dataset
- invalid file type
- malformed config
- impossible table name
- absent environment variable

A good skill should fail **clearly**, not just crash.

## Expected target-skill conventions

This verifier should reward skills that are explicit about their contracts.

A strong target `SKILL.md` should ideally state:

- accepted input types
- required columns / parameters / files
- expected outputs
- minimal runnable path
- failure conditions
- dependency boundaries
- whether mock / dry-run / local-only validation is supported

If these are absent, the verifier should still do best-effort inference, but report reduced confidence.

## Failure interpretation rules

Do not confuse these cases:

### Environment issue
Examples:
- missing Python package
- no `uv`
- no system executable

This is not always a skill defect, but it must still be reported.

### Skill defect
Examples:
- broken example command
- missing referenced file
- unsupported file type despite claiming support
- impossible-to-test contract because the skill is underspecified

### Integration-boundary issue
Examples:
- real credentials needed
- external service unavailable
- production-only runtime path

Report these separately and recommend mockable or dry-run design improvements.
