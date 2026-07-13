# xyf_dwd.dwd_inloan_leap_vip_order_hf

## 来源文件
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

- `'leap' AS card_type`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `pay_time AS tran_time`
- `real_card_price AS pay_amt`
- `refund_amount AS refund_amt`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| first_vip_order_number | STRING | column | 本次会员卡订单的首个订单号，在同一个续费期内的first_vip_order_number保持一致 |  |
| vip_order_number | STRING | column | 会员卡订单号，每一次签约都会生成一个订单号 |  |
| renew_period | BIGINT | column | 当前会员卡订单处于第几期，签约时rn=0,第一次续费为1，直到后续再次签约时从新0开始计数 |  |
| first_order_time | DATETIME | column | 本次会员卡订单的首次签约日期 |  |
| order_time | DATETIME | column | 每一次会员卡订单日期 | Y |
| order_from | STRING | column | 会员卡购买入口：lend-before：借款下单前，lend_before_retain：借款下单前-提现页挽留弹窗，vip-center：会员中心，lend-after：借款下单后-借款进度页，lend_after_retain：借款下单后-卡单页挽留弹窗，system：系统下单-自动续约，lend_stuck：风控卡单引导购买会员卡，lend_before_check：营销页面购买会员卡，lend-stuck-popup：首页弹窗引导用户购买会员卡 |  |
| order_from_name | STRING | column | 会员卡购买入口：lend-before：借款下单前，lend_before_retain：借款下单前-提现页挽留弹窗，vip-center：会员中心，lend-after：借款下单后-借款进度页，lend_after_retain：借款下单后-卡单页挽留弹窗，system：系统下单-自动续约，lend_stuck：风控卡单引导购买会员卡，lend_before_check：营销页面购买会员卡，lend-stuck-popup：首页弹窗引导用户购买会员卡 |  |
| vip_term | STRING | column | 会员期限:single_month：月卡，continue_month：包月，single_season：季卡，continue_season：包季 |  |
| vip_term_name | STRING | column | 会员期限:single_month：月卡，continue_month：包月，single_season：季卡，continue_season：包季 |  |
| card_price | DOUBLE | column | 会员卡的原始定价，元 |  |
| contract_price | DOUBLE | column | 合约价（自动续费的价格），元 |  |
| real_card_price | DOUBLE | column | 会员卡用户实际需要支付的价格，元 | Y |
| start_time | DATETIME | column | 会员生效的起始时间 |  |
| end_time | DATETIME | column | 会员卡到期的时间 |  |
| pay_time | DATETIME | column | 会员卡支付日期（注意签约日期与支付日期是不一致的） | Y |
| pay_source | STRING | column | 会员卡扣款类型:active_pay-主动支付，withhold-免密代扣 |  |
| pay_source_name | STRING | column | 会员卡扣款类型:active_pay-主动支付，withhold-免密代扣 |  |
| pay_type | STRING | column | 会员卡支付类型:debit_card-银行卡支付，wechat-微信 |  |
| pay_type_name | STRING | column | 会员卡支付类型:debit_card-银行卡支付，wechat-微信 |  |
| order_buy_type | STRING | column | 会员卡购买类型:first_sign：首次签约，manual_renew：手动续费，auto_renew：自动续费 |  |
| order_buy_type_name | STRING | column | 会员卡购买类型:first_sign：首次签约，manual_renew：手动续费，auto_renew：自动续费 |  |
| if_cancel_pay | INT | column | 会员卡是否取消扣款 |  |
| cancel_pay_time | DATETIME | column | 会员卡取消扣款的时间 |  |
| cancel_pay_operator | STRING | column | 会员卡取消扣款操作人（用户，客服，系统） |  |
| if_cancel | INT | column | 会员卡是否取消自动续费 |  |
| cancel_time | DATETIME | column | 会员卡取消自动续费的时间 |  |
| cancel_operator | STRING | column | 会员卡取消续费操作人（用户，客服） |  |
| vip_status | BIGINT | column | 会员卡账单是否生效，在会状态（支付时间小于数据pt且小于会员卡到期的时间，并且无退卡或者在有效期外退卡即为1在会，否则0非在会） |  |
| failure_reason | STRING | column | 会员卡账单失效原因 |  |
| failure_time | STRING | column | 会员卡失效时间 |  |
| order_status | STRING | column | 会员卡订单状态：pay_start：待支付，paying：支付中，pay_success：支付成功，pay_cancel：取消，pay_close：关闭，refund_start：待退款，refunding：退款中，refund_fail：退款失败，refund_success：退款成功 |  |
| order_status_name | STRING | column | 会员卡订单状态：pay_start：待支付，paying：支付中，pay_success：支付成功，pay_cancel：取消，pay_close：关闭，refund_start：待退款，refunding：退款中，refund_fail：退款失败，refund_success：退款成功 |  |
| refund_time | DATETIME | column | 会员卡用户退款时间（首次申请退款的时间） |  |
| refund_amount | DOUBLE | column | 会员卡用户退款金额，元（累计的退款金额，可能一笔订单退款多次） | Y |
| refund_cnt | BIGINT | column | 会员卡用户退款次数 |  |
| refund_operator_department | STRING | column | 会员卡退款操作人（用户自己_客服大厅，一线客服、专家组、关怀组） |  |
| refund_operator_name | STRING | column | 具体操作人（用来定位到组别） |  |
| act_refund_time | DATETIME | column | 会员卡退款实际到账的时间 | Y |
| act_refund_status_name | STRING | column | 会员卡退款实际到帐状态： |  |
| loan_order_number | STRING | column | 信贷订单号(如果是在借款提现页和卡单页购买的会员卡，是信贷订单号;如果用户是在流程外金刚位买卡的，是下一笔的订单号) |  |
| asset_type | STRING | column | 资产类型(用户视角订单表中的asset_type_flag) |  |
| loan_status | STRING | column | 信贷订单的借款状态 |  |
| loan_amt | DECIMAL(38,18) | column | 借款成功金额（元） |  |
| loan_period | BIGINT | column | 信贷订单借款期数 |  |
| loan_flag_vip | STRING | column | 会员卡首复贷（会员中心实际的首复贷,取的是放款交易表中的is_again_loan） |  |
| loan_flag | STRING | column | 信贷订单首复贷（订单表中运营使用的首复贷） |  |
| if_reject_30 | STRING | column | 近30天是否被拒（运营维度，cust_no粒度） |  |
| b_score | STRING | column | B卡分（cust_no粒度,当时那个节点的B卡分，20240514 之后取新表，20240514 之前取老表），t-2，风险那边每天早上8点过产出t—1数） |  |
| model_score | STRING | column | 购卡模型分（cust_no粒度） |  |
| app_user_id | STRING | column | 用户号 | Y |
| user_id | STRING | column | 用户id |  |
| mobile | STRING | column | 手机号 |  |
| cust_no | STRING | column | 客户号 | Y |
| id_card_number | STRING | column | 身份证 |  |
| update_time | DATETIME | column | 更新时间 |  |
| flow_no | STRING | column | 外部流水号 |  |
| contract_no | STRING | column | 签章合约号 |  |
| deduct_org_name | STRING | column | 扣款主体 |  |
| pay_flow_no | STRING | column | 最近一次发起扣款支付流水号 |  |
| out_pay_no | STRING | column | 最近一次扣款外部支付号（资产交换核心） |  |
| high_quality_user | STRING | column | 是否优质用户 |  |
| vip_flow_group | STRING | column | 灰度组 |  |
| sign_fy_vip | STRING | column | 是否签约飞跃会员(弃用) |  |
| unsus_time | DATETIME | column | 解约时间 |  |
| unsus_reason | STRING | column | 解约原因 |  |
| refund_reason | STRING | column | 退款原因 |  |
| risk_price | STRING | column | 风险原始定价 |  |
| vip_status_wide | BIGINT | column | 不考虑是否支付，只考虑是否订单生效中的订单状态 |  |
| if_loan_20 | BIGINT | column | 主动签约订单T20内是否有借款成功 |  |
| first_loan_status | STRING | column | 续约订单首笔签约时的放款结果 |  |
| is_xcx | STRING | column | 会员签约端：小程序、APP |  |
| debit_failed_message | STRING | column | 最近一次扣款失败信息 |  |
| first_debit_time | DATETIME | column | 首次发起扣款时间 |  |
| sum_loan_amt_24 | DECIMAL(38,18) | column | 会员订单在有效期内，24借款成功的总金额，不包含首次签约发起的借款订单，user_no粒度 |  |
| order_number_set | STRING | column | 会员订单在有效期内，借款成功的订单号集合，不包含首次签约发起的借款订单，user_no粒度（拆分多行：LATERAL VIEW OUTER EXPLODE(SPLIT(order_number_set,',')) o AS order_num） |  |
| sum_loan_amt_36 | DECIMAL(38,18) | column | 会员订单在有效期内，36借款成功的总金额，不包含首次签约发起的借款订单，user_no粒度 |  |
| init_credit_line | BIGINT | column | 首次签约会员卡订单签约时间在额度有效期内的初始授信额度，续约订单的初始授信额度与首次签约额度一致，cust_no粒度 |  |
| is_fx_turn_fy | STRING | column | 是否飞享转飞跃 |  |
| cancel_pay_reason | STRING | column | 取消扣款原因 |  |
| first_debit_finish_time | DATETIME | column | 首次扣款完成时间 |  |
| first_pay_receipt_time | DATETIME | column | 首次支付回执时间 |  |
| api_to_app | BIGINT | column | 是否API拉回APP |  |
| sub_vip_type | STRING | column | 子会员类型 |  |
| order_amt | DECIMAL(38,18) | column | 申请金额（元） |  |
| credit_amt | DECIMAL(38,18) | column | 授信额度（固+临） |  |
| available_amt | DECIMAL(38,18) | column | 可用额度 |  |
| channel_code | STRING | column | 支付渠道编码 |  |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_inloan_leap_vip_order_hf` (
  `first_vip_order_number` STRING COMMENT '本次会员卡订单的首个订单号，在同一个续费期内的first_vip_order_number保持一致',
  `vip_order_number` STRING COMMENT '会员卡订单号，每一次签约都会生成一个订单号',
  `renew_period` BIGINT COMMENT '当前会员卡订单处于第几期，签约时rn=0,第一次续费为1，直到后续再次签约时从新0开始计数',
  `first_order_time` DATETIME COMMENT '本次会员卡订单的首次签约日期',
  `order_time` DATETIME COMMENT '每一次会员卡订单日期',
  `order_from` STRING COMMENT '会员卡购买入口：lend-before：借款下单前，lend_before_retain：借款下单前-提现页挽留弹窗，vip-center：会员中心，lend-after：借款下单后-借款进度页，lend_after_retain：借款下单后-卡单页挽留弹窗，system：系统下单-自动续约，lend_stuck：风控卡单引导购买会员卡，lend_before_check：营销页面购买会员卡，lend-stuck-popup：首页弹窗引导用户购买会员卡',
  `order_from_name` STRING COMMENT '会员卡购买入口：lend-before：借款下单前，lend_before_retain：借款下单前-提现页挽留弹窗，vip-center：会员中心，lend-after：借款下单后-借款进度页，lend_after_retain：借款下单后-卡单页挽留弹窗，system：系统下单-自动续约，lend_stuck：风控卡单引导购买会员卡，lend_before_check：营销页面购买会员卡，lend-stuck-popup：首页弹窗引导用户购买会员卡',
  `vip_term` STRING COMMENT '会员期限:single_month：月卡，continue_month：包月，single_season：季卡，continue_season：包季',
  `vip_term_name` STRING COMMENT '会员期限:single_month：月卡，continue_month：包月，single_season：季卡，continue_season：包季',
  `card_price` DOUBLE COMMENT '会员卡的原始定价，元',
  `contract_price` DOUBLE COMMENT '合约价（自动续费的价格），元',
  `real_card_price` DOUBLE COMMENT '会员卡用户实际需要支付的价格，元',
  `start_time` DATETIME COMMENT '会员生效的起始时间',
  `end_time` DATETIME COMMENT '会员卡到期的时间',
  `pay_time` DATETIME COMMENT '会员卡支付日期（注意签约日期与支付日期是不一致的）',
  `pay_source` STRING COMMENT '会员卡扣款类型:active_pay-主动支付，withhold-免密代扣',
  `pay_source_name` STRING COMMENT '会员卡扣款类型:active_pay-主动支付，withhold-免密代扣',
  `pay_type` STRING COMMENT '会员卡支付类型:debit_card-银行卡支付，wechat-微信',
  `pay_type_name` STRING COMMENT '会员卡支付类型:debit_card-银行卡支付，wechat-微信',
  `order_buy_type` STRING COMMENT '会员卡购买类型:first_sign：首次签约，manual_renew：手动续费，auto_renew：自动续费',
  `order_buy_type_name` STRING COMMENT '会员卡购买类型:first_sign：首次签约，manual_renew：手动续费，auto_renew：自动续费',
  `if_cancel_pay` INT COMMENT '会员卡是否取消扣款',
  `cancel_pay_time` DATETIME COMMENT '会员卡取消扣款的时间',
  `cancel_pay_operator` STRING COMMENT '会员卡取消扣款操作人（用户，客服，系统）',
  `if_cancel` INT COMMENT '会员卡是否取消自动续费',
  `cancel_time` DATETIME COMMENT '会员卡取消自动续费的时间',
  `cancel_operator` STRING COMMENT '会员卡取消续费操作人（用户，客服）',
  `vip_status` BIGINT COMMENT '会员卡账单是否生效，在会状态（支付时间小于数据pt且小于会员卡到期的时间，并且无退卡或者在有效期外退卡即为1在会，否则0非在会）',
  `failure_reason` STRING COMMENT '会员卡账单失效原因',
  `failure_time` STRING COMMENT '会员卡失效时间',
  `order_status` STRING COMMENT '会员卡订单状态：pay_start：待支付，paying：支付中，pay_success：支付成功，pay_cancel：取消，pay_close：关闭，refund_start：待退款，refunding：退款中，refund_fail：退款失败，refund_success：退款成功',
  `order_status_name` STRING COMMENT '会员卡订单状态：pay_start：待支付，paying：支付中，pay_success：支付成功，pay_cancel：取消，pay_close：关闭，refund_start：待退款，refunding：退款中，refund_fail：退款失败，refund_success：退款成功',
  `refund_time` DATETIME COMMENT '会员卡用户退款时间（首次申请退款的时间）',
  `refund_amount` DOUBLE COMMENT '会员卡用户退款金额，元（累计的退款金额，可能一笔订单退款多次）',
  `refund_cnt` BIGINT COMMENT '会员卡用户退款次数',
  `refund_operator_department` STRING COMMENT '会员卡退款操作人（用户自己_客服大厅，一线客服、专家组、关怀组）',
  `refund_operator_name` STRING COMMENT '具体操作人（用来定位到组别）',
  `act_refund_time` DATETIME COMMENT '会员卡退款实际到账的时间',
  `act_refund_status_name` STRING COMMENT '会员卡退款实际到帐状态：',
  `loan_order_number` STRING COMMENT '信贷订单号(如果是在借款提现页和卡单页购买的会员卡，是信贷订单号;如果用户是在流程外金刚位买卡的，是下一笔的订单号)',
  `asset_type` STRING COMMENT '资产类型(用户视角订单表中的asset_type_flag)',
  `loan_status` STRING COMMENT '信贷订单的借款状态',
  `loan_amt` DECIMAL(38,18) COMMENT '借款成功金额（元）',
  `loan_period` BIGINT COMMENT '信贷订单借款期数',
  `loan_flag_vip` STRING COMMENT '会员卡首复贷（会员中心实际的首复贷,取的是放款交易表中的is_again_loan）',
  `loan_flag` STRING COMMENT '信贷订单首复贷（订单表中运营使用的首复贷）',
  `if_reject_30` STRING COMMENT '近30天是否被拒（运营维度，cust_no粒度）',
  `b_score` STRING COMMENT 'B卡分（cust_no粒度,当时那个节点的B卡分，20240514 之后取新表，20240514 之前取老表），t-2，风险那边每天早上8点过产出t—1数）',
  `model_score` STRING COMMENT '购卡模型分（cust_no粒度）',
  `app_user_id` STRING COMMENT '用户号',
  `user_id` STRING COMMENT '用户id',
  `mobile` STRING COMMENT '手机号',
  `cust_no` STRING COMMENT '客户号',
  `id_card_number` STRING COMMENT '身份证',
  `update_time` DATETIME COMMENT '更新时间',
  `flow_no` STRING COMMENT '外部流水号',
  `contract_no` STRING COMMENT '签章合约号',
  `deduct_org_name` STRING COMMENT '扣款主体',
  `pay_flow_no` STRING COMMENT '最近一次发起扣款支付流水号',
  `out_pay_no` STRING COMMENT '最近一次扣款外部支付号（资产交换核心）',
  `high_quality_user` STRING COMMENT '是否优质用户',
  `vip_flow_group` STRING COMMENT '灰度组',
  `sign_fy_vip` STRING COMMENT '是否签约飞跃会员(弃用)',
  `unsus_time` DATETIME COMMENT '解约时间',
  `unsus_reason` STRING COMMENT '解约原因',
  `refund_reason` STRING COMMENT '退款原因',
  `risk_price` STRING COMMENT '风险原始定价',
  `vip_status_wide` BIGINT COMMENT '不考虑是否支付，只考虑是否订单生效中的订单状态',
  `if_loan_20` BIGINT COMMENT '主动签约订单T20内是否有借款成功',
  `first_loan_status` STRING COMMENT '续约订单首笔签约时的放款结果',
  `is_xcx` STRING COMMENT '会员签约端：小程序、APP',
  `debit_failed_message` STRING COMMENT '最近一次扣款失败信息',
  `first_debit_time` DATETIME COMMENT '首次发起扣款时间',
  `sum_loan_amt_24` DECIMAL(38,18) COMMENT '会员订单在有效期内，24借款成功的总金额，不包含首次签约发起的借款订单，user_no粒度',
  `order_number_set` STRING COMMENT '会员订单在有效期内，借款成功的订单号集合，不包含首次签约发起的借款订单，user_no粒度（拆分多行：LATERAL VIEW OUTER EXPLODE(SPLIT(order_number_set,\',\')) o AS order_num）',
  `sum_loan_amt_36` DECIMAL(38,18) COMMENT '会员订单在有效期内，36借款成功的总金额，不包含首次签约发起的借款订单，user_no粒度',
  `init_credit_line` BIGINT COMMENT '首次签约会员卡订单签约时间在额度有效期内的初始授信额度，续约订单的初始授信额度与首次签约额度一致，cust_no粒度',
  `is_fx_turn_fy` STRING COMMENT '是否飞享转飞跃',
  `cancel_pay_reason` STRING COMMENT '取消扣款原因',
  `first_debit_finish_time` DATETIME COMMENT '首次扣款完成时间',
  `first_pay_receipt_time` DATETIME COMMENT '首次支付回执时间',
  `api_to_app` BIGINT COMMENT '是否API拉回APP',
  `sub_vip_type` STRING COMMENT '子会员类型',
  `order_amt` DECIMAL(38,18) COMMENT '申请金额（元）',
  `credit_amt` DECIMAL(38,18) COMMENT '授信额度（固+临）',
  `available_amt` DECIMAL(38,18) COMMENT '可用额度',
  `channel_code` STRING COMMENT '支付渠道编码'
)
COMMENT '飞跃会员卡订单表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 36500
```

### 抽样数据
| first_vip_order_number | vip_order_number | renew_period | first_order_time | order_time | order_from | order_from_name | vip_term | vip_term_name | card_price | contract_price | real_card_price | start_time | end_time | pay_time | pay_source | pay_source_name | pay_type | pay_type_name | order_buy_type | order_buy_type_name | if_cancel_pay | cancel_pay_time | cancel_pay_operator | if_cancel | cancel_time | cancel_operator | vip_status | failure_reason | failure_time | order_status | order_status_name | refund_time | refund_amount | refund_cnt | refund_operator_department | refund_operator_name | act_refund_time | act_refund_status_name | loan_order_number | asset_type | loan_status | loan_amt | loan_period | loan_flag_vip | loan_flag | if_reject_30 | b_score | model_score | app_user_id | user_id | mobile | cust_no | id_card_number | update_time | flow_no | contract_no | deduct_org_name | pay_flow_no | out_pay_no | high_quality_user | vip_flow_group | sign_fy_vip | unsus_time | unsus_reason | refund_reason | risk_price | vip_status_wide | if_loan_20 | first_loan_status | is_xcx | debit_failed_message | first_debit_time | sum_loan_amt_24 | order_number_set | sum_loan_amt_36 | init_credit_line | is_fx_turn_fy | cancel_pay_reason | first_debit_finish_time | first_pay_receipt_time | api_to_app | sub_vip_type | order_amt | credit_amt | available_amt | channel_code | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| svip1004233 | svip2188345 | 3 | 2025-05-26 09:06:44 | 2025-08-24 01:00:07 | system | 系统下单-自动续约 | continue_month | 包月 | 399.0 | 279.0 | 279.0 | 2025-08-24 23:59:59 | 2025-09-23 23:59:59 | 2025-08-24 08:09:38 | withhold | 免密代扣 | debit_card | 银行卡 | auto_renew | 自动续费 | 0 |  |  | 0 |  |  | 1 |  |  | pay_success | 支付成功 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 3.1 | 593.32 | 1071605253 | 24505413 | eNoXEXdmGHRTvWFMTtu9cQ== | CTL0783c2ab5d28604210950b9da4121428c | rgeXcP0XTkbJwqa7JIqfwq9sf8QcmmCgekR67nY+RRM= | 2025-08-24 08:09:39 | svipflow17559684077638128056 | 2025052601137139531101000200 | 上海泛惠 | svcpay35413177 | 2025082413948908661100900100 |  |  |  |  |  |  | I24 | 1 |  | failed | APP |  | 2025-08-24 08:09:39 | 27800 | 2025091300123600000049324698 | 0 | 15000 |  |  |  |  |  |  |  |  |  |  | 20250916 | 20250916 |
| svip1042996 | svip2030630 | 2 | 2025-06-19 16:10:58 | 2025-08-18 01:00:12 | system | 系统下单-自动续约 | continue_month | 包月 | 399.0 | 279.0 | 279.0 | 2025-08-18 23:59:59 | 2025-09-17 23:59:59 | 2025-08-18 08:08:22 | withhold | 免密代扣 | debit_card | 银行卡 | auto_renew | 自动续费 | 0 |  |  | 0 |  |  | 1 |  |  | pay_success | 支付成功 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1.2 | 637.37 | 1062041531 | 6989317 | b72b2KnTNMgIEpnzy7+blw== | CTL0f0893f89a4753a0c9329973f92b48848 | Msry8aWBUuproZwPqCPvQV0aJJSERV/wx/62mjxtPcg= | 2025-08-18 08:08:23 | svipflow17554500122511193864 | 2025061901817669181101000200 | 上海泛惠 | svcpay30112448 | 2025081813324775261100900100 |  |  |  |  |  |  | I36 | 1 |  | success | APP |  | 2025-08-18 08:08:23 | 10300 | 2025091300123600000049233536,2025082200123600000046647985 | 0 | 2000 |  |  |  |  |  |  |  |  |  |  | 20250916 | 20250916 |
| svip1066904 | svip2191085 | 2 | 2025-06-25 20:13:18 | 2025-08-24 01:01:08 | system | 系统下单-自动续约 | continue_month | 包月 | 399.0 | 279.0 | 279.0 | 2025-08-24 23:59:59 | 2025-09-23 23:59:59 | 2025-08-28 14:05:27 | withhold | 免密代扣 | debit_card | 银行卡 | auto_renew | 自动续费 | 0 |  |  | 0 |  |  | 1 |  |  | pay_success | 支付成功 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 1.2 | 576.83 | 1145267134 | 66037270 | IbJkx9hy9PqJGuQd/XCubQ== | CTL080164cadab7fa58b04f62c2a526268a9 | OR5eYQ7vUuFqxRr3EWc6dRyVqJBhEHrr3kdZhDa59tc= | 2025-08-28 14:05:28 | svipflow17559684684852310944 | 2025062502031477491101000200 | 上海泛惠 | svcpay39430375 | 2025082814387469681100900100 |  |  |  |  |  |  | I36 | 1 |  | success | APP |  | 2025-08-24 08:09:44 | 0 |  | 0 | 20000 |  |  |  |  |  |  |  |  |  |  | 20250916 | 20250916 |
| svip1205925 | svip2608869 | 2 | 2025-07-08 14:33:12 | 2025-09-06 01:00:54 | system | 系统下单-自动续约 | continue_month | 包月 | 399.0 | 279.0 | 279.0 | 2025-09-06 23:59:59 | 2025-10-06 23:59:59 | 2025-09-06 08:13:00 | withhold | 免密代扣 | debit_card | 银行卡 | auto_renew | 自动续费 | 0 |  |  | 0 |  |  | 1 |  |  | pay_success | 支付成功 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 8.0 | 575.53 | 1047598037 | 31386848 | 279cE2+2jl8eTb7T2h1L1A== | CTL04029e07380684877d71f15796c2495e7 | XwApT8oOcyIrSk8IMgKXxtfzRx4pA9nrtleLlI1OwXA= | 2025-09-06 08:13:00 | svipflow17570916542113745236 | 2025070802436890421101000200 | 上海泛惠 | svcpay48513375 | 2025090615245419981100900100 |  |  |  |  |  |  | I36 | 1 |  | success | APP |  | 2025-09-06 08:13:00 | 0 |  | 0 | 1500 |  |  |  |  |  |  |  |  |  |  | 20250916 | 20250916 |
| svip1226400 | svip1801717 | 1 | 2025-07-10 07:49:38 | 2025-08-09 01:00:20 | system | 系统下单-自动续约 | continue_month | 包月 | 399.0 | 279.0 | 279.0 | 2025-08-09 23:59:59 | 2025-09-08 23:59:59 | 2025-08-09 20:08:03 | withhold | 免密代扣 | debit_card | 银行卡 | auto_renew | 自动续费 | 0 |  |  | 1 | 2025-09-03 22:37:40 | 用户 | 0 | 自动到期 | 2025-09-08 23:59:59 | pay_success | 支付成功 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 10.0 | 600.68 | 1257224376 | 173186977 | XzqnRojJd6kSNDTzkMjcvw== | CTL0bf84d22c60c302fec0a7192a2afbe0f3 | Bqg3DFUlJWQJI9UIDLAqmbtee3GZf73r9XeGSi1/Qy0= | 2025-08-09 20:08:04 | svipflow17546724201555399380 | 2025071002482635201101000200 | 上海泛惠 | svcpay23056346 | 2025080912501605131100900100 |  |  |  | 2025-09-03 22:37:40 | 用户取消续约 |  | I36 | 0 |  | success | APP |  | 2025-08-09 08:09:34 | 0 |  | 0 | 1500 |  |  |  |  |  |  |  |  |  |  | 20250916 | 20250916 |

### 同步来源
- `odps`
