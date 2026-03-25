--月度贷余，包含最新一天贷余
CREATE TABLE IF NOT EXISTS ads_inloan_loan_balance_mthly_df
(
    data_date         STRING COMMENT '放款日期'
    ,loan_type        STRING COMMENT '资产类型'
    ,flag             STRING COMMENT '数据类型'
    ,fund_balance_amt DECIMAL(38,18) COMMENT '代偿余额(亿)_包含代偿'
    ,balance_30_amt   DECIMAL(38,18) COMMENT 't30-余额(亿)'
    ,balance_90_amt   DECIMAL(38,18) COMMENT 't90-余额(亿)'
    ,balance_180_amt  DECIMAL(38,18) COMMENT 't180-余额(亿)'
)
STORED AS ALIORC
TBLPROPERTIES ('COMMENT' = 'API首贷客户到APP登录长期表现数据')
;


-- 一次性补全老系统的历史数据
-- create table xyf_ads.ads_inloan_loan_balance_mthly_df_01 as 
-- select 
--     substr(TO_DATE(t1.pt,'yyyyMMdd'),1,10) as data_date
--     ,'mthly' as flag
--     ,case when app <> inner_app then 'API'
--          when loan_flag = '首贷' then 'APP首贷'
--          else 'APP复贷' end as loan_type
--     ,SUM(case when overdue_days <=30 then loan_balance end)/100000000 AS loan_amt_30
--     ,SUM(case when overdue_days <=90 then loan_balance end)/100000000 AS loan_amt_90
--     ,SUM(case when overdue_days <=180 then loan_balance end)/100000000 AS loan_amt_180
-- from (
-- SELECT  order_number,pt
--         ,SUM(initial_principal - paid_principal)/100 AS loan_balance
--         ,MAX(CASE WHEN pay_status = 'unpaid' THEN overdue_days ELSE 0 END) overdue_days
-- FROM    xyf_dwd.dwd_risk_credit_repay_plan_df_drop
-- WHERE   pt in('20240131','20240229','20240331','20240430','20240531','20240630','20240731','20240831')
-- GROUP BY order_number,pt
-- ) t1 
-- inner join xyf_dws.dws_inloan_user_order_df t2 
-- on t1.order_number = t2.order_number 
-- and t2. pt =MAX_PT('xyf_dws.dws_inloan_user_order_df')
-- GROUP BY substr(TO_DATE(t1.pt,'yyyyMMdd'),1,10),
-- case when app <> inner_app then 'API'
--      when loan_flag = '首贷' then 'APP首贷'
--      else 'APP复贷' end 
-- ;



INSERT OVERWRITE TABLE ads_inloan_loan_balance_mthly_df
SELECT  a.data_date --统计日期/放款日期
        ,a.loan_type
        ,a.flag
        ,b.对资贷余 AS fund_balance_amt
        ,a.`余额_30` AS balance_30_amt
        ,a.`余额_90` AS balance_90_amt
        ,a.`余额_180` AS balance_180_amt
FROM    (
            SELECT  day_id_iso AS data_date
                    ,'mthly' AS flag
                    ,CASE WHEN pt < '20250630' THEN (CASE WHEN app <> inner_app THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END )
                          WHEN pt >= '20250630' THEN (CASE WHEN business_line = 'API' THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END ) 
                          END AS loan_type
                    ,SUM(CASE WHEN overdue_days <=30 THEN loan_balance END)/100000000 AS `余额_30`
                    ,SUM(CASE WHEN overdue_days <=90 THEN loan_balance END)/100000000 AS `余额_90`
                    ,SUM(CASE WHEN overdue_days <=180 THEN loan_balance END)/100000000 AS `余额_180`
            FROM    xyf_dws.dws_repay_user_order_df a 
            INNER JOIN xyf_dim.dim_pub_date b 
            ON a.pt = b.day_id 
            AND b.is_lastday = 1 --月末
            AND b.day_id_iso >= '2023-01-31' 
            AND b.day_id_iso <= DATE_SUB(DATETRUNC(CURRENT_DATE(),'MM'),1) --上月末最后一天
            -- where   pt in ('20230131','20230228','20230331','20230430','20230531','20230630','20230731','20230831','20230930','20231031','20231130','20231231','20240131','20240229','20240331','20240430','20240531','20240630','20240731','20240831','20240930','20241031','20241130','20241231','20250131')
            GROUP BY day_id_iso
                     ,CASE WHEN pt < '20250630' THEN (CASE WHEN app <> inner_app THEN 'API'
                                                        WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                        ELSE 'APP复贷' END )
                        WHEN pt >= '20250630' THEN (CASE WHEN business_line = 'API' THEN 'API'
                                                        WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                        ELSE 'APP复贷' END ) 
                        END
            UNION ALL 
            SELECT data_date,flag,loan_type,loan_amt_30,loan_amt_90,loan_amt_180 FROM xyf_ads.ads_inloan_loan_balance_mthly_df_01
            UNION ALL
            SELECT  substr(TO_DATE(pt,'yyyyMMdd'),1,10) AS data_date
                    ,'daily' AS flag
                    ,CASE WHEN pt < '20250623' THEN (CASE WHEN app <> inner_app THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END )
                          WHEN pt >= '20250623' THEN (CASE WHEN business_line = 'API' THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END ) 
                          END AS loan_type
                    ,SUM(CASE WHEN overdue_days <=30 THEN loan_balance END)/100000000 AS `余额_30`
                    ,SUM(CASE WHEN overdue_days <=90 THEN loan_balance END)/100000000 AS `余额_90`
                    ,SUM(CASE WHEN overdue_days <=180 THEN loan_balance END)/100000000 AS `余额_180`
            FROM    xyf_dws.dws_repay_user_order_df
            WHERE   (
                        pt >= CASE WHEN DAY(CURRENT_DATE()) = 1 THEN REPLACE(CONCAT(SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7),'01'),'-','')
                              ELSE REPLACE(CONCAT(SUBSTR(CURRENT_DATE(),1,7),'01'),'-','') END
                        AND pt <= REPLACE(DATE_ADD(CURRENT_DATE(),-1),'-','')
                    )
            GROUP BY substr(TO_DATE(pt,'yyyyMMdd'),1,10)
                     ,CASE WHEN pt < '20250623' THEN (CASE WHEN app <> inner_app THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END )
                          WHEN pt >= '20250623' THEN (CASE WHEN business_line = 'API' THEN 'API'
                                                          WHEN loan_flag = '首贷' THEN 'APP首贷'
                                                          ELSE 'APP复贷' END ) 
                          END 

            -- 添加导流业务数据 20250418
            UNION ALL
            SELECT  day_id_iso AS data_date
                    ,'mthly' AS flag
                    ,'导流' AS loan_type
                    ,SUM(CASE WHEN NVL(cur_due_days,0) <= 30 THEN principal - paid_principal END)/100000000 AS `余额_30` --loan_amt_30
                    ,SUM(CASE WHEN NVL(cur_due_days,0) <= 90 THEN principal - paid_principal END)/100000000 AS `余额_90` --loan_amt_90
                    ,SUM(CASE WHEN NVL(cur_due_days,0) <= 180 THEN principal - paid_principal END)/100000000 AS `余额_180` -- loan_amt_180
            FROM    (
                        SELECT  b.day_id_iso
                                ,hand_in_order_no
                                ,SUM(principal / 100) AS principal -- 本金
                                ,SUM(paid_principal / 100) AS paid_principal -- 已还本金
                                ,MAX(CASE WHEN STATUS = 'unpaid' THEN overdue_days END) cur_due_days
                        FROM    xyf_dwd.dwd_repay_op_user_bill_df a 
                        INNER JOIN xyf_dim.dim_pub_date b 
                        ON a.pt = b.day_id 
                        AND b.is_lastday = 1 --月末
                        AND b.day_id_iso >= '2024-01-01' 
                        AND b.day_id_iso <= DATE_SUB(DATETRUNC(CURRENT_DATE(),'MM'),1) --上月末最后一天
                        GROUP BY hand_in_order_no
                                 ,b.day_id_iso
                    ) x
            GROUP BY day_id_iso
            UNION ALL  --20250603 由于历史分区数据误删，从以往邮件中找出已经计算出来的结果固定在下面
            SELECT '2025-04-30' AS data_date,'mthly' AS flag,'导流' AS loan_type,3.91 AS `余额_30`,4.05 AS `余额_90`,4.21 AS `余额_180`
            UNION ALL 
            SELECT '2025-03-31' AS data_date,'mthly' AS flag,'导流' AS loan_type,3.95 AS `余额_30`,4.07 AS `余额_90`,4.22 AS `余额_180`
        ) a
LEFT JOIN   (
                SELECT  day_id_iso
                        ,loan_group
                        ,'mthly' AS flag
                        ,(放款金额 - 还款金额_代偿前 - 代偿金额) / 100000000 AS 对资贷余
                FROM    (
                            SELECT  b.day_id_iso
                                    ,'' AS loan_group
                                    ,SUM(pay_amt) 放款金额
                                    ,SUM(repay_amt) 还款金额_代偿前
                                    ,SUM(comp_amt) 代偿金额
                                    ,SUM(after_comp_amt) 还款金额_代偿后
                            FROM    (
                                        SELECT  DAYS AS dayid
                                                ,loan_type
                                                ,risk_price
                                                ,asset_type
                                                ,pay_amt
                                                ,repay_amt
                                                ,comp_amt
                                                ,after_comp_amt
                                                ,1 biz_type
                                        FROM    xyf_ads.ads_fin_onloan_fee_df
                                        WHERE   pt = MAX_PT('xyf_ads.ads_fin_onloan_fee_df')
                                    ) a
                            INNER JOIN  (
                                            SELECT  day_id_iso
                                                    ,1 biz_type
                                            FROM    xyf_dim.dim_pub_date
                                            -- where   day_id in ('20230131','20230228','20230331','20230430','20230531','20230630','20230731','20230831','20230930','20231031','20231130','20231231','20240131','20240229','20240331','20240430','20240531','20240630','20240731','20240831','20240930','20241031','20241130','20241231','20250131')
                                            WHERE day_id_iso >='2023-01-31' 
                                              AND day_id_iso <= DATE_SUB(DATETRUNC(CURRENT_DATE(),'MM'),1) --上月末最后一天
                                              AND is_lastday = 1 --月末
                                        ) b
                            ON      a.biz_type = b.biz_type
                            AND     a.dayid <= b.day_id_iso
                            GROUP BY b.day_id_iso
                        ) 
                UNION ALL
                SELECT  day_id_iso
                        ,loan_group
                        ,'daily' AS flag
                        ,(放款金额 - 还款金额_代偿前 - 代偿金额) / 100000000 AS 对资贷余
                FROM    (
                            SELECT  b.day_id_iso
                                    ,'' AS loan_group
                                    ,SUM(pay_amt) 放款金额
                                    ,SUM(repay_amt) 还款金额_代偿前
                                    ,SUM(comp_amt) 代偿金额
                                    ,SUM(after_comp_amt) 还款金额_代偿后
                            FROM    (
                                        SELECT  DAYS AS dayid
                                                ,loan_type
                                                ,risk_price
                                                ,asset_type
                                                ,pay_amt
                                                ,repay_amt
                                                ,comp_amt
                                                ,after_comp_amt
                                                ,1 biz_type
                                        FROM    xyf_ads.ads_fin_onloan_fee_df
                                        WHERE   pt = MAX_PT('xyf_ads.ads_fin_onloan_fee_df')
                                    ) a
                            INNER JOIN  (
                                            SELECT  day_id_iso
                                                    ,1 biz_type
                                            FROM    xyf_dim.dim_pub_date
                                            WHERE   (
                                                     day_id >= CASE WHEN DAY(CURRENT_DATE()) = 1 THEN REPLACE(CONCAT(SUBSTR(DATE_ADD(CURRENT_DATE(),-5),1,7),'01'),'-','')
                                                                ELSE REPLACE(CONCAT(SUBSTR(CURRENT_DATE(),1,7),'01'),'-','') END
                                                     AND day_id <= REPLACE(DATE_ADD(CURRENT_DATE(),-1),'-','')
                                                    )
                                        ) b
                            ON      a.biz_type = b.biz_type
                            AND     a.dayid <= b.day_id_iso
                            GROUP BY b.day_id_iso
                        ) 
            ) b
ON      a.data_date = b.day_id_iso
AND     a.flag = b.flag
;
