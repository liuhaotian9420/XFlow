# xyf_bi_dev.api_app_2_ord_v1120

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| id_card_number | STRING | column |  |  |
| app_user_id | BIGINT | column |  |  |
| order_number | STRING | column |  |  |
| created_time | DATETIME | column |  |  |
| pay_time | DATETIME | column |  |  |
| loan_type | STRING | column |  |  |
| inner_app | STRING | column |  |  |
| amt | DOUBLE | column |  |  |
| remit_status | STRING | column |  |  |

### DDL
```sql
CREATE TABLE xyf_bi_dev.`api_app_2_ord_v1120` (
  `id_card_number` STRING,
  `app_user_id` BIGINT,
  `order_number` STRING,
  `created_time` DATETIME,
  `pay_time` DATETIME,
  `loan_type` STRING,
  `inner_app` STRING,
  `amt` DOUBLE,
  `remit_status` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| id_card_number | app_user_id | order_number | created_time | pay_time | loan_type | inner_app | amt | remit_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| +++0cdTH34lOwdMxpOKAXuVgIlCZnLIooGuBDfhPkOk= | 1099841798 | 202305141735380241124254 | 2023-05-14 17:35:38 |  | 加贷 | xyf01 | 0.0 | failed |
| +++8cFRjpPb5SOOcC5mJXY0KEr9KivlJRU/stN5SSOw= | 1267309218 | 2024121500123600000014899514 | 2024-12-15 12:31:18 | 2024-12-15 13:08:53 | 加贷 | xyf01 | 1200.0 | success |
| +++C28tUNbJu6K8g6gZmM1Oj/3RBQZPEXYA+PYXtkaw= | 1029932033 | 202308141123150249138258 | 2023-08-14 11:23:15 | 2023-08-14 11:51:14 | 加贷 | fxk | 28000.0 | success |
| +++PS6YLT7zgQzqBwUgw4bThfgtbeR6KsdGm243NmBI= | 1052484495 | 2024062300001700000011482257 | 2024-06-23 18:43:06 |  | 加贷 | xyf01 | 0.0 | failed |
| +++PS6YLT7zgQzqBwUgw4bThfgtbeR6KsdGm243NmBI= | 1052484495 | 2024070500001700000093609675 | 2024-07-05 13:07:30 |  | 加贷 | xyf01 | 0.0 | failed |

## 同步来源
- `odps`
