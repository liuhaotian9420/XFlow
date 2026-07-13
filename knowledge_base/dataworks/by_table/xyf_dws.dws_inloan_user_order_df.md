# xyf_dws.dws_inloan_user_order_df

## 来源文件
- ads_inloan_loan_balance_mthly_df.sql
- ads_inloan_loan_monitor_screen_df.sql
- ads_inloan_loan_pass_monitor_df.sql
- APP新客转化-授信口径.ipynb
- APP新客转化-注册口径.ipynb
- dws_inloan_loan_channel_stat_df.sql
- dws_inloan_loan_pass_stat_df.sql
- dws_inloan_loan_risk_stat_df.sql
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

- `COUNT(DISTINCT cust_no) act_added_c_mthly_id`
- `a.user_no AS app_user_id`
- `substr(loan_time,1,7) AS loan_month`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| first_order_number | STRING | column | 用户真实订单号 | Y |
| fund_order_number | STRING | column | 资方订单号 |  |
| first_order_time | DATETIME | column | 用户申请时间 | Y |
| user_no | BIGINT | column | 用户号 cis系统 app+mobile |  |
| cust_no | STRING | column | 客户号 | Y |
| product_type | STRING | column | 产品类型；cash_loan/person_loan |  |
| fund_source | STRING | column | 资金方 |  |
| period | BIGINT | column | 贷款总期数 |  |
| loan_amt | DECIMAL(38,18) | column | 放款成功金额:元，订单成功状态的金额 | Y |
| loan_time | DATETIME | column | 放款时间 | Y |
| inner_app | STRING | column | 内嵌应用 | Y |
| app | STRING | column | 应用 | Y |
| utm_source | STRING | column | 借款来源（订单表）,如CXH-API-JQNS02 |  |
| loan_status | STRING | column | 订单状态:success成功/failed失败 /none/process处理中 | Y |
| failed_code | STRING | column | 失败码 |  |
| failed_reason | STRING | column | 失败原因 |  |
| risk_status | STRING | column | 风控审核状态 | Y |
| cnl_pd_code | STRING | column | 端产品码 |  |
| biz_flow_number | STRING | column | 进件流水号 |  |
| coupon_id | BIGINT | column | 优惠券id |  |
| out_order_number | STRING | column | 外部进件号 |  |
| order_route | BIGINT | column | 最终路由次数 |  |
| loan_flag | STRING | column | 首复加贷 | Y |
| order_number | STRING | column | 轮训最后一笔订单( 没进路由就是用户订单) |  |
| apply_cust_product_no | BIGINT | column | 订单排序（用户+产品） |  |
| loan_cust_product_no | BIGINT | column | 成功订单排序（用户+产品） |  |
| apply_id | STRING | column | 授信申请流水id |  |
| ori_loan_status | STRING | column | 订单原始状态00:待处理 01:风控审核中 11:风控审核通过 20:放款处理中 03:交易成功 04:交易失败	 |  |
| asset_type_flag | STRING | column | 资产类型(新老兼容):A24/I24/I36/A36/24+/其他 | Y |
| ua_loan_order_no | STRING | column | 外部订单号 |  |
| fee_rate | DECIMAL(38,18) | column | 利率 |  |
| first_order_no | STRING | column | 首笔授信单号（用于关联重复收单的第一笔授信单号） |  |
| source | STRING | column | 下单来源 |  |
| business_line | STRING | column | app,api,小程序 | Y |
| device_id | STRING | column | 设备id |  |
| is_split_order | STRING | column | 是否拆分订单：0否 1是 |  |
| original_order_no | STRING | column | 原始订单号 |  |
| date_applied | DATETIME | column | 申请时间 |  |
| freeze_type | STRING | column | 冻额标识(0未冻额,1已冻额,2冻额后降额) |  |
| freeze_loan_req_no | STRING | column | 冻额订单号(降额订单专有) |  |
| order_amt | DECIMAL(38,18) | column | 申请金额，拆单前主订单号上申请金额 |  |
| order_split_num | BIGINT | column | 拆分笔数，拆分后订单数据，不看状态 |  |
| order_split_status | STRING | column | 拆单订单状态,申请金额=放款金额：成功 申请金额>放款金额且放款金额>0 ：部分成功 放款金额=0：放款失败 |  |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dws.`dws_inloan_user_order_df` (
  `first_order_number` STRING COMMENT '用户真实订单号',
  `fund_order_number` STRING COMMENT '资方订单号',
  `first_order_time` DATETIME COMMENT '用户申请时间',
  `user_no` BIGINT COMMENT '用户号 cis系统 app+mobile',
  `cust_no` STRING COMMENT '客户号',
  `product_type` STRING COMMENT '产品类型；cash_loan/person_loan',
  `fund_source` STRING COMMENT '资金方',
  `period` BIGINT COMMENT '贷款总期数',
  `loan_amt` DECIMAL(38,18) COMMENT '放款成功金额:元，订单成功状态的金额',
  `loan_time` DATETIME COMMENT '放款时间',
  `inner_app` STRING COMMENT '内嵌应用',
  `app` STRING COMMENT '应用',
  `utm_source` STRING COMMENT '借款来源（订单表）,如CXH-API-JQNS02',
  `loan_status` STRING COMMENT '订单状态:success成功/failed失败 /none/process处理中',
  `failed_code` STRING COMMENT '失败码',
  `failed_reason` STRING COMMENT '失败原因',
  `risk_status` STRING COMMENT '风控审核状态',
  `cnl_pd_code` STRING COMMENT '端产品码',
  `biz_flow_number` STRING COMMENT '进件流水号',
  `coupon_id` BIGINT COMMENT '优惠券id',
  `out_order_number` STRING COMMENT '外部进件号',
  `order_route` BIGINT COMMENT '最终路由次数',
  `loan_flag` STRING COMMENT '首复加贷',
  `order_number` STRING COMMENT '轮训最后一笔订单( 没进路由就是用户订单)',
  `apply_cust_product_no` BIGINT COMMENT '订单排序（用户+产品）',
  `loan_cust_product_no` BIGINT COMMENT '成功订单排序（用户+产品）',
  `apply_id` STRING COMMENT '授信申请流水id',
  `ori_loan_status` STRING COMMENT '订单原始状态00:待处理 01:风控审核中 11:风控审核通过 20:放款处理中 03:交易成功 04:交易失败\t',
  `asset_type_flag` STRING COMMENT '资产类型(新老兼容):A24/I24/I36/A36/24+/其他',
  `ua_loan_order_no` STRING COMMENT '外部订单号',
  `fee_rate` DECIMAL(38,18) COMMENT '利率',
  `first_order_no` STRING COMMENT '首笔授信单号（用于关联重复收单的第一笔授信单号）',
  `source` STRING COMMENT '下单来源',
  `business_line` STRING COMMENT 'app,api,小程序',
  `device_id` STRING COMMENT '设备id',
  `is_split_order` STRING COMMENT '是否拆分订单：0否 1是',
  `original_order_no` STRING COMMENT '原始订单号',
  `date_applied` DATETIME COMMENT '申请时间',
  `freeze_type` STRING COMMENT '冻额标识(0未冻额,1已冻额,2冻额后降额)',
  `freeze_loan_req_no` STRING COMMENT '冻额订单号(降额订单专有)',
  `order_amt` DECIMAL(38,18) COMMENT '申请金额，拆单前主订单号上申请金额',
  `order_split_num` BIGINT COMMENT '拆分笔数，拆分后订单数据，不看状态',
  `order_split_status` STRING COMMENT '拆单订单状态,申请金额=放款金额：成功 申请金额>放款金额且放款金额>0 ：部分成功 放款金额=0：放款失败'
)
COMMENT '订单用户申请视角'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 720
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C6721311BAD49FB8E88E1D Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
