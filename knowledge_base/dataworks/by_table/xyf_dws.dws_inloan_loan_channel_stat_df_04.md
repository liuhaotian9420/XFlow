# xyf_dws.dws_inloan_loan_channel_stat_df_04

## 来源文件
- ads_inloan_loan_monitor_screen_df.sql

- `'APP放款' AS flag`
- `'APP首贷（API授信）' AS flag`
- `'APP首贷（API首贷）' AS flag`
- `'APP首贷（APP授信）' AS flag`
- `'mthly_summary' AS stat_type`
- `'个人API复贷' AS flag`
- `'个人API复贷备份' AS flag`
- `'个人API首贷' AS flag`
- `'个人APP复贷' AS flag`
- `'个人APP首贷（新）' AS flag`
- `'新客总体' AS flag`
- `'老客总体' AS flag`
- `'自营总计' AS flag`
- `'自营总计备份' AS flag`
- `(t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord - t1.cum_act_added_apitoapp_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord + t1.cum_act_first_apitoapp_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `CASE WHEN t1.loan_date < '2024-01-01' THEN t1.cum_day_target_added_p + t1.cum_day_target_a24 - t1.cum_day_target_added_apitoapp ELSE 0 END AS target_point`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c) /DAY(t1.loan_date) ELSE (t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date) END AS day_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p) / DAY(t1.loan_date) END AS day_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN COALESCE(t3.act_added_c_mthly_id,0) + t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id ELSE t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id END AS month_loan_num`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c ELSE t1.cum_act_added_p + t1.cum_act_a24_p END AS month_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p ELSE t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p END AS month_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + COALESCE(t3.act_added_c_mthly_id,0) ELSE (COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0)) END AS month_loan_num`
- `CAST(NULL AS DECIMAL(38,18)) AS target_point`
- `COALESCE(t2.act_added_apitoapp_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) - COALESCE(t2.act_added_apitoapp_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_first_api_p_mthly_id,0) + COALESCE(t2.act_added_api_p_mthly_id,0) + COALESCE(t2.act_first_dx_p_mthly_id,0) + COALESCE(t2.act_first_xxl_p_mthly_id,0) + COALESCE(t2.act_first_other_p_mthly_id,0) + COALESCE(t2.act_first_apitoapp_p_mthly_id,0) AS month_loan_num`
- `NULL AS day_asset_amt`
- `t1.cum_act_added_api_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_added_api_p AS month_loan_amt`
- `t1.cum_act_added_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_added_apitoapp_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_added_apitoapp_p AS month_loan_amt`
- `t1.cum_act_added_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p AS month_loan_amt`
- `t1.cum_act_added_p + t1.cum_act_a24_p AS month_loan_amt`
- `t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_api_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_api_p AS month_loan_amt`
- `t1.cum_act_first_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_apitoapp_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_app_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_app_p AS month_loan_amt`
- `t1.cum_act_first_app_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p AS month_loan_amt`
- `t1.cum_day_target_added_apitoapp AS target_point`
- `t1.cum_day_target_added_c + t1.cum_day_target_added_p + t1.cum_day_target_a24 + t1.cum_day_target_first_app_p + t1.cum_day_target_first_api_p AS target_point`
- `t1.cum_day_target_added_p + t1.cum_day_target_a24 AS target_point`
- `t1.cum_day_target_first_api_p + t1.cum_day_target_first_app_p + t1.cum_day_target_first_apitoapp AS target_point`
- `t1.cum_day_target_first_api_p AS target_point`
- `t1.cum_day_target_first_apitoapp AS target_point`
- `t1.cum_day_target_first_app_p AS target_point`
- `t2.act_added_api_p_mthly_id AS month_loan_num`
- `t2.act_first_api_p_mthly_id AS month_loan_num`
- `t2.act_first_apitoapp_p_mthly_id AS month_loan_num`
- `t2.act_first_app_p_mthly_id AS month_loan_num`
- `t2.act_first_dx_p_mthly_id + t2.act_first_xxl_p_mthly_id + t2.act_first_other_p_mthly_id AS month_loan_num`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| loan_month | STRING | column | [AI推测] 放款月份（yyyy-MM） | Y |
| act_first_api_p_mthly_id | BIGINT | column | [AI推测] 当月API首贷放款笔数 | Y |
| act_added_api_p_mthly_id | BIGINT | column | [AI推测] 当月API加贷放款笔数 | Y |
| act_first_app_p_mthly_id | BIGINT | column | [AI推测] 当月APP首贷放款笔数 | Y |
| act_first_dx_p_mthly_id | BIGINT | column | [AI推测] 当月电销首贷放款笔数 | Y |
| act_first_xxl_p_mthly_id | BIGINT | column | [AI推测] 当月小小贷首贷放款笔数 | Y |
| act_first_other_p_mthly_id | BIGINT | column | [AI推测] 当月其他渠道首贷放款笔数 | Y |
| act_first_apitoapp_p_mthly_id | BIGINT | column | [AI推测] 当月API转APP首贷放款笔数 | Y |
| act_added_p_mthly_id | BIGINT | column | [AI推测] 当月老客加贷放款笔数 | Y |
| act_a24_p_mthly_id | INT | column | [AI推测] 当月A24定价放款笔数 | Y |
| act_added_apitoapp_p_mthly_id | BIGINT | column | [AI推测] 当月API转APP加贷放款笔数 | Y |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_inloan_loan_channel_stat_df_04` (
  `loan_month` STRING,
  `act_first_api_p_mthly_id` BIGINT,
  `act_added_api_p_mthly_id` BIGINT,
  `act_first_app_p_mthly_id` BIGINT,
  `act_first_dx_p_mthly_id` BIGINT,
  `act_first_xxl_p_mthly_id` BIGINT,
  `act_first_other_p_mthly_id` BIGINT,
  `act_first_apitoapp_p_mthly_id` BIGINT,
  `act_added_p_mthly_id` BIGINT,
  `act_a24_p_mthly_id` INT,
  `act_added_apitoapp_p_mthly_id` BIGINT
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| loan_month | act_first_api_p_mthly_id | act_added_api_p_mthly_id | act_first_app_p_mthly_id | act_first_dx_p_mthly_id | act_first_xxl_p_mthly_id | act_first_other_p_mthly_id | act_first_apitoapp_p_mthly_id | act_added_p_mthly_id | act_a24_p_mthly_id | act_added_apitoapp_p_mthly_id |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-05 | 122394 | 162 | 38737 | 11214 | 2706 | 14143 | 7552 | 134180 | 0 | 26671 |
| 2024-06 | 212159 | 9137 | 71059 | 13206 | 24413 | 21554 | 10204 | 420219 | 0 | 115204 |
| 2024-08 | 337745 | 15574 | 101551 | 20729 | 27348 | 33275 | 17887 | 591735 | 0 | 153457 |
| 2025-08 | 92051 | 12130 | 49864 | 1405 | 10313 | 17906 | 19373 | 834614 | 0 | 69093 |
| 2026-03 | 30494 | 2062 | 87046 | 14402 | 9817 | 38144 | 23637 | 533978 | 0 | 33931 |

### 同步来源
- `odps`
