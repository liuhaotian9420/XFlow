#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path


PHYSICAL_TABLE_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*\.[A-Za-z_][A-Za-z0-9_]*$")


def is_physical_table(name: str) -> bool:
    return bool(PHYSICAL_TABLE_RE.fullmatch(name))


def is_alias_column_like(name: str) -> bool:
    parts = name.split(".")
    if len(parts) != 2:
        return False
    left, right = parts
    # Typical alias.column pattern; aliases are usually short.
    return len(left) <= 3 and right.lower() not in {"df", "hf", "di", "dwd", "dws", "ads", "dim"}


def read_text(path: Path) -> str:
    raw = path.read_bytes()
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        return raw.decode("gb18030", errors="replace")


def load_chunks(path: Path) -> list[str]:
    if path.suffix.lower() in {".sql", ".txt"}:
        return [read_text(path)]
    if path.suffix.lower() == ".ipynb":
        nb = json.loads(read_text(path))
        out: list[str] = []
        for cell in nb.get("cells", []):
            if cell.get("cell_type") != "code":
                continue
            src = cell.get("source", "")
            if isinstance(src, list):
                src = "".join(src)
            if isinstance(src, str) and src.strip():
                out.append(src)
        return out
    return []


def strip_comments(sql: str) -> str:
    sql = re.sub(r"/\*.*?\*/", " ", sql, flags=re.S)
    sql = re.sub(r"(?m)--[^\n]*$", " ", sql)
    return sql


def split_stmts(sql: str) -> list[str]:
    out: list[str] = []
    buf: list[str] = []
    depth = 0
    in_s = in_d = in_b = False
    for ch in sql:
        if ch == "'" and not in_d and not in_b:
            in_s = not in_s
        elif ch == '"' and not in_s and not in_b:
            in_d = not in_d
        elif ch == "`" and not in_s and not in_d:
            in_b = not in_b
        elif not in_s and not in_d and not in_b:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif ch == ";" and depth == 0:
                s = "".join(buf).strip()
                if s:
                    out.append(s)
                buf = []
                continue
        buf.append(ch)
    tail = "".join(buf).strip()
    if tail:
        out.append(tail)
    return out


def top_positions(text: str, kw: str) -> list[int]:
    low = text.lower()
    k = kw.lower()
    out: list[int] = []
    depth = 0
    in_s = in_d = in_b = False
    i = 0
    while i < len(text):
        ch = text[i]
        if ch == "'" and not in_d and not in_b:
            in_s = not in_s
        elif ch == '"' and not in_s and not in_b:
            in_d = not in_d
        elif ch == "`" and not in_s and not in_d:
            in_b = not in_b
        elif not in_s and not in_d and not in_b:
            if ch == "(":
                depth += 1
            elif ch == ")":
                depth = max(0, depth - 1)
            elif depth == 0 and low.startswith(k, i):
                l = low[i - 1] if i > 0 else " "
                r = low[i + len(k)] if i + len(k) < len(low) else " "
                if not (l.isalnum() or l == "_") and not (r.isalnum() or r == "_"):
                    out.append(i)
                    i += len(k)
                    continue
        i += 1
    return out


def normalize_table(tok: str) -> str:
    t = tok.strip().strip(",")
    t = t.split()[0] if t else t
    if t.startswith(("`", '"')) and t.endswith(("`", '"')) and len(t) >= 2:
        t = t[1:-1]
    return t


def parse_with(sql: str) -> tuple[dict[str, str], str]:
    s = sql.lstrip()
    if not s.lower().startswith("with "):
        return {}, sql
    i = 4
    ctes: dict[str, str] = {}
    while i < len(s):
        while i < len(s) and s[i].isspace():
            i += 1
        j = i
        while j < len(s) and (s[j].isalnum() or s[j] in "._`$"):
            j += 1
        name = normalize_table(s[i:j]).lower()
        i = j
        while i < len(s) and s[i].isspace():
            i += 1
        if s[i : i + 2].lower() != "as":
            return ctes, s[i:]
        i += 2
        while i < len(s) and s[i].isspace():
            i += 1
        if i >= len(s) or s[i] != "(":
            return ctes, s[i:]
        depth = 1
        i += 1
        start = i
        while i < len(s) and depth > 0:
            if s[i] == "(":
                depth += 1
            elif s[i] == ")":
                depth -= 1
            i += 1
        body = s[start : i - 1]
        ctes[name] = body
        while i < len(s) and s[i].isspace():
            i += 1
        if i < len(s) and s[i] == ",":
            i += 1
            continue
        return ctes, s[i:]
    return ctes, ""


def parse_source_part(chunk: str) -> tuple[str, str]:
    c = chunk.strip().rstrip(",")
    if not c:
        return "", ""
    if c.startswith("("):
        depth = 0
        i = 0
        while i < len(c):
            if c[i] == "(":
                depth += 1
            elif c[i] == ")":
                depth -= 1
                if depth == 0:
                    i += 1
                    break
            i += 1
        expr = c[:i].strip()
        rest = c[i:].strip()
    else:
        parts = c.split()
        expr = parts[0]
        rest = " ".join(parts[1:])
    alias = ""
    if rest:
        rest = re.sub(r"(?i)^as\s+", "", rest).strip()
        if rest:
            alias = normalize_table(rest.split()[0])
    return expr, alias


def extract_select_relations(sql: str, out: dict[tuple[str, str], list[tuple[str, str]]]) -> None:
    s = sql.strip()
    if not s:
        return
    low = s.lower()
    if low.startswith(("create table", "drop table", "truncate", "alter table")):
        return
    if low.startswith("insert "):
        sel = top_positions(s, "select")
        wth = top_positions(s, "with")
        pos = min(sel + wth) if (sel or wth) else -1
        if pos < 0:
            return
        s = s[pos:]

    ctes, body = parse_with(s)
    for cte_sql in ctes.values():
        extract_select_relations(cte_sql, out)

    if not re.match(r"(?is)^\s*select\b", body):
        return
    frm = top_positions(body, "from")
    if not frm:
        return
    from_part = body[frm[0] + 4 :]
    next_clause = []
    for kw in ["where", "group by", "having", "order by", "limit"]:
        next_clause.extend(top_positions(from_part, kw))
    cut = min(next_clause) if next_clause else len(from_part)
    from_part = from_part[:cut]

    base_chunk = from_part[: top_positions(from_part, "join")[0]] if top_positions(from_part, "join") else from_part
    base_expr, base_alias = parse_source_part(base_chunk)
    alias_map: dict[str, str] = {}

    def resolve(expr: str, alias: str) -> str:
        e = expr.strip()
        if e.startswith("("):
            inner = e[1:-1].strip()
            if re.match(r"(?is)^(with|select)\b", inner):
                extract_select_relations(inner, out)
                tbls = re.findall(r"\b([A-Za-z_][\w$]*\.[A-Za-z_][\w$]*)\b", inner)
                return tbls[0].lower() if tbls else (alias.lower() if alias else "")
            return alias.lower() if alias else ""
        t = normalize_table(e).lower()
        return t

    left_table = resolve(base_expr, base_alias)
    if base_alias:
        alias_map[base_alias.lower()] = left_table
    if "." in left_table:
        alias_map[left_table.split(".")[-1]] = left_table

    i = 0
    while True:
        joins = top_positions(from_part[i:], "join")
        if not joins:
            break
        j = i + joins[0]
        jp = from_part[i:j].strip().lower()
        jt = "join"
        if re.search(r"\bleft\b", jp):
            jt = "left join"
        elif re.search(r"\bright\b", jp):
            jt = "right join"
        elif re.search(r"\bfull\b", jp):
            jt = "full join"
        elif re.search(r"\bcross\b", jp):
            jt = "cross join"
        elif re.search(r"\binner\b", jp):
            jt = "inner join"

        k = j + 4
        next_join = top_positions(from_part[k:], "join")
        seg_end = (k + next_join[0]) if next_join else len(from_part)
        seg = from_part[k:seg_end]
        on_pos = top_positions(seg, "on")
        using_pos = top_positions(seg, "using")
        cond = ""
        if using_pos and (not on_pos or using_pos[0] < on_pos[0]):
            src = seg[: using_pos[0]]
            cond = "USING " + seg[using_pos[0] + 5 :].strip()
        elif on_pos:
            src = seg[: on_pos[0]]
            cond = seg[on_pos[0] + 2 :].strip()
        else:
            src = seg

        right_expr, right_alias = parse_source_part(src)
        right_table = resolve(right_expr, right_alias)
        if right_alias:
            alias_map[right_alias.lower()] = right_table
        if "." in right_table:
            alias_map[right_table.split(".")[-1]] = right_table

        if left_table and right_table and cond:
            out[(left_table, right_table)].append((jt, re.sub(r"\s+", " ", cond).strip()))

        left_table = right_table or left_table
        i = seg_end


def main() -> None:
    input_dir = Path(".agents/skills/sql-generator/references/sql代码")
    output_path = Path(".agents/skills/sql-generator/references/relations.md")
    rels: dict[tuple[str, str], list[tuple[str, str]]] = defaultdict(list)

    files = sorted(p for p in input_dir.iterdir() if p.is_file() and p.suffix.lower() in {".sql", ".txt", ".ipynb"})
    for p in files:
        for chunk in load_chunks(p):
            clean = strip_comments(chunk)
            for stmt in split_stmts(clean):
                extract_select_relations(stmt, rels)

    lines = ["# join_relations", ""]
    physical_keys = [
        k
        for k in sorted(rels.keys())
        if is_physical_table(k[0]) and is_physical_table(k[1]) and not is_alias_column_like(k[0]) and not is_alias_column_like(k[1])
    ]
    for (l, r) in physical_keys:
        lines.append(f"## {l} -> {r}")
        lines.append("")
        for jt, cond in rels[(l, r)]:
            lines.append(f"- join_type: `{jt}`")
            lines.append(f"- condition: `{cond}`")
            lines.append("")
    output_path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    print(f"[INFO] files={len(files)} relations={sum(len(v) for v in rels.values())} pairs={len(rels)}")
    print(f"[INFO] wrote {output_path}")


if __name__ == "__main__":
    main()
