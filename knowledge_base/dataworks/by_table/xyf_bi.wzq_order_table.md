# xyf_bi.wzq_order_table

## 来源文件
- 未记录

## 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column | [AI推测] 订单号 |  |
| ori_order_number | STRING | column | [AI推测] 原始订单号 |  |
| biz_flow_number | STRING | column | [AI推测] 业务流水号 |  |
| shoufudai_cyx | STRING | column | [AI推测] 首复贷标识（首贷/复贷） |  |
| flow_number | STRING | column | [AI推测] 流水号 |  |
| biz_first_created | STRING | column | [AI推测] 首次业务创建标识 |  |
| created_time_old | DATETIME | column | [AI推测] 旧系统订单创建时间 |  |
| created_time | DATETIME | column | [AI推测] 订单创建时间 |  |
| decision_time_final | DATETIME | column | [AI推测] 最终决策时间 |  |
| draw_day | STRING | column | [AI推测] 动支日期（yyyy-MM-dd） |  |
| draw_week | STRING | column | [AI推测] 动支所在周 |  |
| draw_month | STRING | column | [AI推测] 动支月份（yyyy-MM） |  |
| id_card_number | STRING | column | [AI推测] 身份证号（加密） |  |
| mobile | STRING | column | [AI推测] 手机号（加密） |  |
| app_user_id | BIGINT | column | [AI推测] APP用户ID |  |
| cust_no | STRING | column | [AI推测] 客户号 |  |
| app | STRING | column | [AI推测] 应用标识 |  |
| inner_app | STRING | column | [AI推测] 内部渠道标识 |  |
| draw_chanl | STRING | column | [AI推测] 动支渠道 |  |
| asset_type | BIGINT | column | [AI推测] 资产类型编码 |  |
| risk_price | STRING | column | [AI推测] 风险定价等级 |  |
| loan_type | STRING | column | [AI推测] 贷款产品类型 |  |
| period | BIGINT | column | [AI推测] 贷款期数 |  |
| loan_time | DATETIME | column | [AI推测] 放款时间 |  |
| amount | DECIMAL(38,18) | column | [AI推测] 贷款金额（分） |  |
| loan_amount | DECIMAL(38,18) | column | [AI推测] 放款金额 |  |
| status | STRING | column | [AI推测] 订单状态 |  |
| risk_status | STRING | column | [AI推测] 风控状态 |  |
| remit_status | STRING | column | [AI推测] 放款状态 |  |
| failed_reason | STRING | column | [AI推测] 失败原因 |  |
| fund_source | STRING | column | [AI推测] 资金来源/资方 |  |
| 新老借款流程 | STRING | column | [AI推测] 新老借款流程标识 |  |
| zs_profit_amount | STRING | column | [AI推测] 展示利润金额 |  |
| draw_mob_first | INT | column | [AI推测] 首贷距今月数 |  |
| 账龄 | STRING | column | [AI推测] 账龄分组（短账龄/长账龄） |  |
| first_order_number | STRING | column | [AI推测] 首次订单号 |  |
| first_draw_date | DATETIME | column | [AI推测] 首次动支日期 |  |
| first_flag | STRING | column | [AI推测] 首贷标识 |  |
| draw_chanl_1 | STRING | column | [AI推测] 动支一级渠道 |  |
| cust_type_01 | STRING | column | [AI推测] 客户类型 |  |
| first_inner_app | STRING | column | [AI推测] 首贷内部渠道 |  |
| shoudaiperiod | BIGINT | column | [AI推测] 首贷期数 |  |
| edu_total | DOUBLE | column | [AI推测] 总额度（元） |  |
| edu_zaidai | DOUBLE | column | [AI推测] 在贷额度（元） |  |
| edu_available | DOUBLE | column | [AI推测] 可用额度（元） |  |
| edu_init_credit | DOUBLE | column | [AI推测] 初始授信额度（元） |  |
| credit_expire_date | STRING | column | [AI推测] 授信到期日期 |  |
| edu_credit | DOUBLE | column | [AI推测] 授信额度（元） |  |
| edu_temp | DOUBLE | column | [AI推测] 临时额度（元） |  |
| rejected_1dpast | INT | column | [AI推测] 过去1天内是否被拒 |  |
| rejected_3dpast | INT | column | [AI推测] 过去3天内是否被拒 |  |
| rejected_7dpast | INT | column | [AI推测] 过去7天内是否被拒 |  |
| rejected_10dpast | INT | column | [AI推测] 过去10天内是否被拒 |  |
| rejected_14dpast | INT | column | [AI推测] 过去14天内是否被拒 |  |
| rejected_20dpast | INT | column | [AI推测] 过去20天内是否被拒 |  |
| rejected_25dpast | INT | column | [AI推测] 过去25天内是否被拒 |  |
| rejected_30dpast | INT | column | [AI推测] 过去30天内是否被拒 |  |
| rejected_60dpast | INT | column | [AI推测] 过去60天内是否被拒 |  |
| rejected_90dpast | INT | column | [AI推测] 过去90天内是否被拒 |  |
| bairong_7d_fy | DOUBLE | column | [AI推测] 百融7d放样特征值 |  |
| bairong_15d_fy | DOUBLE | column | [AI推测] 百融15d放样特征值 |  |
| bairong_1m_fy | DOUBLE | column | [AI推测] 百融1m放样特征值 |  |
| bairong_3m_fy | DOUBLE | column | [AI推测] 百融3m放样特征值 |  |
| bairong_6m_fy | DOUBLE | column | [AI推测] 百融6m放样特征值 |  |
| bairong_12m_fy | DOUBLE | column | [AI推测] 百融12m放样特征值 |  |
| huarong2_10 | DOUBLE | column | [AI推测] 华融特征变量_10 |  |
| huarong2_17 | DOUBLE | column | [AI推测] 华融特征变量_17 |  |
| huarong2_22 | DOUBLE | column | [AI推测] 华融特征变量_22 |  |
| huarong2_24 | DOUBLE | column | [AI推测] 华融特征变量_24 |  |
| xinyan_1 | DOUBLE | column | [AI推测] 新颜特征_近90天代扣失败订单占比 |  |
| age | BIGINT | column | [AI推测] 年龄 |  |
| gender | BIGINT | column | [AI推测] 性别 |  |
| race | STRING | column | [AI推测] 民族 |  |
| education | STRING | column | [AI推测] 学历 |  |
| marital_status | STRING | column | [AI推测] 婚姻状况 |  |
| monthly_income | STRING | column | [AI推测] 月收入 |  |
| id_number_province | STRING | column | [AI推测] 身份证归属地_省 |  |
| id_number_city | STRING | column | [AI推测] 身份证归属地_市 |  |
| id_number_city_rank | STRING | column | [AI推测] 身份证归属地城市等级 |  |
| has_house | STRING | column | [AI推测] 是否有房 |  |
| has_car | STRING | column | [AI推测] 是否有车 |  |
| rule_set_id | STRING | column | [AI推测] 命中规则集ID |  |
| rule_id | STRING | column | [AI推测] 命中规则ID |  |
| rule_name | STRING | column | [AI推测] 命中规则名称 |  |
| rule_set_name | STRING | column | [AI推测] 命中规则集名称 |  |
| last_temp_amt_adjust_time | DATETIME | column | [AI推测] 最近临时额度调整时间 |  |
| rejust_date | DATETIME | column | [AI推测] 额度调整日期 |  |
| tiaoe_label | STRING | column | [AI推测] 调额标签 |  |
| mob | BIGINT | column | [AI推测] 账龄月数（Months on Book） |  |
| max_overdue_days | BIGINT | column | [AI推测] 历史最大逾期天数 |  |
| os | STRING | column | [AI推测] 操作系统 |  |
| source | STRING | column | [AI推测] 来源 |  |
| appl_chanel | STRING | column | [AI推测] 申请渠道 |  |
| register_source | STRING | column | [AI推测] 注册来源 |  |
| fenzu_lb | STRING | column | [AI推测] 分组类别/策略版本 |  |
| 新多模型分组 | STRING | column | [AI推测] 新多模型分组结果 |  |
| random_1 | INT | column | [AI推测] 随机数1（AB测试用） |  |
| random_2 | STRING | column | [AI推测] 随机数2（AB测试用） |  |
| decisionid | STRING | column | [AI推测] 决策引擎ID |  |
| personalloan_jfd_draw_creditlevel_ssrh_v2_1 | DECIMAL(38,18) | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v2_1 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v3_2 | DECIMAL(38,18) | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v3_2 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v3_2_1 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v3_2_1 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v2_2_3 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v2_2_3 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v2_2_4 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v2_2_4 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v4 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v4 |  |
| 多模型_cross_审批评级_v4 | DOUBLE | column | [AI推测] 多模型交叉审批评级_V4 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v5 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v5 |  |
| 多模型_cross_审批评级_v5 | DOUBLE | column | [AI推测] 多模型交叉审批评级_V5 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v6 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v6 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v6_2 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v6_2 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v7 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v7 |  |
| personalloan_jfd_stock_creditlevel_hcrh_v2_2_2 | STRING | column | [AI推测] 个人贷存量信用等级_回查人行_v2_2_2 |  |
| personalloan_jfd_stock_creditlevel_hcrh_v2_2_3 | STRING | column | [AI推测] 个人贷存量信用等级_回查人行_v2_2_3 |  |
| 存量v4贷中风险等级 | STRING | column | [AI推测] 存量v4版本贷中风险等级 |  |
| 存量v5贷中风险等级 | STRING | column | [AI推测] 存量v5版本贷中风险等级 |  |
| 存量v6贷中风险等级 | STRING | column | [AI推测] 存量v6版本贷中风险等级 |  |
| 存量v7贷中风险等级 | STRING | column | [AI推测] 存量v7版本贷中风险等级 |  |
| 存量v8贷中风险等级 | STRING | column | [AI推测] 存量v8版本贷中风险等级 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v7_1 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v7_1 |  |
| personalloan_jfd_draw_creditlevel_ssrh_v8 | DOUBLE | column | [AI推测] 个人贷审批信用等级模型分_实时人行_v8 |  |
| personalloan_jfd_stock_creditlevel_detail_hcrh_v8_1 | DOUBLE | column |  |  |
| personalloan_jfd_draw_creditlevel_ssrh_model_v9_apply | DOUBLE | column |  |  |
| personalloan_jfd_draw_creditlevel_ssrh_model_v9_detail | DOUBLE | column |  |  |
| personalloan_jfd_stock_creditlevel_hcrh_v9_2 | STRING | column |  |  |
| personalloan_jfd_stock_creditlevel_detail_hcrh_v9_2 | DOUBLE | column |  |  |
| personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | DOUBLE | column | [AI推测] 个人贷存量信用等级明细_回查人行_V6起 |  |
| 审批评级 | DOUBLE | column | [AI推测] 审批评级分数 |  |
| 存量贷中风险等级 | STRING | column | [AI推测] 当前存量贷中风险等级 |  |
| 存量贷中细分风险等级 | DOUBLE | column |  |  |
| personalloan_fd_creditlevel_level_user_group_v4_output | STRING | column | [AI推测] 个人贷信用等级用户分组_v4_输出 |  |
| personalloan_fd_creditlevel_level_user_group_v5_output | STRING | column | [AI推测] 个人贷信用等级用户分组_v5_输出 |  |
| 提额卡用户分组 | STRING | column | [AI推测] 提额卡用户分组 |  |
| tek_apl_amt_rte | DOUBLE | column | [AI推测] 提额卡申请金额费率 |  |
| 会员卡用户分组 | STRING | column | [AI推测] 会员卡用户分组 |  |
| vip_apl_amt_rte | DOUBLE | column | [AI推测] VIP申请金额费率 |  |
| 飞跃会员卡用户分组 | STRING | column | [AI推测] 飞跃会员卡用户分组 |  |
| fy_vip_apl_amt_rte | DOUBLE | column | [AI推测] 飞跃VIP申请金额费率 |  |
| vip_fk_ord_flg_1 | STRING | column | [AI推测] VIP风控订单标记 |  |
| 复贷细分客群 | STRING | column | [AI推测] 复贷细分客群类别 |  |
| 复贷客群分组 | STRING | column | [AI推测] 复贷客群分组 |  |
| 复贷客群分组2 | STRING | column | [AI推测] 复贷客群分组（第二版） |  |
| 飞跃客群分组 | STRING | column | [AI推测] 飞跃客群分组 |  |
| risk_freeze_amt_now | STRING | column | [AI推测] 当前风控冻结额度 |  |
| f_risk_freeze_amt_rate | STRING | column | [AI推测] 风控冻结额度比率 |  |
| f_risk_freeze_amt_rate_group | STRING | column | [AI推测] 风控冻结额度比率分组 |  |
| freeze_apply_flag | STRING | column | [AI推测] 冻结申请标识 |  |
| freeze_risk_result | STRING | column | [AI推测] 冻结风控结果 |  |
| freeze_rule_set_id | STRING | column | [AI推测] 冻结命中规则集ID |  |
| freeze_rule_set_name | STRING | column | [AI推测] 冻结命中规则集名称 |  |
| freeze_rule_id | STRING | column | [AI推测] 冻结命中规则ID |  |
| freeze_rule_name | STRING | column | [AI推测] 冻结命中规则名称 |  |
| risk_freeze_amt_after | DOUBLE | column | [AI推测] 冻结后风控额度 |  |
| freeze_order_number | STRING | column | [AI推测] 冻结关联订单号 |  |
| freeze_order_created_time | DATETIME | column | [AI推测] 冻结订单创建时间 |  |
| risk_bizid | STRING | column |  |  |
| ori_risk_price | STRING | column | [AI推测] 原始风险定价 |  |
| rh_fuzhai | DOUBLE | column |  |  |
| personalloan_fd_6mceng30_xfzx_offline_v2_prob | DOUBLE | column |  |  |
| y0_1_1 | DOUBLE | column | [AI推测] 第1期_观察1天_逾期金额 |  |
| y1_1_1 | DOUBLE | column | [AI推测] 第1期_观察1天_逾期本金 |  |
| y2_1_1 | DOUBLE | column | [AI推测] 第1期_观察1天_逾期标识 |  |
| y3_1_1 | DOUBLE | column | [AI推测] 第1期_观察1天_逾期天数 |  |
| y0_1_2 | DOUBLE | column | [AI推测] 第1期_观察2天_逾期金额 |  |
| y1_1_2 | DOUBLE | column | [AI推测] 第1期_观察2天_逾期本金 |  |
| y2_1_2 | DOUBLE | column | [AI推测] 第1期_观察2天_逾期标识 |  |
| y3_1_2 | DOUBLE | column | [AI推测] 第1期_观察2天_逾期天数 |  |
| y0_1_3 | DOUBLE | column | [AI推测] 第1期_观察3天_逾期金额 |  |
| y1_1_3 | DOUBLE | column | [AI推测] 第1期_观察3天_逾期本金 |  |
| y2_1_3 | DOUBLE | column | [AI推测] 第1期_观察3天_逾期标识 |  |
| y3_1_3 | DOUBLE | column | [AI推测] 第1期_观察3天_逾期天数 |  |
| y0_1_4 | DOUBLE | column | [AI推测] 第1期_观察4天_逾期金额 |  |
| y1_1_4 | DOUBLE | column | [AI推测] 第1期_观察4天_逾期本金 |  |
| y2_1_4 | DOUBLE | column | [AI推测] 第1期_观察4天_逾期标识 |  |
| y3_1_4 | DOUBLE | column | [AI推测] 第1期_观察4天_逾期天数 |  |
| y0_1_7 | DOUBLE | column | [AI推测] 第1期_观察7天_逾期金额 |  |
| y1_1_7 | DOUBLE | column | [AI推测] 第1期_观察7天_逾期本金 |  |
| y2_1_7 | DOUBLE | column | [AI推测] 第1期_观察7天_逾期标识 |  |
| y3_1_7 | DOUBLE | column | [AI推测] 第1期_观察7天_逾期天数 |  |
| y0_1_15 | DOUBLE | column | [AI推测] 第1期_观察15天_逾期金额 |  |
| y1_1_15 | DOUBLE | column | [AI推测] 第1期_观察15天_逾期本金 |  |
| y2_1_15 | DOUBLE | column | [AI推测] 第1期_观察15天_逾期标识 |  |
| y3_1_15 | DOUBLE | column | [AI推测] 第1期_观察15天_逾期天数 |  |
| y0_1_30 | DOUBLE | column | [AI推测] 第1期_观察30天_逾期金额 |  |
| y1_1_30 | DOUBLE | column | [AI推测] 第1期_观察30天_逾期本金 |  |
| y2_1_30 | DOUBLE | column | [AI推测] 第1期_观察30天_逾期标识 |  |
| y3_1_30 | DOUBLE | column | [AI推测] 第1期_观察30天_逾期天数 |  |
| y4_1_30 | DOUBLE | column | [AI推测] 第1期_观察30天_各期逾期标识 |  |
| y4_2_30 | DOUBLE | column | [AI推测] 第2期_观察30天_各期逾期标识 |  |
| y4_3_30 | DOUBLE | column | [AI推测] 第3期_观察30天_各期逾期标识 |  |
| y4_4_30 | DOUBLE | column | [AI推测] 第4期_观察30天_各期逾期标识 |  |
| y4_5_30 | DOUBLE | column | [AI推测] 第5期_观察30天_各期逾期标识 |  |
| y4_6_30 | DOUBLE | column | [AI推测] 第6期_观察30天_各期逾期标识 |  |
| y4_7_30 | DOUBLE | column | [AI推测] 第7期_观察30天_各期逾期标识 |  |
| y4_8_30 | DOUBLE | column | [AI推测] 第8期_观察30天_各期逾期标识 |  |
| y4_9_30 | DOUBLE | column | [AI推测] 第9期_观察30天_各期逾期标识 |  |
| y4_10_30 | DOUBLE | column | [AI推测] 第10期_观察30天_各期逾期标识 |  |
| y4_11_30 | DOUBLE | column | [AI推测] 第11期_观察30天_各期逾期标识 |  |
| y4_12_30 | DOUBLE | column | [AI推测] 第12期_观察30天_各期逾期标识 |  |
| y0_1_60 | DOUBLE | column | [AI推测] 第1期_观察60天_逾期金额 |  |
| y1_1_60 | DOUBLE | column | [AI推测] 第1期_观察60天_逾期本金 |  |
| y2_1_60 | DOUBLE | column | [AI推测] 第1期_观察60天_逾期标识 |  |
| y3_1_60 | DOUBLE | column | [AI推测] 第1期_观察60天_逾期天数 |  |
| y0_1_90 | DOUBLE | column | [AI推测] 第1期_观察90天_逾期金额 |  |
| y1_1_90 | DOUBLE | column | [AI推测] 第1期_观察90天_逾期本金 |  |
| y2_1_90 | DOUBLE | column | [AI推测] 第1期_观察90天_逾期标识 |  |
| y3_1_90 | DOUBLE | column | [AI推测] 第1期_观察90天_逾期天数 |  |
| y0_2_7 | DOUBLE | column | [AI推测] 第2期_观察7天_逾期金额 |  |
| y1_2_7 | DOUBLE | column | [AI推测] 第2期_观察7天_逾期本金 |  |
| y2_2_7 | DOUBLE | column | [AI推测] 第2期_观察7天_逾期标识 |  |
| y3_2_7 | DOUBLE | column | [AI推测] 第2期_观察7天_逾期天数 |  |
| y0_2_15 | DOUBLE | column | [AI推测] 第2期_观察15天_逾期金额 |  |
| y1_2_15 | DOUBLE | column | [AI推测] 第2期_观察15天_逾期本金 |  |
| y2_2_15 | DOUBLE | column | [AI推测] 第2期_观察15天_逾期标识 |  |
| y3_2_15 | DOUBLE | column | [AI推测] 第2期_观察15天_逾期天数 |  |
| y0_2_30 | DOUBLE | column | [AI推测] 第2期_观察30天_逾期金额 |  |
| y1_2_30 | DOUBLE | column | [AI推测] 第2期_观察30天_逾期本金 |  |
| y2_2_30 | DOUBLE | column | [AI推测] 第2期_观察30天_逾期标识 |  |
| y3_2_30 | DOUBLE | column | [AI推测] 第2期_观察30天_逾期天数 |  |
| y0_3_7 | DOUBLE | column | [AI推测] 第3期_观察7天_逾期金额 |  |
| y1_3_7 | DOUBLE | column | [AI推测] 第3期_观察7天_逾期本金 |  |
| y2_3_7 | DOUBLE | column | [AI推测] 第3期_观察7天_逾期标识 |  |
| y3_3_7 | DOUBLE | column | [AI推测] 第3期_观察7天_逾期天数 |  |
| y0_3_15 | DOUBLE | column | [AI推测] 第3期_观察15天_逾期金额 |  |
| y1_3_15 | DOUBLE | column | [AI推测] 第3期_观察15天_逾期本金 |  |
| y2_3_15 | DOUBLE | column | [AI推测] 第3期_观察15天_逾期标识 |  |
| y3_3_15 | DOUBLE | column | [AI推测] 第3期_观察15天_逾期天数 |  |
| y0_3_30 | DOUBLE | column | [AI推测] 第3期_观察30天_逾期金额 |  |
| y1_3_30 | DOUBLE | column | [AI推测] 第3期_观察30天_逾期本金 |  |
| y2_3_30 | DOUBLE | column | [AI推测] 第3期_观察30天_逾期标识 |  |
| y3_3_30 | DOUBLE | column | [AI推测] 第3期_观察30天_逾期天数 |  |
| y0_4_7 | DOUBLE | column | [AI推测] 第4期_观察7天_逾期金额 |  |
| y1_4_7 | DOUBLE | column | [AI推测] 第4期_观察7天_逾期本金 |  |
| y2_4_7 | DOUBLE | column | [AI推测] 第4期_观察7天_逾期标识 |  |
| y3_4_7 | DOUBLE | column | [AI推测] 第4期_观察7天_逾期天数 |  |
| y0_4_30 | DOUBLE | column | [AI推测] 第4期_观察30天_逾期金额 |  |
| y1_4_30 | DOUBLE | column | [AI推测] 第4期_观察30天_逾期本金 |  |
| y2_4_30 | DOUBLE | column | [AI推测] 第4期_观察30天_逾期标识 |  |
| y3_4_30 | DOUBLE | column | [AI推测] 第4期_观察30天_逾期天数 |  |
| y0_5_7 | DOUBLE | column | [AI推测] 第5期_观察7天_逾期金额 |  |
| y1_5_7 | DOUBLE | column | [AI推测] 第5期_观察7天_逾期本金 |  |
| y2_5_7 | DOUBLE | column | [AI推测] 第5期_观察7天_逾期标识 |  |
| y3_5_7 | DOUBLE | column | [AI推测] 第5期_观察7天_逾期天数 |  |
| y0_5_30 | DOUBLE | column | [AI推测] 第5期_观察30天_逾期金额 |  |
| y1_5_30 | DOUBLE | column | [AI推测] 第5期_观察30天_逾期本金 |  |
| y2_5_30 | DOUBLE | column | [AI推测] 第5期_观察30天_逾期标识 |  |
| y3_5_30 | DOUBLE | column | [AI推测] 第5期_观察30天_逾期天数 |  |
| y0_6_7 | DOUBLE | column | [AI推测] 第6期_观察7天_逾期金额 |  |
| y1_6_7 | DOUBLE | column | [AI推测] 第6期_观察7天_逾期本金 |  |
| y2_6_7 | DOUBLE | column | [AI推测] 第6期_观察7天_逾期标识 |  |
| y3_6_7 | DOUBLE | column | [AI推测] 第6期_观察7天_逾期天数 |  |
| y0_6_30 | DOUBLE | column | [AI推测] 第6期_观察30天_逾期金额 |  |
| y1_6_30 | DOUBLE | column | [AI推测] 第6期_观察30天_逾期本金 |  |
| y2_6_30 | DOUBLE | column | [AI推测] 第6期_观察30天_逾期标识 |  |
| y3_6_30 | DOUBLE | column | [AI推测] 第6期_观察30天_逾期天数 |  |
| y0_7_7 | DOUBLE | column | [AI推测] 第7期_观察7天_逾期金额 |  |
| y1_7_7 | DOUBLE | column | [AI推测] 第7期_观察7天_逾期本金 |  |
| y2_7_7 | DOUBLE | column | [AI推测] 第7期_观察7天_逾期标识 |  |
| y3_7_7 | DOUBLE | column | [AI推测] 第7期_观察7天_逾期天数 |  |
| y0_7_30 | DOUBLE | column | [AI推测] 第7期_观察30天_逾期金额 |  |
| y1_7_30 | DOUBLE | column | [AI推测] 第7期_观察30天_逾期本金 |  |
| y2_7_30 | DOUBLE | column | [AI推测] 第7期_观察30天_逾期标识 |  |
| y3_7_30 | DOUBLE | column | [AI推测] 第7期_观察30天_逾期天数 |  |
| y0_8_7 | DOUBLE | column | [AI推测] 第8期_观察7天_逾期金额 |  |
| y1_8_7 | DOUBLE | column | [AI推测] 第8期_观察7天_逾期本金 |  |
| y2_8_7 | DOUBLE | column | [AI推测] 第8期_观察7天_逾期标识 |  |
| y3_8_7 | DOUBLE | column | [AI推测] 第8期_观察7天_逾期天数 |  |
| y0_8_30 | DOUBLE | column | [AI推测] 第8期_观察30天_逾期金额 |  |
| y1_8_30 | DOUBLE | column | [AI推测] 第8期_观察30天_逾期本金 |  |
| y2_8_30 | DOUBLE | column | [AI推测] 第8期_观察30天_逾期标识 |  |
| y3_8_30 | DOUBLE | column | [AI推测] 第8期_观察30天_逾期天数 |  |
| y0_9_7 | DOUBLE | column | [AI推测] 第9期_观察7天_逾期金额 |  |
| y1_9_7 | DOUBLE | column | [AI推测] 第9期_观察7天_逾期本金 |  |
| y2_9_7 | DOUBLE | column | [AI推测] 第9期_观察7天_逾期标识 |  |
| y3_9_7 | DOUBLE | column | [AI推测] 第9期_观察7天_逾期天数 |  |
| y0_9_30 | DOUBLE | column | [AI推测] 第9期_观察30天_逾期金额 |  |
| y1_9_30 | DOUBLE | column | [AI推测] 第9期_观察30天_逾期本金 |  |
| y2_9_30 | DOUBLE | column | [AI推测] 第9期_观察30天_逾期标识 |  |
| y3_9_30 | DOUBLE | column | [AI推测] 第9期_观察30天_逾期天数 |  |
| y0_10_7 | DOUBLE | column | [AI推测] 第10期_观察7天_逾期金额 |  |
| y1_10_7 | DOUBLE | column | [AI推测] 第10期_观察7天_逾期本金 |  |
| y2_10_7 | DOUBLE | column | [AI推测] 第10期_观察7天_逾期标识 |  |
| y3_10_7 | DOUBLE | column | [AI推测] 第10期_观察7天_逾期天数 |  |
| y0_10_30 | DOUBLE | column | [AI推测] 第10期_观察30天_逾期金额 |  |
| y1_10_30 | DOUBLE | column | [AI推测] 第10期_观察30天_逾期本金 |  |
| y2_10_30 | DOUBLE | column | [AI推测] 第10期_观察30天_逾期标识 |  |
| y3_10_30 | DOUBLE | column | [AI推测] 第10期_观察30天_逾期天数 |  |
| y0_11_7 | DOUBLE | column | [AI推测] 第11期_观察7天_逾期金额 |  |
| y1_11_7 | DOUBLE | column | [AI推测] 第11期_观察7天_逾期本金 |  |
| y2_11_7 | DOUBLE | column | [AI推测] 第11期_观察7天_逾期标识 |  |
| y3_11_7 | DOUBLE | column | [AI推测] 第11期_观察7天_逾期天数 |  |
| y0_11_30 | DOUBLE | column | [AI推测] 第11期_观察30天_逾期金额 |  |
| y1_11_30 | DOUBLE | column | [AI推测] 第11期_观察30天_逾期本金 |  |
| y2_11_30 | DOUBLE | column | [AI推测] 第11期_观察30天_逾期标识 |  |
| y3_11_30 | DOUBLE | column | [AI推测] 第11期_观察30天_逾期天数 |  |
| y0_12_7 | DOUBLE | column | [AI推测] 第12期_观察7天_逾期金额 |  |
| y1_12_7 | DOUBLE | column | [AI推测] 第12期_观察7天_逾期本金 |  |
| y2_12_7 | DOUBLE | column | [AI推测] 第12期_观察7天_逾期标识 |  |
| y3_12_7 | DOUBLE | column | [AI推测] 第12期_观察7天_逾期天数 |  |
| y0_12_30 | DOUBLE | column | [AI推测] 第12期_观察30天_逾期金额 |  |
| y1_12_30 | DOUBLE | column | [AI推测] 第12期_观察30天_逾期本金 |  |
| y2_12_30 | DOUBLE | column | [AI推测] 第12期_观察30天_逾期标识 |  |
| y3_12_30 | DOUBLE | column | [AI推测] 第12期_观察30天_逾期天数 |  |
| y0_13_30 | DOUBLE | column | [AI推测] 第13期_观察30天_逾期金额 |  |
| y1_13_30 | DOUBLE | column | [AI推测] 第13期_观察30天_逾期本金 |  |
| y3_13_30 | DOUBLE | column | [AI推测] 第13期_观察30天_逾期天数 |  |
| y0_14_30 | DOUBLE | column | [AI推测] 第14期_观察30天_逾期金额 |  |
| y1_14_30 | DOUBLE | column | [AI推测] 第14期_观察30天_逾期本金 |  |
| y3_14_30 | DOUBLE | column | [AI推测] 第14期_观察30天_逾期天数 |  |
| y0_15_30 | DOUBLE | column | [AI推测] 第15期_观察30天_逾期金额 |  |
| y1_15_30 | DOUBLE | column | [AI推测] 第15期_观察30天_逾期本金 |  |
| y3_15_30 | DOUBLE | column | [AI推测] 第15期_观察30天_逾期天数 |  |
| y0_16_30 | DOUBLE | column | [AI推测] 第16期_观察30天_逾期金额 |  |
| y1_16_30 | DOUBLE | column | [AI推测] 第16期_观察30天_逾期本金 |  |
| y3_16_30 | DOUBLE | column | [AI推测] 第16期_观察30天_逾期天数 |  |
| y0_17_30 | DOUBLE | column | [AI推测] 第17期_观察30天_逾期金额 |  |
| y1_17_30 | DOUBLE | column | [AI推测] 第17期_观察30天_逾期本金 |  |
| y3_17_30 | DOUBLE | column | [AI推测] 第17期_观察30天_逾期天数 |  |
| y0_18_30 | DOUBLE | column | [AI推测] 第18期_观察30天_逾期金额 |  |
| y1_18_30 | DOUBLE | column | [AI推测] 第18期_观察30天_逾期本金 |  |
| y3_18_30 | DOUBLE | column | [AI推测] 第18期_观察30天_逾期天数 |  |
| 定价 | INT | column | [AI推测] 定价等级（24/36） |  |
| 是否额外放开 | INT | column | [AI推测] 是否额外放开（0/1） |  |
| last_credit_succ_amt | DOUBLE | column | [AI推测] 最近一次授信成功额度 |  |

### DDL
```sql
CREATE TABLE xyf_bi.`wzq_order_table` (
  `order_number` STRING,
  `ori_order_number` STRING,
  `biz_flow_number` STRING,
  `shoufudai_cyx` STRING,
  `flow_number` STRING,
  `biz_first_created` STRING,
  `created_time_old` DATETIME,
  `created_time` DATETIME,
  `decision_time_final` DATETIME,
  `draw_day` STRING,
  `draw_week` STRING,
  `draw_month` STRING,
  `id_card_number` STRING,
  `mobile` STRING,
  `app_user_id` BIGINT,
  `cust_no` STRING,
  `app` STRING,
  `inner_app` STRING,
  `draw_chanl` STRING,
  `asset_type` BIGINT,
  `risk_price` STRING,
  `loan_type` STRING,
  `period` BIGINT,
  `loan_time` DATETIME,
  `amount` DECIMAL(38,18),
  `loan_amount` DECIMAL(38,18),
  `status` STRING,
  `risk_status` STRING,
  `remit_status` STRING,
  `failed_reason` STRING,
  `fund_source` STRING,
  `新老借款流程` STRING,
  `zs_profit_amount` STRING,
  `draw_mob_first` INT,
  `账龄` STRING,
  `first_order_number` STRING,
  `first_draw_date` DATETIME,
  `first_flag` STRING,
  `draw_chanl_1` STRING,
  `cust_type_01` STRING,
  `first_inner_app` STRING,
  `shoudaiperiod` BIGINT,
  `edu_total` DOUBLE,
  `edu_zaidai` DOUBLE,
  `edu_available` DOUBLE,
  `edu_init_credit` DOUBLE,
  `credit_expire_date` STRING,
  `edu_credit` DOUBLE,
  `edu_temp` DOUBLE,
  `rejected_1dpast` INT,
  `rejected_3dpast` INT,
  `rejected_7dpast` INT,
  `rejected_10dpast` INT,
  `rejected_14dpast` INT,
  `rejected_20dpast` INT,
  `rejected_25dpast` INT,
  `rejected_30dpast` INT,
  `rejected_60dpast` INT,
  `rejected_90dpast` INT,
  `bairong_7d_fy` DOUBLE,
  `bairong_15d_fy` DOUBLE,
  `bairong_1m_fy` DOUBLE,
  `bairong_3m_fy` DOUBLE,
  `bairong_6m_fy` DOUBLE,
  `bairong_12m_fy` DOUBLE,
  `huarong2_10` DOUBLE,
  `huarong2_17` DOUBLE,
  `huarong2_22` DOUBLE,
  `huarong2_24` DOUBLE,
  `xinyan_1` DOUBLE,
  `age` BIGINT,
  `gender` BIGINT,
  `race` STRING,
  `education` STRING,
  `marital_status` STRING,
  `monthly_income` STRING,
  `id_number_province` STRING,
  `id_number_city` STRING,
  `id_number_city_rank` STRING,
  `has_house` STRING,
  `has_car` STRING,
  `rule_set_id` STRING,
  `rule_id` STRING,
  `rule_name` STRING,
  `rule_set_name` STRING,
  `last_temp_amt_adjust_time` DATETIME,
  `rejust_date` DATETIME,
  `tiaoe_label` STRING,
  `mob` BIGINT,
  `max_overdue_days` BIGINT,
  `os` STRING,
  `source` STRING,
  `appl_chanel` STRING,
  `register_source` STRING,
  `fenzu_lb` STRING,
  `新多模型分组` STRING,
  `random_1` INT,
  `random_2` STRING,
  `decisionid` STRING,
  `personalloan_jfd_draw_creditlevel_ssrh_v2_1` DECIMAL(38,18),
  `personalloan_jfd_draw_creditlevel_ssrh_v3_2` DECIMAL(38,18),
  `personalloan_jfd_draw_creditlevel_ssrh_v3_2_1` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v2_2_3` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v2_2_4` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v4` DOUBLE,
  `多模型_cross_审批评级_v4` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v5` DOUBLE,
  `多模型_cross_审批评级_v5` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v6` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v6_2` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v7` DOUBLE,
  `personalloan_jfd_stock_creditlevel_hcrh_v2_2_2` STRING,
  `personalloan_jfd_stock_creditlevel_hcrh_v2_2_3` STRING,
  `存量v4贷中风险等级` STRING,
  `存量v5贷中风险等级` STRING,
  `存量v6贷中风险等级` STRING,
  `存量v7贷中风险等级` STRING,
  `存量v8贷中风险等级` STRING,
  `personalloan_jfd_draw_creditlevel_ssrh_v7_1` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_v8` DOUBLE,
  `personalloan_jfd_stock_creditlevel_detail_hcrh_v8_1` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_model_v9_apply` DOUBLE,
  `personalloan_jfd_draw_creditlevel_ssrh_model_v9_detail` DOUBLE,
  `personalloan_jfd_stock_creditlevel_hcrh_v9_2` STRING,
  `personalloan_jfd_stock_creditlevel_detail_hcrh_v9_2` DOUBLE,
  `personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6` DOUBLE,
  `审批评级` DOUBLE,
  `存量贷中风险等级` STRING,
  `存量贷中细分风险等级` DOUBLE,
  `personalloan_fd_creditlevel_level_user_group_v4_output` STRING,
  `personalloan_fd_creditlevel_level_user_group_v5_output` STRING,
  `提额卡用户分组` STRING,
  `tek_apl_amt_rte` DOUBLE,
  `会员卡用户分组` STRING,
  `vip_apl_amt_rte` DOUBLE,
  `飞跃会员卡用户分组` STRING,
  `fy_vip_apl_amt_rte` DOUBLE,
  `vip_fk_ord_flg_1` STRING,
  `复贷细分客群` STRING,
  `复贷客群分组` STRING,
  `复贷客群分组2` STRING,
  `飞跃客群分组` STRING,
  `risk_freeze_amt_now` STRING,
  `f_risk_freeze_amt_rate` STRING,
  `f_risk_freeze_amt_rate_group` STRING,
  `freeze_apply_flag` STRING,
  `freeze_risk_result` STRING,
  `freeze_rule_set_id` STRING,
  `freeze_rule_set_name` STRING,
  `freeze_rule_id` STRING,
  `freeze_rule_name` STRING,
  `risk_freeze_amt_after` DOUBLE,
  `freeze_order_number` STRING,
  `freeze_order_created_time` DATETIME,
  `risk_bizid` STRING,
  `ori_risk_price` STRING,
  `rh_fuzhai` DOUBLE,
  `personalloan_fd_6mceng30_xfzx_offline_v2_prob` DOUBLE,
  `y0_1_1` DOUBLE,
  `y1_1_1` DOUBLE,
  `y2_1_1` DOUBLE,
  `y3_1_1` DOUBLE,
  `y0_1_2` DOUBLE,
  `y1_1_2` DOUBLE,
  `y2_1_2` DOUBLE,
  `y3_1_2` DOUBLE,
  `y0_1_3` DOUBLE,
  `y1_1_3` DOUBLE,
  `y2_1_3` DOUBLE,
  `y3_1_3` DOUBLE,
  `y0_1_4` DOUBLE,
  `y1_1_4` DOUBLE,
  `y2_1_4` DOUBLE,
  `y3_1_4` DOUBLE,
  `y0_1_7` DOUBLE,
  `y1_1_7` DOUBLE,
  `y2_1_7` DOUBLE,
  `y3_1_7` DOUBLE,
  `y0_1_15` DOUBLE,
  `y1_1_15` DOUBLE,
  `y2_1_15` DOUBLE,
  `y3_1_15` DOUBLE,
  `y0_1_30` DOUBLE,
  `y1_1_30` DOUBLE,
  `y2_1_30` DOUBLE,
  `y3_1_30` DOUBLE,
  `y4_1_30` DOUBLE,
  `y4_2_30` DOUBLE,
  `y4_3_30` DOUBLE,
  `y4_4_30` DOUBLE,
  `y4_5_30` DOUBLE,
  `y4_6_30` DOUBLE,
  `y4_7_30` DOUBLE,
  `y4_8_30` DOUBLE,
  `y4_9_30` DOUBLE,
  `y4_10_30` DOUBLE,
  `y4_11_30` DOUBLE,
  `y4_12_30` DOUBLE,
  `y0_1_60` DOUBLE,
  `y1_1_60` DOUBLE,
  `y2_1_60` DOUBLE,
  `y3_1_60` DOUBLE,
  `y0_1_90` DOUBLE,
  `y1_1_90` DOUBLE,
  `y2_1_90` DOUBLE,
  `y3_1_90` DOUBLE,
  `y0_2_7` DOUBLE,
  `y1_2_7` DOUBLE,
  `y2_2_7` DOUBLE,
  `y3_2_7` DOUBLE,
  `y0_2_15` DOUBLE,
  `y1_2_15` DOUBLE,
  `y2_2_15` DOUBLE,
  `y3_2_15` DOUBLE,
  `y0_2_30` DOUBLE,
  `y1_2_30` DOUBLE,
  `y2_2_30` DOUBLE,
  `y3_2_30` DOUBLE,
  `y0_3_7` DOUBLE,
  `y1_3_7` DOUBLE,
  `y2_3_7` DOUBLE,
  `y3_3_7` DOUBLE,
  `y0_3_15` DOUBLE,
  `y1_3_15` DOUBLE,
  `y2_3_15` DOUBLE,
  `y3_3_15` DOUBLE,
  `y0_3_30` DOUBLE,
  `y1_3_30` DOUBLE,
  `y2_3_30` DOUBLE,
  `y3_3_30` DOUBLE,
  `y0_4_7` DOUBLE,
  `y1_4_7` DOUBLE,
  `y2_4_7` DOUBLE,
  `y3_4_7` DOUBLE,
  `y0_4_30` DOUBLE,
  `y1_4_30` DOUBLE,
  `y2_4_30` DOUBLE,
  `y3_4_30` DOUBLE,
  `y0_5_7` DOUBLE,
  `y1_5_7` DOUBLE,
  `y2_5_7` DOUBLE,
  `y3_5_7` DOUBLE,
  `y0_5_30` DOUBLE,
  `y1_5_30` DOUBLE,
  `y2_5_30` DOUBLE,
  `y3_5_30` DOUBLE,
  `y0_6_7` DOUBLE,
  `y1_6_7` DOUBLE,
  `y2_6_7` DOUBLE,
  `y3_6_7` DOUBLE,
  `y0_6_30` DOUBLE,
  `y1_6_30` DOUBLE,
  `y2_6_30` DOUBLE,
  `y3_6_30` DOUBLE,
  `y0_7_7` DOUBLE,
  `y1_7_7` DOUBLE,
  `y2_7_7` DOUBLE,
  `y3_7_7` DOUBLE,
  `y0_7_30` DOUBLE,
  `y1_7_30` DOUBLE,
  `y2_7_30` DOUBLE,
  `y3_7_30` DOUBLE,
  `y0_8_7` DOUBLE,
  `y1_8_7` DOUBLE,
  `y2_8_7` DOUBLE,
  `y3_8_7` DOUBLE,
  `y0_8_30` DOUBLE,
  `y1_8_30` DOUBLE,
  `y2_8_30` DOUBLE,
  `y3_8_30` DOUBLE,
  `y0_9_7` DOUBLE,
  `y1_9_7` DOUBLE,
  `y2_9_7` DOUBLE,
  `y3_9_7` DOUBLE,
  `y0_9_30` DOUBLE,
  `y1_9_30` DOUBLE,
  `y2_9_30` DOUBLE,
  `y3_9_30` DOUBLE,
  `y0_10_7` DOUBLE,
  `y1_10_7` DOUBLE,
  `y2_10_7` DOUBLE,
  `y3_10_7` DOUBLE,
  `y0_10_30` DOUBLE,
  `y1_10_30` DOUBLE,
  `y2_10_30` DOUBLE,
  `y3_10_30` DOUBLE,
  `y0_11_7` DOUBLE,
  `y1_11_7` DOUBLE,
  `y2_11_7` DOUBLE,
  `y3_11_7` DOUBLE,
  `y0_11_30` DOUBLE,
  `y1_11_30` DOUBLE,
  `y2_11_30` DOUBLE,
  `y3_11_30` DOUBLE,
  `y0_12_7` DOUBLE,
  `y1_12_7` DOUBLE,
  `y2_12_7` DOUBLE,
  `y3_12_7` DOUBLE,
  `y0_12_30` DOUBLE,
  `y1_12_30` DOUBLE,
  `y2_12_30` DOUBLE,
  `y3_12_30` DOUBLE,
  `y0_13_30` DOUBLE,
  `y1_13_30` DOUBLE,
  `y3_13_30` DOUBLE,
  `y0_14_30` DOUBLE,
  `y1_14_30` DOUBLE,
  `y3_14_30` DOUBLE,
  `y0_15_30` DOUBLE,
  `y1_15_30` DOUBLE,
  `y3_15_30` DOUBLE,
  `y0_16_30` DOUBLE,
  `y1_16_30` DOUBLE,
  `y3_16_30` DOUBLE,
  `y0_17_30` DOUBLE,
  `y1_17_30` DOUBLE,
  `y3_17_30` DOUBLE,
  `y0_18_30` DOUBLE,
  `y1_18_30` DOUBLE,
  `y3_18_30` DOUBLE,
  `定价` INT,
  `是否额外放开` INT,
  `last_credit_succ_amt` DOUBLE
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

## 抽样数据
| order_number | ori_order_number | biz_flow_number | shoufudai_cyx | flow_number | biz_first_created | created_time_old | created_time | decision_time_final | draw_day | draw_week | draw_month | id_card_number | mobile | app_user_id | cust_no | app | inner_app | draw_chanl | asset_type | risk_price | loan_type | period | loan_time | amount | loan_amount | status | risk_status | remit_status | failed_reason | fund_source | 新老借款流程 | zs_profit_amount | draw_mob_first | 账龄 | first_order_number | first_draw_date | first_flag | draw_chanl_1 | cust_type_01 | first_inner_app | shoudaiperiod | edu_total | edu_zaidai | edu_available | edu_init_credit | credit_expire_date | edu_credit | edu_temp | rejected_1dpast | rejected_3dpast | rejected_7dpast | rejected_10dpast | rejected_14dpast | rejected_20dpast | rejected_25dpast | rejected_30dpast | rejected_60dpast | rejected_90dpast | bairong_7d_fy | bairong_15d_fy | bairong_1m_fy | bairong_3m_fy | bairong_6m_fy | bairong_12m_fy | huarong2_10 | huarong2_17 | huarong2_22 | huarong2_24 | xinyan_1 | age | gender | race | education | marital_status | monthly_income | id_number_province | id_number_city | id_number_city_rank | has_house | has_car | rule_set_id | rule_id | rule_name | rule_set_name | last_temp_amt_adjust_time | rejust_date | tiaoe_label | mob | max_overdue_days | os | source | appl_chanel | register_source | fenzu_lb | 新多模型分组 | random_1 | random_2 | decisionid | personalloan_jfd_draw_creditlevel_ssrh_v2_1 | personalloan_jfd_draw_creditlevel_ssrh_v3_2 | personalloan_jfd_draw_creditlevel_ssrh_v3_2_1 | personalloan_jfd_draw_creditlevel_ssrh_v2_2_3 | personalloan_jfd_draw_creditlevel_ssrh_v2_2_4 | personalloan_jfd_draw_creditlevel_ssrh_v4 | 多模型_cross_审批评级_v4 | personalloan_jfd_draw_creditlevel_ssrh_v5 | 多模型_cross_审批评级_v5 | personalloan_jfd_draw_creditlevel_ssrh_v6 | personalloan_jfd_draw_creditlevel_ssrh_v6_2 | personalloan_jfd_draw_creditlevel_ssrh_v7 | personalloan_jfd_stock_creditlevel_hcrh_v2_2_2 | personalloan_jfd_stock_creditlevel_hcrh_v2_2_3 | 存量v4贷中风险等级 | 存量v5贷中风险等级 | 存量v6贷中风险等级 | 存量v7贷中风险等级 | 存量v8贷中风险等级 | personalloan_jfd_draw_creditlevel_ssrh_v7_1 | personalloan_jfd_draw_creditlevel_ssrh_v8 | personalloan_jfd_stock_creditlevel_detail_hcrh_v8_1 | personalloan_jfd_draw_creditlevel_ssrh_model_v9_apply | personalloan_jfd_draw_creditlevel_ssrh_model_v9_detail | personalloan_jfd_stock_creditlevel_hcrh_v9_2 | personalloan_jfd_stock_creditlevel_detail_hcrh_v9_2 | personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | 审批评级 | 存量贷中风险等级 | 存量贷中细分风险等级 | personalloan_fd_creditlevel_level_user_group_v4_output | personalloan_fd_creditlevel_level_user_group_v5_output | 提额卡用户分组 | tek_apl_amt_rte | 会员卡用户分组 | vip_apl_amt_rte | 飞跃会员卡用户分组 | fy_vip_apl_amt_rte | vip_fk_ord_flg_1 | 复贷细分客群 | 复贷客群分组 | 复贷客群分组2 | 飞跃客群分组 | risk_freeze_amt_now | f_risk_freeze_amt_rate | f_risk_freeze_amt_rate_group | freeze_apply_flag | freeze_risk_result | freeze_rule_set_id | freeze_rule_set_name | freeze_rule_id | freeze_rule_name | risk_freeze_amt_after | freeze_order_number | freeze_order_created_time | risk_bizid | ori_risk_price | rh_fuzhai | personalloan_fd_6mceng30_xfzx_offline_v2_prob | y0_1_1 | y1_1_1 | y2_1_1 | y3_1_1 | y0_1_2 | y1_1_2 | y2_1_2 | y3_1_2 | y0_1_3 | y1_1_3 | y2_1_3 | y3_1_3 | y0_1_4 | y1_1_4 | y2_1_4 | y3_1_4 | y0_1_7 | y1_1_7 | y2_1_7 | y3_1_7 | y0_1_15 | y1_1_15 | y2_1_15 | y3_1_15 | y0_1_30 | y1_1_30 | y2_1_30 | y3_1_30 | y4_1_30 | y4_2_30 | y4_3_30 | y4_4_30 | y4_5_30 | y4_6_30 | y4_7_30 | y4_8_30 | y4_9_30 | y4_10_30 | y4_11_30 | y4_12_30 | y0_1_60 | y1_1_60 | y2_1_60 | y3_1_60 | y0_1_90 | y1_1_90 | y2_1_90 | y3_1_90 | y0_2_7 | y1_2_7 | y2_2_7 | y3_2_7 | y0_2_15 | y1_2_15 | y2_2_15 | y3_2_15 | y0_2_30 | y1_2_30 | y2_2_30 | y3_2_30 | y0_3_7 | y1_3_7 | y2_3_7 | y3_3_7 | y0_3_15 | y1_3_15 | y2_3_15 | y3_3_15 | y0_3_30 | y1_3_30 | y2_3_30 | y3_3_30 | y0_4_7 | y1_4_7 | y2_4_7 | y3_4_7 | y0_4_30 | y1_4_30 | y2_4_30 | y3_4_30 | y0_5_7 | y1_5_7 | y2_5_7 | y3_5_7 | y0_5_30 | y1_5_30 | y2_5_30 | y3_5_30 | y0_6_7 | y1_6_7 | y2_6_7 | y3_6_7 | y0_6_30 | y1_6_30 | y2_6_30 | y3_6_30 | y0_7_7 | y1_7_7 | y2_7_7 | y3_7_7 | y0_7_30 | y1_7_30 | y2_7_30 | y3_7_30 | y0_8_7 | y1_8_7 | y2_8_7 | y3_8_7 | y0_8_30 | y1_8_30 | y2_8_30 | y3_8_30 | y0_9_7 | y1_9_7 | y2_9_7 | y3_9_7 | y0_9_30 | y1_9_30 | y2_9_30 | y3_9_30 | y0_10_7 | y1_10_7 | y2_10_7 | y3_10_7 | y0_10_30 | y1_10_30 | y2_10_30 | y3_10_30 | y0_11_7 | y1_11_7 | y2_11_7 | y3_11_7 | y0_11_30 | y1_11_30 | y2_11_30 | y3_11_30 | y0_12_7 | y1_12_7 | y2_12_7 | y3_12_7 | y0_12_30 | y1_12_30 | y2_12_30 | y3_12_30 | y0_13_30 | y1_13_30 | y3_13_30 | y0_14_30 | y1_14_30 | y3_14_30 | y0_15_30 | y1_15_30 | y3_15_30 | y0_16_30 | y1_16_30 | y3_16_30 | y0_17_30 | y1_17_30 | y3_17_30 | y0_18_30 | y1_18_30 | y3_18_30 | 定价 | 是否额外放开 | last_credit_succ_amt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20170626082809100006801 |  | 201706260828091014727 | 首贷 |  | 201706260828091014727 | 2017-06-26 08:28:09 | 2017-06-26 08:28:09 |  | 2017-06-26 | 2017-06-23 | 2017-06 | tnVulFHyGNugKJxEuIlqbbugQDzASj3uvj+XcQP7v8M= | GHhSadpMWXajpIP04oSppQ== | 1307310 | CTL06f225657afc8f9d19c3af476774ce0c9 | xyf | xyf | APP流量 |  | I36 | cash_loan | 12 |  | 1800000 | 0 | reject |  | none | 提现时命中黑名单 |  |  |  | -23 | 短账龄 |  | 2017-07-19 03:06:18 | 其他 | APP流量 | 首借APP | xyf | -1 |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 流程中 |  |  | 非调额组 |  |  |  | ios | 其他 | APP流量 | 无分组 | 其他 | 92 | 9223586158617613820116292656342392899269213962992680203304521106215069297225472647384874013852967918 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非额外放开 | 无APP放款 | 老客其他 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 0 | 0.0 |
| 20170713065414011000340 |  | 201707130654141028553 | 首贷 |  | 201707130654141028553 | 2017-07-13 06:54:14 | 2017-07-13 06:54:14 |  | 2017-07-13 | 2017-07-07 | 2017-07 | MgpZH2wGaSSUiaXKOvsWQfmvSgJ4klTYV3mA/iki1QE= | aS/V3bMUcTy7YvCgo8GJIQ== | 1231028 | CTL0c0d8f6dcfcd234f5b17796cf441e11c8 | xyf | xyf | APP流量 |  | I36 | cash_loan | 9 |  | 900000 | 0 | reject | reject | none | 002:命中提现时风控策略 |  |  |  | -247 | 短账龄 |  | 2018-03-17 21:13:49 | 其他 | APP流量 | 首借APP | xyf | -1 |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非调额组 |  |  |  | android | 其他 | APP流量 | 无分组 | 其他 | 92 | 9242201804262613201038197459484106148062308711886374448749560860596999488319280848426047633218867393 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非额外放开 | 无APP放款 | 老客其他 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 0 | 0.0 |
| 20170723133508011000803 |  | 201707231335081036054 | 首贷 |  | 201707231335081036054 | 2017-07-23 13:35:08 | 2017-07-23 13:35:08 |  | 2017-07-23 | 2017-07-21 | 2017-07 | bbhAPZRuUsVpNUk36MO8AftpOL3zZcYk8ZTatJOzibo= | jgCYG6Q0llH7PTaEQZV/1g== | 1349103 | CTL09aed906d3c79cc0e5a4511e4ded11b19 | xyf | xyf | APP流量 |  | I36 | cash_loan | 6 |  | 500000 | 0 | reject | reject | none | reject\|汪晨 |  |  |  |  | 短账龄 |  |  | 其他 |  |  |  | -1 |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非调额组 |  |  |  | android | 其他 | APP流量 | 无分组 | 其他 | 46 | 4600834964358253666987961723657325152748871682760093397705870548884706153103257844401350292143302828 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非额外放开 | 无APP放款 | 老客其他 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 0 | 0.0 |
| 20170723145931011000807 |  | 201707231459311036093 | 加复贷 |  | 201707231459311036093 | 2017-07-23 14:59:31 | 2017-07-23 14:59:31 |  | 2017-07-23 | 2017-07-21 | 2017-07 | EaBBfYr3LTu3ibvz3ZAZOTF0jz7Ep2o81tpmZnP/I7s= | 56WTi466CZiU5IuVJivhYA== | 1355549 | CTL046b69659877487fcc66748202a618346 | xyf | xyf | APP流量 |  | I36 | cash_loan | 3 |  | 150000 | 0 | reject | reject | none | reject\|汪晨 |  |  |  | 2 | 短账龄 |  | 2017-07-21 14:38:17 | 其他 | APP流量 | 首借APP | xyf | 0 |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非调额组 |  |  |  | android | 其他 | APP流量 | 无分组 | 其他 | 74 | 7467769775617323305403115817586056548737921110333059122983907639004508516384706635262790295787176916 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非额外放开 | 无APP放款 | 老客其他 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 0 | 0.0 |
| 20170728205237011001051 |  | 201707282052371039665 | 加复贷 |  | 201707282052371039665 | 2017-07-28 20:52:37 | 2017-07-28 20:52:37 |  | 2017-07-28 | 2017-07-28 | 2017-07 | T9vgnf2I7iJgpbZA9Rx2Hqppk2T0MenaeSjnusABWGY= | DfnXgbCjSuj4XXdZSc+rqA== | 1114330 | CTL0af9b84bb9672354cf59cade2943a2651 | xyf | xyf | APP流量 |  | I36 | cash_loan | 1 |  | 300000 | 0 | reject | reject | none | reject\|汪晨 |  |  |  | 11 | 短账龄 |  | 2017-07-17 22:36:23 | 其他 | APP流量 | 首借APP | xyf | 1 |  |  |  |  |  |  |  | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非调额组 |  |  |  | android | 其他 | APP流量 | 无分组 | 其他 | 78 | 7868665531021463104138724333383530626625700101495676153705223014154570268002696415418956538189725949 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 非额外放开 | 无APP放款 | 老客其他 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 36 | 0 | 0.0 |

## 同步来源
- `odps`
