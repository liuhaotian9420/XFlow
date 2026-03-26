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
SELECT *
FROM  xyf_bi_dev.bi_app_zhuanhua_tixian_new_uid 
limit 1000;