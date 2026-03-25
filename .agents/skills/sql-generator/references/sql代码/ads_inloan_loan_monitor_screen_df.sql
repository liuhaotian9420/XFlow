CREATE TABLE IF NOT EXISTS ads_inloan_loan_monitor_screen_df 
(
     stat_type      STRING         COMMENT  '统计口径' 
    ,loan_date      STRING         COMMENT  '放款日期'
    ,flag           STRING         COMMENT  '放款渠道' 
    ,day_loan_amt   DECIMAL(38,18) COMMENT  '日放款金额' 
    ,day_loan_cnt   DOUBLE         COMMENT  '日订单数' 
    ,month_loan_amt DECIMAL(38,18) COMMENT  '月累计放款' 
    ,target_point   DECIMAL(38,18) COMMENT  '目标' 
    ,month_loan_num BIGINT         COMMENT  '月放款人数' 
    ,day_asset_amt  DECIMAL(38,18) COMMENT  '每日资产金额' ) 
COMMENT '大盘放款量级监控日报-邮件任务';


DROP TABLE IF EXISTS ads_inloan_loan_monitor_screen_df_01;
CREATE TABLE ads_inloan_loan_monitor_screen_df_01 AS
SELECT  DATE(COALESCE(loan_remit_time,loan_audit_time))           AS loan_date
       ,od.loan_remit_time
       ,od.loan_audit_time
       ,od.STATUS
       ,od.order_no
       ,od.user_id
       ,od.amount
       ,CASE WHEN pp.name LIKE '%你我贷%' THEN '你我贷'
             WHEN pp.name LIKE '%哈啰%' THEN '哈啰'  ELSE pp.name END AS name
       ,pp.match_type
FROM xyf_dwd.dwd_xyf_op_user_order_df od
INNER JOIN xyf_dwd.dwd_open_platform_product_df pp
ON od.product_no = pp.product_no AND pp.pt = '${bizdate}' AND pp.match_type = 1 -- 分发全流程产品 
WHERE od.pt = '${bizdate}'
;


INSERT OVERWRITE TABLE ads_inloan_loan_monitor_screen_df

SELECT  'current_mth'            AS stat_type --统计口径 
       ,t1.loan_date 				--放款日期（pay_date） 
       ,'个人API首贷'                AS flag
       ,t1.act_first_api_p       AS day_loan_amt --`日放款` 
       ,t1.act_first_api_p_ord   AS day_loan_cnt --`日订单数` 
       ,t1.cum_act_first_api_p   AS month_loan_amt --`月累计放款` 
       ,t2.first_api_tgt         AS target_point --`目标` 
       ,0                        AS month_loan_num --月放款人数 
       ,t3.act_first_api_p_asset AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(`日期`,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt
	       ,SUM(`api新客`) OVER (PARTITION BY substr(`日期`,1,7) ORDER BY  `日期`)AS first_api_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                AS stat_type --统计口径 
       ,loan_date 					--放款日期（pay_date） 
       ,'个人API复贷'                    AS flag
       ,act_added_api_p              AS day_loan_amt --`日放款` 
       ,act_added_api_p_ord          AS day_loan_cnt --`日订单数` 
       ,cum_act_added_api_p          AS month_loan_amt --`月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18)) AS target_point --`目标` 
       ,0                            AS month_loan_num --月放款人数 
       ,t3.act_added_api_p_asset     AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'            AS stat_type --统计口径 
       ,t1.loan_date             --放款日期（pay_date) 
       ,'个人APP首贷（新）'             AS flag
       ,t1.act_first_app_p       AS day_loan_amt --`日放款` 
       ,t1.act_first_app_p_ord   AS day_loan_cnt --`日订单数` 
       ,t1.cum_act_first_app_p   AS month_loan_amt --`月累计放款` 
       ,t2.first_app_tgt         AS target_point --`目标` 
       ,0                        AS month_loan_num --月放款人数 
       ,t3.act_first_app_p_asset AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10)             AS tgt_dt
	       ,SUM(app新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期) AS first_app_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                                                                                  AS stat_type --统计口径 
       ,t1.loan_date                                                                                   --放款日期（pay_date) 
       ,'个人APP复贷'                                                                                      AS flag
-- 下沉客群移动至个人复贷放款中 
       ,COALESCE(t1.act_added_p,0) + COALESCE(t1.act_a24_p,0) + COALESCE(t1.act_added_c,0)             AS day_loan_amt --`日放款` 
       ,COALESCE(t1.act_added_p_ord,0) + COALESCE(t1.act_a24_p_ord,0) + COALESCE(t1.act_added_c_ord,0) AS day_loan_cnt --`日订单数` 
       ,COALESCE(t1.cum_act_added_p) + COALESCE(t1.cum_act_a24_p) + COALESCE(t1.cum_act_added_c,0)     AS month_loan_amt --`月累计放款` 
       ,t2.added_tgt                                                                                   AS target_point --`目标` 
       ,0                                                                                              AS month_loan_num --月放款人数 
       ,t3.act_added_p_asset                                                                           AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt
	       ,SUM(老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期)AS added_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                                                                                                                     AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'自营总计'                                                                                                                            AS flag
       ,COALESCE(t1.act_added_c,0) + COALESCE(t1.act_added_p,0) + COALESCE(t1.act_a24_p,0) + COALESCE(t1.act_first_app_p,0) + COALESCE(t1.act_first_api_p,0)+ COALESCE(t1.act_added_api_p,0) AS day_loan_amt --`日放款` 
       ,COALESCE(t1.act_added_c_ord,0) + COALESCE(t1.act_added_p_ord,0) + COALESCE(t1.act_a24_p_ord,0) + COALESCE(t1.act_first_app_p_ord,0) + COALESCE(t1.act_first_api_p_ord,0) + COALESCE(t1.act_added_api_p_ord,0) AS day_loan_cnt --`日订单数` 
       ,COALESCE(t1.cum_act_added_c,0) + COALESCE(t1.cum_act_added_p,0) + COALESCE(t1.cum_act_a24_p,0) + COALESCE(t1.cum_act_first_app_p,0) + COALESCE(t1.cum_act_first_api_p,0) + COALESCE(t1.cum_act_added_api_p,0) AS month_loan_amt --`月累计放款` 
       ,t2.total_tgt                                                                                                                      AS target_point --`目标` 
       ,0                                                                                                                                 AS month_loan_num --月放款人数 
       ,nvl(t3.act_first_api_p_asset,0) + nvl(t3.act_added_api_p_asset,0) + nvl(t3.act_first_app_p_asset,0) + nvl(t3.act_added_p_asset,0) AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10)                        AS tgt_dt
	       ,SUM(app新客+api新客+老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期) AS total_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE()

----------新客部分-------------------------- 
UNION ALL
SELECT  'current_mth'                                                                                                 AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'APP首贷（APP授信）'                                                                                                AS flag
       ,COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0)             AS day_loan_amt --`日放款` 
       ,COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0) AS day_loan_cnt --`日订单数` 
       ,t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p                                     AS month_loan_amt --`月累计放款` 
       ,t2.first_app_tgt                                                                                              AS target_point --`目标` 
       ,0                                                                                                             AS month_loan_num --月放款人数 
       ,NULL                                                                                                          AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10)             AS tgt_dt
	       ,SUM(app新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期) AS first_app_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                 AS stat_type --统计口径 
       ,loan_date --放款日期（pay_date) 
       ,'APP首贷（API授信）'                AS flag
       ,act_first_apitoapp_p          AS day_loan_amt --`日放款` 
       ,act_first_apitoapp_p_ord      AS day_loan_cnt -- `日订单数` 
       ,cum_act_first_apitoapp_p      AS month_loan_amt --`月累计放款` 
       ,cum_day_target_first_apitoapp AS target_point --`目标` 
       ,0                             AS month_loan_num --月放款人数 
       ,NULL                          AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df
WHERE pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'      AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'新客总体'             AS flag
		-- API首贷 包含少量API复贷 
	   ,COALESCE(t1.act_first_api_p,0) + COALESCE(t1.act_added_api_p,0)
		-- APP首贷（APP授信） 
		+ COALESCE(t1.act_first_dx_p,0) + COALESCE(t1.act_first_xxl_p,0) + COALESCE(t1.act_first_other_p,0)
		-- APP首贷（API授信） 
		+ COALESCE(t1.act_first_apitoapp_p,0) AS day_loan_amt -- `日放款`
		-- API首贷 包含少量API复贷 
	   ,COALESCE(t1.act_first_api_p_ord,0) + COALESCE(t1.act_added_api_p_ord,0)
		-- APP首贷（APP授信） 
		+ COALESCE(t1.act_first_dx_p_ord,0) + COALESCE(t1.act_first_xxl_p_ord,0) + COALESCE(t1.act_first_other_p_ord,0)
		-- APP首贷（API授信） 
		+ COALESCE(t1.act_first_apitoapp_p_ord,0) AS day_loan_cnt -- `日订单数` 
       ,t1.cum_act_first_api_p + t1.cum_act_added_api_p + t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt -- `月累计放款` 
       ,t2.total_first_tgt AS target_point -- `目标` 
       ,0                  AS month_loan_num -- 月放款人数 
       ,NULL               AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10)                   AS tgt_dt
	       ,SUM(app新客+api新客) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期) AS total_first_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE()
----------------老客部分------------------------------- 
 
UNION ALL

SELECT  'current_mth'                 AS stat_type --统计口径 
       ,loan_date --放款日期（pay_date) 
       ,'APP首贷（API首贷）'                AS flag
       ,act_added_apitoapp_p          AS day_loan_amt --`日放款` 
       ,act_added_apitoapp_p_ord      AS day_loan_cnt --`日订单数` 
       ,cum_act_added_apitoapp_p      AS month_loan_amt --`月累计放款` 
       ,cum_day_target_added_apitoapp AS target_point --`目标` 
       ,0                             AS month_loan_num --月放款人数 
       ,NULL                          AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df
WHERE pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                                                                      AS stat_type --统计口径 
       ,loan_date --放款日期（pay_date) 
       ,'APP放款'                                                                            AS flag
       ,COALESCE(act_added_p,0) + COALESCE(act_a24_p,0) - act_added_apitoapp_p             AS day_loan_amt --`日放款` 
       ,COALESCE(act_added_p_ord,0) + COALESCE(act_a24_p_ord,0) - act_added_apitoapp_p_ord AS day_loan_cnt --`日订单数` 
       ,cum_act_added_p + cum_act_a24_p - cum_act_added_apitoapp_p                         AS month_loan_amt --`月累计放款` 
       ,0                                                                                  AS target_point --`目标` 
       ,0                                                                                  AS month_loan_num --月放款人数 
       ,NULL                                                                               AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df
WHERE pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'current_mth'                                                 AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'老客总体'                                                        AS flag
       ,COALESCE(t1.act_added_p,0) + COALESCE(t1.act_a24_p,0)         AS day_loan_amt --`日放款` 
       ,COALESCE(t1.act_added_p_ord,0) + COALESCE(t1.act_a24_p_ord,0) AS day_loan_cnt --`日订单数` 
       ,t1.cum_act_added_p + t1.cum_act_a24_p                         AS month_loan_amt --`月累计放款` 
       ,t2.added_tgt                                                  AS target_point --`目标` 
       ,0                                                             AS month_loan_num --月放款人数 
       ,NULL                                                          AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN
(
	SELECT  substr(to_date(日期,'yyyy-mm-dd hh:mi:ss'),1,10) AS tgt_dt
	       ,SUM(老客预估) OVER (PARTITION BY substr(日期,1,7) ORDER BY  日期)AS added_tgt
	FROM xyf_bi_dev.amt_predict_oct24_v2
) t2
ON substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10)
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE()
------------ 总体部分 月度汇总 -----------------------------
-- 月度总计以及未来月份目标 
 
UNION ALL

SELECT  'mthly_summary'                                AS stat_type --统计口径 
       ,t1.loan_date                                    --放款日期（pay_date) 
       ,'个人API首贷'                                      AS flag
       ,t1.cum_act_first_api_p / DAY(t1.loan_date)     AS day_loan_amt --`日均放款` 
       ,t1.cum_act_first_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt --`日均订单数` 
       ,t1.cum_act_first_api_p                         AS month_loan_amt --`月累计放款` 
       ,t1.cum_day_target_first_api_p                  AS target_point --`目标` 
       ,t2.act_first_api_p_mthly_id                    AS month_loan_num --`月度放款人数` 
       ,NULL                                           AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_first_api_p
	       ,b.cum_act_first_api_p_ord
	       ,b.cum_day_target_first_api_p
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                AS stat_type --统计口径 
       ,t1.loan_date                          --放款日期（pay_date) 
       ,'个人API复贷'                                      AS flag
       ,t1.cum_act_added_api_p / DAY(t1.loan_date)     AS day_loan_amt --`日均放款` 
       ,t1.cum_act_added_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt --`日均订单数` 
       ,t1.cum_act_added_api_p                         AS month_loan_amt -- `月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18))                   AS target_point -- `目标` 
       ,t2.act_added_api_p_mthly_id                    AS month_loan_num -- `月度放款人数` 
       ,NULL                                           AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_added_api_p
	       ,b.cum_act_added_api_p_ord
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'个人APP首贷（新）'                                   AS flag
       ,t1.cum_act_first_app_p / DAY(t1.loan_date)     AS day_loan_amt -- `日均放款` 
       ,t1.cum_act_first_app_p_ord / DAY(t1.loan_date) AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_first_app_p                         AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_first_app_p                  AS target_point -- `目标` 
       ,t2.act_first_app_p_mthly_id                    AS month_loan_num -- `月度放款人数` 
       ,NULL                                           AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_first_app_p
	       ,b.cum_act_first_app_p_ord
	       ,b.cum_day_target_first_app_p
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                   AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'个人APP复贷'                                         AS flag
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c) /DAY(t1.loan_date)  ELSE (t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date) END AS day_loan_amt -- `日均放款` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date)  ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt -- `日均订单数` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_added_c  ELSE t1.cum_act_added_p + t1.cum_act_a24_p END AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_added_p + t1.cum_day_target_a24 AS target_point -- `目标` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + COALESCE(t3.act_added_c_mthly_id,0)  ELSE (COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0)) END AS month_loan_num -- `月累计放款人数` 
       ,NULL                                              AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                      AS loan_date
	       ,a.month_id_iso                    AS loan_month
	       ,b.cum_act_added_p
	       ,b.cum_act_a24_p
	       ,COALESCE(b.cum_act_added_c,0)     AS cum_act_added_c -- 
	       ,b.cum_act_added_p_ord
	       ,b.cum_act_a24_p_ord
	       ,COALESCE(b.cum_act_added_c_ord,0) AS cum_act_added_c_ord -- 
	       ,b.cum_day_target_added_p
	       ,b.cum_day_target_a24
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month
LEFT JOIN
(
	SELECT  substr(loan_time,1,7) AS loan_month
	       ,COUNT(DISTINCT cust_no) act_added_c_mthly_id
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = max_pt('xyf_dws.dws_inloan_user_order_df')
	AND app IN ('cxh')
	AND DATE(loan_time) >= '2023-01-01'
	GROUP BY  substr(loan_time,1,7)
) t3
ON t1.loan_month = t3.loan_month

UNION ALL

SELECT  'mthly_summary'                                                                                                                               AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'自营总计'                                                                                                                                        AS flag
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p) / DAY(t1.loan_date)  
	   		ELSE (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p) / DAY(t1.loan_date) END AS day_loan_amt -- `日均放款` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date)  
	   		ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt --`日均订单数` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p  
	   		ELSE t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p END AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_added_c + t1.cum_day_target_added_p + t1.cum_day_target_a24 + t1.cum_day_target_first_app_p + t1.cum_day_target_first_api_p AS target_point -- `目标` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN COALESCE(t3.act_added_c_mthly_id,0) + t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id  
	   		ELSE t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id END AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                                                                                                          AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                             AS loan_date
	       ,a.month_id_iso                           AS loan_month
	       ,b.cum_act_added_p
	       ,b.cum_act_a24_p
	       ,b.cum_act_first_app_p
	       ,b.cum_act_first_api_p
	       ,COALESCE(b.cum_act_added_c,0)            AS cum_act_added_c
	       ,b.cum_act_added_api_p
	       ,b.cum_act_added_p_ord
	       ,b.cum_act_a24_p_ord
	       ,b.cum_act_first_app_p_ord
	       ,b.cum_act_first_api_p_ord
	       ,b.cum_act_added_api_p_ord
	       ,COALESCE(b.cum_act_added_c_ord,0)        AS cum_act_added_c_ord
	       ,COALESCE(b.cum_day_target_added_c,0)     AS cum_day_target_added_c
	       ,COALESCE(b.cum_day_target_added_p,0)     AS cum_day_target_added_p
	       ,COALESCE(b.cum_day_target_a24,0)         AS cum_day_target_a24
	       ,COALESCE(b.cum_day_target_first_app_p,0) AS cum_day_target_first_app_p
	       ,COALESCE(b.cum_day_target_first_api_p,0) AS cum_day_target_first_api_p
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month
LEFT JOIN
(
	SELECT  substr(loan_time,1,7) AS loan_month
	       ,COUNT(DISTINCT cust_no) act_added_c_mthly_id
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = max_pt('xyf_dws.dws_inloan_user_order_df')
	AND app IN ('cxh')
	AND DATE(loan_time) >= '2023-01-01'
	GROUP BY  substr(loan_time,1,7)
) t3
ON t1.loan_month = t3.loan_month

------------- 新客部分 月度汇总 --------------------------- 
UNION ALL

SELECT  'mthly_summary'                                                                                             AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'APP首贷（APP授信）'                                                                                              AS flag
       ,(t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p) / DAY(t1.loan_date)             AS day_loan_amt -- `日均放款` 
       ,(t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord) / DAY(t1.loan_date) AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p                                   AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_first_app_p                                                                               AS target_point -- `目标` 
       ,t2.act_first_dx_p_mthly_id + t2.act_first_xxl_p_mthly_id + t2.act_first_other_p_mthly_id                    AS month_loan_num --`月累计放款人数` 
       ,NULL                                                                                                        AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                             AS loan_date
	       ,a.month_id_iso                           AS loan_month
	       ,COALESCE(b.cum_act_first_dx_p,0)         AS cum_act_first_dx_p
	       ,COALESCE(b.cum_act_first_xxl_p,0)        AS cum_act_first_xxl_p
	       ,COALESCE(b.cum_act_first_other_p,0)      AS cum_act_first_other_p
	       ,COALESCE(b.cum_act_first_dx_p_ord,0)     AS cum_act_first_dx_p_ord
	       ,COALESCE(b.cum_act_first_xxl_p_ord,0)    AS cum_act_first_xxl_p_ord
	       ,COALESCE(b.cum_act_first_other_p_ord,0)  AS cum_act_first_other_p_ord
	       ,COALESCE(b.cum_day_target_first_app_p,0) AS cum_day_target_first_app_p
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                     AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'APP首贷（API授信）'                                      AS flag
       ,t1.cum_act_first_apitoapp_p / DAY(t1.loan_date)     AS day_loan_amt -- `日均放款` 
       ,t1.cum_act_first_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_first_apitoapp_p                         AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_first_apitoapp                    AS target_point -- `目标` 
       ,t2.act_first_apitoapp_p_mthly_id                    AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_first_apitoapp_p
	       ,b.cum_act_first_apitoapp_p_ord
	       ,b.cum_day_target_first_apitoapp
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                                                                  AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'新客总体'                                                                                           AS flag
		-- API首贷 包含少量API复贷 
	   ,(t1.cum_act_first_api_p + t1.cum_act_added_api_p --717新增API复贷
		-- APP首贷（APP授信） 
		+ t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p
		-- APP首贷（API授信） 
		+ t1.cum_act_first_apitoapp_p) / DAY(t1.loan_date) AS day_loan_amt --`日均放款`
		-- API首贷 包含少量API复贷 
	   ,(t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord --717新增API复贷
		-- APP首贷（APP授信） 
		+ t1.cum_act_first_dx_p_ord + t1.cum_act_first_xxl_p_ord + t1.cum_act_first_other_p_ord
		-- APP首贷（API授信） 
		+ t1.cum_act_first_apitoapp_p_ord) / DAY(t1.loan_date) AS day_loan_cnt -- `日均订单数` 
	   ,t1.cum_act_first_api_p + t1.cum_act_added_api_p + --717新增API复贷 
		t1.cum_act_first_dx_p + t1.cum_act_first_xxl_p + t1.cum_act_first_other_p + t1.cum_act_first_apitoapp_p AS month_loan_amt -- `月累计放款` 
	   ,t1.cum_day_target_first_api_p + t1.cum_day_target_first_app_p + t1.cum_day_target_first_apitoapp AS target_point -- `目标`
		-- API首贷 包含少量API复贷 
	   ,COALESCE(t2.act_first_api_p_mthly_id,0) + COALESCE(t2.act_added_api_p_mthly_id,0)
		-- APP首贷（APP授信） 
		+ COALESCE(t2.act_first_dx_p_mthly_id,0) + COALESCE(t2.act_first_xxl_p_mthly_id,0) + COALESCE(t2.act_first_other_p_mthly_id,0)
		-- APP首贷（API授信） 
		+ COALESCE(t2.act_first_apitoapp_p_mthly_id,0) AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                                                             AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                                AS loan_date
	       ,a.month_id_iso                              AS loan_month
	       ,COALESCE(b.cum_act_first_api_p,0)           AS cum_act_first_api_p
	       ,COALESCE(b.cum_act_added_api_p,0)           AS cum_act_added_api_p
	       ,COALESCE(b.cum_act_first_apitoapp_p,0)      AS cum_act_first_apitoapp_p
	       ,COALESCE(b.cum_act_first_api_p_ord,0)       AS cum_act_first_api_p_ord
	       ,COALESCE(b.cum_act_added_api_p_ord,0)       AS cum_act_added_api_p_ord
	       ,COALESCE(b.cum_act_first_apitoapp_p_ord,0)  AS cum_act_first_apitoapp_p_ord
	       ,COALESCE(b.cum_act_first_dx_p,0)            AS cum_act_first_dx_p
	       ,COALESCE(b.cum_act_first_xxl_p,0)           AS cum_act_first_xxl_p
	       ,COALESCE(b.cum_act_first_other_p,0)         AS cum_act_first_other_p
	       ,COALESCE(b.cum_act_first_dx_p_ord,0)        AS cum_act_first_dx_p_ord
	       ,COALESCE(b.cum_act_first_xxl_p_ord,0)       AS cum_act_first_xxl_p_ord
	       ,COALESCE(b.cum_act_first_other_p_ord,0)     AS cum_act_first_other_p_ord
	       ,COALESCE(b.cum_day_target_first_api_p,0)    AS cum_day_target_first_api_p
	       ,COALESCE(b.cum_day_target_first_app_p,0)    AS cum_day_target_first_app_p
	       ,COALESCE(b.cum_day_target_first_apitoapp,0) AS cum_day_target_first_apitoapp
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

-------------- 老客部分 ------------------------- 
UNION ALL

SELECT  'mthly_summary'                                     AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'APP首贷（API首贷）'                                      AS flag
       ,t1.cum_act_added_apitoapp_p / DAY(t1.loan_date)     AS day_loan_amt -- `日均放款` 
       ,t1.cum_act_added_apitoapp_p_ord / DAY(t1.loan_date) AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_added_apitoapp_p                         AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_added_apitoapp                    AS target_point -- `目标` 
       ,COALESCE(t2.act_added_apitoapp_p_mthly_id,0)        AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_added_apitoapp_p
	       ,b.cum_act_added_apitoapp_p_ord
	       ,b.cum_day_target_added_apitoapp
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                                                                                                             AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'APP放款'                                                                                                                                     AS flag
       ,(t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p) / DAY(t1.loan_date)                                                   AS day_loan_amt -- `日均放款` 
       ,(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord - t1.cum_act_added_apitoapp_p_ord) / DAY(t1.loan_date)                                       AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_added_p + t1.cum_act_a24_p - t1.cum_act_added_apitoapp_p                                                                         AS month_loan_amt -- `月累计放款` 
       ,CASE WHEN t1.loan_date < '2024-01-01' THEN t1.cum_day_target_added_p + t1.cum_day_target_a24 - t1.cum_day_target_added_apitoapp  ELSE 0 END AS target_point -- `目标` 
       ,COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) - COALESCE(t2.act_added_apitoapp_p_mthly_id,0)                      AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                                                                                                        AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                               AS loan_date
	       ,a.month_id_iso                             AS loan_month
	       ,COALESCE(b.cum_act_added_p,0)              AS cum_act_added_p
	       ,COALESCE(b.cum_act_a24_p,0)                AS cum_act_a24_p
	       ,COALESCE(b.cum_act_added_apitoapp_p,0)     AS cum_act_added_apitoapp_p
	       ,COALESCE(b.cum_act_added_p_ord,0)          AS cum_act_added_p_ord
	       ,COALESCE(b.cum_act_a24_p_ord,0)            AS cum_act_a24_p_ord
	       ,COALESCE(b.cum_act_added_apitoapp_p_ord,0) AS cum_act_added_apitoapp_p_ord
	       ,b.cum_day_target_added_p
	       ,b.cum_day_target_a24
	       ,b.cum_day_target_added_apitoapp
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'                                                         AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'老客总体'                                                                  AS flag
       ,(t1.cum_act_added_p + t1.cum_act_a24_p) / DAY(t1.loan_date)             AS day_loan_amt -- `日均放款` 
       ,(t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord) / DAY(t1.loan_date)     AS day_loan_cnt -- `日均订单数` 
       ,t1.cum_act_added_p + t1.cum_act_a24_p                                   AS month_loan_amt -- `月累计放款` 
       ,t1.cum_day_target_added_p + t1.cum_day_target_a24                       AS target_point -- `目标` 
       ,COALESCE(t2.act_added_p_mthly_id,0) + COALESCE(t2.act_a24_p_mthly_id,0) AS month_loan_num -- `月累计放款人数` 
       ,NULL                                                                    AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                      AS loan_date
	       ,a.month_id_iso                    AS loan_month
	       ,COALESCE(b.cum_act_added_p,0)     AS cum_act_added_p
	       ,COALESCE(b.cum_act_a24_p,0)       AS cum_act_a24_p
	       ,COALESCE(b.cum_act_added_p_ord,0) AS cum_act_added_p_ord
	       ,COALESCE(b.cum_act_a24_p_ord,0)   AS cum_act_a24_p_ord
	       ,b.cum_day_target_added_p
	       ,b.cum_day_target_a24
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- 
	AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month
------------ API导流业务数据 月度汇总 -----------------------------

UNION ALL

SELECT  'mthly_summary'                   AS stat_type --统计口径 
       ,day_id_iso                        AS loan_date --放款日期（pay_date) 
       ,'导流'                              AS flag
       ,cum_day_loan_amt / DAY(loan_date) AS day_loan_amt --`日均放款` 
       ,cum_day_loan_cnt / DAY(loan_date) AS day_loan_cnt --`日均订单数` 
       ,cum_day_loan_amt                  AS month_loan_amt --`月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18))      AS target_point --`目标` 
       ,t2.month_loan_num --`月度放款人数` 
       ,NULL                              AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso
	       ,substr(a.day_id_iso,1,7) AS loan_month
	       ,v2.*
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN
	(
		SELECT  loan_date
		       ,SUM(day_loan_amt) OVER (PARTITION BY substr(loan_date,1,7) ORDER BY  loan_date) / 100 /100000000 AS cum_day_loan_amt
		       ,SUM(day_loan_cnt) OVER (PARTITION BY substr(loan_date,1,7) ORDER BY loan_date)                   AS cum_day_loan_cnt
		FROM
		(
			SELECT  loan_date
			       ,SUM(CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN amount ELSE 0 END)       AS day_loan_amt
			       ,COUNT(DISTINCT CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN order_no END) AS day_loan_cnt
			FROM ads_inloan_loan_monitor_screen_df_01
			WHERE name NOT IN ('信用飞', '畅行花', '飞行卡')
			AND loan_date >= '2024-01-01'
			GROUP BY  loan_date
		)v1
	) v2
	ON v2.loan_date = a.day_id_iso
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
) t1
LEFT JOIN
(
	SELECT  SUBSTR(loan_date,1,7)                                                             AS loan_month
	       ,COUNT(DISTINCT CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN user_id END) AS month_loan_num
	FROM ads_inloan_loan_monitor_screen_df_01
	WHERE name NOT IN ('信用飞', '畅行花', '飞行卡')
	AND loan_date >= '2024-01-01'
	GROUP BY  SUBSTR(loan_date,1,7)
) t2
ON t1.loan_month = t2.loan_month
--导流备份/自营总计备份(mthly_summary)用于帆软自定义分组用，和上面的导流自营总计(mthly_summary)数据一模一样，纯为了帆软展示方便用（自营+导流总计） 20250418 

UNION ALL

SELECT  'mthly_summary'                   AS stat_type --统计口径 
       ,day_id_iso                        AS loan_date --放款日期（pay_date) 
       ,'导流备份'                            AS flag
       ,cum_day_loan_amt / DAY(loan_date) AS day_loan_amt --`日均放款` 
       ,cum_day_loan_cnt / DAY(loan_date) AS day_loan_cnt --`日均订单数` 
       ,cum_day_loan_amt                  AS month_loan_amt --`月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18))      AS target_point --`目标` 
       ,t2.month_loan_num --`月度放款人数` 
       ,NULL                              AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso
	       ,substr(a.day_id_iso,1,7) AS loan_month
	       ,v2.*
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN
	(
		SELECT  loan_date
		       ,SUM(day_loan_amt) OVER (PARTITION BY substr(loan_date,1,7) ORDER BY  loan_date) / 100 /100000000 AS cum_day_loan_amt
		       ,SUM(day_loan_cnt) OVER (PARTITION BY substr(loan_date,1,7) ORDER BY loan_date)                   AS cum_day_loan_cnt
		FROM
		(
			SELECT  loan_date
			       ,SUM(CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN amount ELSE 0 END)       AS day_loan_amt
			       ,COUNT(DISTINCT CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN order_no END) AS day_loan_cnt
			FROM ads_inloan_loan_monitor_screen_df_01
			WHERE name NOT IN ('信用飞', '畅行花', '飞行卡')
			AND loan_date >= '2024-01-01'
			GROUP BY  loan_date
		)v1
	) v2
	ON v2.loan_date = a.day_id_iso
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
) t1
LEFT JOIN
(
	SELECT  SUBSTR(loan_date,1,7)                                                             AS loan_month
	       ,COUNT(DISTINCT CASE WHEN STATUS >= 22 AND STATUS NOT IN (23,24) THEN user_id END) AS month_loan_num
	FROM ads_inloan_loan_monitor_screen_df_01
	WHERE name NOT IN ('信用飞', '畅行花', '飞行卡')
	AND loan_date >= '2024-01-01'
	GROUP BY  SUBSTR(loan_date,1,7)
) t2
ON t1.loan_month = t2.loan_month

UNION ALL

SELECT  'mthly_summary'              AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'自营总计备份'                     AS flag
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p) / DAY(t1.loan_date)  
	    	ELSE (t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p) / DAY(t1.loan_date) END AS day_loan_amt -- `日均放款` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord + t1.cum_act_added_c_ord) / DAY(t1.loan_date)  
	    	ELSE (t1.cum_act_added_p_ord + t1.cum_act_a24_p_ord + t1.cum_act_first_app_p_ord + t1.cum_act_first_api_p_ord + t1.cum_act_added_api_p_ord) / DAY(t1.loan_date) END AS day_loan_cnt --`日均订单数` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_c + t1.cum_act_added_api_p  
			ELSE t1.cum_act_added_p + t1.cum_act_a24_p + t1.cum_act_first_app_p + t1.cum_act_first_api_p + t1.cum_act_added_api_p END AS month_loan_amt -- `月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18)) AS target_point -- `目标` 
       ,CASE WHEN t1.loan_date >= '2024-04-01' THEN COALESCE(t3.act_added_c_mthly_id,0) + t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id  
	   		ELSE t2.act_added_p_mthly_id + t2.act_a24_p_mthly_id + t2.act_first_app_p_mthly_id + t2.act_first_api_p_mthly_id + t2.act_added_api_p_mthly_id END AS month_loan_num -- `月累计放款人数` 
       ,NULL                         AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso                             AS loan_date
	       ,a.month_id_iso                           AS loan_month
	       ,b.cum_act_added_p
	       ,b.cum_act_a24_p
	       ,b.cum_act_first_app_p
	       ,b.cum_act_first_api_p
	       ,COALESCE(b.cum_act_added_c,0)            AS cum_act_added_c
	       ,b.cum_act_added_api_p
	       ,b.cum_act_added_p_ord
	       ,b.cum_act_a24_p_ord
	       ,b.cum_act_first_app_p_ord
	       ,b.cum_act_first_api_p_ord
	       ,b.cum_act_added_api_p_ord
	       ,COALESCE(b.cum_act_added_c_ord,0)        AS cum_act_added_c_ord
	       ,COALESCE(b.cum_day_target_added_c,0)     AS cum_day_target_added_c
	       ,COALESCE(b.cum_day_target_added_p,0)     AS cum_day_target_added_p
	       ,COALESCE(b.cum_day_target_a24,0)         AS cum_day_target_a24
	       ,COALESCE(b.cum_day_target_first_app_p,0) AS cum_day_target_first_app_p
	       ,COALESCE(b.cum_day_target_first_api_p,0) AS cum_day_target_first_api_p
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month
LEFT JOIN
(
	SELECT  substr(loan_time,1,7) AS loan_month
	       ,COUNT(DISTINCT cust_no) act_added_c_mthly_id
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = max_pt('xyf_dws.dws_inloan_user_order_df')
	AND app IN ('cxh')
	AND DATE(loan_time) >= '2023-01-01'
	GROUP BY  substr(loan_time,1,7)
) t3
ON t1.loan_month = t3.loan_month
UNION ALL
SELECT  'current_mth'                AS stat_type --统计口径 
       ,loan_date --放款日期（pay_date） 
       ,'个人API复贷备份'                  AS flag
       ,act_added_api_p              AS day_loan_amt --`日放款` 
       ,act_added_api_p_ord          AS day_loan_cnt --`日订单数` 
       ,cum_act_added_api_p          AS month_loan_amt --`月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18)) AS target_point --`目标` 
       ,0                            AS month_loan_num --月放款人数 
       ,t3.act_added_api_p_asset     AS day_asset_amt --每日资产金额 
FROM xyf_dws.dws_inloan_loan_channel_stat_df t1
LEFT JOIN xyf_dws.dws_inloan_loan_risk_stat_df t3
ON t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')
WHERE t1.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
AND substr(t1.loan_date, 1, 7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN substr(date_add(CURRENT_DATE(), -5), 1, 7 ) ELSE substr(CURRENT_DATE(), 1, 7) END
AND t1.loan_date < CURRENT_DATE() 

UNION ALL

SELECT  'mthly_summary'                                AS stat_type --统计口径 
       ,t1.loan_date --放款日期（pay_date) 
       ,'个人API复贷备份'                                    AS flag
       ,t1.cum_act_added_api_p / DAY(t1.loan_date)     AS day_loan_amt --`日均放款` 
       ,t1.cum_act_added_api_p_ord / DAY(t1.loan_date) AS day_loan_cnt --`日均订单数` 
       ,t1.cum_act_added_api_p                         AS month_loan_amt -- `月累计放款` 
       ,CAST(NULL AS DECIMAL(38,18))                   AS target_point -- `目标` 
       ,t2.act_added_api_p_mthly_id                    AS month_loan_num -- `月度放款人数` 
       ,NULL                                           AS day_asset_amt --资产金额 
FROM
(
	SELECT  a.day_id_iso   AS loan_date
	       ,a.month_id_iso AS loan_month
	       ,b.cum_act_added_api_p
	       ,b.cum_act_added_api_p_ord
	FROM xyf_dim.dim_pub_date a
	LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df b
	ON b.loan_date = a.day_id_iso AND b.pt = MAX_PT('xyf_dws.dws_inloan_loan_channel_stat_df')
	WHERE a.day_id_iso >= '2024-01-01'
	AND a.day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
	-- AND a.day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，历史数据从24年1.1开始，后面要保持修改这个时间范围 
	AND a.is_lastday = 1 --取月末最后一天 
 
)t1
LEFT JOIN xyf_dws.dws_inloan_loan_channel_stat_df_04 t2
ON t1.loan_month = t2.loan_month
;
