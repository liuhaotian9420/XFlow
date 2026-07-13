# xyf_jingying.weekly_analysis_report_df_lss

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| original_order_no | STRING | column | [AI推测] 原始订单号（主订单号） |  |
| order_number | STRING | column | [AI推测] 订单号（子订单号） |  |
| user_no | BIGINT | column | [AI推测] 用户号 |  |
| first_order_number | STRING | column | [AI推测] 首次订单号 |  |
| split_rn | BIGINT | column | [AI推测] 拆单序号 |  |
| 业务线 | STRING | column | [AI推测] 业务线（APP首贷/APP复贷/API首复贷） |  |
| out_order_number | STRING | column | [AI推测] 外部订单号 |  |
| inner_app | STRING | column | [AI推测] 内部渠道标识 |  |
| loan_flag | STRING | column | [AI推测] 贷款标识（首贷/加贷） |  |
| 订单发起时间 | DATETIME | column | [AI推测] 订单发起时间 |  |
| 订单发起日期 | DATE | column | [AI推测] 订单发起日期 |  |
| 订单发起月 | STRING | column | [AI推测] 订单发起月份（yyyy-MM） |  |
| 订单发起周 | STRING | column | [AI推测] 订单发起所在周 |  |
| 风险通过时间 | DATETIME | column | [AI推测] 风控审批通过时间 |  |
| 放款时间 | DATETIME | column | [AI推测] 放款时间 |  |
| 放款日期 | DATE | column | [AI推测] 放款日期 |  |
| 放款月 | STRING | column | [AI推测] 放款月份（yyyy-MM） |  |
| 放款周 | STRING | column | [AI推测] 放款所在周 |  |
| order_amt | DECIMAL(38,18) | column | [AI推测] 订单金额（元） |  |
| loan_amt | DECIMAL(38,18) | column | [AI推测] 放款金额（元） |  |
| 订单期限 | BIGINT | column | [AI推测] 订单期限（期数） |  |
| 风险原始定价 | DOUBLE | column | [AI推测] 风险原始定价费率 |  |
| 资产实际价格 | STRING | column | [AI推测] 资产实际定价（如I36/I24） |  |
| fee_rate | DECIMAL(38,18) | column | [AI推测] 综合费率 |  |
| initial_interest_fee | DECIMAL(38,18) | column | [AI推测] 初始利息费用（元） |  |
| 离线评级 | STRING | column | [AI推测] 离线风控评级（如A1/C2/F） |  |
| 是否额外放开 | INT | column | [AI推测] 是否额外放开（0/1） |  |
| 2h内资金通过 | INT | column | [AI推测] 2小时内资金是否通过（0/1） |  |
| 24h内资金通过 | INT | column | [AI推测] 24小时内资金是否通过（0/1） |  |
| 72h内资金通过 | INT | column | [AI推测] 72小时内资金是否通过（0/1） |  |
| 飞跃在会 | STRING | column | [AI推测] 飞跃会员是否在会（在会/非在会） |  |
| 飞跃在会已扣得 | INT | column | [AI推测] 飞跃在会会员费是否已扣（0/1） |  |
| vip_flow_group | STRING | column | [AI推测] VIP流量分组 |  |
| 飞享在会 | STRING | column | [AI推测] 飞享会员是否在会（在会/非在会） |  |
| 飞享在会已扣得 | INT | column | [AI推测] 飞享在会会员费是否已扣（0/1） |  |
| fy_vip_order_number | STRING | column | [AI推测] 飞跃VIP订单号 |  |
| 飞跃会员卡开始时间 | DATETIME | column | [AI推测] 飞跃会员卡生效时间 |  |
| 飞跃会员卡结束时间 | DATETIME | column | [AI推测] 飞跃会员卡到期时间 |  |
| fx_vip_order_number | STRING | column | [AI推测] 飞享VIP订单号 |  |
| 飞享会员卡开始时间 | DATETIME | column | [AI推测] 飞享会员卡生效时间 |  |
| 飞享会员卡结束时间 | DATETIME | column | [AI推测] 飞享会员卡到期时间 |  |

### DDL
```sql
CREATE TABLE xyf_jingying.`weekly_analysis_report_df_lss` (
  `original_order_no` STRING,
  `order_number` STRING,
  `user_no` BIGINT,
  `first_order_number` STRING,
  `split_rn` BIGINT,
  `业务线` STRING,
  `out_order_number` STRING,
  `inner_app` STRING,
  `loan_flag` STRING,
  `订单发起时间` DATETIME,
  `订单发起日期` DATE,
  `订单发起月` STRING,
  `订单发起周` STRING,
  `风险通过时间` DATETIME,
  `放款时间` DATETIME,
  `放款日期` DATE,
  `放款月` STRING,
  `放款周` STRING,
  `order_amt` DECIMAL(38,18),
  `loan_amt` DECIMAL(38,18),
  `订单期限` BIGINT,
  `风险原始定价` DOUBLE,
  `资产实际价格` STRING,
  `fee_rate` DECIMAL(38,18),
  `initial_interest_fee` DECIMAL(38,18),
  `离线评级` STRING,
  `是否额外放开` INT,
  `2h内资金通过` INT,
  `24h内资金通过` INT,
  `72h内资金通过` INT,
  `飞跃在会` STRING,
  `飞跃在会已扣得` INT,
  `vip_flow_group` STRING,
  `飞享在会` STRING,
  `飞享在会已扣得` INT,
  `fy_vip_order_number` STRING,
  `飞跃会员卡开始时间` DATETIME,
  `飞跃会员卡结束时间` DATETIME,
  `fx_vip_order_number` STRING,
  `飞享会员卡开始时间` DATETIME,
  `飞享会员卡结束时间` DATETIME
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| original_order_no | order_number | user_no | first_order_number | split_rn | 业务线 | out_order_number | inner_app | loan_flag | 订单发起时间 | 订单发起日期 | 订单发起月 | 订单发起周 | 风险通过时间 | 放款时间 | 放款日期 | 放款月 | 放款周 | order_amt | loan_amt | 订单期限 | 风险原始定价 | 资产实际价格 | fee_rate | initial_interest_fee | 离线评级 | 是否额外放开 | 2h内资金通过 | 24h内资金通过 | 72h内资金通过 | 飞跃在会 | 飞跃在会已扣得 | vip_flow_group | 飞享在会 | 飞享在会已扣得 | fy_vip_order_number | 飞跃会员卡开始时间 | 飞跃会员卡结束时间 | fx_vip_order_number | 飞享会员卡开始时间 | 飞享会员卡结束时间 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025070100123600000040002622 | 2025070100123700000021970795 | 1107480518 | 2025070100123600000040002622 | 1 | APP复贷 |  | xyf01 | 加贷 | 2025-07-01 00:01:44 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 2025-07-01 00:33:08 | 2025-07-01 00:46:06 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 5300 | 5300 | 3 | 0.36 | I36 | 0.3599 | 321.04 | A1 | 0 | 1 | 1 | 1 | 非在会 | 0 |  | 非在会 | 0 |  |  |  |  |  |  |
| 2025070100123600000040002624 | 2025070100123700000022005912 | 1101297832 | 2025070100123600000040002624 | 1 | APP复贷 |  | xyf01 | 加贷 | 2025-07-01 00:02:34 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 2025-07-01 00:34:08 | 2025-07-01 00:51:26 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 15000 | 15000 | 12 | 0.36 | I36 | 0.3599 | 3082.2 | F | 0 | 1 | 1 | 1 | 非在会 | 0 |  | 非在会 | 0 |  |  |  |  |  |  |
| 2025070100123600000040002791 | 2025070100123700000021981501 | 1266600887 | 2025070100123600000040002791 | 1 | APP复贷 |  | xyf01 | 加贷 | 2025-07-01 00:03:34 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 2025-07-01 00:03:35 | 2025-07-01 00:07:12 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 1000 | 1000 | 6 | 0.36 | I36 | 0.3599 | 107.54 | C2 | 0 | 1 | 1 | 1 | 非在会 | 0 |  | 在会 | 1 |  |  |  | vcvip113827704 | 2025-06-28 23:44:30 | 2025-09-26 23:59:59 |
| 2025070100123600000040003077 | 2025070100123700000021989251 | 1141906422 | 2025070100123600000040003077 | 1 | API首复贷 | msxj_2778783580040462984 | xyf01_msxj | 首贷 | 2025-07-01 00:03:32 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 2025-07-01 00:10:00 | 2025-07-01 00:21:18 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 22500 | 22500 | 12 | 0.36 | I36 | 0.3599 | 4623.36 |  | 0 | 1 | 1 | 1 | 非在会 | 0 |  | 非在会 | 0 |  |  |  |  |  |  |
| 2025070100123600000040003857 | 2025070300123700000023819815 | 1141353927 | 2025070100123600000040003857 | 1 | APP首贷 |  | xyf01 | 首贷 | 2025-07-01 00:11:38 | 2025-07-01 | 2025-07 | 2025-06-27至2025-07-03 | 2025-07-01 00:13:09 |  |  |  |  | 16000 | 16000 | 12 | 0.36 | I36 |  |  |  | 0 | 0 | 0 | 0 | 非在会 | 0 |  | 非在会 | 0 |  |  |  |  |  |  |

## 同步来源
- `odps`
