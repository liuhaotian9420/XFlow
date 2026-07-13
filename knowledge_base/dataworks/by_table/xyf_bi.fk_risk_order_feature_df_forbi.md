# xyf_bi.fk_risk_order_feature_df_forbi

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | 订单号 |  |
| user_no | BIGINT | column | 用户号cis系统 app+mobile |  |
| acct_no | STRING | column | 账户号 |  |
| cust_no | STRING | column | 客户号 |  |
| ori_order_number | STRING | column | 用户订单号 |  |
| biz_flow_number | STRING | column | 业务流水号 |  |
| apply_cust_product_no | BIGINT | column | 用户申请次数(cust_no+产品类型) |  |
| apply_cust_app_no | BIGINT | column | 用户申请次数(cust_no+app) |  |
| loan_amt | DECIMAL(38,18) | column | 借款金额:元 |  |
| period | BIGINT | column | 期数 |  |
| product_type | STRING | column | 产品代码:cash_loan/personal_loan |  |
| fund_source | STRING | column | 资方 |  |
| status_code | STRING | column | 借据申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝,99-其它 |  |
| status | STRING | column | 借据申请状态解释 |  |
| date_cash | DATETIME | column | 资金到账日期 |  |
| risk_status | STRING | column | 风控状态 |  |
| id_card_number | STRING | column | 身份证 |  |
| date_created | DATETIME | column | 订单申请时间 |  |
| main_biz_flow_number | STRING | column | 主订单业务流水号 |  |
| system | BIGINT | column | 系统来源,0:老,1:新 |  |
| app | STRING | column | app |  |
| inner_app | STRING | column | 资金动用渠道 |  |
| cnl_pd_code | STRING | column | 端产品码 |  |
| push_fundsys_time | DATETIME | column | 推到资金系统时间 |  |
| fund_apply_time | DATETIME | column | 资方授信申请时间 |  |
| fund_query_time | DATETIME | column | 资方授信查询时间 |  |
| fund_loan_time | DATETIME | column | 支用申请时间 |  |
| fund_loan_query_time | DATETIME | column | 支用查询时间 |  |
| fund_loan_success_time | DATETIME | column | 资方通知放款成功时间 |  |
| fund_repay_plan_query_time | DATETIME | column | 资方还款计划查询时间 |  |
| fund_upload_file_time | DATETIME | column | 活体/影像件/个人征信信息查询及使用授权书时间 |  |
| fund_contract_time | DATETIME | column | 委托保证合同/担保咨询服务合同时间  |  |
| source | STRING | column | 下单来源 |  |
| device_id | STRING | column | 设备id |  |
| created_ip | STRING | column | 创单ip |  |
| risk_first_success_time | DATETIME | column | 用户申请后第一次风控通过时间 |  |
| main_date_created | DATETIME | column | 用户申请时间 |  |
| first_push_fundsys_time | DATETIME | column | 首次推到资金系统时间 |  |
| third_code | STRING | column | 第三方编码 |  |
| main_status_code | STRING | column | 主订单申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝 |  |
| risk_price | STRING | column | 真实定价（历史数据只保留A24） |  |
| fund_source_new | STRING | column | 资方(新系统标准) |  |
| mobile | STRING | column | 手机号 |  |
| utm_source | STRING | column | 提现utm_source |  |
| failed_code | STRING | column | 失败code |  |
| failed_reason | STRING | column | 失败原因 |  |
| first_biz_flow_number | STRING | column | 用户本次申请首次进决策系统 |  |
| pay_date | STRING | column | 资金到账日期，yyyymmdd |  |
| crt_date | STRING | column | 动支日期，yyyymmdd |  |
| scene | STRING | column | 场景，API/APP |  |
| join_biz_flow_number | STRING | column | 关联决策引擎流水号 |  |
| 首复贷 | STRING | column | [AI推测] 首贷/复贷标识 |  |
| qudao3 | STRING | column | 动支渠道 |  |
| qudao_second | STRING | column | 动支二级渠道 |  |
| phone_number_prefix | STRING | column | 手机号前三位 |  |
| phone_number_city_rank | STRING | column | 手机号归属地几线城市 |  |
| monthly_income | STRING | column | 月收入 |  |
| education | STRING | column | 学历 |  |
| gender | BIGINT | column | 性别 |  |
| age | BIGINT | column | 年龄 |  |
| race | STRING | column | 民族 |  |
| xinyan_1 | DOUBLE | column | 最近90天代扣失败订单数占总订单数的比值下限 |  |
| id_number_province | STRING | column | 身份证归属地_省 |  |
| id_number_city | STRING | column | 身份证归属地_市 |  |
| id_number_district | STRING | column | 身份证归属地_区县 |  |
| phone_number_province | STRING | column | 手机号归属地_省 |  |
| phone_number_city | STRING | column | 手机号归属地_市 |  |
| phone_number_isp | STRING | column | 运营商 |  |
| ip_province | STRING | column | IP地址归属地_省 |  |
| ip_city | STRING | column | IP地址归属地_市 |  |
| job | STRING | column | 职业 |  |
| company | STRING | column | 公司 |  |
| title | STRING | column | 职位 |  |
| company_address_province | STRING | column | 单位地址_省 |  |
| company_address_city | STRING | column | 单位地址_市 |  |
| company_address_district | STRING | column | 单位地址_区县 |  |
| company_address | STRING | column | 单位地址 |  |
| residence_province | STRING | column | 居住地_省 |  |
| residence_city | STRING | column | 居住地_市 |  |
| residence_district | STRING | column | 居住地_区县 |  |
| marital_status | STRING | column | 婚姻状况 |  |
| id_number_city_rank | STRING | column | 身份证归属地几线城市 |  |
| expect_loan_period | STRING | column | 借款意向期限 |  |
| expect_loan_amount | STRING | column | 借款意向金额 |  |
| has_car | STRING | column | 是否有车 |  |
| has_house | STRING | column | 是否有房 |  |
| house_type_status | STRING | column | 有房状态，房子类型： 0:未知 1:自购房，有按揭 2:自购房，无按揭 3:无房，租房 4:无房，集体宿舍 5:无房，与父母共住 9:其他 |  |
| work_seniority | STRING | column | 工作年限： 1 {3年以下} 2 {3-4年} 3 {5-7年} 4 {8-9年} 5 {10-14年} 6 {15-20年} * 7 {20年以上} |  |
| house_price | STRING | column | 购房总额: 1 {未购房} 2 {1-50万元} 3 {51-100万元} 4 {101-200万元} 5 {201-300万元} 6 {301-500万元} 7 {501-1000万元} 8 {1000万以上} |  |
| car_price | STRING | column | 购车总额: 1 {未购车} 2 {3万以下} 3 {3-5万} 4 {6-10万} 5 {11-20万} 6 {21-50万} 7 {51-100万} 8 {101万以上} |  |
| tengxun_customize_score_v2 | DOUBLE | column | 腾讯反欺诈风险评估分 |  |
| volcano_customize_score | DOUBLE | column | 火山定制模型17207分 |  |
| personalloan_sd_6mceng30_nozy_lgb_rh_v2_score | DOUBLE | column | 个人分期首贷6期30+无中原征信模型lgb版v2模型分 |  |
| personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob | DOUBLE | column | 个人分期首贷6期30+无中原征信模型lgb版v2概率分 |  |
| personalloan_sd_3mceng30_xfzx_rh_fix_v2_score | DOUBLE | column | 个人分期首贷3mceng30_新版征信_人行子分V2_score |  |
| personalloan_sd_3mceng30_xfzx_rh_fix_v2_prob | DOUBLE | column | 个人分期首贷3mceng30_新版征信_人行子分V2_prob |  |
| code | STRING | column | 百融return_data反馈码 |  |
| bairong_als_274 | DOUBLE | column | 近1个月在非银机构申请机构数 |  |
| bairong_als_402 | DOUBLE | column | 近3个月在非银机构申请机构数 |  |
| bairong_als_554 | DOUBLE | column | 近6个月在非银机构申请机构数 |  |
| bairong_als_code | STRING | column | 百融多头空值code |  |
| bairong_rongzhiscore_3 | DOUBLE | column | 百融评分积极指数 |  |
| ym_xf_customize_score | DOUBLE | column | 友盟信飞定制模型2301 |  |
| hj_3y_xfnl_1 | BIGINT | column | 航聚-金额下线 |  |
| bd_general_fraudc_v3 | DOUBLE | column | 度小满欺诈因子 |  |
| hujin_credit_7 | DOUBLE | column | 当前违约账户数 |  |
| hujin_credit_8 | DOUBLE | column | 当前违约金额 |  |
| hujin_credit_9 | DOUBLE | column | 当前不良账户数 |  |
| hujin_credit_10 | DOUBLE | column | 当前不良额 |  |
| xinyan_1_特征加工版 | DOUBLE | column | 最近90天代扣失败订单数占总订单数的比值下限 |  |
| huarong2_1 | DOUBLE | column | 人行学历 |  |
| huarong2_3 | DOUBLE | column | 最早信用记录距今月数 |  |
| huarong2_10 | DOUBLE | column | 个人住房贷款总合同金额 |  |
| huarong2_11 | DOUBLE | column | 个人住房贷款已还款期数 |  |
| huarong2_13 | DOUBLE | column | 所有账户当前逾期金额 |  |
| huarong2_15 | DOUBLE | column | 所有账户最近24个月累计逾期次数 |  |
| huarong2_17 | DOUBLE | column | 所有账户最新表现还款状态 |  |
| huarong2_20 | DOUBLE | column | 贷记卡最高额度 |  |
| huarong2_24 | DOUBLE | column | 人行婚姻 |  |
| huarong2_25 | DOUBLE | column | 人行职业 |  |
| huarong2_41 | DOUBLE | column | 最近1个月本人查询次数 |  |
| huarong2_100 | DOUBLE | column | 结清房贷笔数 |  |
| huarong2_145 | DOUBLE | column | 所有账户近6个月平均应还款金额 |  |
| huarong2_176 | DOUBLE | column | 非循环贷本月应还款金额总和 |  |
| huarong2_192 | DOUBLE | column | 非循环贷个人住房贷款+个人商用住房贷款本月应还款金额总和 |  |
| huarong2_238 | DOUBLE | column | 循环额度下分账户本月应还款金额总和 |  |
| huarong2_260 | DOUBLE | column | 循环贷本月应还款金额总和 |  |
| huarong2_281 | DOUBLE | column | 贷记卡最近月度本月应还金额总和 |  |
| huarong2_294 | DOUBLE | column | 贷记卡最近6个月平均使用额度 |  |
| huarong2_356 | DOUBLE | column | 所有账户当前正常汽车贷款余额总和 |  |
| huarong2_337 | DOUBLE | column | 当前贷款最大逾期期数 |  |
| huarong2_345 | DOUBLE | column | 所有账户最近6个月累计逾期次数 |  |
| huarong2_346 | DOUBLE | column | 所有账户最近12个月累计逾期次数 |  |
| huarong2_347 | DOUBLE | column | 所有账户最近5年累计逾期次数 |  |
| huarong2_338 | DOUBLE | column | 当前贷款最大逾期金额 |  |
| huarong2_340 | DOUBLE | column | 所有账户最近6个月最大逾期次数 |  |
| huarong2_341 | DOUBLE | column | 所有账户最近12个月最大逾期次数 |  |
| huarong2_342 | DOUBLE | column | 所有账户最近24个月最大逾期次数 |  |
| huarong2_343 | DOUBLE | column | 所有账户最近5年最大逾期次数 |  |
| huarong3_136 | DOUBLE | column | 缴存状态且最近参缴公积金的月缴存额 |  |
| huarong5_1336 | DOUBLE | column | 最近3个月贷款正常状态合计月份数(当前未结清) |  |
| huarong5_1337 | DOUBLE | column | 最近12个月贷款正常状态合计月份数(当前未结清) |  |
| huarong5_1338 | DOUBLE | column | 最近24个月贷款正常状态合计月份数(当前未结清) |  |
| huarong5_1087 | DOUBLE | column | 一年内贷款已结清状态贷款金额 |  |
| huarong5_309 | DOUBLE | column | 发放时间在12个月内非循环贷已结清状态贷款金额 |  |
| huarong6_38 | DOUBLE | column | 最近3个月正常状态信用卡合计月份数(历史还款) |  |
| huarong6_39 | DOUBLE | column | 最近12个月正常状态信用卡合计月份数(历史还款) |  |
| huarong6_40 | DOUBLE | column | 最近24个月正常状态信用卡合计月份数(历史还款) |  |
| huarong7_103 | DOUBLE | column | 汽车贷款的最大授信金额 |  |
| device_system | STRING | column | 手机系统 |  |
| tongdun_3 | BIGINT | column | 近7天的一般消费分期平台申请平台数 |  |
| tongdun_4 | BIGINT | column | 近7天的P2P网贷申请平台数 |  |
| tongdun_5 | BIGINT | column | 近7天的大型消费金融公司申请平台数 |  |
| tongdun_7 | BIGINT | column | 近7天的小额贷款公司申请平台数 |  |
| tongdun_12 | BIGINT | column | 近1个月的一般消费分期平台申请平台数 |  |
| tongdun_13 | BIGINT | column | 近1个月的P2P网贷申请平台数 |  |
| tongdun_14 | BIGINT | column | 近1个月的大型消费金融公司申请平台数 |  |
| tongdun_16 | BIGINT | column | 近1个月的小额贷款公司申请平台数 |  |
| tongdun_21 | BIGINT | column | 近3个月的一般消费分期平台申请平台数 |  |
| tongdun_22 | BIGINT | column | 近3个月的P2P网贷申请平台数 |  |
| tongdun_23 | BIGINT | column | 近3个月的大型消费金融公司申请平台数 |  |
| tongdun_25 | BIGINT | column | 近3个月的小额贷款公司申请平台数 |  |
| tongdun_34 | BIGINT | column | 近6个月的小额贷款公司申请平台数 |  |
| tongdun_43 | BIGINT | column | 近12个月的小额贷款公司申请平台数 |  |
| rh_debt_all | DOUBLE | column |  人行月负债_最全 |  |
| rh_debt_with_half_houseloan | DOUBLE | column |  人行月负债_360定义 |  |
| rh_debt_without_houseloan | DOUBLE | column |  人行月负债_不含房贷 |  |
| rh_overdueamt_now | DOUBLE | column |  贷款当前逾期总额 |  |
| rh_overdue_times_6p | DOUBLE | column |  贷款近6期逾期次数 |  |
| rh_overdue_times_24p | DOUBLE | column |  贷款近24期逾期次数 |  |
| rh_overdue_times_12p | DOUBLE | column |  贷款近12期逾期次数 |  |
| rh_need_pay_6m | DOUBLE | column |  贷款最近6个月平均应还款 |  |
| rh_applytimes_debt_card_1m | DOUBLE | column |  近1个月贷记卡审批查询次数与近1个月贷款审批查询次数之和 |  |
| rh_applytimes_debt_card_3m | DOUBLE | column |  近3个月贷记卡审批查询次数与近3个月贷款审批查询次数之和 |  |
| rh_applytimes_debt_card_6m | DOUBLE | column |  近6个月贷记卡审批查询次数与近6个月贷款审批查询次数之和 |  |
| tongdun_273 | DOUBLE | column | 近7天资产转让平台申请数 |  |
| tongdun_278 | DOUBLE | column | 近7天企业主所有平台申请数 |  |
| tongdun_309 | DOUBLE | column | 近1个月企业主所有平台申请数 |  |
| tongdun_340 | DOUBLE | column | 近3个月企业主所有平台申请数 |  |
| tongdun_371 | DOUBLE | column | 近6个月企业主所有平台申请数 |  |
| tongdun_402 | DOUBLE | column | 近12个月企业主所有平台申请数 |  |
| tongdun_363 | DOUBLE | column |  近6个月融资租赁平台申请数 |  |
| td_90d_mobile_abnomal_device_freq | DOUBLE | column | 90天手机号所属设备异常频次，手机号关联设备号二度关联到的90天内全行业下所有事件中设备越狱、厂商位置、安卓模拟器、疑似刷机、疑似模拟定位、多开设备的频次 |  |
| td_30d_idcard_abnomal_device_freq | DOUBLE | column | 30天身份证所属设备异常频次，身份证关联设备号二度关联到的30天内全行业下所有事件中检测到改机工具、脚本版本过期、模拟定位的设备频次 |  |
| td_30d_idcard_abnomal_device_cnt | DOUBLE | column | 30天身份证所属设备异常去重设备数，身份证关联设备号二度关联到的30天内全行业下所有事件中检测到改机工具、版本过期、模拟定位的去重设备个数 |  |
| td_idcard_owing_taxs | DOUBLE | column | 身份证或身份证关联企业是否命中欠税 |  |
| td_idcard_court_dishonesty | INT | column | 身份证是否命中法院失信(案件状态为失信或终本)，或被执行 |  |
| td_idcard_or_mobile_related_risk | INT | column | 手机号或身份证是否命中关联风险(关联来源为非入参身份证或手机号) |  |
| td_mobile_fake | DOUBLE | column | 手机号是否命中疑似虚假号码 |  |
| td_idcard_car_rental_default | DOUBLE | column | 身份证是否命中汽车租赁违约 |  |
| 百融积极收入区间 | STRING | column | [AI推测] 百融数据-积极收入区间 |  |
| 性别 | STRING | column | [AI推测] 性别（M/F） |  |
| 年龄 | BIGINT | column | [AI推测] 年龄 |  |
| 年龄分组 | STRING | column | [AI推测] 年龄分组 |  |
| 自填学历 | STRING | column | [AI推测] 用户自填学历 |  |
| 自填收入 | STRING | column | [AI推测] 用户自填月收入 |  |
| 学历分 | BIGINT | column | [AI推测] 学历评分 |  |
| 收入分 | BIGINT | column | [AI推测] 收入评分 |  |
| 自填婚姻状况 | STRING | column | [AI推测] 用户自填婚姻状况 |  |
| 自填职业 | STRING | column | [AI推测] 用户自填职业 |  |
| 身份证归属地几线城市 | STRING | column | [AI推测] 身份证归属地城市等级 |  |
| 身份证归属地_省 | STRING | column | [AI推测] 身份证归属地省份 |  |
| 系统 | STRING | column | [AI推测] 系统来源（新/老） |  |
| 公积金在缴月缴存额 | DOUBLE | column | [AI推测] 征信-公积金在缴月缴存额 |  |
| 公积金在缴月缴存额_grp | STRING | column | [AI推测] 公积金在缴月缴存额分组 |  |
| 贷记卡账户数 | DOUBLE | column | [AI推测] 征信-贷记卡账户数 |  |
| 最近还款贷记卡开立日期距今天数 | DOUBLE | column | [AI推测] 征信-最近还款贷记卡开立日期距今天数 |  |
| 贷记卡最高授信额度 | DOUBLE | column | [AI推测] 征信-贷记卡最高授信额度 |  |
| 贷记卡平均授信额度 | DOUBLE | column | [AI推测] 征信-贷记卡平均授信额度 |  |
| 房贷本月应还款总额 | DOUBLE | column | [AI推测] 征信-房贷本月应还款总额 |  |
| 房贷已还款期数 | DOUBLE | column | [AI推测] 征信-房贷已还款期数 |  |
| 最早信用记录距今月数 | DOUBLE | column | [AI推测] 征信-最早信用记录距今月数 |  |
| 房贷金额 | DOUBLE | column | [AI推测] 征信-房贷金额 |  |
| 结清房贷笔数 | DOUBLE | column | [AI推测] 征信-已结清房贷笔数 |  |
| 公积金缴交基数 | DOUBLE | column | [AI推测] 征信-公积金缴交基数 |  |
| 企业担保金额 | DOUBLE | column | [AI推测] 征信-企业担保金额 |  |
| 信用卡额度使用率 | DOUBLE | column | [AI推测] 征信-信用卡额度使用率 |  |
| 汽车贷款的最大授信金额 | DOUBLE | column | [AI推测] 征信-汽车贷款最大授信金额 |  |
| 一年内非循环贷已结清状态贷款金额 | DOUBLE | column | [AI推测] 征信-一年内非循环贷已结清贷款金额 |  |
| 个人经营贷款正常状态最大授信金额 | DOUBLE | column | [AI推测] 征信-个人经营贷正常状态最大授信金额 |  |
| 一年内贷款已结清状态贷款金额 | DOUBLE | column | [AI推测] 征信-一年内已结清贷款金额 |  |
| 呆账账户数 | DOUBLE | column | [AI推测] 征信-呆账账户数 |  |
| 贷记卡当前逾期金额 | DOUBLE | column | [AI推测] 征信-贷记卡当前逾期金额 |  |
| 当前贷款最大逾期金额 | DOUBLE | column | [AI推测] 征信-当前贷款最大逾期金额 |  |
| 最近5年最大逾期金额 | DOUBLE | column | [AI推测] 征信-最近5年最大逾期金额 |  |
| 被追偿资产处置业务账户数 | DOUBLE | column | [AI推测] 征信-被追偿资产处置业务账户数 |  |
| 民事判决信息记录数 | DOUBLE | column | [AI推测] 征信-民事判决信息记录数 |  |
| 强制执行信息记录数 | DOUBLE | column | [AI推测] 征信-强制执行信息记录数 |  |
| 行政处罚信息记录数 | DOUBLE | column | [AI推测] 征信-行政处罚信息记录数 |  |
| 近1月查询机构数 | DOUBLE | column | [AI推测] 征信-近1月查询机构数 |  |
| 近1月查询机构数_信用卡审批 | DOUBLE | column | [AI推测] 征信-近1月信用卡审批查询机构数 |  |
| 近1月查询机构数_贷款审批 | DOUBLE | column | [AI推测] 征信-近1月贷款审批查询机构数 |  |
| 近3月查询机构数 | DOUBLE | column | [AI推测] 征信-近3月查询机构数 |  |
| 近3月查询机构数_信用卡审批 | DOUBLE | column | [AI推测] 征信-近3月信用卡审批查询机构数 |  |
| 近3月查询机构数_贷款审批 | DOUBLE | column | [AI推测] 征信-近3月贷款审批查询机构数 |  |
| 近6月查询机构数 | DOUBLE | column | [AI推测] 征信-近6月查询机构数 |  |
| 近6月查询机构数_信用卡审批 | DOUBLE | column | [AI推测] 征信-近6月信用卡审批查询机构数 |  |
| 近6月查询机构数_贷款审批 | DOUBLE | column | [AI推测] 征信-近6月贷款审批查询机构数 |  |
| 近12月查询机构数 | DOUBLE | column | [AI推测] 征信-近12月查询机构数 |  |
| 近12月查询机构数_信用卡审批 | DOUBLE | column | [AI推测] 征信-近12月信用卡审批查询机构数 |  |
| 近12月查询机构数_贷款审批 | DOUBLE | column | [AI推测] 征信-近12月贷款审批查询机构数 |  |
| 近1月本人查询次数 | DOUBLE | column | [AI推测] 征信-近1月本人查询次数 |  |
| personalloan_sd_rh_goodlabel_level_v2_prob | DOUBLE | column | 新征信好人分 |  |
| label_sum_wgt | DOUBLE | column | 旧征信好人分 |  |
| 百融m3非银多头 | DOUBLE | column | [AI推测] 百融数据-近3月非银多头借贷次数 |  |
| 百融m3非银多头cut | STRING | column | [AI推测] 百融数据-近3月非银多头分组 |  |
| huarong6_318 | DOUBLE | column | 所有信用卡平均授信金额(人民币) |  |
| rh_debt_with_half_houseloan_new | DOUBLE | column |  人行月负债_新_250529 |  |
| app白户标签 | STRING | column | [AI推测] APP白户标签（是否为新用户） |  |
| pt | STRING | column | 日期，分区字段 |  |
| pt | STRING | partition | 日期，分区字段 |  |

### DDL
```sql
CREATE TABLE xyf_bi.`fk_risk_order_feature_df_forbi` (
  `order_number` STRING COMMENT '订单号',
  `user_no` BIGINT COMMENT '用户号cis系统 app+mobile',
  `acct_no` STRING COMMENT '账户号',
  `cust_no` STRING COMMENT '客户号',
  `ori_order_number` STRING COMMENT '用户订单号',
  `biz_flow_number` STRING COMMENT '业务流水号',
  `apply_cust_product_no` BIGINT COMMENT '用户申请次数(cust_no+产品类型)',
  `apply_cust_app_no` BIGINT COMMENT '用户申请次数(cust_no+app)',
  `loan_amt` DECIMAL(38,18) COMMENT '借款金额:元',
  `period` BIGINT COMMENT '期数',
  `product_type` STRING COMMENT '产品代码:cash_loan/personal_loan',
  `fund_source` STRING COMMENT '资方',
  `status_code` STRING COMMENT '借据申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝,99-其它',
  `status` STRING COMMENT '借据申请状态解释',
  `date_cash` DATETIME COMMENT '资金到账日期',
  `risk_status` STRING COMMENT '风控状态',
  `id_card_number` STRING COMMENT '身份证',
  `date_created` DATETIME COMMENT '订单申请时间',
  `main_biz_flow_number` STRING COMMENT '主订单业务流水号',
  `system` BIGINT COMMENT '系统来源,0:老,1:新',
  `app` STRING COMMENT 'app',
  `inner_app` STRING COMMENT '资金动用渠道',
  `cnl_pd_code` STRING COMMENT '端产品码',
  `push_fundsys_time` DATETIME COMMENT '推到资金系统时间',
  `fund_apply_time` DATETIME COMMENT '资方授信申请时间',
  `fund_query_time` DATETIME COMMENT '资方授信查询时间',
  `fund_loan_time` DATETIME COMMENT '支用申请时间',
  `fund_loan_query_time` DATETIME COMMENT '支用查询时间',
  `fund_loan_success_time` DATETIME COMMENT '资方通知放款成功时间',
  `fund_repay_plan_query_time` DATETIME COMMENT '资方还款计划查询时间',
  `fund_upload_file_time` DATETIME COMMENT '活体/影像件/个人征信信息查询及使用授权书时间',
  `fund_contract_time` DATETIME COMMENT '委托保证合同/担保咨询服务合同时间 ',
  `source` STRING COMMENT '下单来源',
  `device_id` STRING COMMENT '设备id',
  `created_ip` STRING COMMENT '创单ip',
  `risk_first_success_time` DATETIME COMMENT '用户申请后第一次风控通过时间',
  `main_date_created` DATETIME COMMENT '用户申请时间',
  `first_push_fundsys_time` DATETIME COMMENT '首次推到资金系统时间',
  `third_code` STRING COMMENT '第三方编码',
  `main_status_code` STRING COMMENT '主订单申请状态:00-待处理,01-系统处理中,02-报盘处理中,03-交易成功,04-交易失败,05-审核拒绝',
  `risk_price` STRING COMMENT '真实定价（历史数据只保留A24）',
  `fund_source_new` STRING COMMENT '资方(新系统标准)',
  `mobile` STRING COMMENT '手机号',
  `utm_source` STRING COMMENT '提现utm_source',
  `failed_code` STRING COMMENT '失败code',
  `failed_reason` STRING COMMENT '失败原因',
  `first_biz_flow_number` STRING COMMENT '用户本次申请首次进决策系统',
  `pay_date` STRING COMMENT '资金到账日期，yyyymmdd',
  `crt_date` STRING COMMENT '动支日期，yyyymmdd',
  `scene` STRING COMMENT '场景，API/APP',
  `join_biz_flow_number` STRING COMMENT '关联决策引擎流水号',
  `首复贷` STRING,
  `qudao3` STRING COMMENT '动支渠道',
  `qudao_second` STRING COMMENT '动支二级渠道',
  `phone_number_prefix` STRING COMMENT '手机号前三位',
  `phone_number_city_rank` STRING COMMENT '手机号归属地几线城市',
  `monthly_income` STRING COMMENT '月收入',
  `education` STRING COMMENT '学历',
  `gender` BIGINT COMMENT '性别',
  `age` BIGINT COMMENT '年龄',
  `race` STRING COMMENT '民族',
  `xinyan_1` DOUBLE COMMENT '最近90天代扣失败订单数占总订单数的比值下限',
  `id_number_province` STRING COMMENT '身份证归属地_省',
  `id_number_city` STRING COMMENT '身份证归属地_市',
  `id_number_district` STRING COMMENT '身份证归属地_区县',
  `phone_number_province` STRING COMMENT '手机号归属地_省',
  `phone_number_city` STRING COMMENT '手机号归属地_市',
  `phone_number_isp` STRING COMMENT '运营商',
  `ip_province` STRING COMMENT 'IP地址归属地_省',
  `ip_city` STRING COMMENT 'IP地址归属地_市',
  `job` STRING COMMENT '职业',
  `company` STRING COMMENT '公司',
  `title` STRING COMMENT '职位',
  `company_address_province` STRING COMMENT '单位地址_省',
  `company_address_city` STRING COMMENT '单位地址_市',
  `company_address_district` STRING COMMENT '单位地址_区县',
  `company_address` STRING COMMENT '单位地址',
  `residence_province` STRING COMMENT '居住地_省',
  `residence_city` STRING COMMENT '居住地_市',
  `residence_district` STRING COMMENT '居住地_区县',
  `marital_status` STRING COMMENT '婚姻状况',
  `id_number_city_rank` STRING COMMENT '身份证归属地几线城市',
  `expect_loan_period` STRING COMMENT '借款意向期限',
  `expect_loan_amount` STRING COMMENT '借款意向金额',
  `has_car` STRING COMMENT '是否有车',
  `has_house` STRING COMMENT '是否有房',
  `house_type_status` STRING COMMENT '有房状态，房子类型： 0:未知 1:自购房，有按揭 2:自购房，无按揭 3:无房，租房 4:无房，集体宿舍 5:无房，与父母共住 9:其他',
  `work_seniority` STRING COMMENT '工作年限： 1 {3年以下} 2 {3-4年} 3 {5-7年} 4 {8-9年} 5 {10-14年} 6 {15-20年} * 7 {20年以上}',
  `house_price` STRING COMMENT '购房总额: 1 {未购房} 2 {1-50万元} 3 {51-100万元} 4 {101-200万元} 5 {201-300万元} 6 {301-500万元} 7 {501-1000万元} 8 {1000万以上}',
  `car_price` STRING COMMENT '购车总额: 1 {未购车} 2 {3万以下} 3 {3-5万} 4 {6-10万} 5 {11-20万} 6 {21-50万} 7 {51-100万} 8 {101万以上}',
  `tengxun_customize_score_v2` DOUBLE COMMENT '腾讯反欺诈风险评估分',
  `volcano_customize_score` DOUBLE COMMENT '火山定制模型17207分',
  `personalloan_sd_6mceng30_nozy_lgb_rh_v2_score` DOUBLE COMMENT '个人分期首贷6期30+无中原征信模型lgb版v2模型分',
  `personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob` DOUBLE COMMENT '个人分期首贷6期30+无中原征信模型lgb版v2概率分',
  `personalloan_sd_3mceng30_xfzx_rh_fix_v2_score` DOUBLE COMMENT '个人分期首贷3mceng30_新版征信_人行子分V2_score',
  `personalloan_sd_3mceng30_xfzx_rh_fix_v2_prob` DOUBLE COMMENT '个人分期首贷3mceng30_新版征信_人行子分V2_prob',
  `code` STRING COMMENT '百融return_data反馈码',
  `bairong_als_274` DOUBLE COMMENT '近1个月在非银机构申请机构数',
  `bairong_als_402` DOUBLE COMMENT '近3个月在非银机构申请机构数',
  `bairong_als_554` DOUBLE COMMENT '近6个月在非银机构申请机构数',
  `bairong_als_code` STRING COMMENT '百融多头空值code',
  `bairong_rongzhiscore_3` DOUBLE COMMENT '百融评分积极指数',
  `ym_xf_customize_score` DOUBLE COMMENT '友盟信飞定制模型2301',
  `hj_3y_xfnl_1` BIGINT COMMENT '航聚-金额下线',
  `bd_general_fraudc_v3` DOUBLE COMMENT '度小满欺诈因子',
  `hujin_credit_7` DOUBLE COMMENT '当前违约账户数',
  `hujin_credit_8` DOUBLE COMMENT '当前违约金额',
  `hujin_credit_9` DOUBLE COMMENT '当前不良账户数',
  `hujin_credit_10` DOUBLE COMMENT '当前不良额',
  `xinyan_1_特征加工版` DOUBLE COMMENT '最近90天代扣失败订单数占总订单数的比值下限',
  `huarong2_1` DOUBLE COMMENT '人行学历',
  `huarong2_3` DOUBLE COMMENT '最早信用记录距今月数',
  `huarong2_10` DOUBLE COMMENT '个人住房贷款总合同金额',
  `huarong2_11` DOUBLE COMMENT '个人住房贷款已还款期数',
  `huarong2_13` DOUBLE COMMENT '所有账户当前逾期金额',
  `huarong2_15` DOUBLE COMMENT '所有账户最近24个月累计逾期次数',
  `huarong2_17` DOUBLE COMMENT '所有账户最新表现还款状态',
  `huarong2_20` DOUBLE COMMENT '贷记卡最高额度',
  `huarong2_24` DOUBLE COMMENT '人行婚姻',
  `huarong2_25` DOUBLE COMMENT '人行职业',
  `huarong2_41` DOUBLE COMMENT '最近1个月本人查询次数',
  `huarong2_100` DOUBLE COMMENT '结清房贷笔数',
  `huarong2_145` DOUBLE COMMENT '所有账户近6个月平均应还款金额',
  `huarong2_176` DOUBLE COMMENT '非循环贷本月应还款金额总和',
  `huarong2_192` DOUBLE COMMENT '非循环贷个人住房贷款+个人商用住房贷款本月应还款金额总和',
  `huarong2_238` DOUBLE COMMENT '循环额度下分账户本月应还款金额总和',
  `huarong2_260` DOUBLE COMMENT '循环贷本月应还款金额总和',
  `huarong2_281` DOUBLE COMMENT '贷记卡最近月度本月应还金额总和',
  `huarong2_294` DOUBLE COMMENT '贷记卡最近6个月平均使用额度',
  `huarong2_356` DOUBLE COMMENT '所有账户当前正常汽车贷款余额总和',
  `huarong2_337` DOUBLE COMMENT '当前贷款最大逾期期数',
  `huarong2_345` DOUBLE COMMENT '所有账户最近6个月累计逾期次数',
  `huarong2_346` DOUBLE COMMENT '所有账户最近12个月累计逾期次数',
  `huarong2_347` DOUBLE COMMENT '所有账户最近5年累计逾期次数',
  `huarong2_338` DOUBLE COMMENT '当前贷款最大逾期金额',
  `huarong2_340` DOUBLE COMMENT '所有账户最近6个月最大逾期次数',
  `huarong2_341` DOUBLE COMMENT '所有账户最近12个月最大逾期次数',
  `huarong2_342` DOUBLE COMMENT '所有账户最近24个月最大逾期次数',
  `huarong2_343` DOUBLE COMMENT '所有账户最近5年最大逾期次数',
  `huarong3_136` DOUBLE COMMENT '缴存状态且最近参缴公积金的月缴存额',
  `huarong5_1336` DOUBLE COMMENT '最近3个月贷款正常状态合计月份数(当前未结清)',
  `huarong5_1337` DOUBLE COMMENT '最近12个月贷款正常状态合计月份数(当前未结清)',
  `huarong5_1338` DOUBLE COMMENT '最近24个月贷款正常状态合计月份数(当前未结清)',
  `huarong5_1087` DOUBLE COMMENT '一年内贷款已结清状态贷款金额',
  `huarong5_309` DOUBLE COMMENT '发放时间在12个月内非循环贷已结清状态贷款金额',
  `huarong6_38` DOUBLE COMMENT '最近3个月正常状态信用卡合计月份数(历史还款)',
  `huarong6_39` DOUBLE COMMENT '最近12个月正常状态信用卡合计月份数(历史还款)',
  `huarong6_40` DOUBLE COMMENT '最近24个月正常状态信用卡合计月份数(历史还款)',
  `huarong7_103` DOUBLE COMMENT '汽车贷款的最大授信金额',
  `device_system` STRING COMMENT '手机系统',
  `tongdun_3` BIGINT COMMENT '近7天的一般消费分期平台申请平台数',
  `tongdun_4` BIGINT COMMENT '近7天的P2P网贷申请平台数',
  `tongdun_5` BIGINT COMMENT '近7天的大型消费金融公司申请平台数',
  `tongdun_7` BIGINT COMMENT '近7天的小额贷款公司申请平台数',
  `tongdun_12` BIGINT COMMENT '近1个月的一般消费分期平台申请平台数',
  `tongdun_13` BIGINT COMMENT '近1个月的P2P网贷申请平台数',
  `tongdun_14` BIGINT COMMENT '近1个月的大型消费金融公司申请平台数',
  `tongdun_16` BIGINT COMMENT '近1个月的小额贷款公司申请平台数',
  `tongdun_21` BIGINT COMMENT '近3个月的一般消费分期平台申请平台数',
  `tongdun_22` BIGINT COMMENT '近3个月的P2P网贷申请平台数',
  `tongdun_23` BIGINT COMMENT '近3个月的大型消费金融公司申请平台数',
  `tongdun_25` BIGINT COMMENT '近3个月的小额贷款公司申请平台数',
  `tongdun_34` BIGINT COMMENT '近6个月的小额贷款公司申请平台数',
  `tongdun_43` BIGINT COMMENT '近12个月的小额贷款公司申请平台数',
  `rh_debt_all` DOUBLE COMMENT ' 人行月负债_最全',
  `rh_debt_with_half_houseloan` DOUBLE COMMENT ' 人行月负债_360定义',
  `rh_debt_without_houseloan` DOUBLE COMMENT ' 人行月负债_不含房贷',
  `rh_overdueamt_now` DOUBLE COMMENT ' 贷款当前逾期总额',
  `rh_overdue_times_6p` DOUBLE COMMENT ' 贷款近6期逾期次数',
  `rh_overdue_times_24p` DOUBLE COMMENT ' 贷款近24期逾期次数',
  `rh_overdue_times_12p` DOUBLE COMMENT ' 贷款近12期逾期次数',
  `rh_need_pay_6m` DOUBLE COMMENT ' 贷款最近6个月平均应还款',
  `rh_applytimes_debt_card_1m` DOUBLE COMMENT ' 近1个月贷记卡审批查询次数与近1个月贷款审批查询次数之和',
  `rh_applytimes_debt_card_3m` DOUBLE COMMENT ' 近3个月贷记卡审批查询次数与近3个月贷款审批查询次数之和',
  `rh_applytimes_debt_card_6m` DOUBLE COMMENT ' 近6个月贷记卡审批查询次数与近6个月贷款审批查询次数之和',
  `tongdun_273` DOUBLE COMMENT '近7天资产转让平台申请数',
  `tongdun_278` DOUBLE COMMENT '近7天企业主所有平台申请数',
  `tongdun_309` DOUBLE COMMENT '近1个月企业主所有平台申请数',
  `tongdun_340` DOUBLE COMMENT '近3个月企业主所有平台申请数',
  `tongdun_371` DOUBLE COMMENT '近6个月企业主所有平台申请数',
  `tongdun_402` DOUBLE COMMENT '近12个月企业主所有平台申请数',
  `tongdun_363` DOUBLE COMMENT ' 近6个月融资租赁平台申请数',
  `td_90d_mobile_abnomal_device_freq` DOUBLE COMMENT '90天手机号所属设备异常频次，手机号关联设备号二度关联到的90天内全行业下所有事件中设备越狱、厂商位置、安卓模拟器、疑似刷机、疑似模拟定位、多开设备的频次',
  `td_30d_idcard_abnomal_device_freq` DOUBLE COMMENT '30天身份证所属设备异常频次，身份证关联设备号二度关联到的30天内全行业下所有事件中检测到改机工具、脚本版本过期、模拟定位的设备频次',
  `td_30d_idcard_abnomal_device_cnt` DOUBLE COMMENT '30天身份证所属设备异常去重设备数，身份证关联设备号二度关联到的30天内全行业下所有事件中检测到改机工具、版本过期、模拟定位的去重设备个数',
  `td_idcard_owing_taxs` DOUBLE COMMENT '身份证或身份证关联企业是否命中欠税',
  `td_idcard_court_dishonesty` INT COMMENT '身份证是否命中法院失信(案件状态为失信或终本)，或被执行',
  `td_idcard_or_mobile_related_risk` INT COMMENT '手机号或身份证是否命中关联风险(关联来源为非入参身份证或手机号)',
  `td_mobile_fake` DOUBLE COMMENT '手机号是否命中疑似虚假号码',
  `td_idcard_car_rental_default` DOUBLE COMMENT '身份证是否命中汽车租赁违约',
  `百融积极收入区间` STRING,
  `性别` STRING,
  `年龄` BIGINT,
  `年龄分组` STRING,
  `自填学历` STRING,
  `自填收入` STRING,
  `学历分` BIGINT,
  `收入分` BIGINT,
  `自填婚姻状况` STRING,
  `自填职业` STRING,
  `身份证归属地几线城市` STRING,
  `身份证归属地_省` STRING,
  `系统` STRING,
  `公积金在缴月缴存额` DOUBLE,
  `公积金在缴月缴存额_grp` STRING,
  `贷记卡账户数` DOUBLE,
  `最近还款贷记卡开立日期距今天数` DOUBLE,
  `贷记卡最高授信额度` DOUBLE,
  `贷记卡平均授信额度` DOUBLE,
  `房贷本月应还款总额` DOUBLE,
  `房贷已还款期数` DOUBLE,
  `最早信用记录距今月数` DOUBLE,
  `房贷金额` DOUBLE,
  `结清房贷笔数` DOUBLE,
  `公积金缴交基数` DOUBLE,
  `企业担保金额` DOUBLE,
  `信用卡额度使用率` DOUBLE,
  `汽车贷款的最大授信金额` DOUBLE,
  `一年内非循环贷已结清状态贷款金额` DOUBLE,
  `个人经营贷款正常状态最大授信金额` DOUBLE,
  `一年内贷款已结清状态贷款金额` DOUBLE,
  `呆账账户数` DOUBLE,
  `贷记卡当前逾期金额` DOUBLE,
  `当前贷款最大逾期金额` DOUBLE,
  `最近5年最大逾期金额` DOUBLE,
  `被追偿资产处置业务账户数` DOUBLE,
  `民事判决信息记录数` DOUBLE,
  `强制执行信息记录数` DOUBLE,
  `行政处罚信息记录数` DOUBLE,
  `近1月查询机构数` DOUBLE,
  `近1月查询机构数_信用卡审批` DOUBLE,
  `近1月查询机构数_贷款审批` DOUBLE,
  `近3月查询机构数` DOUBLE,
  `近3月查询机构数_信用卡审批` DOUBLE,
  `近3月查询机构数_贷款审批` DOUBLE,
  `近6月查询机构数` DOUBLE,
  `近6月查询机构数_信用卡审批` DOUBLE,
  `近6月查询机构数_贷款审批` DOUBLE,
  `近12月查询机构数` DOUBLE,
  `近12月查询机构数_信用卡审批` DOUBLE,
  `近12月查询机构数_贷款审批` DOUBLE,
  `近1月本人查询次数` DOUBLE,
  `personalloan_sd_rh_goodlabel_level_v2_prob` DOUBLE COMMENT '新征信好人分',
  `label_sum_wgt` DOUBLE COMMENT '旧征信好人分',
  `百融m3非银多头` DOUBLE,
  `百融m3非银多头cut` STRING,
  `huarong6_318` DOUBLE COMMENT '所有信用卡平均授信金额(人民币)',
  `rh_debt_with_half_houseloan_new` DOUBLE COMMENT ' 人行月负债_新_250529',
  `app白户标签` STRING
)
COMMENT '风控-动支-特征宽表(BI同步表)'
PARTITIONED BY (
  `pt` STRING NOT NULL COMMENT '日期，分区字段'
)
STORED AS AliOrc
LIFECYCLE 60
```

## 抽样数据
| order_number | user_no | acct_no | cust_no | ori_order_number | biz_flow_number | apply_cust_product_no | apply_cust_app_no | loan_amt | period | product_type | fund_source | status_code | status | date_cash | risk_status | id_card_number | date_created | main_biz_flow_number | system | app | inner_app | cnl_pd_code | push_fundsys_time | fund_apply_time | fund_query_time | fund_loan_time | fund_loan_query_time | fund_loan_success_time | fund_repay_plan_query_time | fund_upload_file_time | fund_contract_time | source | device_id | created_ip | risk_first_success_time | main_date_created | first_push_fundsys_time | third_code | main_status_code | risk_price | fund_source_new | mobile | utm_source | failed_code | failed_reason | first_biz_flow_number | pay_date | crt_date | scene | join_biz_flow_number | 首复贷 | qudao3 | qudao_second | phone_number_prefix | phone_number_city_rank | monthly_income | education | gender | age | race | xinyan_1 | id_number_province | id_number_city | id_number_district | phone_number_province | phone_number_city | phone_number_isp | ip_province | ip_city | job | company | title | company_address_province | company_address_city | company_address_district | company_address | residence_province | residence_city | residence_district | marital_status | id_number_city_rank | expect_loan_period | expect_loan_amount | has_car | has_house | house_type_status | work_seniority | house_price | car_price | tengxun_customize_score_v2 | volcano_customize_score | personalloan_sd_6mceng30_nozy_lgb_rh_v2_score | personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob | personalloan_sd_3mceng30_xfzx_rh_fix_v2_score | personalloan_sd_3mceng30_xfzx_rh_fix_v2_prob | code | bairong_als_274 | bairong_als_402 | bairong_als_554 | bairong_als_code | bairong_rongzhiscore_3 | ym_xf_customize_score | hj_3y_xfnl_1 | bd_general_fraudc_v3 | hujin_credit_7 | hujin_credit_8 | hujin_credit_9 | hujin_credit_10 | xinyan_1_特征加工版 | huarong2_1 | huarong2_3 | huarong2_10 | huarong2_11 | huarong2_13 | huarong2_15 | huarong2_17 | huarong2_20 | huarong2_24 | huarong2_25 | huarong2_41 | huarong2_100 | huarong2_145 | huarong2_176 | huarong2_192 | huarong2_238 | huarong2_260 | huarong2_281 | huarong2_294 | huarong2_356 | huarong2_337 | huarong2_345 | huarong2_346 | huarong2_347 | huarong2_338 | huarong2_340 | huarong2_341 | huarong2_342 | huarong2_343 | huarong3_136 | huarong5_1336 | huarong5_1337 | huarong5_1338 | huarong5_1087 | huarong5_309 | huarong6_38 | huarong6_39 | huarong6_40 | huarong7_103 | device_system | tongdun_3 | tongdun_4 | tongdun_5 | tongdun_7 | tongdun_12 | tongdun_13 | tongdun_14 | tongdun_16 | tongdun_21 | tongdun_22 | tongdun_23 | tongdun_25 | tongdun_34 | tongdun_43 | rh_debt_all | rh_debt_with_half_houseloan | rh_debt_without_houseloan | rh_overdueamt_now | rh_overdue_times_6p | rh_overdue_times_24p | rh_overdue_times_12p | rh_need_pay_6m | rh_applytimes_debt_card_1m | rh_applytimes_debt_card_3m | rh_applytimes_debt_card_6m | tongdun_273 | tongdun_278 | tongdun_309 | tongdun_340 | tongdun_371 | tongdun_402 | tongdun_363 | td_90d_mobile_abnomal_device_freq | td_30d_idcard_abnomal_device_freq | td_30d_idcard_abnomal_device_cnt | td_idcard_owing_taxs | td_idcard_court_dishonesty | td_idcard_or_mobile_related_risk | td_mobile_fake | td_idcard_car_rental_default | 百融积极收入区间 | 性别 | 年龄 | 年龄分组 | 自填学历 | 自填收入 | 学历分 | 收入分 | 自填婚姻状况 | 自填职业 | 身份证归属地几线城市 | 身份证归属地_省 | 系统 | 公积金在缴月缴存额 | 公积金在缴月缴存额_grp | 贷记卡账户数 | 最近还款贷记卡开立日期距今天数 | 贷记卡最高授信额度 | 贷记卡平均授信额度 | 房贷本月应还款总额 | 房贷已还款期数 | 最早信用记录距今月数 | 房贷金额 | 结清房贷笔数 | 公积金缴交基数 | 企业担保金额 | 信用卡额度使用率 | 汽车贷款的最大授信金额 | 一年内非循环贷已结清状态贷款金额 | 个人经营贷款正常状态最大授信金额 | 一年内贷款已结清状态贷款金额 | 呆账账户数 | 贷记卡当前逾期金额 | 当前贷款最大逾期金额 | 最近5年最大逾期金额 | 被追偿资产处置业务账户数 | 民事判决信息记录数 | 强制执行信息记录数 | 行政处罚信息记录数 | 近1月查询机构数 | 近1月查询机构数_信用卡审批 | 近1月查询机构数_贷款审批 | 近3月查询机构数 | 近3月查询机构数_信用卡审批 | 近3月查询机构数_贷款审批 | 近6月查询机构数 | 近6月查询机构数_信用卡审批 | 近6月查询机构数_贷款审批 | 近12月查询机构数 | 近12月查询机构数_信用卡审批 | 近12月查询机构数_贷款审批 | 近1月本人查询次数 | personalloan_sd_rh_goodlabel_level_v2_prob | label_sum_wgt | 百融m3非银多头 | 百融m3非银多头cut | huarong6_318 | rh_debt_with_half_houseloan_new | app白户标签 | pt | pt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 202202011147490219215503 | 1041170034 | L000818254013095357 | CTL0211d850a1accd3a0c6fd30f9f6b48ae7 | 202202011147490219215503 | 20220201114749360918280 | 1 | 1 | 9000 | 12 | personal_loan | zzr_zy_cash | 03 | 交易成功 | 2022-02-01 11:50:39 | pass | dE8wGKf2kGBo77suJXQ/kH/b0a4ZNRrMxC7kMOOQen4= | 2022-02-01 11:47:49 | 20220201114749360918280 | 0 | xyf01 | xyf01_jd01 |  |  |  |  |  |  |  |  |  |  | ios | 20220128575229202a | 114.101.33.155 |  | 2022-02-01 11:47:49 |  | zzr_zy_cash_1 | 03 |  | zzr_zy_cash | IunD7RU5yKE8ENKw6XRTLw== | XYF01-API-JIDAI01 | 000000 | remit_success\|remitSuccess | 20220201114749360918280 | 20220201 | 20220201 | API | 20220201114749360918280 | 首贷 | API | xyf01_jd01 | 189 | 三线 | 10,000~20,000 | 高中/中专/技校 | 0 | 34 | 汉 | 0.1 | 安徽省 | 阜阳市 |  | 安徽 | 阜阳 | 中国电信 | 安徽省 | 蚌埠市 | 公司员工 | 安徽伟辰钢结构有限公司 |  | 安徽省 | 阜阳市 | 颍泉区 | 安徽省阜阳市颍泉区中市街道顶大路安徽阜阳工业园区 |  |  |  | 20 | 三线 |  |  |  |  |  |  |  |  | 554841.0 | 0.0481 |  |  |  |  | 00 | 4.0 | 10.0 | 12.0 | 00 | 0.0 | 625.0 |  | 40.71 |  |  |  |  | 0.1 | 4.0 | 81.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 45273.0 | 5.0 | 4.0 | 0.0 | 0.0 | 37109.5 | 10552.0 | 0.0 | 205.0 | 11934.0 | 20455.0 | 5917.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 1.0 |  | 54.0 | 109.0 | 113.0 | 16500.0 | 14000.0 | 16.0 | 67.0 | 139.0 |  | ios |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 24736.5 | 24736.5 | 24736.5 | 0.0 | 0.0 | 0.0 | 0.0 | 17884.0 | 4.0 | 7.0 | 13.0 |  |  |  |  |  |  |  | 5.0 | 0.0 | 0.0 | -1998.0 | 0 | 0 | -999.0 | -999.0 |  | F | 34 | [31-35] | 高中 | 5.[10k-20k] | 1 | 4 | 20 | 公司员工 | 三线 | 安徽省 | ios |  |  | 13.0 | 1131.0 | 45273.0 | 34853.2857 | 0.0 | 0.0 | 81.0 | 0.0 | 0.0 |  |  | 0.5904 |  | 14000.0 |  | 16500.0 |  | 0.0 | 0.0 | 5.0 |  |  |  |  | 4.0 | 0.0 | 4.0 | 6.0 | 0.0 | 6.0 | 11.0 | 1.0 | 10.0 | 15.0 | 1.0 | 14.0 | 0.0 |  |  | 10.0 | 07_10 | 23340.0 | 37095.0 | 1.人行活跃用户 | 20260211 | 20260211 |
| 202307171525290246002898 | 1107839654 | L000818125521072086 | CTL02f3182a2352aff306fb412a03180d2be | 202307171525290246002898 | 202307171525291221756125 | 1 | 1 | 1500 | 12 | personal_loan | mzks_cash_p2 | 03 | 交易成功 | 2023-07-17 15:38:12 | pass | oALpKf3WPJFos9DM9V9dHlOj/3RBQZPEXYA+PYXtkaw= | 2023-07-17 15:25:29 | 202307171525291221756125 | 0 | xyf01 | xyf01_58jr |  | 2023-07-17 15:26:11 |  |  |  |  |  |  |  |  | android | 20230717b8b3f292e7 | 111.26.209.223 | 2023-07-17 15:25:31 | 2023-07-17 15:25:29 | 2023-07-17 15:26:11 | mzks_cash_p2 | 03 |  | mzks_cash | DQ/Ly55Wfz+GGV7U6QLrng== | XYF01-API-58JINRONG01 | 000000 | remit_success\|remitSuccess | 202307171525291221756125 | 20230717 | 20230717 | API | 202307171525291221756125 | 首贷 | API | xyf01_58jr | 138 | 二线 | 6,000~10,000 | 高中/中专/技校 | 1 | 36 | 汉 | 0.6 | 吉林省 | 松原市 |  | 吉林 | 长春 | 中国移动 | 吉林省 | 长春市 | 公司员工 | 活力城购物广场有限责任公司 |  | 吉林省 | 长春市 | 南关区 | 吉林省长春市重庆路与大经路交汇88号 |  |  |  |  | 四线 |  |  |  |  |  |  |  |  | 867797.0 |  | 0.0 | 0.0508097216938288 |  |  | 00 | 9.0 | 19.0 | 25.0 | 00 | 0.0 | 515.0 |  | 47.35 | 0.0 | 0.0 | 0.0 | 0.0 | 0.6 | 6.0 | 67.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 10500.0 | 5.0 | 4.0 | 0.0 | 0.0 | 19420.3333 | 502.0 | 0.0 |  | 1523.0 | 9533.0 | 10123.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  | 14.0 | 30.0 | 35.0 | 0.0 | 0.0 | 26.0 | 98.0 | 194.0 |  | android | 1 | 1 |  |  | 1 | 1 |  | 1 | 3 | 3 | 1 | 1 | 1 | 1 | 2978.3 | 2978.3 | 2978.3 | 0.0 | 0.0 | 0.0 | 0.0 | 2029.0 | 5.0 | 10.0 | 20.0 |  | 0.0 | 0.0 | 1.0 | 1.0 | 1.0 |  | -5994.0 | 0.0 | 0.0 | -1998.0 | 0 | 0 | -999.0 | -999.0 |  | M | 36 | [36-40] | 高中 | 7.[6k-10k] | 1 | 3 |  | 公司员工 | 四线 | 吉林省 | android |  |  | 19.0 | 1771.0 | 10500.0 | 5044.7368 | 0.0 | 0.0 | 67.0 | 0.0 | 0.0 |  |  | 0.5802 |  | 0.0 |  | 0.0 |  | 0.0 | 0.0 |  |  |  |  |  | 5.0 | 0.0 | 5.0 | 12.0 | 0.0 | 9.0 | 16.0 | 0.0 | 13.0 | 17.0 | 0.0 | 17.0 | 0.0 |  |  | 19.0 | g15 | 6950.0 | 7586.6 | 1.人行活跃用户 | 20260211 | 20260211 |
| 202312030946330269030013 | 1064530562 | L000818101621431223 | CTL073717cfdbe372d328ed34e2c1d31e9c5 | 202312030946330269030013 | 202312030946331724353034 | 0 | 0 | 0 | 12 | personal_loan | xyxj_cash | 04 | 交易失败 |  | reject | 9xfMh9Hy14aVmCVdpla8rzF0jz7Ep2o81tpmZnP/I7s= | 2023-12-03 09:46:33 | 202312030946331724353034 | 0 | xyf01 | xyf01_jd01 |  |  |  |  |  |  |  |  |  |  | android | 20231123d4fef41670 | 112.224.166.16 |  | 2023-12-03 09:46:33 |  | xyxj_cash | 04 | 0 | xyxj_cash | PQFPkYdkF7h+eQAcCeMsXQ== | XYF01-API-JIDAI01 | 420000 | reject\|[riskAudit]大额取现策略审核:reject | 202312030946331724353034 |  | 20231203 | API | 202312030946331724353034 | 首贷 | API | xyf01_jd01 | 176 | 新一线 | 10,000~20,000 | 专科 | 1 | 29 | 汉 | -999999.0 | 山东省 | 青岛市 |  | 山东 | 青岛 | 中国联通 | 山东省 | 济南市 | 公司员工 | 青岛金格仪表有限公司 |  | 山东省 | 青岛市 | 平度市 | 山东省青岛市平度市白沙河办事处白沙工业园金沙路六号 |  |  |  |  | 新一线 |  |  |  |  |  |  |  |  |  | 0.0775 | 0.0 | 0.108217369185452 |  |  | 00 | 14.0 | 19.0 | 21.0 | 00 | 0.0 | 701.0 |  | 47.25 | 0.0 | 0.0 | 0.0 | 0.0 | -999999.0 | 6.0 | 60.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 12000.0 | 5.0 | 15.0 | 0.0 | 0.0 | 6717.5 | 4262.0 | 0.0 | 953.0 | 2275.0 | 5663.0 | 11054.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 |  | 48.0 | 128.0 | 162.0 | 0.0 | 0.0 | 13.0 | 49.0 | 60.0 | 60000.0 | android | 1 | 1 |  |  | 2 | 2 |  |  | 2 | 3 | 1 | 1 | 1 | 1 | 8056.3 | 8056.3 | 8056.3 | 0.0 | 0.0 | 0.0 | 0.0 | 6971.0 | 3.0 | 12.0 | 14.0 |  | 0.0 | 0.0 | 2.0 | 2.0 | 2.0 |  | 0.0 | 0.0 | 0.0 | -1998.0 | 0 | 0 | -999.0 | -999.0 |  | M | 29 | [26-30] | 专科 | 5.[10k-20k] | 2 | 4 |  | 公司员工 | 新一线 | 山东省 | android |  |  | 6.0 | 485.0 | 12000.0 | 6900.0 | 0.0 | 0.0 | 60.0 | 0.0 | 0.0 |  |  | 0.648 | 60000.0 | 0.0 |  | 0.0 |  | 0.0 | 0.0 |  |  |  |  |  | 3.0 | 0.0 | 3.0 | 12.0 | 2.0 | 9.0 | 16.0 | 2.0 | 10.0 | 23.0 | 3.0 | 20.0 | 0.0 |  |  | 19.0 | g15 | 7750.0 | 9725.5 | 1.人行活跃用户 | 20260211 | 20260211 |
| 202401221921020277814915 | 1044921539 | L000818209719396047 | CTL0d799dfd7416af1e44aa57afd3d918b67 | 202401221920590277824129 | 202401221921021820582414 | 0 | 0 | 0 | 3 | personal_loan | lhzl_cash | 04 | 交易失败 | 2024-01-22 19:58:30 | reject | Q9nme648kh9FkuGBdbZAjT+iN/Ju9B5++55csRY4UbU= | 2024-01-22 19:21:02 | 202401221920591820582399 | 0 | xyf01 | xyf01 |  |  |  |  |  |  |  |  |  |  | ios | 202304279820ad1fe6 | 39.148.180.8 |  | 2024-01-22 19:20:59 |  | lhzl_cash_1 | 04 | A24 | lhzl_cash | V0Ay9skIY/anWsJ9FK+MHA== | xyf01_app | 420000 | reject\|[riskAudit]大额取现策略审核:reject | 202401221921021820582414 | 20240122 | 20240122 | APP | 202401221921021820582414 | 复贷 | 复贷 | 复贷 | 150 | 新一线 | 6,000~10,000 | 专科 | 1 | 31 | 汉 | 0.7 | 河南省 | 濮阳市 |  | 河南 | 郑州 | 中国移动 | 河南省 | 郑州市 | 其他 | 东莞市康宝来有限公司 |  | 河南省 | 濮阳市 | 清丰县 | 河南省清丰县古城乡吴家村6排 |  |  |  |  | 四线 |  |  |  |  |  |  |  |  |  | 0.3035 | 0.0 | 0.0674312617745497 |  |  | 00 | 1.0 | 17.0 | 20.0 | 00 | 6.0 | 576.0 | 700 | 50.68 |  |  |  |  | 0.7 | 6.0 | 82.0 | 230000.0 | 79.0 | 0.0 | 4.0 | 0.0 | 9000.0 | 2.0 | 15.0 | 0.0 | 1.0 | 11868.6667 | 1443.0 | 1443.0 |  | 173.0 | 1928.0 | 5846.0 | 0.0 | 0.0 | 2.0 | 2.0 | 4.0 | 0.0 | 1.0 | 1.0 | 1.0 | 1.0 |  | 10.0 | 35.0 | 58.0 | 5500.0 | 0.0 | 15.0 | 55.0 | 115.0 |  | ios | 1 | 2 |  |  | 1 | 2 |  |  | 1 | 3 |  |  | 1 | 1 | 1808.8 | 1087.3 | 365.8 | 0.0 | 2.0 | 4.0 | 2.0 | 2531.0 | 4.0 | 4.0 | 13.0 |  | 0.0 | 0.0 | 0.0 | 2.0 | 2.0 |  | 0.0 | 0.0 | 0.0 | -1998.0 | 0 | 0 | -999.0 | -999.0 | 0 | M | 31 | [31-35] | 专科 | 7.[6k-10k] | 2 | 3 |  | 其他 | 四线 | 河南省 | ios |  |  | 10.0 | 1151.0 | 9000.0 | 4385.7143 | 1443.0 | 79.0 | 82.0 | 230000.0 | 1.0 |  |  | 1.0715 |  | 0.0 |  | 5500.0 |  | 0.0 | 0.0 | 1306.0 |  |  |  |  | 6.0 | 0.0 | 4.0 | 7.0 | 0.0 | 4.0 | 15.0 | 0.0 | 9.0 | 15.0 | 0.0 | 15.0 | 0.0 |  |  | 17.0 | g15 | 3775.0 | 4184.0 | 1.人行活跃用户 | 20260211 | 20260211 |
| 202403161007060286733094 | 1076929699 | 0757729961956892672 | CTL00906f9a364ec0f365175dd00847a61e4 | 202403160953440286737699 | 202403161007061876761385 | 1 | 1 | 8000 | 12 | personal_loan | htyh_cash | 03 | 交易成功 | 2024-03-16 10:13:46 | pass | MJ2KfERwdxT5cYgCycBwQF/SlwTufvadDxoG1Zh0kec= | 2024-03-16 10:07:06 | 202403160953441876747046 | 0 | xyf01 | xyf01_rs03 |  | 2024-03-16 10:07:28 |  |  |  |  |  |  |  |  | android | 20240316e439b793fa | 42.93.154.103 | 2024-03-16 09:53:45 | 2024-03-16 09:53:44 | 2024-03-16 09:54:31 | htyh_cash | 03 | 0 | htyh_cash | nFt/rBLsOdzqs98CzMJ2iw== | XYF01-API-RS03 |  |  | 202403160953441876747046 | 20240316 | 20240316 | API | 202403161007061876761385 | 首贷 | API | xyf01_rs03 | 139 | 五线 | 6,000~10,000 | 专科 | 1 | 52 | 汉 | 0.01 | 甘肃省 | 金昌市 |  | 甘肃 | 武威 | 中国移动 | 甘肃省 | 酒泉市 | 公司员工 | 甘肃安拓化工科技有限公司 |  | 甘肃省 | 金昌市 | 永昌县 | 甘肃省金昌市河西堡镇工业园区 |  |  |  |  | 五线 |  |  |  |  |  |  |  |  | 529951.0 | 0.0414 | 0.0 | 0.0491549892779794 |  |  | 00 | 17.0 | 23.0 | 29.0 | 00 | 0.0 | 730.0 | 700 | 42.06 | 0.0 | 0.0 | 0.0 | 0.0 | 0.01 | 6.0 | 246.0 | 20000.0 | 24.0 | 0.0 | 0.0 | 0.0 | 5000.0 | 5.0 | 4.0 | 0.0 | 1.0 | 10197.666667 | 37742.0 | 0.0 |  | 5159.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 | 0.0 | 0.0 | 0.0 | 0.0 | 7.0 |  | 160.0 | 207.0 | 218.0 | 150211.0 | 126971.0 | 0.0 | 0.0 | 0.0 |  | android | 1 |  |  |  | 2 | 4 |  | 2 | 3 | 6 |  | 2 | 2 | 2 | 42901.0 | 42901.0 | 42901.0 | 0.0 | 0.0 | 0.0 | 0.0 | 30593.0 | 6.0 | 20.0 | 45.0 |  | 0.0 | 2.0 | 2.0 | 2.0 | 2.0 |  | 0.0 | 0.0 | 0.0 | -1998.0 | 0 | 0 | -999.0 | -999.0 |  | M | 52 | [46-55] | 专科 | 7.[6k-10k] | 2 | 3 |  | 公司员工 | 五线 | 甘肃省 | android |  |  | 5.0 | 4426.0 | 5000.0 | 5000.0 | 0.0 | 24.0 | 246.0 | 20000.0 | 1.0 |  |  | 0.0 |  | 126971.0 |  | 150211.0 |  | 0.0 | 0.0 | 25900.0 |  |  |  |  | 13.0 | 0.0 | 9.0 | 23.0 | 0.0 | 17.0 | 37.0 | 0.0 | 28.0 | 33.0 | 1.0 | 32.0 | 0.0 | 2.15 |  | 23.0 | g15 | 1666.666667 | 42901.0 | 1.人行活跃用户 | 20260211 | 20260211 |

## 同步来源
- `odps`
