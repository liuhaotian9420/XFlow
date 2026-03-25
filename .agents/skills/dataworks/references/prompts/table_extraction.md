# SQL 表字段抽取 Prompt（最终版）

你现在要做的是：扫描 `@sql代码` 文件夹下的 SQL 文件，从其中的**常规 SQL query** 中抽取结构化信息，并将结果整理为 Markdown 文档，写入：

`.agents\skills\dataworks\references\tables.md`

---

# 任务目标

从 SQL 中抽取以下信息：

1. **来源物理表**
2. **原始字段名**
3. **字段加工表达式**
   - 包括但不限于：
     - 字段别名
     - 聚合函数（sum / count / avg / max / min 等）
     - case when
     - if
     - concat
     - cast
     - 条件聚合
     - 常量赋值
     - 其他可以从 SQL 字面上明确识别的字段加工

最终输出为一个 Markdown 文档，按表汇总这些信息。

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

则只分析其后面的 **select query 主体**，不要把目标表当作来源表。

---

## 2. 只记录“确定性信息”
你只能写入**可以从 SQL 字面直接确认**的信息。

禁止做以下事情：
- 根据字段名猜业务含义
- 根据 alias 猜字段语义
- 根据函数名猜业务用途
- 根据上下文补充注释里没明确写出的结论

例如：
- `flag_a` 不能自动解释成“是否活跃用户”
- `score_x` 不能自动解释成“标准化分”
- `f_1(score)` 不能推断为“归一化”或“分桶”

对于无法确定语义的表达式，**保留原 SQL 表达式即可**。

---

## 3. 要追溯到底层物理表
如果 SQL 中使用了：
- CTE (`with ... as (...)`)
- 子查询
- 多层嵌套查询
- `union all`

你需要尽量将字段使用追溯到**底层物理表**。

注意：
- 不要把 CTE 名称当作物理表
- 不要把子查询别名当作物理表
- 中间层别名如 `t`、`base`、`agg` 不是最终沉淀对象
- 最终应以真实来源表为单位整理

---

## 4. 原始字段与字段加工的区分规则

### 原始字段
指直接来自来源表、未经过加工的底层字段，例如：
- `user_id`
- `dt`
- `amount`
- `order_id`

### 字段加工
指任何带有变换、重命名、聚合、条件逻辑的表达式，例如：
- `level AS vip_level`
- `sum(amount) AS total_amt`
- `count(*) AS order_cnt`
- `case when score >= 90 then 'A' else 'B' end AS score_level`
- `concat(dt, '_', city_code) AS dt_city_key`
- `'A' AS src`

---

## 5. group by / where / join 中出现的底层字段也应纳入原始字段
只要某字段被明确用于 query 中，并且可确认来自某来源表，就应记录到该表的“原始字段”里。常见位置包括：
- `select`
- `where`
- `join on`
- `group by`
- `having`

---

## 6. 多表同名字段不能混淆
如果多个表中都有同名字段，例如 `a.dt`、`b.dt`，必须按各自来源表分别记录，不能合并成一个不区分来源的字段集合。

---

## 7. 输出应尽量去重、合并
对于同一张表：
- 原始字段去重
- 字段加工去重
- 同一表达式不要重复记录多次

---

# 输出格式要求

将结果输出为 Markdown，格式如下：

# tables

## <table_name>

### 原始字段
- <column_1>
- <column_2>
- <column_3>

### 字段加工
- `<expression_1>`
- `<expression_2>`

说明：
- 每张表一个二级标题
- 原始字段与字段加工分别列出
- 字段加工请尽量保留原 SQL 表达式
- 若某表没有可明确识别的字段加工，可写：
  - `- 无`
  或者省略“字段加工”小节，但全文风格要统一
- 不要输出多余解释，不要写分析过程，不要写推测性备注

---

# 执行优先级

当信息不完整或存在歧义时，遵循以下优先级：

1. **宁可少写，也不要猜**
2. **宁可保留原表达式，也不要解释语义**
3. **宁可忽略不确定映射，也不要写错来源表**

---

# Few-shot Examples

## Example 1

### Input
```sql
DROP TABLE IF EXISTS tmp_a;

CREATE TABLE tmp_b AS
SELECT *
FROM some_other_table;

SELECT
    a.user_id,
    a.dt,
    a.city_code,
    b.level AS vip_level,
    concat(a.dt, '_', a.city_code) AS dt_city_key
FROM dwd.user_profile a
LEFT JOIN dim.vip_user b
    ON a.user_id = b.user_id
WHERE a.dt = '${bizdate}';
```

### Output
```markdown
# tables

## dwd.user_profile

### 原始字段
- user_id
- dt
- city_code

### 字段加工
- `concat(dt, '_', city_code) AS dt_city_key`

## dim.vip_user

### 原始字段
- user_id
- level

### 字段加工
- `level AS vip_level`
```

---

## Example 2

### Input
```sql
SELECT
    order_date,
    shop_id,
    count(*) AS order_cnt,
    sum(pay_amount) AS total_pay_amount,
    avg(pay_amount) AS avg_pay_amount,
    max(pay_amount) AS max_pay_amount
FROM dws.trade_order_di
WHERE order_date >= '2026-01-01'
GROUP BY order_date, shop_id;
```

### Output
```markdown
# tables

## dws.trade_order_di

### 原始字段
- order_date
- shop_id
- pay_amount

### 字段加工
- `count(*) AS order_cnt`
- `sum(pay_amount) AS total_pay_amount`
- `avg(pay_amount) AS avg_pay_amount`
- `max(pay_amount) AS max_pay_amount`
```

---

## Example 3

### Input
```sql
SELECT
    dt,
    user_id,
    case
        when score >= 90 then 'A'
        when score >= 80 then 'B'
        else 'C'
    end AS score_level,
    sum(case when is_paid = 1 then amount else 0 end) AS paid_amount,
    count(case when is_paid = 1 then order_id end) AS paid_order_cnt
FROM app.user_score_order_df
GROUP BY
    dt,
    user_id,
    case
        when score >= 90 then 'A'
        when score >= 80 then 'B'
        else 'C'
    end;
```

### Output
```markdown
# tables

## app.user_score_order_df

### 原始字段
- dt
- user_id
- score
- is_paid
- amount
- order_id

### 字段加工
- `case when score >= 90 then 'A' when score >= 80 then 'B' else 'C' end AS score_level`
- `sum(case when is_paid = 1 then amount else 0 end) AS paid_amount`
- `count(case when is_paid = 1 then order_id end) AS paid_order_cnt`
```

---

## Example 4

### Input
```sql
SELECT
    t.user_id,
    t.total_amt,
    t.order_cnt
FROM (
    SELECT
        user_id,
        sum(amount) AS total_amt,
        count(order_id) AS order_cnt
    FROM ods.order_info_di
    WHERE dt = '${bizdate}'
    GROUP BY user_id
) t
WHERE t.total_amt > 100;
```

### Output
```markdown
# tables

## ods.order_info_di

### 原始字段
- user_id
- amount
- order_id
- dt

### 字段加工
- `sum(amount) AS total_amt`
- `count(order_id) AS order_cnt`
```

---

## Example 5

### Input
```sql
WITH base AS (
    SELECT
        user_id,
        item_id,
        pay_amount,
        dt
    FROM dwd.trade_detail_di
    WHERE dt = '${bizdate}'
),
agg AS (
    SELECT
        user_id,
        sum(pay_amount) AS total_pay_amount,
        count(item_id) AS item_cnt
    FROM base
    GROUP BY user_id
)
SELECT
    user_id,
    total_pay_amount,
    item_cnt
FROM agg;
```

### Output
```markdown
# tables

## dwd.trade_detail_di

### 原始字段
- user_id
- item_id
- pay_amount
- dt

### 字段加工
- `sum(pay_amount) AS total_pay_amount`
- `count(item_id) AS item_cnt`
```

---

## Example 6

### Input
```sql
SELECT
    user_id,
    f_1(score) AS score_x,
    f_2(tag) AS tag_y
FROM ads.user_feature_df;
```

### Output
```markdown
# tables

## ads.user_feature_df

### 原始字段
- user_id
- score
- tag

### 字段加工
- `f_1(score) AS score_x`
- `f_2(tag) AS tag_y`
```

---

# 现在开始执行

请扫描 `@sql代码` 文件夹中的 SQL 文件，基于以上规则抽取信息，并生成最终 Markdown 内容，写入：

`.agents\skills\dataworks\references\tables.md`

只输出最终 Markdown 成品，不要输出解释、过程、推理或额外说明。
