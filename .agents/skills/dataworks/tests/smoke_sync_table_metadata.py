#!/usr/bin/env python3
from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SKILL_DIR = ROOT / ".agents" / "skills" / "dataworks"
SCRIPT_PATH = SKILL_DIR / "scripts" / "sync_table_metadata.py"
FIXTURE_PATH = SKILL_DIR / "tests" / "fixtures" / "mock_table_metadata.json"
TMP_DIR = SKILL_DIR / "tests" / "tmp"
INDEX_PATH = TMP_DIR / "tables.md"
DETAIL_PATH = TMP_DIR / "by_table" / "demo_project.sales_order_di.md"
BY_TABLE_INDEX_PATH = TMP_DIR / "by_table" / "index.md"


def main() -> None:
    if TMP_DIR.exists():
        shutil.rmtree(TMP_DIR)
    TMP_DIR.mkdir(parents=True, exist_ok=True)

    INDEX_PATH.write_text(
        "# tables\n\n"
        "## SQL代码索引（表 -> 文件）\n\n"
        "### demo_project.sales_order_di\n"
        "- sample.sql\n\n",
        encoding="utf-8",
    )

    command = [
        sys.executable,
        str(SCRIPT_PATH),
        "--mock-metadata-json",
        str(FIXTURE_PATH),
        "--tables-md",
        str(INDEX_PATH),
    ]
    result = subprocess.run(command, capture_output=True, text=True)
    if result.returncode != 0:
        raise SystemExit(
            "sync_table_metadata.py failed in mock mode:\n"
            f"stdout:\n{result.stdout}\n\nstderr:\n{result.stderr}"
        )

    if not INDEX_PATH.exists():
        raise SystemExit(f"expected index markdown missing: {INDEX_PATH}")
    if not DETAIL_PATH.exists():
        raise SystemExit(f"expected detail markdown missing: {DETAIL_PATH}")
    if not BY_TABLE_INDEX_PATH.exists():
        raise SystemExit(f"expected by-table index markdown missing: {BY_TABLE_INDEX_PATH}")

    index_content = INDEX_PATH.read_text(encoding="utf-8")
    detail_content = DETAIL_PATH.read_text(encoding="utf-8")
    by_table_index_content = BY_TABLE_INDEX_PATH.read_text(encoding="utf-8")

    index_required = [
        "## SQL代码索引（表 -> 文件）",
        "### demo_project.sales_order_di",
        "- sample.sql",
        "## By Table",
        "[详情](./by_table/demo_project.sales_order_di.md)",
    ]
    detail_required = [
        "# demo_project.sales_order_di",
        "## 来源文件",
        "- sample.sql",
        "## 表结构",
        "| order_id | string | column | primary order id |  |",
        "### DDL",
        "CREATE TABLE demo_project.sales_order_di",
        "## 抽样数据",
        "o_1001",
        "## 同步来源",
        "`mock:mock_table_metadata.json`",
    ]

    missing = [fragment for fragment in index_required if fragment not in index_content]
    missing.extend(fragment for fragment in detail_required if fragment not in detail_content)
    missing.extend(
        fragment
        for fragment in [
            "# by_table",
            "| demo_project.sales_order_di | 1 | [详情](./demo_project.sales_order_di.md) |",
        ]
        if fragment not in by_table_index_content
    )
    if missing:
        raise SystemExit(f"output markdown missing expected fragments: {missing}")

    print("smoke_sync_table_metadata: PASS")


if __name__ == "__main__":
    main()
