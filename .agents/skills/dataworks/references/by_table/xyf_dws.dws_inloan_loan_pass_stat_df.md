# xyf_dws.dws_inloan_loan_pass_stat_df

## 来源文件
- ads_inloan_loan_pass_monitor_df.sql

- `DATE(created_time) AS created_date`
- `DATE_ADD(created_time,-30) AS sub30_created_date`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| cust_no | STRING | column |  | Y |
| inner_app | STRING | column |  |  |
| app | STRING | column |  |  |
| loan_type_flag | STRING | column |  |  |
| order_number | STRING | column |  |  |
| amt | DECIMAL(38,18) | column |  |  |
| created_time | DATETIME | column |  | Y |
| risk_status | STRING | column |  | Y |
| remit_status | STRING | column |  |  |
| pay_time | DATETIME | column |  |  |
| loan_rn | BIGINT | column |  |  |
| b_cust_no | STRING | column |  |  |
| b_pay_time | DATETIME | column |  | Y |
| b_inner_app | STRING | column |  |  |
| c_cust_no | STRING | column |  |  |
| c_created_time | DATETIME | column |  | Y |
| is_refuse_recent30 | STRING | column |  |  |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_inloan_loan_pass_stat_df` (
  `cust_no` STRING,
  `inner_app` STRING,
  `app` STRING,
  `loan_type_flag` STRING,
  `order_number` STRING,
  `amt` DECIMAL(38,18),
  `created_time` DATETIME,
  `risk_status` STRING,
  `remit_status` STRING,
  `pay_time` DATETIME,
  `loan_rn` BIGINT,
  `b_cust_no` STRING,
  `b_pay_time` DATETIME,
  `b_inner_app` STRING,
  `c_cust_no` STRING,
  `c_created_time` DATETIME,
  `is_refuse_recent30` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| cust_no | inner_app | app | loan_type_flag | order_number | amt | created_time | risk_status | remit_status | pay_time | loan_rn | b_cust_no | b_pay_time | b_inner_app | c_cust_no | c_created_time | is_refuse_recent30 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTL00000074ac23c3f79bec0abc09b316b25 | xyf01 | xyf01 | 加贷 | 2025041600123600000030552248 | 600 | 2025-04-16 14:10:42 | reject | failed |  | 1 | CTL00000074ac23c3f79bec0abc09b316b25 | 2025-01-27 13:40:09 | xyf01_shenbei | CTL00000074ac23c3f79bec0abc09b316b25 | 2025-05-28 17:15:01 | 0 |
| CTL0000007b70a20e317423a3316750e5602 | xyf01 | xyf01 | 复贷 | 202311211622380266904617 | 7000 | 2023-11-21 16:22:35 | reject | failed |  | 17 |  |  |  |  |  | 1 |
| CTL0000007e4a32a9129595542fe72664d33 | xyf01 | xyf01 | 加贷 | 2024111200123700000036825822 | 40000 | 2024-11-12 12:06:24 | pass | success | 2024-11-12 12:41:58 | 3 |  |  |  | CTL0000007e4a32a9129595542fe72664d33 | 2024-11-11 09:21:37 | 0 |
| CTL000000ea50a5c32cc5008cc8fa4da96cd | xyf01 | xyf01 | 加贷 | 2025032800123700000062888570 | 3100 | 2025-03-28 18:38:15 | pass | success | 2025-03-28 18:46:12 | 3 |  |  |  | CTL000000ea50a5c32cc5008cc8fa4da96cd | 2025-03-20 11:00:17 | 0 |
| CTL000001761fdbf81cc28c8805c80d55571 | xyf01 | xyf01 | 加贷 | 2025071300123700000032320582 | 1100 | 2025-07-13 11:20:36 | pass | success | 2025-07-13 11:56:16 | 5 |  |  |  | CTL000001761fdbf81cc28c8805c80d55571 | 2025-04-24 12:01:14 | 0 |

### 同步来源
- `odps`
