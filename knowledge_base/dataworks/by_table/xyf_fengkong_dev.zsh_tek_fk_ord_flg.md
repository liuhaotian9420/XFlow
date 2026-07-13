# xyf_fengkong_dev.zsh_tek_fk_ord_flg

## 来源文件
- 老客月会sql代码.ipynb

- 无

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | [AI推测] 订单号 | Y |
| id_card_number | STRING | column | [AI推测] 身份证号（加密） |  |
| created_time | DATETIME | column | [AI推测] 订单创建时间 |  |
| decision_time | DATETIME | column | [AI推测] 风控决策时间 |  |
| cashloan_order_periods | DOUBLE | column | [AI推测] 现金贷订单期数 |  |
| tek_apl_amt_rte_b | DOUBLE | column | [AI推测] 提额卡申请金额费率（基准） |  |
| fd_multiple_draw_creditlevel_stock_creditlevel_cross_3_hz | STRING | column | [AI推测] 多次支用信用等级_存量交叉_3期_汇总评级 |  |
| fd_multiple_draw_creditlevel_stock_creditlevel_cross_6_hz | STRING | column | [AI推测] 多次支用信用等级_存量交叉_6期_汇总评级 |  |
| fd_multiple_draw_creditlevel_stock_creditlevel_cross_12_hz | STRING | column | [AI推测] 多次支用信用等级_存量交叉_12期_汇总评级 |  |
| 综合评级 | STRING | column | [AI推测] 风控综合评级（如A-F） |  |
| str_ver | STRING | column | [AI推测] 策略版本号（如V4/V6/24+权益） |  |
| tek_fk_ord_flg | STRING | column | [AI推测] 提额卡风控订单标记（额外放开/非额外放开） | Y |
| tek_fk_ord_flg_new | STRING | column | [AI推测] 提额卡风控订单标记_新规则 |  |
| old_str_ver_add_fy | STRING | column | [AI推测] 旧策略版本_附加飞跃权益标识 |  |

#### DDL
```sql
CREATE TABLE xyf_fengkong_dev.`zsh_tek_fk_ord_flg` (
  `order_number` STRING,
  `id_card_number` STRING,
  `created_time` DATETIME,
  `decision_time` DATETIME,
  `cashloan_order_periods` DOUBLE,
  `tek_apl_amt_rte_b` DOUBLE,
  `fd_multiple_draw_creditlevel_stock_creditlevel_cross_3_hz` STRING,
  `fd_multiple_draw_creditlevel_stock_creditlevel_cross_6_hz` STRING,
  `fd_multiple_draw_creditlevel_stock_creditlevel_cross_12_hz` STRING,
  `综合评级` STRING,
  `str_ver` STRING,
  `tek_fk_ord_flg` STRING,
  `tek_fk_ord_flg_new` STRING,
  `old_str_ver_add_fy` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| order_number | id_card_number | created_time | decision_time | cashloan_order_periods | tek_apl_amt_rte_b | fd_multiple_draw_creditlevel_stock_creditlevel_cross_3_hz | fd_multiple_draw_creditlevel_stock_creditlevel_cross_6_hz | fd_multiple_draw_creditlevel_stock_creditlevel_cross_12_hz | 综合评级 | str_ver | tek_fk_ord_flg | tek_fk_ord_flg_new | old_str_ver_add_fy |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2026031200123600000074394997 | YXDjulk0OlHPyu7Y7bb7N1/SlwTufvadDxoG1Zh0kec= | 2026-03-12 23:34:34 | 2026-03-13 00:05:20 | 12.0 | 0.0 |  |  |  |  | V4 | 非额外放开 | 非额外放开 |  |
| 2026031600123600000075002846 | Lpg8ut9egL1B/uQSs+b/KDSp1fGzgxlXA4JfpqNkQTo= | 2026-03-16 23:18:19 | 2026-03-16 23:20:30 | 12.0 | 0.0 |  |  |  |  | V4 | 非额外放开 | 非额外放开 |  |
| 2025050900123600000033635182 | wOhSkkcsxK+Wvd1dlg+XYzF0jz7Ep2o81tpmZnP/I7s= | 2025-05-09 21:29:14 | 2025-05-09 21:29:14 | 12.0 | 0.0 |  |  |  |  | V6 | 非额外放开 | 非额外放开 |  |
| 2025080500123600000044477664 | IqYvJ8ZuMDWUz6nJIl0/81/SlwTufvadDxoG1Zh0kec= | 2025-08-05 11:48:32 | 2025-08-05 11:48:33 | 12.0 | 0.0 | F | F | F | F | 24+权益 | 非额外放开 | 非额外放开 | 24+权益 |
| 2025092000123600000050124657 | dudUd/3dcSZUOU4UPuadNPtpOL3zZcYk8ZTatJOzibo= | 2025-09-20 13:43:04 | 2025-09-20 14:14:27 | 12.0 | 0.0 |  |  |  |  | V4 | 非额外放开 | 额外放开 |  |

### 同步来源
- `odps`
