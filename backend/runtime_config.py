"""Central runtime mode and dependency checks."""

from __future__ import annotations

import os
import shutil
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv

from backend.codex.xinfei_sso import (
    check_enterprise_sso,
    is_xinfei_enterprise_binary,
    resolve_codex_executable,
)

APP_MODE_MOCK = "mock"
APP_MODE_REAL = "real"
REPO_ROOT = Path(__file__).resolve().parents[1]

# Centralize .env loading here so preflight, backend routes, and UI status use the same source.
load_dotenv(REPO_ROOT / ".env", override=False)

ODPS_ENV_KEYS = {
    "access_id": ("ODPS_ACCESS_KEY_ID", "ALIBABA_CLOUD_ACCESS_KEY_ID"),
    "access_key": ("ODPS_ACCESS_KEY_SECRET", "ALIBABA_CLOUD_ACCESS_KEY_SECRET"),
    "project": ("ODPS_PROJECT", "ALIBABA_CLOUD_PROJECT_JINGYING"),
    "endpoint": ("ODPS_ENDPOINT", "ALIBABA_CLOUD_REGION_ENDPOINT"),
}


@dataclass(frozen=True)
class ReadinessIssue:
    code: str
    message: str


def get_app_mode() -> str:
    raw = os.getenv("APP_MODE", "").strip().lower()
    if raw in (APP_MODE_MOCK, APP_MODE_REAL):
        return raw
    if os.getenv("CODEX_MOCK", "true").strip().lower() == "true":
        return APP_MODE_MOCK
    return APP_MODE_REAL


def default_use_mock() -> bool:
    return get_app_mode() != APP_MODE_REAL


def resolve_odps_env() -> dict[str, str | None]:
    resolved: dict[str, str | None] = {}
    for key, aliases in ODPS_ENV_KEYS.items():
        value = None
        for env_name in aliases:
            current = os.getenv(env_name, "").strip()
            if current:
                value = current
                break
        resolved[key] = value
    return resolved


def _codex_issues() -> list[ReadinessIssue]:
    issues: list[ReadinessIssue] = []
    command = resolve_codex_executable()
    resolved = shutil.which(command) if command else None
    if not command or (command == "codex" and not resolved):
        issues.append(
            ReadinessIssue(
                "codex_not_resolved",
                "Codex CLI is not configured or not on PATH; set CODEX_CLI_COMMAND or CODEX_BINARY.",
            )
        )
        return issues
    if is_xinfei_enterprise_binary(command) and not check_enterprise_sso(command):
        issues.append(
            ReadinessIssue(
                "codex_login_missing",
                "Xinfei Codex is not logged in with enterprise SSO.",
            )
        )
    return issues


def _odps_issues() -> list[ReadinessIssue]:
    issues: list[ReadinessIssue] = []
    resolved = resolve_odps_env()
    missing = [name for name, value in resolved.items() if not value]
    if missing:
        issues.append(
            ReadinessIssue(
                "odps_env_missing",
                "Missing ODPS settings: " + ", ".join(sorted(missing)),
            )
        )
    return issues


def get_runtime_status() -> dict[str, object]:
    mode = get_app_mode()
    codex_command = resolve_codex_executable()
    codex_issues = _codex_issues()
    odps_issues = _odps_issues()
    odps_env = resolve_odps_env()
    return {
        "app_mode": mode,
        "default_use_mock": default_use_mock(),
        "codex": {
            "command": codex_command,
            "is_xinfei": is_xinfei_enterprise_binary(codex_command),
            "ready": not codex_issues,
            "issues": [issue.__dict__ for issue in codex_issues],
        },
        "odps": {
            "ready": not odps_issues,
            "project": odps_env["project"],
            "endpoint": odps_env["endpoint"],
            "issues": [issue.__dict__ for issue in odps_issues],
        },
    }


def require_runtime_ready(*, needs_codex: bool = False, needs_odps: bool = False) -> None:
    issues: list[str] = []
    if needs_codex:
        issues.extend(issue.message for issue in _codex_issues())
    if needs_odps:
        issues.extend(issue.message for issue in _odps_issues())
    if issues:
        raise RuntimeError("Runtime is not ready: " + " | ".join(issues))
