# xyf_bi_dev.amt_predict_oct24_v2

## 来源文件
- ads_inloan_loan_monitor_screen_df.sql

- `SUM(`api新客`) OVER (PARTITION BY substr(`日期`,1,7) ORDER BY `日期`)AS first_api_tgt`
- `SUM(app新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS first_app_tgt`
- `SUM(app新客+api新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS total_first_tgt`
- `SUM(app新客+api新客+老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS total_tgt`
- `SUM(老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期)AS added_tgt`
- `substr(to_date(`日期`,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt`
- `substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| 日期 | STRING | column | 日期 | Y |
| api新客 | DOUBLE | column | API新客 | Y |
| app新客 | DOUBLE | column | APP新客 | Y |
| 老客预估 | STRING | column | 老客预估 |  |

#### DDL
```sql
CREATE TABLE xyf_bi_dev.`amt_predict_oct24_v2` (
  `日期` STRING COMMENT '日期',
  `api新客` DOUBLE COMMENT 'API新客',
  `app新客` DOUBLE COMMENT 'APP新客',
  `老客预估` STRING COMMENT '老客预估'
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
LIFECYCLE 365
```

### 抽样数据
| 日期 | api新客 | app新客 | 老客预估 |
| --- | --- | --- | --- |
| 2024-10-01 00:00:00 | 0.7149671052631579 | 0.2991524015290012 | 1.0730847405474402 |
| 2024-10-02 00:00:00 | 0.7149671052631579 | 0.2991524015290012 | 1.0605073357424477 |
| 2024-10-03 00:00:00 | 0.7149671052631579 | 0.2991524015290012 | 1.067768599018579 |
| 2024-10-04 00:00:00 | 0.7149671052631579 | 0.2991524015290012 | 1.0615271944858886 |
| 2024-10-05 00:00:00 | 0.7149671052631579 | 0.2991524015290012 | 1.03430263331726 |

### 同步来源
- `odps`
