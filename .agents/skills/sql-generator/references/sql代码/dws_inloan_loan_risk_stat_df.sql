CREATE TABLE IF NOT EXISTS dws_inloan_loan_risk_stat_df 
(
     order_date            STRING         COMMENT  '订单申请时间' 
    ,act_first_api_p_asset DECIMAL(38,18) COMMENT  '个人API首贷资产金额' 
    ,act_added_api_p_asset DECIMAL(38,18) COMMENT  '个人API复贷资产金额' 
    ,act_first_app_p_asset DECIMAL(38,18) COMMENT  '个人APP首贷(新)资产金额' 
    ,act_added_p_asset     DECIMAL(38,18) COMMENT  '个人APP复贷资产金额' 
) 
COMMENT '每日资产放款统计表' 
PARTITIONED BY (pt STRING COMMENT '分区日期') 
LIFECYCLE 30 
;

DROP TABLE IF EXISTS dws_inloan_loan_risk_stat_df_01;
CREATE TABLE dws_inloan_loan_risk_stat_df_01 AS
SELECT  t1.first_order_number
       ,t1.order_number
       ,t1.user_no
       ,t1.cust_no
       ,DATE(t1.loan_time)                                                                                    AS loan_date
       ,substr(t1.loan_time,1,7)                                                                              AS loan_month
       ,t1.loan_amt
       ,t1.loan_flag
       ,t1.inner_app
       ,t1.asset_type_flag
       ,CASE WHEN t1.business_line = 'API' THEN 'API'  ELSE 'APP' END                                         AS pay_channel
    -- , CASE WHEN t4.business_line = 'API' THEN 'API'  ELSE 'APP' END                                         AS first_loan_channel --首笔放款渠道 
       ,t2.credit_type
       ,t2.biz_type
       ,t3.register_channel
    -- , t1.all_channel_loan_rk 
       ,CASE WHEN t2.credit_type = 'API' THEN t2.biz_type  ELSE nvl(t2.first_channel,t3.register_channel) END AS credit_channel -- APP首贷渠道归因
    -- , CASE WHEN t1.all_channel_loan_rk = 1 AND t2.credit_type <> 'xyf01_cxh' THEN '首贷' --722新增
    --        WHEN t1.all_channel_loan_rk > 1 AND t1.loan_flag = '加贷' THEN '加贷'  ELSE '复贷' END                 AS loan_times_flag
       ,t1.risk_status
       ,t1.first_order_time
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
	       ,risk_status
	       ,first_order_time 
           -- , ROW_NUMBER () OVER (partition by cust_no ORDER BY  loan_time) AS all_channel_loan_rk --全站渠道放款次数 -- 放款排序 
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE pt = MAX_PT("xyf_dws.dws_inloan_user_order_df")
	AND app IN ('xyf01', 'fxk')
	AND inner_app NOT IN ('fxk_hexj', 'fxk_aj360', 'fxk_zyxj', 'fxk01_360zybx', 'fxk01_360zyaj')
	AND DATE(first_order_time) >= '2025-01-01' 
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
	       ,CASE WHEN lower(inner_app) = 'xyf01_cxh' THEN 'xyf01_cxh'  ELSE NVL(b.zero_channel,IF(lower(inner_app) IN ('xyf01','fxk'),'APP','API')) END AS credit_type
	       ,b.first_channel
	       ,ROW_NUMBER() OVER(PARTITION BY a.cust_no ORDER BY  a.created_time)                                                                          AS rn --取首次授信 
	FROM xyf_dwd.dwd_preloan_credit_apply_df a
	LEFT JOIN
	(
		SELECT  user_id
		       ,zero_channel
		       ,first_channel
		FROM
		(
			SELECT  user_id
			       ,attribution_source
			FROM xyf_dwd.dwd_xyf_flow_sys_flow_attribution_result_dup_df
			WHERE pt = MAX_PT('xyf_dwd.dwd_xyf_flow_sys_flow_attribution_result_dup_df') 
            QUALIFY ROW_NUMBER() OVER (PARTITION BY user_id ORDER BY created_time DESC ) = 1 
		) drv
		LEFT JOIN xyf_bi_dev.utm_source_channel_v1_cdf_v b
		ON drv.attribution_source = b.source AND b.pt = MAX_PT('xyf_bi_dev.utm_source_channel_v1_cdf_v')
	)b
	ON a.user_no = b.user_id
	WHERE a.pt = MAX_PT("xyf_dwd.dwd_preloan_credit_apply_df")
	AND a.app IN ('xyf01', 'fxk')
	AND a.STATUS = 2 --审批通过 
	AND a.apply_source <> 'fxk_copy' 
    QUALIFY ROW_NUMBER() OVER(PARTITION BY a.cust_no ORDER BY a.created_time) = 1 
) t2
ON t1.cust_no = t2.cust_no
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
	             WHEN current_utm_source LIKE 'QD-CPP-XYF01-%' THEN '其他付费渠道'  ELSE '其他渠道' 
            END AS register_channel -- 注册渠道 
	       ,ROW_NUMBER() OVER(PARTITION BY mobile ORDER BY  register_time)                    AS rn
	FROM xyf_dim.dim_user_app_basic_info_df
	WHERE pt = max_pt('xyf_dim.dim_user_app_basic_info_df')
	AND app IN ('xyf01', 'fxk')
	AND channel <> 'fxk_copy' 
) t3
ON t1.user_no = t3.app_user_id AND t3.rn = 1
-- left join 
-- (
--     select
--         order_number
--         ,user_no
--         ,cust_no
--         ,inner_app
--         ,loan_time
--         ,loan_amt
--         ,loan_flag
--         ,business_line
--         ,row_number () over (partition by cust_no order by loan_time) as all_channel_loan_rk --全站渠道放款次数 -- 放款排序
--     from xyf_dws.dws_inloan_user_order_df
--     where pt = MAX_PT("xyf_dws.dws_inloan_user_order_df")
--       and app in ('xyf01','fxk')
--       and inner_app not in ('fxk_hexj','fxk_aj360','fxk_zyxj','fxk01_360zybx','fxk01_360zyaj')
--       and loan_time is not null
-- ) t4 
-- on t1.cust_no = t4.cust_no and t4.all_channel_loan_rk = 1 
;

INSERT OVERWRITE TABLE dws_inloan_loan_risk_stat_df PARTITION(pt = '${bizdate}')
SELECT  DATE(first_order_time)                                                                                                        AS order_date
       ,SUM(CASE WHEN risk_status = 'pass' AND pay_channel = 'API' AND loan_flag = '首贷' THEN loan_amt / 100000000 ELSE 0 END)         AS act_first_api_p_asset -- 个人API首贷 
       ,SUM(CASE WHEN risk_status = 'pass' AND pay_channel = 'API' AND loan_flag IN ('加贷','复贷') THEN loan_amt / 100000000 ELSE 0 END) AS act_added_api_p_asset -- 个人API复贷 
       ,SUM(CASE WHEN risk_status = 'pass' AND pay_channel = 'APP' AND loan_flag = '首贷' AND credit_type IN ("APP","API") THEN loan_amt / 100000000 ELSE 0 END) AS act_first_app_p_asset -- 个人APP首贷(新) 
       ,SUM(CASE WHEN (risk_status = 'pass' AND pay_channel = 'APP' AND loan_flag IN ('加贷','复贷')) 
                        OR (risk_status = 'pass' AND pay_channel = 'APP' AND credit_type = 'xyf01_cxh') THEN loan_amt / 100000000 ELSE 0 END) AS act_added_p_asset -- 个人APP复贷 
FROM dws_inloan_loan_risk_stat_df_01
GROUP BY  DATE(first_order_time)
;

