#!/usr/bin/env python3
"""
Split a legacy monolithic tables.md into a top-level index and by-table docs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Rebuild tables reference layout into top-level index + by_table docs."
    )
    parser.add_argument(
        "--tables-md",
        default=".agents/skills/dataworks/references/tables.md",
        help="Legacy or current tables.md path.",
    )
    return parser.parse_args()


def slugify_table_name(table_name: str) -> str:
    return table_name.replace("/", "_")


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


def render_index_markdown(table_to_files: dict[str, list[str]]) -> str:
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
        lines.append(f"| {table} | [详情](./by_table/{slugify_table_name(table)}.md) |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_by_table_index_markdown(table_to_files: dict[str, list[str]]) -> str:
    lines = ["# by_table", ""]
    lines.append("| 表名 | 来源文件数 | 详情 |")
    lines.append("| --- | --- | --- |")
    for table in sorted(table_to_files.keys()):
        lines.append(f"| {table} | {len(table_to_files[table])} | [详情](./{slugify_table_name(table)}.md) |")
    lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def convert_detail(table: str, source_files: list[str], detail_text: str) -> str:
    body = re.sub(rf"(?m)^##\s+{re.escape(table)}\s*$", f"# {table}", detail_text, count=1).strip()
    if "## 来源文件" in body:
        return body + "\n"

    lines = [f"# {table}", "", "## 来源文件"]
    if source_files:
        for file_name in source_files:
            lines.append(f"- {file_name}")
    else:
        lines.append("- 未记录")
    lines.append("")

    remainder = "\n".join(body.splitlines()[2:]).strip()
    if remainder:
        lines.append(remainder)
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> None:
    args = parse_args()
    index_path = Path(args.tables_md)
    by_table_dir = index_path.parent / "by_table"
    content = index_path.read_text(encoding="utf-8")
    table_to_files, details = parse_legacy_file(content)

    by_table_dir.mkdir(parents=True, exist_ok=True)
    for table, detail_text in details.items():
        detail_path = by_table_dir / f"{slugify_table_name(table)}.md"
        detail_path.write_text(
            convert_detail(table, table_to_files.get(table, []), detail_text),
            encoding="utf-8",
        )
    (by_table_dir / "index.md").write_text(render_by_table_index_markdown(table_to_files), encoding="utf-8")

    index_path.write_text(render_index_markdown(table_to_files), encoding="utf-8")
    print(f"[INFO] Updated index: {index_path}")
    print(f"[INFO] Wrote by-table docs: {len(details)}")


if __name__ == "__main__":
    main()
