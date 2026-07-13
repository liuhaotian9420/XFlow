# xyf_dws.dws_repay_user_order_df

## 来源文件
- ads_inloan_loan_balance_mthly_df.sql
- 老客月会sql代码.ipynb

- `'daily' AS flag`
- `CASE WHEN pt < '20250623' THEN (CASE WHEN app <> inner_app THEN 'API' WHEN loan_flag = '首贷' THEN 'APP首贷' ELSE 'APP复贷' END ) WHEN pt >= '20250623' THEN (CASE WHEN business_line = 'API' THEN 'API' WHEN loan_flag = '首贷' THEN 'APP首贷' ELSE 'APP复贷' END ) END AS loan_type`
- `COUNT(DISTINCT CASE WHEN overdue_days <= 30 AND loan_balance > 0 THEN order_number END) AS loan_cnt_30_minus`
- `SUM(CASE WHEN overdue_days <= 30 THEN loan_balance END) AS loan_balance_30_minus`
- `SUM(CASE WHEN overdue_days <=180 THEN loan_balance END)/100000000 AS `余额_180``
- `SUM(CASE WHEN overdue_days <=30 THEN loan_balance END)/100000000 AS `余额_30``
- `SUM(CASE WHEN overdue_days <=90 THEN loan_balance END)/100000000 AS `余额_90``
- `substr(TO_DATE(pt,'yyyyMMdd'),1,10) AS data_date`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | 订单号(借据号) | Y |
| first_order_number | STRING | column | 用户真实订单号 |  |
| apply_id | STRING | column | 授信申请流水id |  |
| acct_no | STRING | column | 账户号 |  |
| cust_no | STRING | column | 客户号 |  |
| user_no | STRING | column | 用户号 | Y |
| product_type | STRING | column | 产品类型；cash_loan/person_loan |  |
| fund_source | STRING | column | 资金方 |  |
| period | BIGINT | column | 贷款总期数 |  |
| loan_amt | DECIMAL(38,18) | column | 提现金额:元 |  |
| loan_time | DATETIME | column | 放款时间 |  |
| bank_name | STRING | column | 银行 |  |
| pay_order_no | STRING | column | 支付订单号 |  |
| inner_app | STRING | column | 内嵌应用 | Y |
| app | STRING | column | 应用 | Y |
| utm_source | STRING | column | 借款来源（订单表）,如CXH-API-JQNS02 |  |
| cnl_pd_code | STRING | column | 端产品码 |  |
| loan_flag | STRING | column | 首复加贷 | Y |
| asset_type_flag | STRING | column | 资产类型(新老兼容):A24/I24/I36/A36/24+/其他 |  |
| rpy_type | STRING | column | 还款方式:00-等额本金，01-等额本息，02-先息后本,03-等本等息 |  |
| due_day | BIGINT | column | 还款日 |  |
| end_date | DATETIME | column | 贷款止期 |  |
| settle_date | DATETIME | column | 结清日期 |  |
| loan_balance | DECIMAL(38,18) | column | 剩余本金 | Y |
| repay_status | STRING | column | 借据状态:AP-待放款,RP-还款中,OD-逾期中,FP-结清,BD-呆账,WO-坏账 |  |
| overdue_m | STRING | column | 预期阶段：M1/M2.. |  |
| overdue_days | BIGINT | column | 当前逾期天数 | Y |
| max_overdue_days | BIGINT | column | 最大逾期天数 |  |
| settle_period | BIGINT | column | 提前结清所在期数 |  |
| pre_settle_time | DATETIME | column | 提前结清时间 |  |
| last_repay_time | DATETIME | column | 用户最后一次还款时间 |  |
| business_line | STRING | column | app,api,小程序 | Y |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_repay_user_order_df` (
  `order_number` STRING COMMENT '订单号(借据号)',
  `first_order_number` STRING COMMENT '用户真实订单号',
  `apply_id` STRING COMMENT '授信申请流水id',
  `acct_no` STRING COMMENT '账户号',
  `cust_no` STRING COMMENT '客户号',
  `user_no` STRING COMMENT '用户号',
  `product_type` STRING COMMENT '产品类型；cash_loan/person_loan',
  `fund_source` STRING COMMENT '资金方',
  `period` BIGINT COMMENT '贷款总期数',
  `loan_amt` DECIMAL(38,18) COMMENT '提现金额:元',
  `loan_time` DATETIME COMMENT '放款时间',
  `bank_name` STRING COMMENT '银行',
  `pay_order_no` STRING COMMENT '支付订单号',
  `inner_app` STRING COMMENT '内嵌应用',
  `app` STRING COMMENT '应用',
  `utm_source` STRING COMMENT '借款来源（订单表）,如CXH-API-JQNS02',
  `cnl_pd_code` STRING COMMENT '端产品码',
  `loan_flag` STRING COMMENT '首复加贷',
  `asset_type_flag` STRING COMMENT '资产类型(新老兼容):A24/I24/I36/A36/24+/其他',
  `rpy_type` STRING COMMENT '还款方式:00-等额本金，01-等额本息，02-先息后本,03-等本等息',
  `due_day` BIGINT COMMENT '还款日',
  `end_date` DATETIME COMMENT '贷款止期',
  `settle_date` DATETIME COMMENT '结清日期',
  `loan_balance` DECIMAL(38,18) COMMENT '剩余本金',
  `repay_status` STRING COMMENT '借据状态:AP-待放款,RP-还款中,OD-逾期中,FP-结清,BD-呆账,WO-坏账',
  `overdue_m` STRING COMMENT '预期阶段：M1/M2..',
  `overdue_days` BIGINT COMMENT '当前逾期天数',
  `max_overdue_days` BIGINT COMMENT '最大逾期天数',
  `settle_period` BIGINT COMMENT '提前结清所在期数',
  `pre_settle_time` DATETIME COMMENT '提前结清时间',
  `last_repay_time` DATETIME COMMENT '用户最后一次还款时间',
  `business_line` STRING COMMENT 'app,api,小程序'
)
COMMENT '贷中贷后宽表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 3650
```

### 抽样数据
| order_number | first_order_number | apply_id | acct_no | cust_no | user_no | product_type | fund_source | period | loan_amt | loan_time | bank_name | pay_order_no | inner_app | app | utm_source | cnl_pd_code | loan_flag | asset_type_flag | rpy_type | due_day | end_date | settle_date | loan_balance | repay_status | overdue_m | overdue_days | max_overdue_days | settle_period | pre_settle_time | last_repay_time | business_line | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20200101082905014524366 | 20200101082905014524366 | 0075e9529d104d51839359e288167149 | L000081803154606205 | CTL02dfc51e83b6326d4457734fdb0d62dc6 | 1002024197 | cash_loan | sj_cash | 3 | 3000 | 2020-01-01 00:00:00 | 建设银行 | 20010109042148511106 | xyf | xyf | 信用飞APP |  | 复贷 |  | 01 | 29 | 2020-03-29 00:00:00 | 2020-03-13 09:52:25 | 0 | FP | M0 | 0 | 0 | 1 | 2020-01-29 07:32:02 |  |  | 20240923 | 20240923 |
| 20200101092336014524575 | 20200101092336014524575 | 53a85c63e67b47aaa34b82218b4ffd5a | L000081814143125353 | CTL0873b982b6034868e729f5a5dc4bd7b25 | 3339607 | cash_loan | xl_cash | 6 | 5000 | 2020-01-01 09:48:53 | 农业银行 | 20010110173083281202 | xyf | xyf | 信用飞APP |  | 复贷 |  | 01 | 1 | 2020-07-01 00:00:00 | 2020-07-10 17:48:02 | 0 | FP | M0 | 0 | 9 |  |  |  |  | 20240923 | 20240923 |
| 20200101144014014535084 | 20200101144014014535084 | a077b96c96a74b6b87465745fbb514d8 | L000081800124602564 | CTL0297b09691705a5613e6372f47c038509 | 1002361199 | cash_loan | sj_cash | 3 | 3900 | 2020-01-01 00:00:00 | 工商银行 | 20010114530573432763 | xyf | xyf | 信用飞APP |  | 复贷 |  | 01 | 29 | 2020-03-29 00:00:00 | 2020-04-01 11:39:12 | 0 | FP | M0 | 0 | 3 |  |  |  |  | 20240923 | 20240923 |
| 20200101145544014535090 | 20200101145544014535090 | 38b4353aef9342ffb61c38f49dd70419 | L000081803344590402 | CTL0f2a3fe0da34eea4839cb21cd4bdedd5c | 1002310838 | cash_loan | sj_cash | 3 | 3900 | 2020-01-01 00:00:00 | 建设银行 | 20010115226302253054 | xyf | xyf | 信用飞APP |  | 复贷 |  | 01 | 29 | 2020-03-29 00:00:00 | 2020-03-28 20:21:55 | 0 | FP | M0 | 0 | 1 |  |  |  |  | 20240923 | 20240923 |
| 20200102090035014535161 | 20200102090035014535161 | 9610026b57a94713914318f28f2abe95 | L000081809183127460 | CTL0bc4cfbdda88e15931c9b4ec019299edf | 4004665 | cash_loan | xl_cash | 6 | 5000 | 2020-01-02 09:14:30 | 农业银行 | 20010209253891530491 | xyf | xyf | 信用飞APP |  | 复贷 |  | 01 | 2 | 2020-07-02 00:00:00 | 2020-04-28 11:00:42 | 0 | FP | M0 | 0 | 0 | 4 | 2020-04-28 11:00:42 |  |  | 20240923 | 20240923 |

### 同步来源
- `odps`
