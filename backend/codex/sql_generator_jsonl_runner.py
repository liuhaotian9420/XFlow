"""Run `codex exec --json` for sql-generator eval cases (shared by CLI + Streamlit + E2E)."""

from __future__ import annotations

import json
import subprocess
import tempfile
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from backend.codex.jsonl_encoding_fix import repair_jsonl_text
from backend.codex.xinfei_sso import resolve_codex_executable

Mode = Literal["raw", "hint"]


@dataclass(frozen=True)
class SqlGeneratorJsonStreamResult:
    """Outcome of a single `codex exec --json` run for one case + mode."""

    argv: list[str]
    case_id: str
    mode: Mode
    jsonl_text: str
    last_message: str
    stderr: str
    elapsed_s: float
    returncode: int
    jsonl_path: Path | None
    last_message_path: Path | None


def load_cases_dicts(cases_path: Path) -> list[dict[str, Any]]:
    return json.loads(cases_path.read_text(encoding="utf-8"))


def load_case(cases_path: Path, case_id: str) -> dict[str, Any]:
    for c in load_cases_dicts(cases_path):
        if c.get("id") == case_id:
            return c
    raise KeyError(f"Unknown case id: {case_id}")


def build_prompt(*, business_request: str, mode: Mode) -> str:
    hint = "Skill hint: $sql-generator\n\n" if mode == "hint" else ""
    return (
        "You are a senior data analyst writing ODPS SQL.\n"
        + hint
        + "CRITICAL OUTPUT RULES:\n"
        + "- Output ONLY the SQL script.\n"
        + "- No markdown, no code fences, no explanations.\n"
        + "- Use ODPS-compatible SQL style.\n"
        + "- Use placeholders like ${bizdate} when date partition is required.\n"
        + "- If you need MAX_PT(...) per local convention, include it.\n\n"
        + "Business request (written by a stakeholder):\n"
        + business_request.strip()
        + "\n"
    )


def _run_codex_sql_generator_prompt(
    *,
    repo_root: Path,
    case_id: str,
    mode: Mode,
    prompt: str,
    timeout_s: int,
    out_dir: Path | None,
    fix_shell_utf8: bool,
    sandbox_mode: str | None,
    approval_policy: str | None,
    bypass_sandbox: bool,
) -> SqlGeneratorJsonStreamResult:
    codex = resolve_codex_executable()

    jsonl_path: Path | None = None
    last_msg_path: Path | None = None
    out_dir_resolved: Path | None = None
    if out_dir is not None:
        out_dir_resolved = out_dir.resolve()
        out_dir_resolved.mkdir(parents=True, exist_ok=True)
        jsonl_path = out_dir_resolved / f"codex_exec__{case_id}__{mode}.jsonl"
        last_msg_path = out_dir_resolved / f"codex_last_message__{case_id}__{mode}.txt"

    tmp_last: Path | None = None
    if last_msg_path is None:
        with tempfile.NamedTemporaryFile(
            mode="w+b", delete=False, prefix="codex-last-", suffix=".txt"
        ) as tmp:
            tmp_last = Path(tmp.name)
    out_for_codex_path = last_msg_path if last_msg_path is not None else tmp_last
    assert out_for_codex_path is not None

    try:
        out_for_codex = str(out_for_codex_path)
        argv: list[str] = [codex]
        if bypass_sandbox:
            # Codex CLI forbids combining bypass flag with explicit approval policy.
            argv.append("--dangerously-bypass-approvals-and-sandbox")
        else:
            if sandbox_mode:
                argv.extend(["-s", sandbox_mode])
            if approval_policy:
                argv.extend(["-a", approval_policy])
        argv.extend(
            [
                "exec",
                "--json",
                "-o",
                out_for_codex,
                "-",
            ]
        )
        t0 = time.perf_counter()
        try:
            completed = subprocess.run(
                argv,
                input=prompt.encode("utf-8"),
                capture_output=True,
                timeout=int(timeout_s),
            )
        except subprocess.TimeoutExpired as exc:
            elapsed = time.perf_counter() - t0
            stderr = f"[argv] {json.dumps(argv, ensure_ascii=False)}\n"
            stderr += f"[timeout] timed out after {timeout_s}s\n"
            stderr += f"[exception] {exc}\n"
            if out_dir_resolved:
                stderr_path = out_dir_resolved / f"codex_stderr__{case_id}__{mode}.txt"
                try:
                    stderr_path.write_text(stderr, encoding="utf-8", newline="\n")
                except OSError:
                    pass
            return SqlGeneratorJsonStreamResult(
                argv=argv,
                case_id=case_id,
                mode=mode,
                jsonl_text="",
                last_message="",
                stderr=stderr,
                elapsed_s=elapsed,
                returncode=124,
                jsonl_path=jsonl_path,
                last_message_path=last_msg_path,
            )
        elapsed = time.perf_counter() - t0

        jsonl_raw = (completed.stdout or b"").decode("utf-8", errors="replace")
        jsonl_text = (
            repair_jsonl_text(jsonl_raw, repo_root=repo_root.resolve())
            if fix_shell_utf8
            else jsonl_raw
        )

        if jsonl_path is not None:
            jsonl_path.write_text(jsonl_text, encoding="utf-8", newline="\n")

        last_msg_file = out_for_codex_path
        last_message = ""
        try:
            last_message = last_msg_file.read_text(encoding="utf-8", errors="replace").strip()
        except OSError:
            pass

        stderr = (completed.stderr or b"").decode("utf-8", errors="replace")
        stderr = (
            f"[argv] {json.dumps(argv, ensure_ascii=False)}\n"
            + stderr
            + f"\n\n[exit_code]={completed.returncode} elapsed_s={elapsed:.3f}\n"
        )

        if json_dir := out_dir_resolved:
            stderr_path = json_dir / f"codex_stderr__{case_id}__{mode}.txt"
            try:
                stderr_path.write_text(stderr, encoding="utf-8", newline="\n")
            except OSError:
                pass

        rc = int(completed.returncode if completed.returncode is not None else 0)
        return SqlGeneratorJsonStreamResult(
            argv=argv,
            case_id=case_id,
            mode=mode,
            jsonl_text=jsonl_text,
            last_message=last_message,
            stderr=stderr,
            elapsed_s=elapsed,
            returncode=rc,
            jsonl_path=jsonl_path,
            last_message_path=last_msg_path,
        )
    finally:
        if tmp_last is not None:
            tmp_last.unlink(missing_ok=True)


def run_codex_json_stream_raw_prompt(
    *,
    repo_root: Path,
    run_id: str,
    prompt: str,
    mode: Mode = "raw",
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
) -> SqlGeneratorJsonStreamResult:
    """Run ``codex exec --json`` with a **fully custom** prompt (e.g. multi-skill serial instructions).

    Artifact names use ``run_id`` and ``mode`` (default ``raw``) like other runners.
    """
    if not (prompt or "").strip():
        raise ValueError("prompt is empty")
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=run_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
    )


def run_sql_generator_json_stream_inline(
    *,
    repo_root: Path,
    case_id: str,
    business_request: str,
    mode: Mode,
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
) -> SqlGeneratorJsonStreamResult:
    """Like :func:`run_sql_generator_json_stream` but takes NL directly (no cases JSON lookup)."""
    if not business_request.strip():
        raise ValueError("business_request is empty")
    prompt = build_prompt(business_request=business_request, mode=mode)
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=case_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
    )


def run_sql_generator_json_stream(
    *,
    repo_root: Path,
    case_id: str,
    mode: Mode,
    cases_relative: str = "tests/sql_generator_eval_cases.json",
    timeout_s: int = 300,
    out_dir: Path | None = None,
    fix_shell_utf8: bool = True,
    sandbox_mode: str | None = None,
    approval_policy: str | None = None,
    bypass_sandbox: bool = False,
) -> SqlGeneratorJsonStreamResult:
    """Spawn `codex exec --json`, return stdout JSONL (optionally repaired) and paths if ``out_dir`` set."""
    cases_path = repo_root / cases_relative
    case = load_case(cases_path, case_id)
    br = case.get("business_request")
    if not isinstance(br, str) or not br.strip():
        raise ValueError(f"Case {case_id!r} has no business_request")
    prompt = build_prompt(business_request=br, mode=mode)
    return _run_codex_sql_generator_prompt(
        repo_root=repo_root,
        case_id=case_id,
        mode=mode,
        prompt=prompt,
        timeout_s=timeout_s,
        out_dir=out_dir,
        fix_shell_utf8=fix_shell_utf8,
        sandbox_mode=sandbox_mode,
        approval_policy=approval_policy,
        bypass_sandbox=bypass_sandbox,
    )
