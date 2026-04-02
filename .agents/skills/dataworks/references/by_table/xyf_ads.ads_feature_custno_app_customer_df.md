# xyf_ads.ads_feature_custno_app_customer_df

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| mob_date | DATE | column | 观测日T-0 |  |
| cust_no | STRING | column | 客户号 |  |
| product_type | STRING | column | 产品类型personal_loan/cash_loan |  |
| app | STRING | column | app |  |
| user_no | STRING | column | 用户号,同app_user_id,优先从订单表取,否则从授信表取 |  |
| user_id | STRING | column | 用户id，手机号粒度 |  |
| acct_no | STRING | column | 账户号 |  |
| mobile | STRING | column | 手机号,优先从订单表取,否则从授信表取 |  |
| id_card_number | STRING | column | 身份证 |  |
| customer_type | STRING | column | 睡眠：从未有过成功订单；流失：有过成功订单，目前无在贷余额；在贷：当前有余额 |  |
| customer_type_1 | STRING | column | 不可经营/睡眠/流失/在贷 |  |
| loss_reason | STRING | column | 睡眠/流失的原因:主动/被动 |  |
| loss_days | BIGINT | column | 睡眠/流失距今天数 |  |
| loss_days_interval | STRING | column | 睡眠/流失距今天数区间 |  |
| last_register_time | DATETIME | column | 最近一次注册时间 |  |
| register_status | BIGINT | column | 最近一次注册账号的注册状态 |  |
| last_register_channel | STRING | column | 注册渠道 |  |
| last_app_login_time | DATETIME | column | 最近一次app登录时间 |  |
| is_app_login_180d | STRING | column | 最近180天是否登录app |  |
| first_credit_succ_time | DATETIME | column | 首次授信成功时间 |  |
| first_credit_succ_amt | DOUBLE | column | 首次授信成功额度 |  |
| first_credit_succ_channel | STRING | column | 首次授信成功渠道 |  |
| last_credit_succ_time | DATETIME | column | 最近一次授信成功时间 |  |
| last_credit_succ_month | STRING | column | 最近一次授信成功年月 |  |
| last_credit_succ_amt | DOUBLE | column | 最近一次授信成功额度 |  |
| last_credit_succ_amt_interval | STRING | column | 最近一次授信成功额度区间 |  |
| last_credit_succ_channel | STRING | column | 最近一次授信成功渠道 |  |
| credit_expire_time | DATETIME | column | 授信/额度失效时间 |  |
| fixed_amt | DOUBLE | column | 固额,元 |  |
| temp_amt | DOUBLE | column | 临额,元 |  |
| total_amt | DOUBLE | column | 总额=固额+临额,元 |  |
| total_amt_interval | STRING | column | 总额区间,元 |  |
| debit_amt | DOUBLE | column | 贷还本金/在贷金额,元 |  |
| freeze_amt | DOUBLE | column | 冻结额度(在途订单占用额度),元 |  |
| freeze_bal | DOUBLE | column | 冻结余额(风控冻额),元 |  |
| used_amt | DOUBLE | column | 已用额度(在贷余额+在途订单的预占用额度),元 |  |
| used_amt_rate | STRING | column | 额度使用率 |  |
| available_amt | DOUBLE | column | 可用额度=固额+临额-已用额度(在贷余额+在途订单的预占用额度)-风控冻额,元 |  |
| available_amt_interval | STRING | column | 可用额度区间,元 |  |
| expire_temp_amt_used | DOUBLE | column | 临额过期占用,元 |  |
| last_adjust_amt_time | DATETIME | column | 最近一次调额时间 |  |
| adjust_amt_label_30d | STRING | column | 最近30天调额标签 |  |
| order_succ_cnt | BIGINT | column | 成功订单数 |  |
| first_withdraw_succ_days | INT | column | 首贷距今天数 |  |
| first_withdraw_succ_loan_time | DATETIME | column | 首贷放款时间 |  |
| first_withdraw_succ_channel | STRING | column | 首贷借款渠道 |  |
| first_withdraw_succ_amt | DOUBLE | column | 首贷金额 |  |
| last_withdraw_apply_time | DATETIME | column | 最近一次提现申请时间 |  |
| last_withdraw_apply_channel | STRING | column | 最近一次提现申请渠道 |  |
| last_withdraw_apply_status | STRING | column | 最近一次提现申请结果 |  |
| last_withdraw_apply_biz_flow_number | STRING | column | 最近一次提现申请业务流水号 |  |
| last_withdraw_succ_loan_time | DATETIME | column | 最近一次提现放款时间 |  |
| last_app_withdraw_succ_loan_time | DATETIME | column | 最近一次app提现放款时间 |  |
| last_withdraw_succ_inner_app | STRING | column | 最近一次提现成功inner_app |  |
| last_withdraw_reject_time | DATETIME | column | 最近一次提现拒绝时间 |  |
| last_withdraw_reject_reason | STRING | column | 最近一次提现拒绝原因 |  |
| last_withdraw_reject_days_interval | STRING | column | 最近一次提现拒绝距今天数区间 |  |
| last_fund_reject_time | DATETIME | column | 最近一次资方拒绝时间，含子订单资方拒绝 |  |
| last_fund_reject_days | INT | column | 最近一次资方拒绝距今天数 |  |
| first_withdraw_paid_period_cnt | BIGINT | column | 首贷已还分期数 |  |
| first_withdraw_paid_period_cnt_interval | STRING | column | 首贷已还分期数区间 |  |
| other_app_zaidai | STRING | column | 其他app在贷 |  |
| max_paid_period | STRING | column | 最大还款期数 |  |
| paid_period_cnt_100d | STRING | column | 近100天还款期数 |  |
| unpaid_order_cnt | BIGINT | column | 在贷订单数/未结清订单数 |  |
| last_paid_time | DATETIME | column | 最近一次还款时间 |  |
| settle_months | BIGINT | column | 所有订单结清距今月份 |  |
| settle_months_interval | STRING | column | 所有订单结清距今月份区间 |  |
| custno_max_overdue_days | BIGINT | column | 客户号粒度历史最大逾期天数,含逾期已还 |  |
| custno_max_overdue_days_interval | STRING | column | 客户号粒度历史最大逾期天数区间,含逾期已还 |  |
| custno_max_overdue_days_current | BIGINT | column | 当前最大逾期天数 |  |
| custno_max_overdue_days_interval_current | STRING | column | 当前最大逾期天数区间 |  |
| duotou_br_td | STRING | column | 多头类型 |  |
| tongdun_3m_fy | DOUBLE | column | 切片时间最近一次申请订单的同盾3m多头 |  |
| bairong_3m_fy | DOUBLE | column | 切片时间最近一次申请订单的百融3m多头 |  |
| hj_1y_xfnl_1 | BIGINT | column | 近1年国内购票金额（下限） |  |
| rhyz | STRING | column | 人行优质客户标签 |  |
| if_credit_card | STRING | column | 是否信用卡客户 |  |
| if_rh | STRING | column | 是否有人行 |  |
| huarong3_131 | DOUBLE | column | 未结清贷款最近1个月平均应还款 |  |
| huarong3_133 | DOUBLE | column | 未结清信用贷款最近1个月平均应还款 |  |
| huarong2_139 | DOUBLE | column | 准贷记卡账户近6个月平均应还款金额 |  |
| huarong2_176 | DOUBLE | column | 非循环贷本月应还款金额总和 |  |
| huarong2_238 | DOUBLE | column | 循环额度下分账户本月应还款金额总和 |  |
| huarong2_260 | DOUBLE | column | 循环贷本月应还款金额总和 |  |
| huarong2_281 | DOUBLE | column | 贷记卡最近月度本月应还金额总和 |  |
| huarong2_356 | DOUBLE | column | 所有账户当前正常汽车贷款余额总和 |  |
| huarong2_362 | DOUBLE | column | 所有账户当前贷款本月应还金额总和 |  |
| risk_price | STRING | column | 风险定价 |  |
| forbidden_expiration_time | DATETIME | column | 禁申期解除时间 |  |
| risk_level | STRING | column | 风险评级A-K |  |
| is_black | BIGINT | column | 是否黑名单(身份证/手机号) |  |
| province_true | STRING | column | 省份 |  |
| education | STRING | column | 学历水平 |  |
| is_education | STRING | column | 有学历/无学历 |  |
| job | STRING | column | 职业 |  |
| monthly_income | STRING | column | 月收入 |  |
| random_1 | STRING | column | 贷前随机数 |  |
| random_2 | STRING | column | 贷中随机数 |  |
| forbidden_withdraw_apply | INT | column | 禁止提现，1/0 |  |
| migrate_flag | INT | column | 是否fxk xyf01合并用户,1/0 |  |
| first_withdraw_succ_order_number | STRING | column | 首贷成功订单号 |  |
| first_withdraw_succ_ori_order_number | STRING | column | 首贷成功主订单号 |  |
| first_withdraw_succ_rh_level | DOUBLE | column | 首贷人行评级 |  |
| first_withdraw_succ_rh_level_channel | STRING | column | 首贷人行评级实际来源,如在api被拒后进入app流程 |  |
| app_order_succ_cnt | BIGINT | column | app提现成功订单数 |  |
| last_should_pay_date | DATETIME | column | 最晚应还日 |  |
| tek_adjust_amt_30d | INT | column | 近30天是否提额卡调额 |  |
| tek_adjust_amt_cnt | BIGINT | column | 累计提额卡购卡调额次数 |  |
| tek_adjust_amt_cnt_90d | BIGINT | column | 近90天提额卡调额次数 |  |
| tek_adjust_amt_cnt_180d | BIGINT | column | 近180天提额卡调额次数 |  |
| lift_forbidden_time | DATETIME | column | 禁申手动解除时间 |  |
| age | BIGINT | column | 年龄 |  |
| forbidden_end_time | DATETIME | column | 禁申结束时间,min(手动解除,到期自动解除) |  |
| last_zhengxin_report_days_interval | STRING | column | 最近一次征信报告距今天数区间 |  |
| zhengxin_debt | DOUBLE | column | 征信负债 |  |
| sd_zhengxin_good_label | DOUBLE | column | 首贷征信好人标签(好人标签命中数之和) |  |
| personalloan_fd_6mceng30_xfzx_offline_v2_prob | DOUBLE | column | 贷中融担征信6M30子模型v2打分_离线 |  |
| leap_vip_status_1 | STRING | column | 飞跃会员状态(支付时间小于数据pt且小于会员卡到期的时间，并且无退卡或者在有效期外退卡):从未入会/曾经在会/当前在会 |  |
| leap_vip_status_2 | STRING | column | 飞跃会员状态(不考虑是否支付，只考虑是否订单生效中的状态):从未入会/曾经在会/当前在会 |  |
| withdraw_fk_reject_cnt_30d | BIGINT | column | 近30天风控拒绝订单数 |  |
| first_app_withdraw_succ_loan_time | DATETIME | column | 首次app放款时间 |  |
| first_withdraw_succ_apply_total_amt | DOUBLE | column | 首贷放款前客户总额度(固+临)，无首贷则为空值，约百条记录值不准确 |  |
| is_logoff | BIGINT | column | 是否注销1/0，客户在当前app下所有注册手机号均注销 |  |
| avg_overdue_days_his | DOUBLE | column | 平均历史逾期天数: 累计历史逾期天数/累计历史逾期期次数 |  |
| overdue_rate_his | DOUBLE | column | 历史逾期率: 累计历史逾期期次数/到期期次数 |  |
| personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | DOUBLE | column | 从v6版本开始的细分评级 |  |
| last_risk_price_adjust_decision_time | DATETIME | column | 最近一次风险定价决策时间 |  |
| risk_price_adjustment_output | STRING | column | 最近一次风险定价输出结果 |  |
| first_withdraw_succ_bizid | STRING | column | 首贷成功bizid |  |
| pt | STRING | column |  |  |
| pt | STRING | partition |  |  |

### DDL
```sql
CREATE TABLE xyf_ads.`ads_feature_custno_app_customer_df` (
  `mob_date` DATE COMMENT '观测日T-0',
  `cust_no` STRING COMMENT '客户号',
  `product_type` STRING COMMENT '产品类型personal_loan/cash_loan',
  `app` STRING COMMENT 'app',
  `user_no` STRING COMMENT '用户号,同app_user_id,优先从订单表取,否则从授信表取',
  `user_id` STRING COMMENT '用户id，手机号粒度',
  `acct_no` STRING COMMENT '账户号',
  `mobile` STRING COMMENT '手机号,优先从订单表取,否则从授信表取',
  `id_card_number` STRING COMMENT '身份证',
  `customer_type` STRING COMMENT '睡眠：从未有过成功订单；流失：有过成功订单，目前无在贷余额；在贷：当前有余额',
  `customer_type_1` STRING COMMENT '不可经营/睡眠/流失/在贷',
  `loss_reason` STRING COMMENT '睡眠/流失的原因:主动/被动',
  `loss_days` BIGINT COMMENT '睡眠/流失距今天数',
  `loss_days_interval` STRING COMMENT '睡眠/流失距今天数区间',
  `last_register_time` DATETIME COMMENT '最近一次注册时间',
  `register_status` BIGINT COMMENT '最近一次注册账号的注册状态',
  `last_register_channel` STRING COMMENT '注册渠道',
  `last_app_login_time` DATETIME COMMENT '最近一次app登录时间',
  `is_app_login_180d` STRING COMMENT '最近180天是否登录app',
  `first_credit_succ_time` DATETIME COMMENT '首次授信成功时间',
  `first_credit_succ_amt` DOUBLE COMMENT '首次授信成功额度',
  `first_credit_succ_channel` STRING COMMENT '首次授信成功渠道',
  `last_credit_succ_time` DATETIME COMMENT '最近一次授信成功时间',
  `last_credit_succ_month` STRING COMMENT '最近一次授信成功年月',
  `last_credit_succ_amt` DOUBLE COMMENT '最近一次授信成功额度',
  `last_credit_succ_amt_interval` STRING COMMENT '最近一次授信成功额度区间',
  `last_credit_succ_channel` STRING COMMENT '最近一次授信成功渠道',
  `credit_expire_time` DATETIME COMMENT '授信/额度失效时间',
  `fixed_amt` DOUBLE COMMENT '固额,元',
  `temp_amt` DOUBLE COMMENT '临额,元',
  `total_amt` DOUBLE COMMENT '总额=固额+临额,元',
  `total_amt_interval` STRING COMMENT '总额区间,元',
  `debit_amt` DOUBLE COMMENT '贷还本金/在贷金额,元',
  `freeze_amt` DOUBLE COMMENT '冻结额度(在途订单占用额度),元',
  `freeze_bal` DOUBLE COMMENT '冻结余额(风控冻额),元',
  `used_amt` DOUBLE COMMENT '已用额度(在贷余额+在途订单的预占用额度),元',
  `used_amt_rate` STRING COMMENT '额度使用率',
  `available_amt` DOUBLE COMMENT '可用额度=固额+临额-已用额度(在贷余额+在途订单的预占用额度)-风控冻额,元',
  `available_amt_interval` STRING COMMENT '可用额度区间,元',
  `expire_temp_amt_used` DOUBLE COMMENT '临额过期占用,元',
  `last_adjust_amt_time` DATETIME COMMENT '最近一次调额时间',
  `adjust_amt_label_30d` STRING COMMENT '最近30天调额标签',
  `order_succ_cnt` BIGINT COMMENT '成功订单数',
  `first_withdraw_succ_days` INT COMMENT '首贷距今天数',
  `first_withdraw_succ_loan_time` DATETIME COMMENT '首贷放款时间',
  `first_withdraw_succ_channel` STRING COMMENT '首贷借款渠道',
  `first_withdraw_succ_amt` DOUBLE COMMENT '首贷金额',
  `last_withdraw_apply_time` DATETIME COMMENT '最近一次提现申请时间',
  `last_withdraw_apply_channel` STRING COMMENT '最近一次提现申请渠道',
  `last_withdraw_apply_status` STRING COMMENT '最近一次提现申请结果',
  `last_withdraw_apply_biz_flow_number` STRING COMMENT '最近一次提现申请业务流水号',
  `last_withdraw_succ_loan_time` DATETIME COMMENT '最近一次提现放款时间',
  `last_app_withdraw_succ_loan_time` DATETIME COMMENT '最近一次app提现放款时间',
  `last_withdraw_succ_inner_app` STRING COMMENT '最近一次提现成功inner_app',
  `last_withdraw_reject_time` DATETIME COMMENT '最近一次提现拒绝时间',
  `last_withdraw_reject_reason` STRING COMMENT '最近一次提现拒绝原因',
  `last_withdraw_reject_days_interval` STRING COMMENT '最近一次提现拒绝距今天数区间',
  `last_fund_reject_time` DATETIME COMMENT '最近一次资方拒绝时间，含子订单资方拒绝',
  `last_fund_reject_days` INT COMMENT '最近一次资方拒绝距今天数',
  `first_withdraw_paid_period_cnt` BIGINT COMMENT '首贷已还分期数',
  `first_withdraw_paid_period_cnt_interval` STRING COMMENT '首贷已还分期数区间',
  `other_app_zaidai` STRING COMMENT '其他app在贷',
  `max_paid_period` STRING COMMENT '最大还款期数',
  `paid_period_cnt_100d` STRING COMMENT '近100天还款期数',
  `unpaid_order_cnt` BIGINT COMMENT '在贷订单数/未结清订单数',
  `last_paid_time` DATETIME COMMENT '最近一次还款时间',
  `settle_months` BIGINT COMMENT '所有订单结清距今月份',
  `settle_months_interval` STRING COMMENT '所有订单结清距今月份区间',
  `custno_max_overdue_days` BIGINT COMMENT '客户号粒度历史最大逾期天数,含逾期已还',
  `custno_max_overdue_days_interval` STRING COMMENT '客户号粒度历史最大逾期天数区间,含逾期已还',
  `custno_max_overdue_days_current` BIGINT COMMENT '当前最大逾期天数',
  `custno_max_overdue_days_interval_current` STRING COMMENT '当前最大逾期天数区间',
  `duotou_br_td` STRING COMMENT '多头类型',
  `tongdun_3m_fy` DOUBLE COMMENT '切片时间最近一次申请订单的同盾3m多头',
  `bairong_3m_fy` DOUBLE COMMENT '切片时间最近一次申请订单的百融3m多头',
  `hj_1y_xfnl_1` BIGINT COMMENT '近1年国内购票金额（下限）',
  `rhyz` STRING COMMENT '人行优质客户标签',
  `if_credit_card` STRING COMMENT '是否信用卡客户',
  `if_rh` STRING COMMENT '是否有人行',
  `huarong3_131` DOUBLE COMMENT '未结清贷款最近1个月平均应还款',
  `huarong3_133` DOUBLE COMMENT '未结清信用贷款最近1个月平均应还款',
  `huarong2_139` DOUBLE COMMENT '准贷记卡账户近6个月平均应还款金额',
  `huarong2_176` DOUBLE COMMENT '非循环贷本月应还款金额总和',
  `huarong2_238` DOUBLE COMMENT '循环额度下分账户本月应还款金额总和',
  `huarong2_260` DOUBLE COMMENT '循环贷本月应还款金额总和',
  `huarong2_281` DOUBLE COMMENT '贷记卡最近月度本月应还金额总和',
  `huarong2_356` DOUBLE COMMENT '所有账户当前正常汽车贷款余额总和',
  `huarong2_362` DOUBLE COMMENT '所有账户当前贷款本月应还金额总和',
  `risk_price` STRING COMMENT '风险定价',
  `forbidden_expiration_time` DATETIME COMMENT '禁申期解除时间',
  `risk_level` STRING COMMENT '风险评级A-K',
  `is_black` BIGINT COMMENT '是否黑名单(身份证/手机号)',
  `province_true` STRING COMMENT '省份',
  `education` STRING COMMENT '学历水平',
  `is_education` STRING COMMENT '有学历/无学历',
  `job` STRING COMMENT '职业',
  `monthly_income` STRING COMMENT '月收入',
  `random_1` STRING COMMENT '贷前随机数',
  `random_2` STRING COMMENT '贷中随机数',
  `forbidden_withdraw_apply` INT COMMENT '禁止提现，1/0',
  `migrate_flag` INT COMMENT '是否fxk xyf01合并用户,1/0',
  `first_withdraw_succ_order_number` STRING COMMENT '首贷成功订单号',
  `first_withdraw_succ_ori_order_number` STRING COMMENT '首贷成功主订单号',
  `first_withdraw_succ_rh_level` DOUBLE COMMENT '首贷人行评级',
  `first_withdraw_succ_rh_level_channel` STRING COMMENT '首贷人行评级实际来源,如在api被拒后进入app流程',
  `app_order_succ_cnt` BIGINT COMMENT 'app提现成功订单数',
  `last_should_pay_date` DATETIME COMMENT '最晚应还日',
  `tek_adjust_amt_30d` INT COMMENT '近30天是否提额卡调额',
  `tek_adjust_amt_cnt` BIGINT COMMENT '累计提额卡购卡调额次数',
  `tek_adjust_amt_cnt_90d` BIGINT COMMENT '近90天提额卡调额次数',
  `tek_adjust_amt_cnt_180d` BIGINT COMMENT '近180天提额卡调额次数',
  `lift_forbidden_time` DATETIME COMMENT '禁申手动解除时间',
  `age` BIGINT COMMENT '年龄',
  `forbidden_end_time` DATETIME COMMENT '禁申结束时间,min(手动解除,到期自动解除)',
  `last_zhengxin_report_days_interval` STRING COMMENT '最近一次征信报告距今天数区间',
  `zhengxin_debt` DOUBLE COMMENT '征信负债',
  `sd_zhengxin_good_label` DOUBLE COMMENT '首贷征信好人标签(好人标签命中数之和)',
  `personalloan_fd_6mceng30_xfzx_offline_v2_prob` DOUBLE COMMENT '贷中融担征信6M30子模型v2打分_离线',
  `leap_vip_status_1` STRING COMMENT '飞跃会员状态(支付时间小于数据pt且小于会员卡到期的时间，并且无退卡或者在有效期外退卡):从未入会/曾经在会/当前在会',
  `leap_vip_status_2` STRING COMMENT '飞跃会员状态(不考虑是否支付，只考虑是否订单生效中的状态):从未入会/曾经在会/当前在会',
  `withdraw_fk_reject_cnt_30d` BIGINT COMMENT '近30天风控拒绝订单数',
  `first_app_withdraw_succ_loan_time` DATETIME COMMENT '首次app放款时间',
  `first_withdraw_succ_apply_total_amt` DOUBLE COMMENT '首贷放款前客户总额度(固+临)，无首贷则为空值，约百条记录值不准确',
  `is_logoff` BIGINT COMMENT '是否注销1/0，客户在当前app下所有注册手机号均注销',
  `avg_overdue_days_his` DOUBLE COMMENT '平均历史逾期天数: 累计历史逾期天数/累计历史逾期期次数',
  `overdue_rate_his` DOUBLE COMMENT '历史逾期率: 累计历史逾期期次数/到期期次数',
  `personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6` DOUBLE COMMENT '从v6版本开始的细分评级',
  `last_risk_price_adjust_decision_time` DATETIME COMMENT '最近一次风险定价决策时间',
  `risk_price_adjustment_output` STRING COMMENT '最近一次风险定价输出结果',
  `first_withdraw_succ_bizid` STRING COMMENT '首贷成功bizid'
)
COMMENT '客户宽表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 2000
```

## 抽样数据
| mob_date | cust_no | product_type | app | user_no | user_id | acct_no | mobile | id_card_number | customer_type | customer_type_1 | loss_reason | loss_days | loss_days_interval | last_register_time | register_status | last_register_channel | last_app_login_time | is_app_login_180d | first_credit_succ_time | first_credit_succ_amt | first_credit_succ_channel | last_credit_succ_time | last_credit_succ_month | last_credit_succ_amt | last_credit_succ_amt_interval | last_credit_succ_channel | credit_expire_time | fixed_amt | temp_amt | total_amt | total_amt_interval | debit_amt | freeze_amt | freeze_bal | used_amt | used_amt_rate | available_amt | available_amt_interval | expire_temp_amt_used | last_adjust_amt_time | adjust_amt_label_30d | order_succ_cnt | first_withdraw_succ_days | first_withdraw_succ_loan_time | first_withdraw_succ_channel | first_withdraw_succ_amt | last_withdraw_apply_time | last_withdraw_apply_channel | last_withdraw_apply_status | last_withdraw_apply_biz_flow_number | last_withdraw_succ_loan_time | last_app_withdraw_succ_loan_time | last_withdraw_succ_inner_app | last_withdraw_reject_time | last_withdraw_reject_reason | last_withdraw_reject_days_interval | last_fund_reject_time | last_fund_reject_days | first_withdraw_paid_period_cnt | first_withdraw_paid_period_cnt_interval | other_app_zaidai | max_paid_period | paid_period_cnt_100d | unpaid_order_cnt | last_paid_time | settle_months | settle_months_interval | custno_max_overdue_days | custno_max_overdue_days_interval | custno_max_overdue_days_current | custno_max_overdue_days_interval_current | duotou_br_td | tongdun_3m_fy | bairong_3m_fy | hj_1y_xfnl_1 | rhyz | if_credit_card | if_rh | huarong3_131 | huarong3_133 | huarong2_139 | huarong2_176 | huarong2_238 | huarong2_260 | huarong2_281 | huarong2_356 | huarong2_362 | risk_price | forbidden_expiration_time | risk_level | is_black | province_true | education | is_education | job | monthly_income | random_1 | random_2 | forbidden_withdraw_apply | migrate_flag | first_withdraw_succ_order_number | first_withdraw_succ_ori_order_number | first_withdraw_succ_rh_level | first_withdraw_succ_rh_level_channel | app_order_succ_cnt | last_should_pay_date | tek_adjust_amt_30d | tek_adjust_amt_cnt | tek_adjust_amt_cnt_90d | tek_adjust_amt_cnt_180d | lift_forbidden_time | age | forbidden_end_time | last_zhengxin_report_days_interval | zhengxin_debt | sd_zhengxin_good_label | personalloan_fd_6mceng30_xfzx_offline_v2_prob | leap_vip_status_1 | leap_vip_status_2 | withdraw_fk_reject_cnt_30d | first_app_withdraw_succ_loan_time | first_withdraw_succ_apply_total_amt | is_logoff | avg_overdue_days_his | overdue_rate_his | personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | last_risk_price_adjust_decision_time | risk_price_adjustment_output | first_withdraw_succ_bizid | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2023-03-01 | CTL011793f364a3a4895b57cd4eb22867002 | personal_loan | fxk | 1029003005 | 21257761 | L000818165410231557 | F/lao7mLmTbYA+CY2vFW9w== | +ATXsQDIHSLqPm1fJc5DF+3Ta4qQ1g7rii9IET6n0Us= | 流失 | 流失 | 被动 | 268 | 90+ | 2021-06-06 18:00:04 | 10 | 中原消金 |  | 未登陆APP | 2021-11-02 20:34:13 | 7000.0 | 中原消金 | 2021-11-02 20:34:13 | 2021-11 | 7000.0 | 5000-10000 | 中原消金 | 2025-04-08 00:00:00 | 7000.0 | 0.0 | 7000.0 | 5000-10000 | 0.0 | 0.0 | 0.0 | 0.01 | 0-30% | 6999.99 | 5000-10000 | 0.0 | 2021-06-06 18:01:00 | 非调额组 | 1 | 633 | 2021-06-06 18:27:20 | 中原消金 | 3000.0 | 2022-04-13 09:26:02 | 中原消金 | 交易失败 | 20220413092602375699454 | 2021-06-06 18:27:20 |  | fxk_zyxj | 2022-04-13 09:26:02 | reject\|[riskAudit]大额取现策略审核:reject | 90+ |  | -1 | 12 | 10-12 | 历史无在贷订单 | 12 | 0 | 0 | 2022-06-06 04:00:33 | 9 | 6+ | 0 | 0 | 0 | 0 | Personal_Actree02 | 7.0 | 9.0 |  | 其他 | 1 | 0 |  |  |  |  |  |  |  |  |  |  |  | F | 0 | 湖南省 | 高中/中专/技校 | 无学历 | 其他 | 未知 | 2897692769083487613163973383614336577532040263756774933676910904765961737499149844985021002216772651 | 3000312611371074009902893425162853117068712550698871465935067329550453713726280073399081557855559260 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 43 |  | 无记录 | 0.0 |  |  |  |  |  |  |  | 0 | 0.0 | 0.0 |  |  |  |  | 20230228 | 20230228 |
| 2023-03-01 | CTL087b95c48c1ae7cd89da1f604ef787c2c | cash_loan | xyf | 1009342278 | 12910729 | L000081855687109161 | efcnVZj7zprV3NCaJmoZVQ== | +w+3hy5v0Nqp++QGvldVAPzSZ15fAG3ArkVoZWkihBs= | 流失 | 流失 | 主动 | 609 | 90+ | 2020-10-01 15:34:47 | 10 | API流量 | 2022-11-19 07:03:02 | 登陆APP | 2021-11-02 19:54:49 | 6000.0 | API流量 | 2021-11-02 19:54:49 | 2021-11 | 6000.0 | 5000-10000 | API流量 | 2025-04-08 00:00:00 | 6600.0 | 0.0 | 6600.0 | 5000-10000 | 0.0 | 0.0 | 0.0 | 0.0 | 0-30% | 6600.0 | 5000-10000 | 0.0 | 2021-06-30 10:19:10 | 非调额组 | 1 | 880 | 2020-10-02 11:03:22 | API流量 | 6000.0 | 2020-10-02 10:58:42 | API流量 | 交易成功 | 20201002105842177104145 | 2020-10-02 11:03:22 |  | xyf_jqns |  |  | -1 |  | -1 | 9 | 6-9 | 历史无在贷订单 | 9 | 0 | 0 | 2021-06-30 09:51:26 | 21 | 6+ | 0 | 0 | 0 | 0 | Personal_Actree03 | 20.0 | 32.0 | 500 | 其他 | 1 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 湖南省 | 大专 | 有学历 | 其他 | 10,000~20,000 | 1118797072662723640261230162314659389489201375931589585150028527879982409879096515251441172403529139 | 2992998864911314240150143530013754729669156370696113780508223505115063888533744792463094696413826792 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 25 |  | 无记录 | 0.0 |  |  |  |  |  |  |  | 0 | 0.0 | 0.0 |  |  |  |  | 20230228 | 20230228 |
| 2023-03-01 | CTL0f30e8017ef7b4b831ef62e39572d6201 | cash_loan | xyf | 1008790484 | 12440460 | L000081875156934251 | uVqjgekB17YtqFIP9nygmg== | /ntVGrcilzz509Q4B7AbJjSp1fGzgxlXA4JfpqNkQTo= | 睡眠 | 睡眠 | 主动 | 484 | 90+ | 2020-09-15 16:01:22 | 10 | 其他 | 2021-10-10 12:22:49 | 未登陆APP | 2021-11-02 20:12:19 | 5000.0 | APP流量 | 2021-11-02 20:12:19 | 2021-11 | 5000.0 | 5000-10000 | APP流量 | 2025-04-08 00:00:00 | 5000.0 | 0.0 | 5000.0 | 3000-5000 | 0.0 | 0.0 | 0.0 | 0.0 | 0-30% | 5000.0 | 5000-10000 | 0.0 | 2021-03-05 14:35:30 | 非调额组 |  |  |  | 其他 |  |  | 其他 |  |  |  |  | 缺失 |  |  | -1 |  | -1 |  | 0 | 历史无在贷订单 | 缺失 | 缺失 |  |  | -1 |  | 0 | 0 | 0 | 0 | Personal_Actree01 | 6.0 | 7.0 |  | 其他 | 1 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 湖南省 | 高中/中专/技校 | 无学历 | 其他 | 10,000~20,000 | 6620972305323981202151562769813548871618852879956009031182267472723163870626916266010621906291911099 | 0620165520503308152478550582026820198192383250668388481007292587644435236958580647954129532281190195 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 44 |  | 无记录 | 0.0 |  |  |  |  |  |  |  | 0 |  |  |  |  |  |  | 20230228 | 20230228 |
| 2023-03-01 | CTL06d2c909700afc3993f379973646b87e5 | cash_loan | cxh | 1005367267 | 8375476 | L000081812555719078 | E7he2TYFNFDpiwbSPPkhhQ== | 0h3xsHkBMri2E7EruQrZ6lOj/3RBQZPEXYA+PYXtkaw= | 睡眠 | 睡眠 | 主动 | 484 | 90+ | 2020-06-24 15:36:26 | 0 | 其他 |  | 未登陆APP | 2021-11-02 19:43:33 | 5000.0 | APP流量 | 2021-11-02 19:43:33 | 2021-11 | 5000.0 | 5000-10000 | APP流量 | 2025-04-08 00:00:00 | 5000.0 | 0.0 | 5000.0 | 3000-5000 | 0.0 | 0.0 | 0.0 | 0.0 | 0-30% | 5000.0 | 5000-10000 | 0.0 | 2020-06-24 15:41:45 | 非调额组 |  |  |  | 其他 |  |  | 其他 |  |  |  |  | 缺失 |  |  | -1 |  | -1 |  | 0 | 当前无在贷订单 | 缺失 | 缺失 |  |  | -1 |  | 1 | 1-2 | 0 | 0 | Personal_Actree03 | 18.0 | 23.0 |  | 其他 | 1 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 北京市 | 大专 | 有学历 | 其他 | 10,000~20,000 | 7434378932421749283945644254148164198307587527206716839014063787926768988346976337152896274748761096 | 4549732380339214062167374334320181266633102331691761087130950077733900550889687149172222130919770654 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 30 |  | 无记录 | 0.0 |  |  |  |  |  |  |  | 0 |  |  |  |  |  |  | 20230228 | 20230228 |
| 2023-03-01 | CTL03f6709f06aa2b98247444c04af1f9f77 | personal_loan | fxk | 1064155540 | 34845549 | L000818244715305456 | bir/myvLPAzyjSENLbEL5A== | 0lWKWRST6zQN6SK9ZOpc22lJ0YBc0RlLLdO6bVACfj8= | 睡眠 | 睡眠 | 主动 |  |  |  |  | 其他 |  | 未登陆APP |  |  | 其他 |  |  |  |  | 其他 |  | 9000.0 | 0.0 | 9000.0 | 5000-10000 | 0.0 | 0.0 | 0.0 | 0.0 | 0-30% | 9000.0 | 5000-10000 | 0.0 | 2022-08-30 09:02:35 | 非调额组 |  |  |  | 其他 |  |  | 其他 |  |  |  |  | 缺失 |  |  | -1 |  | -1 |  | 0 | 历史无在贷订单 | 缺失 | 缺失 |  |  | -1 |  | 0 | 0 | 0 | 0 | Personal_Actree02 | 10.0 | 10.0 |  | 2.公积金优质用户 | 0 | 1 | 21007.8624 | 3473.616 |  | 70952.0 | 44731.0 | 12071.0 | 27072.0 | 0.0 | 154826.0 |  |  |  | 0 | 北京市 | 硕博 | 有学历 | 其他 | 20,000~50,000 | 7516993792132493908229960983155122699449865524775746541208086185744602625318638068407001145089822997 | 6373575399897326383638670718070734496804913564217041888470006151251139862978090200223124163580932018 | 0 |  |  |  |  |  |  |  |  |  |  |  |  | 41 |  | 03_近12m | 182728.8 | 15.0579121373412 |  |  |  |  |  |  | 0 |  |  |  |  |  |  | 20230228 | 20230228 |

## 同步来源
- `odps`
