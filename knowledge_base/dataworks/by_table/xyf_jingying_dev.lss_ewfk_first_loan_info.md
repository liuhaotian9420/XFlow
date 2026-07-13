# xyf_jingying_dev.lss_ewfk_first_loan_info

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| 订单发起日期 | DATE | column | [AI推测] 订单发起日期 |  |
| 订单发起月 | STRING | column | [AI推测] 订单发起月份（yyyy-MM） |  |
| 放款日期 | DATE | column | [AI推测] 放款日期 |  |
| 放款月 | STRING | column | [AI推测] 放款月份（yyyy-MM） |  |
| order_number | STRING | column | [AI推测] 订单号 |  |
| user_no | BIGINT | column | [AI推测] 用户号 |  |
| cust_no | STRING | column | [AI推测] 客户号 |  |
| first_order_number | STRING | column | [AI推测] 首次订单号 |  |
| app | STRING | column | [AI推测] 应用标识 |  |
| inner_app | STRING | column | [AI推测] 内部渠道标识 |  |
| business_line | STRING | column | [AI推测] 业务线（APP/API） |  |
| loan_flag | STRING | column | [AI推测] 贷款标识（首贷） |  |
| first_order_time | DATETIME | column | [AI推测] 首次订单发起时间 |  |
| loan_time | DATETIME | column | [AI推测] 放款时间 |  |
| loan_amt | DECIMAL(38,18) | column | [AI推测] 放款金额（元） |  |
| period | BIGINT | column | [AI推测] 贷款期数 |  |
| asset_type_flag | STRING | column | [AI推测] 资产定价类型（I24/I36） |  |
| fee_rate | DECIMAL(38,18) | column | [AI推测] 综合费率 |  |
| biz_flow_number | STRING | column | [AI推测] 业务流水号 |  |
| 授信金额 | DOUBLE | column | [AI推测] 授信金额（元） |  |
| 授信额度区间 | STRING | column | [AI推测] 授信额度区间 |  |
| 授信时间 | DATETIME | column | [AI推测] 授信时间 |  |
| 授信inner_app | STRING | column | [AI推测] 授信渠道内部标识 |  |
| 授信user_no | STRING | column | [AI推测] 授信用户号 |  |
| 授信渠道 | STRING | column | [AI推测] 授信渠道（APP/API） |  |
| is_虚假给额 | INT | column | [AI推测] 是否虚假给额（0/1） |  |
| 虚假给额类型 | STRING | column | [AI推测] 虚假给额类型（APP虚假给额/非虚假给额） |  |

### DDL
```sql
CREATE TABLE xyf_jingying_dev.`lss_ewfk_first_loan_info` (
  `订单发起日期` DATE,
  `订单发起月` STRING,
  `放款日期` DATE,
  `放款月` STRING,
  `order_number` STRING,
  `user_no` BIGINT,
  `cust_no` STRING,
  `first_order_number` STRING,
  `app` STRING,
  `inner_app` STRING,
  `business_line` STRING,
  `loan_flag` STRING,
  `first_order_time` DATETIME,
  `loan_time` DATETIME,
  `loan_amt` DECIMAL(38,18),
  `period` BIGINT,
  `asset_type_flag` STRING,
  `fee_rate` DECIMAL(38,18),
  `biz_flow_number` STRING,
  `授信金额` DOUBLE,
  `授信额度区间` STRING,
  `授信时间` DATETIME,
  `授信inner_app` STRING,
  `授信user_no` STRING,
  `授信渠道` STRING,
  `is_虚假给额` INT,
  `虚假给额类型` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| 订单发起日期 | 订单发起月 | 放款日期 | 放款月 | order_number | user_no | cust_no | first_order_number | app | inner_app | business_line | loan_flag | first_order_time | loan_time | loan_amt | period | asset_type_flag | fee_rate | biz_flow_number | 授信金额 | 授信额度区间 | 授信时间 | 授信inner_app | 授信user_no | 授信渠道 | is_虚假给额 | 虚假给额类型 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-01-01 | 2025-01 |  |  | 2025010100123600000016904612 | 1129562082 | CTL01d82650ab49fc2ce19e4f9eb8b8fee56 | 2025010100123600000016904612 | xyf01 | xyf01 | APP | 首贷 | 2025-01-01 00:00:09 |  | 0 | 3 | I36 |  | 2025010100123600000016904612 | 1000.0 | [0-1000] | 2024-12-31 22:32:03 | xyf01 | 1129562082 | APP | 1 | APP虚假给额 |
| 2025-01-01 | 2025-01 |  |  | 2025010100123600000016904934 | 1102446728 | CTL09cfa1f57897298fc8f3baddc7ee6f29f | 2025010100123600000016904934 | xyf01 | xyf01 | APP | 首贷 | 2025-01-01 00:01:36 |  | 0 | 6 | I36 |  | 2025010100123600000016904934 | 1000.0 | [0-1000] | 2024-08-02 20:52:29 | xyf01_xykd | 1102446728 | API | 0 | 非虚假给额 |
| 2025-01-01 | 2025-01 |  |  | 2025010100123600000016905621 | 1276423812 | CTL06e30e0c141d9d773339096f041b48262 | 2025010100123600000016905621 | xyf01 | xyf01 | APP | 首贷 | 2025-01-01 00:09:33 |  | 0 | 6 | I24 |  | 2025010100123600000016905621 | 500.0 | [0-1000] | 2025-01-01 00:07:29 | xyf01 | 1276423812 | APP | 0 | 非虚假给额 |
| 2025-01-01 | 2025-01 |  |  | 2025010100123600000016905753 | 1275363217 | CTL0fafb657d876360a0adda51decb0e42bf | 2025010100123600000016905753 | xyf01 | xyf01 | APP | 首贷 | 2025-01-01 00:14:59 |  | 0 | 6 | I36 |  | 2025010100123600000016905753 | 1000.0 | [0-1000] | 2024-12-29 22:45:40 | xyf01 | 1275363217 | APP | 1 | APP虚假给额 |
| 2025-01-01 | 2025-01 |  |  | 2025010100123600000016906331 | 1255883214 | CTL017cf93c9ffde893ae13a9c77db9ff71f | 2025010100123600000016906331 | xyf01 | xyf01 | APP | 首贷 | 2025-01-01 00:27:33 |  | 0 | 6 | I36 |  | 2025010100123600000016906331 | 1000.0 | [0-1000] | 2024-12-24 17:58:42 | xyf01 | 1255883214 | APP | 1 | APP虚假给额 |

## 同步来源
- `odps`
