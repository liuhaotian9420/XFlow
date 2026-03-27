# xyf_dwd.dwd_repay_loan_repay_plan_df

## 来源文件
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- 老客月会sql代码.ipynb

- `SUM(initial_principal) AS initial_principal`
- `SUM(nvl(initial_interest,0)+nvl(initial_after_loan_fee,0)+nvl(initial_platform_fee,0)) AS initial_interest_fee`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | 借据号 | Y |
| bill_number | STRING | column | 还款计划流水号 |  |
| period_number | BIGINT | column | 期数 |  |
| acct_no | STRING | column | 账户号 |  |
| cust_no | STRING | column | 客户号 |  |
| user_no | STRING | column | 用户号 |  |
| fund_source_old | STRING | column | 资方编码老系统 |  |
| fund_source | STRING | column | 资方编码新系统 |  |
| product_type | STRING | column | 产品编码cash_loan/personal_loan |  |
| product_code | STRING | column | 产品编码 |  |
| date_due | DATETIME | column | 还款期限 |  |
| buffer_deadline | DATETIME | column | 宽限日 |  |
| pay_status | STRING | column | 状态,0-未到期,1-逾期,2-本期结清 |  |
| settle_time | DATETIME | column | 结清时间 |  |
| start_time | DATETIME | column | 当期起息日 |  |
| overdue_days | BIGINT | column | 逾期天数 |  |
| initial_remain_amt | DECIMAL(38,18) | column | 初始剩余本金 |  |
| initial_principal | DECIMAL(38,18) | column | 初始应还本金 | Y |
| initial_interest | DECIMAL(38,18) | column | 初始应还利息 | Y |
| initial_overdue_fee | DECIMAL(38,18) | column | 初始应还罚息(逾期费) |  |
| initial_after_loan_fee | DECIMAL(38,18) | column | 初始应还担保费(贷款服务费) | Y |
| initial_platform_fee | DECIMAL(38,18) | column | 初始应还反担保费(平台服务费） | Y |
| initial_after_loan_overdue_fee | DECIMAL(38,18) | column | 初始应还逾期还款违约金(逾期贷后管理费) |  |
| initial_prepayment_fee | DECIMAL(38,18) | column | 初始应还提前结清手续费 |  |
| initial_violation_fee | DECIMAL(38,18) | column | 初始应还违约金 |  |
| initial_late_fee | DECIMAL(38,18) | column | 初始应还逾期费(逾期费) |  |
| remain_amt | DECIMAL(38,18) | column | 剩余本金 |  |
| should_pay_principal | DECIMAL(38,18) | column | 应还本金 |  |
| should_pay_interest | DECIMAL(38,18) | column | 应还利息 |  |
| should_pay_overdue_fee | DECIMAL(38,18) | column | 应还罚息 |  |
| should_deduct_amt | DECIMAL(38,18) | column | 应减免金额 |  |
| should_pay_after_loan_fee | DECIMAL(38,18) | column | 应还担保费(贷款服务费) |  |
| should_pay_platform_fee | DECIMAL(38,18) | column | 应还反担保费(平台服务费） |  |
| should_pay_after_loan_overdue_fee | DECIMAL(38,18) | column | 应还逾期还款违约金(逾期贷后管理费) |  |
| should_pay_prepayment_fee | DECIMAL(38,18) | column | 应还提前结清手续费 |  |
| should_pay_violation_fee | DECIMAL(38,18) | column | 应还违约金 |  |
| should_pay_late_fee | DECIMAL(38,18) | column | 应还逾期费(逾期费) |  |
| paid_principal_cd | DECIMAL(38,18) | column | 实还本金(包含减免) |  |
| paid_interest_cd | DECIMAL(38,18) | column | 实还利息(包含减免) |  |
| paid_overdue_fee_cd | DECIMAL(38,18) | column | 实还罚息(包含减免) |  |
| paid_after_loan_fee_cd | DECIMAL(38,18) | column | 实还担保费(贷款服务费)(包含减免) |  |
| paid_platform_fee_cd | DECIMAL(38,18) | column | 实还反担保费(平台服务费)(包含减免) |  |
| paid_after_loan_overdue_fee_cd | DECIMAL(38,18) | column | 实还逾期还款违约金(逾期贷后管理费)(包含减免) |  |
| paid_prepayment_fee_cd | DECIMAL(38,18) | column | 实还提前结清手续费(包含减免) |  |
| paid_violation_fee_cd | DECIMAL(38,18) | column | 实还违约金(包含减免) |  |
| paid_late_fee_cd | DECIMAL(38,18) | column | 实还逾期费(逾期费)(包含减免) |  |
| act_deduct_amt | DECIMAL(38,18) | column | 实际减免金额 |  |
| act_red_deduct_amt | DECIMAL(38,18) | column | 实际红线减免金额 |  |
| refund_amt | DECIMAL(38,18) | column | 退款金额 |  |
| should_unprofit_deduct_amt | DECIMAL(38,18) | column | 应减免非营销类金额 |  |
| act_unprofit_deduct_amt | DECIMAL(38,18) | column | 实际减免非营销类金额 |  |
| paid_principal | DECIMAL(38,18) | column | 实还本金 |  |
| paid_interest | DECIMAL(38,18) | column | 实还利息 |  |
| paid_overdue_fee | DECIMAL(38,18) | column | 实还罚息 |  |
| paid_after_loan_fee | DECIMAL(38,18) | column | 实还担保费(贷款服务费) |  |
| paid_platform_fee | DECIMAL(38,18) | column | 实还反担保费(平台服务费） |  |
| paid_after_loan_overdue_fee | DECIMAL(38,18) | column | 实还逾期还款违约金(逾期贷后管理费) |  |
| paid_prepayment_fee | DECIMAL(38,18) | column | 实还提前结清手续费 |  |
| paid_violation_fee | DECIMAL(38,18) | column | 实还违约金 |  |
| paid_late_fee | DECIMAL(38,18) | column | 实还逾期费(逾期费) |  |
| discount_principal | DECIMAL(38,18) | column | 减免本金 |  |
| discount_interest | DECIMAL(38,18) | column | 减免利息 |  |
| discount_overdue_fee | DECIMAL(38,18) | column | 减免罚息 |  |
| discount_after_loan_fee | DECIMAL(38,18) | column | 减免担保费(贷款服务费) |  |
| discount_platform_fee | DECIMAL(38,18) | column | 减免反担保费(平台服务费） |  |
| discount_after_loan_overdue_fee | DECIMAL(38,18) | column | 减免逾期还款违约金(逾期贷后管理费) |  |
| discount_prepayment_fee | DECIMAL(38,18) | column | 减免提前结清手续费 |  |
| discount_violation_fee | DECIMAL(38,18) | column | 减免违约金 |  |
| discount_late_fee | DECIMAL(38,18) | column | 减免违约金 |  |
| comp_type | STRING | column | 代偿类型: 0 未代偿, 1 发生代偿且代偿罚息, 2 发生代偿不代偿罚息 |  |
| app | STRING | column | App |  |
| inner_app | STRING | column | 资金动用渠道 |  |
| date_created | DATETIME | column | 账单创建时间 |  |
| date_updated | DATETIME | column | 账单修改时间 |  |
| principal_paid_time | DATETIME | column | 本金还款时间 |  |
| paid_time | DATETIME | column | 还款时间(最新) |  |
| paid_amt | DECIMAL(38,18) | column | 实还金额 |  |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_repay_loan_repay_plan_df` (
  `order_number` STRING COMMENT '借据号',
  `bill_number` STRING COMMENT '还款计划流水号',
  `period_number` BIGINT COMMENT '期数',
  `acct_no` STRING COMMENT '账户号',
  `cust_no` STRING COMMENT '客户号',
  `user_no` STRING COMMENT '用户号',
  `fund_source_old` STRING COMMENT '资方编码老系统',
  `fund_source` STRING COMMENT '资方编码新系统',
  `product_type` STRING COMMENT '产品编码cash_loan/personal_loan',
  `product_code` STRING COMMENT '产品编码',
  `date_due` DATETIME COMMENT '还款期限',
  `buffer_deadline` DATETIME COMMENT '宽限日',
  `pay_status` STRING COMMENT '状态,0-未到期,1-逾期,2-本期结清',
  `settle_time` DATETIME COMMENT '结清时间',
  `start_time` DATETIME COMMENT '当期起息日',
  `overdue_days` BIGINT COMMENT '逾期天数',
  `initial_remain_amt` DECIMAL(38,18) COMMENT '初始剩余本金',
  `initial_principal` DECIMAL(38,18) COMMENT '初始应还本金',
  `initial_interest` DECIMAL(38,18) COMMENT '初始应还利息',
  `initial_overdue_fee` DECIMAL(38,18) COMMENT '初始应还罚息(逾期费)',
  `initial_after_loan_fee` DECIMAL(38,18) COMMENT '初始应还担保费(贷款服务费)',
  `initial_platform_fee` DECIMAL(38,18) COMMENT '初始应还反担保费(平台服务费）',
  `initial_after_loan_overdue_fee` DECIMAL(38,18) COMMENT '初始应还逾期还款违约金(逾期贷后管理费)',
  `initial_prepayment_fee` DECIMAL(38,18) COMMENT '初始应还提前结清手续费',
  `initial_violation_fee` DECIMAL(38,18) COMMENT '初始应还违约金',
  `initial_late_fee` DECIMAL(38,18) COMMENT '初始应还逾期费(逾期费)',
  `remain_amt` DECIMAL(38,18) COMMENT '剩余本金',
  `should_pay_principal` DECIMAL(38,18) COMMENT '应还本金',
  `should_pay_interest` DECIMAL(38,18) COMMENT '应还利息',
  `should_pay_overdue_fee` DECIMAL(38,18) COMMENT '应还罚息',
  `should_deduct_amt` DECIMAL(38,18) COMMENT '应减免金额',
  `should_pay_after_loan_fee` DECIMAL(38,18) COMMENT '应还担保费(贷款服务费)',
  `should_pay_platform_fee` DECIMAL(38,18) COMMENT '应还反担保费(平台服务费）',
  `should_pay_after_loan_overdue_fee` DECIMAL(38,18) COMMENT '应还逾期还款违约金(逾期贷后管理费)',
  `should_pay_prepayment_fee` DECIMAL(38,18) COMMENT '应还提前结清手续费',
  `should_pay_violation_fee` DECIMAL(38,18) COMMENT '应还违约金',
  `should_pay_late_fee` DECIMAL(38,18) COMMENT '应还逾期费(逾期费)',
  `paid_principal_cd` DECIMAL(38,18) COMMENT '实还本金(包含减免)',
  `paid_interest_cd` DECIMAL(38,18) COMMENT '实还利息(包含减免)',
  `paid_overdue_fee_cd` DECIMAL(38,18) COMMENT '实还罚息(包含减免)',
  `paid_after_loan_fee_cd` DECIMAL(38,18) COMMENT '实还担保费(贷款服务费)(包含减免)',
  `paid_platform_fee_cd` DECIMAL(38,18) COMMENT '实还反担保费(平台服务费)(包含减免)',
  `paid_after_loan_overdue_fee_cd` DECIMAL(38,18) COMMENT '实还逾期还款违约金(逾期贷后管理费)(包含减免)',
  `paid_prepayment_fee_cd` DECIMAL(38,18) COMMENT '实还提前结清手续费(包含减免)',
  `paid_violation_fee_cd` DECIMAL(38,18) COMMENT '实还违约金(包含减免)',
  `paid_late_fee_cd` DECIMAL(38,18) COMMENT '实还逾期费(逾期费)(包含减免)',
  `act_deduct_amt` DECIMAL(38,18) COMMENT '实际减免金额',
  `act_red_deduct_amt` DECIMAL(38,18) COMMENT '实际红线减免金额',
  `refund_amt` DECIMAL(38,18) COMMENT '退款金额',
  `should_unprofit_deduct_amt` DECIMAL(38,18) COMMENT '应减免非营销类金额',
  `act_unprofit_deduct_amt` DECIMAL(38,18) COMMENT '实际减免非营销类金额',
  `paid_principal` DECIMAL(38,18) COMMENT '实还本金',
  `paid_interest` DECIMAL(38,18) COMMENT '实还利息',
  `paid_overdue_fee` DECIMAL(38,18) COMMENT '实还罚息',
  `paid_after_loan_fee` DECIMAL(38,18) COMMENT '实还担保费(贷款服务费)',
  `paid_platform_fee` DECIMAL(38,18) COMMENT '实还反担保费(平台服务费）',
  `paid_after_loan_overdue_fee` DECIMAL(38,18) COMMENT '实还逾期还款违约金(逾期贷后管理费)',
  `paid_prepayment_fee` DECIMAL(38,18) COMMENT '实还提前结清手续费',
  `paid_violation_fee` DECIMAL(38,18) COMMENT '实还违约金',
  `paid_late_fee` DECIMAL(38,18) COMMENT '实还逾期费(逾期费)',
  `discount_principal` DECIMAL(38,18) COMMENT '减免本金',
  `discount_interest` DECIMAL(38,18) COMMENT '减免利息',
  `discount_overdue_fee` DECIMAL(38,18) COMMENT '减免罚息',
  `discount_after_loan_fee` DECIMAL(38,18) COMMENT '减免担保费(贷款服务费)',
  `discount_platform_fee` DECIMAL(38,18) COMMENT '减免反担保费(平台服务费）',
  `discount_after_loan_overdue_fee` DECIMAL(38,18) COMMENT '减免逾期还款违约金(逾期贷后管理费)',
  `discount_prepayment_fee` DECIMAL(38,18) COMMENT '减免提前结清手续费',
  `discount_violation_fee` DECIMAL(38,18) COMMENT '减免违约金',
  `discount_late_fee` DECIMAL(38,18) COMMENT '减免违约金',
  `comp_type` STRING COMMENT '代偿类型: 0 未代偿, 1 发生代偿且代偿罚息, 2 发生代偿不代偿罚息',
  `app` STRING COMMENT 'App',
  `inner_app` STRING COMMENT '资金动用渠道',
  `date_created` DATETIME COMMENT '账单创建时间',
  `date_updated` DATETIME COMMENT '账单修改时间',
  `principal_paid_time` DATETIME COMMENT '本金还款时间',
  `paid_time` DATETIME COMMENT '还款时间(最新)',
  `paid_amt` DECIMAL(38,18) COMMENT '实还金额'
)
COMMENT '现金贷还款计划表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 36000
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C671DA32E7475A6BE6881D Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
