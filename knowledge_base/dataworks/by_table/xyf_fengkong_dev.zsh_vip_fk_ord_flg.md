# xyf_fengkong_dev.zsh_vip_fk_ord_flg

## 来源文件
- 老客月会sql代码.ipynb

- 无

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | [AI推测] 订单号 | Y |
| id_card_number | STRING | column | [AI推测] 身份证号（加密） |  |
| created_time | DATETIME | column | [AI推测] 订单创建时间 |  |
| decision_time_vip | DATETIME | column | [AI推测] VIP风控决策时间 |  |
| vip_apl_amt_rte_b | DOUBLE | column | [AI推测] VIP申请金额费率（基准） |  |
| vip_fk_ord_flg | STRING | column | [AI推测] VIP风控订单标记（额外放开/非额外放开） | Y |
| vip_fk_ord_flg_new | STRING | column | [AI推测] VIP风控订单标记_新规则 |  |

#### DDL
```sql
CREATE TABLE xyf_fengkong_dev.`zsh_vip_fk_ord_flg` (
  `order_number` STRING,
  `id_card_number` STRING,
  `created_time` DATETIME,
  `decision_time_vip` DATETIME,
  `vip_apl_amt_rte_b` DOUBLE,
  `vip_fk_ord_flg` STRING,
  `vip_fk_ord_flg_new` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| order_number | id_card_number | created_time | decision_time_vip | vip_apl_amt_rte_b | vip_fk_ord_flg | vip_fk_ord_flg_new |
| --- | --- | --- | --- | --- | --- | --- |
| 2025081100123600000045347007 | SvOt/tUb8M9jhfAayC+0XhzVwBDhsOijwBW7FXWQk2U= | 2025-08-11 21:46:47 | 2025-08-11 21:46:48 | 0.0 | 非额外放开 | 额外放开 |
| 2025051900123600000034885445 | yGP3f+uy2TEheBGctkhEUSb8BMQ0fckV5FavettW74k= | 2025-05-19 20:16:12 | 2025-05-19 20:48:39 | 0.0 | 非额外放开 | 额外放开 |
| 2025052900123600000036036966 | s7v+gpp0/m7GzKhJknsOQ7ThfgtbeR6KsdGm243NmBI= | 2025-05-29 15:05:29 |  |  | 非额外放开 | 非额外放开 |
| 2025062300123600000039073778 | T2fXtKmwj2dhyA+RH0eAsF0aJJSERV/wx/62mjxtPcg= | 2025-06-23 11:24:47 | 2025-06-23 11:56:03 | 0.0 | 非额外放开 | 额外放开 |
| 2025101200123600000052942591 | cOB39NKUooLHVakdTudthNBpWbKHvuIuDbbXXBCg++Q= | 2025-10-12 10:13:02 | 2025-10-12 10:13:03 | 0.15893333333333337 | 非额外放开 | 额外放开 |

### 同步来源
- `odps`
