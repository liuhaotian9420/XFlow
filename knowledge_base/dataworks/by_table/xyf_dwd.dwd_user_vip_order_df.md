# xyf_dwd.dwd_user_vip_order_df

## 来源文件
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

- `'vip' AS card_type`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `pay_time AS tran_time`
- `real_card_price/100 AS pay_amt`
- `refund_amount/100 AS refund_amt`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| vip_order_number | STRING | column | 每一次签约都会生成一个订单号，无论结果（参照订单表中的order_number） |  |
| first_vip_order_number | STRING | column | 本次订单的首个订单号，在同一个续费期内的first_vip_order_number保持一致，主要用户续费月卡（参照资金路由） |  |
| order_time | DATETIME | column | 每一次的签约日期，精确到时分秒 | Y |
| first_order_time | DATETIME | column | 本次订单的首次签约日期，精确到时分秒（first_vip_order_number对应的时间） |  |
| app_user_id | STRING | column | app_user_id（请不要记录xyf的app_user_id） | Y |
| user_id | STRING | column | 用户id |  |
| cust_no | STRING | column | 客户号 | Y |
| app | STRING | column | 用户的APP |  |
| mobile_protyle | STRING | column | 手机密文 |  |
| id_card_protyle | STRING | column | 身份证密文 |  |
| utm_source | STRING | column | utm_source |  |
| flow_number | STRING | column | 进件号-流程号 |  |
| pay_biz_order_no | STRING | column | 支付回调的业务单号，退款需要这个 |  |
| pay_flow_no | STRING | column | 支付发起payOrderNo |  |
| order_buy_type | BIGINT | column | 订单操作类型：1-首次购买，2-手动续期，3-自动续期，4-手动关闭，5-自动关闭 |  |
| order_buy_type_name | STRING | column | 订单操作类型：首次购买，手动续期，自动续期，手动关闭，自动关闭 |  |
| pay_type | BIGINT | column | 支付类型:1-支付宝，2-银行卡支付，3-微信 |  |
| pay_type_name | STRING | column | 支付类型:支付宝，银行卡支付，微信 |  |
| decute_type | BIGINT | column | 扣款类型:1-收银台支付，2-免密代扣 |  |
| decute_type_name | STRING | column | 扣款类型:收银台支付，免密代扣 |  |
| pay_time | DATETIME | column | 支付日期（注意签约日期与支付日期是不一致的） | Y |
| order_from | STRING | column | 购买入口：vip-center，lend-before，lend-after，system |  |
| order_number_loan | STRING | column | 如果是在借款提现页和卡单页购买的会员卡，需要匹配出其相对应的信贷订单 |  |
| if_validation | BIGINT | column | 会员卡账单是否生效 | Y |
| validation_reson | STRING | column | 会员卡账单失效原因 1-先还款后退款 2-失效后的假退款 3-客服直接取消扣款 |  |
| vip_card_type | BIGINT | column | 会员卡类型:1:会员卡，2:御金卡，3:速通卡，4:提额卡 | Y |
| vip_card_type_name | STRING | column | 会员卡类型:会员卡，御金卡，速通卡，提额卡 |  |
| vip_term | BIGINT | column | 会员期限:1-月卡，2-连续包月，3-季卡 |  |
| vip_term_name | STRING | column | 会员期限:月卡，连续包月，季卡 |  |
| card_price | BIGINT | column | 会员卡的原始定价，分 |  |
| real_card_price | BIGINT | column | 用户实际需要支付的价格，分 | Y |
| order_status | BIGINT | column | 订单状态 0:初始创建，1:代扣处理中，2:支付发起，3-支付成功，4-支付失败，5-包括代扣全部失败和客服操作支付关闭，6-已退卡 |  |
| order_status_name | STRING | column | 订单状态 初始创建，代扣处理中，支付发起，支付成功，支付失败，包括代扣全部失败和客服操作支付关闭，已退卡 |  |
| refund_time | DATETIME | column | 用户退款时间 |  |
| refund_amount | BIGINT | column | 用户退款金额，分 | Y |
| if_cancel | INT | column | 是否取消自动续费 |  |
| cancel_time | DATETIME | column | 取消自动续费的时间 |  |
| start_time | DATETIME | column | 会员生效的起始时间，以首次签约时间（first_order_time）开始计算 |  |
| end_time | DATETIME | column | 如果是月卡&季卡，则为30天或者90天有效期，如果为续费月卡，则记录无限大，待续费卡结束后统一更新？ |  |
| message | STRING | column | 订单状态信息 |  |
| user_gay_group | STRING | column | 用户灰度组 |  |
| create_time | DATETIME | column | 创建时间 |  |
| update_time | DATETIME | column | 更新时间 |  |
| loan_status | STRING | column | 借款状态 |  |
| mobile | STRING | column | 手机号 |  |
| id_card_number | STRING | column | 身份证号 |  |
| id | BIGINT | column | 主键id |  |
| failure_time | STRING | column | 失效时间 1. 自然到期失效：用户在start和endtime之间没有过任何退卡操作，则失效时间=end_time 2. 由于发起扣款起的7天内未成功支付，所以7天后自动失效，这时失效时间=7天后的那个节点 3. 由于用户要求客服退卡，客服操作退卡成功时间即为失效时间 |  |
| vip_status | STRING | column | 在会状态 1）pay_time非空，且<=pt 2）end_time>=pt 3）假如有退卡，则refund_time>pt 满足以上3个条件即为1（在会） 否则0（非在会） |  |
| act_refund_status_name | STRING | column | 退款实际到帐状态 未退款 退款中 退款成功 退款失败 其他 |  |
| act_refund_time | DATETIME | column | 退款实际到账的时间 | Y |
| contract_price | INT | column | 签约价（分） |  |
| pay_center_handel_status | TINYINT | column | 支付中心支付处理状态：0-初始，1-处理中,2-支付成功 |  |
| operator | STRING | column | 操作人 |  |
| refund_operator | STRING | column | 会员卡退款操作人 |  |
| first_vip_order_number_new | STRING | column | 本次订单的首个订单号(线上) |  |
| if_cancel_pay | BIGINT | column | 会员卡是否取消扣款 |  |
| cancel_pay_time | DATETIME | column | 会员卡取消扣款时间 |  |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_user_vip_order_df` (
  `vip_order_number` STRING COMMENT '每一次签约都会生成一个订单号，无论结果（参照订单表中的order_number）',
  `first_vip_order_number` STRING COMMENT '本次订单的首个订单号，在同一个续费期内的first_vip_order_number保持一致，主要用户续费月卡（参照资金路由）',
  `order_time` DATETIME COMMENT '每一次的签约日期，精确到时分秒',
  `first_order_time` DATETIME COMMENT '本次订单的首次签约日期，精确到时分秒（first_vip_order_number对应的时间）',
  `app_user_id` STRING COMMENT 'app_user_id（请不要记录xyf的app_user_id）',
  `user_id` STRING COMMENT '用户id',
  `cust_no` STRING COMMENT '客户号',
  `app` STRING COMMENT '用户的APP',
  `mobile_protyle` STRING COMMENT '手机密文',
  `id_card_protyle` STRING COMMENT '身份证密文',
  `utm_source` STRING COMMENT 'utm_source',
  `flow_number` STRING COMMENT '进件号-流程号',
  `pay_biz_order_no` STRING COMMENT '支付回调的业务单号，退款需要这个',
  `pay_flow_no` STRING COMMENT '支付发起payOrderNo',
  `order_buy_type` BIGINT COMMENT '订单操作类型：1-首次购买，2-手动续期，3-自动续期，4-手动关闭，5-自动关闭',
  `order_buy_type_name` STRING COMMENT '订单操作类型：首次购买，手动续期，自动续期，手动关闭，自动关闭',
  `pay_type` BIGINT COMMENT '支付类型:1-支付宝，2-银行卡支付，3-微信',
  `pay_type_name` STRING COMMENT '支付类型:支付宝，银行卡支付，微信',
  `decute_type` BIGINT COMMENT '扣款类型:1-收银台支付，2-免密代扣',
  `decute_type_name` STRING COMMENT '扣款类型:收银台支付，免密代扣',
  `pay_time` DATETIME COMMENT '支付日期（注意签约日期与支付日期是不一致的）',
  `order_from` STRING COMMENT '购买入口：vip-center，lend-before，lend-after，system',
  `order_number_loan` STRING COMMENT '如果是在借款提现页和卡单页购买的会员卡，需要匹配出其相对应的信贷订单',
  `if_validation` BIGINT COMMENT '会员卡账单是否生效',
  `validation_reson` STRING COMMENT '会员卡账单失效原因 1-先还款后退款 2-失效后的假退款 3-客服直接取消扣款',
  `vip_card_type` BIGINT COMMENT '会员卡类型:1:会员卡，2:御金卡，3:速通卡，4:提额卡',
  `vip_card_type_name` STRING COMMENT '会员卡类型:会员卡，御金卡，速通卡，提额卡',
  `vip_term` BIGINT COMMENT '会员期限:1-月卡，2-连续包月，3-季卡',
  `vip_term_name` STRING COMMENT '会员期限:月卡，连续包月，季卡',
  `card_price` BIGINT COMMENT '会员卡的原始定价，分',
  `real_card_price` BIGINT COMMENT '用户实际需要支付的价格，分',
  `order_status` BIGINT COMMENT '订单状态 0:初始创建，1:代扣处理中，2:支付发起，3-支付成功，4-支付失败，5-包括代扣全部失败和客服操作支付关闭，6-已退卡',
  `order_status_name` STRING COMMENT '订单状态 初始创建，代扣处理中，支付发起，支付成功，支付失败，包括代扣全部失败和客服操作支付关闭，已退卡',
  `refund_time` DATETIME COMMENT '用户退款时间',
  `refund_amount` BIGINT COMMENT '用户退款金额，分',
  `if_cancel` INT COMMENT '是否取消自动续费',
  `cancel_time` DATETIME COMMENT '取消自动续费的时间',
  `start_time` DATETIME COMMENT '会员生效的起始时间，以首次签约时间（first_order_time）开始计算',
  `end_time` DATETIME COMMENT '如果是月卡&季卡，则为30天或者90天有效期，如果为续费月卡，则记录无限大，待续费卡结束后统一更新？',
  `message` STRING COMMENT '订单状态信息',
  `user_gay_group` STRING COMMENT '用户灰度组',
  `create_time` DATETIME COMMENT '创建时间',
  `update_time` DATETIME COMMENT '更新时间',
  `loan_status` STRING COMMENT '借款状态',
  `mobile` STRING COMMENT '手机号',
  `id_card_number` STRING COMMENT '身份证号',
  `id` BIGINT COMMENT '主键id',
  `failure_time` STRING COMMENT '失效时间 1. 自然到期失效：用户在start和endtime之间没有过任何退卡操作，则失效时间=end_time 2. 由于发起扣款起的7天内未成功支付，所以7天后自动失效，这时失效时间=7天后的那个节点 3. 由于用户要求客服退卡，客服操作退卡成功时间即为失效时间',
  `vip_status` STRING COMMENT '在会状态 1）pay_time非空，且<=pt 2）end_time>=pt 3）假如有退卡，则refund_time>pt 满足以上3个条件即为1（在会） 否则0（非在会）',
  `act_refund_status_name` STRING COMMENT '退款实际到帐状态 未退款 退款中 退款成功 退款失败 其他',
  `act_refund_time` DATETIME COMMENT '退款实际到账的时间',
  `contract_price` INT COMMENT '签约价（分）',
  `pay_center_handel_status` TINYINT COMMENT '支付中心支付处理状态：0-初始，1-处理中,2-支付成功',
  `operator` STRING COMMENT '操作人',
  `refund_operator` STRING COMMENT '会员卡退款操作人',
  `first_vip_order_number_new` STRING COMMENT '本次订单的首个订单号(线上)',
  `if_cancel_pay` BIGINT COMMENT '会员卡是否取消扣款',
  `cancel_pay_time` DATETIME COMMENT '会员卡取消扣款时间'
)
COMMENT '会员卡订单表(老飞享会员卡)，将会下线慎用，请使用 xyf_dwd.dwd_inloan_vip_order_df'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 36500
```

### 抽样数据
| vip_order_number | first_vip_order_number | order_time | first_order_time | app_user_id | user_id | cust_no | app | mobile_protyle | id_card_protyle | utm_source | flow_number | pay_biz_order_no | pay_flow_no | order_buy_type | order_buy_type_name | pay_type | pay_type_name | decute_type | decute_type_name | pay_time | order_from | order_number_loan | if_validation | validation_reson | vip_card_type | vip_card_type_name | vip_term | vip_term_name | card_price | real_card_price | order_status | order_status_name | refund_time | refund_amount | if_cancel | cancel_time | start_time | end_time | message | user_gay_group | create_time | update_time | loan_status | mobile | id_card_number | id | failure_time | vip_status | act_refund_status_name | act_refund_time | contract_price | pay_center_handel_status | operator | refund_operator | first_vip_order_number_new | if_cancel_pay | cancel_pay_time | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| vcvip1055634 | vcvip1055634 | 2024-05-09 16:29:52 | 2024-05-09 16:29:52 | 1022871118 | 13081835 | CTL09e7c5341b5a06d052eac14ce992d40d4 | xyf01 | mdd67e9f464d5b574776a2d77b3ae7100 | i072ab317a35548e76ac948e44d693b22 | xyf01_app | 20240509162849000014000021181930 | 2024051000117800000000894103 |   | 1 | 首次购买 | 2 | 银行卡支付 | 2 | 免密代扣 | 2024-05-10 03:03:12 | lend-before | 2024050900001700000074833108 | 1 |  | 1 | 会员卡 | 2 | 连续包月 | 14900 | 9900 | 3 | 支付成功 |  |  | 0 |  | 2024-05-09 16:29:52 | 2024-06-08 16:29:52 | 成功 | C | 2024-05-09 16:29:52 | 2024-05-18 18:51:09 | failed | NZsx2esXEafyM/6QOyu6hw== | 6GBh+RT8KLCGSDKeH99nB7ugQDzASj3uvj+XcQP7v8M= | 45745 | 2024-06-08 16:29:52 | 1 |  |  |  |  |  |  |  |  |  | 20240510 | 20240510 |
| vcvip1026639 | vcvip1026639 | 2024-05-04 10:58:26 | 2024-05-04 10:58:26 | 1132134246 | 59872933 | CTL0172d4278c036044320c922181c620d91 | xyf01 | mabda18cafcfbae54f6f6ecf41ae6fb31 | i1d52db134e508e3698d3217a0b3dcabf | xyf01_app | 20240504105618000014000018220448 | 2024051100117800000001165767 |   | 1 | 首次购买 | 2 | 银行卡支付 | 2 | 免密代扣 |  | lend-before | 2024050400001700000038104812 | 0 |  | 1 | 会员卡 | 2 | 连续包月 | 14900 | 11900 | 4 | 支付失败 |  |  | 0 |  |  |  | 余额不足，请核实后重新发起 | C | 2024-05-04 10:58:26 | 2024-05-18 18:51:09 | failed | C7Gp8+TOpJefqWU2yApvfQ== | x7LrCIcRN0UnWCsKPuHyOF0aJJSERV/wx/62mjxtPcg= | 18446 | 2024-05-11 10:58:26 | 0 |  |  |  |  |  |  |  |  |  | 20240510 | 20240510 |
| vcvip1040976 | vcvip1040976 | 2024-05-07 18:06:19 | 2024-05-07 18:06:19 | 1043639124 | 29978041 | CTL0e90b2b81aa7212bf89de086d182a59f1 | xyf01 | mf19d68d0b5b47eda5937af5bcb65ea5b | i9c4efe2e49dff2371883c91bd2783ab3 | xyf01_app | 20240507175932000014000020081898 | pay1010070 | JDFH7880845309799792647 | 1 | 首次购买 | 2 | 银行卡支付 | 1 | 收银台支付 | 2024-05-07 18:08:49 | lend-after | 2024050700001700000023893574 | 1 |  | 1 | 会员卡 | 2 | 连续包月 | 14900 | 7900 | 3 | 支付成功 |  |  | 0 |  | 2024-05-07 18:06:19 | 2024-06-06 18:06:19 | 成功 | C | 2024-05-07 18:06:19 | 2024-05-18 18:51:09 | failed | 9doIREl+uqQ8loXVaNgkYA== | ylgP5aMF/FmbZpZvDbd1io0KEr9KivlJRU/stN5SSOw= | 32564 | 2024-06-06 18:06:19 | 1 |  |  |  |  |  |  |  |  |  | 20240510 | 20240510 |
| vcvip1019375 | vcvip1019375 | 2024-05-02 20:16:31 | 2024-05-02 20:16:31 | 1016961122 | 8232565 | CTL045f3daf361f15ffa5f192e6e2d0f5e90 | xyf01 | m078f8398637a4e7f1e6cc00dfb322870 | ie3dcefe031b26f866f50f54cbaf974e7 | xyf01_app | 20240502201008000014000017487654 | 2024050900117800000000792938 |   | 1 | 首次购买 | 2 | 银行卡支付 | 2 | 免密代扣 |  | lend-before | 2024050200001700000004196208 | 0 |  | 1 | 会员卡 | 2 | 连续包月 | 14900 | 11900 | 4 | 支付失败 |  |  | 0 |  |  |  | 余额不足，请核实后重新发起 | C | 2024-05-02 20:16:31 | 2024-05-18 18:51:09 | failed | Z62qgy3E03ISDOjb+rIi8A== | cxv+Y4FaUBCT+soHIQ0Qr7ugQDzASj3uvj+XcQP7v8M= | 12707 | 2024-05-09 20:16:31 | 0 |  |  |  |  |  |  |  |  |  | 20240510 | 20240510 |
| vcvip1048860 | vcvip1048860 | 2024-05-09 01:57:59 | 2024-05-09 01:57:59 | 1047783073 | 31462312 | CTL05115c87d2096972d5abf7817691ce895 | xyf01 | ma7c97e1715eb4cffd57043608c27618f | i9baae4df9e1fac9ae5f1de6e5e45e4e7 | xyf01_app | 20240509015731000014000020805819 | 2024051600117800000002428247 |   | 1 | 首次购买 | 2 | 银行卡支付 | 2 | 免密代扣 |  | lend-before | 2024050900001700000057708744 | 0 |  | 1 | 会员卡 | 2 | 连续包月 | 14900 | 13900 | 4 | 支付失败 |  |  | 0 |  |  |  | 余额不足，请核实后重新发起 | C | 2024-05-09 01:57:59 | 2024-05-20 19:00:05 | failed | PyC3uW1g//08hG5FljLELQ== | uh7FKK1ddcgiO9+drF7bRjF0jz7Ep2o81tpmZnP/I7s= | 38721 | 2024-05-16 01:57:59 | 0 |  |  |  |  |  |  |  |  |  | 20240510 | 20240510 |

### 同步来源
- `odps`
