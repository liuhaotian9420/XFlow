"""One-shot Codex prompt + JSONL analysis: sql-generator → sql-export-agent → scorecardpy."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from backend.codex.two_skill_chain import _norm_pathish

SKILL_SQL_GENERATOR = "sql-generator"
SKILL_SQL_EXPORT_AGENT = "sql-export-agent"
# From ``.agents/skills/scorecardpy/SKILL.md`` frontmatter ``name``.
SKILL_SCORECARDBY = "scorecardpy-duckdb-large-scale-scorecard"


@dataclass(frozen=True)
class FullIntegrationLayout:
    """Stable paths (relative to repo root) for one-go orchestration + post-verify."""

    sql_workdir_rel: str
    excel_dir_rel: str
    duckdb_path_rel: str
    duckdb_table: str
    score_out_rel: str

    @staticmethod
    def default_layout() -> "FullIntegrationLayout":
        return FullIntegrationLayout(
            sql_workdir_rel="artifacts/full_integration_onego",
            excel_dir_rel="artifacts/full_integration_onego/excel",
            duckdb_path_rel=".agents/assets/full_integration_onego.duckdb",
            duckdb_table="full_integration_odps_result",
            score_out_rel="artifacts/full_integration_onego/scorecardpy",
        )

    def resolve(self, repo_root: Path) -> dict[str, Path]:
        r = repo_root.resolve()
        return {
            "sql_workdir": r / self.sql_workdir_rel,
            "excel_dir": r / self.excel_dir_rel,
            "duckdb": r / self.duckdb_path_rel,
            "score_out": r / self.score_out_rel,
        }


def build_full_integration_onego_prompt(
    *,
    business_request: str,
    layout: FullIntegrationLayout | None = None,
) -> str:
    """Single Codex turn: three skills in **strict serial order** (handoff to real scripts)."""
    lay = layout or FullIntegrationLayout.default_layout()
    br = business_request.strip()
    # Use one f-string + `{br}` at the end only — never ``str.format`` on user text (e.g. ``${bizdate}`` would break).
    return f"""You are a lead data engineer inside this **git repository**. \
Three Codex skills apply in **strict serial order**: finish **Step 1** completely, then **Step 2**, then **Step 3**. \
Execute shell/Python when the sandbox allows; otherwise print exact commands and paths.

Skill hint: ${SKILL_SQL_GENERATOR}
**STEP 1 — SQL**
- Produce **one** ODPS/MaxCompute `.sql` file that satisfies the business request at the bottom.
- Save it under `{lay.sql_workdir_rel}/` (create directories as needed). Use a descriptive filename ending in `.sql`.
- The result set must be usable by scorecardpy after export: include **`entity_id`** (stable row key) and \
a **binary `target`** column (0/1). Map/rename from source columns in SQL; if no natural label, \
construct a defensible `target` with `CASE …` and state the rule briefly in comments in the SQL file.

Skill hint: ${SKILL_SQL_EXPORT_AGENT}
**STEP 2 — Export (dataworks)**
- Run from **repository root** (or output the exact command if execution is blocked):
```
python .agents/skills/dataworks/scripts/run_sql_export.py "<path_to_step1_sql>" \
--save_path "{lay.excel_dir_rel}" \
--duckdb-path "{lay.duckdb_path_rel}" \
--duckdb-table "{lay.duckdb_table}" \
--lifecycle 30
```
- Use these paths literally unless a path is impossible in the sandbox — then use the closest under the same folders:
  - `--save_path` → `{lay.excel_dir_rel}`
  - `--duckdb-path` → `{lay.duckdb_path_rel}`
  - `--duckdb-table` → `{lay.duckdb_table}`
- After a successful run, confirm the Excel path and that DuckDB contains the table.

Skill hint: ${SKILL_SCORECARDBY}
**STEP 3 — Scorecard (scorecardpy)**
- From **repository root**, run (or print if blocked):
```
python .agents/skills/scorecardpy/scripts/run_scorecardpy.py \
--db-path "{lay.duckdb_path_rel}" \
--table "{lay.duckdb_table}" \
--target target --id-col entity_id \
--out-dir "{lay.score_out_rel}" \
--save-plots --plots-max 30
```
Then run:
```
python .agents/skills/scorecardpy/scripts/export_breaks.py \
--bins-pkl "{lay.score_out_rel}/bins.pkl" \
--out-dir "{lay.score_out_rel}"
```
(Adjust `--target` / `--id-col` only if your SQL used different column names — then make them consistent.)

**Final reply (concise)**
1) Path to the `.sql` file  2) Whether ODPS export + DuckDB write succeeded  \
3) Whether scorecardpy + export_breaks succeeded  4) Paths to `bins.pkl` / `breaks_export.json` if present.

---
Business request:
{br}
"""


@dataclass(frozen=True)
class FullIntegrationEvidence:
    event_lines: int
    mentions_sql_generator: bool
    mentions_dataworks: bool
    mentions_scorecardpy: bool
    cmd_sql_generator_tree: bool
    cmd_dataworks_export: bool
    cmd_scorecardpy: bool
    order_sg_dw_sc_ok: bool

    @property
    def looks_like_full_chain(self) -> bool:
        return (
            self.mentions_sql_generator
            and self.mentions_dataworks
            and self.mentions_scorecardpy
            and self.order_sg_dw_sc_ok
        )


def analyze_full_integration_onego_jsonl(jsonl_text: str) -> FullIntegrationEvidence:
    """Heuristic: all three skills appear; order sql-generator → dataworks → scorecardpy by first line index."""
    mentions_sg = mentions_dw = mentions_sc = False
    cmd_sg = cmd_dw = cmd_sc = False
    idx_sg: list[int] = []
    idx_dw: list[int] = []
    idx_sc: list[int] = []
    n = 0

    def _touch_sg(blob: str, line_no: int) -> None:
        nonlocal mentions_sg, cmd_sg
        lb = blob.lower()
        np = _norm_pathish(blob)
        if "$sql-generator" in lb or "skills/sql-generator" in np:
            mentions_sg = True
            idx_sg.append(line_no)

    def _touch_dw(blob: str, line_no: int) -> None:
        nonlocal mentions_dw, cmd_dw
        lb = blob.lower()
        np = _norm_pathish(blob)
        if (
            "$sql-export-agent" in lb
            or "run_sql_export" in lb
            or "skills/dataworks" in np
        ):
            mentions_dw = True
            idx_dw.append(line_no)

    def _touch_sc(blob: str, line_no: int) -> None:
        nonlocal mentions_sc, cmd_sc
        lb = blob.lower()
        np = _norm_pathish(blob)
        if (
            "$scorecardpy" in lb
            or "scorecardpy-duckdb" in lb
            or "run_scorecardpy" in lb
            or "skills/scorecardpy" in np
            or "export_breaks" in lb
        ):
            mentions_sc = True
            idx_sc.append(line_no)

    for line in jsonl_text.splitlines():
        if not line.strip():
            continue
        try:
            o = json.loads(line)
        except json.JSONDecodeError:
            continue
        n += 1
        item = o.get("item")
        if not isinstance(item, dict):
            continue
        itype = item.get("type")
        parts: list[str] = []
        if itype in ("agent_message", "reasoning"):
            parts.append(str(item.get("text") or ""))
        elif itype == "command_execution":
            c = str(item.get("command") or "")
            parts.append(c)
            nc = _norm_pathish(c)
            if "skills/sql-generator" in nc or "sql-generator" in nc:
                cmd_sg = True
                idx_sg.append(n)
            if "run_sql_export" in nc or "skills/dataworks" in nc:
                cmd_dw = True
                idx_dw.append(n)
            if "run_scorecardpy" in nc or "skills/scorecardpy" in nc or "export_breaks" in nc:
                cmd_sc = True
                idx_sc.append(n)
        blob = "\n".join(parts)
        _touch_sg(blob, n)
        _touch_dw(blob, n)
        _touch_sc(blob, n)

    fsg = min(idx_sg) if idx_sg else None
    fdw = min(idx_dw) if idx_dw else None
    fsc = min(idx_sc) if idx_sc else None
    order_ok = True
    if fsg is not None and fdw is not None and fsg > fdw:
        order_ok = False
    if fdw is not None and fsc is not None and fdw > fsc:
        order_ok = False
    if fsg is not None and fsc is not None and fsg > fsc:
        order_ok = False

    return FullIntegrationEvidence(
        event_lines=n,
        mentions_sql_generator=mentions_sg,
        mentions_dataworks=mentions_dw,
        mentions_scorecardpy=mentions_sc,
        cmd_sql_generator_tree=cmd_sg,
        cmd_dataworks_export=cmd_dw,
        cmd_scorecardpy=cmd_sc,
        order_sg_dw_sc_ok=order_ok,
    )
