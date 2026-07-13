# xyf_ads.ads_user_market_portfolio_label_df

## 来源文件
- 老客月会sql代码.ipynb

- `CASE WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) <= 30 THEN '高_day30' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) BETWEEN 30 AND 90 THEN '中_day30_90' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) BETWEEN 90 AND 360 THEN '低_day90_360' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) > 360 THEN '睡眠_day360+' END AS apply_active_last_apply`
- `CASE WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) <= 30 THEN '高_day30' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) BETWEEN 30 AND 90 THEN '中_day30_90' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) BETWEEN 90 AND 360 THEN '低_day90_360' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) > 360 THEN '睡眠_day360+' END AS login_active_last_login`
- `CASE WHEN b_card_model IS NULL OR b_card_model < 0 THEN '空' WHEN b_card_model < 3 THEN 'AB' WHEN b_card_model < 5 THEN 'CD' WHEN b_card_model < 7 THEN 'EF' WHEN b_card_model < 9 THEN 'GH' ELSE 'IJK' END AS b_card_category`
- `CASE WHEN customer_pool IN ('API首贷池','API复贷池') THEN 'API' WHEN customer_pool IN ('APP首贷池','APP复贷池') THEN 'APP' END AS api_app_pool`
- `CASE WHEN regulation_reason IN ('不管制' ) THEN '可发标' WHEN regulation_reason IN ('可用额度低于500','禁申') THEN '可经营不可发标' WHEN regulation_reason NOT IN ('不管制' ,'可用额度低于500','禁申','可用额度低于1k') THEN '不可经营' END AS regulation_type`
- `CASE WHEN regulation_reason IN ('不管制' ) THEN '可发标' WHEN regulation_reason IN ('可用额度低于500','禁申','可用额度低于1k') THEN '可经营不可发标' WHEN regulation_reason NOT IN ('不管制' ,'可用额度低于500','禁申') THEN '不可经营' END AS regulation_type`
- `substr(last_login_time,1,7) AS login_mth`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| user_no | BIGINT | column | 用户号 cis系统 app+mobile | Y |
| cust_no | STRING | column | 客户号 |  |
| id_card_number | STRING | column | 身份证 |  |
| regulation_reason | STRING | column | 客户管制情况 | Y |
| customer_pool | STRING | column | 客群池 | Y |
| cust_loan_status | STRING | column | 在贷结清 |  |
| test_group | STRING | column | 组别 |  |
| first_loan_inner_app | STRING | column | 首贷inner_app |  |
| first_loan_appi | STRING | column | 首贷inner_appi |  |
| last_loan_inner_app | STRING | column | 最近一次inner_app |  |
| first_apply_time | DATETIME | column | 首次发标日期 |  |
| last_apply_time | DATETIME | column | 最近发标日期 | Y |
| first_loan_time | DATETIME | column | 首次放款日期 |  |
| last_loan_time | DATETIME | column | 最近放款日期 |  |
| dis_first_apply_flag | STRING | column | 距发标GAP_flag |  |
| dis_first_loan_flag | STRING | column | 距首贷GAP_flag |  |
| rej_flag_recent_30d | BIGINT | column | 近30天是否被拒 |  |
| b_card_model | DECIMAL(38,18) | column | B卡分 | Y |
| xyl_score | DOUBLE | column | 响应分 |  |
| last_login_time | DATETIME | column | 最近一次登录时间 | Y |
| login_cnt_30d | BIGINT | column | 近30天登录次数 |  |
| login_days_30d | BIGINT | column | 近30天登录天数 |  |
| loan_cnt | BIGINT | column | 订单总数 |  |
| pay_order_cnt | BIGINT | column | 结清订单数 |  |
| recent_date_due | DATETIME | column | 最近账单日期 |  |
| last_date_due | DATETIME | column | 最晚账单到期日 |  |
| first_credit_time | DATETIME | column | 首次授信日期 |  |
| first_activation_line_amt | DECIMAL(38,18) | column | 初始授信额度，单位：元 |  |
| last_activation_line_amt | DECIMAL(38,18) | column | 当前授信额度，单位：元 |  |
| last_increased_time | DATETIME | column | 最近提额时间 |  |
| last_manage_type | STRING | column | 最近提额类型 |  |
| available_amt | DECIMAL(38,18) | column | 可用额度，单位：元 |  |
| temporary_amt | DECIMAL(38,18) | column | 临时额度，单位：元 |  |
| line_used_amt | DECIMAL(38,18) | column | 已用额度，单位：元 |  |
| t30_inlist_tele | BIGINT | column | 近30天人工电销入库次数 |  |
| t30_call_tele | BIGINT | column | 近30天人工电销拨打次数 |  |
| t30_answer_tele | BIGINT | column | 近30天人工电销接通次数 |  |
| t30_inlist_ai | BIGINT | column | 近30天人工AI入库次数 |  |
| t30_call_ai | BIGINT | column | 近30天人工AI拨打次数 |  |
| t30_answer_ai | BIGINT | column | 近30天人工AI接通次数 |  |
| last_sms_reach_time | DATETIME | column | 最近短信触达日期 |  |
| sms_reach_cnt_7d | BIGINT | column | 近7天短信触达量 |  |
| sms_reach_cnt_30d | BIGINT | column | 近30天短信触达量 |  |
| overdue_days | BIGINT | column | 逾期天数 |  |
| overdue_nums | BIGINT | column | 逾期订单数 |  |
| is_advance_settle | BIGINT | column | 是否提前结清 |  |
| settle_time | DATETIME | column | 结清时间 |  |
| pt | STRING | column | [AI推测] 分区日期（yyyyMMdd格式） | Y |
| pt | STRING | partition | [AI推测] 分区日期（yyyyMMdd格式） | Y |

#### DDL
```sql
CREATE TABLE xyf_ads.`ads_user_market_portfolio_label_df` (
  `user_no` BIGINT COMMENT '用户号 cis系统 app+mobile',
  `cust_no` STRING COMMENT '客户号',
  `id_card_number` STRING COMMENT '身份证',
  `regulation_reason` STRING COMMENT '客户管制情况',
  `customer_pool` STRING COMMENT '客群池',
  `cust_loan_status` STRING COMMENT '在贷结清',
  `test_group` STRING COMMENT '组别',
  `first_loan_inner_app` STRING COMMENT '首贷inner_app',
  `first_loan_appi` STRING COMMENT '首贷inner_appi',
  `last_loan_inner_app` STRING COMMENT '最近一次inner_app',
  `first_apply_time` DATETIME COMMENT '首次发标日期',
  `last_apply_time` DATETIME COMMENT '最近发标日期',
  `first_loan_time` DATETIME COMMENT '首次放款日期',
  `last_loan_time` DATETIME COMMENT '最近放款日期',
  `dis_first_apply_flag` STRING COMMENT '距发标GAP_flag',
  `dis_first_loan_flag` STRING COMMENT '距首贷GAP_flag',
  `rej_flag_recent_30d` BIGINT COMMENT '近30天是否被拒',
  `b_card_model` DECIMAL(38,18) COMMENT 'B卡分',
  `xyl_score` DOUBLE COMMENT '响应分',
  `last_login_time` DATETIME COMMENT '最近一次登录时间',
  `login_cnt_30d` BIGINT COMMENT '近30天登录次数',
  `login_days_30d` BIGINT COMMENT '近30天登录天数',
  `loan_cnt` BIGINT COMMENT '订单总数',
  `pay_order_cnt` BIGINT COMMENT '结清订单数',
  `recent_date_due` DATETIME COMMENT '最近账单日期',
  `last_date_due` DATETIME COMMENT '最晚账单到期日',
  `first_credit_time` DATETIME COMMENT '首次授信日期',
  `first_activation_line_amt` DECIMAL(38,18) COMMENT '初始授信额度，单位：元',
  `last_activation_line_amt` DECIMAL(38,18) COMMENT '当前授信额度，单位：元',
  `last_increased_time` DATETIME COMMENT '最近提额时间',
  `last_manage_type` STRING COMMENT '最近提额类型',
  `available_amt` DECIMAL(38,18) COMMENT '可用额度，单位：元',
  `temporary_amt` DECIMAL(38,18) COMMENT '临时额度，单位：元',
  `line_used_amt` DECIMAL(38,18) COMMENT '已用额度，单位：元',
  `t30_inlist_tele` BIGINT COMMENT '近30天人工电销入库次数',
  `t30_call_tele` BIGINT COMMENT '近30天人工电销拨打次数',
  `t30_answer_tele` BIGINT COMMENT '近30天人工电销接通次数',
  `t30_inlist_ai` BIGINT COMMENT '近30天人工AI入库次数',
  `t30_call_ai` BIGINT COMMENT '近30天人工AI拨打次数',
  `t30_answer_ai` BIGINT COMMENT '近30天人工AI接通次数',
  `last_sms_reach_time` DATETIME COMMENT '最近短信触达日期',
  `sms_reach_cnt_7d` BIGINT COMMENT '近7天短信触达量',
  `sms_reach_cnt_30d` BIGINT COMMENT '近30天短信触达量',
  `overdue_days` BIGINT COMMENT '逾期天数',
  `overdue_nums` BIGINT COMMENT '逾期订单数',
  `is_advance_settle` BIGINT COMMENT '是否提前结清',
  `settle_time` DATETIME COMMENT '结清时间'
)
COMMENT '老客客群池表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 720
```

### 抽样数据
| user_no | cust_no | id_card_number | regulation_reason | customer_pool | cust_loan_status | test_group | first_loan_inner_app | first_loan_appi | last_loan_inner_app | first_apply_time | last_apply_time | first_loan_time | last_loan_time | dis_first_apply_flag | dis_first_loan_flag | rej_flag_recent_30d | b_card_model | xyl_score | last_login_time | login_cnt_30d | login_days_30d | loan_cnt | pay_order_cnt | recent_date_due | last_date_due | first_credit_time | first_activation_line_amt | last_activation_line_amt | last_increased_time | last_manage_type | available_amt | temporary_amt | line_used_amt | t30_inlist_tele | t30_call_tele | t30_answer_tele | t30_inlist_ai | t30_call_ai | t30_answer_ai | last_sms_reach_time | sms_reach_cnt_7d | sms_reach_cnt_30d | overdue_days | overdue_nums | is_advance_settle | settle_time | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1003155341 | CTL07b25487cfdc9c38b2df86fd29f832ba5 | iVwNnJ4G0MV+K8GctFyoPi+8U9U+WTRapzsmDDdrlGI= | 可用额度低于1k | APP复贷池 | 在贷 | 人工营销组(11_99) | fxk_h5 | API | fxk | 2021-02-28 18:51:46 | 2023-12-19 17:14:52 | 2021-02-28 18:54:08 | 2023-12-19 17:36:08 | MOB11+ | MOB11+ | 0 | 9 | 10.0 | 2024-01-10 18:21:22 | 22 | 11 | 12 | 8 | 2024-01-17 00:00:00 | 2024-10-19 00:00:00 | 2021-02-28 18:50:12 | 6000 | 20000 |  |  | -3612.95 | 0 | 17812.95 | 0 | 0 | 0 | 0 | 0 | 0 | 2023-08-12 10:03:32 | 0 | 0 | 274 | 6 | 0 |  | 20240115 | 20240115 |
| 1003228337 | CTL06969017f0476e72fe0aad9f93fbf2902 | ADSFw/NRnthfFbwkxs/SUz7at8xa+eOCkkjmrhok+LM= | 不管制 | APP复贷池 | 结清 | 人工营销组(11_99) | fxk_rs | API | fxk | 2021-03-10 16:33:49 | 2022-07-23 17:17:01 | 2021-03-10 16:36:18 | 2022-05-28 14:21:05 | MOB11+ | MOB11+ | 0 | 9 | 10.0 | 2022-08-05 14:25:55 | 0 | 0 | 3 | 3 |  |  | 2021-03-10 16:31:42 | 9000 | 16100 |  |  | 16100 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2023-10-20 21:55:02 | 0 | 0 |  | 0 | 1 | 2022-08-05 14:35:20 | 20240115 | 20240115 |
| 1003261237 | CTL09d9a365e976ea502a41217f0d35fd3b1 | vyCgf+kZrJgj7+nj8V1AAqppk2T0MenaeSjnusABWGY= | 黑名单 | API首贷池 | 结清 | 人工营销组(11_99) | fxk_jqns02 | API | fxk_jqns02 | 2022-01-26 16:17:54 | 2023-10-20 18:41:54 | 2022-01-27 03:08:28 | 2022-01-27 03:08:28 | MOB11+ | MOB11+ | 0 | 10 | 10.0 | 2023-10-29 00:00:56 | 0 | 0 | 1 | 1 |  |  | 2021-12-10 17:19:51 | 10000 | 12600 |  |  | 12600 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2023-11-03 16:05:17 | 0 | 0 | 687 | 1 | 0 | 2023-01-28 22:23:48 | 20240115 | 20240115 |
| 1003299929 | CTL00f159067961037314d0fee273e0af289 | 4p8jY4SJC9N8RXb9P9nO59BpWbKHvuIuDbbXXBCg++Q= | 不管制 | APP复贷池 | 结清 | 人工营销组(11_99) | fxk_jqns03 | API | fxk | 2022-06-24 11:14:26 | 2023-04-05 15:53:16 | 2022-06-24 11:31:37 | 2023-01-10 07:36:06 | MOB11+ | MOB11+ | 0 | 10 | 10.0 | 2024-01-10 07:24:44 | 5 | 3 | 2 | 2 |  |  | 2021-11-02 15:16:14 | 9000 | 12500 |  |  | 12500 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 2023-10-20 09:24:12 | 0 | 0 |  | 0 | 0 | 2024-01-10 08:06:51 | 20240115 | 20240115 |
| 1003525801 | CTL03043d18a1312efca808dac199422ec5a | 7bQqA7GPay67ZbwVzQKVLxzVwBDhsOijwBW7FXWQk2U= | 不管制 | API首贷池 | 结清 | 人工营销组(11_99) | fxk_58jr | API | fxk_58jr | 2022-09-30 10:13:57 | 2023-11-10 23:47:40 | 2022-09-30 11:12:02 | 2022-09-30 11:12:02 | MOB11+ | MOB11+ | 0 | 10 | 1.0 | 2023-12-29 02:24:05 | 2 | 1 | 1 | 1 |  |  | 2020-04-05 14:41:07 | 12000 | 24062.5 |  |  | 15400 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  | 0 | 1 | 2023-08-18 11:22:09 | 20240115 | 20240115 |

### 同步来源
- `odps`
