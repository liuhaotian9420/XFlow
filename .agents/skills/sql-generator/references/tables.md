# tables

## SQL代码索引（表 -> 文件）

### xyf_ads.ads_fin_onloan_fee_df
- ads_inloan_loan_balance_mthly_df.sql

### xyf_ads.ads_inloan_loan_balance_mthly_df_01
- ads_inloan_loan_balance_mthly_df.sql

### xyf_ads.ads_inloan_loan_monitor_screen_df
- ads_inloan_loan_pass_monitor_df.sql

### xyf_ads.ads_user_market_portfolio_label_df
- 老客月会sql代码.ipynb

### xyf_bi_dev.amt_predict_oct24_v2
- ads_inloan_loan_monitor_screen_df.sql

### xyf_dim.dim_pub_date
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

### xyf_dwd.dwd_inloan_leap_vip_order_hf
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

### xyf_dwd.dwd_inloan_loan_apply_main_df
- xyf_jingying.weekly_analysis_report_df_lss.txt
- 老客月会sql代码.ipynb

### xyf_dwd.dwd_preloan_credit_apply_df
- ads_inloan_loan_pass_monitor_df.sql
- APP新客转化-授信口径.ipynb
- APP新客转化-注册口径.ipynb
- dws_inloan_loan_channel_stat_df.sql
- dws_inloan_loan_risk_stat_df.sql
- 授信口径转化率_虚假给额.ipynb

### xyf_dwd.dwd_repay_loan_repay_plan_df
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- 老客月会sql代码.ipynb

### xyf_dwd.dwd_risk_model_b_card_df
- 老客月会sql代码.ipynb

### xyf_dwd.dwd_user_tek_order_df
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 老客月会sql代码.ipynb

### xyf_dwd.dwd_user_vip_order_df
- APP新客转化-注册口径.ipynb
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

### xyf_dws.dws_inloan_loan_channel_stat_df
- ads_inloan_loan_monitor_screen_df.sql

### xyf_dws.dws_inloan_loan_channel_stat_df_04
- ads_inloan_loan_monitor_screen_df.sql

### xyf_dws.dws_inloan_loan_pass_stat_df
- ads_inloan_loan_pass_monitor_df.sql

### xyf_dws.dws_inloan_loan_risk_stat_df
- ads_inloan_loan_monitor_screen_df.sql

### xyf_dws.dws_inloan_user_order_df
- ads_inloan_loan_balance_mthly_df.sql
- ads_inloan_loan_monitor_screen_df.sql
- ads_inloan_loan_pass_monitor_df.sql
- APP新客转化-授信口径.ipynb
- APP新客转化-注册口径.ipynb
- dws_inloan_loan_channel_stat_df.sql
- dws_inloan_loan_pass_stat_df.sql
- dws_inloan_loan_risk_stat_df.sql
- xyf_jingying.weekly_analysis_report_df_lss.txt
- xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

### xyf_dws.dws_inloan_user_order_hf_v
- 老客月会sql代码.ipynb

### xyf_dws.dws_repay_risk_order_bill_mob_df
- APP新客转化-注册口径.ipynb
- 授信口径转化率_虚假给额.ipynb
- 老客月会sql代码.ipynb

### xyf_dws.dws_repay_user_order_df
- ads_inloan_loan_balance_mthly_df.sql
- 老客月会sql代码.ipynb

### xyf_fengkong_dev.hhn_fk_ord_flg_all
- 老客月会sql代码.ipynb

### xyf_fengkong_dev.scq_fy_history_risk_price_modify
- 老客月会sql代码.ipynb

### xyf_fengkong_dev.wzq_order_b5_b4_compare_base
- 老客月会sql代码.ipynb

### xyf_fengkong_dev.zsh_tek_fk_ord_flg
- 老客月会sql代码.ipynb

### xyf_fengkong_dev.zsh_vip_fk_ord_flg
- 老客月会sql代码.ipynb

## xyf_ads.ads_fin_onloan_fee_df

### 原始字段
- DAYS
- after_comp_amt
- asset_type
- comp_amt
- loan_type
- pay_amt
- pt
- repay_amt
- risk_price

### 字段加工
- `1 biz_type`
- `DAYS AS dayid`

## xyf_ads.ads_inloan_loan_balance_mthly_df_01

### 原始字段
- data_date
- flag
- loan_amt_180
- loan_amt_30
- loan_amt_90
- loan_type

### 字段加工
- 无

## xyf_ads.ads_inloan_loan_monitor_screen_df

### 原始字段
- day_loan_amt
- day_loan_cnt
- flag
- loan_date
- stat_type

### 字段加工
- `CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)' WHEN flag IN ('APP放款') THEN '老客_APP放款' ELSE flag END AS flag`
- `IF(SUM(day_loan_cnt) = 0,0,SUM(day_loan_amt) / SUM(day_loan_cnt) * 100000000) 放款件均`
- `loan_date AS pay_date`
- `stat_type AS date_type`

## xyf_ads.ads_user_market_portfolio_label_df

### 原始字段
- b_card_model
- customer_pool
- day_id
- day_month01
- day_monthend
- last_apply_time
- last_login_time
- pt
- regulation_reason
- user_no

### 字段加工
- `CASE WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) <= 30 THEN '高_day30' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) BETWEEN 30 AND 90 THEN '中_day30_90' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) BETWEEN 90 AND 360 THEN '低_day90_360' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_apply_time)) > 360 THEN '睡眠_day360+' END AS apply_active_last_apply`
- `CASE WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) <= 30 THEN '高_day30' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) BETWEEN 30 AND 90 THEN '中_day30_90' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) BETWEEN 90 AND 360 THEN '低_day90_360' WHEN DATEDIFF(DATE(CONCAT(SUBSTR(pt,1,4),'-',SUBSTR(pt,5,2),'-',SUBSTR(pt,7,2))),DATE(last_login_time)) > 360 THEN '睡眠_day360+' END AS login_active_last_login`
- `CASE WHEN b_card_model IS NULL OR b_card_model < 0 THEN '空' WHEN b_card_model < 3 THEN 'AB' WHEN b_card_model < 5 THEN 'CD' WHEN b_card_model < 7 THEN 'EF' WHEN b_card_model < 9 THEN 'GH' ELSE 'IJK' END AS b_card_category`
- `CASE WHEN customer_pool IN ('API首贷池','API复贷池') THEN 'API' WHEN customer_pool IN ('APP首贷池','APP复贷池') THEN 'APP' END AS api_app_pool`
- `CASE WHEN regulation_reason IN ('不管制' ) THEN '可发标' WHEN regulation_reason IN ('可用额度低于500','禁申') THEN '可经营不可发标' WHEN regulation_reason NOT IN ('不管制' ,'可用额度低于500','禁申','可用额度低于1k') THEN '不可经营' END AS regulation_type`
- `CASE WHEN regulation_reason IN ('不管制' ) THEN '可发标' WHEN regulation_reason IN ('可用额度低于500','禁申','可用额度低于1k') THEN '可经营不可发标' WHEN regulation_reason NOT IN ('不管制' ,'可用额度低于500','禁申') THEN '不可经营' END AS regulation_type`
- `substr(last_login_time,1,7) AS login_mth`

## xyf_bi_dev.amt_predict_oct24_v2

### 原始字段
- api新客
- app新客
- 日期

### 字段加工
- `SUM(`api新客`) OVER (PARTITION BY substr(`日期`,1,7) ORDER BY `日期`)AS first_api_tgt`
- `SUM(app新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS first_app_tgt`
- `SUM(app新客+api新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS total_first_tgt`
- `SUM(app新客+api新客+老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期) AS total_tgt`
- `SUM(老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY 日期)AS added_tgt`
- `substr(to_date(`日期`,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt`
- `substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt`

## xyf_dim.dim_pub_date

### 原始字段
- day_id
- day_id_iso
- is_lastday

### 字段加工
- `1 biz_type`
- `substr(a.day_id_iso,1,7) AS loan_month`

## xyf_dwd.dwd_inloan_leap_vip_order_hf

### 原始字段
- act_refund_time
- app_user_id
- cust_no
- order_time
- pay_time
- pt
- real_card_price
- refund_amount

### 字段加工
- `'leap' AS card_type`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `pay_time AS tran_time`
- `real_card_price AS pay_amt`
- `refund_amount AS refund_amt`

## xyf_dwd.dwd_inloan_loan_apply_main_df

### 原始字段
- ori_order_number
- ori_risk_price
- pt
- risk_price
- risk_price_type

### 字段加工
- 无

## xyf_dwd.dwd_preloan_credit_apply_df

### 原始字段
- STATUS
- app
- apply_source
- created_time
- cust_no
- inner_app
- pt

### 字段加工
- `CASE WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app" ELSE "api" END AS ap_flg`
- `DATE(created_time) AS row_crt_ts_date`
- `MAX(CASE WHEN STATUS = 2 THEN 1 ELSE 0 END) AS shouxin_cnt`
- `MAX(created_time) AS created_time`

## xyf_dwd.dwd_repay_loan_repay_plan_df

### 原始字段
- initial_after_loan_fee
- initial_interest
- initial_platform_fee
- initial_principal
- order_number
- pt

### 字段加工
- `SUM(initial_principal) AS initial_principal`
- `SUM(nvl(initial_interest,0)+nvl(initial_after_loan_fee,0)+nvl(initial_platform_fee,0)) AS initial_interest_fee`

## xyf_dwd.dwd_risk_model_b_card_df

### 原始字段
- cust_no
- decision_time
- model_value
- pt

### 字段加工
- `CASE WHEN b.model_value <= 1.2 THEN 'qualified' ELSE 'unqualified' END AS apply_24_risk_qualification`
- `CASE WHEN b.model_value IS NULL OR b.model_value < 0 THEN '空' WHEN b.model_value < 3 THEN 'AB' WHEN b.model_value < 5 THEN 'CD' WHEN b.model_value < 7 THEN 'EF' WHEN b.model_value < 9 THEN 'GH' ELSE 'IJK' END AS apply_model_score_category`
- `CASE WHEN b.model_value IS NULL OR b.model_value < 0 THEN '空' WHEN b.model_value < 3 THEN 'AB' WHEN b.model_value < 5 THEN 'CD' WHEN b.model_value < 7 THEN 'EF' WHEN b.model_value < 9 THEN 'GH' ELSE 'IJK' END AS loan_model_score_category`
- `DISTINCT a.*`

## xyf_dwd.dwd_user_tek_order_df

### 原始字段
- act_refund_time
- app_user_id
- cust_no
- order_time
- pt
- real_order_price
- refund_amount

### 字段加工
- `'tek' AS card_type`
- `'复贷' AS vip_classifier`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `order_time AS tran_time`
- `real_order_price AS pay_amt`
- `refund_amount AS refund_amt`

## xyf_dwd.dwd_user_vip_order_df

### 原始字段
- act_refund_time
- app_user_id
- cust_no
- if_validation
- order_time
- pay_time
- pt
- real_card_price
- refund_amount
- vip_card_type

### 字段加工
- `'vip' AS card_type`
- `0 AS pay_amt`
- `0 AS refund_amt`
- `act_refund_time AS tran_time`
- `pay_time AS tran_time`
- `real_card_price/100 AS pay_amt`
- `refund_amount/100 AS refund_amt`

## xyf_dws.dws_inloan_loan_channel_stat_df

### 原始字段
- act_a24_p
- act_a24_p_ord
- act_added_apitoapp_p
- act_added_apitoapp_p_ord
- act_added_p
- act_added_p_ord
- act_first_apitoapp_p
- act_first_apitoapp_p_ord
- cum_act_a24_p
- cum_act_a24_p_ord
- cum_act_added_api_p
- cum_act_added_api_p_ord
- cum_act_added_apitoapp_p
- cum_act_added_apitoapp_p_ord
- cum_act_added_c
- cum_act_added_c_ord
- cum_act_added_p
- cum_act_added_p_ord
- cum_act_first_api_p
- cum_act_first_api_p_ord
- cum_act_first_apitoapp_p
- cum_act_first_apitoapp_p_ord
- cum_act_first_app_p
- cum_act_first_app_p_ord
- cum_act_first_dx_p
- cum_act_first_dx_p_ord
- cum_act_first_other_p
- cum_act_first_other_p_ord
- cum_act_first_xxl_p
- cum_act_first_xxl_p_ord
- cum_day_target_a24
- cum_day_target_added_apitoapp
- cum_day_target_added_c
- cum_day_target_added_p
- cum_day_target_first_api_p
- cum_day_target_first_apitoapp
- cum_day_target_first_app_p
- loan_date
- pt

### 字段加工
- `'APP放款' AS flag`
- `'APP首贷（API授信）' AS flag`
- `'APP首贷（API首贷）' AS flag`
- `'APP首贷（APP授信）' AS flag`
- `'current_mth' AS stat_type`
- `'新客总体' AS flag`
- `'老客总体' AS flag`
- `0 AS month_loan_num`
- `0 AS target_point`
- `COALESCE(act_added_p,0) + COALESCE(act_a24_p,0) - act_added_apitoapp_p AS day_loan_amt`
- `COALESCE(act_added_p_ord,0) + COALESCE(act_a24_p_ord,0) - act_added_apitoapp_p_ord AS day_loan_cnt`
- `COALESCE(b.cum_act_a24_p,0) AS cum_act_a24_p`
- `COALESCE(b.cum_act_a24_p_ord,0) AS cum_act_a24_p_ord`
- `COALESCE(b.cum_act_added_api_p,0) AS cum_act_added_api_p`
- `COALESCE(b.cum_act_added_api_p_ord,0) AS cum_act_added_api_p_ord`
- `COALESCE(b.cum_act_added_apitoapp_p,0) AS cum_act_added_apitoapp_p`
- `COALESCE(b.cum_act_added_apitoapp_p_ord,0) AS cum_act_added_apitoapp_p_ord`
- `COALESCE(b.cum_act_added_c,0) AS cum_act_added_c`
- `COALESCE(b.cum_act_added_c_ord,0) AS cum_act_added_c_ord`
- `COALESCE(b.cum_act_added_p,0) AS cum_act_added_p`
- `COALESCE(b.cum_act_added_p_ord,0) AS cum_act_added_p_ord`
- `COALESCE(b.cum_act_first_api_p,0) AS cum_act_first_api_p`
- `COALESCE(b.cum_act_first_api_p_ord,0) AS cum_act_first_api_p_ord`
- `COALESCE(b.cum_act_first_apitoapp_p,0) AS cum_act_first_apitoapp_p`
- `COALESCE(b.cum_act_first_apitoapp_p_ord,0) AS cum_act_first_apitoapp_p_ord`
- `COALESCE(b.cum_act_first_dx_p,0) AS cum_act_first_dx_p`
- `COALESCE(b.cum_act_first_dx_p_ord,0) AS cum_act_first_dx_p_ord`
- `COALESCE(b.cum_act_first_other_p,0) AS cum_act_first_other_p`
- `COALESCE(b.cum_act_first_other_p_ord,0) AS cum_act_first_other_p_ord`
- `COALESCE(b.cum_act_first_xxl_p,0) AS cum_act_first_xxl_p`
- `COALESCE(b.cum_act_first_xxl_p_ord,0) AS cum_act_first_xxl_p_ord`
- `COALESCE(b.cum_day_target_a24,0) AS cum_day_target_a24`
- `COALESCE(b.cum_day_target_added_c,0) AS cum_day_target_added_c`
- `COALESCE(b.cum_day_target_added_p,0) AS cum_day_target_added_p`
- `COALESCE(b.cum_day_target_first_api_p,0) AS cum_day_target_first_api_p`
- `COALESCE(b.cum_day_target_first_apitoapp,0) AS cum_day_target_first_apitoapp`
- `COALESCE(b.cum_day_target_first_app_p,0) AS cum_day_target_first_app_p`
- `COALESCE(t1.act_added_p,0) + COALESCE(t1.act_a24_p,0) AS day_loan_amt`
- `COALESCE(t1.act_added_p_ord,0) + COALESCE(t1.act_a24_p_ord,0) AS day_loan_cnt`
- `COALESCE(t1.act_first_api_p,0) + COALESCE(t1.act_added_api_p,0) + COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0) + COALESCE(t1.act_first_apitoapp_p,0) AS day_loan_amt`
- `COALESCE(t1.act_first_api_p_ord,0) + COALESCE(t1.act_added_api_p_ord,0) + COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0) + COALESCE(t1.act_first_apitoapp_p_ord,0) AS day_loan_cnt`
- `COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0) AS day_loan_amt`
- `COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0) AS day_loan_cnt`
- `NULL AS day_asset_amt`
- `act_added_apitoapp_p AS day_loan_amt`
- `act_added_apitoapp_p_ord AS day_loan_cnt`
- `act_first_apitoapp_p AS day_loan_amt`
- `act_first_apitoapp_p_ord AS day_loan_cnt`
- `cum_act_added_apitoapp_p AS month_loan_amt`
- `cum_act_added_p + cum_act_a24_p - cum_act_added_apitoapp_p AS month_loan_amt`
- `cum_act_first_apitoapp_p AS month_loan_amt`
- `cum_day_target_added_apitoapp AS target_point`
- `cum_day_target_first_apitoapp AS target_point`
- `t1.cum_act_added_p + t1.cum_act_a24_p AS month_loan_amt`
- `t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p AS month_loan_amt`
- `t2.added_tgt AS target_point`
- `t2.first_app_tgt AS target_point`
- `t2.total_first_tgt AS target_point`

## xyf_dws.dws_inloan_loan_channel_stat_df_04

### 原始字段
- act_a24_p_mthly_id
- act_added_api_p_mthly_id
- act_added_apitoapp_p_mthly_id
- act_added_p_mthly_id
- act_first_api_p_mthly_id
- act_first_apitoapp_p_mthly_id
- act_first_app_p_mthly_id
- act_first_dx_p_mthly_id
- act_first_other_p_mthly_id
- act_first_xxl_p_mthly_id
- loan_month
- t1

### 字段加工
- `'APP放款' AS flag`
- `'APP首贷（API授信）' AS flag`
- `'APP首贷（API首贷）' AS flag`
- `'APP首贷（APP授信）' AS flag`
- `'mthly_summary' AS stat_type`
- `'个人API复贷' AS flag`
- `'个人API复贷备份' AS flag`
- `'个人API首贷' AS flag`
- `'个人APP复贷' AS flag`
- `'个人APP首贷（新）' AS flag`
- `'新客总体' AS flag`
- `'老客总体' AS flag`
- `'自营总计' AS flag`
- `'自营总计备份' AS flag`
- `(t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord - t1.cum_act_added_apitoapp_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord + t1.cum_act_first_apitoapp_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `(t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p) / DAY(t1.loan_date) AS day_loan_amt`
- `(t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord) / DAY(t1.loan_date) AS day_loan_cnt`
- `CASE WHEN t1.loan_date < '2024-01-01' THEN t1.cum_day_target_added_p + t1.cum_day_target_a24 - t1.cum_day_target_added_apitoapp ELSE 0 END AS target_point`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c) /DAY(t1.loan_date) ELSE (t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date) END AS day_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p) / DAY(t1.loan_date) END AS day_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date) ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN COALESCE(t3.act_added_c_mthly_id,0) + t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id ELSE t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id END AS month_loan_num`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c ELSE t1.cum_act_added_p + t1.cum_act_a24_p END AS month_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p ELSE t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p END AS month_loan_amt`
- `CASE WHEN t1.loan_date >= '2024-04-01' THEN t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + COALESCE(t3.act_added_c_mthly_id,0) ELSE (COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0)) END AS month_loan_num`
- `CAST(NULL AS DECIMAL(38,18)) AS target_point`
- `COALESCE(t2.act_added_apitoapp_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) - COALESCE(t2.act_added_apitoapp_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) AS month_loan_num`
- `COALESCE(t2.act_first_api_p_mthly_id,0) + COALESCE(t2.act_added_api_p_mthly_id,0) + COALESCE(t2.act_first_dx_p_mthly_id,0) + COALESCE(t2.act_first_xxl_p_mthly_id,0) + COALESCE(t2.act_first_other_p_mthly_id,0) + COALESCE(t2.act_first_apitoapp_p_mthly_id,0) AS month_loan_num`
- `NULL AS day_asset_amt`
- `t1.cum_act_added_api_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_added_api_p AS month_loan_amt`
- `t1.cum_act_added_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_added_apitoapp_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_added_apitoapp_p AS month_loan_amt`
- `t1.cum_act_added_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p AS month_loan_amt`
- `t1.cum_act_added_p + t1.cum_act_a24_p AS month_loan_amt`
- `t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_api_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_api_p AS month_loan_amt`
- `t1.cum_act_first_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_apitoapp_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_apitoapp_p AS month_loan_amt`
- `t1.cum_act_first_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_app_p / DAY(t1.loan_date) AS day_loan_amt`
- `t1.cum_act_first_app_p AS month_loan_amt`
- `t1.cum_act_first_app_p_ord / DAY(t1.loan_date) AS day_loan_cnt`
- `t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p AS month_loan_amt`
- `t1.cum_day_target_added_apitoapp AS target_point`
- `t1.cum_day_target_added_c + t1.cum_day_target_added_p + t1.cum_day_target_a24 + t1.cum_day_target_first_app_p + t1.cum_day_target_first_api_p AS target_point`
- `t1.cum_day_target_added_p + t1.cum_day_target_a24 AS target_point`
- `t1.cum_day_target_first_api_p + t1.cum_day_target_first_app_p + t1.cum_day_target_first_apitoapp AS target_point`
- `t1.cum_day_target_first_api_p AS target_point`
- `t1.cum_day_target_first_apitoapp AS target_point`
- `t1.cum_day_target_first_app_p AS target_point`
- `t2.act_added_api_p_mthly_id AS month_loan_num`
- `t2.act_first_api_p_mthly_id AS month_loan_num`
- `t2.act_first_apitoapp_p_mthly_id AS month_loan_num`
- `t2.act_first_app_p_mthly_id AS month_loan_num`
- `t2.act_first_dx_p_mthly_id + t2.act_first_xxl_p_mthly_id + t2.act_first_other_p_mthly_id AS month_loan_num`

## xyf_dws.dws_inloan_loan_pass_stat_df

### 原始字段
- b_pay_time
- c_created_time
- created_time
- cust_no
- risk_status

### 字段加工
- `DATE(created_time) AS created_date`
- `DATE_ADD(created_time,-30) AS sub30_created_date`

## xyf_dws.dws_inloan_loan_risk_stat_df

### 原始字段
- act_added_api_p_asset
- act_added_p_asset
- act_first_api_p_asset
- act_first_app_p_asset
- order_date
- pt

### 字段加工
- `nvl(t3.act_first_api_p_asset,0) + nvl(t3.act_added_api_p_asset,0) + nvl(t3.act_first_app_p_asset,0) + nvl(t3.act_added_p_asset,0) AS day_asset_amt`
- `t3.act_added_api_p_asset AS day_asset_amt`
- `t3.act_added_p_asset AS day_asset_amt`
- `t3.act_first_api_p_asset AS day_asset_amt`
- `t3.act_first_app_p_asset AS day_asset_amt`

## xyf_dws.dws_inloan_user_order_df

### 原始字段
- app
- asset_type_flag
- business_line
- cust_no
- first_order_number
- first_order_time
- inner_app
- loan_amt
- loan_flag
- loan_status
- loan_time
- pt
- risk_status

### 字段加工
- `COUNT(DISTINCT cust_no) act_added_c_mthly_id`
- `a.user_no AS app_user_id`
- `substr(loan_time,1,7) AS loan_month`

## xyf_dws.dws_inloan_user_order_hf_v

### 原始字段
- amount
- app
- app_user_id
- first_order_time
- inner_app
- loan_status
- loan_type_flag
- risk_status
- user_no

### 字段加工
- `COUNT(DISTINCT CASE WHEN b.loan_status = 'success' THEN b.app_user_id END) loan_succeed_user_cnt`
- `COUNT(DISTINCT CASE WHEN b.risk_status = 'pass' THEN b.app_user_id END) risk_passed_user_cnt`
- `COUNT(DISTINCT b.app_user_id) applied_user_cnt`
- `COUNT(DISTINCT user_no) user_cnt`
- `SUM(CASE WHEN b.loan_status = 'success' THEN b.amount END) loan_succeed_amount`

## xyf_dws.dws_repay_risk_order_bill_mob_df

### 原始字段
- order_number
- pt

### 字段加工
- 无

## xyf_dws.dws_repay_user_order_df

### 原始字段
- app
- business_line
- day_id
- day_monthend
- inner_app
- loan_balance
- loan_cnt_30_minus
- loan_flag
- order_number
- overdue_days
- pt
- user_no

### 字段加工
- `'daily' AS flag`
- `CASE WHEN pt < '20250623' THEN (CASE WHEN app <> inner_app THEN 'API' WHEN loan_flag = '首贷' THEN 'APP首贷' ELSE 'APP复贷' END ) WHEN pt >= '20250623' THEN (CASE WHEN business_line = 'API' THEN 'API' WHEN loan_flag = '首贷' THEN 'APP首贷' ELSE 'APP复贷' END ) END AS loan_type`
- `COUNT(DISTINCT CASE WHEN overdue_days <= 30 AND loan_balance > 0 THEN order_number END) AS loan_cnt_30_minus`
- `SUM(CASE WHEN overdue_days <= 30 THEN loan_balance END) AS loan_balance_30_minus`
- `SUM(CASE WHEN overdue_days <=180 THEN loan_balance END)/100000000 AS `余额_180``
- `SUM(CASE WHEN overdue_days <=30 THEN loan_balance END)/100000000 AS `余额_30``
- `SUM(CASE WHEN overdue_days <=90 THEN loan_balance END)/100000000 AS `余额_90``
- `substr(TO_DATE(pt,'yyyyMMdd'),1,10) AS data_date`

## xyf_fengkong_dev.hhn_fk_ord_flg_all

### 原始字段
- 复贷客群分组

### 字段加工
- `DISTINCT order_number`

## xyf_fengkong_dev.scq_fy_history_risk_price_modify

### 原始字段
- ori_order_number

### 字段加工
- `CASE WHEN ori_price_overwritten.ori_order_number IS NOT NULL THEN 'I36' WHEN application.ori_order_number IS NOT NULL THEN 'I36' WHEN orders.asset_type_flag = 'I36' THEN 'I36' ELSE 'I24' END AS ori_risk_price`

## xyf_fengkong_dev.wzq_order_b5_b4_compare_base

### 原始字段
- RLIKE

### 字段加工
- `DISTINCT order_number`

## xyf_fengkong_dev.zsh_tek_fk_ord_flg

### 原始字段
- order_number
- tek_fk_ord_flg

### 字段加工
- 无

## xyf_fengkong_dev.zsh_vip_fk_ord_flg

### 原始字段
- order_number
- vip_fk_ord_flg

### 字段加工
- 无
