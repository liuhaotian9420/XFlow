"""Prompt + JSONL heuristics for serial use of sql-generator then dataworks (sql-export-agent)."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

# Frontmatter ``name`` values from ``.agents/skills/*/SKILL.md`` (Codex ``$...`` skill hints).
SKILL_SQL_GENERATOR = "sql-generator"
SKILL_SQL_EXPORT_AGENT = "sql-export-agent"  # dataworks / SQL Export Agent

_SLASH = re.compile(r"[\\/]+")


def build_serial_two_skill_prompt(*, business_request: str) -> str:
    """Instruction to apply **$sql-generator** then **$sql-export-agent** in order within one Codex turn.

    The model is asked to finish SQL generation (and persist a `.sql` path) before describing
    the dataworks export command. This matches the product intent: chain skills serially, not in parallel.
    """
    br = business_request.strip()
    return (
        "You are a data engineer working inside this git repository.\n\n"
        "Two Codex skills apply **in strict serial order** — complete all of **Step 1** before starting **Step 2**.\n\n"
        f"Skill hint: ${SKILL_SQL_GENERATOR}\n"
        "**STEP 1** — From the business request at the bottom, produce exactly **one** ODPS/MaxCompute-ready SQL script. "
        "Save it as a **single** `.sql` file under `artifacts/two_skill_chain/` (create that folder if needed). "
        "Use a descriptive filename. Do not run ODPS in this step unless the sandbox explicitly allows it.\n\n"
        f"Skill hint: ${SKILL_SQL_EXPORT_AGENT}\n"
        "**STEP 2** — Using the SQL Export / dataworks workflow, take the `.sql` file from Step 1 as `file_path`. "
        "Output the **exact** command line to run from the **repository root**, for example:\n"
        "`python .agents/skills/dataworks/scripts/run_sql_export.py <file_path> --save_path artifacts/two_skill_chain/excel`\n"
        "If execution is blocked, still print the command and the resolved paths.\n\n"
        "**Final reply** — Briefly state: (1) path to the `.sql` file, (2) the full `run_sql_export.py` command for Step 2.\n"
        "You may use short bullet points; no long prose.\n\n"
        "---\n"
        "Business request:\n"
        f"{br}\n"
    )


@dataclass(frozen=True)
class TwoSkillSerialEvidence:
    """Heuristic signals parsed from ``codex exec --json`` JSONL (not a proof of correctness)."""

    event_lines: int
    mentions_sql_generator_hint: bool
    mentions_sql_export_or_dataworks: bool
    command_touches_sql_generator_tree: bool
    command_touches_dataworks_run_sql_export: bool
    step1_before_step2_order_ok: bool

    @property
    def looks_like_serial_two_skill(self) -> bool:
        """Rough pass: both skill areas appear and dataworks appears after sql-generator in the stream."""
        both = self.mentions_sql_generator_hint and self.mentions_sql_export_or_dataworks
        return both and self.step1_before_step2_order_ok


def _norm_pathish(text: str) -> str:
    return _SLASH.sub("/", text.lower())


def analyze_two_skill_serial_jsonl(jsonl_text: str) -> TwoSkillSerialEvidence:
    """Scan JSONL events for references to sql-generator vs sql-export-agent / dataworks."""
    mentions_sg = False
    mentions_dw = False
    cmd_sg = False
    cmd_dw = False
    idx_sg: list[int] = []
    idx_dw: list[int] = []
    n = 0
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
        chunks: list[str] = []
        itype = item.get("type")
        if itype in ("agent_message", "reasoning"):
            chunks.append(str(item.get("text") or ""))
        elif itype == "command_execution":
            cmd = str(item.get("command") or "")
            chunks.append(cmd)
            nc = _norm_pathish(cmd)
            if "skills/sql-generator" in nc or "sql-generator" in nc:
                cmd_sg = True
                idx_sg.append(n)
            if "run_sql_export" in nc or "skills/dataworks" in nc:
                cmd_dw = True
                idx_dw.append(n)
        blob = "\n".join(chunks)
        lb = blob.lower()
        if "$sql-generator" in lb or "sql-generator" in lb or "skills/sql-generator" in _norm_pathish(blob):
            mentions_sg = True
            idx_sg.append(n)
        if (
            "$sql-export-agent" in lb
            or "sql-export-agent" in lb
            or "run_sql_export" in lb
            or "skills/dataworks" in _norm_pathish(blob)
        ):
            mentions_dw = True
            idx_dw.append(n)

    first_sg = min(idx_sg) if idx_sg else None
    first_dw = min(idx_dw) if idx_dw else None
    order_ok = True
    if first_sg is not None and first_dw is not None:
        order_ok = first_sg <= first_dw

    return TwoSkillSerialEvidence(
        event_lines=n,
        mentions_sql_generator_hint=mentions_sg,
        mentions_sql_export_or_dataworks=mentions_dw,
        command_touches_sql_generator_tree=cmd_sg,
        command_touches_dataworks_run_sql_export=cmd_dw,
        step1_before_step2_order_ok=order_ok,
    )
