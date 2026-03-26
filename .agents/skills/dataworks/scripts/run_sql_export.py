#!/usr/bin/env python3
"""
Execute one ODPS SQL file, export result to Excel, and optionally cache to DuckDB.
"""

from __future__ import annotations

import argparse
import multiprocessing
import os
import re
import sys
import traceback
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import duckdb
import pandas as pd
from dotenv import load_dotenv

TABLE_NAME_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run one SQL file on ODPS and export results")
    parser.add_argument("file_path", help="Path to one .sql file")
    parser.add_argument("--save_path", default="./files", help="Directory for Excel output")
    parser.add_argument("--file_name", default=None, help="Output xlsx file name")

    parser.add_argument("--access-id", default=None, help="ODPS Access ID")
    parser.add_argument("--access-key", default=None, help="ODPS Access Key")
    parser.add_argument("--project", default=None, help="ODPS project")
    parser.add_argument("--endpoint", default=None, help="ODPS endpoint")

    parser.add_argument("--duckdb-path", default="warehouse.db", help="DuckDB database path")
    parser.add_argument("--duckdb-table", default=None, help="DuckDB table name for cache")
    parser.add_argument("--lifecycle", type=int, default=30, help="DuckDB cache lifecycle in days")
    return parser.parse_args()


def fail(stage: str, msg: str) -> None:
    print(f"[ERROR] {stage}: {msg}", file=sys.stderr)
    sys.exit(1)


def write_error_log(log_path: Path, stage: str, exc: Exception) -> None:
    log_path.parent.mkdir(parents=True, exist_ok=True)
    body = [
        f"stage: {stage}",
        f"timestamp: {datetime.now().isoformat(timespec='seconds')}",
        f"exception_type: {type(exc).__name__}",
        f"exception_message: {exc}",
        "",
        "traceback:",
        traceback.format_exc().rstrip(),
        "",
    ]
    log_path.write_text("\n".join(body), encoding="utf-8")
    print(f"[WARN] Error log saved: {log_path}")


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

    missing = []
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
    
    print(f"[INFO] ODPS credentials resolved in function: {access_id}, {access_key}, {project}, {endpoint}",flush=True)

    return access_id, access_key, project, endpoint


def read_sql_file(path: Path) -> str:
    if not path.exists() or not path.is_file():
        fail("SQL file read failure", f"file not found: {path}")
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:
        fail("SQL file read failure", str(exc))
        raise


def run_odps_sql(
    sql_text: str, access_id: str, access_key: str, project: str, endpoint: str, error_log_path: Path
) -> pd.DataFrame:
    try:
        from odps import ODPS
    except Exception as exc:
        fail("ODPS authentication/config failure", f"failed to import odps package: {exc}")

    try:
        odps = ODPS(access_id=access_id, secret_access_key=access_key, project=project, endpoint=endpoint)
        print(f"[INFO] ODPS client constructed: {access_id}, {access_key}, {project}, {endpoint}",flush=True)
    except Exception as exc:
        fail("ODPS authentication/config failure", str(exc))

    try:
        instance = odps.run_sql(sql_text)
        try:
            logview = instance.get_logview_address()
            print(f"[INFO] Logview: {logview}")
        except Exception:
            print("[INFO] Logview: unavailable")
    except Exception as exc:
        fail("ODPS execution failure", str(exc))

    try:
        instance.wait_for_success()
    except Exception as exc:
        fail("ODPS execution failure", str(exc))

    try:
        with instance.open_reader(tunnel=True, limit=False) as reader:
            # df = reader.to_pandas(n_process=multiprocessing.cpu_count())
            df = reader.to_pandas()
    except Exception as exc:
        write_error_log(error_log_path, "result fetch / reader failure", exc)
        try:
            with instance.open_reader(tunnel=False, limit=False) as reader:
                df = reader.to_pandas()
            print("[WARN] Fallback reader succeeded with tunnel=False")
        except Exception:
            fail("result fetch / reader failure", str(exc))

    return df


def validate_duckdb_table_name(name: str) -> None:
    if not TABLE_NAME_RE.fullmatch(name):
        fail("invalid DuckDB table name", f"unsafe table name: {name}")


def ensure_lifecycle(lifecycle: int) -> None:
    if lifecycle <= 0:
        fail("invalid lifecycle value", "lifecycle must be > 0 when duckdb-table is provided")


def cleanup_expired_tables(con: duckdb.DuckDBPyConnection, now: datetime) -> None:
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS __table_lifecycle (
            table_name VARCHAR PRIMARY KEY,
            created_at TIMESTAMP,
            expires_at TIMESTAMP,
            lifecycle_days INTEGER
        )
        """
    )

    expired = con.execute(
        """
        SELECT table_name
        FROM __table_lifecycle
        WHERE expires_at < ?
        """,
        [now],
    ).fetchall()

    for (table_name,) in expired:
        # table_name is produced by strict regex during insert; quote for safety.
        con.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    con.execute("DELETE FROM __table_lifecycle WHERE expires_at < ?", [now])


def write_to_duckdb(
    df: pd.DataFrame, db_path: str, table_name: str, lifecycle_days: int
) -> tuple[str, datetime]:
    now = datetime.now()
    expires_at = now + timedelta(days=lifecycle_days)
    con = None
    try:
        con = duckdb.connect(db_path)
        cleanup_expired_tables(con, now)
        con.register("df_tmp", df)
        con.execute(f'CREATE OR REPLACE TABLE "{table_name}" AS SELECT * FROM df_tmp')
        con.execute(
            """
            INSERT OR REPLACE INTO __table_lifecycle
            (table_name, created_at, expires_at, lifecycle_days)
            VALUES (?, ?, ?, ?)
            """,
            [table_name, now, expires_at, lifecycle_days],
        )
        con.unregister("df_tmp")
        return db_path, expires_at
    except Exception as exc:
        fail("DuckDB connection or write failure", str(exc))
        raise
    finally:
        if con is not None:
            con.close()


def main() -> None:
    load_dotenv(override=False)
    args = parse_args()

    # 1. verify file_path exists and is a file
    sql_path = Path(args.file_path)
    sql_text = read_sql_file(sql_path)

    # 2. verify ODPS credentials are present through args or env
    access_id, access_key, project, endpoint = resolve_odps_config(args)

    print(f"[INFO] ODPS credentials resolved: {access_id}, {access_key}, {project}, {endpoint}",flush=True)

    # 3. read SQL text exactly as-is from disk (already done above)
    # 4. execute SQL in ODPS
    # 5. wait for success before reading results
    # 6. fetch into pandas
    error_log_path = Path(args.save_path) / f"{sql_path.stem}.error.log"
    df = run_odps_sql(sql_text, access_id, access_key, project, endpoint, error_log_path)

    # 7. if empty, stop and report
    if df.empty:
        print("No data returned. Skipping exports.")
        return

    # 8. determine base_name
    base_name = (args.file_name or f"{sql_path.stem}.xlsx").strip()
    if not base_name.lower().endswith(".xlsx"):
        base_name += ".xlsx"

    # 9. export Excel
    save_dir = Path(args.save_path)
    save_dir.mkdir(parents=True, exist_ok=True)
    out_path = save_dir / base_name
    try:
        df.to_excel(out_path, index=False)
    except Exception as exc:
        fail("Excel write failure", str(exc))

    print(f"[INFO] Row count: {len(df)}")
    print(f"[INFO] Columns: {list(df.columns)}")
    print(f"[INFO] Excel output: {out_path}")

    # 10. optional DuckDB write
    if args.duckdb_table:
        validate_duckdb_table_name(args.duckdb_table)
        ensure_lifecycle(args.lifecycle)
        db_path, expires_at = write_to_duckdb(
            df=df,
            db_path=args.duckdb_path,
            table_name=args.duckdb_table,
            lifecycle_days=args.lifecycle,
        )
        print(f"[INFO] DuckDB output: {db_path}::{args.duckdb_table}")
        print(f"[INFO] Lifecycle expires at: {expires_at.isoformat(timespec='seconds')}")


if __name__ == "__main__":
    main()
