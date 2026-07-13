# xyf_dwd.dwd_user_tek_order_df

## 来源文件
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 老客月会sql代码.ipynb

- `'tek' AS card_type`
- `'复贷' AS vip_classifier`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `order_time AS tran_time`
- `real_order_price AS pay_amt`
- `refund_amount AS refund_amt`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| app_user_id | STRING | column | app_user_id | Y |
| id_card_number | STRING | column | 身份证号 |  |
| cust_no | STRING | column | 客户编号 | Y |
| order_time | DATETIME | column | 购卡时间 | Y |
| order_no | BIGINT | column | 购卡订单号 |  |
| origin_price | DOUBLE | column | 展示价格 |  |
| real_order_price | DOUBLE | column | 购卡价格 | Y |
| is_coupon | STRING | column | 是否使用优惠券 |  |
| coupon_amt | DOUBLE | column | 优惠金额 |  |
| limit_result | STRING | column | 提额结果 |  |
| limit_amt | DOUBLE | column | 提额额度 |  |
| status | STRING | column | 最终额度使用结果 |  |
| pay_type | STRING | column | 支付方式 |  |
| loan_order_number | STRING | column | 使用提额卡额度的发起订单号 |  |
| loan_order_status | STRING | column | 借款结果 |  |
| loan_order_create_time | DATETIME | column | 购卡提额后发起时间 |  |
| loan_order_amt | DECIMAL(38,18) | column | 购卡提额后发起金额 |  |
| first_refund_time | DATETIME | column | 首次退卡发起时间 |  |
| first_refund_reason | STRING | column | 首次退卡原因 |  |
| first_refund_operator | STRING | column | 首次退款操作人 |  |
| first_refund_status | STRING | column | 首次退款状态 |  |
| last_refund_time | DATETIME | column | 末次退卡发起时间 |  |
| last_refund_reason | STRING | column | 末次退卡原因 |  |
| last_refund_operator | STRING | column | 末次退款操作人 |  |
| last_refund_status | STRING | column | 末次退款状态 |  |
| act_refund_time | DATETIME | column | 退款实际到账时间 | Y |
| end_time | DATETIME | column | 会员结束时间 |  |
| refund_amount | DECIMAL(10,2) | column | 退款金额 | Y |
| buy_source | STRING | column | 购买来源 |  |
| app | STRING | column | app |  |
| user_type | STRING | column | 用户类型：1-首贷2-加贷3-复贷 |  |
| pt | STRING | column | 分区日期 | Y |
| pt | STRING | partition | 分区日期 | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_user_tek_order_df` (
  `app_user_id` STRING COMMENT 'app_user_id',
  `id_card_number` STRING COMMENT '身份证号',
  `cust_no` STRING COMMENT '客户编号',
  `order_time` DATETIME COMMENT '购卡时间',
  `order_no` BIGINT COMMENT '购卡订单号',
  `origin_price` DOUBLE COMMENT '展示价格',
  `real_order_price` DOUBLE COMMENT '购卡价格',
  `is_coupon` STRING COMMENT '是否使用优惠券',
  `coupon_amt` DOUBLE COMMENT '优惠金额',
  `limit_result` STRING COMMENT '提额结果',
  `limit_amt` DOUBLE COMMENT '提额额度',
  `status` STRING COMMENT '最终额度使用结果',
  `pay_type` STRING COMMENT '支付方式',
  `loan_order_number` STRING COMMENT '使用提额卡额度的发起订单号',
  `loan_order_status` STRING COMMENT '借款结果',
  `loan_order_create_time` DATETIME COMMENT '购卡提额后发起时间',
  `loan_order_amt` DECIMAL(38,18) COMMENT '购卡提额后发起金额',
  `first_refund_time` DATETIME COMMENT '首次退卡发起时间',
  `first_refund_reason` STRING COMMENT '首次退卡原因',
  `first_refund_operator` STRING COMMENT '首次退款操作人',
  `first_refund_status` STRING COMMENT '首次退款状态',
  `last_refund_time` DATETIME COMMENT '末次退卡发起时间',
  `last_refund_reason` STRING COMMENT '末次退卡原因',
  `last_refund_operator` STRING COMMENT '末次退款操作人',
  `last_refund_status` STRING COMMENT '末次退款状态',
  `act_refund_time` DATETIME COMMENT '退款实际到账时间',
  `end_time` DATETIME COMMENT '会员结束时间',
  `refund_amount` DECIMAL(10,2) COMMENT '退款金额',
  `buy_source` STRING COMMENT '购买来源',
  `app` STRING COMMENT 'app',
  `user_type` STRING COMMENT '用户类型：1-首贷2-加贷3-复贷'
)
COMMENT '用户提额卡购卡订单表'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '分区日期'
)
STORED AS AliOrc
LIFECYCLE 3650
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C671E83D3BD39C93E7D4F0 Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
