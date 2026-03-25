"""Repair mojibake inside Codex `codex exec --json` JSONL streams.

On Windows, PowerShell often emits command output using a legacy ANSI code page while
the source files are UTF-8. Codex embeds that output in ``aggregated_output`` fields,
which makes Chinese look like ``浠ｇ爜`` instead of ``代码``.

When the command is a plain ``Get-Content -Raw '<path>'`` (or double-quoted) call, we
can replace ``aggregated_output`` by reading the same path from disk as UTF-8.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

# Paths are usually passed with single quotes inside the -Command string.
_GET_CONTENT_RE = re.compile(
    r"Get-Content\s+-Raw\s+(?P<q>['\"])(?P<path>.+?)(?P=q)",
    re.IGNORECASE,
)


def _resolve_read_path(raw_path: str, *, repo_root: Path) -> Path | None:
    """Return an existing file path, or None if not found under repo_root."""
    p = raw_path.strip().strip("'\"")
    # JSON escapes and PowerShell sometimes use mixed slashes.
    p = p.replace("\\\\", "/").replace("\\", "/")
    candidate = (repo_root / p).resolve()
    try:
        candidate.relative_to(repo_root.resolve())
    except ValueError:
        return None
    return candidate if candidate.is_file() else None


def _maybe_refresh_aggregated_output(item: Any, *, repo_root: Path) -> Any:
    if not isinstance(item, dict):
        return item
    if item.get("type") != "command_execution":
        return item
    cmd = item.get("command")
    if not isinstance(cmd, str):
        return item
    m = _GET_CONTENT_RE.search(cmd)
    if not m:
        return item
    disk_path = _resolve_read_path(m.group("path"), repo_root=repo_root)
    if disk_path is None:
        return item
    try:
        text = disk_path.read_text(encoding="utf-8")
    except OSError:
        return item
    out = dict(item)
    out["aggregated_output"] = text
    return out


def repair_jsonl_event_line(line: str, *, repo_root: Path) -> str:
    """Parse one JSONL line, patch command_execution outputs, re-serialize."""
    raw = line.rstrip("\r\n")
    if not raw.strip():
        return ""
    try:
        evt = json.loads(raw)
    except json.JSONDecodeError:
        return raw + "\n"
    item = evt.get("item")
    if isinstance(item, dict):
        new_item = _maybe_refresh_aggregated_output(item, repo_root=repo_root)
        if new_item is not item:
            evt = dict(evt)
            evt["item"] = new_item
    return json.dumps(evt, ensure_ascii=False, separators=(",", ":")) + "\n"


def repair_jsonl_text(text: str, *, repo_root: Path) -> str:
    """Repair a full JSONL document (multiple lines)."""
    out_parts: list[str] = []
    for raw_line in text.splitlines():
        if not raw_line.strip():
            continue
        out_parts.append(repair_jsonl_event_line(raw_line, repo_root=repo_root))
    return "".join(out_parts)


def repair_jsonl_file(path: Path, *, repo_root: Path) -> None:
    """Rewrite a JSONL file in place with UTF-8 re-read fixes."""
    original = path.read_text(encoding="utf-8")
    fixed = repair_jsonl_text(original, repo_root=repo_root)
    path.write_text(fixed, encoding="utf-8", newline="\n")
