#!/usr/bin/env python3
"""
Synchronize known ODPS table metadata into a top-level index plus by-table docs.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any

try:
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover
    def load_dotenv(*args: Any, **kwargs: Any) -> bool:
        return False


DEFAULT_TABLES_MD = Path(".agents/skills/dataworks/references/tables.md")
SCRIPT_DIR = Path(__file__).resolve().parent


@dataclass
class ColumnMeta:
    name: str
    data_type: str
    comment: str = ""
    kind: str = "column"


@dataclass
class TableMetadata:
    table_name: str
    columns: list[ColumnMeta]
    ddl: str | None
    sample_rows: list[dict[str, Any]]
    source: str
    warnings: list[str]


@dataclass
class ExistingDetailParts:
    processed_lines: list[str]
    ground_truth_fields: set[str]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Fetch known table metadata and upsert it into top-level index + by-table docs."
    )
    parser.add_argument("--table-name", help="ODPS table name to inspect.")
    parser.add_argument(
        "--mock-metadata-json",
        help="Local JSON fixture for smoke tests. Skips live ODPS calls.",
    )
    parser.add_argument(
        "--tables-md",
        default=str(DEFAULT_TABLES_MD),
        help="Top-level index markdown path.",
    )
    parser.add_argument(
        "--sample-limit",
        type=int,
        default=5,
        help="How many head rows to capture. Must be between 1 and 10.",
    )
    parser.add_argument("--skip-ddl", action="store_true", help="Skip DDL retrieval.")
    parser.add_argument("--skip-head", action="store_true", help="Skip head row retrieval.")
    parser.add_argument("--print-only", action="store_true", help="Print the by-table markdown without writing.")
    parser.add_argument("--access-id", default=None, help="ODPS Access ID")
    parser.add_argument("--access-key", default=None, help="ODPS Access Key")
    parser.add_argument("--project", default=None, help="ODPS project")
    parser.add_argument("--endpoint", default=None, help="ODPS endpoint")
    return parser.parse_args()


def fail(stage: str, message: str) -> None:
    print(f"[ERROR] {stage}: {message}", file=sys.stderr)
    sys.exit(1)


def load_local_env() -> None:
    candidates = [SCRIPT_DIR / ".env", Path.cwd() / ".env"]
    seen: set[Path] = set()
    for path in candidates:
        resolved = path.resolve()
        if resolved in seen or not path.exists():
            continue
        seen.add(resolved)

        try:
            load_dotenv(dotenv_path=path, override=False)
        except TypeError:
            load_dotenv(override=False)

        for line in path.read_text(encoding="utf-8").splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#") or "=" not in stripped:
                continue
            key, value = stripped.split("=", 1)
            key = key.strip()
            value = value.strip().strip("'").strip('"')
            if key and key not in os.environ:
                os.environ[key] = value


def resolve_odps_config(args: argparse.Namespace) -> tuple[str, str, str, str]:
    access_id = (
        args.access_id
        or os.getenv("ODPS_ACCESS_KEY_ID")
        or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_ID")
    )
    access_key = (
        args.access_key
        or os.getenv("ODPS_ACCESS_KEY_SECRET")
        or os.getenv("ALIBABA_CLOUD_ACCESS_KEY_SECRET")
    )
    project = (
        args.project
        or os.getenv("ODPS_PROJECT")
        or os.getenv("ALIBABA_CLOUD_PROJECT_JINGYING")
    )
    endpoint = (
        args.endpoint
        or os.getenv("ODPS_ENDPOINT")
        or os.getenv("ALIBABA_CLOUD_REGION_ENDPOINT")
    )

    missing: list[str] = []
    if not access_id:
        missing.append("access-id / ODPS_ACCESS_KEY_ID")
    if not access_key:
        missing.append("access-key / ODPS_ACCESS_KEY_SECRET")
    if not project:
        missing.append("project / ODPS_PROJECT")
    if not endpoint:
        missing.append("endpoint / ODPS_ENDPOINT")
    if missing:
        fail("ODPS authentication/config failure", f"missing: {', '.join(missing)}")
    return access_id, access_key, project, endpoint


def validate_args(args: argparse.Namespace) -> None:
    if bool(args.table_name) == bool(args.mock_metadata_json):
        fail("table metadata input failure", "provide exactly one of --table-name or --mock-metadata-json")
    if not 1 <= args.sample_limit <= 10:
        fail("table metadata input failure", "--sample-limit must be between 1 and 10")


def load_mock_metadata(path: Path) -> TableMetadata:
    if not path.exists():
        fail("table metadata input failure", f"mock metadata file not found: {path}")

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        fail("table metadata input failure", f"invalid mock metadata json: {exc}")
        raise

    table_name = payload.get("table_name")
    columns = payload.get("columns")
    if not isinstance(table_name, str) or not table_name.strip():
        fail("table metadata input failure", "mock metadata missing table_name")
    if not isinstance(columns, list) or not columns:
        fail("table metadata input failure", "mock metadata missing columns")

    normalized_columns: list[ColumnMeta] = []
    for item in columns:
        if not isinstance(item, dict):
            fail("table metadata input failure", "column items must be objects")
        name = str(item.get("name", "")).strip()
        data_type = str(item.get("type", "")).strip()
        if not name or not data_type:
            fail("table metadata input failure", "each column needs name and type")
        normalized_columns.append(
            ColumnMeta(
                name=name,
                data_type=data_type,
                comment=str(item.get("comment", "") or ""),
                kind=str(item.get("kind", "column") or "column"),
            )
        )

    sample_rows = payload.get("sample_rows") or []
    if not isinstance(sample_rows, list):
        fail("table metadata input failure", "sample_rows must be a list")

    return TableMetadata(
        table_name=table_name.strip(),
        columns=normalized_columns,
        ddl=(payload.get("ddl") or None),
        sample_rows=[row for row in sample_rows if isinstance(row, dict)],
        source=f"mock:{path.name}",
        warnings=[],
    )


def fetch_live_metadata(args: argparse.Namespace) -> TableMetadata:
    try:
        from odps import ODPS
    except Exception as exc:
        fail("ODPS authentication/config failure", f"failed to import odps package: {exc}")

    access_id, access_key, project, endpoint = resolve_odps_config(args)

    try:
        odps = ODPS(
            access_id=access_id,
            secret_access_key=access_key,
            project=project,
            endpoint=endpoint,
        )
        table = odps.get_table(args.table_name)
    except Exception as exc:
        fail("table metadata fetch failure", str(exc))
        raise

    try:
        schema = table.table_schema
        columns: list[ColumnMeta] = []
        for column in list(getattr(schema, "columns", []) or []):
            columns.append(
                ColumnMeta(
                    name=str(column.name),
                    data_type=str(column.type),
                    comment=str(getattr(column, "comment", "") or ""),
                    kind="column",
                )
            )
        for partition in list(getattr(schema, "partitions", []) or []):
            columns.append(
                ColumnMeta(
                    name=str(partition.name),
                    data_type=str(partition.type),
                    comment=str(getattr(partition, "comment", "") or ""),
                    kind="partition",
                )
            )
    except Exception as exc:
        fail("table metadata fetch failure", f"failed to read table schema: {exc}")
        raise

    warnings: list[str] = []
    ddl: str | None = None
    if not args.skip_ddl:
        try:
            ddl = table.get_ddl(with_comments=True, if_not_exists=False)
        except Exception as exc:
            warnings.append(f"DDL unavailable: {exc}")

    sample_rows: list[dict[str, Any]] = []
    if not args.skip_head:
        try:
            records = table.head(args.sample_limit)
            column_order = [column.name for column in columns]
            for record in records:
                row = {
                    name: normalize_value(record[idx])
                    for idx, name in enumerate(column_order[: len(record)])
                }
                sample_rows.append(row)
        except Exception as exc:
            warnings.append(f"Sample rows unavailable: {exc}")

    return TableMetadata(
        table_name=args.table_name,
        columns=columns,
        ddl=ddl,
        sample_rows=sample_rows,
        source="odps",
        warnings=warnings,
    )


def normalize_value(value: Any) -> Any:
    if value is None:
        return ""
    if isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def escape_cell(value: Any) -> str:
    if value is None:
        return ""
    text = str(value).replace("\r", " ").replace("\n", " ")
    return text.replace("|", "\\|")


def slugify_table_name(table_name: str) -> str:
    return table_name.replace("/", "_")


def by_table_dir_for(index_path: Path) -> Path:
    return index_path.parent / "by_table"


def detail_path_for(index_path: Path, table_name: str) -> Path:
    return by_table_dir_for(index_path) / f"{slugify_table_name(table_name)}.md"


def by_table_index_path_for(index_path: Path) -> Path:
    return by_table_dir_for(index_path) / "index.md"


def extract_subsection_lines(section_text: str, heading: str, level: str = "##") -> list[str]:
    pattern = re.compile(rf"^{re.escape(level)}\s+{re.escape(heading)}\s*$", re.MULTILINE)
    match = pattern.search(section_text)
    if not match:
        return []
    start = match.end()
    next_match = re.compile(rf"^{re.escape(level)}\s+.+?$", re.MULTILINE).search(section_text, start)
    end = next_match.start() if next_match else len(section_text)
    body = section_text[start:end].strip()
    if not body:
        return []
    return [line.rstrip() for line in body.splitlines()]


def extract_ground_truth_field_names(raw_field_lines: list[str]) -> set[str]:
    names: set[str] = set()
    for line in raw_field_lines:
        stripped = line.strip()
        if stripped.startswith("- "):
            value = stripped[2:].strip()
            if value and value != "无":
                names.add(value)
    return names


def parse_legacy_file(content: str) -> tuple[dict[str, list[str]], dict[str, str]]:
    mapping: dict[str, list[str]] = {}
    details: dict[str, str] = {}

    map_match = re.search(r"(?ms)^##\s+SQL.*?(?=^##\s+(?!SQL)[^\r\n]+|\Z)", content)
    if map_match:
        map_text = map_match.group(0)
        table_matches = list(re.finditer(r"(?m)^###\s+([^\r\n]+)\s*$", map_text))
        for index, match in enumerate(table_matches):
            table = match.group(1).strip()
            end = table_matches[index + 1].start() if index + 1 < len(table_matches) else len(map_text)
            block = map_text[match.end() : end]
            files = [line[2:].strip() for line in block.splitlines() if line.strip().startswith("- ")]
            mapping[table] = files

    detail_matches = list(re.finditer(r"(?m)^##\s+((?!SQL)[^\r\n]+)\s*$", content))
    for index, match in enumerate(detail_matches):
        table = match.group(1).strip()
        end = detail_matches[index + 1].start() if index + 1 < len(detail_matches) else len(content)
        details[table] = content[match.start() : end].strip() + "\n"

    return mapping, details


def parse_index_mapping(content: str) -> dict[str, list[str]]:
    mapping, _ = parse_legacy_file(content)
    return mapping


def load_existing_detail_parts(index_path: Path, table_name: str) -> ExistingDetailParts:
    detail_path = detail_path_for(index_path, table_name)
    if detail_path.exists():
        detail_text = detail_path.read_text(encoding="utf-8")
        processed_lines = extract_subsection_lines(detail_text, "字段加工")
        structure_lines = extract_subsection_lines(detail_text, "表结构")
        ground_truth_fields: set[str] = set()
        for line in structure_lines:
            if re.match(r"^\|\s*[^|]+\|\s*[^|]+\|\s*[^|]+\|\s*[^|]+\|\s*Y\s*\|", line):
                parts = [part.strip() for part in line.strip("|").split("|")]
                if parts:
                    ground_truth_fields.add(parts[0])
        return ExistingDetailParts(processed_lines=processed_lines, ground_truth_fields=ground_truth_fields)

    if index_path.exists():
        index_text = index_path.read_text(encoding="utf-8")
        _, legacy_details = parse_legacy_file(index_text)
        legacy = legacy_details.get(table_name)
        if legacy:
            processed_lines = extract_subsection_lines(legacy, "字段加工", level="###")
            raw_lines = extract_subsection_lines(legacy, "原始字段", level="###")
            return ExistingDetailParts(
                processed_lines=processed_lines,
                ground_truth_fields=extract_ground_truth_field_names(raw_lines),
            )

    return ExistingDetailParts(processed_lines=[], ground_truth_fields=set())


def render_columns_table(columns: list[ColumnMeta], ground_truth_fields: set[str]) -> list[str]:
    lines = [
        "| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |",
        "| --- | --- | --- | --- | --- |",
    ]
    for column in columns:
        lines.append(
            f"| {escape_cell(column.name)} | {escape_cell(column.data_type)} | "
            f"{escape_cell(column.kind)} | {escape_cell(column.comment)} | "
            f"{'Y' if column.name in ground_truth_fields else ''} |"
        )
    return lines


def render_sample_table(columns: list[ColumnMeta], sample_rows: list[dict[str, Any]]) -> list[str]:
    column_names = [column.name for column in columns]
    if not sample_rows:
        return ["- 未采样"]

    header = "| " + " | ".join(escape_cell(name) for name in column_names) + " |"
    separator = "| " + " | ".join(["---"] * len(column_names)) + " |"
    lines = [header, separator]
    for row in sample_rows:
        lines.append("| " + " | ".join(escape_cell(row.get(name, "")) for name in column_names) + " |")
    return lines


def render_detail_markdown(
    metadata: TableMetadata,
    source_files: list[str],
    existing_parts: ExistingDetailParts,
) -> str:
    lines = [f"# {metadata.table_name}", ""]

    lines.append("## 来源文件")
    if source_files:
        for file_name in source_files:
            lines.append(f"- {file_name}")
    else:
        lines.append("- 未记录")
    lines.append("")

    if existing_parts.processed_lines:
        lines.append("## 字段加工")
        lines.extend(existing_parts.processed_lines)
        lines.append("")

    lines.append("## 表结构")
    lines.extend(render_columns_table(metadata.columns, existing_parts.ground_truth_fields))
    lines.append("")

    lines.append("### DDL")
    if metadata.ddl:
        lines.append("```sql")
        lines.append(metadata.ddl.rstrip())
        lines.append("```")
    else:
        lines.append("- 未获取")
    lines.append("")

    lines.append("## 抽样数据")
    lines.extend(render_sample_table(metadata.columns, metadata.sample_rows))
    lines.append("")

    lines.append("## 同步来源")
    lines.append(f"- `{metadata.source}`")
    lines.append("")

    if metadata.warnings:
        lines.append("## 同步备注")
        for warning in metadata.warnings:
            lines.append(f"- {warning}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def render_index_markdown(index_path: Path, table_to_files: dict[str, list[str]]) -> str:
    lines = ["# tables", ""]
    lines.append("## SQL代码索引（表 -> 文件）")
    lines.append("")
    for table in sorted(table_to_files.keys()):
        lines.append(f"### {table}")
        files = table_to_files[table]
        if files:
            for file_name in files:
                lines.append(f"- {file_name}")
        else:
            lines.append("- 未记录")
        lines.append("")

    lines.append("## By Table")
    lines.append("")
    lines.append("| 表名 | 详情 |")
    lines.append("| --- | --- |")
    for table in sorted(table_to_files.keys()):
        relative = f"./by_table/{slugify_table_name(table)}.md"
        lines.append(f"| {table} | [详情]({relative}) |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_by_table_index_markdown(table_to_files: dict[str, list[str]]) -> str:
    lines = ["# by_table", ""]
    lines.append("| 表名 | 来源文件数 | 详情 |")
    lines.append("| --- | --- | --- |")
    for table in sorted(table_to_files.keys()):
        relative = f"./{slugify_table_name(table)}.md"
        lines.append(f"| {table} | {len(table_to_files[table])} | [详情]({relative}) |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content.rstrip() + "\n", encoding="utf-8")


def main() -> None:
    load_local_env()
    args = parse_args()
    validate_args(args)

    index_path = Path(args.tables_md)
    by_table_dir = by_table_dir_for(index_path)
    if args.mock_metadata_json:
        metadata = load_mock_metadata(Path(args.mock_metadata_json))
    else:
        metadata = fetch_live_metadata(args)

    index_text = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    table_to_files = parse_index_mapping(index_text) if index_text else {}
    table_to_files.setdefault(metadata.table_name, [])

    existing_parts = load_existing_detail_parts(index_path, metadata.table_name)
    detail_markdown = render_detail_markdown(metadata, table_to_files[metadata.table_name], existing_parts)

    if args.print_only:
        print(detail_markdown.rstrip())
        return

    write_text(detail_path_for(index_path, metadata.table_name), detail_markdown)
    write_text(index_path, render_index_markdown(index_path, table_to_files))
    write_text(by_table_index_path_for(index_path), render_by_table_index_markdown(table_to_files))

    print(f"[INFO] Updated index: {index_path}")
    print(f"[INFO] Updated detail: {detail_path_for(index_path, metadata.table_name)}")
    print(f"[INFO] Table synced: {metadata.table_name}")
    print(f"[INFO] Column count: {len(metadata.columns)}")
    print(f"[INFO] Sample row count: {len(metadata.sample_rows)}")


if __name__ == "__main__":
    main()
