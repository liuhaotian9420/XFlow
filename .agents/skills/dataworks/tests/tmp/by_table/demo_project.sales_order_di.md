# demo_project.sales_order_di

## 来源文件
- sample.sql

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_id | string | column | primary order id |  |
| buyer_id | string | column | buyer user id |  |
| pay_amount | decimal(18,2) | column | paid amount |  |
| ds | string | partition | partition date |  |

### DDL
```sql
CREATE TABLE demo_project.sales_order_di (
  order_id STRING COMMENT 'primary order id',
  buyer_id STRING COMMENT 'buyer user id',
  pay_amount DECIMAL(18,2) COMMENT 'paid amount'
)
PARTITIONED BY (
  ds STRING COMMENT 'partition date'
);
```

## 抽样数据
| order_id | buyer_id | pay_amount | ds |
| --- | --- | --- | --- |
| o_1001 | u_01 | 128.50 | 2026-03-27 |
| o_1002 | u_02 | 256.00 | 2026-03-27 |

## 同步来源
- `mock:mock_table_metadata.json`
