# xyf_ads.ads_fin_onloan_fee_df

## 来源文件
- ads_inloan_loan_balance_mthly_df.sql

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| days | DATE | column | 日期 |  |
| fund_source | STRING | column | 资方 |  |
| loan_type | STRING | column | 产品类型 |  |
| asset_type | BIGINT | column | 资产类型 |  |
| risk_price | STRING | column | 风险定价 |  |
| pay_amt | DOUBLE | column | 放款金额 |  |
| pay_cnt | BIGINT | column | 放款订单数 |  |
| repay_amt | DECIMAL(38,18) | column | 还款金额 |  |
| repay_cnt | BIGINT | column | 还款订单数 |  |
| repay_clear_cnt | BIGINT | column | 还款清贷数 |  |
| comp_amt | DOUBLE | column | 代偿金额 |  |
| comp_cnt | BIGINT | column | 代偿订单数 |  |
| comp_clear_cnt | BIGINT | column | 代偿清贷数 |  |
| comp_one_amt | DOUBLE | column | 单期代偿金额 |  |
| comp_one_cnt | BIGINT | column | 单期代偿笔数 |  |
| comp_all_amt | DOUBLE | column | 全额代偿金额 |  |
| comp_all_cnt | BIGINT | column | 全额代偿笔数 |  |
| after_comp_amt | DOUBLE | column | 代偿后回款金额 |  |
| model_value_flag | STRING | column | 下探标签 |  |
| fin_product_name | STRING | column | 金融产品名称 |  |
| settle_cnt | BIGINT | column | 结清笔数 |  |
| comp_fund_penalty_interest | DOUBLE | column | 代偿罚息 |  |
| pt | STRING | column |  |  |
| pt | STRING | partition |  |  |

### DDL
```sql
CREATE TABLE xyf_ads.`ads_fin_onloan_fee_df` (
  `days` DATE COMMENT '日期',
  `fund_source` STRING COMMENT '资方',
  `loan_type` STRING COMMENT '产品类型',
  `asset_type` BIGINT COMMENT '资产类型',
  `risk_price` STRING COMMENT '风险定价',
  `pay_amt` DOUBLE COMMENT '放款金额',
  `pay_cnt` BIGINT COMMENT '放款订单数',
  `repay_amt` DECIMAL(38,18) COMMENT '还款金额',
  `repay_cnt` BIGINT COMMENT '还款订单数',
  `repay_clear_cnt` BIGINT COMMENT '还款清贷数',
  `comp_amt` DOUBLE COMMENT '代偿金额',
  `comp_cnt` BIGINT COMMENT '代偿订单数',
  `comp_clear_cnt` BIGINT COMMENT '代偿清贷数',
  `comp_one_amt` DOUBLE COMMENT '单期代偿金额',
  `comp_one_cnt` BIGINT COMMENT '单期代偿笔数',
  `comp_all_amt` DOUBLE COMMENT '全额代偿金额',
  `comp_all_cnt` BIGINT COMMENT '全额代偿笔数',
  `after_comp_amt` DOUBLE COMMENT '代偿后回款金额',
  `model_value_flag` STRING COMMENT '下探标签',
  `fin_product_name` STRING COMMENT '金融产品名称',
  `settle_cnt` BIGINT COMMENT '结清笔数',
  `comp_fund_penalty_interest` DOUBLE COMMENT '代偿罚息'
)
COMMENT '在贷余额'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 9999
```

## 抽样数据
- 未采样

## 同步来源
- `odps`

## 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C6747DC6E4BCE316EC6B2A Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
