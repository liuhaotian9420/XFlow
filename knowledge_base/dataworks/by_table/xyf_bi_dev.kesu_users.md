# xyf_bi_dev.kesu_users

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| month_cj | STRING | column | [AI推测] 创建月份 |  |
| is_zq | STRING | column | [AI推测] 是否诈骗 |  |
| cust_no | STRING | column | [AI推测] 客户号 |  |
| id_card_number | STRING | column | [AI推测] 身份证号（加密） |  |
| task_type_name_new | STRING | column | [AI推测] 工单类型（新分类） |  |
| order_number_source | STRING | column | [AI推测] 订单来源渠道（APP/API） |  |
| channel_1_type_new | STRING | column | [AI推测] 一级投诉渠道（新分类） |  |
| order_number1 | STRING | column | [AI推测] 关联订单号 |  |
| cust_status | STRING | column | [AI推测] 客户贷款状态（在贷/结清） |  |
| task_number | STRING | column | [AI推测] 工单编号 |  |
| cjdate | STRING | column | [AI推测] 创建日期 |  |

### DDL
```sql
CREATE TABLE xyf_bi_dev.`kesu_users` (
  `month_cj` STRING,
  `is_zq` STRING,
  `cust_no` STRING,
  `id_card_number` STRING,
  `task_type_name_new` STRING,
  `order_number_source` STRING,
  `channel_1_type_new` STRING,
  `order_number1` STRING,
  `cust_status` STRING,
  `task_number` STRING,
  `cjdate` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| month_cj | is_zq | cust_no | id_card_number | task_type_name_new | order_number_source | channel_1_type_new | order_number1 | cust_status | task_number | cjdate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2025-01 | 否 | CTL0d45103c40d9843f35195a2dcd5ea17f8 | oXmEvry0tPwaxQswe0Mg+K9sf8QcmmCgekR67nY+RRM= | 费用问题 | APP | 内部 | 2024123100123700000046739207 | 在贷 | 2025010109151700384 | 2025-01-01 |
| 2025-01 | 否 | CTL08418a7f12ae131feaf91724e895c6f41 | 493B/dXrgqnKF3yAKzwmWDSp1fGzgxlXA4JfpqNkQTo= | 费用问题 | API | 内部 | 202107301224240213458744 | 结清 | 2025010109155700389 | 2025-01-01 |
| 2025-01 | 否 | CTL02a006cb9b0686fe1d5794d24293a75b1 | oXiEiKy9loQyZZXGmr7lpi4UmcYZPUi6Nao75nxycXk= | 费用问题 | APP | 内部 | 202309231716330256025559 | 结清 | 2025010109251400436 | 2025-01-01 |
| 2025-01 | 否 | CTL0fc0ffe6ff13a3eb109d936a0c1eb5815 | duQNAzC/nLDpKolfnIOGsxm8rScW3YvCkNpvW6YFgAs= | 费用问题 | APP | 内部 | 2024122300123700000044846988 | 在贷 | 2025010109253800440 | 2025-01-01 |
| 2025-01 | 否 | CTL0fac317945acb4af4d0c217e2196bfd6c | Suauy/q+mrj8vqgQaO7SODF0jz7Ep2o81tpmZnP/I7s= | 费用问题 | APP | 黑猫 | 2024121400123700000043150759 | 在贷 | 2025010109300400474 | 2025-01-01 |

## 同步来源
- `odps`
