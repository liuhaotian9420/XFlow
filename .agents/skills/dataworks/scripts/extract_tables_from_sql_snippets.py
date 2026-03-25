#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path


DDL_PREFIXES = (
    "create table",
    "drop table",
    "truncate",
    "alter table",
)

CLAUSE_KEYWORDS = (
    "where",
    "group by",
    "having",
    "order by",
    "limit",
    "distribute by",
    "sort by",
    "cluster by",
    "qualify",
)

SQL_KEYWORDS = {
    "select",
    "from",
    "where",
    "join",
    "left",
    "right",
    "full",
    "inner",
    "outer",
    "on",
    "group",
    "by",
    "having",
    "order",
    "limit",
    "as",
    "and",
    "or",
    "not",
    "in",
    "is",
    "null",
    "case",
    "when",
    "then",
    "else",
    "end",
    "distinct",
    "union",
    "all",
    "insert",
    "into",
    "overwrite",
    "table",
    "with",
    "if",
    "exists",
    "true",
    "false",
    "current_date",
    "date",
    "cast",
    "max_pt",
    "between",
    "over",
    "partition",
    "except",
}


@dataclass
class ExtractionResult:
    raw_fields: dict[str, set[str]]
    processed_fields: dict[str, set[str]]


def strip_identifier(token: str) -> str:
    t = token.strip()
    if t.startswith(("`", '"')) and t.endswith(("`", '"')) and len(t) >= 2:
        return t[1:-1]
    return t


def read_text_with_fallback(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")


def load_sql_chunks(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in {".sql", ".txt"}:
        return [read_text_with_fallback(path)]
    if suffix == ".ipynb":
        text = read_text_with_fallback(path)
        nb = json.loads(text)
        chunks: list[str] = []
        for cell in nb.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            source = cell.get("source", "")
            if isinstance(source, list):
                source = "".join(source)
            if isinstance(source, str) and source.strip():
                chunks.append(source)
        return chunks
    return []


def remove_sql_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"(?m)--[^\n]*$", " ", sql)
    return sql


def split_statements(sql: str) -> list[str]:
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False

    for ch in sql:
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif not in_single and not in_double and not in_backtick:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif ch == ";" and depth == 0:
                stmt = "".join(buf).strip()
                if stmt:
                    out.append(stmt)
                buf = []
                continue
        buf.append(ch)

    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out


def normalize_space(text: str) -> str:
    return re.sub(r"\s+", " ", text.strip())


def strip_outer_parens(text: str) -> str:
    s = text.strip()
    while s.startswith("(") and s.endswith(")"):
        depth = 0
        ok = True
        for i, ch in enumerate(s):
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
            if depth == 0 and i != len(s) - 1:
                ok = False
                break
        if not ok:
            break
        s = s[1:-1].strip()
    return s


def is_word_boundary(text: str, idx: int, ln: int) -> bool:
    left = text[idx - 1] if idx > 0 else " "
    right = text[idx + ln] if idx + ln < len(text) else " "
    return not (left.isalnum() or left == "_") and not (right.isalnum() or right == "_")


def find_keyword_positions_top_level(text: str, keyword: str) -> list[int]:
    lower = text.lower()
    kw = keyword.lower()
    hits: list[int] = []
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif not in_single and not in_double and not in_backtick:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif depth == 0 and lower.startswith(kw, i) and is_word_boundary(lower, i, len(kw)):
                hits.append(i)
                i += len(kw)
                continue
        i += 1
    return hits


def split_top_level_csv(text: str) -> list[str]:
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False

    for ch in text:
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif not in_single and not in_double and not in_backtick:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif ch == "," and depth == 0:
                part = "".join(buf).strip()
                if part:
                    out.append(part)
                buf = []
                continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out


def split_top_level_union(sql: str) -> list[str]:
    lower = sql.lower()
    parts: list[str] = []
    start = 0
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False
    i = 0
    while i < len(sql):
        ch = sql[i]
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif not in_single and not in_double and not in_backtick:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif depth == 0:
                if lower.startswith("union all", i) and is_word_boundary(lower, i, 9):
                    segment = sql[start:i].strip()
                    if segment:
                        parts.append(segment)
                    i += 9
                    start = i
                    continue
                if lower.startswith("union", i) and is_word_boundary(lower, i, 5):
                    segment = sql[start:i].strip()
                    if segment:
                        parts.append(segment)
                    i += 5
                    start = i
                    continue
        i += 1
    tail = sql[start:].strip()
    if tail:
        parts.append(tail)
    return parts


def parse_with_clause(sql: str) -> tuple[dict[str, str], str]:
    s = sql.lstrip()
    if not s.lower().startswith("with "):
        return {}, sql

    idx = 4
    while idx < len(s) and s[idx].isspace():
        idx += 1
    if s[idx : idx + 9].lower() == "recursive":
        idx += 9

    ctes: dict[str, str] = {}
    while idx < len(s):
        while idx < len(s) and s[idx].isspace():
            idx += 1
        name_start = idx
        while idx < len(s) and (s[idx].isalnum() or s[idx] in "._`$"):
            idx += 1
        cte_name = strip_identifier(s[name_start:idx])
        while idx < len(s) and s[idx].isspace():
            idx += 1
        if s[idx : idx + 2].lower() != "as":
            return ctes, s[name_start:]
        idx += 2
        while idx < len(s) and s[idx].isspace():
            idx += 1
        if idx >= len(s) or s[idx] != "(":
            return ctes, s[name_start:]
        depth = 0
        body_start = idx + 1
        while idx < len(s):
            ch = s[idx]
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth -= 1
                if depth == 0:
                    body = s[body_start:idx]
                    ctes[cte_name.lower()] = body
                    idx += 1
                    break
            idx += 1
        while idx < len(s) and s[idx].isspace():
            idx += 1
        if idx < len(s) and s[idx] == ",":
            idx += 1
            continue
        return ctes, s[idx:]
    return ctes, ""


def find_first_top_level(text: str, candidates: list[str]) -> tuple[int, str]:
    best = (-1, "")
    for kw in candidates:
        hits = find_keyword_positions_top_level(text, kw)
        if not hits:
            continue
        pos = hits[0]
        if best[0] == -1 or pos < best[0]:
            best = (pos, kw)
    return best


def parse_select_core(sql: str) -> tuple[str, str, dict[str, str]]:
    core = strip_outer_parens(sql)
    lower = core.lower().lstrip()
    if not lower.startswith("select "):
        return "", "", {}

    off = core.lower().find("select")
    after_select = core[off + 6 :]
    from_pos, _ = find_first_top_level(after_select, ["from"])
    if from_pos < 0:
        return after_select.strip(), "", {}
    select_clause = after_select[:from_pos].strip()
    after_from = after_select[from_pos + 4 :]

    clause_slices: dict[str, str] = {}
    clauses_sorted = sorted(
        ((p, kw) for kw in CLAUSE_KEYWORDS for p in find_keyword_positions_top_level(after_from, kw)),
        key=lambda x: x[0],
    )
    if not clauses_sorted:
        from_clause = after_from.strip()
    else:
        first_pos = clauses_sorted[0][0]
        from_clause = after_from[:first_pos].strip()
        for i, (pos, kw) in enumerate(clauses_sorted):
            end = clauses_sorted[i + 1][0] if i + 1 < len(clauses_sorted) else len(after_from)
            clause_slices[kw] = after_from[pos + len(kw) : end].strip()
    return select_clause, from_clause, clause_slices


def split_table_expr_and_alias(fragment: str) -> tuple[str, str]:
    frag = fragment.strip()
    if not frag:
        return "", ""
    if frag.startswith("("):
        depth = 0
        i = 0
        while i < len(frag):
            if frag[i] == "(":
                depth += 1
            elif frag[i] == ")":
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            i += 1
        expr = frag[:i].strip()
        rest = frag[i:].strip()
        rest = re.sub(r"^(?i:as)\s+", "", rest)
        alias = rest.split()[0] if rest else ""
        return expr, strip_identifier(alias)
    parts = frag.split()
    if len(parts) == 1:
        return parts[0], strip_identifier(parts[0].split(".")[-1])
    if len(parts) >= 3 and parts[-2].lower() == "as":
        alias = parts[-1]
        expr = " ".join(parts[:-2])
        return expr, strip_identifier(alias)
    alias = parts[-1]
    expr = " ".join(parts[:-1])
    return expr, strip_identifier(alias)


def parse_from_items(from_clause: str) -> tuple[list[tuple[str, str]], list[str]]:
    tables: list[tuple[str, str]] = []
    subqueries: list[str] = []
    s = from_clause.strip()
    if not s:
        return tables, subqueries

    def find_top_level(text: str, keyword: str, start: int = 0) -> int:
        hits = [p for p in find_keyword_positions_top_level(text[start:], keyword)]
        if not hits:
            return -1
        return start + hits[0]

    def find_next_join(text: str, start: int = 0) -> int:
        positions = find_keyword_positions_top_level(text[start:], "join")
        if not positions:
            return -1
        return start + positions[0]

    def parse_source(source_part: str) -> None:
        chunk = source_part.strip().rstrip(",")
        if not chunk:
            return
        if "," in chunk:
            pieces = split_top_level_csv(chunk)
            # If top-level split fails (e.g. commas only inside parentheses),
            # avoid recursive self-call on identical fragment.
            if len(pieces) > 1:
                for piece in pieces:
                    parse_source(piece)
                return
            if len(pieces) == 1 and pieces[0].strip() != chunk:
                parse_source(pieces[0])
                return
            # Otherwise fall through and parse as a single source chunk.
        table_expr, alias = split_table_expr_and_alias(chunk)
        if not table_expr:
            return
        if table_expr.startswith("("):
            inner = strip_outer_parens(table_expr)
            if re.match(r"(?is)^\s*(with|select)\b", inner):
                subqueries.append(inner)
            return
        table_name = strip_identifier(table_expr)
        if "." in table_name and not table_name.lower().startswith("select"):
            tables.append((table_name, alias or strip_identifier(table_name.split(".")[-1])))

    join_pos = find_next_join(s, 0)
    first_part = s if join_pos < 0 else s[:join_pos]
    parse_source(first_part)

    pos = join_pos
    while pos >= 0:
        j = pos + 4
        while j < len(s) and s[j].isspace():
            j += 1
        next_join = find_next_join(s, j)
        segment = s[j:] if next_join < 0 else s[j:next_join]
        on_pos = find_top_level(segment, "on", 0)
        source_part = segment if on_pos < 0 else segment[:on_pos]
        parse_source(source_part)
        pos = next_join

    return tables, subqueries


def extract_qualified_refs(expr: str) -> list[tuple[str, str]]:
    pattern = re.compile(r'([A-Za-z_][\w$]*|`[^`]+`)\s*\.\s*(`[^`]+`|[A-Za-z_][\w$]*)')
    out: list[tuple[str, str]] = []
    for a, c in pattern.findall(expr):
        out.append((strip_identifier(a).lower(), strip_identifier(c)))
    return out


def extract_unqualified_tokens(expr: str) -> list[str]:
    stripped = re.sub(r"'(?:''|[^'])*'", " ", expr)
    stripped = re.sub(r'"(?:""|[^"])*"', " ", stripped)
    tokens = re.findall(r"`[^`]+`|[A-Za-z_][\w$]*", stripped)
    out: list[str] = []
    for t in tokens:
        tok = strip_identifier(t)
        if tok.lower() in SQL_KEYWORDS:
            continue
        if re.search(rf"\b{re.escape(t)}\s*\(", stripped):
            continue
        out.append(tok)
    return out


def canonical_table_name(name: str) -> str:
    s = normalize_space(name)
    if not s:
        return ""
    # Remove trailing alias if accidentally kept in table token.
    parts = s.split()
    s = parts[0]
    s = strip_identifier(s)
    return s


def split_select_expr_alias(item: str) -> tuple[str, str]:
    s = item.strip()
    m = re.match(r"(?is)^(.*?)(?:\s+as\s+)(`[^`]+`|[A-Za-z_][\w$]*)\s*$", s)
    if m:
        return m.group(1).strip(), strip_identifier(m.group(2))
    depth = 0
    in_single = False
    in_double = False
    in_backtick = False
    for i in range(len(s) - 1, -1, -1):
        ch = s[i]
        if ch == "'" and not in_double and not in_backtick:
            in_single = not in_single
        elif ch == '"' and not in_single and not in_backtick:
            in_double = not in_double
        elif ch == "`" and not in_single and not in_double:
            in_backtick = not in_backtick
        elif ch.isspace() and depth == 0 and not in_single and not in_double and not in_backtick:
            rhs = s[i:].strip()
            lhs = s[:i].strip()
            if re.fullmatch(r"`[^`]+`|[A-Za-z_][\w$]*", rhs):
                return lhs, strip_identifier(rhs)
            break
        elif ch == ")" and not in_single and not in_double and not in_backtick:
            depth += 1
        elif ch == "(" and not in_single and not in_double and not in_backtick:
            depth = max(0, depth - 1)
    return s, ""


def is_simple_column(expr: str) -> bool:
    s = expr.strip()
    if s == "*" or re.fullmatch(r"([A-Za-z_][\w$]*|`[^`]+`)\s*\.\s*\*", s):
        return True
    return bool(re.fullmatch(r"([A-Za-z_][\w$]*|`[^`]+`)(\s*\.\s*([A-Za-z_][\w$]*|`[^`]+`))?", s))


def maybe_select_from_insert(stmt: str) -> str:
    lower = stmt.lower()
    if not lower.startswith("insert "):
        return stmt
    with_pos = find_keyword_positions_top_level(stmt, "with")
    select_pos = find_keyword_positions_top_level(stmt, "select")
    candidates = with_pos + select_pos
    if not candidates:
        return ""
    pos = min(candidates)
    return stmt[pos:]


def ensure_table(result: ExtractionResult, table: str) -> None:
    _ = result.raw_fields[table]
    _ = result.processed_fields[table]


def analyze_select(sql: str, result: ExtractionResult) -> None:
    union_parts = split_top_level_union(sql)
    if len(union_parts) > 1:
        for part in union_parts:
            analyze_query(part, result)
        return

    ctes, body = parse_with_clause(sql)
    for cte_sql in ctes.values():
        analyze_query(cte_sql, result)

    select_clause, from_clause, clauses = parse_select_core(body)
    if not select_clause or not from_clause:
        return

    tables, subqueries = parse_from_items(from_clause)
    alias_to_table: dict[str, str] = {}
    for table_name, alias in tables:
        ensure_table(result, table_name)
        alias_to_table[alias.lower()] = table_name
        alias_to_table[strip_identifier(table_name.split(".")[-1]).lower()] = table_name

    for sub in subqueries:
        analyze_query(sub, result)

    physical_tables = set(alias_to_table.values())
    default_table = next(iter(physical_tables)) if len(physical_tables) == 1 else ""

    def add_raw_from_expr(expr: str) -> set[str]:
        touched_tables: set[str] = set()
        for al, col in extract_qualified_refs(expr):
            if al in alias_to_table:
                table_name = alias_to_table[al]
                result.raw_fields[table_name].add(col)
                touched_tables.add(table_name)
        if default_table:
            expr_wo_qualified = re.sub(
                r'([A-Za-z_][\w$]*|`[^`]+`)\s*\.\s*(`[^`]+`|[A-Za-z_][\w$]*)',
                " ",
                expr,
            )
            expr_wo_qualified = re.sub(r'([A-Za-z_][\w$]*|`[^`]+`)\s*\.\s*\*', " ", expr_wo_qualified)
            for tok in extract_unqualified_tokens(expr_wo_qualified):
                if tok.lower() in alias_to_table:
                    continue
                result.raw_fields[default_table].add(tok)
                touched_tables.add(default_table)
        return touched_tables

    for item in split_top_level_csv(select_clause):
        src_expr, alias = split_select_expr_alias(item)
        touched = add_raw_from_expr(src_expr)
        simple = is_simple_column(src_expr)
        has_transform = (not simple) or bool(alias)
        if has_transform:
            target_tables = touched or ({default_table} if default_table else set())
            expr_text = normalize_space(item)
            for table_name in target_tables:
                if table_name:
                    result.processed_fields[table_name].add(expr_text)

    for clause_key in ("where", "group by", "having"):
        clause_text = clauses.get(clause_key, "")
        if clause_text:
            add_raw_from_expr(clause_text)

    for on_expr in re.findall(r"(?is)\bon\b(.*?)(?=(?:\bleft\b|\bright\b|\bfull\b|\binner\b|\bouter\b|\bcross\b)?\s*\bjoin\b|$)", from_clause):
        add_raw_from_expr(on_expr)


def analyze_query(sql: str, result: ExtractionResult) -> None:
    s = strip_outer_parens(sql.strip())
    if not s:
        return
    lowered = normalize_space(s).lower()
    if lowered.startswith(DDL_PREFIXES):
        return
    s = maybe_select_from_insert(s)
    if not s:
        return
    if re.match(r"(?is)^\s*(with|select)\b", s):
        analyze_select(s, result)


def build_markdown(result: ExtractionResult, file_to_tables: dict[str, set[str]]) -> str:
    merged_raw: dict[str, set[str]] = defaultdict(set)
    merged_proc: dict[str, set[str]] = defaultdict(set)
    for table, cols in result.raw_fields.items():
        ct = canonical_table_name(table)
        if ct:
            merged_raw[ct].update(cols)
    for table, exprs in result.processed_fields.items():
        ct = canonical_table_name(table)
        if ct:
            merged_proc[ct].update(exprs)

    table_to_files: dict[str, set[str]] = defaultdict(set)
    for file_name, tables in file_to_tables.items():
        for table in tables:
            table_to_files[table].add(file_name)

    lines = ["# tables", ""]
    lines.append("## SQL代码索引（文件 -> 表）")
    lines.append("")
    for file_name in sorted(file_to_tables.keys()):
        lines.append(f"### {file_name}")
        tables = sorted(file_to_tables[file_name])
        if tables:
            for table in tables:
                lines.append(f"- {table}")
        else:
            lines.append("- 无")
        lines.append("")

    lines.append("## SQL代码索引（表 -> 文件）")
    lines.append("")
    for table in sorted(table_to_files.keys()):
        lines.append(f"### {table}")
        for file_name in sorted(table_to_files[table]):
            lines.append(f"- {file_name}")
        lines.append("")

    all_tables = sorted(set(merged_raw.keys()) | set(merged_proc.keys()))
    for table in all_tables:
        raw_cols = sorted(merged_raw.get(table, set()))
        proc_exprs = sorted(merged_proc.get(table, set()))
        if not raw_cols and not proc_exprs:
            continue
        lines.append(f"## {table}")
        lines.append("")
        lines.append("### 原始字段")
        if raw_cols:
            for col in raw_cols:
                lines.append(f"- {col}")
        else:
            lines.append("- 无")
        lines.append("")
        lines.append("### 字段加工")
        if proc_exprs:
            for expr in proc_exprs:
                lines.append(f"- `{expr}`")
        else:
            lines.append("- 无")
        lines.append("")
    return "\n".join(lines).strip() + "\n"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Extract table fields from SQL snippets into Markdown.")
    parser.add_argument(
        "--input-dir",
        default=".agents/skills/dataworks/references/sql_snippets/sql代码",
        help="Input directory containing SQL-like files.",
    )
    parser.add_argument(
        "--output",
        default=".agents/skills/dataworks/references/tables.md",
        help="Output Markdown file path.",
    )
    parser.add_argument(
        "--include-ext",
        default=".sql,.txt,.ipynb",
        help="Comma-separated extensions to include.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    input_dir = Path(args.input_dir)
    output_path = Path(args.output)
    include_ext = {e.strip().lower() for e in args.include_ext.split(",") if e.strip()}

    result = ExtractionResult(raw_fields=defaultdict(set), processed_fields=defaultdict(set))
    file_text_map: dict[str, str] = {}

    files = sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in include_ext)
    for path in files:
        chunks = load_sql_chunks(path)
        file_text_map[path.name] = "\n".join(chunks)
        for chunk in chunks:
            clean = remove_sql_comments(chunk)
            for stmt in split_statements(clean):
                analyze_query(stmt, result)

    extracted_tables = set()
    extracted_tables.update(canonical_table_name(t) for t in result.raw_fields.keys())
    extracted_tables.update(canonical_table_name(t) for t in result.processed_fields.keys())
    extracted_tables = {t for t in extracted_tables if t}

    file_to_tables: dict[str, set[str]] = defaultdict(set)
    for file_name, text in file_text_map.items():
        lower_text = text.lower()
        for table in extracted_tables:
            pattern = rf"(?<![A-Za-z0-9_]){re.escape(table.lower())}(?![A-Za-z0-9_])"
            if re.search(pattern, lower_text):
                file_to_tables[file_name].add(table)
        if file_name not in file_to_tables:
            file_to_tables[file_name] = set()

    markdown = build_markdown(result, file_to_tables)
    output_path.write_text(markdown, encoding="utf-8")
    print(f"[INFO] Processed files: {len(files)}")
    print(f"[INFO] Output written: {output_path}")
    print(f"[INFO] Tables extracted: {len(set(result.raw_fields.keys()) | set(result.processed_fields.keys()))}")


if __name__ == "__main__":
    main()
