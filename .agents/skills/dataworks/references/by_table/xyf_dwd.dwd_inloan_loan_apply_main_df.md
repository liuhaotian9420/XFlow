# xyf_dwd.dwd_inloan_loan_apply_main_df

## 来源文件
- xyf_jingying.weekly_analysis_report_df_lss.txt
- 老客月会sql代码.ipynb

- 无

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| ori_order_number | STRING | column | 主订单号 | Y |
| acct_no | STRING | column | 账户号 |  |
| cust_no | STRING | column | 客户号 |  |
| user_no | BIGINT | column | 用户号 cis系统 app+mobile |  |
| product_type | STRING | column | 产品代码 |  |
| product_group_no | STRING | column | 产品组合编码 |  |
| sub_product_code | STRING | column | 子产品代码 |  |
| sub_product_ver | BIGINT | column | 子产品版本号 |  |
| appoint_third_code | STRING | column | 指定子资金 |  |
| risk_status | STRING | column | 风险状态 |  |
| status_code | STRING | column | 借据申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝,99-其它 |  |
| loan_amt | DECIMAL(38,18) | column | 借款金额 |  |
| date_cash | DATETIME | column | 资金到账日期 |  |
| term | BIGINT | column | 期数 |  |
| rpy_type | STRING | column | 还款方式:00-等额本金，01-等额本息，02-先息后本 |  |
| bank_code | STRING | column | 银行代码 |  |
| db_acct | STRING | column | 放款卡号 |  |
| db_acct_name | STRING | column | 放款账户名称 |  |
| offer_req_no | STRING | column | 报盘流水号 |  |
| loan_purpose | STRING | column | 贷款用途 |  |
| inner_app | STRING | column | 资金动用渠道 |  |
| app | STRING | column | 旧系统中的App字段(非真实App) |  |
| remark | STRING | column | 备注 |  |
| date_created | DATETIME | column | 创建时间 |  |
| trd_loan_req_no | STRING | column | 三方借款请求流水号 |  |
| risk_price_type | STRING | column | 用户风险定价类型A或I | Y |
| risk_price | DECIMAL(38,18) | column | 用户风险定价 | Y |
| coupon_id | BIGINT | column | 优惠劵id |  |
| bankcard_id | STRING | column | 银行卡id |  |
| is_again_loan | BIGINT | column | 是否是复贷订单 0:不是，1:是 |  |
| loan_no | STRING | column | 借据号 |  |
| contract_number | STRING | column | 合同编号 |  |
| fund_source | STRING | column | 资金方 |  |
| third_code | STRING | column | 第三方编码 |  |
| failed_code | STRING | column | 失败编码 |  |
| failed_reason | STRING | column | 失败原因 |  |
| utm_source | STRING | column | 来源 |  |
| flow_id | STRING | column | 流程id |  |
| biz_type | STRING | column | 业务类型，预留字段 |  |
| ext_info | STRING | column | 扩展字段 |  |
| system | BIGINT | column | 系统来源, 0: credit_system,1:lendtrade |  |
| version | BIGINT | column | 版本号 |  |
| biz_data | STRING | column | 业务数据 |  |
| fund_fee_rate | DECIMAL(38,18) | column | 资方年利率 |  |
| cnl_no | STRING | column | 端流水号 |  |
| cnl_pd_code | STRING | column | 端产品码 |  |
| cnl_ev_code | STRING | column | 端事件码 |  |
| white_list_type | STRING | column | financial_institution_whitelist:资金白名单，uat_whitelist:员工白名单 |  |
| freeze_type | STRING | column | 冻额标识(0未冻额,1已冻额,2冻额后降额) |  |
| freeze_loan_req_no | STRING | column | 冻额订单号(降额订单专有) |  |
| source | STRING | column | 下单来源 |  |
| device_id | STRING | column | 设备id |  |
| created_ip | STRING | column | 创单ip |  |
| source_type | STRING | column | 来源类型：client 客户端，wap 移动web端 |  |
| is_screen | BIGINT | column | 是否前筛 |  |
| special_type | STRING | column | 订单特殊标识:0无特殊标识,1免息贷 |  |
| freeze_code | STRING | column | 冻结编码 |  |
| ori_risk_price_type | STRING | column | 原始用户风险定价类型 A或I |  |
| ori_risk_price | DECIMAL(38,18) | column | 原始用户风险定价 | Y |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_inloan_loan_apply_main_df` (
  `ori_order_number` STRING COMMENT '主订单号',
  `acct_no` STRING COMMENT '账户号',
  `cust_no` STRING COMMENT '客户号',
  `user_no` BIGINT COMMENT '用户号 cis系统 app+mobile',
  `product_type` STRING COMMENT '产品代码',
  `product_group_no` STRING COMMENT '产品组合编码',
  `sub_product_code` STRING COMMENT '子产品代码',
  `sub_product_ver` BIGINT COMMENT '子产品版本号',
  `appoint_third_code` STRING COMMENT '指定子资金',
  `risk_status` STRING COMMENT '风险状态',
  `status_code` STRING COMMENT '借据申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝,99-其它',
  `loan_amt` DECIMAL(38,18) COMMENT '借款金额',
  `date_cash` DATETIME COMMENT '资金到账日期',
  `term` BIGINT COMMENT '期数',
  `rpy_type` STRING COMMENT '还款方式:00-等额本金，01-等额本息，02-先息后本',
  `bank_code` STRING COMMENT '银行代码',
  `db_acct` STRING COMMENT '放款卡号',
  `db_acct_name` STRING COMMENT '放款账户名称',
  `offer_req_no` STRING COMMENT '报盘流水号',
  `loan_purpose` STRING COMMENT '贷款用途',
  `inner_app` STRING COMMENT '资金动用渠道',
  `app` STRING COMMENT '旧系统中的App字段(非真实App)',
  `remark` STRING COMMENT '备注',
  `date_created` DATETIME COMMENT '创建时间',
  `trd_loan_req_no` STRING COMMENT '三方借款请求流水号',
  `risk_price_type` STRING COMMENT '用户风险定价类型A或I',
  `risk_price` DECIMAL(38,18) COMMENT '用户风险定价',
  `coupon_id` BIGINT COMMENT '优惠劵id',
  `bankcard_id` STRING COMMENT '银行卡id',
  `is_again_loan` BIGINT COMMENT '是否是复贷订单 0:不是，1:是',
  `loan_no` STRING COMMENT '借据号',
  `contract_number` STRING COMMENT '合同编号',
  `fund_source` STRING COMMENT '资金方',
  `third_code` STRING COMMENT '第三方编码',
  `failed_code` STRING COMMENT '失败编码',
  `failed_reason` STRING COMMENT '失败原因',
  `utm_source` STRING COMMENT '来源',
  `flow_id` STRING COMMENT '流程id',
  `biz_type` STRING COMMENT '业务类型，预留字段',
  `ext_info` STRING COMMENT '扩展字段',
  `system` BIGINT COMMENT '系统来源, 0: credit_system,1:lendtrade',
  `version` BIGINT COMMENT '版本号',
  `biz_data` STRING COMMENT '业务数据',
  `fund_fee_rate` DECIMAL(38,18) COMMENT '资方年利率',
  `cnl_no` STRING COMMENT '端流水号',
  `cnl_pd_code` STRING COMMENT '端产品码',
  `cnl_ev_code` STRING COMMENT '端事件码',
  `white_list_type` STRING COMMENT 'financial_institution_whitelist:资金白名单，uat_whitelist:员工白名单',
  `freeze_type` STRING COMMENT '冻额标识(0未冻额,1已冻额,2冻额后降额)',
  `freeze_loan_req_no` STRING COMMENT '冻额订单号(降额订单专有)',
  `source` STRING COMMENT '下单来源',
  `device_id` STRING COMMENT '设备id',
  `created_ip` STRING COMMENT '创单ip',
  `source_type` STRING COMMENT '来源类型：client 客户端，wap 移动web端',
  `is_screen` BIGINT COMMENT '是否前筛',
  `special_type` STRING COMMENT '订单特殊标识:0无特殊标识,1免息贷',
  `freeze_code` STRING COMMENT '冻结编码',
  `ori_risk_price_type` STRING COMMENT '原始用户风险定价类型 A或I',
  `ori_risk_price` DECIMAL(38,18) COMMENT '原始用户风险定价'
)
COMMENT '现金贷主订单申请明细表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 62
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C671CE3D3BD39C93E7B35B Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
