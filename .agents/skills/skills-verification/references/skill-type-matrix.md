# Skill Type Matrix

This file indexes the skill-profile guidance already described in `SKILL.md`.

| Skill profile | Typical signals | Validate |
| --- | --- | --- |
| Documentation-only skill | Instructional content and no executable path | structure, completeness, file references, example correctness |
| File-processing skill | Consumes or produces `csv`, `parquet`, `json`, `xlsx`, `sql`, or `duckdb` files | minimal fixture generation, file ingestion, output creation, schema assumptions |
| Model / analytics skill | Trains, scores, transforms, bins, or analyzes data | minimal synthetic dataset, required columns, target/feature assumptions, output object or artifact structure |
| External-system skill | Depends on ODPS, APIs, services, cloud databases, or credentials | mock/stub/dry-run readiness, graceful failure when credentials are missing, minimal offline behavior if supported |
| Hybrid skill | Spans multiple categories | each applicable layer conservatively |

## Example validation heuristics

### For a SQL export skill
Verify:
- SQL input exists or can be mocked
- DuckDB fixture can be created
- query execution produces rows
- empty result path is handled intentionally
- invalid table name is rejected clearly
- declared export artifact is actually created

### For a scorecardpy skill
Verify:
- binary target exists
- sample dataset has valid class diversity
- required package imports
- a minimal binning / iv / woe path runs
- bad target or missing columns fail clearly

### For a pure documentation skill
Verify:
- frontmatter valid
- references and scripts paths valid
- examples are coherent
- no false implication of runtime capability
