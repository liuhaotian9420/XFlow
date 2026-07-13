# xyf_ads.ads_inloan_loan_monitor_screen_df

## 来源文件
- ads_inloan_loan_pass_monitor_df.sql

- `CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)' WHEN flag IN ('APP放款') THEN '老客_APP放款' ELSE flag END AS flag`
- `IF(SUM(day_loan_cnt) = 0,0,SUM(day_loan_amt) / SUM(day_loan_cnt) * 100000000) 放款件均`
- `loan_date AS pay_date`
- `stat_type AS date_type`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| stat_type | STRING | column | 统计口径 | Y |
| loan_date | STRING | column | 放款日期 | Y |
| flag | STRING | column | 放款渠道 | Y |
| day_loan_amt | DECIMAL(38,18) | column | 日放款金额 | Y |
| day_loan_cnt | DOUBLE | column | 日订单数 | Y |
| month_loan_amt | DECIMAL(38,18) | column | 月累计放款 |  |
| target_point | DECIMAL(38,18) | column | 目标 |  |
| month_loan_num | BIGINT | column | 月放款人数 |  |
| day_asset_amt | DECIMAL(38,18) | column | 每日资产金额 |  |

#### DDL
```sql
CREATE TABLE xyf_ads.`ads_inloan_loan_monitor_screen_df` (
  `stat_type` STRING COMMENT '统计口径',
  `loan_date` STRING COMMENT '放款日期',
  `flag` STRING COMMENT '放款渠道',
  `day_loan_amt` DECIMAL(38,18) COMMENT '日放款金额',
  `day_loan_cnt` DOUBLE COMMENT '日订单数',
  `month_loan_amt` DECIMAL(38,18) COMMENT '月累计放款',
  `target_point` DECIMAL(38,18) COMMENT '目标',
  `month_loan_num` BIGINT COMMENT '月放款人数',
  `day_asset_amt` DECIMAL(38,18) COMMENT '每日资产金额'
)
COMMENT '大盘放款量级监控日报-邮件任务'
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| stat_type | loan_date | flag | day_loan_amt | day_loan_cnt | month_loan_amt | target_point | month_loan_num | day_asset_amt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mthly_summary | 2025-01-31 | 老客总体 | 1.526116032258064516 | 41388.0 | 47.309597 | 45.690000000000000004 | 873641 |  |
| mthly_summary | 2025-02-28 | 老客总体 | 1.5841845 | 43403.857142857145 | 44.357166 | 41.290000000000000004 | 860981 |  |
| mthly_summary | 2025-03-31 | 老客总体 | 1.845644096774193548 | 50543.51612903226 | 57.214967 | 47.42000000000000001 | 1065264 |  |
| mthly_summary | 2025-04-30 | 老客总体 | 1.994991933333333333 | 51334.0 | 59.849758 | 50.81000000000000001 | 1053581 |  |
| mthly_summary | 2025-05-31 | 老客总体 | 1.79072841935483871 | 42405.1935483871 | 55.512581 | 54.25999999999999999 | 955768 |  |

### 同步来源
- `odps`
