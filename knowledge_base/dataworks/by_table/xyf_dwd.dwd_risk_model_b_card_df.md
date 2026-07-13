# xyf_dwd.dwd_risk_model_b_card_df

## 来源文件
- 老客月会sql代码.ipynb

- `CASE WHEN b.model_value <= 1.2 THEN 'qualified' ELSE 'unqualified' END AS apply_24_risk_qualification`
- `CASE WHEN b.model_value IS NULL OR b.model_value < 0 THEN '空' WHEN b.model_value < 3 THEN 'AB' WHEN b.model_value < 5 THEN 'CD' WHEN b.model_value < 7 THEN 'EF' WHEN b.model_value < 9 THEN 'GH' ELSE 'IJK' END AS apply_model_score_category`
- `CASE WHEN b.model_value IS NULL OR b.model_value < 0 THEN '空' WHEN b.model_value < 3 THEN 'AB' WHEN b.model_value < 5 THEN 'CD' WHEN b.model_value < 7 THEN 'EF' WHEN b.model_value < 9 THEN 'GH' ELSE 'IJK' END AS loan_model_score_category`
- `DISTINCT a.*`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| cust_no | STRING | column | 客户号 | Y |
| random | BIGINT | column | 随机数 |  |
| id | BIGINT | column | personalloan_b_card_custlevel_v2.id |  |
| loan_type | STRING | column | 贷款类型 |  |
| decision_time | DATETIME | column | 决策时间 | Y |
| model_name | STRING | column | 模型名 |  |
| model_value | DOUBLE | column | 模型结果(老客评级) | Y |
| created_time | DATETIME | column | 创建时间 |  |
| updated_time | DATETIME | column | 更新时间 |  |
| model_value_detail | DOUBLE | column | 老客评级细分 |  |
| pt | STRING | column | 分区字段(yyyymmdd) | Y |
| pt | STRING | partition | 分区字段(yyyymmdd) | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_risk_model_b_card_df` (
  `cust_no` STRING COMMENT '客户号',
  `random` BIGINT COMMENT '随机数',
  `id` BIGINT COMMENT 'personalloan_b_card_custlevel_v2.id',
  `loan_type` STRING COMMENT '贷款类型',
  `decision_time` DATETIME COMMENT '决策时间',
  `model_name` STRING COMMENT '模型名',
  `model_value` DOUBLE COMMENT '模型结果(老客评级)',
  `created_time` DATETIME COMMENT '创建时间',
  `updated_time` DATETIME COMMENT '更新时间',
  `model_value_detail` DOUBLE COMMENT '老客评级细分'
)
COMMENT '个人分期放款成功用户b卡分明细'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '分区字段(yyyymmdd)'
)
STORED AS AliOrc
LIFECYCLE 2000
```

### 抽样数据
| cust_no | random | id | loan_type | decision_time | model_name | model_value | created_time | updated_time | model_value_detail | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| CTL000006706b9f954b722f5389153fa8d20 | 28 | 1026602 | personal_loan | 2024-05-19 00:00:00 | personalloan_jfd_stock_creditlevel_hcrh_v4_2_1 | 2.0 | 2024-05-19 07:13:15 | 2024-05-19 07:13:15 |  | 20240518 | 20240518 |
| CTL00000a0e81d6e2292cd4c25a864794e7a | 63 | 692639 | personal_loan | 2024-05-19 00:00:00 | personalloan_jfd_stock_creditlevel_hcrh_v4_2_1 | 9.0 | 2024-05-19 07:19:36 | 2024-05-19 07:19:36 |  | 20240518 | 20240518 |
| CTL00000ad3d9189a6bdd88c933649446def | 75 | 1218738 | personal_loan | 2024-05-19 00:00:00 | personalloan_jfd_stock_creditlevel_hcrh_v4_2_1 | 4.0 | 2024-05-19 07:16:33 | 2024-05-19 07:16:33 |  | 20240518 | 20240518 |
| CTL00000d05919071be9c0561b996f62e491 | 62 | 3319268 | personal_loan | 2024-05-19 00:00:00 | personalloan_jfd_stock_creditlevel_hcrh_v4_2_1 | 9.0 | 2024-05-19 07:12:17 | 2024-05-19 07:12:17 |  | 20240518 | 20240518 |
| CTL000011cad63fd9fce66698219836f8ab2 | 9 | 591010 | personal_loan | 2024-05-19 00:00:00 | personalloan_jfd_stock_creditlevel_hcrh_v4_2_1 | 2.0 | 2024-05-19 07:24:30 | 2024-05-19 07:24:30 |  | 20240518 | 20240518 |

### 同步来源
- `odps`
