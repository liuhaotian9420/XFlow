CREATE TABLE IF NOT EXISTS dws_inloan_loan_channel_stat_df
(
    loan_date                          STRING COMMENT '借款日期'
    ,act_first_api_p                   DECIMAL(38,18) COMMENT '个人API首贷金额'
    ,act_added_api_p                   DECIMAL(38,18) COMMENT '个人API复贷金额'
    ,act_first_app_p                   DECIMAL(38,18) COMMENT '个人APP首贷金额'
    ,act_first_dx_p                    DECIMAL(38,18) COMMENT '个人APP首贷_短信金额'
    ,act_first_xxl_p                   DECIMAL(38,18) COMMENT '个人APP首贷_信息流金额'
    ,act_first_other_p                 DECIMAL(38,18) COMMENT '个人APP首贷_其他金额'
    ,act_first_apitoapp_p              DECIMAL(38,18) COMMENT '个人APP首贷API首贷金额'
    ,act_added_p                       DECIMAL(38,18) COMMENT '个人APP复贷金额'
    ,act_a24_p                         BIGINT COMMENT '废弃，默认为0'
    ,act_added_apitoapp_p              DECIMAL(38,18) COMMENT '个人APP复贷API复贷金额'
    ,act_added_c                       DOUBLE COMMENT '现金贷(畅行花)金额'
    ,act_first_api_p_ord               BIGINT COMMENT '个人API首贷订单量'
    ,act_added_api_p_ord               BIGINT COMMENT '个人API复贷订单量'
    ,act_first_app_p_ord               BIGINT COMMENT '个人APP首贷订单量'
    ,act_first_dx_p_ord                BIGINT COMMENT '个人APP首贷_短信订单量'
    ,act_first_xxl_p_ord               BIGINT COMMENT '个人APP首贷_信息流订单量'
    ,act_first_other_p_ord             BIGINT COMMENT '个人APP首贷_其他订单量'
    ,act_first_apitoapp_p_ord          BIGINT COMMENT '个人APP首贷API首贷订单量'
    ,act_added_p_ord                   BIGINT COMMENT '个人APP复贷订单量'
    ,act_a24_p_ord                     BIGINT COMMENT '废弃，默认为0'
    ,act_added_apitoapp_p_ord          BIGINT COMMENT '个人APP复贷API复贷订单量'
    ,act_added_c_ord                   DOUBLE COMMENT '现金贷(畅行花)订单量'
    ,cum_act_first_api_p               DECIMAL(38,18) COMMENT '累计个人API首贷金额'
    ,cum_act_added_api_p               DECIMAL(38,18) COMMENT '累计个人API复贷金额'
    ,cum_act_first_app_p               DECIMAL(38,18) COMMENT '累计个人APP首贷金额'
    ,cum_act_first_dx_p                DECIMAL(38,18) COMMENT '累计个人APP首贷_短信金额'
    ,cum_act_first_xxl_p               DECIMAL(38,18) COMMENT '累计个人APP首贷_信息流金额'
    ,cum_act_first_other_p             DECIMAL(38,18) COMMENT '累计个人APP首贷_其他金额'
    ,cum_act_first_apitoapp_p          DECIMAL(38,18) COMMENT '累计个人APP首贷API首贷金额'
    ,cum_act_added_p                   DECIMAL(38,18) COMMENT '累计个人APP复贷金额'
    ,cum_act_a24_p                     BIGINT COMMENT '废弃，默认为0'
    ,cum_act_added_apitoapp_p          DECIMAL(38,18) COMMENT '累计个人APP复贷API复贷金额'
    ,cum_act_added_c                   DOUBLE COMMENT '累计现金贷(畅行花)金额'
    ,cum_act_first_api_p_ord           BIGINT COMMENT '累计个人API首贷订单量'
    ,cum_act_added_api_p_ord           BIGINT COMMENT '累计个人API复贷订单量'
    ,cum_act_first_app_p_ord           BIGINT COMMENT '累计个人APP首贷订单量'
    ,cum_act_first_dx_p_ord            BIGINT COMMENT '累计个人APP首贷_短信订单量'
    ,cum_act_first_xxl_p_ord           BIGINT COMMENT '累计个人APP首贷_信息流订单量'
    ,cum_act_first_other_p_ord         BIGINT COMMENT '累计个人APP首贷_其他订单量'
    ,cum_act_first_apitoapp_p_ord      BIGINT COMMENT '累计个人APP首贷API首贷订单量'
    ,cum_act_added_p_ord               BIGINT COMMENT '累计个人APP复贷订单量'
    ,cum_act_a24_p_ord                 BIGINT COMMENT '废弃，默认为0'
    ,cum_act_added_apitoapp_p_ord      BIGINT COMMENT '累计个人APP复贷API复贷订单量'
    ,cum_act_added_c_ord               DOUBLE COMMENT '累计现金贷(畅行花)订单量'
    ,cum_day_target_first_api_p        DECIMAL(38,18) COMMENT '累计个人_首贷API目标金额'
    ,cum_day_target_first_app_p        DECIMAL(38,18) COMMENT '累计个人_首贷APP目标金额'
    ,cum_day_target_first_xxl_p        DECIMAL(38,18) COMMENT '累计个人_信息流目标金额'
    ,cum_day_target_first_dx_p         DECIMAL(38,18) COMMENT '累计个人_短信目标金额'
    ,cum_day_target_first_other_p      DECIMAL(38,18) COMMENT '累计个人_其他-付费目标金额'
    ,cum_day_target_first_other_p_free DECIMAL(38,18) COMMENT '累计个人_其他目标金额'
    ,cum_day_target_added_p            DECIMAL(38,18) COMMENT '累计个人_复贷目标金额'
    ,cum_day_target_total_p            DECIMAL(38,18) COMMENT '累计个人_分期整体目标金额'
    ,cum_day_target_a24                DECIMAL(38,18) COMMENT '累计下探_复贷A24目标金额'
    ,cum_day_target_added_c            DECIMAL(38,18) COMMENT '累计现金_复贷目标金额'
    ,cum_day_target_first_api          DECIMAL(38,18) COMMENT '累计整体_首贷API目标金额'
    ,cum_day_target_first_app          DECIMAL(38,18) COMMENT '累计整体_首贷APP目标金额'
    ,cum_day_target_first_xxl          DECIMAL(38,18) COMMENT '累计整体_信息流目标金额'
    ,cum_day_target_first_dx           DECIMAL(38,18) COMMENT '累计整体_短信目标金额'
    ,cum_day_target_first_other        DECIMAL(38,18) COMMENT '累计整体_其他目标金额'
    ,cum_day_target_added              DECIMAL(38,18) COMMENT '累计整体_复贷目标金额'
    ,cum_day_target_total              DECIMAL(38,18) COMMENT '累计整体目标金额'
    ,cum_day_target_first_apitoapp     DECIMAL(38,18) COMMENT '累计个人_APItoAPP首贷目标金额'
    ,cum_day_target_added_apitoapp     DECIMAL(38,18) COMMENT '累计个人_APItoAPP复贷目标金额'
)
PARTITIONED BY 
(
    pt                                 STRING COMMENT '分区日期'
)
STORED AS ALIORC
TBLPROPERTIES ('columnar.nested.type' = 'true','comment' = '贷中app/api渠道放款量级统计')
LIFECYCLE 365
;


DROP TABLE IF EXISTS dws_inloan_loan_channel_stat_df_01;
CREATE TABLE dws_inloan_loan_channel_stat_df_01 AS

SELECT  t1.first_order_number
       ,t1.order_number
       ,t1.user_no
       ,t1.cust_no
       ,DATE(t1.loan_time)                                                                    AS loan_date
       ,substr(t1.loan_time,1,7)                                                              AS loan_month
       ,t1.loan_amt
       ,t1.loan_flag
       ,t1.inner_app
       ,t1.asset_type_flag
       ,CASE WHEN t1.business_line = 'API' THEN 'API'  ELSE 'APP' END                         AS pay_channel
       ,CASE WHEN t4.business_line = 'API' THEN 'API'  ELSE 'APP' END                         AS first_loan_channel --首笔放款渠道
       ,t2.credit_type
       ,t2.biz_type
       ,t3.register_channel
       ,t1.all_channel_loan_rk
       ,CASE WHEN t2.credit_type = 'API' THEN t2.biz_type  ELSE t3.register_channel END       AS credit_channel -- APP首贷渠道归因
       ,CASE WHEN t1.all_channel_loan_rk = 1 AND t2.credit_type <> 'xyf01_cxh' THEN '首贷' --722新增
             WHEN t1.all_channel_loan_rk > 1 AND t1.loan_flag = '加贷' THEN '加贷'  ELSE '复贷' END AS loan_times_flag
FROM
(
	SELECT  first_order_number
	       ,order_number
	       ,user_no
	       ,cust_no
	       ,inner_app
	       ,loan_time
	       ,loan_amt
	       ,loan_flag
	       ,asset_type_flag
	       ,business_line
	       ,ROW_NUMBER () OVER (PARTITION BY cust_no ORDER BY  loan_time) AS all_channel_loan_rk --全站渠道放款次数 -- 放款排序
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = MAX_PT("xyf_dws.dws_inloan_user_order_df")
	AND app IN ('xyf01', 'fxk')
	AND inner_app NOT IN ('fxk_hexj', 'fxk_aj360', 'fxk_zyxj', 'fxk01_360zybx', 'fxk01_360zyaj')  --剔除融资担保项目 
	-- AND substr(loan_time, 1, 7) >= '2023-01-01'
	AND loan_time IS NOT NULL 
) t1
LEFT JOIN
(
	SELECT  a.user_no
	       ,a.cust_no
	       ,a.inner_app
	       ,a.utm_source
	       ,CASE WHEN a.utm_source IN ('XYF01-API-PPD01' ,'XYF01-API-JDD01' ,'XYF01-API-HBEI01' ,'XYF01-API-RSH5' ,
                                          'XYF01-API-HBWEAPP01' ,'XYF01-API-HBHXD01' ,'XYF01-API-NWD01' ,'XYF01-API-HBHXJ01' ,'XYF01-API-YQG01' ,
                                          'XYF01-API-OPPO01' ,'FXK-API-HEXJ' ,'FXK-API-YQG01' ,'XYF01-API-BR01' ,'XYF01-API-RS01') THEN 'API不可营销'  
               ELSE 'API可营销' END AS biz_type
	       ,CASE WHEN lower(inner_app) IN ('xyf01','fxk') THEN 'APP'
	             WHEN lower(inner_app) = 'xyf01_cxh' THEN 'xyf01_cxh'  ELSE 'API' END AS credit_type --722新增
	       ,ROW_NUMBER() OVER(PARTITION BY a.cust_no ORDER BY  a.created_time)        AS rn --取首次授信
	FROM xyf_dwd.dwd_preloan_credit_apply_df a
	WHERE a.pt = MAX_PT("xyf_dwd.dwd_preloan_credit_apply_df")
	AND a.app IN ('xyf01', 'fxk')
	AND a.STATUS = 2 --审批通过
	AND a.apply_source <> 'fxk_copy' 
) t2
ON t1.cust_no = t2.cust_no AND t2.rn = 1
LEFT JOIN
(
	SELECT  app_user_id
	       ,app
	       ,inner_app
	       ,utm_source
	       ,current_utm_source
	       ,register_time                                                                     AS created_time
	       ,CASE WHEN current_utm_source LIKE '%DY%' THEN '信息流' -- 抖音
	             WHEN current_utm_source LIKE '%XXL-BD%' THEN '信息流' -- 百度，主要变动在这里这里这里这里这里这里这里这里哈，百度算到信息流了
	             WHEN current_utm_source LIKE '%-DX-%' THEN '短信' -- 只包含短信
	             WHEN current_utm_source LIKE 'XYF01-API-DL%' THEN '其他付费渠道' -- 半流程
	             WHEN lower(current_utm_source) LIKE '%api%' THEN 'API' -- API注册
	             WHEN current_utm_source IN ('信用飞APP','xyf_app') THEN '其他渠道'
	             WHEN lower(current_utm_source) LIKE '%hw%' THEN '其他付费渠道' -- 其他付费渠道有一丢丢丢丢丢丢丢丢丢丢丢丢的变化哈
	             WHEN current_utm_source LIKE 'QD-CPA-XYF01%' THEN '其他付费渠道'
	             WHEN current_utm_source LIKE 'QD-CPP-APK%' THEN '其他付费渠道'
	             WHEN current_utm_source LIKE 'QD-CPS-XYF01%' THEN '其他付费渠道'
	             WHEN current_utm_source LIKE 'XYF01-QLC-%' THEN '其他付费渠道'
	             WHEN current_utm_source LIKE 'QD-CPP-XYF01-%' THEN '其他付费渠道'  ELSE '其他渠道' END AS register_channel -- 注册渠道
	       ,ROW_NUMBER() OVER(PARTITION BY mobile ORDER BY  register_time)                    AS rn
	FROM xyf_dim.dim_user_app_basic_info_df
	WHERE pt = max_pt('xyf_dim.dim_user_app_basic_info_df')
	AND app IN ('xyf01', 'fxk')
	AND channel <> 'fxk_copy' 
) t3
ON t1.user_no = t3.app_user_id AND t3.rn = 1
LEFT JOIN
(
	SELECT  order_number
	       ,user_no
	       ,cust_no
	       ,inner_app
	       ,loan_time
	       ,loan_amt
	       ,loan_flag
	       ,business_line
	       ,ROW_NUMBER () OVER (PARTITION BY cust_no ORDER BY  loan_time) AS all_channel_loan_rk --全站渠道放款次数 -- 放款排序
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = MAX_PT("xyf_dws.dws_inloan_user_order_df")
	AND app IN ('xyf01', 'fxk')
	AND inner_app NOT IN ('fxk_hexj', 'fxk_aj360', 'fxk_zyxj', 'fxk01_360zybx', 'fxk01_360zyaj')
	AND loan_time IS NOT NULL 
) t4
ON t1.cust_no = t4.cust_no AND t4.all_channel_loan_rk = 1
;


DROP TABLE IF EXISTS dws_inloan_loan_channel_stat_df_02;
CREATE TABLE dws_inloan_loan_channel_stat_df_02 AS
SELECT  DATE(pay_time)                                                                AS pay_dt
       ,CAST(SUM(CASE WHEN loan_type_flag = '首贷' THEN amt END) AS DOUBLE)             AS first_loan_amt -- 首贷放款
       ,CAST(SUM(CASE WHEN loan_type_flag = '加贷' THEN amt END) AS DOUBLE)             AS added_loan_amt -- 加贷放款
       ,CAST(SUM(CASE WHEN loan_type_flag = '复贷' THEN amt END) AS DOUBLE)             AS again_loan_amt -- 复贷放款
       ,COUNT(DISTINCT CASE WHEN loan_type_flag IN ('复贷','加贷') THEN order_number END) AS added_again_order_cnt -- 加复贷订单数
FROM
(
	SELECT  cust_no
	       ,app
	       ,inner_app
	       ,loan_flag        AS loan_type_flag
	       ,order_number
	       ,loan_amt         AS amt
	       ,first_order_time AS created_time
	       ,loan_time        AS pay_time
	       ,product_type
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = MAX_PT('xyf_dws.dws_inloan_user_order_df')
	AND app IN ('cxh')
	AND inner_app NOT IN ('fxk_hexj', 'fxk_aj360', 'fxk_zyxj', 'fxk01_360zybx', 'fxk01_360zyaj')
	AND DATE(loan_time) >= '2023-01-01' 
) t
GROUP BY  DATE(pay_time)
;


-- 每月不同渠道目标计算
DROP TABLE IF EXISTS dws_inloan_loan_channel_stat_df_03;
CREATE TABLE dws_inloan_loan_channel_stat_df_03 AS
SELECT  t1.day_id_iso
       ,substr(t1.day_id_iso,1,7)                                                                                               AS mth
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '首贷API' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_first_API_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '首贷APP' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_first_APP_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '信息流' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)        AS day_target_first_XXL_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '短信' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_first_DX_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '其他-付费' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_first_OTHER_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '其他' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_first_OTHER_p_free
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '复贷' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_added_p
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE '个人分期整体' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)     AS day_target_total_p
       ,SUM(CASE WHEN t2.product = '下探' AND t2.loan_type LIKE '复贷A24' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_A24
       ,SUM(CASE WHEN t2.product = '现金' AND t2.loan_type LIKE '复贷' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_added_c
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '首贷API' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_first_API
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '首贷APP' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)      AS day_target_first_APP
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '信息流' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)        AS day_target_first_XXL
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '短信' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_first_DX
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '其他' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_first_OTHER
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '复贷' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_added
       ,SUM(CASE WHEN t2.product = '整体' AND t2.loan_type LIKE '整体' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days)         AS day_target_total
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE 'APItoAPP首贷' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days) AS day_target_first_APItoAPP
       ,SUM(CASE WHEN t2.product = '个人' AND t2.loan_type LIKE 'APItoAPP复贷' THEN t2.loan_amt2 ELSE 0 END)/MAX(t1.mth_total_days) AS day_target_added_APItoAPP
FROM
(
	SELECT  day_id_iso
	       ,substr(day_monthend_iso,9,2) AS mth_total_days
	FROM xyf_dim.dim_pub_date
	WHERE day_id_iso >= '2023-01-01'
	AND day_id_iso <= concat(YEAR(CURRENT_DATE ()), '-12-31') --小于当年的最后一天
	--AND day_id_iso <= '2025-06-30' --20241204 shenxinru 要求 展示到未来25年6月，后面要保持修改这个时间范围
 
)t1
LEFT JOIN
(
	SELECT  loan_month
	       ,product
	       ,loan_type
	       ,loan_amt/100 AS loan_amt2
	FROM xyf_bi_dev.loan_target_2023_2024kpi_v2
) t2
ON substr(t1.day_id_iso, 1, 7) = t2.loan_month
WHERE t2.loan_month IS NOT NULL
GROUP BY  t1.day_id_iso
         ,substr(t1.day_id_iso,1,7)
;



--月度放款人数（临时表需要保留，下游在使用！！！） 
DROP TABLE IF EXISTS dws_inloan_loan_channel_stat_df_04;
CREATE TABLE dws_inloan_loan_channel_stat_df_04 AS

SELECT  loan_month
       ,COUNT(distinct CASE WHEN pay_channel = 'API' AND loan_times_flag = '首贷' THEN cust_no end)                                  AS act_first_api_p_mthly_id -- 个人API首贷
-- 少量API上的复加贷数据 
       ,COUNT(distinct CASE WHEN pay_channel = 'API' AND loan_times_flag IN ('加贷','复贷') THEN cust_no end)                          AS act_added_api_p_mthly_id -- 个人API复贷 --717新增 
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type IN ("APP","API") THEN cust_no end) AS act_first_app_p_mthly_id -- 个人APP首贷 
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('短信') THEN cust_no end) AS act_first_DX_p_mthly_id -- 个人APP首贷_短信 
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('信息流') THEN cust_no end) AS act_first_XXL_p_mthly_id -- 个人APP首贷_信息流 
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel NOT IN ('信息流','短信') THEN cust_no end) AS act_first_OTHER_p_mthly_id -- 个人APP首贷_其他 
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "API" THEN cust_no end)          AS act_first_APItoAPP_p_mthly_id -- API授信后拉回APP放第一笔 
       ,COUNT(distinct CASE WHEN --asset_type_flag <> 'A24' AND 
					( (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API')
					-- APP上3次及以上复贷 
					or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk >= 3)
					-- APP首贷后APP复贷 
					or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP') 
					or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh') ) THEN cust_no end) AS act_added_p_mthly_id -- 个人APP复贷(剔除A24)
		-- , count(distinct CASE WHEN asset_type_flag = 'A24' AND (
		-- (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API')
		-- -- APP上3次及以上复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk >= 3)
		-- -- APP首贷后APP复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP')
		-- or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh')
		-- ) THEN cust_no end) 
       ,0                                                                                                                          AS act_A24_p_mthly_id
       ,COUNT(distinct CASE WHEN pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API' THEN cust_no end) AS act_added_APItoAPP_p_mthly_id -- 个人APP首贷API首贷 
FROM dws_inloan_loan_channel_stat_df_01
WHERE loan_date >= '2023-01-01'
GROUP BY  loan_month
;


INSERT OVERWRITE TABLE dws_inloan_loan_channel_stat_df PARTITION (pt = '${bizdate}')
SELECT  t0.day_id_iso                                                                                      AS loan_date
-- 实际每日 放款金额 
       ,t1.act_first_api_p
       ,t1.act_added_api_p --717新增 
       ,t1.act_first_app_p
       ,t1.act_first_DX_p
       ,t1.act_first_XXL_p
       ,t1.act_first_OTHER_p
       ,t1.act_first_APItoAPP_p
       ,t1.act_added_p
       ,t1.act_A24_p
       ,t1.act_added_APItoAPP_p
       ,t2.act_added_c
-- 实际每日 放款订单数 
       ,t1.act_first_api_p_ord
       ,t1.act_added_api_p_ord --717新增 
       ,t1.act_first_app_p_ord
       ,t1.act_first_DX_p_ord
       ,t1.act_first_XXL_p_ord
       ,t1.act_first_OTHER_p_ord
       ,t1.act_first_APItoAPP_p_ord
       ,t1.act_added_p_ord
       ,t1.act_A24_p_ord
       ,t1.act_added_APItoAPP_p_ord
       ,t2.act_added_c_ord
-- 实际累计放款 
       ,SUM(t1.act_first_api_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY  t1.loan_date)         AS cum_act_first_api_p -- 个人API首贷 
       ,SUM(t1.act_added_api_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)          AS cum_act_added_api_p -- 个人API复贷 --717新增 
       ,SUM(t1.act_first_app_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)          AS cum_act_first_app_p -- 个人APP首贷 
       ,SUM(t1.act_first_DX_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)           AS cum_act_first_DX_p -- 个人APP首贷_短信 
       ,SUM(t1.act_first_XXL_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)          AS cum_act_first_XXL_p -- 个人APP首贷_信息流 
       ,SUM(t1.act_first_OTHER_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)        AS cum_act_first_OTHER_p -- 个人APP首贷_其他 
       ,SUM(t1.act_first_APItoAPP_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)     AS cum_act_first_APItoAPP_p -- API授信后拉回APP放第一笔 
       ,SUM(t1.act_added_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)              AS cum_act_added_p -- 个人APP复贷(剔除A24) 
       ,SUM(t1.act_A24_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)                AS cum_act_A24_p
       ,SUM(t1.act_added_APItoAPP_p) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)     AS cum_act_added_APItoAPP_p -- 个人APP首贷API首贷 
       ,SUM(t2.act_added_c) over(PARTITION BY substr(t2.pay_dt,1,7) ORDER BY t2.pay_dt)                    AS cum_act_added_c -- 现金复贷
-- 实际累计放款订单数 
       ,SUM(t1.act_first_api_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)      AS cum_act_first_api_p_ord -- 个人API首贷 
       ,SUM(t1.act_added_api_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)      AS cum_act_added_api_p_ord -- 个人API复贷 --717新增 
       ,SUM(t1.act_first_app_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)      AS cum_act_first_app_p_ord -- 个人APP首贷 
       ,SUM(t1.act_first_DX_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)       AS cum_act_first_DX_p_ord -- 个人APP首贷_短信 
       ,SUM(t1.act_first_XXL_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)      AS cum_act_first_XXL_p_ord -- 个人APP首贷_信息流 
       ,SUM(t1.act_first_OTHER_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)    AS cum_act_first_OTHER_p_ord -- 个人APP首贷_其他 
       ,SUM(t1.act_first_APItoAPP_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date) AS cum_act_first_APItoAPP_p_ord -- API授信后拉回APP放第一笔 
       ,SUM(t1.act_added_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)          AS cum_act_added_p_ord -- 个人APP复贷(剔除A24) 
       ,SUM(t1.act_A24_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date)            AS cum_act_A24_p_ord
       ,SUM(t1.act_added_APItoAPP_p_ord) over(PARTITION BY substr(t1.loan_date,1,7) ORDER BY t1.loan_date) AS cum_act_added_APItoAPP_p_ord -- 个人APP首贷API首贷 
       ,SUM(t2.act_added_c_ord) over(PARTITION BY substr(t2.pay_dt,1,7) ORDER BY t2.pay_dt)                AS cum_act_added_c_ord -- 现金复贷
-----MTD目标 累计---- 
       ,SUM(t0.day_target_first_API_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                    AS cum_day_target_first_API_p
       ,SUM(t0.day_target_first_APP_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                    AS cum_day_target_first_APP_p
       ,SUM(t0.day_target_first_XXL_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                    AS cum_day_target_first_XXL_p
       ,SUM(t0.day_target_first_DX_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                     AS cum_day_target_first_DX_p
       ,SUM(t0.day_target_first_OTHER_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                  AS cum_day_target_first_OTHER_p
       ,SUM(t0.day_target_first_OTHER_p_free) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)             AS cum_day_target_first_OTHER_p_free
       ,SUM(t0.day_target_added_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                        AS cum_day_target_added_p
       ,SUM(t0.day_target_total_p) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                        AS cum_day_target_total_p
       ,SUM(t0.day_target_A24) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                            AS cum_day_target_A24
       ,SUM(t0.day_target_added_c) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                        AS cum_day_target_added_c
       ,SUM(t0.day_target_first_API) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                      AS cum_day_target_first_API
       ,SUM(t0.day_target_first_APP) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                      AS cum_day_target_first_APP
       ,SUM(t0.day_target_first_XXL) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                      AS cum_day_target_first_XXL
       ,SUM(t0.day_target_first_DX) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                       AS cum_day_target_first_DX
       ,SUM(t0.day_target_first_OTHER) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                    AS cum_day_target_first_OTHER
       ,SUM(t0.day_target_added) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                          AS cum_day_target_added
       ,SUM(t0.day_target_total) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                          AS cum_day_target_total
       ,SUM(t0.day_target_first_APItoAPP) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                 AS cum_day_target_first_APItoAPP
       ,SUM(t0.day_target_added_APItoAPP) over(PARTITION BY t0.mth ORDER BY t0.day_id_iso)                 AS cum_day_target_added_APItoAPP
FROM dws_inloan_loan_channel_stat_df_03 t0
LEFT JOIN
(
	SELECT  loan_date 
	-- -------------------------- 放款金额部分 --------------------------------- 
	       ,SUM(case WHEN pay_channel = 'API' AND loan_times_flag = '首贷' THEN loan_amt / 100000000 else 0 end)                                          AS act_first_api_p -- 个人API首贷
	-- 少量API上的复加贷数据 
	       ,SUM(case WHEN pay_channel = 'API' AND loan_times_flag IN ('加贷','复贷') THEN loan_amt / 100000000 else 0 end)                                  AS act_added_api_p -- 个人API复贷 --717新增 
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type IN ("APP","API") THEN loan_amt / 100000000 else 0 end)         AS act_first_app_p -- 个人APP首贷 
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('短信') THEN loan_amt / 100000000 else 0 end) AS act_first_DX_p -- 个人APP首贷_短信 
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('信息流') THEN loan_amt / 100000000 else 0 end) AS act_first_XXL_p -- 个人APP首贷_信息流 
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel NOT IN ('信息流','短信') THEN loan_amt / 100000000 else 0 end) AS act_first_OTHER_p -- 个人APP首贷_其他 
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "API" THEN loan_amt / 100000000 else 0 end)                  AS act_first_APItoAPP_p -- API授信后拉回APP放第一笔 
	       ,SUM(case WHEN --asset_type_flag <> 'A24' AND 
				( (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API') 
				-- APP上3次及以上复贷 
				or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk >= 3) 
				-- APP首贷后APP复贷 
				or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP') 
				or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh') --722 
				) THEN loan_amt / 100000000 else 0 end) AS act_added_p -- 个人APP复贷(剔除A24)
		-- , sum(case WHEN asset_type_flag = 'A24' AND (
		-- (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API')
		-- -- APP上3次及以上复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk >= 3)
		-- -- APP首贷后APP复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP')
		-- or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh')--722
		-- ) THEN loan_amt / 100000000 else 0 end) 
	       ,0                                                                                                                                           AS act_A24_p
	       ,SUM(case WHEN pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API' THEN loan_amt / 100000000 else 0 end) AS act_added_APItoAPP_p -- 个人APP首贷API首贷
	-- -------------------------- 放款订单数 --------------------------------- 
	       ,COUNT(case WHEN pay_channel = 'API' AND loan_times_flag = '首贷' THEN order_number end)                                                       AS act_first_api_p_ord -- 个人API首贷
	-- 少量API上的复加贷数据 
	       ,COUNT(case WHEN pay_channel = 'API' AND loan_times_flag IN ('加贷','复贷') THEN order_number end)                                               AS act_added_api_p_ord -- 个人API复贷 --717新增 
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type IN ("APP","API") THEN order_number end)                      AS act_first_app_p_ord -- 个人APP首贷 
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('短信') THEN order_number end)  AS act_first_DX_p_ord -- 个人APP首贷_短信 
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel IN ('信息流') THEN order_number end) AS act_first_XXL_p_ord -- 个人APP首贷_信息流 
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "APP" AND credit_channel NOT IN ('信息流','短信') THEN order_number end) AS act_first_OTHER_p_ord -- 个人APP首贷_其他 
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag = '首贷' AND credit_type = "API" THEN order_number end)                               AS act_first_APItoAPP_p_ord -- API授信后拉回APP放第一笔 
	       ,COUNT(case WHEN --asset_type_flag <> 'A24' AND 
					( (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API') -- APP上3次及以上复贷 
					or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk >= 3) -- APP首贷后APP复贷 
					or (pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP') 
					or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh') --722 
					) THEN order_number end) AS act_added_p_ord -- 个人APP复贷(剔除A24)
		-- , count(case WHEN asset_type_flag = 'A24' AND (
		-- (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API')
		-- -- APP上3次及以上复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk >= 3)
		-- -- APP首贷后APP复贷
		-- or (pay_channel = 'APP' AND loan_times_flag IN ('加贷', '复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'APP')
		-- or (pay_channel = 'APP' AND credit_type = 'xyf01_cxh')--722
		-- ) THEN order_number end) 
	       ,0                                                                                                                                           AS act_A24_p_ord
	       ,COUNT(case WHEN pay_channel = 'APP' AND loan_times_flag IN ('加贷','复贷') AND all_channel_loan_rk = 2 AND first_loan_channel = 'API' THEN order_number end) AS act_added_APItoAPP_p_ord -- 个人APP首贷API首贷 
	FROM dws_inloan_loan_channel_stat_df_01
	WHERE loan_date >= '2023-01-01'
	GROUP BY  loan_date
) t1
ON t1.loan_date = t0.day_id_iso
-- 现金实际放款(cxh) 
LEFT JOIN
(
	SELECT  pay_dt
	       ,added_again_order_cnt                                                AS act_added_c_ord
	       ,(COALESCE(added_loan_amt,0) + COALESCE(again_loan_amt,0)) /100000000 AS act_added_c
	FROM dws_inloan_loan_channel_stat_df_02
) t2
ON t1.loan_date = t2.pay_dt
;


