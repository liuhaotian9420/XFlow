--@exclude_input=xyf_dim.dim_pub_date
--@exclude_input=xyf_bi.aji_app_rank_order_forbi
--@exclude_input=xyf_fengkong.api_activation_base
--@exclude_input=xyf_bi.aji_app_rank_activation_forbi
--@exclude_input=xyf_bi.qudao_uid_syt
--@exclude_input=xyf_dwd.dwd_user_vip_order_df
--@exclude_input=xyf_dwd.dwd_inloan_leap_vip_order_hf
--@exclude_input=xyf_dwd.dwd_inloan_t_decision_result_detail_df
--odps sql 
--********************************************************************--
--author:邵逸婷
--create time:2025-10-23 19:38:13
--********************************************************************--
-- DROP TABLE IF EXISTS xyf_bi_dev.bi_app_zhuanhua_tixian_new_uid
-- ;

-- CREATE TABLE xyf_bi_dev.bi_app_zhuanhua_tixian_new_uid AS
WITH coupon AS 
(
    SELECT  app_user_id
            ,status
            ,created_time
            ,used_time
            ,sub_id
            ,discount_amount / 100 AS 优惠金额_提额金额
            ,actual_discount_amount / 100 AS 实际抵扣金额
            ,GET_JSON_OBJECT(order_number,'$.froze_order') first_order_number
            ,GET_JSON_OBJECT(order_number,'$.order') order_number
            ,activity_id
            ,coupon_type
    FROM    xyf_dwd.dwd_makt_coupon_user_cash_coupon_info_df
    WHERE   pt = '${bizdate}'
)
,zhubiao AS 
(
    SELECT  o.*
            ,shouxin.是否虚假给额
            ,人行评级
            ,授信额度
            ,shouxin_type
            ,shouxin.credit_success_time
            ,CASE   WHEN rand_num <= 9 THEN '大盘对照组'
                    WHEN rand_num <= 19 THEN '电销对照组'
                    WHEN rand_num <= 99 THEN '电销营销组'
            END AS 大盘分组
            ,shouxin.biz_flow_number AS shouxin_biz_flow_number
    FROM    (
                SELECT  order.*
                        ,CASE   WHEN rk_o.人行评级 IS NOT NULL THEN rk_o.人行评级
                                ELSE line_risk_level_output
                        END AS 动支评级
                FROM    (
                            SELECT  *
                                    ,CASE   WHEN date(first_order_time) <= '2024-01-05' THEN SUBSTR(conv2(sha2(CONCAT('xinkeyunying',user_no),256),16,10),-2)
                                            WHEN date(first_order_time) <= '2025-01-22' THEN RANDOMV3('xinkeyunying',user_no,2)
                                            ELSE RANDOMV3('xinkeyunying2025',user_no,2)
                                    END AS rand_num
                            FROM    xyf_dws.dws_inloan_user_order_df
                            WHERE   pt = '${bizdate}'
                            AND     loan_flag = '首贷'
                            AND     business_line IN ('APP','小程序端')
                            AND     date(first_order_time) >= '2024-01-01'
                            QUALIFY ROW_NUMBER() OVER (PARTITION BY cust_no,user_no,date(first_order_time) ORDER BY first_order_time DESC ) = 1
                        ) order
                LEFT JOIN xyf_bi.aji_app_rank_order_forbi rk_o
                ON      rk_o.ori_order_number = order.first_order_number
                LEFT JOIN   (
                                SELECT  biz_flow_number --业务流水号
                                        ,GET_JSON_OBJECT(context,'$.line_risk_level_output') AS line_risk_level_output
                                        ,0 AS is_credit --标明是不是授信的风险评级，0：不是
                                        ,ROW_NUMBER() OVER (PARTITION BY biz_flow_number ORDER BY decision_time DESC ) AS rank_no
                                FROM    xyf_dwd.dwd_inloan_t_decision_result_detail_df
                                WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_t_decision_result_detail_df')
                                AND     enginecode = 'jcl_20230807000004' --个人分期动支决策-API
                                AND     state = 'SUCCESS'
                                AND     decision_time >= '2024-11-18 00:00:00'
                                QUALIFY rank_no = 1
                            ) rk_a
                ON      rk_a.biz_flow_number = order.biz_flow_number
            ) o
    LEFT JOIN   (
                    SELECT  sx.*
                            ,CASE   WHEN xujia.biz_flow_number IS NOT NULL AND sx.inner_app IN ('xyf01','fxk') THEN '虚假给额'
                                    when sx.shouxin_type = 'API半流程' and sx.授信额度< 1000 THEN '虚假给额'
                                    ELSE '非虚假给额'
                            END AS 是否虚假给额
                            ,CASE   WHEN rk.人行评级 IS NOT NULL THEN rk.人行评级
                                    ELSE api_rk.personalloan_sd_line_amtlevel_rh_api
                            END AS 人行评级
                    FROM    (
                                SELECT  CASE    WHEN lower(inner_app) IN ('xyf01','fxk','cxh') AND client_code IN ('MPP001000068') THEN '微信小程序授信'
                                                WHEN lower(inner_app) IN ('xyf01','fxk','cxh') AND client_code IN ('MPP002000069') THEN '抖音小程序授信'
                                                WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "APP"
                                                WHEN lower(inner_app) IN ('xyf01_hrui02','xyf01_xcjr','xyf01_hrui01','xyf01_alyxy','xyf01_alygd','xyf01_alyfz','xyf01_zyxj01','xyf01_zyxjwld01','xyf01_zyxjzl01','xyf01_elm') THEN 'API半流程'
                                                ELSE 'API'
                                        END AS shouxin_type
                                        ,init_credit_line / 100 AS 授信额度
                                        ,*
                                FROM    xyf_dwd.dwd_preloan_credit_apply_df
                                WHERE   pt = '${bizdate}'
                                AND     status = 2
                                AND     app IN ('xyf01','fxk') --AND     NVL(app_activation_type,'') <> 'loan_recredit_activation'
                            ) sx
                    LEFT JOIN   (
                                    -- 虚假给额的授信成功用户口径，biz_flow_number关联授信表
                                    SELECT  biz_flow_number
                                    FROM    xyf_dwd.dwd_inloan_t_decision_result_detail_df
                                    WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_t_decision_result_detail_df')
                                    AND     enginecode = 'jcl_20240923000003'
                                    AND     GET_JSON_OBJECT(context,"$.app_new_risk_mark_output") RLIKE 'fake_activation'
                                    AND     decision_time >= '2024-10-15 00:00:00' --
                                    QUALIFY ROW_NUMBER() OVER (PARTITION BY biz_flow_number,date(decision_time) ORDER BY decision_time DESC ) = 1
                                ) xujia
                    ON      sx.biz_flow_number = xujia.biz_flow_number
                    LEFT JOIN xyf_bi.aji_app_rank_activation_forbi rk
                    ON      rk.授信_biz_flow_number = sx.biz_flow_number
                    LEFT JOIN xyf_fengkong.api_activation_base api_rk
                    ON      sx.biz_flow_number = api_rk.biz_flow_number
                ) shouxin
    ON      shouxin.cust_no = o.cust_no
    AND     shouxin.credit_expire_date > o.first_order_time
    AND     shouxin.credit_success_time <= o.first_order_time
    QUALIFY ROW_NUMBER() OVER (PARTITION BY o.user_no,date(o.first_order_time) ORDER BY shouxin.credit_success_time DESC ) = 1
)SELECT  date(d.first_order_time) AS dt
        ,d.loan_time 放款日
        ,zhou2.week_range AS 放款周
        ,d.user_no
        ,zhou.week_range AS wt
        ,SUBSTR(d.first_order_time,1,7) AS mt
        ,CASE   WHEN 0 <= 授信额度 AND 授信额度 < 1000 THEN 'A. [0k-1k)'
                WHEN 1000 <= 授信额度 AND 授信额度 < 3000 THEN 'B.[1k,3k)'
                WHEN 3000 <= 授信额度 AND 授信额度 <= 5000 THEN 'C.[3k,5k]'
                WHEN 5000 < 授信额度 AND 授信额度 <= 10000 THEN 'D. (5k,1w]'
                WHEN 10000 < 授信额度 AND 授信额度 <= 20000 THEN 'E. (1w,2w]'
                WHEN 20000 < 授信额度 AND 授信额度 <= 50000 THEN 'F. (2w,5w]'
                WHEN 50000 < 授信额度 AND 授信额度 <= 100000 THEN 'G. (5w-10w]'
                WHEN 100000 < 授信额度 THEN 'H.10w+'
                ELSE ''
        END AS 授信金额_level
        ,是否虚假给额
        ,qd.注册渠道大类 AS biz_type_bi
        ,qd.归因渠道大类 AS biz_type_bi_3
        ,qd.归因渠道大类_放款
        ,大盘分组
        ,CASE   WHEN 是否虚假给额 = '虚假给额' THEN '虚假给额'
                WHEN laohui.biz_flow_number IS NOT NULL OR tp3.biz_flow_number IS NOT NULL THEN '会员卡放开'
                WHEN d.freeze_type = 2 THEN '冻额放开'
                ELSE '正常审批'
        END AS 是否额外放开
        ,CASE   WHEN jc.age <= 24 THEN jc.age
                WHEN jc.age BETWEEN 55 AND 60 THEN jc.age
                WHEN jc.age BETWEEN 25 AND 54 THEN '25~54'
                WHEN jc.age >= 61 THEN '61岁以上'
        END AS 年龄
        ,shouxin_type AS 是否API授信
        ,CASE   WHEN 人行评级 > 0 AND 人行评级 < 2 THEN 人行评级
                WHEN 人行评级 >= 2 AND 人行评级 < 7 THEN floor(人行评级)
                WHEN 人行评级 >= 7 THEN '7+'
                ELSE '无评级'
        END AS 授信评级 ---动支评级
        ,CASE   WHEN 动支评级 > 0 AND 动支评级 < 2 THEN 动支评级
                WHEN 动支评级 >= 2 AND 动支评级 < 7 THEN floor(动支评级)
                WHEN 动支评级 >= 7 THEN '7+'
                ELSE '无评级'
        END AS 动支评级
        ,CASE   WHEN DATEDIFF(d.first_order_time,r.register_time) = 0 THEN '0d'
                WHEN 0 < DATEDIFF(d.first_order_time,r.register_time) AND DATEDIFF(d.first_order_time,r.register_time) <= 30 THEN '1-30d'
                WHEN DATEDIFF(d.first_order_time,r.register_time) > 30 AND DATEDIFF(d.first_order_time,r.register_time) <= 60 THEN '31d-60d'
                WHEN DATEDIFF(d.first_order_time,r.register_time) > 60 THEN '61d+'
                ELSE ''
        END AS 注册提现时间差
        ,CASE   WHEN DATEDIFF(d.first_order_time,d.credit_success_time) = 0 THEN '0d'
                WHEN DATEDIFF(d.first_order_time,d.credit_success_time) BETWEEN 1 AND 30 THEN '1-30d'
                WHEN DATEDIFF(d.first_order_time,d.credit_success_time) BETWEEN 31 AND 60 THEN '31d-60d'
                WHEN DATEDIFF(d.first_order_time,d.credit_success_time) > 60 THEN '61d+'
                ELSE ''
        END AS 授信提现时间差
        ,CASE   WHEN DATEDIFF(本次提现前最近一次提现时间,d.first_order_time) = 0 THEN '当天提现失败过'
                WHEN DATEDIFF(d.first_order_time,本次提现前最近一次提现时间) BETWEEN 0 AND 30 THEN '30天内提现失败过'
                WHEN DATEDIFF(d.first_order_time,本次提现前最近一次提现时间) >= 30 THEN '历史提现失败过'
                ELSE '未提现过'
        END AS 是否首次提现
        ,CASE   WHEN hx.bairong_als_code = '100002' THEN 'E.未查询'
                WHEN hx.bairong_als_code = '00' AND bairong_als_402 IS NULL THEN 'A. 0'
                WHEN bairong_als_402 = 0 THEN 'A. 0'
                WHEN hx.bairong_als_402 BETWEEN 1 AND 4 THEN 'B. 1~4'
                WHEN hx.bairong_als_402 > 5 THEN 'C. 4+'
                ELSE 'D.缺失'
        END AS 授信多头
        ,CASE   WHEN d.freeze_type = 0 THEN '未冻额'
                WHEN d.freeze_type = 1 THEN '被冻但当日未同意降额'
                ELSE '冻额后降额'
        END AS 冻额标识
        ,case when d.is_split_order = 1 then '拆单订单' else '普通订单' END AS 是否拆单
        ,MAX(d.period) 期限 ----期限
        ,d.asset_type_flag 定价
        ,d.business_line 是否小程序提现
        ,MAX(授信额度) 授信额度
        ,COUNT(DISTINCT d.user_no) 提现人
        ,MAX(d.order_amt) 提现金额
        ,COUNT(DISTINCT CASE    WHEN risk_status = 'pass' THEN d.user_no END) 风险通过人数
        ,MAX(CASE    WHEN risk_status = 'pass' THEN d.order_amt END) 风险通过金额
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) = 0 THEN d.user_no END) T0资方通过人
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 3 THEN d.user_no END) T3资方通过人
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 3 THEN d.user_no END) T7资方通过人
        ,COUNT(distinct CASE    WHEN loan_time IS NOT NULL THEN d.user_no END) 累积资方通过人
        ,COUNT(DISTINCT 
              CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time,'hh') BETWEEN 0 AND 2 THEN d.user_no END
        ) 资方通过人2h
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) = 0 THEN d.loan_amt END) 放款金额
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 3 THEN d.loan_amt END) t3放款金额
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 7 THEN d.loan_amt END) t7放款金额
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) >= 0 THEN d.loan_amt END) 累计放款金额
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) >= 0 THEN 初始应还总息费 END) APR口径应收息费 ----是否首次提现
        ,MAX(
            CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) >= 0 THEN CASE   WHEN d.asset_type_flag = 'I24' THEN 0.24 * d.loan_amt
                            WHEN d.asset_type_flag = 'I36' THEN 0.36 * d.loan_amt
                    END END
        ) 定价_金额
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) >= 0 THEN d.loan_amt * d.period END) 累积放款金额_期限
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) >= 0 THEN 授信额度 END) 授信金额_累积放款
        ,MAX(CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 7 THEN 授信额度 END) t7授信金额_放款
        ,COUNT(DISTINCT CASE    WHEN d.loan_time IS NOT NULL THEN d.user_no END) 累计放款人
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 7 THEN d.user_no END) t7放款人
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) BETWEEN 0 AND 3 THEN d.user_no END) t3放款人
        ,COUNT(DISTINCT CASE    WHEN DATEDIFF(d.loan_time,d.first_order_time) = 0 THEN d.user_no END) 放款人
        ,COUNT(DISTINCT CASE    WHEN coupon_Xdfree.app_user_id IS NOT NULL THEN d.user_no END) 借款订单绑定免息券 --- 借款订单使用免息券，借款订单绑定息费券,免息券成本,借款券成本
        ,COUNT(DISTINCT 
              CASE    WHEN coupon_Xdfree.app_user_id IS NOT NULL AND coupon_Xdfree.used_time IS NOT NULL THEN d.user_no END
        ) 借款订单使用免息券
        ,COUNT(DISTINCT CASE    WHEN coupon_jkq.app_user_id IS NOT NULL THEN d.user_no END) 借款订单绑定息费券
        ,MAX(
            CASE    WHEN coupon_Xdfree.app_user_id IS NOT NULL AND coupon_Xdfree.used_time IS NOT NULL THEN coupon_Xdfree.实际抵扣金额 END
        ) 免息券成本
        ,MAX(
            CASE    WHEN coupon_jkq.app_user_id IS NOT NULL AND coupon_jkq.used_time IS NOT NULL THEN coupon_jkq.实际抵扣金额 END
        ) 借款券成本
        ,COUNT(DISTINCT 
              CASE    WHEN (vip_fx.order_time IS NOT NULL OR vip_fy.order_time IS NOT NULL) THEN d.user_no END
        ) 会员卡签约人
        ,COUNT(DISTINCT CASE    WHEN (vip_fy.order_time IS NOT NULL) THEN d.user_no END) 飞跃会员卡签约人
        ,COUNT(DISTINCT 
              CASE    WHEN ((vip_fy.order_time IS NOT NULL
                          AND vip_fy.order_status = 'pay_success')
                          OR (vip_fx.order_time IS NOT NULL
                          AND vip_fx.order_status = 3)) THEN d.user_no END
        ) 会员卡扣费用户
        ,MAX(
            CASE    WHEN vip_fy.order_time IS NOT NULL AND vip_fy.order_status = 'pay_success' THEN vip_fy.real_card_price
                    WHEN vip_fx.order_time IS NOT NULL AND vip_fx.order_status = 3 THEN vip_fx.real_card_price / 100
            END
        ) 会员卡扣款金额
        ,COUNT(DISTINCT CASE    WHEN po.cust_no IS NOT NULL THEN d.user_no END) 预借款发起
        ,COUNT(DISTINCT CASE    WHEN rh_debt_with_half_houseloan_new >= 11000 THEN d.user_no END) 高负债人数 ----有负债人数,负债金额总和
        ,COUNT(DISTINCT CASE    WHEN rh_debt_with_half_houseloan_new >= 0 THEN d.user_no END) 有负债人数
        ,MAX(rh_debt_with_half_houseloan_new) 负债金额总和
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账7plus金额 ELSE NULL END) 出账7plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账15plus金额 ELSE NULL END) 出账15plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账30plus金额 ELSE NULL END) 出账30plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账60plus金额 ELSE NULL END) 出账60plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账90plus金额 ELSE NULL END) 出账90plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账120plus金额 ELSE NULL END) 出账120plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账150plus金额 ELSE NULL END) 出账150plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账180plus金额 ELSE NULL END) 出账180plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账210plus金额 ELSE NULL END) 出账210plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账240plus金额 ELSE NULL END) 出账240plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账270plus金额 ELSE NULL END) 出账270plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账300plus金额 ELSE NULL END) 出账300plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账330plus金额 ELSE NULL END) 出账330plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账360plus金额 ELSE NULL END) 出账360plus金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账7plus逾期金额 ELSE NULL END) 出账7plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账15plus逾期金额 ELSE NULL END) 出账15plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账30plus逾期金额 ELSE NULL END) 出账30plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账60plus逾期金额 ELSE NULL END) 出账60plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账90plus逾期金额 ELSE NULL END) 出账90plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账120plus逾期金额 ELSE NULL END) 出账120plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账150plus逾期金额 ELSE NULL END) 出账150plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账180plus逾期金额 ELSE NULL END) 出账180plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账210plus逾期金额 ELSE NULL END) 出账210plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账240plus逾期金额 ELSE NULL END) 出账240plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账270plus逾期金额 ELSE NULL END) 出账270plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账300plus逾期金额 ELSE NULL END) 出账300plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账330plus逾期金额 ELSE NULL END) 出账330plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN 出账360plus逾期金额 ELSE NULL END) 出账360plus逾期金额
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN fpd7_available ELSE NULL END) fpd7_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN fpd15_available ELSE NULL END) fpd15_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m1_available ELSE NULL END) m1_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m2_available ELSE NULL END) m2_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m3_available ELSE NULL END) m3_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m4_available ELSE NULL END) m4_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m5_available ELSE NULL END) m5_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m6_available ELSE NULL END) m6_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m7_available ELSE NULL END) m7_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m8_available ELSE NULL END) m8_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m9_available ELSE NULL END) m9_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m10_available ELSE NULL END) m10_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m11_available ELSE NULL END) m11_available
        ,MAX(CASE    WHEN d.loan_time IS NOT NULL THEN m12_available ELSE NULL END) m12_available
FROM    zhubiao d
LEFT JOIN   (
                SELECT  *
                FROM    xyf_dws.dws_preloan_register_conversion_df
                WHERE   pt = MAX_PT('xyf_dws.dws_preloan_register_conversion_df')
            ) r
ON      d.user_no = r.app_user_id
LEFT JOIN   (
                SELECT  *
                FROM    xyf_bi.fk_risk_act_feature_df_forbi
                WHERE   pt = MAX_PT('xyf_bi.fk_risk_act_feature_df_forbi')
            ) hx
ON      d.shouxin_biz_flow_number = hx.biz_flow_number
LEFT JOIN   (
                ----判断用户当天是否动支失败过？
                SELECT  fail.cust_no
                        ,zhubiao.first_order_time
                        ,MAX(fail.first_order_time) 本次提现前最近一次提现时间
                FROM    (
                            SELECT  *
                            FROM    xyf_dws.dws_inloan_user_order_df
                            WHERE   pt = '${bizdate}'
                            AND     loan_flag = '首贷'
                            AND     loan_status = 'failed'
                            AND     date(first_order_time) >= '2024-01-01'
                        ) fail
                INNER JOIN  (
                                SELECT  *
                                FROM    zhubiao
                            ) zhubiao
                ON      fail.cust_no = zhubiao.cust_no
                AND     fail.first_order_time < zhubiao.first_order_time
                GROUP BY fail.cust_no
                         ,zhubiao.first_order_time
            ) dzsb
ON      dzsb.cust_no = d.cust_no
AND     dzsb.first_order_time = d.first_order_time
LEFT JOIN   (
                SELECT  *
                        ,CAST(GET_JSON_OBJECT(extend_data,'$.loanAmountFen') / 100 AS DOUBLE) AS 预借款提交金额
                        ,GET_JSON_OBJECT(extend_data,'$.term') AS 预借款提交期数
                FROM    xyf_dwd.dwd_inloan_loan_pre_apply_df
                WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_loan_pre_apply_df')
            ) po
ON      d.first_order_number = po.relate_order_no
LEFT JOIN   (
                SELECT  *
                FROM    coupon
                WHERE   coupon_type = 5
            ) coupon_Xdfree
ON      d.coupon_id = coupon_Xdfree.sub_id
AND     d.user_no = coupon_Xdfree.app_user_id
LEFT JOIN   (
                SELECT  *
                FROM    coupon
                WHERE   coupon_type IN (1,6)
            ) coupon_jkq
ON      d.coupon_id = coupon_jkq.sub_id
AND     d.user_no = coupon_jkq.app_user_id
LEFT JOIN   (
                SELECT  *
                FROM    xyf_dwd.dwd_inloan_leap_vip_order_hf
                WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_leap_vip_order_hf')
                AND     vip_order_number = first_vip_order_number --不看续约
                AND     order_time IS NOT NULL
            ) vip_fy
ON      vip_fy.loan_order_number = d.first_order_number
LEFT JOIN   (
                SELECT  *
                FROM    xyf_dwd.dwd_user_vip_order_df
                WHERE   pt = MAX_PT('xyf_dwd.dwd_user_vip_order_df')
                AND     vip_card_type = 1 ----筛选会员卡购卡订单
                AND     order_status IN (1,3,4,5,6) ----成功签约，不一定成功付款
                AND     vip_order_number = first_vip_order_number --不看续约
                AND     order_time IS NOT NULL
                AND     app_user_id IS NOT NULL
            ) vip_fx
ON      vip_fx.order_number_loan = d.first_order_number
LEFT JOIN   (
                SELECT  id_card_number
                        ,cust_no
                        ,monthly_income
                        ,gender
                        ,age
                        ,education
                FROM    xyf_ads.ads_feature_idcard_essentialinfo_v2_df
                WHERE   pt = MAX_PT('xyf_ads.ads_feature_idcard_essentialinfo_v2_df')
            ) jc
ON      d.cust_no = jc.cust_no
LEFT JOIN xyf_bi.qudao_uid_syt qd
ON      qd.app_user_id = d.user_no --
LEFT JOIN   (
                SELECT  DISTINCT biz_flow_number
                FROM    xyf_dwd.dwd_inloan_t_decision_result_detail_df
                WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_t_decision_result_detail_df')
                AND     enginecode IN ('jcl_20240906000005','jcl_20240906000003')
                AND     GET_JSON_OBJECT(context,'$.app_laohui_label_output') = 'vip_laohui'
            ) laohui
ON      d.biz_flow_number = laohui.biz_flow_number
LEFT JOIN   (
                SELECT  DISTINCT biz_flow_number
                FROM    xyf_dwd.dwd_inloan_t_decision_result_detail_df
                WHERE   pt = MAX_PT('xyf_dwd.dwd_inloan_t_decision_result_detail_df')
                AND     decision_time >= '2025-03-01 00:00:00'
                AND     enginecode = 'jcl_20240402000002'
                AND     (
                            GET_JSON_OBJECT(context,'$.jcl_20240402000002_50_classify_name') = '会员卡捞回'
                            OR      GET_JSON_OBJECT(context,'$.jcl_20240402000002_52_classify_name') = '会员卡捞回'
                )
                AND     hitresultlist RLIKE 'API转APP人行阶段规则_api'
            ) tp3
ON      tp3.biz_flow_number = d.biz_flow_number
LEFT JOIN   (
                ---订单表拆单订单中间表
                SELECT  t.first_order_number
                        ,SUM(初始应还总息费) 初始应还总息费
                FROM    zhubiao t
                LATERAL VIEW EXPLODE(SPLIT(t.order_number,',')) tmp AS split_ordernumber
                JOIN    (
                            SELECT  user_no
                                    ,order_number
                                    ,SUM(initial_interest + initial_after_loan_fee + initial_platform_fee) AS 初始应还总息费
                            FROM    xyf_dwd.dwd_repay_loan_repay_plan_df
                            WHERE   pt = '${bizdate}'
                            AND     date(date_created) >= '2024-01-01'
                            GROUP BY user_no
                                     ,order_number
                        ) rp
                ON      tmp.split_ordernumber = rp.order_number
                GROUP BY first_order_number
            ) zj
ON      zj.first_order_number = d.first_order_number
LEFT JOIN   (
                SELECT                  ---order_number
                        ori_order_number
                        ,cust_no
                        ,CASE   WHEN y0_1_7 = 1 THEN due_amt / 100
                        END AS 出账7plus金额
                        ,NVL(CASE    WHEN y0_1_7 = 1 THEN y3_1_7 / 100 END,0) AS 出账7plus逾期金额
                        ,CASE   WHEN y0_1_15 = 1 THEN due_amt / 100
                        END AS 出账15plus金额
                        ,NVL(CASE    WHEN y0_1_15 = 1 THEN y3_1_15 / 100 END,0) AS 出账15plus逾期金额 --1_30
                        ,CASE   WHEN y0_1_30 = 1 THEN due_amt / 100
                        END AS 出账30plus金额
                        ,NVL(CASE    WHEN y0_1_30 = 1 THEN y3_1_30 / 100 END,0) AS 出账30plus逾期金额 --2_30
                        ,CASE   WHEN y0_2_30 = 1 THEN due_amt / 100
                        END AS 出账60plus金额
                        ,NVL(CASE    WHEN y0_2_30 = 1 THEN y3_2_30 / 100 END,0) AS 出账60plus逾期金额 --3_30
                        ,CASE   WHEN y0_3_30 = 1 THEN due_amt / 100
                        END AS 出账90plus金额
                        ,NVL(CASE    WHEN y0_3_30 = 1 THEN y3_3_30 / 100 END,0) AS 出账90plus逾期金额 --4_30
                        ,CASE   WHEN y0_4_30 = 1 THEN due_amt / 100
                        END AS 出账120plus金额
                        ,NVL(CASE    WHEN y0_4_30 = 1 THEN y3_4_30 / 100 END,0) AS 出账120plus逾期金额 --6_30
                        ,CASE   WHEN y0_5_30 = 1 THEN due_amt / 100
                        END AS 出账150plus金额
                        ,NVL(CASE    WHEN y0_5_30 = 1 THEN y3_5_30 / 100 END,0) AS 出账150plus逾期金额 --_30
                        ,CASE   WHEN y0_6_30 = 1 THEN due_amt / 100
                        END AS 出账180plus金额
                        ,NVL(CASE    WHEN y0_6_30 = 1 THEN y3_6_30 / 100 END,0) AS 出账180plus逾期金额
                        ,CASE   WHEN y0_7_30 = 1 THEN due_amt / 100
                        END AS 出账210plus金额
                        ,NVL(CASE    WHEN y0_7_30 = 1 THEN y3_7_30 / 100 END,0) AS 出账210plus逾期金额
                        ,CASE   WHEN y0_8_30 = 1 THEN due_amt / 100
                        END AS 出账240plus金额
                        ,NVL(CASE    WHEN y0_8_30 = 1 THEN y3_8_30 / 100 END,0) AS 出账240plus逾期金额
                        ,CASE   WHEN y0_9_30 = 1 THEN due_amt / 100
                        END AS 出账270plus金额
                        ,NVL(CASE    WHEN y0_9_30 = 1 THEN y3_9_30 / 100 END,0) AS 出账270plus逾期金额
                        ,CASE   WHEN y0_10_30 = 1 THEN due_amt / 100
                        END AS 出账300plus金额
                        ,NVL(CASE    WHEN y0_10_30 = 1 THEN y3_10_30 / 100 END,0) AS 出账300plus逾期金额
                        ,CASE   WHEN y0_11_30 = 1 THEN due_amt / 100
                        END AS 出账330plus金额
                        ,NVL(CASE    WHEN y0_11_30 = 1 THEN y3_11_30 / 100 END,0) AS 出账330plus逾期金额
                        ,CASE   WHEN y0_12_30 = 1 THEN due_amt / 100
                        END AS 出账360plus金额
                        ,NVL(CASE    WHEN y0_12_30 = 1 THEN y3_12_30 / 100 END,0) AS 出账360plus逾期金额 ---------
                        ,CASE   WHEN y0_1_7 = 1 THEN 1
                                ELSE 0
                        END AS fpd7_available
                        ,CASE   WHEN y0_1_15 = 1 THEN 1
                                ELSE 0
                        END AS fpd15_available
                        ,CASE   WHEN y0_1_30 = 1 THEN 1
                                ELSE 0
                        END AS m1_available
                        ,CASE   WHEN y0_2_30 = 1 THEN 1
                                ELSE 0
                        END AS m2_available
                        ,CASE   WHEN y0_3_30 = 1 THEN 1
                                ELSE 0
                        END AS m3_available
                        ,CASE   WHEN y0_4_30 = 1 THEN 1
                                ELSE 0
                        END AS m4_available
                        ,CASE   WHEN y0_5_30 = 1 THEN 1
                                ELSE 0
                        END AS m5_available
                        ,CASE   WHEN y0_6_30 = 1 THEN 1
                                ELSE 0
                        END AS m6_available
                        ,CASE   WHEN y0_7_30 = 1 THEN 1
                                ELSE 0
                        END AS m7_available
                        ,CASE   WHEN y0_8_30 = 1 THEN 1
                                ELSE 0
                        END AS m8_available
                        ,CASE   WHEN y0_9_30 = 1 THEN 1
                                ELSE 0
                        END AS m9_available
                        ,CASE   WHEN y0_10_30 = 1 THEN 1
                                ELSE 0
                        END AS m10_available
                        ,CASE   WHEN y0_11_30 = 1 THEN 1
                                ELSE 0
                        END AS m11_available
                        ,CASE   WHEN y0_12_30 = 1 THEN 1
                                ELSE 0
                        END AS m12_available ---FROM    xyf_dws.dws_repay_risk_order_bill_mob_df
                FROM    xyf_dws.dws_repay_risk_order_bill_mob_agg_df ---这个是大额拆单后的新表,区别在于，用户1笔拆成多笔之后有1笔违约就算全部违约。
                WHERE   pt = '${bizdate}'
            ) mob ---ON      d.order_number = mob.order_number
ON      d.first_order_number = mob.ori_order_number -- LEFT JOIN   (
--                 SELECT  user_no
--                         ,order_number
--                         ,SUM(initial_interest + initial_after_loan_fee + initial_platform_fee) AS 初始应还总息费
--                 FROM    xyf_dwd.dwd_repay_loan_repay_plan_df
--                 WHERE   pt = '${bizdate}'
--                 AND     date(date_created) >= '2024-01-01'
--                 GROUP BY user_no
--                          ,order_number
--             ) rp
-- ON      d.order_number = rp.order_number
LEFT JOIN   (
                SELECT  day_id_iso
                        ,CONCAT(day_week01_xf_new,'至',day_weekend_xf_new) AS week_range
                FROM    xyf_dim.dim_pub_date
            ) zhou
ON      TO_DATE(d.first_order_time) = zhou.day_id_iso
LEFT JOIN   (
                SELECT  day_id_iso
                        ,CONCAT(day_week01_xf_new,'至',day_weekend_xf_new) AS week_range
                FROM    xyf_dim.dim_pub_date
            ) zhou2
ON      TO_DATE(d.loan_time) = zhou2.day_id_iso
GROUP BY d.user_no
         ,dt
         ,wt
         ,放款周
         ,mt
         ,授信金额_level
         ,biz_type_bi
         ,biz_type_bi_3
         ,CASE   WHEN jc.age <= 24 THEN jc.age
                 WHEN jc.age BETWEEN 55 AND 60 THEN jc.age
                 WHEN jc.age BETWEEN 25 AND 54 THEN '25~54'
                 WHEN jc.age >= 61 THEN '61岁以上'
         END
         ,是否API授信
         ,注册提现时间差
         ,授信提现时间差
         ,是否小程序提现
         ,定价
         ,是否虚假给额
         ,归因渠道大类_放款
         ,大盘分组
         ,授信评级
         ,动支评级
         ,放款日
         ,是否首次提现
         ,授信多头
         ,冻额标识
         ,是否额外放开
         ,是否拆单
;

DROP TABLE IF EXISTS xyf_bi_dev.bi_app_zhuanhua_tixian_sum
;

CREATE TABLE xyf_bi_dev.bi_app_zhuanhua_tixian_sum AS
SELECT  dt
        ,wt
        ,mt
        ,放款周
        ,SUBSTR(放款日,1,7) 放款月
        ,授信金额_level
        ,biz_type_bi
        ,biz_type_bi_3
        ,年龄
        ,是否API授信
        ,注册提现时间差
        ,授信提现时间差
        ,是否小程序提现
        ,定价
        ,是否虚假给额
        ,归因渠道大类_放款
        ,大盘分组
        ,授信评级
        ,动支评级
        ,是否首次提现
        ,授信多头
        ,冻额标识
        ,是否额外放开
        ,是否拆单
        ,CASE   WHEN 高负债人数 = 1 THEN '高负债>=1.1w'
                WHEN 有负债人数 = 1 THEN '低负债<1.1w'
                ELSE '无负债数据'
        END AS 授信时负债情况 ----有负债人数,负债金额总和
        ,CASE   WHEN 累计放款人 = 1 THEN '放款'
                ELSE '未放款'
        END AS 是否放款
        ,CASE   WHEN 会员卡签约人 = 1 THEN '签约会员卡'
                ELSE '未签约会员卡'
        END AS 是否会员卡签约
        ,CASE   WHEN 飞跃会员卡签约人 = 1 THEN '签约飞跃'
                WHEN 会员卡签约人 = 1 THEN '签约飞享'
                ELSE '未签约会员卡'
        END AS 签约会员卡类型
        ,CASE   WHEN 会员卡扣费用户 = 1 THEN '会员卡扣款'
                ELSE '未付费或未签约'
        END AS 是否会员卡扣款
        ,CASE   WHEN 预借款发起 = 1 THEN '预借款订单'
                ELSE '其他订单'
        END AS 是否预借款订单
        ,CASE   WHEN 借款订单绑定免息券 = 1 AND 借款订单绑定息费券 = 1 THEN '绑定借款券和免息券'
                WHEN 借款订单绑定免息券 = 1 THEN '仅绑定免息券'
                WHEN 借款订单绑定息费券 = 1 THEN '仅绑定借款券'
                ELSE '无券'
        END AS 订单是否绑定券
        ,CASE   WHEN 借款订单使用免息券 = 1 THEN '使用免息券'
                WHEN 借款订单绑定免息券 = 1 THEN '绑定免息券但未使用'
                ELSE '未绑定免息券'
        END AS 是否使用免息券
        ,SUM(NVL(免息券成本,0) + NVL(借款券成本,0)) 优惠券成本
        ,SUM(有负债人数) 授信时有负债人数
        ,SUM(负债金额总和) 授信时负债金额总和
        ,SUM(高负债人数) 授信时高负债人数
        ,SUM(会员卡签约人) 会员卡签约用户
        ,SUM(会员卡扣款金额) 会员卡扣款金额
        ,SUM(会员卡扣费用户) 会员卡扣费用户
        ,SUM(授信额度) 授信额度
        ,SUM(提现人) 提现人
        ,SUM(提现金额) 提现金额
        ,SUM(期限 * 提现金额) 提现金额_期限
        ,SUM(风险通过人数) 风险通过人数
        ,SUM(风险通过金额) 风险通过金额
        ,SUM(t0资方通过人) t0资方通过人
        ,SUM(t3资方通过人) t3资方通过人
        ,SUM(t7资方通过人) t7资方通过人
        ,SUM(累积资方通过人) 累积资方通过人
        ,SUM(资方通过人2h) 资方通过人2h
        ,SUM(放款金额) 放款金额
        ,SUM(t3放款金额) t3放款金额
        ,SUM(t7放款金额) t7放款金额
        ,SUM(累计放款金额) 累计放款金额
        ,SUM(累积放款金额_期限) 累积放款金额_期限
        ,SUM(授信金额_累积放款) 授信金额_累积放款
        ,SUM(t7授信金额_放款) t7授信金额_放款
        ,SUM(累计放款人) 累计放款人
        ,SUM(t7放款人) t7放款人
        ,SUM(t3放款人) t3放款人
        ,SUM(放款人) 放款人
        ,SUM(定价_金额) 定价_金额
        ,SUM(APR口径应收息费) APR口径应收息费
        ,SUM(出账7plus金额) 出账7plus金额
        ,SUM(出账15plus金额) 出账15plus金额
        ,SUM(出账30plus金额) 出账30plus金额
        ,SUM(出账60plus金额) 出账60plus金额
        ,SUM(出账90plus金额) 出账90plus金额
        ,SUM(出账120plus金额) 出账120plus金额
        ,SUM(出账150plus金额) 出账150plus金额
        ,SUM(出账180plus金额) 出账180plus金额
        ,SUM(出账210plus金额) 出账210plus金额
        ,SUM(出账240plus金额) 出账240plus金额
        ,SUM(出账270plus金额) 出账270plus金额
        ,SUM(出账300plus金额) 出账300plus金额
        ,SUM(出账330plus金额) 出账330plus金额
        ,SUM(出账360plus金额) 出账360plus金额
        ,SUM(出账7plus逾期金额) 出账7plus逾期金额
        ,SUM(出账15plus逾期金额) 出账15plus逾期金额
        ,SUM(出账30plus逾期金额) 出账30plus逾期金额
        ,SUM(出账60plus逾期金额) 出账60plus逾期金额
        ,SUM(出账90plus逾期金额) 出账90plus逾期金额
        ,SUM(出账120plus逾期金额) 出账120plus逾期金额
        ,SUM(出账150plus逾期金额) 出账150plus逾期金额
        ,SUM(出账180plus逾期金额) 出账180plus逾期金额
        ,SUM(出账210plus逾期金额) 出账210plus逾期金额
        ,SUM(出账240plus逾期金额) 出账240plus逾期金额
        ,SUM(出账270plus逾期金额) 出账270plus逾期金额
        ,SUM(出账300plus逾期金额) 出账300plus逾期金额
        ,SUM(出账330plus逾期金额) 出账330plus逾期金额
        ,SUM(出账360plus逾期金额) 出账360plus逾期金额
        ,SUM(fpd7_available) fpd7_available
        ,SUM(fpd15_available) fpd15_available
        ,SUM(m1_available) m1_available
        ,SUM(m2_available) m2_available
        ,SUM(m3_available) m3_available
        ,SUM(m4_available) m4_available
        ,SUM(m5_available) m5_available
        ,SUM(m6_available) m6_available
        ,SUM(m7_available) m7_available
        ,SUM(m8_available) m8_available
        ,SUM(m9_available) m9_available
        ,SUM(m10_available) m10_available
        ,SUM(m11_available) m11_available
        ,SUM(m12_available) m12_available
FROM    xyf_bi_dev.bi_app_zhuanhua_tixian_new_uid
GROUP BY dt
         ,wt
         ,mt
         ,授信金额_level
         ,biz_type_bi
         ,biz_type_bi_3
         ,年龄
         ,是否API授信
         ,注册提现时间差
         ,授信提现时间差
         ,是否小程序提现
         ,定价
         ,是否虚假给额
         ,是否会员卡签约
         ,归因渠道大类_放款
         ,大盘分组
         ,是否预借款订单 ----
         ,是否会员卡扣款
         ,签约会员卡类型
         ,授信评级
         ,动支评级
         ,放款周
         ,放款月
         ,是否放款
         ,订单是否绑定券 ---
         ,是否使用免息券
         ,是否首次提现
         ,授信多头
         ,冻额标识
         ,授信时负债情况
         ,是否额外放开
         ,是否拆单