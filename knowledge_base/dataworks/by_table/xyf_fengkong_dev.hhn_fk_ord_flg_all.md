# xyf_fengkong_dev.hhn_fk_ord_flg_all

## 来源文件
- 老客月会sql代码.ipynb

- `DISTINCT order_number`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | [AI推测] 订单号 |  |
| ori_order_number | STRING | column | [AI推测] 原始订单号 |  |
| 复贷客群分组 | STRING | column | [AI推测] 复贷客群分组（如提额卡等） | Y |
| created_time | DATETIME | column | [AI推测] 订单创建时间 |  |
| decision_time | DATETIME | column | [AI推测] 风控决策时间 |  |
| ord_flg | STRING | column | [AI推测] 订单风控标记（额外放开/非额外放开） |  |
| fenzu_lb | STRING | column | [AI推测] 分组类别/策略版本（如V2.1/V4） |  |
| b_order_number | STRING | column | [AI推测] 关联B订单号 |  |
| tek_apl_amt_rte | DOUBLE | column | [AI推测] 提额卡申请金额费率 |  |
| vip_apl_amt_rte | DOUBLE | column | [AI推测] VIP申请金额费率 |  |
| fy_vip_apl_amt_rte | DOUBLE | column | [AI推测] 飞跃VIP申请金额费率 |  |
| personalloan_fd_creditlevel_level_user_group_v8_36_tek | STRING | column | [AI推测] 个人贷信用等级_用户分组V8_36期_提额卡 |  |
| personalloan_fd_creditlevel_level_user_group_v8_1_36_tek | STRING | column | [AI推测] 个人贷信用等级_用户分组V8.1_36期_提额卡 |  |
| personalloan_fd_creditlevel_level_user_group_v8_36 | STRING | column | [AI推测] 个人贷信用等级_用户分组V8_36期 |  |
| personalloan_fd_creditlevel_level_user_group_v8_1_36 | STRING | column | [AI推测] 个人贷信用等级_用户分组V8.1_36期 |  |
| qyk_apl_amt_rte_100 | STRING | column | [AI推测] 全域客申请金额费率（百分制） |  |

#### DDL
```sql
CREATE TABLE xyf_fengkong_dev.`hhn_fk_ord_flg_all` (
  `order_number` STRING,
  `ori_order_number` STRING,
  `复贷客群分组` STRING,
  `created_time` DATETIME,
  `decision_time` DATETIME,
  `ord_flg` STRING,
  `fenzu_lb` STRING,
  `b_order_number` STRING,
  `tek_apl_amt_rte` DOUBLE,
  `vip_apl_amt_rte` DOUBLE,
  `fy_vip_apl_amt_rte` DOUBLE,
  `personalloan_fd_creditlevel_level_user_group_v8_36_tek` STRING,
  `personalloan_fd_creditlevel_level_user_group_v8_1_36_tek` STRING,
  `personalloan_fd_creditlevel_level_user_group_v8_36` STRING,
  `personalloan_fd_creditlevel_level_user_group_v8_1_36` STRING,
  `qyk_apl_amt_rte_100` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| order_number | ori_order_number | 复贷客群分组 | created_time | decision_time | ord_flg | fenzu_lb | b_order_number | tek_apl_amt_rte | vip_apl_amt_rte | fy_vip_apl_amt_rte | personalloan_fd_creditlevel_level_user_group_v8_36_tek | personalloan_fd_creditlevel_level_user_group_v8_1_36_tek | personalloan_fd_creditlevel_level_user_group_v8_36 | personalloan_fd_creditlevel_level_user_group_v8_1_36 | qyk_apl_amt_rte_100 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024042500001700000038582317 | 2024042500001700000038582317 | 提额卡 | 2024-04-25 22:49:15 |  | 额外放开 | V2.1 | 2024042500001700000038582317 | 0.06846153846153846 |  |  |  |  |  |  |  |
| 2024042600001700000040448146 | 2024042600001700000040448146 | 提额卡 | 2024-04-26 04:00:29 |  | 额外放开 | V4 | 2024042600001700000040448146 | 0.16125 |  |  |  |  |  |  |  |
| 2024042600001700000041293121 | 2024042600001700000041293121 | 提额卡 | 2024-04-26 06:54:47 |  | 额外放开 | V4 | 2024042600001700000041293121 | 0.14363636363636365 |  |  |  |  |  |  |  |
| 2024042600001700000042006574 | 2024042600001700000042006574 | 提额卡 | 2024-04-26 07:59:53 |  | 额外放开 | V4 | 2024042600001700000042006574 | 0.129375 |  |  |  |  |  |  |  |
| 2024042600001700000043485312 | 2024042600001700000043485312 | 提额卡 | 2024-04-26 09:16:16 |  | 额外放开 | V2.1 | 2024042600001700000043485312 | 0.051304347826086956 |  |  |  |  |  |  |  |

### 同步来源
- `odps`
