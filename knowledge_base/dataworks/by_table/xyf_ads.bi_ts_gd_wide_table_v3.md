# xyf_ads.bi_ts_gd_wide_table_v3

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| month_cj | STRING | column | 创建月份 |  |
| week_cj | STRING | column | 创建客服周 |  |
| date_cj | STRING | column | 创建日期 |  |
| real_time | DATETIME | column | 真实投诉时间 |  |
| create_time | DATETIME | column | 创建时间 |  |
| distributed_time | STRING | column | 分配时间 |  |
| end_time | STRING | column | 结单时间 |  |
| task_number | STRING | column | 工单编号 |  |
| is_zq | STRING | column | 是否重渠 |  |
| channel_1_type_new | STRING | column | 新一级渠道 |  |
| channel_2_type_new | STRING | column | 新二级渠道 |  |
| task_type_name_new | STRING | column | 新一级诉因 |  |
| question_type_name_new | STRING | column | 新二级诉因 |  |
| complaint_type_new | STRING | column | 新三级诉因 |  |
| task_status | STRING | column | 工单状态 |  |
| company_name | STRING | column | 被诉主体 |  |
| comment | STRING | column | 投诉内容 |  |
| channel_1_type | STRING | column | 原一级渠道 |  |
| channel_2_type | STRING | column | 原二级渠道 |  |
| task_type_name | STRING | column | 原一级诉因 |  |
| question_type_name | STRING | column | 原二级诉因 |  |
| complaint_type | STRING | column | 原三级诉因 |  |
| create_work_number | STRING | column | 创建人工号 |  |
| create_work_name | STRING | column | 创建人姓名 |  |
| create_department | STRING | column | 创建人分类 |  |
| process_work_number | STRING | column | 跟进人工号 |  |
| process_work_name | STRING | column | 跟进人姓名 |  |
| work_department | STRING | column | 跟进人分类 |  |
| vip_order_number | STRING | column | 飞享会员卡订单号_原始 |  |
| vip_order_number_pd | STRING | column | 飞享会员卡订单号_填写判断 |  |
| vip_order_no_new | STRING | column | 飞享会员订单号_正则提取 |  |
| is_exposure | STRING | column | 是否曝光 |  |
| hm_cs | BIGINT | column | 黑猫历史投诉次数_含本次 |  |
| hm_app_name | STRING | column | 黑猫app划分 |  |
| is_yangyan | BIGINT | column | 是否扬言_备注或小结命中扬言关键词 |  |
| is_blackindustry | BIGINT | column | 是否命中黑产标签 |  |
| blackindustry_complaint_app | STRING | column | 黑产标签_投诉app |  |
| blackindustry_wifi_gather | STRING | column | 黑产标签_wifi聚集 |  |
| blackindustry_device_gather | STRING | column | 黑产标签_设备聚集 |  |
| blackindustry_customer_annotation | STRING | column | 黑产标签_客服标注 |  |
| black_industry_level | STRING | column | 黑产级别 |  |
| is_complaint_risk | STRING | column | 是否高风险用户 |  |
| business_line_name | STRING | column | 业务线名称 |  |
| b_score | STRING | column | 最新b卡评分 |  |
| b_score_level | STRING | column | 最新b卡等级划分 |  |
| mobile | STRING | column | 手机号 |  |
| mobile_md5 | STRING | column | 手机号md5 |  |
| id_card_number | STRING | column | 身份证号 |  |
| cust_no | STRING | column | 客户号 |  |
| user_no | STRING | column | 用户号 |  |
| register_utm_source | STRING | column | 注册utm_source |  |
| mobile_utm_source | STRING | column | 手机utm_source |  |
| user_name | STRING | column | 客户名称 |  |
| gender | STRING | column | 性别 |  |
| age | STRING | column | 年龄 |  |
| education | STRING | column | 学历 |  |
| job | STRING | column | 职业 |  |
| monthly_income | STRING | column | 收入 |  |
| province | STRING | column | 省份 |  |
| city | STRING | column | 城市 |  |
| order_number | STRING | column | 订单号 |  |
| order_number_source | STRING | column | 订单来源 |  |
| app | STRING | column | 订单app |  |
| inner_app | STRING | column | 订单inner_app |  |
| inner_app_name | STRING | column | inner_app名称 |  |
| loan_type_name | STRING | column | 订单首复贷 |  |
| fund | STRING | column | 资方or监管名称 |  |
| fund_name | STRING | column | 资方名称 |  |
| fund_jg | STRING | column | 资方监管名称 |  |
| asset_type | STRING | column | 费率 |  |
| new_asset_type | STRING | column | 产品类型 |  |
| pre_settle_time | DATETIME | column | 提前结清时间 |  |
| pre_perprid | STRING | column | 在哪一期提前结清 |  |
| settle_date | DATETIME | column | 订单结清时间 |  |
| end_date | DATETIME | column | 贷款最后一期还款日期 |  |
| settle_date_pd | STRING | column | 结清时间判断 |  |
| loan_time | DATETIME | column | 订单放款时间 |  |
| date_fk | DATETIME | column | 订单放款日期 |  |
| week_fk | STRING | column | 订单放款客服周 |  |
| month_fk | STRING | column | 订单放款月份 |  |
| order_month | BIGINT | column | 投诉间隔月_投诉月减放款月 |  |
| last_repay_time | DATETIME | column | 投诉时用户最后一次还款时间 |  |
| overdue_zl_tss | STRING | column | 投诉时账龄 |  |
| repay_status_tss | STRING | column | 投诉时订单状态 |  |
| repay_status_after30d | STRING | column | 投诉后第30天订单状态 |  |
| overdue_m_tss | STRING | column | 投诉时逾期阶段 |  |
| overdue_days_tss | BIGINT | column | 投诉时逾期天数 |  |
| period | BIGINT | column | 贷款总期数 |  |
| loan_amt | DECIMAL(38,18) | column | 贷款金额元 |  |
| loan_amt_fb | STRING | column | 贷款金额分布 |  |
| case_id | BIGINT | column | 案件id |  |
| case_code | STRING | column | 案件号 |  |
| dept_name | STRING | column | 诉时机构 |  |
| over_due_days | BIGINT | column | 逾期天数 |  |
| coll_stage | STRING | column | 诉时队列 |  |
| in_agssin_over_due_days | INT | column | 诉时入催天数 |  |
| zhongqu_score | STRING | column | 当日重渠分 |  |
| zhongqu_score_max_7d | STRING | column | 近7天重渠分最大值 |  |
| zhongqu_score_max_30d | STRING | column | 近30天重渠分最大值 |  |
| is_zqts_7d_after | BIGINT | column | 投诉后7天内是否重渠投诉 |  |
| is_zqts_15d_after | BIGINT | column | 投诉后15天内是否重渠投诉 |  |
| is_zqts_30d_after | BIGINT | column | 投诉后30天内是否重渠投诉 |  |
| zqcs_7d | BIGINT | column | 投诉后7天内重渠次数_创建时间 |  |
| zqcs_15d | BIGINT | column | 投诉后15天内重渠次数_创建时间 |  |
| zqcs_30d | BIGINT | column | 投诉后30天内重渠次数_创建时间 |  |
| create_time_zq_15d | DATETIME | column | 创建时间_15天内首次重渠 |  |
| task_number_15d | STRING | column | 工单号_15天内首次重渠 |  |
| order_number_15d | STRING | column | 订单号_15天内首次重渠 |  |
| channel_1_type_zq_15d | STRING | column | 新一级渠道_15天内首次重渠 |  |
| channel_2_type_15d | STRING | column | 新二级渠道_15天内首次重渠 |  |
| task_type_name_15d | STRING | column | 新一级诉因_15天内首次重渠 |  |
| question_type_name_15d | STRING | column | 新二级诉因_15天内首次重渠 |  |
| complaint_type_15d | STRING | column | 新三级诉因_15天内首次重渠 |  |
| comment_15d | STRING | column | 投诉内容_15天内首次重渠 |  |
| create_work_number_15d | STRING | column | 创建人工号_15天内首次重渠 |  |
| create_work_name_15d | STRING | column | 创建人姓名_15天内首次重渠 |  |
| create_department_15d | STRING | column | 创建人分类_15天内首次重渠 |  |
| process_work_number_15d | STRING | column | 跟进人工号_15天内首次重渠 |  |
| process_work_name_15d | STRING | column | 跟进人姓名_15天内首次重渠 |  |
| work_department_15d | STRING | column | 跟进人分类_15天内首次重渠 |  |
| create_time_zq_30d | DATETIME | column | 创建时间_30天内首次重渠 |  |
| task_number_30d | STRING | column | 工单号_30天内首次重渠 |  |
| order_number_30d | STRING | column | 订单号_30天内首次重渠 |  |
| channel_1_type_zq_30d | STRING | column | 新一级渠道_30天内首次重渠 |  |
| channel_2_type_30d | STRING | column | 新二级渠道_30天内首次重渠 |  |
| task_type_name_30d | STRING | column | 新一级诉因_30天内首次重渠 |  |
| question_type_name_30d | STRING | column | 新二级诉因_30天内首次重渠 |  |
| complaint_type_30d | STRING | column | 新三级诉因_30天内首次重渠 |  |
| comment_30d | STRING | column | 投诉内容_30天内首次重渠 |  |
| create_work_number_30d | STRING | column | 创建人工号_30天内首次重渠 |  |
| create_work_name_30d | STRING | column | 创建人姓名_30天内首次重渠 |  |
| create_department_30d | STRING | column | 创建人分类_30天内首次重渠 |  |
| process_work_number_30d | STRING | column | 跟进人工号_30天内首次重渠 |  |
| process_work_name_30d | STRING | column | 跟进人姓名_30天内首次重渠 |  |
| work_department_30d | STRING | column | 跟进人分类_30天内首次重渠 |  |
| tsll_7 | STRING | column | 投诉前链路_7天内 |  |
| tsll_15 | STRING | column | 投诉前链路_15天内 |  |
| tsll_30 | STRING | column | 投诉前链路_30天内 |  |
| is_kfdt_7d_before | BIGINT | column | 是否进过客服大厅_前7天内 |  |
| is_jqr_7d_before | BIGINT | column | 是否进过机器人_前7天内 |  |
| is_ivr_7d_before | BIGINT | column | 是否进过IVR_前7天内 |  |
| is_kfzx_7d_before | BIGINT | column | 是否进过客服咨询_前7天内 |  |
| is_dhib_7d_before | BIGINT | column | 是否进过贷后IB_前7天内 |  |
| is_xbrx_7d_before | BIGINT | column | 是否进过消保热线_前7天内 |  |
| is_fzqts_7d_before | BIGINT | column | 是否进过非重渠投诉_前7天内 |  |
| is_kfdt_7d_before_cnt | BIGINT | column | 进过客服大厅次数_前7天内 |  |
| is_jqr_7d_before_cnt | BIGINT | column | 进过机器人次数_前7天内 |  |
| is_ivr_7d_before_cnt | BIGINT | column | 进过IVR次数_前7天内 |  |
| is_kfzx_7d_before_cnt | BIGINT | column | 进过客服咨询次数_前7天内 |  |
| is_dhib_7d_before_cnt | BIGINT | column | 进过贷后IB次数_前7天内 |  |
| is_xbrx_7d_before_cnt | BIGINT | column | 进过消保热线次数_前7天内 |  |
| is_fzqts_7d_before_cnt | BIGINT | column | 进过非重渠投诉次数_前7天内 |  |
| is_kfdt_15d_before | BIGINT | column | 是否进过客服大厅_前15天内 |  |
| is_jqr_15d_before | BIGINT | column | 是否进过机器人_前15天内 |  |
| is_ivr_15d_before | BIGINT | column | 是否进过ivr_前15天内 |  |
| is_kfzx_15d_before | BIGINT | column | 是否进过客服咨询_前15天内 |  |
| is_dhib_15d_before | BIGINT | column | 是否进过贷后ib_前15天内 |  |
| is_xbrx_15d_before | BIGINT | column | 是否进过消保热线_前15天内 |  |
| is_fzqts_15d_before | BIGINT | column | 是否进过非重渠投诉_前15天内 |  |
| is_kfdt_15d_before_cnt | BIGINT | column | 进过客服大厅次数_前15天内 |  |
| is_jqr_15d_before_cnt | BIGINT | column | 进过机器人次数_前15天内 |  |
| is_ivr_15d_before_cnt | BIGINT | column | 进过IVR次数_前15天内 |  |
| is_kfzx_15d_before_cnt | BIGINT | column | 进过客服咨询次数_前15天内 |  |
| is_dhib_15d_before_cnt | BIGINT | column | 进过贷后IB次数_前15天内 |  |
| is_xbrx_15d_before_cnt | BIGINT | column | 进过消保热线次数_前15天内 |  |
| is_fzqts_15d_before_cnt | BIGINT | column | 进过非重渠投诉次数_前15天内 |  |
| is_kfdt_30d_before | BIGINT | column | 是否进过客服大厅_前30天内 |  |
| is_jqr_30d_before | BIGINT | column | 是否进过机器人_前30天内 |  |
| is_ivr_30d_before | BIGINT | column | 是否进过IVR_前30天内 |  |
| is_kfzx_30d_before | BIGINT | column | 是否进过客服咨询_前30天内 |  |
| is_dhib_30d_before | BIGINT | column | 是否进过贷后IB_前30天内 |  |
| is_xbrx_30d_before | BIGINT | column | 是否进过消保热线_前30天内 |  |
| is_fzqts_30d_before | BIGINT | column | 是否进过非重渠投诉_前30天内 |  |
| is_kfdt_30d_before_cnt | BIGINT | column | 进过客服大厅次数_前30天内 |  |
| is_jqr_30d_before_cnt | BIGINT | column | 进过机器人次数_前30天内 |  |
| is_ivr_30d_before_cnt | BIGINT | column | 进过IVR次数_前30天内 |  |
| is_kfzx_30d_before_cnt | BIGINT | column | 进过客服咨询次数_前30天内 |  |
| is_dhib_30d_before_cnt | BIGINT | column | 进过贷后IB次数_前30天内 |  |
| is_xbrx_30d_before_cnt | BIGINT | column | 进过消保热线次数_前30天内 |  |
| is_fzqts_30d_before_cnt | BIGINT | column | 进过非重渠投诉次数_前30天内 |  |
| gdts_cnt_all | BIGINT | column | 历史投诉次数含本次_相同手机号 |  |
| gdts_cnt_all_sy | BIGINT | column | 历史投诉次数含本次_相同手机号和一级诉因 |  |
| ddts_cnt_all | BIGINT | column | 历史投诉次数含本次_相同订单号 |  |
| ddts_cnt_all_sy | BIGINT | column | 历史投诉次数含本次_相同订单号和一级诉因 |  |
| zs_cnt_all | BIGINT | column | 投诉前历史咨询量_相同手机号 |  |
| gy_cnt_all | BIGINT | column | 投诉前历史干预处理量_相同手机号 |  |
| zj_cnt_all | BIGINT | column | 投诉前历史专家处理量_相同手机号 |  |
| gh_cnt_all | BIGINT | column | 投诉前历史关怀处理量_相同手机号 |  |
| zf_cnt_all | BIGINT | column | 投诉前历史资方非监管投诉量_相同手机号 |  |
| zfjg_cnt_all | BIGINT | column | 投诉前历史资方监管投诉量_相同手机号 |  |
| jg_cnt_all | BIGINT | column | 投诉前历史监管投诉量_相同手机号 |  |
| zs_cnt_7d | BIGINT | column | 投诉前7天咨询量_相同手机号和一级诉因 |  |
| zs_cnt_30d | BIGINT | column | 投诉前30天咨询量_相同手机号和一级诉因 |  |
| gy_cnt | BIGINT | column | 投诉前30天内干预组处理量_相同手机号和一级诉因 |  |
| zs_cnt1 | BIGINT | column | 投诉前30天咨询量_相同手机号 |  |
| zj_cnt1 | BIGINT | column | 投诉前30天内专家处理量_相同手机号 |  |
| gh_cnt1 | BIGINT | column | 投诉前30天内关怀处理量_相同手机号 |  |
| zf_cnt1 | BIGINT | column | 投诉前30天内资方非监管投诉量_相同手机号 |  |
| zfjg_cnt1 | BIGINT | column | 投诉前30天内资方监管投诉量_相同手机号 |  |
| jg_cnt1 | BIGINT | column | 投诉前30天内监管投诉量_相同手机号 |  |
| zj_cnt | BIGINT | column | 投诉前30天内专家处理量_相同手机号和一级诉因 |  |
| gh_cnt | BIGINT | column | 投诉前30天内关怀处理量_相同手机号和一级诉因 |  |
| zf_cnt | BIGINT | column | 投诉前30天内资方非监管投诉量_相同手机号和一级诉因 |  |
| zfjg_cnt | BIGINT | column | 投诉前30天内资方监管投诉量_相同手机号和一级诉因 |  |
| jg_cnt | BIGINT | column | 投诉前30天内监管投诉量_相同手机号和一级诉因 |  |
| qblj_30 | BIGINT | column | 全部累计值_投诉前30天_相同手机号_咨询量+专家处理量+关怀处理量+监管投诉量+资方非监管投诉量+资方监管投诉量 |  |
| twtljz | BIGINT | column | 同问题累计值_投诉前30天_相同手机号和一级诉因_咨询量+专家处理量+关怀处理量+监管投诉量+资方非监管投诉量+资方监管投诉量 |  |
| task_feedback_comment_all | STRING | column | 工单跟进反馈所有内容 |  |
| s_vip_order_number | STRING | column | 飞跃会员订单号 |  |
| tsll_60 | STRING | column | 投诉前链路_60天内 |  |
| tsll_90 | STRING | column | 投诉前链路_90天内 |  |
| is_kfdt_60d_before | BIGINT | column | 是否进过客服大厅_前60天内 |  |
| is_jqr_60d_before | BIGINT | column | 是否进过机器人_前60天内 |  |
| is_ivr_60d_before | BIGINT | column | 是否进过IVR_前60天内 |  |
| is_kfzx_60d_before | BIGINT | column | 是否进过客服咨询_前60天内 |  |
| is_dhib_60d_before | BIGINT | column | 是否进过贷后IB_前60天内 |  |
| is_xbrx_60d_before | BIGINT | column | 是否进过消保热线_前60天内 |  |
| is_fzqts_60d_before | BIGINT | column | 是否进过非重渠投诉_前60天内 |  |
| is_kfdt_60d_before_cnt | BIGINT | column | 进过客服大厅次数_前60天内 |  |
| is_jqr_60d_before_cnt | BIGINT | column | 进过机器人次数_前60天内 |  |
| is_ivr_60d_before_cnt | BIGINT | column | 进过IVR次数_前60天内 |  |
| is_kfzx_60d_before_cnt | BIGINT | column | 进过客服咨询次数_前60天内 |  |
| is_dhib_60d_before_cnt | BIGINT | column | 进过贷后IB次数_前60天内 |  |
| is_xbrx_60d_before_cnt | BIGINT | column | 进过消保热线次数_前60天内 |  |
| is_fzqts_60d_before_cnt | BIGINT | column | 进过非重渠投诉次数_前60天内 |  |
| is_kfdt_90d_before | BIGINT | column | 是否进过客服大厅_前90天内 |  |
| is_jqr_90d_before | BIGINT | column | 是否进过机器人_前90天内 |  |
| is_ivr_90d_before | BIGINT | column | 是否进过IVR_前90天内 |  |
| is_kfzx_90d_before | BIGINT | column | 是否进过客服咨询_前90天内 |  |
| is_dhib_90d_before | BIGINT | column | 是否进过贷后IB_前90天内 |  |
| is_xbrx_90d_before | BIGINT | column | 是否进过消保热线_前90天内 |  |
| is_fzqts_90d_before | BIGINT | column | 是否进过非重渠投诉_前90天内 |  |
| is_kfdt_90d_before_cnt | BIGINT | column | 进过客服大厅次数_前90天内 |  |
| is_jqr_90d_before_cnt | BIGINT | column | 进过机器人次数_前90天内 |  |
| is_ivr_90d_before_cnt | BIGINT | column | 进过IVR次数_前90天内 |  |
| is_kfzx_90d_before_cnt | BIGINT | column | 进过客服咨询次数_前90天内 |  |
| is_dhib_90d_before_cnt | BIGINT | column | 进过贷后IB次数_前90天内 |  |
| is_xbrx_90d_before_cnt | BIGINT | column | 进过消保热线次数_前90天内 |  |
| is_fzqts_90d_before_cnt | BIGINT | column | 进过非重渠投诉次数_前90天内 |  |
| custom_setting | STRING | column | 系统标签底层内容 |  |
| is_misreported | STRING | column | 标签_是否误投诉 |  |
| blackindustry_incall_gather | STRING | column | 黑产类型_来电聚集 |  |
| zql_before_7d | BIGINT | column | 投诉前重渠次数_前7天内 |  |
| zql_before_15d | BIGINT | column | 投诉前重渠次数_前15天内 |  |
| zql_before_30d | BIGINT | column | 投诉前重渠次数_前30天内 |  |
| zql_before_60d | BIGINT | column | 投诉前重渠次数_前60天内 |  |
| zql_before_90d | BIGINT | column | 投诉前重渠次数_前90天内 |  |
| first_follow_up_time | DATETIME | column | 首次跟进时间 |  |
| first_follow_up_comment | STRING | column | 首次跟进内容 |  |
| if_loan | STRING | column | 投诉时用户是否首贷，null则为无贷款 |  |
| fund_source | STRING | column | 资方编码 |  |
| cust_status | STRING | column | 投诉时用户维度还款状态 |  |
| pt | STRING | column | 数据日期yyyyMMdd |  |
| pt | STRING | partition | 数据日期yyyyMMdd |  |

### DDL
```sql
CREATE TABLE xyf_ads.`bi_ts_gd_wide_table_v3` (
  `month_cj` STRING COMMENT '创建月份',
  `week_cj` STRING COMMENT '创建客服周',
  `date_cj` STRING COMMENT '创建日期',
  `real_time` DATETIME COMMENT '真实投诉时间',
  `create_time` DATETIME COMMENT '创建时间',
  `distributed_time` STRING COMMENT '分配时间',
  `end_time` STRING COMMENT '结单时间',
  `task_number` STRING COMMENT '工单编号',
  `is_zq` STRING COMMENT '是否重渠',
  `channel_1_type_new` STRING COMMENT '新一级渠道',
  `channel_2_type_new` STRING COMMENT '新二级渠道',
  `task_type_name_new` STRING COMMENT '新一级诉因',
  `question_type_name_new` STRING COMMENT '新二级诉因',
  `complaint_type_new` STRING COMMENT '新三级诉因',
  `task_status` STRING COMMENT '工单状态',
  `company_name` STRING COMMENT '被诉主体',
  `comment` STRING COMMENT '投诉内容',
  `channel_1_type` STRING COMMENT '原一级渠道',
  `channel_2_type` STRING COMMENT '原二级渠道',
  `task_type_name` STRING COMMENT '原一级诉因',
  `question_type_name` STRING COMMENT '原二级诉因',
  `complaint_type` STRING COMMENT '原三级诉因',
  `create_work_number` STRING COMMENT '创建人工号',
  `create_work_name` STRING COMMENT '创建人姓名',
  `create_department` STRING COMMENT '创建人分类',
  `process_work_number` STRING COMMENT '跟进人工号',
  `process_work_name` STRING COMMENT '跟进人姓名',
  `work_department` STRING COMMENT '跟进人分类',
  `vip_order_number` STRING COMMENT '飞享会员卡订单号_原始',
  `vip_order_number_pd` STRING COMMENT '飞享会员卡订单号_填写判断',
  `vip_order_no_new` STRING COMMENT '飞享会员订单号_正则提取',
  `is_exposure` STRING COMMENT '是否曝光',
  `hm_cs` BIGINT COMMENT '黑猫历史投诉次数_含本次',
  `hm_app_name` STRING COMMENT '黑猫app划分',
  `is_yangyan` BIGINT COMMENT '是否扬言_备注或小结命中扬言关键词',
  `is_blackindustry` BIGINT COMMENT '是否命中黑产标签',
  `blackindustry_complaint_app` STRING COMMENT '黑产标签_投诉app',
  `blackindustry_wifi_gather` STRING COMMENT '黑产标签_wifi聚集',
  `blackindustry_device_gather` STRING COMMENT '黑产标签_设备聚集',
  `blackindustry_customer_annotation` STRING COMMENT '黑产标签_客服标注',
  `black_industry_level` STRING COMMENT '黑产级别',
  `is_complaint_risk` STRING COMMENT '是否高风险用户',
  `business_line_name` STRING COMMENT '业务线名称',
  `b_score` STRING COMMENT '最新b卡评分',
  `b_score_level` STRING COMMENT '最新b卡等级划分',
  `mobile` STRING COMMENT '手机号',
  `mobile_md5` STRING COMMENT '手机号md5',
  `id_card_number` STRING COMMENT '身份证号',
  `cust_no` STRING COMMENT '客户号',
  `user_no` STRING COMMENT '用户号',
  `register_utm_source` STRING COMMENT '注册utm_source',
  `mobile_utm_source` STRING COMMENT '手机utm_source',
  `user_name` STRING COMMENT '客户名称',
  `gender` STRING COMMENT '性别',
  `age` STRING COMMENT '年龄',
  `education` STRING COMMENT '学历',
  `job` STRING COMMENT '职业',
  `monthly_income` STRING COMMENT '收入',
  `province` STRING COMMENT '省份',
  `city` STRING COMMENT '城市',
  `order_number` STRING COMMENT '订单号',
  `order_number_source` STRING COMMENT '订单来源',
  `app` STRING COMMENT '订单app',
  `inner_app` STRING COMMENT '订单inner_app',
  `inner_app_name` STRING COMMENT 'inner_app名称',
  `loan_type_name` STRING COMMENT '订单首复贷',
  `fund` STRING COMMENT '资方or监管名称',
  `fund_name` STRING COMMENT '资方名称',
  `fund_jg` STRING COMMENT '资方监管名称',
  `asset_type` STRING COMMENT '费率',
  `new_asset_type` STRING COMMENT '产品类型',
  `pre_settle_time` DATETIME COMMENT '提前结清时间',
  `pre_perprid` STRING COMMENT '在哪一期提前结清',
  `settle_date` DATETIME COMMENT '订单结清时间',
  `end_date` DATETIME COMMENT '贷款最后一期还款日期',
  `settle_date_pd` STRING COMMENT '结清时间判断',
  `loan_time` DATETIME COMMENT '订单放款时间',
  `date_fk` DATETIME COMMENT '订单放款日期',
  `week_fk` STRING COMMENT '订单放款客服周',
  `month_fk` STRING COMMENT '订单放款月份',
  `order_month` BIGINT COMMENT '投诉间隔月_投诉月减放款月',
  `last_repay_time` DATETIME COMMENT '投诉时用户最后一次还款时间',
  `overdue_zl_tss` STRING COMMENT '投诉时账龄',
  `repay_status_tss` STRING COMMENT '投诉时订单状态',
  `repay_status_after30d` STRING COMMENT '投诉后第30天订单状态',
  `overdue_m_tss` STRING COMMENT '投诉时逾期阶段',
  `overdue_days_tss` BIGINT COMMENT '投诉时逾期天数',
  `period` BIGINT COMMENT '贷款总期数',
  `loan_amt` DECIMAL(38,18) COMMENT '贷款金额元',
  `loan_amt_fb` STRING COMMENT '贷款金额分布',
  `case_id` BIGINT COMMENT '案件id',
  `case_code` STRING COMMENT '案件号',
  `dept_name` STRING COMMENT '诉时机构',
  `over_due_days` BIGINT COMMENT '逾期天数',
  `coll_stage` STRING COMMENT '诉时队列',
  `in_agssin_over_due_days` INT COMMENT '诉时入催天数',
  `zhongqu_score` STRING COMMENT '当日重渠分',
  `zhongqu_score_max_7d` STRING COMMENT '近7天重渠分最大值',
  `zhongqu_score_max_30d` STRING COMMENT '近30天重渠分最大值',
  `is_zqts_7d_after` BIGINT COMMENT '投诉后7天内是否重渠投诉',
  `is_zqts_15d_after` BIGINT COMMENT '投诉后15天内是否重渠投诉',
  `is_zqts_30d_after` BIGINT COMMENT '投诉后30天内是否重渠投诉',
  `zqcs_7d` BIGINT COMMENT '投诉后7天内重渠次数_创建时间',
  `zqcs_15d` BIGINT COMMENT '投诉后15天内重渠次数_创建时间',
  `zqcs_30d` BIGINT COMMENT '投诉后30天内重渠次数_创建时间',
  `create_time_zq_15d` DATETIME COMMENT '创建时间_15天内首次重渠',
  `task_number_15d` STRING COMMENT '工单号_15天内首次重渠',
  `order_number_15d` STRING COMMENT '订单号_15天内首次重渠',
  `channel_1_type_zq_15d` STRING COMMENT '新一级渠道_15天内首次重渠',
  `channel_2_type_15d` STRING COMMENT '新二级渠道_15天内首次重渠',
  `task_type_name_15d` STRING COMMENT '新一级诉因_15天内首次重渠',
  `question_type_name_15d` STRING COMMENT '新二级诉因_15天内首次重渠',
  `complaint_type_15d` STRING COMMENT '新三级诉因_15天内首次重渠',
  `comment_15d` STRING COMMENT '投诉内容_15天内首次重渠',
  `create_work_number_15d` STRING COMMENT '创建人工号_15天内首次重渠',
  `create_work_name_15d` STRING COMMENT '创建人姓名_15天内首次重渠',
  `create_department_15d` STRING COMMENT '创建人分类_15天内首次重渠',
  `process_work_number_15d` STRING COMMENT '跟进人工号_15天内首次重渠',
  `process_work_name_15d` STRING COMMENT '跟进人姓名_15天内首次重渠',
  `work_department_15d` STRING COMMENT '跟进人分类_15天内首次重渠',
  `create_time_zq_30d` DATETIME COMMENT '创建时间_30天内首次重渠',
  `task_number_30d` STRING COMMENT '工单号_30天内首次重渠',
  `order_number_30d` STRING COMMENT '订单号_30天内首次重渠',
  `channel_1_type_zq_30d` STRING COMMENT '新一级渠道_30天内首次重渠',
  `channel_2_type_30d` STRING COMMENT '新二级渠道_30天内首次重渠',
  `task_type_name_30d` STRING COMMENT '新一级诉因_30天内首次重渠',
  `question_type_name_30d` STRING COMMENT '新二级诉因_30天内首次重渠',
  `complaint_type_30d` STRING COMMENT '新三级诉因_30天内首次重渠',
  `comment_30d` STRING COMMENT '投诉内容_30天内首次重渠',
  `create_work_number_30d` STRING COMMENT '创建人工号_30天内首次重渠',
  `create_work_name_30d` STRING COMMENT '创建人姓名_30天内首次重渠',
  `create_department_30d` STRING COMMENT '创建人分类_30天内首次重渠',
  `process_work_number_30d` STRING COMMENT '跟进人工号_30天内首次重渠',
  `process_work_name_30d` STRING COMMENT '跟进人姓名_30天内首次重渠',
  `work_department_30d` STRING COMMENT '跟进人分类_30天内首次重渠',
  `tsll_7` STRING COMMENT '投诉前链路_7天内',
  `tsll_15` STRING COMMENT '投诉前链路_15天内',
  `tsll_30` STRING COMMENT '投诉前链路_30天内',
  `is_kfdt_7d_before` BIGINT COMMENT '是否进过客服大厅_前7天内',
  `is_jqr_7d_before` BIGINT COMMENT '是否进过机器人_前7天内',
  `is_ivr_7d_before` BIGINT COMMENT '是否进过IVR_前7天内',
  `is_kfzx_7d_before` BIGINT COMMENT '是否进过客服咨询_前7天内',
  `is_dhib_7d_before` BIGINT COMMENT '是否进过贷后IB_前7天内',
  `is_xbrx_7d_before` BIGINT COMMENT '是否进过消保热线_前7天内',
  `is_fzqts_7d_before` BIGINT COMMENT '是否进过非重渠投诉_前7天内',
  `is_kfdt_7d_before_cnt` BIGINT COMMENT '进过客服大厅次数_前7天内',
  `is_jqr_7d_before_cnt` BIGINT COMMENT '进过机器人次数_前7天内',
  `is_ivr_7d_before_cnt` BIGINT COMMENT '进过IVR次数_前7天内',
  `is_kfzx_7d_before_cnt` BIGINT COMMENT '进过客服咨询次数_前7天内',
  `is_dhib_7d_before_cnt` BIGINT COMMENT '进过贷后IB次数_前7天内',
  `is_xbrx_7d_before_cnt` BIGINT COMMENT '进过消保热线次数_前7天内',
  `is_fzqts_7d_before_cnt` BIGINT COMMENT '进过非重渠投诉次数_前7天内',
  `is_kfdt_15d_before` BIGINT COMMENT '是否进过客服大厅_前15天内',
  `is_jqr_15d_before` BIGINT COMMENT '是否进过机器人_前15天内',
  `is_ivr_15d_before` BIGINT COMMENT '是否进过ivr_前15天内',
  `is_kfzx_15d_before` BIGINT COMMENT '是否进过客服咨询_前15天内',
  `is_dhib_15d_before` BIGINT COMMENT '是否进过贷后ib_前15天内',
  `is_xbrx_15d_before` BIGINT COMMENT '是否进过消保热线_前15天内',
  `is_fzqts_15d_before` BIGINT COMMENT '是否进过非重渠投诉_前15天内',
  `is_kfdt_15d_before_cnt` BIGINT COMMENT '进过客服大厅次数_前15天内',
  `is_jqr_15d_before_cnt` BIGINT COMMENT '进过机器人次数_前15天内',
  `is_ivr_15d_before_cnt` BIGINT COMMENT '进过IVR次数_前15天内',
  `is_kfzx_15d_before_cnt` BIGINT COMMENT '进过客服咨询次数_前15天内',
  `is_dhib_15d_before_cnt` BIGINT COMMENT '进过贷后IB次数_前15天内',
  `is_xbrx_15d_before_cnt` BIGINT COMMENT '进过消保热线次数_前15天内',
  `is_fzqts_15d_before_cnt` BIGINT COMMENT '进过非重渠投诉次数_前15天内',
  `is_kfdt_30d_before` BIGINT COMMENT '是否进过客服大厅_前30天内',
  `is_jqr_30d_before` BIGINT COMMENT '是否进过机器人_前30天内',
  `is_ivr_30d_before` BIGINT COMMENT '是否进过IVR_前30天内',
  `is_kfzx_30d_before` BIGINT COMMENT '是否进过客服咨询_前30天内',
  `is_dhib_30d_before` BIGINT COMMENT '是否进过贷后IB_前30天内',
  `is_xbrx_30d_before` BIGINT COMMENT '是否进过消保热线_前30天内',
  `is_fzqts_30d_before` BIGINT COMMENT '是否进过非重渠投诉_前30天内',
  `is_kfdt_30d_before_cnt` BIGINT COMMENT '进过客服大厅次数_前30天内',
  `is_jqr_30d_before_cnt` BIGINT COMMENT '进过机器人次数_前30天内',
  `is_ivr_30d_before_cnt` BIGINT COMMENT '进过IVR次数_前30天内',
  `is_kfzx_30d_before_cnt` BIGINT COMMENT '进过客服咨询次数_前30天内',
  `is_dhib_30d_before_cnt` BIGINT COMMENT '进过贷后IB次数_前30天内',
  `is_xbrx_30d_before_cnt` BIGINT COMMENT '进过消保热线次数_前30天内',
  `is_fzqts_30d_before_cnt` BIGINT COMMENT '进过非重渠投诉次数_前30天内',
  `gdts_cnt_all` BIGINT COMMENT '历史投诉次数含本次_相同手机号',
  `gdts_cnt_all_sy` BIGINT COMMENT '历史投诉次数含本次_相同手机号和一级诉因',
  `ddts_cnt_all` BIGINT COMMENT '历史投诉次数含本次_相同订单号',
  `ddts_cnt_all_sy` BIGINT COMMENT '历史投诉次数含本次_相同订单号和一级诉因',
  `zs_cnt_all` BIGINT COMMENT '投诉前历史咨询量_相同手机号',
  `gy_cnt_all` BIGINT COMMENT '投诉前历史干预处理量_相同手机号',
  `zj_cnt_all` BIGINT COMMENT '投诉前历史专家处理量_相同手机号',
  `gh_cnt_all` BIGINT COMMENT '投诉前历史关怀处理量_相同手机号',
  `zf_cnt_all` BIGINT COMMENT '投诉前历史资方非监管投诉量_相同手机号',
  `zfjg_cnt_all` BIGINT COMMENT '投诉前历史资方监管投诉量_相同手机号',
  `jg_cnt_all` BIGINT COMMENT '投诉前历史监管投诉量_相同手机号',
  `zs_cnt_7d` BIGINT COMMENT '投诉前7天咨询量_相同手机号和一级诉因',
  `zs_cnt_30d` BIGINT COMMENT '投诉前30天咨询量_相同手机号和一级诉因',
  `gy_cnt` BIGINT COMMENT '投诉前30天内干预组处理量_相同手机号和一级诉因',
  `zs_cnt1` BIGINT COMMENT '投诉前30天咨询量_相同手机号',
  `zj_cnt1` BIGINT COMMENT '投诉前30天内专家处理量_相同手机号',
  `gh_cnt1` BIGINT COMMENT '投诉前30天内关怀处理量_相同手机号',
  `zf_cnt1` BIGINT COMMENT '投诉前30天内资方非监管投诉量_相同手机号',
  `zfjg_cnt1` BIGINT COMMENT '投诉前30天内资方监管投诉量_相同手机号',
  `jg_cnt1` BIGINT COMMENT '投诉前30天内监管投诉量_相同手机号',
  `zj_cnt` BIGINT COMMENT '投诉前30天内专家处理量_相同手机号和一级诉因',
  `gh_cnt` BIGINT COMMENT '投诉前30天内关怀处理量_相同手机号和一级诉因',
  `zf_cnt` BIGINT COMMENT '投诉前30天内资方非监管投诉量_相同手机号和一级诉因',
  `zfjg_cnt` BIGINT COMMENT '投诉前30天内资方监管投诉量_相同手机号和一级诉因',
  `jg_cnt` BIGINT COMMENT '投诉前30天内监管投诉量_相同手机号和一级诉因',
  `qblj_30` BIGINT COMMENT '全部累计值_投诉前30天_相同手机号_咨询量+专家处理量+关怀处理量+监管投诉量+资方非监管投诉量+资方监管投诉量',
  `twtljz` BIGINT COMMENT '同问题累计值_投诉前30天_相同手机号和一级诉因_咨询量+专家处理量+关怀处理量+监管投诉量+资方非监管投诉量+资方监管投诉量',
  `task_feedback_comment_all` STRING COMMENT '工单跟进反馈所有内容',
  `s_vip_order_number` STRING COMMENT '飞跃会员订单号',
  `tsll_60` STRING COMMENT '投诉前链路_60天内',
  `tsll_90` STRING COMMENT '投诉前链路_90天内',
  `is_kfdt_60d_before` BIGINT COMMENT '是否进过客服大厅_前60天内',
  `is_jqr_60d_before` BIGINT COMMENT '是否进过机器人_前60天内',
  `is_ivr_60d_before` BIGINT COMMENT '是否进过IVR_前60天内',
  `is_kfzx_60d_before` BIGINT COMMENT '是否进过客服咨询_前60天内',
  `is_dhib_60d_before` BIGINT COMMENT '是否进过贷后IB_前60天内',
  `is_xbrx_60d_before` BIGINT COMMENT '是否进过消保热线_前60天内',
  `is_fzqts_60d_before` BIGINT COMMENT '是否进过非重渠投诉_前60天内',
  `is_kfdt_60d_before_cnt` BIGINT COMMENT '进过客服大厅次数_前60天内',
  `is_jqr_60d_before_cnt` BIGINT COMMENT '进过机器人次数_前60天内',
  `is_ivr_60d_before_cnt` BIGINT COMMENT '进过IVR次数_前60天内',
  `is_kfzx_60d_before_cnt` BIGINT COMMENT '进过客服咨询次数_前60天内',
  `is_dhib_60d_before_cnt` BIGINT COMMENT '进过贷后IB次数_前60天内',
  `is_xbrx_60d_before_cnt` BIGINT COMMENT '进过消保热线次数_前60天内',
  `is_fzqts_60d_before_cnt` BIGINT COMMENT '进过非重渠投诉次数_前60天内',
  `is_kfdt_90d_before` BIGINT COMMENT '是否进过客服大厅_前90天内',
  `is_jqr_90d_before` BIGINT COMMENT '是否进过机器人_前90天内',
  `is_ivr_90d_before` BIGINT COMMENT '是否进过IVR_前90天内',
  `is_kfzx_90d_before` BIGINT COMMENT '是否进过客服咨询_前90天内',
  `is_dhib_90d_before` BIGINT COMMENT '是否进过贷后IB_前90天内',
  `is_xbrx_90d_before` BIGINT COMMENT '是否进过消保热线_前90天内',
  `is_fzqts_90d_before` BIGINT COMMENT '是否进过非重渠投诉_前90天内',
  `is_kfdt_90d_before_cnt` BIGINT COMMENT '进过客服大厅次数_前90天内',
  `is_jqr_90d_before_cnt` BIGINT COMMENT '进过机器人次数_前90天内',
  `is_ivr_90d_before_cnt` BIGINT COMMENT '进过IVR次数_前90天内',
  `is_kfzx_90d_before_cnt` BIGINT COMMENT '进过客服咨询次数_前90天内',
  `is_dhib_90d_before_cnt` BIGINT COMMENT '进过贷后IB次数_前90天内',
  `is_xbrx_90d_before_cnt` BIGINT COMMENT '进过消保热线次数_前90天内',
  `is_fzqts_90d_before_cnt` BIGINT COMMENT '进过非重渠投诉次数_前90天内',
  `custom_setting` STRING COMMENT '系统标签底层内容',
  `is_misreported` STRING COMMENT '标签_是否误投诉',
  `blackindustry_incall_gather` STRING COMMENT '黑产类型_来电聚集',
  `zql_before_7d` BIGINT COMMENT '投诉前重渠次数_前7天内',
  `zql_before_15d` BIGINT COMMENT '投诉前重渠次数_前15天内',
  `zql_before_30d` BIGINT COMMENT '投诉前重渠次数_前30天内',
  `zql_before_60d` BIGINT COMMENT '投诉前重渠次数_前60天内',
  `zql_before_90d` BIGINT COMMENT '投诉前重渠次数_前90天内',
  `first_follow_up_time` DATETIME COMMENT '首次跟进时间',
  `first_follow_up_comment` STRING COMMENT '首次跟进内容',
  `if_loan` STRING COMMENT '投诉时用户是否首贷，null则为无贷款',
  `fund_source` STRING COMMENT '资方编码',
  `cust_status` STRING COMMENT '投诉时用户维度还款状态'
)
COMMENT '投诉工单宽表_v3版本'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '数据日期yyyyMMdd'
)
STORED AS AliOrc
```

## 抽样数据
- 未采样

## 同步来源
- `odps`

## 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69CE5D8D32E7470E5AD40C0E Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
