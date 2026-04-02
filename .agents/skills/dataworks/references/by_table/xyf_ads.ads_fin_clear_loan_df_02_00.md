# xyf_ads.ads_fin_clear_loan_df_02_00

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| fund_source | STRING | column |  |  |
| asset_loan_type | STRING | column |  |  |
| period | BIGINT | column |  |  |
| loan_type_flag | STRING | column |  |  |
| pay_time1 | DATETIME | column |  |  |
| pay_month | STRING | column |  |  |
| payment_deadline | DATETIME | column |  |  |
| risk_price | STRING | column |  |  |
| order_number | STRING | column |  |  |
| paid_time | DATETIME | column |  |  |
| period_number | BIGINT | column |  |  |
| amount | DECIMAL(38,12) | column |  |  |
| should_interest | DECIMAL(38,12) | column |  |  |
| should_after_loan_fee | DECIMAL(38,12) | column |  |  |
| should_platform_fee | DECIMAL(38,12) | column |  |  |
| paid_interest | DECIMAL(38,12) | column |  |  |
| paid_after_loan_fee | DECIMAL(38,12) | column |  |  |
| paid_platform_fee | DECIMAL(38,12) | column |  |  |
| paid_prepayment_fee | DECIMAL(38,12) | column |  |  |
| discount_interest | DECIMAL(38,12) | column |  |  |
| discount_after_loan_fee | DECIMAL(38,12) | column |  |  |
| discount_platform_fee | DECIMAL(38,12) | column |  |  |
| discount_prepayment_fee | DECIMAL(38,12) | column |  |  |
| red_deduct_interest | DECIMAL(38,12) | column |  |  |
| red_deduct_after_loan_fee | DECIMAL(38,12) | column |  |  |
| red_deduct_platform_fee | DECIMAL(38,12) | column |  |  |
| red_deduct_prepayment_fee | DECIMAL(38,12) | column |  |  |
| act_red_deduct_amt | DECIMAL(38,12) | column |  |  |
| if_red_deduct | STRING | column |  |  |
| fee_rate | STRING | column |  |  |
| is_clear | BIGINT | column |  |  |
| max_paid_time | DATETIME | column |  |  |
| cap_type | STRING | column |  |  |
| loan_app | STRING | column |  |  |
| risk_asset_type | STRING | column |  |  |
| type_24 | STRING | column |  |  |
| ori_risk_price | STRING | column |  |  |
| credit_rate | DECIMAL(38,18) | column |  |  |
| irr12_fund_rate | DECIMAL(38,18) | column |  |  |
| 利息损失合计 | DECIMAL(38,12) | column |  |  |
| inner_app | STRING | column |  |  |
| coupon_type | STRING | column |  |  |
| attribution_source | STRING | column |  |  |

### DDL
```sql
CREATE TABLE xyf_ads.`ads_fin_clear_loan_df_02_00` (
  `fund_source` STRING,
  `asset_loan_type` STRING,
  `period` BIGINT,
  `loan_type_flag` STRING,
  `pay_time1` DATETIME,
  `pay_month` STRING,
  `payment_deadline` DATETIME,
  `risk_price` STRING,
  `order_number` STRING,
  `paid_time` DATETIME,
  `period_number` BIGINT,
  `amount` DECIMAL(38,12),
  `should_interest` DECIMAL(38,12),
  `should_after_loan_fee` DECIMAL(38,12),
  `should_platform_fee` DECIMAL(38,12),
  `paid_interest` DECIMAL(38,12),
  `paid_after_loan_fee` DECIMAL(38,12),
  `paid_platform_fee` DECIMAL(38,12),
  `paid_prepayment_fee` DECIMAL(38,12),
  `discount_interest` DECIMAL(38,12),
  `discount_after_loan_fee` DECIMAL(38,12),
  `discount_platform_fee` DECIMAL(38,12),
  `discount_prepayment_fee` DECIMAL(38,12),
  `red_deduct_interest` DECIMAL(38,12),
  `red_deduct_after_loan_fee` DECIMAL(38,12),
  `red_deduct_platform_fee` DECIMAL(38,12),
  `red_deduct_prepayment_fee` DECIMAL(38,12),
  `act_red_deduct_amt` DECIMAL(38,12),
  `if_red_deduct` STRING,
  `fee_rate` STRING,
  `is_clear` BIGINT,
  `max_paid_time` DATETIME,
  `cap_type` STRING,
  `loan_app` STRING,
  `risk_asset_type` STRING,
  `type_24` STRING,
  `ori_risk_price` STRING,
  `credit_rate` DECIMAL(38,18),
  `irr12_fund_rate` DECIMAL(38,18),
  `利息损失合计` DECIMAL(38,12),
  `inner_app` STRING,
  `coupon_type` STRING,
  `attribution_source` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| fund_source | asset_loan_type | period | loan_type_flag | pay_time1 | pay_month | payment_deadline | risk_price | order_number | paid_time | period_number | amount | should_interest | should_after_loan_fee | should_platform_fee | paid_interest | paid_after_loan_fee | paid_platform_fee | paid_prepayment_fee | discount_interest | discount_after_loan_fee | discount_platform_fee | discount_prepayment_fee | red_deduct_interest | red_deduct_after_loan_fee | red_deduct_platform_fee | red_deduct_prepayment_fee | act_red_deduct_amt | if_red_deduct | fee_rate | is_clear | max_paid_time | cap_type | loan_app | risk_asset_type | type_24 | ori_risk_price | credit_rate | irr12_fund_rate | 利息损失合计 | inner_app | coupon_type | attribution_source |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| xl_cash | 现金分期-36 | 6 | 复贷 | 2020-01-01 09:54:19 | 2020-01 | 2020-05-01 00:00:00 | 其他 | 20200101094047014534908 | 2020-04-30 17:50:24 | 4 | 836.02 | 16.62 | 0 | 0 | 16.62 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 否 |  | 0 | 2020-07-01 13:23:24 | other | app | 36% | 36 | other | 0.078 | 0.079 | 0 | xyf | 否 | 其他 |
| xl_cash | 现金分期-36 | 6 | 复贷 | 2020-01-01 09:54:19 | 2020-01 | 2020-07-01 00:00:00 | 其他 | 20200101094047014534908 | 2020-07-01 13:23:24 | 6 | 847.07 | 5.58 | 0 | 0 | 5.58 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 否 |  | 0 | 2020-07-01 13:23:24 | other | app | 36% | 36 | other | 0.078 | 0.079 | 0 | xyf | 否 | 其他 |
| xl_cash | 现金分期-36 | 6 | 复贷 | 2020-01-01 09:54:19 | 2020-01 | 2020-06-01 00:00:00 | 其他 | 20200101094047014534908 | 2020-05-26 12:49:13 | 5 | 841.52 | 11.12 | 0 | 0 | 11.12 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 否 |  | 0 | 2020-07-01 13:23:24 | other | app | 36% | 36 | other | 0.078 | 0.079 | 0 | xyf | 否 | 其他 |
| xl_cash | 现金分期-36 | 6 | 复贷 | 2020-01-01 09:54:19 | 2020-01 | 2020-02-01 00:00:00 | 其他 | 20200101094047014534908 | 2020-02-04 16:59:54 | 1 | 819.72 | 32.92 | 336.75 | 55.32 | 32.92 | 336.75 | 55.32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 否 |  | 0 | 2020-07-01 13:23:24 | other | app | 36% | 36 | other | 0.078 | 0.079 | 0 | xyf | 否 | 其他 |
| xl_cash | 现金分期-36 | 6 | 复贷 | 2020-01-01 09:54:19 | 2020-01 | 2020-03-01 00:00:00 | 其他 | 20200101094047014534908 | 2020-03-03 14:26:59 | 2 | 825.12 | 27.52 | 336.75 | 55.32 | 27.52 | 336.75 | 55.32 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 否 |  | 0 | 2020-07-01 13:23:24 | other | app | 36% | 36 | other | 0.078 | 0.079 | 0 | xyf | 否 | 其他 |

## 同步来源
- `odps`
