"""Legacy one-shot ``codex exec`` subprocess provider (no ACP session)."""

from __future__ import annotations

import asyncio
import json
import os
import shutil
import subprocess
import sys
from dataclasses import dataclass

from pydantic import ValidationError

from backend.acp.errors import CodexAdapterError
from backend.acp.json_util import extract_json_array_payload, extract_json_payload
from backend.acp.xinfei_sso import resolve_codex_executable
from backend.skills import (
    SKILL_ANALYSIS_PLANNER,
    SKILL_DATA_CHAT,
    SKILL_PLAN_REVISER,
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


def _format_exception_for_logs(exc: BaseException, *, max_chain: int = 5) -> str:
    """Stable, non-empty detail for nested errors (some builtins stringify to '')."""
    parts: list[str] = []
    cur: BaseException | None = exc
    for _ in range(max_chain):
        if cur is None:
            break
        name = type(cur).__name__
        text = str(cur).strip()
        if not text:
            if isinstance(cur, ValidationError):
                try:
                    text = cur.json()
                except Exception:
                    text = repr(cur)
            else:
                text = repr(cur)
        parts.append(f"{name}: {text}")
        cur = cur.__cause__ or cur.__context__
    return " | ".join(parts) if parts else repr(exc)


def _codex_exec_config_args() -> list[str]:
    """Extra ``codex exec`` ``-c`` overrides (see OpenAI Codex config reference)."""
    parts: list[str] = []
    raw = os.getenv("CODEX_HTTP_TRANSPORT_ONLY", "true").strip().lower()
    if raw not in ("0", "false", "no", "off"):
        alias = os.getenv("CODEX_SSE_PROVIDER_ID", "openai_sse").strip() or "openai_sse"
        display_name = (
            os.getenv("CODEX_MODEL_PROVIDER_NAME", "OpenAI (HTTP/SSE)").strip()
            or "OpenAI (HTTP/SSE)"
        )
        name_toml = json.dumps(display_name, ensure_ascii=False)
        parts.extend(
            [
                "-c",
                f"model_providers.{alias}.name={name_toml}",
                "-c",
                f"model_providers.{alias}.requires_openai_auth=true",
                "-c",
                f"model_providers.{alias}.wire_api=responses",
                "-c",
                f"model_providers.{alias}.supports_websockets=false",
                "-c",
                f"model_provider={alias}",
            ]
        )

    extra = os.getenv("CODEX_EXTRA_CONFIG", "").strip()
    if extra:
        for segment in extra.split(";"):
            segment = segment.strip()
            if segment:
                parts.extend(["-c", segment])
    return parts


def _stdio_to_codex_result(stdout: bytes, stderr: bytes, returncode: int) -> str:
    out_text = stdout.decode("utf-8", errors="ignore").strip()
    err_text = stderr.decode("utf-8", errors="ignore").strip()
    if returncode != 0:
        raise CodexAdapterError(f"Codex command failed (code={returncode}): {err_text}")
    if not out_text:
        raise CodexAdapterError("Codex returned empty stdout.")
    return out_text


def _run_codex_subprocess_sync(argv: list[str], prompt: str, timeout_seconds: int) -> str:
    """Blocking Codex invoke with stdin; safe on Windows (used via ``asyncio.to_thread``)."""
    try:
        completed = subprocess.run(
            argv,
            input=prompt.encode("utf-8"),
            capture_output=True,
            timeout=timeout_seconds,
        )
    except subprocess.TimeoutExpired as exc:
        raise CodexAdapterError(
            f"Codex command timed out after {timeout_seconds}s"
        ) from exc
    return _stdio_to_codex_result(
        completed.stdout or b"",
        completed.stderr or b"",
        int(completed.returncode if completed.returncode is not None else 0),
    )


def _build_codex_argv(command: str, *subargs: str) -> list[str]:
    """Build argv for invoking Codex (Windows ``.cmd`` shim aware)."""
    resolved = shutil.which(command.strip()) or command
    tail = list(subargs)
    if sys.platform == "win32":
        low = resolved.lower()
        if low.endswith((".cmd", ".bat")):
            return ["cmd.exe", "/c", resolved, *tail]
    return [resolved, *tail]


@dataclass
class LegacyCodexProvider:
    """Run ``codex exec`` as a one-shot subprocess per prompt."""

    command: str = "codex"
    timeout_seconds: int = 60
    retry_count: int = 1

    async def generate_plan(
        self, question: str, schema_profile: dict, task_id: str = "unknown"
    ) -> AnalysisPlan:
        si = skill_instructions_for_prompt(SKILL_ANALYSIS_PLANNER, inject=True)
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
                raw = await self._run_prompt(prompt)
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
                    },
                )
                log_event(task_id, "plan", "codex_call", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "codex_call",
                    {
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- codex stdout (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to generate plan:\n{detail}") from last_error

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
            payload = extract_json_array_payload(raw)
            followups = [str(item) for item in payload][:3]
        except CodexAdapterError:
            followups = []
        save_snapshot(
            task_id,
            "codex_followups_call",
            {"prompt": prompt, "raw_output": raw, "parsed_result": followups},
        )
        return followups

    async def chat(
        self,
        message: str,
        history: list[dict],
        file_context: dict | None,
        task_id: str = "chat",
    ) -> str:
        si = skill_instructions_for_prompt(SKILL_DATA_CHAT, inject=True)
        prompt = build_chat_prompt(
            message=message,
            history=history,
            file_context=file_context,
            skill_instructions=si,
        )
        raw = await self._run_prompt(prompt)
        save_snapshot(
            task_id,
            "codex_chat_call",
            {"prompt": prompt, "raw_output": raw, "parse_success": True},
        )
        log_event(task_id, "chat", "codex_call", {"parse_success": True})
        return raw.strip()

    async def revise_plan(
        self,
        current_plan: AnalysisPlan,
        instruction: str,
        schema_profile: dict,
        task_id: str = "unknown",
    ) -> AnalysisPlan:
        si = skill_instructions_for_prompt(SKILL_PLAN_REVISER, inject=True)
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
                raw = await self._run_prompt(prompt)
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
                    },
                )
                log_event(task_id, "plan", "codex_revise", {"parse_success": True})
                return plan
            except Exception as exc:  # pragma: no cover - runtime path
                last_error = exc
                log_event(
                    task_id,
                    "plan",
                    "codex_revise",
                    {
                        "parse_success": False,
                        "error": _format_exception_for_logs(exc),
                    },
                )
        assert last_error is not None
        detail = _format_exception_for_logs(last_error)
        if last_stdout is not None:
            detail = (
                f"{detail}\n\n--- codex stdout (first 2000 chars) ---\n"
                f"{last_stdout[:2000]}"
            )
        raise CodexAdapterError(f"Failed to revise plan:\n{detail}") from last_error

    async def _run_prompt_async_subprocess(self, argv: list[str], prompt: str) -> str:
        process = await asyncio.create_subprocess_exec(
            *argv,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(input=prompt.encode("utf-8")),
                timeout=self.timeout_seconds,
            )
        except asyncio.TimeoutError as exc:
            process.kill()
            await process.wait()
            raise CodexAdapterError(
                f"Codex command timed out after {self.timeout_seconds}s"
            ) from exc
        return _stdio_to_codex_result(
            stdout or b"",
            stderr or b"",
            int(process.returncode if process.returncode is not None else 0),
        )

    async def _run_prompt(self, prompt: str) -> str:
        argv = _build_codex_argv(
            self.command, "exec", *_codex_exec_config_args(), "-"
        )
        force_async = os.getenv("CODEX_ASYNC_SUBPROCESS", "").strip().lower() in (
            "1",
            "true",
            "yes",
        )
        if sys.platform == "win32" and not force_async:
            return await asyncio.to_thread(
                _run_codex_subprocess_sync, argv, prompt, self.timeout_seconds
            )
        try:
            return await self._run_prompt_async_subprocess(argv, prompt)
        except NotImplementedError:
            return await asyncio.to_thread(
                _run_codex_subprocess_sync, argv, prompt, self.timeout_seconds
            )


_LEGACY_SINGLETON: LegacyCodexProvider | None = None


def get_legacy_codex_provider() -> LegacyCodexProvider:
    """Process-wide singleton for scripts that expect a stable ``get_adapter()`` instance."""
    global _LEGACY_SINGLETON
    if _LEGACY_SINGLETON is None:
        command = resolve_codex_executable()
        timeout_seconds = int(os.getenv("CODEX_TIMEOUT_SECONDS", "60"))
        retry_count = int(os.getenv("CODEX_RETRY_COUNT", "1"))
        _LEGACY_SINGLETON = LegacyCodexProvider(
            command=command,
            timeout_seconds=timeout_seconds,
            retry_count=retry_count,
        )
    return _LEGACY_SINGLETON
