"""Adapt skill-produced files into the existing ``ResultPayload`` shape."""

from __future__ import annotations

import base64
import csv
import json
from pathlib import Path
from typing import Any

from backend.schemas.plan import ChartType
from backend.schemas.result import ArtifactPayload, ChartPayload, ResultPayload, TablePayload

_MAX_ARTIFACT_BYTES = 1_000_000
_TEXT_EXTS = {".json", ".csv", ".txt", ".sql", ".md"}
_BINARY_EXT_MIME = {
    ".png": "image/png",
    ".jpg": "image/jpeg",
    ".jpeg": "image/jpeg",
    ".gif": "image/gif",
    ".webp": "image/webp",
    ".xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    ".xls": "application/vnd.ms-excel",
    ".pkl": "application/octet-stream",
    ".duckdb": "application/octet-stream",
}
_PRIORITY_FILES = (
    "metrics.json",
    "run_summary.json",
    "selected_variables.json",
    "breaks_export.json",
    "scored_test.csv",
)


def _normalize_dir(path: str, *, repo_root: Path) -> Path:
    p = Path(path)
    if not p.is_absolute():
        p = (repo_root / p).resolve()
    return p


def _find_candidate_files(root: Path) -> list[Path]:
    if not root.exists() or not root.is_dir():
        return []
    files: list[Path] = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        lower = p.name.lower()
        ext = p.suffix.lower()
        if lower in _PRIORITY_FILES or ext in _TEXT_EXTS or ext in _BINARY_EXT_MIME:
            files.append(p)
    files.sort(key=lambda p: (p.name.lower() not in _PRIORITY_FILES, str(p).lower()))
    return files


def _safe_load_json(path: Path) -> Any | None:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return None


def _extract_numeric_map(obj: Any, *, prefix: str = "") -> dict[str, float]:
    out: dict[str, float] = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            key = f"{prefix}.{k}" if prefix else str(k)
            out.update(_extract_numeric_map(v, prefix=key))
        return out
    if isinstance(obj, (int, float)) and not isinstance(obj, bool):
        out[prefix or "value"] = float(obj)
    return out


def _build_metrics_table_and_chart(metrics_json: dict[str, Any]) -> tuple[TablePayload, ChartPayload] | None:
    if not isinstance(metrics_json, dict):
        return None
    train_map = _extract_numeric_map(metrics_json.get("train", {}))
    test_map = _extract_numeric_map(metrics_json.get("test", {}))
    keys = sorted(set(train_map.keys()) | set(test_map.keys()))
    if not keys:
        return None
    rows: list[dict[str, Any]] = []
    for key in keys:
        rows.append(
            {
                "metric": key,
                "train": train_map.get(key),
                "test": test_map.get(key),
            }
        )
    chart_rows = [
        {"metric": r["metric"], "test": r["test"]}
        for r in rows
        if isinstance(r.get("test"), (int, float))
    ]
    chart = ChartPayload(
        chart_type=ChartType.BAR,
        x="metric",
        y="test",
        data=chart_rows if chart_rows else rows,
    )
    table = TablePayload(columns=["metric", "train", "test"], rows=rows)
    return table, chart


def _build_run_summary_table(run_summary_json: dict[str, Any]) -> TablePayload | None:
    if not isinstance(run_summary_json, dict):
        return None
    rows: list[dict[str, Any]] = []
    for k, v in run_summary_json.items():
        if isinstance(v, (str, int, float, bool)) or v is None:
            rows.append({"key": k, "value": v})
    if not rows:
        return None
    return TablePayload(columns=["key", "value"], rows=rows)


def _make_artifact(path: Path, *, root: Path) -> ArtifactPayload | None:
    rel_name = str(path.relative_to(root)).replace("\\", "/")
    ext = path.suffix.lower()
    size = path.stat().st_size
    if size > _MAX_ARTIFACT_BYTES:
        return None
    if ext == ".html":
        try:
            html = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None
        return ArtifactPayload(name=rel_name, mime="text/html", html=html)

    mime = "application/octet-stream"
    if ext in _BINARY_EXT_MIME:
        mime = _BINARY_EXT_MIME[ext]
    elif ext == ".json":
        mime = "application/json"
    elif ext == ".csv":
        mime = "text/csv"
    elif ext == ".txt":
        mime = "text/plain"
    elif ext == ".sql":
        mime = "text/plain"
    elif ext == ".md":
        mime = "text/markdown"
    try:
        raw = path.read_bytes()
    except OSError:
        return None
    return ArtifactPayload(
        name=rel_name,
        mime=mime,
        data_base64=base64.b64encode(raw).decode("ascii"),
    )


def enrich_result_with_skill_outputs(
    result: ResultPayload,
    *,
    repo_root: Path,
    artifact_dirs: list[str],
) -> ResultPayload:
    files_seen: set[Path] = set()
    metrics_table_chart: tuple[TablePayload, ChartPayload] | None = None
    fallback_table: TablePayload | None = None
    attached_count = 0
    for raw_dir in artifact_dirs:
        if not (raw_dir or "").strip():
            continue
        root = _normalize_dir(raw_dir, repo_root=repo_root)
        for f in _find_candidate_files(root):
            if f in files_seen:
                continue
            files_seen.add(f)
            if f.name == "metrics.json" and metrics_table_chart is None:
                parsed = _safe_load_json(f)
                if isinstance(parsed, dict):
                    metrics_table_chart = _build_metrics_table_and_chart(parsed)
            if f.name == "run_summary.json" and fallback_table is None:
                parsed = _safe_load_json(f)
                if isinstance(parsed, dict):
                    fallback_table = _build_run_summary_table(parsed)
            artifact = _make_artifact(f, root=root)
            if artifact is not None:
                result.artifacts.append(artifact)
                attached_count += 1

    if metrics_table_chart is not None:
        result.table, result.chart = metrics_table_chart
    elif fallback_table is not None:
        result.table = fallback_table
        if fallback_table.rows:
            chart_rows = [
                {"key": r["key"], "value": r["value"]}
                for r in fallback_table.rows
                if isinstance(r.get("value"), (int, float))
            ]
            if chart_rows:
                result.chart = ChartPayload(
                    chart_type=ChartType.BAR,
                    x="key",
                    y="value",
                    data=chart_rows,
                )

    if attached_count > 0:
        suffix = f" Attached {attached_count} skill artifact(s)."
        if suffix not in result.execution_summary:
            result.execution_summary = f"{result.execution_summary}{suffix}"
    return result


def csv_preview_rows(path: Path, *, limit: int = 50) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    try:
        with path.open("r", encoding="utf-8", errors="replace", newline="") as fp:
            reader = csv.DictReader(fp)
            for idx, row in enumerate(reader):
                if idx >= limit:
                    break
                rows.append(dict(row))
    except OSError:
        return []
    return rows
