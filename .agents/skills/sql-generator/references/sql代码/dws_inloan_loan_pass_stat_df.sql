DROP TABLE IF EXISTS dws_inloan_loan_pass_stat_df_01;
CREATE TABLE dws_inloan_loan_pass_stat_df_01 AS
SELECT 
    cust_no
    ,app
    ,inner_app
    ,loan_type_flag
    ,order_number
    ,amt
    ,created_time
    ,risk_status
    ,remit_status
    ,pay_time
    ,row_number() OVER(PARTITION BY cust_no,remit_status ORDER BY created_time) AS loan_rn
FROM 
(
    SELECT
        cust_no,
        app,
        inner_app,
        loan_flag AS loan_type_flag,
        order_number,
        loan_amt AS amt,
        first_order_time AS created_time, 
        IF(CASE WHEN risk_status IN ('pass','reject') THEN 1 ELSE 0 END = 1, 
            IF(CASE WHEN risk_status IN ('pass') THEN 1 ELSE 0 END = 1, 'pass', 'reject') , NULL) risk_status,
        IF( CASE WHEN loan_status IN ('success','failed') THEN 1 ELSE 0 END = 1, 
            IF(CASE WHEN loan_status IN ('success') THEN 1 ELSE 0 END = 1, 'success', 'failed') , NULL) remit_status,
        loan_time AS pay_time 
    FROM xyf_dws.dws_inloan_user_order_df
    WHERE app IN ('xyf01', 'fxk', 'cxh', 'fxk01') -- 个人
      AND pt = MAX_PT('xyf_dws.dws_inloan_user_order_df')
      AND DATE(first_order_time) >='2023-04-01'
      AND DATE(first_order_time) < CURRENT_DATE()
      AND failed_code <> '10001' --排除风险预筛失败的数据
) a 
;

-- SET odps.stage.joiner.num = 50;
DROP TABLE IF EXISTS dws_inloan_loan_pass_stat_df;
CREATE TABLE dws_inloan_loan_pass_stat_df AS
SELECT   t1.cust_no
        ,t1.inner_app
        ,t1.app
        ,t1.loan_type_flag
        ,t1.order_number
        ,t1.amt
        ,t1.created_time
        ,t1.risk_status
        ,t1.remit_status
        ,t1.pay_time
        ,t1.loan_rn
        ,t1.b_cust_no --b_id_card_number
        ,t1.b_pay_time
        ,t1.b_inner_app
        ,t1.c_cust_no  --c_id_card_number
        ,t1.c_created_time
        ,CAST(max(CASE WHEN t2.cust_no IS NULL THEN 0 ELSE 1 END) AS STRING) AS is_refuse_recent30 --`最近30天是否被拒` 
FROM    (
            SELECT  a.*
                    ,b.cust_no AS b_cust_no --b_id_card_number
                    ,b.pay_time AS b_pay_time
                    ,b.inner_app AS b_inner_app
                    ,c.cust_no AS c_cust_no --c_id_card_number
                    ,c.created_time AS c_created_time
                    ,DATE(a.created_time) AS created_date
                    ,DATE_ADD(a.created_time,-30) AS sub30_created_date
            FROM  dws_inloan_loan_pass_stat_df_01 a -- 加复贷每日放款     
            LEFT JOIN dws_inloan_loan_pass_stat_df_01 b  -- 首贷放款      
            ON      a.cust_no = b.cust_no
            AND     b.app IN ('xyf01','fxk')
            AND     b.remit_status = 'success'
            AND     b.loan_rn = 1
            AND     b.inner_app NOT IN ('xyf01','fxk')
            LEFT JOIN dws_inloan_loan_pass_stat_df_01 c -- 第二笔APP放款
            ON      a.cust_no = c.cust_no
            AND     c.app IN ('xyf01','fxk')
            AND     c.remit_status = 'success'
            AND     c.loan_rn = 2
            AND     c.inner_app IN ('xyf01','fxk')
            WHERE   DATE(a.created_time) >= '2023-04-01'
            AND     a.inner_app IN ('xyf01','fxk')
            AND     a.loan_type_flag IN ('加贷','复贷')
        ) t1
LEFT JOIN  
        (
            SELECT cust_no,DATE(created_time) AS created_date
            FROM dws_inloan_loan_pass_stat_df_01
            WHERE app IN ('xyf01','fxk')
              AND risk_status = 'reject'
        ) t2
ON      t1.cust_no = t2.cust_no
AND     t2.created_date >= t1.sub30_created_date
AND     t2.created_date < t1.created_date
GROUP BY 
        t1.cust_no
        ,t1.inner_app
        ,t1.app
        ,t1.loan_type_flag
        ,t1.order_number
        ,t1.amt
        ,t1.created_time
        ,t1.risk_status
        ,t1.remit_status
        ,t1.pay_time
        ,t1.loan_rn
        ,t1.b_cust_no --b_id_card_number
        ,t1.b_pay_time
        ,t1.b_inner_app
        ,t1.c_cust_no  --c_id_card_number
        ,t1.c_created_time
;