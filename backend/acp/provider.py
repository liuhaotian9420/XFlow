"""Analysis provider that drives prompts through an ACP session manager."""

from __future__ import annotations

import os
from dataclasses import dataclass

from backend.acp.client import AcpSessionManager
from backend.acp.errors import CodexAdapterError
from backend.acp.json_util import extract_json_array_payload, extract_json_payload
from backend.acp.legacy_codex import _format_exception_for_logs
from backend.skills import (
    SKILL_ANALYSIS_PLANNER,
    SKILL_DATA_CHAT,
    SKILL_PLAN_REVISER,
    acp_agent_uses_native_skills,
    skill_instructions_for_prompt,
)
from backend.codex.prompts import (
    build_chat_prompt,
    build_followups_prompt,
    build_plan_prompt,
    build_revise_plan_prompt,
    build_summary_prompt,
)
from backend.observability import log_event, save_snapshot
from backend.schemas.plan import AnalysisPlan


@dataclass
class AcpProvider:
    """Map analysis steps to ACP ``session/prompt`` turns (one ACP session per ``task_id``)."""

    _mgr: AcpSessionManager
    retry_count: int = 1

    @property
    def command(self) -> str:
        """Agent executable (for logging / diagnostics)."""
        return self._mgr._agent_command  # noqa: SLF001

    @property
    def acp_spawn_argv(self) -> tuple[str, ...]:
        """Full ACP subprocess argv (codex-acp / npx …) for diagnostics."""
        return self._mgr.spawn_argv

    @property
    def timeout_seconds(self) -> int:
        return self._mgr._timeout  # noqa: SLF001

    @timeout_seconds.setter
    def timeout_seconds(self, value: int) -> None:
        self._mgr._timeout = int(value)  # noqa: SLF001

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "unknown"
    ) -> AnalysisPlan:
        inject_skills = not acp_agent_uses_native_skills()
        si = skill_instructions_for_prompt(
            SKILL_ANALYSIS_PLANNER, inject=inject_skills
        )
        prompt = build_plan_prompt(
            question=question,
            schema_profile=schema_profile,
            skill_instructions=si,
        )
        last_error: Exception | None = None
        last_stdout: str | None = None
        for _ in range(self.retry_count + 1):
            raw: str | None = None
            try:
                raw = await self._mgr.prompt_for(task_id, prompt)
                last_stdout = raw
                payload = extract_json_payload(raw)
                plan = AnalysisPlan.model_validate(payload)
                save_snapshot(
                    task_id,
                    "codex_plan_call",
                    {
                        "prompt": prompt,
                        "raw_output": raw,
                        "parsed_result": payload,
                        "parse_success": True,
                        "transport": "acp",
                    },
                )
                log_event(task_id, "plan", "acp_call", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "acp_call",
                    {
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- agent text (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to generate plan:\n{detail}") from last_error

    async def generate_summary(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> str:
        prompt = build_summary_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._mgr.prompt_for(task_id, prompt)
        save_snapshot(
            task_id,
            "codex_summary_call",
            {"prompt": prompt, "raw_output": raw, "parse_success": True, "transport": "acp"},
        )
        log_event(task_id, "summary", "acp_call", {"parse_success": True})
        return raw.strip()

    async def generate_followups(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> list[str]:
        prompt = build_followups_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._mgr.prompt_for(task_id, prompt)
        try:
            payload = extract_json_array_payload(raw)
            followups = [str(item) for item in payload][:3]
        except CodexAdapterError:
            followups = []
        save_snapshot(
            task_id,
            "codex_followups_call",
            {"prompt": prompt, "raw_output": raw, "parsed_result": followups, "transport": "acp"},
        )
        return followups

    async def chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        task_id: str = "chat",
    ) -> str:
        inject_skills = not acp_agent_uses_native_skills()
        si = skill_instructions_for_prompt(SKILL_DATA_CHAT, inject=inject_skills)
        prompt = build_chat_prompt(
            message=message,
            history=history,
            file_context=file_context,
            skill_instructions=si,
        )
        logical = os.getenv("ACP_CHAT_SESSION_KEY", "xyf-global-chat")
        raw = await self._mgr.prompt_for(logical, prompt)
        save_snapshot(
            task_id,
            "codex_chat_call",
            {"prompt": prompt, "raw_output": raw, "parse_success": True, "transport": "acp"},
        )
        log_event(task_id, "chat", "acp_call", {"parse_success": True})
        return raw.strip()

    async def revise_plan(
        self,
        current_plan: AnalysisPlan,
        instruction: str,
        schema_profile: dict,
        task_id: str = "unknown",
    ) -> AnalysisPlan:
        inject_skills = not acp_agent_uses_native_skills()
        si = skill_instructions_for_prompt(SKILL_PLAN_REVISER, inject=inject_skills)
        prompt = build_revise_plan_prompt(
            current_plan=current_plan.model_dump(),
            instruction=instruction,
            schema_profile=schema_profile,
            skill_instructions=si,
        )
        last_error: Exception | None = None
        last_stdout: str | None = None
        for _ in range(self.retry_count + 1):
            raw: str | None = None
            try:
                raw = await self._mgr.prompt_for(task_id, prompt)
                last_stdout = raw
                payload = extract_json_payload(raw)
                plan = AnalysisPlan.model_validate(payload)
                save_snapshot(
                    task_id,
                    "codex_revise_call",
                    {
                        "prompt": prompt,
                        "raw_output": raw,
                        "parsed_result": payload,
                        "parse_success": True,
                        "transport": "acp",
                    },
                )
                log_event(task_id, "plan", "acp_revise", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "acp_revise",
                    {
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- agent text (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to revise plan:\n{detail}") from last_error
