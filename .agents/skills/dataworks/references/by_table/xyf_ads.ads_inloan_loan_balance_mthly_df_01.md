# xyf_ads.ads_inloan_loan_balance_mthly_df_01

## 来源文件
- ads_inloan_loan_balance_mthly_df.sql

- 无

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| data_date | STRING | column |  | Y |
| flag | STRING | column |  | Y |
| loan_type | STRING | column |  | Y |
| loan_amt_30 | DOUBLE | column |  | Y |
| loan_amt_90 | DOUBLE | column |  | Y |
| loan_amt_180 | DOUBLE | column |  | Y |

#### DDL
```sql
CREATE TABLE xyf_ads.`ads_inloan_loan_balance_mthly_df_01` (
  `data_date` STRING,
  `flag` STRING,
  `loan_type` STRING,
  `loan_amt_30` DOUBLE,
  `loan_amt_90` DOUBLE,
  `loan_amt_180` DOUBLE
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| data_date | flag | loan_type | loan_amt_30 | loan_amt_90 | loan_amt_180 |
| --- | --- | --- | --- | --- | --- |
| 2024-03-31 | mthly | API | 39.44977877430019 | 40.69985272550023 | 42.642388743200264 |
| 2024-02-29 | mthly | APP复贷 | 71.63382141860028 | 73.88702738890035 | 77.01463771080033 |
| 2024-06-30 | mthly | APP复贷 | 90.07300340219967 | 92.08394419509972 | 95.05535688219973 |
| 2024-05-31 | mthly | APP首贷 | 12.733329153100005 | 13.068081589400013 | 13.726104438400018 |
| 2024-04-30 | mthly | API | 40.9943649420001 | 42.176884343700145 | 44.12736553530012 |

### 同步来源
- `odps`
