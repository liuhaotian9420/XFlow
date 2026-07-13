# xyf_dws.dws_inloan_loan_channel_stat_df

## 来源文件
- ads_inloan_loan_monitor_screen_df.sql

- `'APP放款' AS flag`
- `'APP首贷（API授信）' AS flag`
- `'APP首贷（API首贷）' AS flag`
- `'APP首贷（APP授信）' AS flag`
- `'current_mth' AS stat_type`
- `'新客总体' AS flag`
- `'老客总体' AS flag`
- `0 AS month_loan_num`
- `0 AS target_point`
- `COALESCE(act_added_p,0) + COALESCE(act_a24_p,0) - act_added_apitoapp_p AS day_loan_amt`
- `COALESCE(act_added_p_ord,0) + COALESCE(act_a24_p_ord,0) - act_added_apitoapp_p_ord AS day_loan_cnt`
- `COALESCE(b.cum_act_a24_p,0) AS cum_act_a24_p`
- `COALESCE(b.cum_act_a24_p_ord,0) AS cum_act_a24_p_ord`
- `COALESCE(b.cum_act_added_api_p,0) AS cum_act_added_api_p`
- `COALESCE(b.cum_act_added_api_p_ord,0) AS cum_act_added_api_p_ord`
- `COALESCE(b.cum_act_added_apitoapp_p,0) AS cum_act_added_apitoapp_p`
- `COALESCE(b.cum_act_added_apitoapp_p_ord,0) AS cum_act_added_apitoapp_p_ord`
- `COALESCE(b.cum_act_added_c,0) AS cum_act_added_c`
- `COALESCE(b.cum_act_added_c_ord,0) AS cum_act_added_c_ord`
- `COALESCE(b.cum_act_added_p,0) AS cum_act_added_p`
- `COALESCE(b.cum_act_added_p_ord,0) AS cum_act_added_p_ord`
- `COALESCE(b.cum_act_first_api_p,0) AS cum_act_first_api_p`
- `COALESCE(b.cum_act_first_api_p_ord,0) AS cum_act_first_api_p_ord`
- `COALESCE(b.cum_act_first_apitoapp_p,0) AS cum_act_first_apitoapp_p`
- `COALESCE(b.cum_act_first_apitoapp_p_ord,0) AS cum_act_first_apitoapp_p_ord`
- `COALESCE(b.cum_act_first_dx_p,0) AS cum_act_first_dx_p`
- `COALESCE(b.cum_act_first_dx_p_ord,0) AS cum_act_first_dx_p_ord`
- `COALESCE(b.cum_act_first_other_p,0) AS cum_act_first_other_p`
- `COALESCE(b.cum_act_first_other_p_ord,0) AS cum_act_first_other_p_ord`
- `COALESCE(b.cum_act_first_xxl_p,0) AS cum_act_first_xxl_p`
- `COALESCE(b.cum_act_first_xxl_p_ord,0) AS cum_act_first_xxl_p_ord`
- `COALESCE(b.cum_day_target_a24,0) AS cum_day_target_a24`
- `COALESCE(b.cum_day_target_added_c,0) AS cum_day_target_added_c`
- `COALESCE(b.cum_day_target_added_p,0) AS cum_day_target_added_p`
- `COALESCE(b.cum_day_target_first_api_p,0) AS cum_day_target_first_api_p`
- `COALESCE(b.cum_day_target_first_apitoapp,0) AS cum_day_target_first_apitoapp`
- `COALESCE(b.cum_day_target_first_app_p,0) AS cum_day_target_first_app_p`
- `COALESCE(t1.act_added_p,0) + COALESCE(t1.act_a24_p,0) AS day_loan_amt`
- `COALESCE(t1.act_added_p_ord,0) + COALESCE(t1.act_a24_p_ord,0) AS day_loan_cnt`
- `COALESCE(t1.act_first_api_p,0) + COALESCE(t1.act_added_api_p,0) + COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0) + COALESCE(t1.act_first_apitoapp_p,0) AS day_loan_amt`
- `COALESCE(t1.act_first_api_p_ord,0) + COALESCE(t1.act_added_api_p_ord,0) + COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0) + COALESCE(t1.act_first_apitoapp_p_ord,0) AS day_loan_cnt`
- `COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0) AS day_loan_amt`
- `COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0) AS day_loan_cnt`
- `NULL AS day_asset_amt`
- `act_added_apitoapp_p AS day_loan_amt`
- `act_added_apitoapp_p_ord AS day_loan_cnt`
- `act_first_apitoapp_p AS day_loan_amt`
- `act_first_apitoapp_p_ord AS day_loan_cnt`
- `cum_act_added_apitoapp_p AS month_loan_amt`
- `cum_act_added_p + cum_act_a24_p - cum_act_added_apitoapp_p AS month_loan_amt`
- `cum_act_first_apitoapp_p AS month_loan_amt`
- `cum_day_target_added_apitoapp AS target_point`
- `cum_day_target_first_apitoapp AS target_point`
- `t1.cum_act_added_p + t1.cum_act_a24_p AS month_loan_amt`
- `t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p AS month_loan_amt`
- `t2.added_tgt AS target_point`
- `t2.first_app_tgt AS target_point`
- `t2.total_first_tgt AS target_point`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| loan_date | STRING | column | 借款日期 | Y |
| act_first_api_p | DECIMAL(38,18) | column | 个人API首贷金额 |  |
| act_added_api_p | DECIMAL(38,18) | column | 个人API复贷金额 |  |
| act_first_app_p | DECIMAL(38,18) | column | 个人APP首贷金额 |  |
| act_first_dx_p | DECIMAL(38,18) | column | 个人APP首贷_短信金额 |  |
| act_first_xxl_p | DECIMAL(38,18) | column | 个人APP首贷_信息流金额 |  |
| act_first_other_p | DECIMAL(38,18) | column | 个人APP首贷_其他金额 |  |
| act_first_apitoapp_p | DECIMAL(38,18) | column | 个人APP首贷API首贷金额 | Y |
| act_added_p | DECIMAL(38,18) | column | 个人APP复贷金额 | Y |
| act_a24_p | BIGINT | column | 废弃，默认为0 | Y |
| act_added_apitoapp_p | DECIMAL(38,18) | column | 个人APP复贷API复贷金额 | Y |
| act_added_c | DOUBLE | column | 现金贷(畅行花)金额 |  |
| act_first_api_p_ord | BIGINT | column | 个人API首贷订单量 |  |
| act_added_api_p_ord | BIGINT | column | 个人API复贷订单量 |  |
| act_first_app_p_ord | BIGINT | column | 个人APP首贷订单量 |  |
| act_first_dx_p_ord | BIGINT | column | 个人APP首贷_短信订单量 |  |
| act_first_xxl_p_ord | BIGINT | column | 个人APP首贷_信息流订单量 |  |
| act_first_other_p_ord | BIGINT | column | 个人APP首贷_其他订单量 |  |
| act_first_apitoapp_p_ord | BIGINT | column | 个人APP首贷API首贷订单量 | Y |
| act_added_p_ord | BIGINT | column | 个人APP复贷订单量 | Y |
| act_a24_p_ord | BIGINT | column | 废弃，默认为0 | Y |
| act_added_apitoapp_p_ord | BIGINT | column | 个人APP复贷API复贷订单量 | Y |
| act_added_c_ord | DOUBLE | column | 现金贷(畅行花)订单量 |  |
| cum_act_first_api_p | DECIMAL(38,18) | column | 累计个人API首贷金额 | Y |
| cum_act_added_api_p | DECIMAL(38,18) | column | 累计个人API复贷金额 | Y |
| cum_act_first_app_p | DECIMAL(38,18) | column | 累计个人APP首贷金额 | Y |
| cum_act_first_dx_p | DECIMAL(38,18) | column | 累计个人APP首贷_短信金额 | Y |
| cum_act_first_xxl_p | DECIMAL(38,18) | column | 累计个人APP首贷_信息流金额 | Y |
| cum_act_first_other_p | DECIMAL(38,18) | column | 累计个人APP首贷_其他金额 | Y |
| cum_act_first_apitoapp_p | DECIMAL(38,18) | column | 累计个人APP首贷API首贷金额 | Y |
| cum_act_added_p | DECIMAL(38,18) | column | 累计个人APP复贷金额 | Y |
| cum_act_a24_p | BIGINT | column | 废弃，默认为0 | Y |
| cum_act_added_apitoapp_p | DECIMAL(38,18) | column | 累计个人APP复贷API复贷金额 | Y |
| cum_act_added_c | DOUBLE | column | 累计现金贷(畅行花)金额 | Y |
| cum_act_first_api_p_ord | BIGINT | column | 累计个人API首贷订单量 | Y |
| cum_act_added_api_p_ord | BIGINT | column | 累计个人API复贷订单量 | Y |
| cum_act_first_app_p_ord | BIGINT | column | 累计个人APP首贷订单量 | Y |
| cum_act_first_dx_p_ord | BIGINT | column | 累计个人APP首贷_短信订单量 | Y |
| cum_act_first_xxl_p_ord | BIGINT | column | 累计个人APP首贷_信息流订单量 | Y |
| cum_act_first_other_p_ord | BIGINT | column | 累计个人APP首贷_其他订单量 | Y |
| cum_act_first_apitoapp_p_ord | BIGINT | column | 累计个人APP首贷API首贷订单量 | Y |
| cum_act_added_p_ord | BIGINT | column | 累计个人APP复贷订单量 | Y |
| cum_act_a24_p_ord | BIGINT | column | 废弃，默认为0 | Y |
| cum_act_added_apitoapp_p_ord | BIGINT | column | 累计个人APP复贷API复贷订单量 | Y |
| cum_act_added_c_ord | DOUBLE | column | 累计现金贷(畅行花)订单量 | Y |
| cum_day_target_first_api_p | DECIMAL(38,18) | column | 累计个人_首贷API目标金额 | Y |
| cum_day_target_first_app_p | DECIMAL(38,18) | column | 累计个人_首贷APP目标金额 | Y |
| cum_day_target_first_xxl_p | DECIMAL(38,18) | column | 累计个人_信息流目标金额 |  |
| cum_day_target_first_dx_p | DECIMAL(38,18) | column | 累计个人_短信目标金额 |  |
| cum_day_target_first_other_p | DECIMAL(38,18) | column | 累计个人_其他-付费目标金额 |  |
| cum_day_target_first_other_p_free | DECIMAL(38,18) | column | 累计个人_其他目标金额 |  |
| cum_day_target_added_p | DECIMAL(38,18) | column | 累计个人_复贷目标金额 | Y |
| cum_day_target_total_p | DECIMAL(38,18) | column | 累计个人_分期整体目标金额 |  |
| cum_day_target_a24 | DECIMAL(38,18) | column | 累计下探_复贷A24目标金额 | Y |
| cum_day_target_added_c | DECIMAL(38,18) | column | 累计现金_复贷目标金额 | Y |
| cum_day_target_first_api | DECIMAL(38,18) | column | 累计整体_首贷API目标金额 |  |
| cum_day_target_first_app | DECIMAL(38,18) | column | 累计整体_首贷APP目标金额 |  |
| cum_day_target_first_xxl | DECIMAL(38,18) | column | 累计整体_信息流目标金额 |  |
| cum_day_target_first_dx | DECIMAL(38,18) | column | 累计整体_短信目标金额 |  |
| cum_day_target_first_other | DECIMAL(38,18) | column | 累计整体_其他目标金额 |  |
| cum_day_target_added | DECIMAL(38,18) | column | 累计整体_复贷目标金额 |  |
| cum_day_target_total | DECIMAL(38,18) | column | 累计整体目标金额 |  |
| cum_day_target_first_apitoapp | DECIMAL(38,18) | column | 累计个人_APItoAPP首贷目标金额 | Y |
| cum_day_target_added_apitoapp | DECIMAL(38,18) | column | 累计个人_APItoAPP复贷目标金额 | Y |
| pt | STRING | column | 分区日期 | Y |
| pt | STRING | partition | 分区日期 | Y |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_inloan_loan_channel_stat_df` (
  `loan_date` STRING COMMENT '借款日期',
  `act_first_api_p` DECIMAL(38,18) COMMENT '个人API首贷金额',
  `act_added_api_p` DECIMAL(38,18) COMMENT '个人API复贷金额',
  `act_first_app_p` DECIMAL(38,18) COMMENT '个人APP首贷金额',
  `act_first_dx_p` DECIMAL(38,18) COMMENT '个人APP首贷_短信金额',
  `act_first_xxl_p` DECIMAL(38,18) COMMENT '个人APP首贷_信息流金额',
  `act_first_other_p` DECIMAL(38,18) COMMENT '个人APP首贷_其他金额',
  `act_first_apitoapp_p` DECIMAL(38,18) COMMENT '个人APP首贷API首贷金额',
  `act_added_p` DECIMAL(38,18) COMMENT '个人APP复贷金额',
  `act_a24_p` BIGINT COMMENT '废弃，默认为0',
  `act_added_apitoapp_p` DECIMAL(38,18) COMMENT '个人APP复贷API复贷金额',
  `act_added_c` DOUBLE COMMENT '现金贷(畅行花)金额',
  `act_first_api_p_ord` BIGINT COMMENT '个人API首贷订单量',
  `act_added_api_p_ord` BIGINT COMMENT '个人API复贷订单量',
  `act_first_app_p_ord` BIGINT COMMENT '个人APP首贷订单量',
  `act_first_dx_p_ord` BIGINT COMMENT '个人APP首贷_短信订单量',
  `act_first_xxl_p_ord` BIGINT COMMENT '个人APP首贷_信息流订单量',
  `act_first_other_p_ord` BIGINT COMMENT '个人APP首贷_其他订单量',
  `act_first_apitoapp_p_ord` BIGINT COMMENT '个人APP首贷API首贷订单量',
  `act_added_p_ord` BIGINT COMMENT '个人APP复贷订单量',
  `act_a24_p_ord` BIGINT COMMENT '废弃，默认为0',
  `act_added_apitoapp_p_ord` BIGINT COMMENT '个人APP复贷API复贷订单量',
  `act_added_c_ord` DOUBLE COMMENT '现金贷(畅行花)订单量',
  `cum_act_first_api_p` DECIMAL(38,18) COMMENT '累计个人API首贷金额',
  `cum_act_added_api_p` DECIMAL(38,18) COMMENT '累计个人API复贷金额',
  `cum_act_first_app_p` DECIMAL(38,18) COMMENT '累计个人APP首贷金额',
  `cum_act_first_dx_p` DECIMAL(38,18) COMMENT '累计个人APP首贷_短信金额',
  `cum_act_first_xxl_p` DECIMAL(38,18) COMMENT '累计个人APP首贷_信息流金额',
  `cum_act_first_other_p` DECIMAL(38,18) COMMENT '累计个人APP首贷_其他金额',
  `cum_act_first_apitoapp_p` DECIMAL(38,18) COMMENT '累计个人APP首贷API首贷金额',
  `cum_act_added_p` DECIMAL(38,18) COMMENT '累计个人APP复贷金额',
  `cum_act_a24_p` BIGINT COMMENT '废弃，默认为0',
  `cum_act_added_apitoapp_p` DECIMAL(38,18) COMMENT '累计个人APP复贷API复贷金额',
  `cum_act_added_c` DOUBLE COMMENT '累计现金贷(畅行花)金额',
  `cum_act_first_api_p_ord` BIGINT COMMENT '累计个人API首贷订单量',
  `cum_act_added_api_p_ord` BIGINT COMMENT '累计个人API复贷订单量',
  `cum_act_first_app_p_ord` BIGINT COMMENT '累计个人APP首贷订单量',
  `cum_act_first_dx_p_ord` BIGINT COMMENT '累计个人APP首贷_短信订单量',
  `cum_act_first_xxl_p_ord` BIGINT COMMENT '累计个人APP首贷_信息流订单量',
  `cum_act_first_other_p_ord` BIGINT COMMENT '累计个人APP首贷_其他订单量',
  `cum_act_first_apitoapp_p_ord` BIGINT COMMENT '累计个人APP首贷API首贷订单量',
  `cum_act_added_p_ord` BIGINT COMMENT '累计个人APP复贷订单量',
  `cum_act_a24_p_ord` BIGINT COMMENT '废弃，默认为0',
  `cum_act_added_apitoapp_p_ord` BIGINT COMMENT '累计个人APP复贷API复贷订单量',
  `cum_act_added_c_ord` DOUBLE COMMENT '累计现金贷(畅行花)订单量',
  `cum_day_target_first_api_p` DECIMAL(38,18) COMMENT '累计个人_首贷API目标金额',
  `cum_day_target_first_app_p` DECIMAL(38,18) COMMENT '累计个人_首贷APP目标金额',
  `cum_day_target_first_xxl_p` DECIMAL(38,18) COMMENT '累计个人_信息流目标金额',
  `cum_day_target_first_dx_p` DECIMAL(38,18) COMMENT '累计个人_短信目标金额',
  `cum_day_target_first_other_p` DECIMAL(38,18) COMMENT '累计个人_其他-付费目标金额',
  `cum_day_target_first_other_p_free` DECIMAL(38,18) COMMENT '累计个人_其他目标金额',
  `cum_day_target_added_p` DECIMAL(38,18) COMMENT '累计个人_复贷目标金额',
  `cum_day_target_total_p` DECIMAL(38,18) COMMENT '累计个人_分期整体目标金额',
  `cum_day_target_a24` DECIMAL(38,18) COMMENT '累计下探_复贷A24目标金额',
  `cum_day_target_added_c` DECIMAL(38,18) COMMENT '累计现金_复贷目标金额',
  `cum_day_target_first_api` DECIMAL(38,18) COMMENT '累计整体_首贷API目标金额',
  `cum_day_target_first_app` DECIMAL(38,18) COMMENT '累计整体_首贷APP目标金额',
  `cum_day_target_first_xxl` DECIMAL(38,18) COMMENT '累计整体_信息流目标金额',
  `cum_day_target_first_dx` DECIMAL(38,18) COMMENT '累计整体_短信目标金额',
  `cum_day_target_first_other` DECIMAL(38,18) COMMENT '累计整体_其他目标金额',
  `cum_day_target_added` DECIMAL(38,18) COMMENT '累计整体_复贷目标金额',
  `cum_day_target_total` DECIMAL(38,18) COMMENT '累计整体目标金额',
  `cum_day_target_first_apitoapp` DECIMAL(38,18) COMMENT '累计个人_APItoAPP首贷目标金额',
  `cum_day_target_added_apitoapp` DECIMAL(38,18) COMMENT '累计个人_APItoAPP复贷目标金额'
)
COMMENT '贷中app/api渠道放款量级统计'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '分区日期'
)
STORED AS AliOrc
LIFECYCLE 365
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C671F632E7475A6BE6ABBA Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
