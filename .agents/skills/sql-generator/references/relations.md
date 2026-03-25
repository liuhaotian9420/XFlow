# join_relations

## xyf_ads.ads_fin_onloan_fee_df -> xyf_dim.dim_pub_date

- join_type: `inner join`
- condition: `a.biz_type = b.biz_type AND a.dayid <= b.day_id_iso`

## xyf_bi_dev.amt_predict_oct24_v2 -> xyf_dws.dws_inloan_loan_risk_stat_df

- join_type: `join`
- condition: `t1.loan_date = t3.order_date AND t3.pt = MAX_PT('xyf_dws.dws_inloan_loan_risk_stat_df')`

## xyf_dws.dws_inloan_loan_channel_stat_df -> xyf_bi_dev.amt_predict_oct24_v2

- join_type: `left join`
- condition: `substr(t1.loan_date, 1, 10) = substr(t2.tgt_dt, 1, 10) LEFT`

## xyf_dws.dws_inloan_user_order_df -> xyf_dwd.dwd_risk_model_b_card_df

- join_type: `left join`
- condition: `a.cust_no = b.cust_no AND b.pt >= '20240901' AND DATE(a.first_order_time) = DATE(b.decision_time)`

- join_type: `left join`
- condition: `a.cust_no = b.cust_no AND b.pt >= '20240901' AND DATE(a.first_order_time) = DATE(b.decision_time)`

## xyf_dws.dws_inloan_user_order_df -> xyf_dws.dws_repay_risk_order_bill_mob_df

- join_type: `inner join`
- condition: `a.pt = '${bizdate}' AND b.pt = '${bizdate}' AND DATE(a.loan_time) >= '2024-07-01' AND a.order_number = b.order_number AND a.app IN ('xyf01', 'fxk') AND lower(a.app) = lower(a.inner_app) AND a.loan_flag IN ('复贷', '加贷') AND a.loan_status = 'success' LEFT`

## xyf_dws.dws_inloan_user_order_df -> xyf_fengkong_dev.scq_fy_history_risk_price_modify

- join_type: `left join`
- condition: `orders.first_order_number = ori_price_overwritten.ori_order_number LEFT`

## xyf_dws.dws_repay_risk_order_bill_mob_df -> xyf_fengkong_dev.wzq_order_b5_b4_compare_base

- join_type: `join`
- condition: `a.order_number = c.order_number`

## xyf_dws.dws_repay_user_order_df -> xyf_dim.dim_pub_date

- join_type: `inner join`
- condition: `a.pt = b.day_id AND b.is_lastday = 1 AND b.day_id_iso >= '2023-01-31' AND b.day_id_iso <= DATE_SUB(DATETRUNC(CURRENT_DATE(),'MM'),1)`

## xyf_fengkong_dev.scq_fy_history_risk_price_modify -> xyf_dwd.dwd_inloan_loan_apply_main_df

- join_type: `join`
- condition: `orders.first_order_number = application.ori_order_number`
