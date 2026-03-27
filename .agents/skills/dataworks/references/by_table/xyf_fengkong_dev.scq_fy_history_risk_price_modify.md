# xyf_fengkong_dev.scq_fy_history_risk_price_modify

## 来源文件
- 老客月会sql代码.ipynb

- `CASE WHEN ori_price_overwritten.ori_order_number IS NOT NULL THEN 'I36' WHEN application.ori_order_number IS NOT NULL THEN 'I36' WHEN orders.asset_type_flag = 'I36' THEN 'I36' ELSE 'I24' END AS ori_risk_price`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column |  |  |
| ori_order_number | STRING | column |  | Y |
| 输出风险定价 | STRING | column |  |  |
| 是否结清 | STRING | column |  |  |

#### DDL
```sql
CREATE TABLE xyf_fengkong_dev.`scq_fy_history_risk_price_modify` (
  `order_number` STRING,
  `ori_order_number` STRING,
  `输出风险定价` STRING,
  `是否结清` STRING
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| order_number | ori_order_number | 输出风险定价 | 是否结清 |
| --- | --- | --- | --- |
| 2025052500123700000093477879 | 2025052500123600000035574124 | I24 | 在贷 |
| 2025052500123700000093560346 | 2025052500123600000035582654 | I24 | 在贷 |
| 2025052500123700000094037706 | 2025052500123600000035619795 | I24 | 在贷 |
| 2025052600123700000094135281 | 2025052600123600000035625243 | I24 | 在贷 |
| 2025052600123700000094500399 | 2025052600123600000035664122 | I24 | 结清 |

### 同步来源
- `odps`
