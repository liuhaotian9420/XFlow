# xyf_dws.dws_inloan_loan_risk_stat_df

## 来源文件
- ads_inloan_loan_monitor_screen_df.sql

- `nvl(t3.act_first_api_p_asset,0) + nvl(t3.act_added_api_p_asset,0) + nvl(t3.act_first_app_p_asset,0) + nvl(t3.act_added_p_asset,0) AS day_asset_amt`
- `t3.act_added_api_p_asset AS day_asset_amt`
- `t3.act_added_p_asset AS day_asset_amt`
- `t3.act_first_api_p_asset AS day_asset_amt`
- `t3.act_first_app_p_asset AS day_asset_amt`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_date | STRING | column | 订单申请时间 | Y |
| act_first_api_p_asset | DECIMAL(38,18) | column | 个人API首贷资产金额 | Y |
| act_added_api_p_asset | DECIMAL(38,18) | column | 个人API复贷资产金额 | Y |
| act_first_app_p_asset | DECIMAL(38,18) | column | 个人APP首贷(新)资产金额 | Y |
| act_added_p_asset | DECIMAL(38,18) | column | 个人APP复贷资产金额 | Y |
| pt | STRING | column | 分区日期 | Y |
| pt | STRING | partition | 分区日期 | Y |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_inloan_loan_risk_stat_df` (
  `order_date` STRING COMMENT '订单申请时间',
  `act_first_api_p_asset` DECIMAL(38,18) COMMENT '个人API首贷资产金额',
  `act_added_api_p_asset` DECIMAL(38,18) COMMENT '个人API复贷资产金额',
  `act_first_app_p_asset` DECIMAL(38,18) COMMENT '个人APP首贷(新)资产金额',
  `act_added_p_asset` DECIMAL(38,18) COMMENT '个人APP复贷资产金额'
)
COMMENT '每日资产放款统计表'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '分区日期'
)
STORED AS AliOrc
LIFECYCLE 30
```

### 抽样数据
| order_date | act_first_api_p_asset | act_added_api_p_asset | act_first_app_p_asset | act_added_p_asset | pt | pt |
| --- | --- | --- | --- | --- | --- | --- |
| 2025-01-12 | 0.606576 | 0.048872 | 0.326687 | 1.353309 | 20260227 | 20260227 |
| 2026-02-10 | 0.180458 | 0.011802 | 0.48743 | 1.734432 | 20260227 | 20260227 |
| 2025-06-12 | 0.51886 | 0.042054 | 0.245013 | 1.588556 | 20260227 | 20260227 |
| 2025-05-30 | 0.669674 | 0.044782 | 0.27819 | 1.486187 | 20260227 | 20260227 |
| 2025-01-14 | 0.707574 | 0.055041 | 0.384163 | 1.61367 | 20260227 | 20260227 |

### 同步来源
- `odps`
