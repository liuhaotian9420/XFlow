# xyf_dim.dim_pub_date

## 来源文件
- ads_inloan_loan_balance_mthly_df.sql
- ads_inloan_loan_monitor_screen_df.sql
- ads_inloan_loan_pass_monitor_df.sql
- APP新客转化-授信口径.ipynb
- APP新客转化-注册口径.ipynb
- dws_inloan_loan_channel_stat_df.sql
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| day_id | STRING | column | 日期id格式yyyymmdd |  |
| day_id_iso | STRING | column | 日期长格式yyyy-mm-dd |  |
| day_id_desc | STRING | column | 日期中文格式 |  |
| month_id | STRING | column | 日期月id |  |
| month_id_iso | STRING | column | 日期长格式月id |  |
| month_id_desc | STRING | column | 日期月中文格式 |  |
| year_desc | STRING | column | 年id |  |
| week_id | INT | column | 周id |  |
| week_desc | STRING | column | 周中文格式 |  |
| ten_days | INT | column | 旬 |  |
| dt_week | BIGINT | column | 一周第几天 |  |
| dt_month | INT | column | 一个月第几天 |  |
| dt_year | INT | column | 一年第几天 |  |
| is_lastday | INT | column | 是否月末最后一天 |  |
| is_weekend | INT | column | 是否周六日 |  |
| is_holiday | INT | column | 是否节假日 |  |
| quarter_id | INT | column | 季度id |  |
| quarter_desc | STRING | column | 季度中文描述 |  |
| day_month01 | STRING | column | 当月第一天 |  |
| day_month01_iso | STRING | column | 当月第一天长格式 |  |
| day_monthend | STRING | column | 当月最后一天 |  |
| day_monthend_iso | STRING | column | 当月最后一天长格式 |  |
| day_last01 | STRING | column | 日期前一天 |  |
| day_last01_iso | STRING | column | 日期前一天长格式 |  |
| day_last03 | STRING | column | 日期前三天 |  |
| day_last03_iso | STRING | column | 日期前三天长格式 |  |
| day_last07 | STRING | column | 日期前七天 |  |
| day_last07_iso | STRING | column | 日期前七天长格式 |  |
| day_last30 | STRING | column | 日期前三十天 |  |
| day_last30_iso | STRING | column | 日期前三十天长格式 |  |
| day_lastmonth | STRING | column | 上月同期 |  |
| day_lastmonth_iso | STRING | column | 上月同期长格式 |  |
| day_last2month | STRING | column | 上2月同期 |  |
| day_last2month_iso | STRING | column | 上2月同期长格式 |  |
| day_last3month | STRING | column | 上3月同期 |  |
| day_last3month_iso | STRING | column | 上3月同期长格式 |  |
| day_lastyear | STRING | column | 去年同期 |  |
| day_lastyear_iso | STRING | column | 去年同期长格式 |  |
| day_year01 | STRING | column | 当年第1天 |  |
| day_year01_iso | STRING | column | 当年第1天长格式 |  |
| day_yearend | STRING | column | 当年最后1天 |  |
| day_yearend_iso | STRING | column | 当年最后1天长格式 |  |
| month_weeks | INT | column | 本周第几周 |  |
| holiday_type | INT | column | 节假日分类,1元旦,2春节,3清明,4五一,5端午,6国庆,7中秋 |  |
| holiday_desc | STRING | column | 节假日分类描述 |  |
| day_quarter01 | STRING | column | 季度开始日期 |  |
| day_quarterend | STRING | column | 季度结束日期 |  |
| day_week01 | STRING | column | 周开始日期 |  |
| day_weekend | STRING | column | 周结束日期 |  |
| week_id_xf | STRING | column | 当年第几周 |  |
| week_desc_xf | STRING | column | 年周 |  |
| day_week01_xf | STRING | column | 周开始日期 |  |
| day_weekend_xf | STRING | column | 周结束日期 |  |
| dt_week_xf | INT | column | 一周第几天（周报周：周四~周三） |  |
| week_id_xf_new | STRING | column | 周报周new，（周报周：周五~周四） |  |
| week_desc_xf_new | STRING | column | 年周 |  |
| day_week01_xf_new | STRING | column | 周开始日期 |  |
| day_weekend_xf_new | STRING | column | 周结束日期 |  |
| dt_week_xf_new | INT | column | 一周第几天 |  |
| reperforating | STRING | column | 补班类型 |  |
| is_weekday | STRING | column | 是否工作日，1是工作日，0否(已经对补班进行了逻辑处理) |  |

### DDL
```sql
CREATE TABLE xyf_dim.`dim_pub_date` (
  `day_id` STRING COMMENT '日期id格式yyyymmdd',
  `day_id_iso` STRING COMMENT '日期长格式yyyy-mm-dd',
  `day_id_desc` STRING COMMENT '日期中文格式',
  `month_id` STRING COMMENT '日期月id',
  `month_id_iso` STRING COMMENT '日期长格式月id',
  `month_id_desc` STRING COMMENT '日期月中文格式',
  `year_desc` STRING COMMENT '年id',
  `week_id` INT COMMENT '周id',
  `week_desc` STRING COMMENT '周中文格式',
  `ten_days` INT COMMENT '旬',
  `dt_week` BIGINT COMMENT '一周第几天',
  `dt_month` INT COMMENT '一个月第几天',
  `dt_year` INT COMMENT '一年第几天',
  `is_lastday` INT COMMENT '是否月末最后一天',
  `is_weekend` INT COMMENT '是否周六日',
  `is_holiday` INT COMMENT '是否节假日',
  `quarter_id` INT COMMENT '季度id',
  `quarter_desc` STRING COMMENT '季度中文描述',
  `day_month01` STRING COMMENT '当月第一天',
  `day_month01_iso` STRING COMMENT '当月第一天长格式',
  `day_monthend` STRING COMMENT '当月最后一天',
  `day_monthend_iso` STRING COMMENT '当月最后一天长格式',
  `day_last01` STRING COMMENT '日期前一天',
  `day_last01_iso` STRING COMMENT '日期前一天长格式',
  `day_last03` STRING COMMENT '日期前三天',
  `day_last03_iso` STRING COMMENT '日期前三天长格式',
  `day_last07` STRING COMMENT '日期前七天',
  `day_last07_iso` STRING COMMENT '日期前七天长格式',
  `day_last30` STRING COMMENT '日期前三十天',
  `day_last30_iso` STRING COMMENT '日期前三十天长格式',
  `day_lastmonth` STRING COMMENT '上月同期',
  `day_lastmonth_iso` STRING COMMENT '上月同期长格式',
  `day_last2month` STRING COMMENT '上2月同期',
  `day_last2month_iso` STRING COMMENT '上2月同期长格式',
  `day_last3month` STRING COMMENT '上3月同期',
  `day_last3month_iso` STRING COMMENT '上3月同期长格式',
  `day_lastyear` STRING COMMENT '去年同期',
  `day_lastyear_iso` STRING COMMENT '去年同期长格式',
  `day_year01` STRING COMMENT '当年第1天',
  `day_year01_iso` STRING COMMENT '当年第1天长格式',
  `day_yearend` STRING COMMENT '当年最后1天',
  `day_yearend_iso` STRING COMMENT '当年最后1天长格式',
  `month_weeks` INT COMMENT '本周第几周',
  `holiday_type` INT COMMENT '节假日分类,1元旦,2春节,3清明,4五一,5端午,6国庆,7中秋',
  `holiday_desc` STRING COMMENT '节假日分类描述',
  `day_quarter01` STRING COMMENT '季度开始日期',
  `day_quarterend` STRING COMMENT '季度结束日期',
  `day_week01` STRING COMMENT '周开始日期',
  `day_weekend` STRING COMMENT '周结束日期',
  `week_id_xf` STRING COMMENT '当年第几周',
  `week_desc_xf` STRING COMMENT '年周',
  `day_week01_xf` STRING COMMENT '周开始日期',
  `day_weekend_xf` STRING COMMENT '周结束日期',
  `dt_week_xf` INT COMMENT '一周第几天（周报周：周四~周三）',
  `week_id_xf_new` STRING COMMENT '周报周new，（周报周：周五~周四）',
  `week_desc_xf_new` STRING COMMENT '年周',
  `day_week01_xf_new` STRING COMMENT '周开始日期',
  `day_weekend_xf_new` STRING COMMENT '周结束日期',
  `dt_week_xf_new` INT COMMENT '一周第几天',
  `reperforating` STRING COMMENT '补班类型',
  `is_weekday` STRING COMMENT '是否工作日，1是工作日，0否(已经对补班进行了逻辑处理)'
)
COMMENT '日期维表'
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| day_id | day_id_iso | day_id_desc | month_id | month_id_iso | month_id_desc | year_desc | week_id | week_desc | ten_days | dt_week | dt_month | dt_year | is_lastday | is_weekend | is_holiday | quarter_id | quarter_desc | day_month01 | day_month01_iso | day_monthend | day_monthend_iso | day_last01 | day_last01_iso | day_last03 | day_last03_iso | day_last07 | day_last07_iso | day_last30 | day_last30_iso | day_lastmonth | day_lastmonth_iso | day_last2month | day_last2month_iso | day_last3month | day_last3month_iso | day_lastyear | day_lastyear_iso | day_year01 | day_year01_iso | day_yearend | day_yearend_iso | month_weeks | holiday_type | holiday_desc | day_quarter01 | day_quarterend | day_week01 | day_weekend | week_id_xf | week_desc_xf | day_week01_xf | day_weekend_xf | dt_week_xf | week_id_xf_new | week_desc_xf_new | day_week01_xf_new | day_weekend_xf_new | dt_week_xf_new | reperforating | is_weekday |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20300101 | 2030-01-01 | 2030年01月01日 | 203001 | 2030-01 | 2030年01月 | 2030年 | 1 | 2030年第1周 | 1 | 2 | 1 | 1 | 0 | 0 | 0 | 1 | 2030年第1季度 | 20300101 | 2030-01-01 | 20300131 | 2030-01-31 | 20291231 | 2029-12-31 | 20291229 | 2029-12-29 | 20291225 | 2029-12-25 | 20291202 | 2029-12-02 | 20291201 | 2029-12-01 | 20291101 | 2029-11-01 | 20291001 | 2029-10-01 | 20290101 | 2029-01-01 | 20300101 | 2030-01-01 | 20301231 | 2030-12-31 | 1 |  |  | 2030-01-01 | 2030-03-31 | 20291231 | 20300106 | 1 | 2030年第1周 | 2029-12-27 | 2030-01-02 | 6 | 1 | 2030年第1周 | 2029-12-28 | 2030-01-03 | 5 |  |  |
| 20300102 | 2030-01-02 | 2030年01月02日 | 203001 | 2030-01 | 2030年01月 | 2030年 | 1 | 2030年第1周 | 1 | 3 | 2 | 2 | 0 | 0 | 0 | 1 | 2030年第1季度 | 20300101 | 2030-01-01 | 20300131 | 2030-01-31 | 20300101 | 2030-01-01 | 20291230 | 2029-12-30 | 20291226 | 2029-12-26 | 20291203 | 2029-12-03 | 20291202 | 2029-12-02 | 20291102 | 2029-11-02 | 20291002 | 2029-10-02 | 20290102 | 2029-01-02 | 20300101 | 2030-01-01 | 20301231 | 2030-12-31 | 1 |  |  | 2030-01-01 | 2030-03-31 | 20291231 | 20300106 | 1 | 2030年第1周 | 2029-12-27 | 2030-01-02 | 7 | 1 | 2030年第1周 | 2029-12-28 | 2030-01-03 | 6 |  |  |
| 20300103 | 2030-01-03 | 2030年01月03日 | 203001 | 2030-01 | 2030年01月 | 2030年 | 1 | 2030年第1周 | 1 | 4 | 3 | 3 | 0 | 0 | 0 | 1 | 2030年第1季度 | 20300101 | 2030-01-01 | 20300131 | 2030-01-31 | 20300102 | 2030-01-02 | 20291231 | 2029-12-31 | 20291227 | 2029-12-27 | 20291204 | 2029-12-04 | 20291203 | 2029-12-03 | 20291103 | 2029-11-03 | 20291003 | 2029-10-03 | 20290103 | 2029-01-03 | 20300101 | 2030-01-01 | 20301231 | 2030-12-31 | 1 |  |  | 2030-01-01 | 2030-03-31 | 20291231 | 20300106 | 2 | 2030年第2周 | 2030-01-03 | 2030-01-09 | 1 | 1 | 2030年第1周 | 2029-12-28 | 2030-01-03 | 7 |  |  |

## 同步来源
- `odps`
