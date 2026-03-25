# SQL 表间 JOIN 关系抽取 Prompt

你现在要做的是：扫描 `@sql代码` 文件夹下的 SQL 文件，从其中的**常规 SQL query** 中抽取表与表之间的 **JOIN relation**，并将结果整理为 Markdown 文档 输出到 `.agents\skills\sql-generator\references\relations.md`。

---

# 任务目标

从 SQL 中抽取以下信息：

1. **参与 JOIN 的左表**
2. **参与 JOIN 的右表**
3. **JOIN 类型**
   - 例如：
     - inner join
     - left join
     - right join
     - full join
     - cross join
4. **JOIN 条件**
   - 即 `on` 后面的明确条件
5. **可选：中间别名映射**
   - 如果 SQL 使用了表别名，应还原成真实表名

最终输出为一个 Markdown 文档，按“表关系”列出。

---

# 严格规则

## 1. 只处理常规 query，忽略 DDL / 非主体语句
以下语句不要作为抽取主体：
- `create table`
- `drop table`
- `truncate`
- `alter`
- 其他 DDL

如果 SQL 中有：
- `insert into ... select ...`
- `insert overwrite ... select ...`

则只分析其后面的 `select query` 主体。

---

## 2. 只记录 SQL 中明确存在的 JOIN relation
你只能提取 SQL 字面中明确写出的关系。

禁止做以下事情：
- 猜测主键 / 外键关系
- 猜测一对一 / 一对多 / 多对多
- 猜测业务含义
- 根据字段名推断表之间“应该”有关联
- 把 `where` 中的过滤条件解释成 join relation

例如：
- `a.user_id = b.user_id` 可以记录
- “用户表和订单表是一对多关系” 不可以写
- “这可能是维表关联” 不可以写

---

## 3. 要尽量还原到真实物理表
如果 SQL 中使用了：
- 表别名
- CTE
- 子查询
- 多层嵌套查询

应尽量还原成真实来源表。

注意：
- 不要把别名 `a`、`b`、`t1`、`t2` 当成最终表名
- 不要把 CTE 名称当作物理表
- 不要把子查询别名当成物理表
- 如果无法可靠追溯到底层物理表，则保留当前 query 中可以确认的最近一层来源，但不要猜

---

## 4. JOIN 条件只保留确定性的 ON / USING 内容
对于每一条 JOIN，只记录 SQL 中明确出现的条件，例如：
- `a.user_id = b.user_id`
- `a.dt = b.dt`
- `a.user_id = b.user_id AND a.ds = b.ds`

如果使用 `USING (user_id, dt)`，则按原样记录。

不要把以下内容写成 JOIN 条件：
- `where`
- `group by`
- `having`
- `select` 中的表达式

---

## 5. 同一对表出现多次 JOIN，要分别记录
如果同一 SQL 或不同 SQL 文件中，同一对表之间存在多种 JOIN 写法或多次 JOIN，不要强行合并成一条模糊关系。应保留各自明确的 JOIN 条件。

---

# 输出格式要求

将结果输出为 Markdown，格式如下：

# join_relations

## <left_table> -> <right_table>

- join_type: `<join_type>`
- condition: `<join_condition>`

如果同一对表有多条关系，可以写成：

## <left_table> -> <right_table>

- join_type: `<join_type_1>`
- condition: `<join_condition_1>`

- join_type: `<join_type_2>`
- condition: `<join_condition_2>`

说明：
- 表名尽量使用真实物理表名
- join_type 统一小写
- condition 尽量保留原 SQL 表达式
- 不要输出解释、推理、猜测或业务说明

---

# 执行优先级

当信息不完整或存在歧义时，遵循以下优先级：

1. **宁可少写，也不要猜**
2. **宁可保留原 join 条件，也不要解释含义**
3. **宁可保留别名层关系，也不要错误追溯到底表**

---

# Few-shot Examples

## Example 1

### Input
```sql
SELECT
    a.user_id,
    b.level
FROM dwd.user_profile a
LEFT JOIN dim.vip_user b
    ON a.user_id = b.user_id;
```

### Output
```markdown
# join_relations

## dwd.user_profile -> dim.vip_user

- join_type: `left join`
- condition: `a.user_id = b.user_id`
```

---

## Example 2

### Input
```sql
SELECT
    a.user_id,
    a.dt,
    b.device_type
FROM dwd.user_trade_di a
INNER JOIN dwd.user_login_di b
    ON a.user_id = b.user_id
   AND a.dt = b.dt;
```

### Output
```markdown
# join_relations

## dwd.user_trade_di -> dwd.user_login_di

- join_type: `inner join`
- condition: `a.user_id = b.user_id AND a.dt = b.dt`
```

---

## Example 3

### Input
```sql
WITH base AS (
    SELECT *
    FROM dwd.order_di
),
dimx AS (
    SELECT *
    FROM dim.shop_df
)
SELECT
    a.order_id,
    b.shop_name
FROM base a
LEFT JOIN dimx b
    ON a.shop_id = b.shop_id;
```

### Output
```markdown
# join_relations

## dwd.order_di -> dim.shop_df

- join_type: `left join`
- condition: `a.shop_id = b.shop_id`
```

---

## Example 4

### Input
```sql
SELECT
    *
FROM ods.a t1
JOIN ods.b t2
    USING (user_id, dt);
```

### Output
```markdown
# join_relations

## ods.a -> ods.b

- join_type: `join`
- condition: `USING (user_id, dt)`
```

---

## Example 5

### Input
```sql
SELECT
    *
FROM ods.order_info o
LEFT JOIN (
    SELECT user_id, max(dt) AS last_dt
    FROM ods.user_log
    GROUP BY user_id
) u
    ON o.user_id = u.user_id;
```

### Output
```markdown
# join_relations

## ods.order_info -> ods.user_log

- join_type: `left join`
- condition: `o.user_id = u.user_id`
```

---

# 现在开始执行

请扫描 `@sql代码` 文件夹中的 SQL 文件，基于以上规则抽取表间 JOIN relation，并输出最终 Markdown 成品。

只输出最终 Markdown，不要输出解释、过程、推理或额外说明。
