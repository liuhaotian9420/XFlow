"""Codex CLI adapter implementation."""

from __future__ import annotations

import asyncio
import json
import os
from dataclasses import dataclass

from backend.observability import log_event, save_snapshot
from backend.codex.prompts import (
    build_followups_prompt,
    build_plan_prompt,
    build_summary_prompt,
)
from backend.schemas.plan import AnalysisPlan


class CodexAdapterError(RuntimeError):
    """Raised when Codex CLI interaction fails."""


@dataclass
class CodexAdapter:
    """Run Codex CLI as subprocess and parse structured outputs."""

    command: str = "codex"
    timeout_seconds: int = 60
    retry_count: int = 1

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "unknown"
    ) -> AnalysisPlan:
        prompt = build_plan_prompt(question=question, schema_profile=schema_profile)
        last_error: Exception | None = None
        for _ in range(self.retry_count + 1):
            try:
                raw = await self._run_prompt(prompt)
                payload = _extract_json_payload(raw)
                plan = AnalysisPlan.model_validate(payload)
                save_snapshot(
                    task_id,
                    "codex_plan_call",
                    {
                        "prompt": prompt,
                        "raw_output": raw,
                        "parsed_result": payload,
                        "parse_success": True,
                    },
                )
                log_event(task_id, "plan", "codex_call", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(task_id, "plan", "codex_call", {"parse_success": False, "error": str(exc)})
        raise CodexAdapterError(f"Failed to generate plan: {last_error}") from last_error

    async def generate_summary(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> str:
        prompt = build_summary_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._run_prompt(prompt)
        save_snapshot(
            task_id,
            "codex_summary_call",
            {"prompt": prompt, "raw_output": raw, "parse_success": True},
        )
        log_event(task_id, "summary", "codex_call", {"parse_success": True})
        return raw.strip()

    async def generate_followups(
        self, goal: str, result_df_summary: dict, task_id: str = "unknown"
    ) -> list[str]:
        prompt = build_followups_prompt(goal=goal, result_summary=result_df_summary)
        raw = await self._run_prompt(prompt)
        try:
            payload = json.loads(raw)
            if isinstance(payload, list):
                followups = [str(item) for item in payload][:3]
            else:
                followups = []
        except json.JSONDecodeError:
            followups = []
        save_snapshot(
            task_id,
            "codex_followups_call",
            {"prompt": prompt, "raw_output": raw, "parsed_result": followups},
        )
        return followups

    async def _run_prompt(self, prompt: str) -> str:
        process = await asyncio.create_subprocess_exec(
            self.command,
            "exec",
            prompt,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(), timeout=self.timeout_seconds
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            await process.wait()
            raise CodexAdapterError(
                f"Codex command timed out after {self.timeout_seconds}s"
            ) from exc

        out_text = stdout.decode("utf-8", errors="ignore").strip()
        err_text = stderr.decode("utf-8", errors="ignore").strip()
        if process.returncode != 0:
            raise CodexAdapterError(
                f"Codex command failed (code={process.returncode}): {err_text}"
            )
        if not out_text:
            raise CodexAdapterError("Codex returned empty stdout.")
        return out_text


def get_adapter() -> CodexAdapter:
    command = os.getenv("CODEX_CLI_COMMAND", "codex")
    timeout_seconds = int(os.getenv("CODEX_TIMEOUT_SECONDS", "60"))
    retry_count = int(os.getenv("CODEX_RETRY_COUNT", "1"))
    return CodexAdapter(
        command=command,
        timeout_seconds=timeout_seconds,
        retry_count=retry_count,
    )


def _extract_json_payload(raw: str) -> dict:
    raw = raw.strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        pass

    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1 or end <= start:
        raise CodexAdapterError("Cannot locate JSON object in Codex output.")
    candidate = raw[start : end + 1]
    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:
        raise CodexAdapterError(f"Invalid JSON extracted from Codex output: {exc}") from exc

