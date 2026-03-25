CREATE TABLE IF NOT EXISTS ads_inloan_loan_pass_monitor_df
(
    dt                  STRING  COMMENT '统计口径'
    ,flg                STRING  COMMENT '组别'
    ,date_type          STRING  COMMENT '数据类型'
    ,loan_num           BIGINT  COMMENT '总人数'
    ,pass_num           BIGINT  COMMENT '通过人数'
    ,loan_amt_avg       DECIMAL(38,18) COMMENT '放款件均'
    ,is_refuse_recent30 STRING  COMMENT '最近30天是否被拒'
)
COMMENT '每日资产邮件'
;


DROP TABLE IF EXISTS ads_inloan_loan_pass_monitor_df_01;
CREATE TABLE ads_inloan_loan_pass_monitor_df_01 AS
SELECT  cust_no
       ,app
       ,inner_app
       ,loan_type_flag
       ,order_number
       ,amt
       ,created_time
       ,risk_status
       ,remit_status
       ,pay_time
       ,ROW_NUMBER() OVER(PARTITION BY cust_no,remit_status ORDER BY  created_time) AS loan_rn
FROM
(
	SELECT  cust_no
	       ,app
	       ,inner_app
	       ,loan_flag        AS loan_type_flag
	       ,order_number
	       ,loan_amt         AS amt
	       ,first_order_time AS created_time
	       ,IF(CASE WHEN risk_status IN ('pass','reject') THEN 1 ELSE 0 END = 1,
                    IF(CASE WHEN risk_status IN ('pass') THEN 1 ELSE 0 END = 1,'pass','reject') ,NULL) risk_status
	       ,IF( CASE WHEN loan_status IN ('success','failed') THEN 1 ELSE 0 END = 1,
                    IF(CASE WHEN loan_status IN ('success') THEN 1 ELSE 0 END = 1,'success','failed') ,NULL) remit_status
	       ,loan_time        AS pay_time
	FROM xyf_dws.dws_inloan_user_order_df
	WHERE app IN ('xyf01', 'fxk', 'cxh', 'fxk01') -- 个人 
	AND pt = MAX_PT('xyf_dws.dws_inloan_user_order_df')
	AND DATE(first_order_time) >= '2023-04-01'
	AND DATE(first_order_time) < CURRENT_DATE()
	AND failed_code <> '10001' --排除风险预筛失败的数据 
 
) a
;




-- drop table if exists ads_inloan_loan_pass_monitor_df_02;
-- create table ads_inloan_loan_pass_monitor_df_02 as
-- select   t1.cust_no
--         ,t1.inner_app
--         ,t1.app
--         ,t1.loan_type_flag
--         ,t1.order_number
--         ,t1.amt
--         ,t1.created_time
--         ,t1.risk_status
--         ,t1.remit_status
--         ,t1.pay_time
--         ,t1.loan_rn
--         ,t1.b_cust_no --b_id_card_number
--         ,t1.b_pay_time
--         ,t1.b_inner_app
--         ,t1.c_cust_no  --c_id_card_number
--         ,t1.c_created_time
--         ,cast(max(case when t2.cust_no is null then 0 else 1 end) as string) as is_refuse_recent30 --`最近30天是否被拒` 
-- from    (
--             select  a.*
--                     ,b.cust_no as b_cust_no --b_id_card_number
--                     ,b.pay_time as b_pay_time
--                     ,b.inner_app as b_inner_app
--                     ,c.cust_no as c_cust_no --c_id_card_number
--                     ,c.created_time as c_created_time
--             from  ads_inloan_loan_pass_monitor_df_01 a -- 加复贷每日放款     
--             left join ads_inloan_loan_pass_monitor_df_01 b  -- 首贷放款      
--             on      a.cust_no = b.cust_no
--             and     b.app in ('xyf01','fxk')
--             and     b.remit_status = 'success'
--             and     b.loan_rn = 1
--             and     b.inner_app not in ('xyf01','fxk')
--             left join ads_inloan_loan_pass_monitor_df_01 c -- 第二笔APP放款
--             on      a.cust_no = c.cust_no
--             and     c.app in ('xyf01','fxk')
--             and     c.remit_status = 'success'
--             and     c.loan_rn = 2
--             and     c.inner_app in ('xyf01','fxk')
--             where   date(a.created_time) >= '2023-01-01'
--             and     a.inner_app in ('xyf01','fxk')
--             and     a.loan_type_flag in ('加贷','复贷')
--         ) t1
-- left join  ads_inloan_loan_pass_monitor_df_01 t2
-- on      t1.cust_no = t2.cust_no
-- and     t2.app in ('xyf01','fxk')
-- and     t2.risk_status = 'reject'
-- and     date(t2.created_time) >= DATE_ADD(t1.created_time,-30)
-- and     date(t2.created_time) < date(t1.created_time)
-- group by 
--         t1.cust_no
--         ,t1.inner_app
--         ,t1.app
--         ,t1.loan_type_flag
--         ,t1.order_number
--         ,t1.amt
--         ,t1.created_time
--         ,t1.risk_status
--         ,t1.remit_status
--         ,t1.pay_time
--         ,t1.loan_rn
--         ,t1.b_cust_no --b_id_card_number
--         ,t1.b_pay_time
--         ,t1.b_inner_app
--         ,t1.c_cust_no  --c_id_card_number
--         ,t1.c_created_time
-- ;




DROP TABLE IF EXISTS ads_inloan_loan_pass_monitor_df_03;
CREATE TABLE ads_inloan_loan_pass_monitor_df_03 AS
SELECT  a.cust_no --id_card_number
        ,a.risk_status
        ,a.created_time
        ,a.remit_status
FROM    ads_inloan_loan_pass_monitor_df_01 a -- APP上的 首贷客户
INNER JOIN   -- 获取API上授信的客户
(
    SELECT  cust_no
            ,CASE   WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                    ELSE "api" END AS ap_flg
    FROM    xyf_dwd.dwd_preloan_credit_apply_df
    WHERE   pt = MAX_PT("xyf_dwd.dwd_preloan_credit_apply_df")
    AND     apply_source != 'fxk_copy'
    AND     app IN ('xyf01')
    AND     cust_no IS NOT NULL
    AND     STATUS = 2 --审批通过
    AND     lower(inner_app) NOT IN ('xyf01','fxk','cxh')---------待确定问题 app 和 inner app的问题
    GROUP BY cust_no
            ,CASE   WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                    ELSE "api" END
) b
ON      a.cust_no = b.cust_no
WHERE   a.inner_app IN ('xyf01','fxk')
AND     a.loan_type_flag IN ('首贷')
;


DROP TABLE IF EXISTS ads_inloan_loan_pass_monitor_df_04;
CREATE TABLE ads_inloan_loan_pass_monitor_df_04 AS
SELECT  a.dt
        ,a.flg
        ,'current_mth' date_type
        ,a.`总人数`
        ,a.`通过人数`
        ,a.`最近30天是否被拒`
FROM    (
            -- 风险通过率 老客
            SELECT  DATE(a.created_time) dt
                    ,'老客_APP放款(API首贷)' flg
                    ,COUNT(DISTINCT a.cust_no) `总人数`
                    ,COUNT(DISTINCT CASE WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                    ,CASE   WHEN b.cust_no IS NULL THEN '0'
                            ELSE '1'
                    END AS `最近30天是否被拒`
            FROM    xyf_dws.dws_inloan_loan_pass_stat_df a
            LEFT JOIN  
            (
                SELECT *
                FROM ads_inloan_loan_pass_monitor_df_01
                WHERE app IN ('xyf01', 'fxk')
                  AND risk_status = 'reject'
            ) b
            ON      a.cust_no = b.cust_no
            AND     DATE(b.created_time) >= DATE_ADD(a.created_time,-30)
            AND     DATE(b.created_time) < DATE(a.created_time)
            WHERE   SUBSTR(a.created_time,1,7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7)
                    ELSE SUBSTR(CURRENT_DATE(),1,7) END
            AND     DATE(a.created_time) < CURRENT_DATE() -- 近获取API拉回第二笔订单
            AND     a.created_time > b_pay_time
            AND     (a.created_time <= a.c_created_time OR a.c_created_time IS NULL)
            GROUP BY DATE(a.created_time)
                     ,CASE WHEN b.cust_no IS NULL THEN '0'
                           ELSE '1' END


            UNION ALL -- 风险通过率 老客
            SELECT  DATE(a.created_time) dt
                    ,'老客_APP放款' flg
                    ,COUNT(DISTINCT a.cust_no) `总人数`
                    ,COUNT(DISTINCT CASE    WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                    ,CASE   WHEN c.cust_no IS NULL THEN '0'
                            ELSE '1'
                    END AS `最近30天是否被拒`
            FROM    ads_inloan_loan_pass_monitor_df_01 a
            LEFT JOIN   (
                            SELECT  *
                            FROM    xyf_dws.dws_inloan_loan_pass_stat_df -- 近获取API拉回第二笔订单
                            WHERE   created_time > b_pay_time
                            AND     (created_time <= c_created_time OR c_created_time IS NULL)
                        ) b
            ON      a.cust_no = b.cust_no
            AND     a.created_time = b.created_time
            LEFT JOIN   (
                            SELECT  *
                            FROM    ads_inloan_loan_pass_monitor_df_01
                            WHERE   app IN ('xyf01','fxk')
                            AND     risk_status = 'reject'
                        ) c
            ON      a.cust_no = c.cust_no
            AND     DATE(c.created_time) >= DATE_ADD(a.created_time,-30)
            AND     DATE(c.created_time) < DATE(a.created_time)
            WHERE   SUBSTR(a.created_time,1,7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7)
                    ELSE SUBSTR(CURRENT_DATE(),1,7) END
            AND     DATE(a.created_time) < CURRENT_DATE() -- 剔除API第二笔订单
            AND     b.cust_no IS NULL -- 仅获取加复贷订单
            AND     a.loan_type_flag IN ('加贷','复贷') -- 仅获取APP上的订单
            AND     a.inner_app IN ('xyf01','fxk')
            GROUP BY DATE(a.created_time)
                     ,CASE   WHEN c.cust_no IS NULL THEN '0'
                             ELSE '1' END
    
            UNION ALL -- ods表授信通过率
            SELECT  row_crt_ts_date
                    ,CASE   WHEN ap_flg IN ('app') THEN '新客_APP首贷'
                            ELSE '新客_API首贷'
                    END AS flg
                    ,COUNT(DISTINCT cust_no) num
                    ,COUNT(DISTINCT CASE WHEN shouxin_cnt = 1 THEN cust_no END) pass_num
                    ,'0' AS `最近30天是否被拒`
            FROM    (
                        SELECT  cust_no
                                ,app
                                ,DATE(created_time) AS row_crt_ts_date
                                ,CASE WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                                      ELSE "api" END AS ap_flg
                                ,MAX(created_time) AS created_time
                                ,MAX(CASE WHEN STATUS = 2 THEN 1 ELSE 0 END) AS shouxin_cnt
                        FROM    xyf_dwd.dwd_preloan_credit_apply_df
                        WHERE   pt = MAX_PT('xyf_dwd.dwd_preloan_credit_apply_df')
                        AND     apply_source != 'fxk_copy'
                        AND     app IN ('xyf01')
                        AND     cust_no IS NOT NULL
                        AND     SUBSTR(created_time,1,7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7)
                                ELSE SUBSTR(CURRENT_DATE(),1,7) END
                        AND     DATE(created_time) < CURRENT_DATE()
                        GROUP BY cust_no
                                 ,app
                                 ,DATE(created_time)
                                 ,CASE WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                                       ELSE "api" END
                    ) 
            GROUP BY row_crt_ts_date
                     ,CASE   WHEN ap_flg IN ('app') THEN '新客_APP首贷'
                             ELSE '新客_API首贷' END
            
            UNION ALL
            SELECT  DATE(a.created_time) dt
                    ,'新客_APP首贷(API授信)' flg
                    ,COUNT(DISTINCT a.cust_no) `总人数`
                    ,COUNT(DISTINCT CASE  WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                    ,'0' AS `最近30天是否被拒`
            FROM    ads_inloan_loan_pass_monitor_df_03 a
            WHERE   SUBSTR(created_time,1,7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7)
                    ELSE SUBSTR(CURRENT_DATE(),1,7) END
            AND     DATE(created_time) < CURRENT_DATE()
            GROUP BY DATE(a.created_time)
        ) a
;

--历史月份数据
INSERT INTO TABLE ads_inloan_loan_pass_monitor_df_04
SELECT  a.dt
        ,a.flg
        ,'mthly_summary' date_type
        ,a.`总人数`
        ,a.`通过人数`
        ,`最近30天是否被拒`
FROM    (
            ------------------------------------------------------------------------
            -- 新逻辑，使用每日计算后平均的口径
            ------------------------------------------------------------------------
            SELECT  DATE(CONCAT(SUBSTR(dt,1,7),'-01')) dt
                    ,flg
                    ,SUM(`总人数`) `总人数`
                    ,SUM(`通过人数`) `通过人数`
                    ,`最近30天是否被拒`
            FROM    (
                        -- 风险通过率 老客
                        SELECT  a.created_date AS dt
                                ,'老客_APP放款(API首贷)' AS flg
                                ,COUNT(DISTINCT a.cust_no) `总人数`
                                ,COUNT(DISTINCT CASE WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                                ,CASE   WHEN b.cust_no IS NULL THEN '0'
                                        ELSE '1'
                                END AS `最近30天是否被拒`
                        FROM  (
                                SELECT cust_no
                                      ,created_time
                                      ,risk_status
                                      ,DATE(created_time) AS created_date
                                      ,DATE_ADD(created_time,-30) AS sub30_created_date
                                FROM xyf_dws.dws_inloan_loan_pass_stat_df
                                WHERE DATE(created_time) >= '2023-04-01' -- 近获取API拉回第二笔订单
                                  AND created_time > b_pay_time
                                  AND (created_time <= c_created_time OR c_created_time IS NULL)
                            ) a
                        LEFT JOIN   (
                                        SELECT  cust_no
                                                ,DATE(created_time) AS created_date
                                        FROM    ads_inloan_loan_pass_monitor_df_01
                                        WHERE   app IN ('xyf01','fxk')
                                        AND     risk_status = 'reject'
                                    ) b
                        ON  a.cust_no = b.cust_no
                        AND b.created_date >= a.sub30_created_date
                        AND b.created_date < a.created_date
                        GROUP BY a.created_date
                                 ,CASE   WHEN b.cust_no IS NULL THEN '0'
                                         ELSE '1' END
                        
                        UNION ALL -- 风险通过率 老客
                        SELECT  a.created_date AS dt
                                ,'老客_APP放款' AS flg
                                ,COUNT(DISTINCT a.cust_no) `总人数`
                                ,COUNT(DISTINCT CASE WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                                ,CASE   WHEN c.cust_no IS NULL THEN '0'
                                        ELSE '1'
                                END AS `最近30天是否被拒`
                        FROM    (
                                SELECT cust_no
                                      ,risk_status
                                      ,created_time
                                      ,DATE(created_time) AS created_date
                                      ,DATE_ADD(created_time,-30) AS sub30_created_date
                                FROM ads_inloan_loan_pass_monitor_df_01 
                                WHERE DATE(created_time) >= '2023-04-01' -- 剔除API第二笔订单
                                  AND loan_type_flag IN ('加贷','复贷') -- 仅获取APP上的订单
                                  AND inner_app IN ('xyf01','fxk') 
                                ) a
                        LEFT JOIN   (
                                        SELECT  cust_no,created_time
                                        FROM    xyf_dws.dws_inloan_loan_pass_stat_df -- 近获取API拉回第二笔订单
                                        WHERE   created_time > b_pay_time
                                          AND   (created_time <= c_created_time OR c_created_time IS NULL)
                                    ) b
                        ON      a.cust_no = b.cust_no
                        AND     a.created_time = b.created_time
                        LEFT JOIN   (
                                        SELECT  cust_no,DATE(created_time) AS created_date
                                        FROM    ads_inloan_loan_pass_monitor_df_01
                                        WHERE   app IN ('xyf01','fxk')
                                        AND     risk_status = 'reject'
                                    ) c
                        ON      a.cust_no = c.cust_no
                        AND     c.created_date >= a.sub30_created_date
                        AND     c.created_date < a.created_date
                        WHERE b.cust_no IS NULL -- 仅获取加复贷订单
                        GROUP BY a.created_date
                                 ,CASE   WHEN c.cust_no IS NULL THEN '0'
                                         ELSE '1' END

                        UNION ALL -- ods表授信通过率
                        SELECT  row_crt_ts_date
                                ,CASE   WHEN ap_flg IN ('app') THEN '新客_APP首贷'
                                        ELSE '新客_API首贷'
                                END AS flg
                                ,COUNT(DISTINCT cust_no) num
                                ,COUNT(DISTINCT CASE WHEN shouxin_cnt = 1 THEN cust_no END) pass_num
                                ,'0' AS `最近30天是否被拒`
                        FROM    (
                                    SELECT  cust_no
                                            ,app
                                            ,DATE(created_time) AS row_crt_ts_date
                                            ,CASE   WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                                                    ELSE "api"
                                            END AS ap_flg
                                            ,MAX(created_time) AS created_time
                                            ,MAX(CASE WHEN STATUS = 2 THEN 1 ELSE 0 END) AS shouxin_cnt
                                    FROM    xyf_dwd.dwd_preloan_credit_apply_df
                                    WHERE   pt = MAX_PT('xyf_dwd.dwd_preloan_credit_apply_df')
                                    AND     apply_source != 'fxk_copy'
                                    AND     app IN ('xyf01') -- and lower(inner_app) in ('xyf01')
                                    AND     cust_no IS NOT NULL
                                    AND     DATE(created_time) >= '2023-04-01'
                                    GROUP BY cust_no
                                            ,app
                                            ,DATE(created_time)
                                            ,CASE   WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app"
                                                    ELSE "api" END
                                ) 
                        GROUP BY row_crt_ts_date
                                ,CASE   WHEN ap_flg IN ('app') THEN '新客_APP首贷'
                                        ELSE '新客_API首贷' END

                        UNION ALL
                        SELECT  DATE(a.created_time) dt
                                ,'新客_APP首贷(API授信)' flg
                                ,COUNT(DISTINCT a.cust_no) `总人数`
                                ,COUNT(DISTINCT CASE WHEN a.risk_status = 'pass' THEN a.cust_no END) `通过人数`
                                ,'0' AS `最近30天是否被拒`
                        FROM    ads_inloan_loan_pass_monitor_df_03 a
                        WHERE   DATE(created_time) >= '2023-04-01'
                        GROUP BY DATE(a.created_time)
                    ) 
            GROUP BY DATE(CONCAT(SUBSTR(dt,1,7),'-01'))
                     ,flg
                     ,`最近30天是否被拒`
        ) a
;



INSERT OVERWRITE TABLE  ads_inloan_loan_pass_monitor_df
SELECT  a.dt
        ,a.flg
        ,a.date_type
        ,a.总人数 AS loan_num
        ,a.通过人数 AS pass_num
        ,b.放款件均 AS loan_amt_avg
        ,a.最近30天是否被拒 AS is_refuse_recent30
FROM    ads_inloan_loan_pass_monitor_df_04 a
LEFT JOIN 
(
        -- 放款件均
        SELECT  stat_type AS date_type
                ,loan_date AS pay_date
                ,CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' 
                      WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' 
                      WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' 
                      --when flag in ('个人API复贷') then '新客_API复贷'
                      WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)'
                      WHEN flag IN ('APP放款') THEN '老客_APP放款' ELSE flag END AS flag
                ,IF(SUM(day_loan_cnt) = 0,0,SUM(day_loan_amt) / SUM(day_loan_cnt) * 100000000) 放款件均
        FROM    xyf_ads.ads_inloan_loan_monitor_screen_df
        WHERE   SUBSTR(loan_date,1,7) = CASE WHEN DAY(CURRENT_DATE()) = 1 THEN SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7)
                ELSE SUBSTR(CURRENT_DATE(),1,7) END
        AND     DATE(loan_date) < CURRENT_DATE()
        AND     stat_type = 'current_mth'
        GROUP BY stat_type
                ,loan_date
                ,CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' 
                      WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' 
                      WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' 
                      --when flag in ('个人API复贷') then '新客_API复贷'
                      WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)'
                      WHEN flag IN ('APP放款') THEN '老客_APP放款' ELSE flag END 
        UNION ALL
        -- 放款件均
        SELECT  stat_type AS date_type
                ,CAST(DATE(CONCAT(SUBSTR(loan_date,1,7),'-01')) AS STRING) pay_date
                ,CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' 
                     WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' 
                     WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' 
                     --when flag in ('个人API复贷') then '新客_API复贷'
                     WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)'
                     WHEN flag IN ('APP放款') THEN '老客_APP放款' 
                ELSE flag END AS flag
                ,IF(SUM(day_loan_cnt) = 0,0,SUM(day_loan_amt) / SUM(day_loan_cnt) * 100000000) 放款件均
        FROM    xyf_ads.ads_inloan_loan_monitor_screen_df a
        INNER JOIN xyf_dim.dim_pub_date b ON a.loan_date = b.day_id_iso
               AND b.day_id_iso >='2023-04-01'
               AND b.day_id_iso <= concat(YEAR(CURRENT_DATE ()),'-12-31') --小于当年的最后一天(隐患当2025年初时，会把未来12个月的月末数据都放出来，此时需要控制FineBI看板或者代码时间范围缩小显示的时间范围)
               AND b.is_lastday = 1 --取月末最后一天
        WHERE stat_type = 'mthly_summary'
        GROUP BY stat_type
                ,DATE(CONCAT(SUBSTR(loan_date,1,7),'-01'))
                ,CASE WHEN flag IN ('个人APP首贷（新）') THEN '新客_APP首贷' 
                      WHEN flag IN ('APP首贷（API授信）') THEN '新客_APP首贷(API授信)' 
                      WHEN flag IN ('个人API首贷','个人API复贷') THEN '新客_API首贷' 
                      --when flag in ('个人API复贷') then '新客_API复贷'
                      WHEN flag IN ('APP首贷（API首贷）') THEN '老客_APP放款(API首贷)'
                      WHEN flag IN ('APP放款') THEN '老客_APP放款' ELSE flag END
)b
ON      a.dt = b.pay_date
AND     a.flg = b.flag
AND     a.date_type = b.date_type
;