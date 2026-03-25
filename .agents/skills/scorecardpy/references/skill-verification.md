# Skill verification

## Automated checks

From the repository root:

```bash
python tests/verify_scorecardpy_skill.py
```

This asserts:

- `.agents/skills/scorecardpy/SKILL.md` exists with `name` and `description` in the frontmatter
- All files listed in the skill directory contract under `references/` and `scripts/` are present

## Smoke test (optional)

Loads `scorecardpy.germancredit()` into a temporary DuckDB table (binary `target` from `creditability`), then runs `scripts/run_scorecardpy.py` and `scripts/export_breaks.py`.

Requires packages not pinned in the main app: `duckdb`, `scorecardpy`, `scikit-learn` (plus `numpy` / `pandas`). Current `scorecardpy` still imports `pkg_resources`; use `setuptools<81` (for example `uv pip install "setuptools>=70,<81"`) if import fails on a newer setuptools.

```bash
python tests/verify_scorecardpy_skill.py --smoke
```

## Pointing Cursor at this skill

Use the folder `.agents/skills/scorecardpy/` (the directory that contains `SKILL.md`) as the skill root when configuring or testing skills in Cursor.
