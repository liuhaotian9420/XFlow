# xyf_fengkong_dev.wzq_order_b5_b4_compare_base

## 来源文件
- 老客月会sql代码.ipynb

- `DISTINCT order_number`

### 表结构
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
| marital_status | STRING | column | [AI推测] 婚姻状况 |  |
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
| personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | DOUBLE | column | [AI推测] 个人贷存量信用等级明细_回查人行_V6起 |  |
| 审批评级 | DOUBLE | column | [AI推测] 审批评级分数 |  |
| 存量贷中风险等级 | STRING | column | [AI推测] 当前存量贷中风险等级 |  |
| personalloan_fd_creditlevel_level_user_group_v4_output | STRING | column | [AI推测] 个人贷信用等级用户分组_v4_输出 |  |
| personalloan_fd_creditlevel_level_user_group_v5_output | STRING | column | [AI推测] 个人贷信用等级用户分组_v5_输出 |  |
| 提额卡用户分组 | STRING | column | [AI推测] 提额卡用户分组 |  |
| 会员卡用户分组 | STRING | column | [AI推测] 会员卡用户分组 |  |
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
| apisd_appfd_flag | INT | column | [AI推测] API审批/APP风控标记 |  |
| decisionid | STRING | column | [AI推测] 决策引擎ID |  |
| decision_time | DATETIME | column | [AI推测] 决策时间 |  |
| result | STRING | column | [AI推测] 决策结果 |  |
| context | STRING | column | [AI推测] 决策上下文 |  |
| track | STRING | column | [AI推测] 决策跟踪信息 |  |
| result_v5_old | STRING | column | [AI推测] v5版本旧策略决策结果 |  |
| result_v4_old | STRING | column | [AI推测] v4版本旧策略决策结果 |  |
| result_v5_tek | STRING | column | [AI推测] v5版本提额卡决策结果 |  |
| result_v4_tek | STRING | column | [AI推测] v4版本提额卡决策结果 |  |
| result_v5_vip | STRING | column | [AI推测] v5版本VIP决策结果 |  |
| result_v4_vip | STRING | column | [AI推测] v4版本VIP决策结果 |  |
| decision_date | DATE | column | [AI推测] 决策日期 |  |
| cross_api_12_b4 | STRING | column | [AI推测] API交叉评级_12期_b4 |  |
| cross_api_6_b4 | STRING | column | [AI推测] API交叉评级_6期_b4 |  |
| cross_api_3_b4 | STRING | column | [AI推测] API交叉评级_3期_b4 |  |
| cross_12_b4 | STRING | column | [AI推测] 交叉评级_12期_b4 |  |
| cross_6_b4 | STRING | column | [AI推测] 交叉评级_6期_b4 |  |
| cross_3_b4 | STRING | column | [AI推测] 交叉评级_3期_b4 |  |
| cross_vip_12_b4 | STRING | column | [AI推测] VIP交叉评级_12期_b4 |  |
| cross_vip_6_b4 | STRING | column | [AI推测] VIP交叉评级_6期_b4 |  |
| cross_vip_3_b4 | STRING | column | [AI推测] VIP交叉评级_3期_b4 |  |
| cross_tek_12_b4 | STRING | column | [AI推测] 提额卡交叉评级_12期_b4 |  |
| cross_tek_6_b4 | STRING | column | [AI推测] 提额卡交叉评级_6期_b4 |  |
| cross_tek_3_b4 | STRING | column | [AI推测] 提额卡交叉评级_3期_b4 |  |
| cross_result_v4 | STRING | column | [AI推测] 交叉评级最终结果_V4 |  |
| cross_result_v4_vip | STRING | column | [AI推测] VIP交叉评级最终结果_V4 |  |
| cross_result_v4_tek | STRING | column | [AI推测] 提额卡交叉评级最终结果_V4 |  |
| new_ssrh_b4 | STRING | column | [AI推测] 新实时人行评级_b4 |  |
| hcrh_b4 | STRING | column | [AI推测] 回查人行评级_b4 |  |
| cross_api_12_b5 | STRING | column | [AI推测] API交叉评级_12期_b5 |  |
| cross_api_6_b5 | STRING | column | [AI推测] API交叉评级_6期_b5 |  |
| cross_api_3_b5 | STRING | column | [AI推测] API交叉评级_3期_b5 |  |
| cross_12_b5 | STRING | column | [AI推测] 交叉评级_12期_b5 |  |
| cross_6_b5 | STRING | column | [AI推测] 交叉评级_6期_b5 |  |
| cross_3_b5 | STRING | column | [AI推测] 交叉评级_3期_b5 |  |
| cross_vip_12_b5 | STRING | column | [AI推测] VIP交叉评级_12期_b5 |  |
| cross_vip_6_b5 | STRING | column | [AI推测] VIP交叉评级_6期_b5 |  |
| cross_vip_3_b5 | STRING | column | [AI推测] VIP交叉评级_3期_b5 |  |
| cross_tek_12_b5 | STRING | column | [AI推测] 提额卡交叉评级_12期_b5 |  |
| cross_tek_6_b5 | STRING | column | [AI推测] 提额卡交叉评级_6期_b5 |  |
| cross_tek_3_b5 | STRING | column | [AI推测] 提额卡交叉评级_3期_b5 |  |
| cross_result_v5 | STRING | column | [AI推测] 交叉评级最终结果_V5 |  |
| cross_result_v5_vip | STRING | column | [AI推测] VIP交叉评级最终结果_V5 |  |
| cross_result_v5_tek | STRING | column | [AI推测] 提额卡交叉评级最终结果_V5 |  |
| new_ssrh_b5 | STRING | column | [AI推测] 新实时人行评级_b5 |  |
| hcrh_b5 | STRING | column | [AI推测] 回查人行评级_b5 |  |
| cross_api_12_b4_adj | STRING | column | [AI推测] API交叉评级_12期_b4_调整后 |  |
| cross_api_6_b4_adj | STRING | column | [AI推测] API交叉评级_6期_b4_调整后 |  |
| cross_api_3_b4_adj | STRING | column | [AI推测] API交叉评级_3期_b4_调整后 |  |
| cross_api_12_b5_adj | STRING | column | [AI推测] API交叉评级_12期_b5_调整后 |  |
| cross_api_6_b5_adj | STRING | column | [AI推测] API交叉评级_6期_b5_调整后 |  |
| cross_api_3_b5_adj | STRING | column | [AI推测] API交叉评级_3期_b5_调整后 |  |
| v4_laohui_tag | STRING | column | [AI推测] v4版本老客回流标签 |  |
| v5_laohui_tag | STRING | column | [AI推测] v5版本老客回流标签 |  |
| v4_laohui_tag_tek | STRING | column | [AI推测] v4版本提额卡老客回流标签 |  |
| v5_laohui_tag_tek | STRING | column | [AI推测] v5版本提额卡老客回流标签 |  |
| v4_laohui_tag_vip | STRING | column | [AI推测] v4版本VIP老客回流标签 |  |
| v5_laohui_tag_vip | STRING | column | [AI推测] v5版本VIP老客回流标签 |  |
| tek_apl_amt_rte | STRING | column | [AI推测] 提额卡申请金额费率 |  |
| vip_apl_amt_rte | STRING | column | [AI推测] VIP申请金额费率 |  |
| vip_tek_apl_amt_rte_max | STRING | column | [AI推测] VIP与提额卡申请费率取大值 |  |
| vip_tek_dec_grp_reloan | STRING | column | [AI推测] VIP提额卡决策分组_复贷 |  |
| order_amount | STRING | column | [AI推测] 订单金额 |  |
| result_v4 | STRING | column | [AI推测] v4版本决策结果 |  |
| result_v5 | STRING | column | [AI推测] v5版本决策结果 |  |
| model_result_v4 | STRING | column | [AI推测] v4版本模型决策结果 |  |
| model_result_v5 | STRING | column | [AI推测] v5版本模型决策结果 |  |
| v4_laohui_tag_total | STRING | column | [AI推测] v4版本老客回流标签_汇总 |  |
| v5_laohui_tag_total | STRING | column | [AI推测] v5版本老客回流标签_汇总 |  |
| 审批评级_多模型 | STRING | column | [AI推测] 审批评级_多模型版本 |  |
| 存量评级 | STRING | column | [AI推测] 存量评级等级 |  |
| swap_tag | STRING | column | [AI推测] 策略互换标签 |  |
| swap_tag_model | STRING | column | [AI推测] 模型互换标签 |  |
| 会员卡分组 | STRING | column | [AI推测] 会员卡策略分组 |  |
| 提额卡分组 | STRING | column | [AI推测] 提额卡策略分组 |  |
| 权益卡分组 | STRING | column | [AI推测] 权益卡策略分组 |  |
| 边界分组_v4 | STRING | column | [AI推测] 边界策略分组_v4 |  |
| 边界分组_v5 | STRING | column | [AI推测] 边界策略分组_v5 |  |
| cross结果_v4 | STRING | column | [AI推测] 交叉评级结果_v4 |  |
| cross结果_v5 | STRING | column | [AI推测] 交叉评级结果_v5 |  |
| 边界分组 | STRING | column | [AI推测] 边界策略分组 |  |
| cross结果 | STRING | column | [AI推测] 交叉评级结果 |  |
| 老客客群分组 | STRING | column | [AI推测] 老客客群分组 |  |
| 老客客群分组_old | STRING | column | [AI推测] 老客客群分组（旧版） |  |
| 策略版本 | STRING | column | [AI推测] 策略版本号 |  |
| personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob | DOUBLE | column | [AI推测] 个人贷6个月层30天无自营LGB人行模型概率_V2 |  |
| rh_good_label | STRING | column | [AI推测] 人行好人标签 |  |
| bairong_als_402 | DOUBLE | column | [AI推测] 百融ALS特征_402 |  |
| monthly_income | STRING | column | [AI推测] 月收入 |  |
| education | STRING | column | [AI推测] 学历 |  |
| 收入 | INT | column | [AI推测] 收入评分 |  |
| 学历 | INT | column | [AI推测] 学历评分 |  |
| label_sum_wgt_app | DOUBLE | column | [AI推测] APP标签加权总分 |  |
| label_sum_wgt_api | DOUBLE | column | [AI推测] API标签加权总分 |  |
| label_sum_wgt | DOUBLE | column | [AI推测] 标签加权总分 |  |

#### DDL
```sql
CREATE TABLE xyf_fengkong_dev.`wzq_order_b5_b4_compare_base` (
  `order_number` STRING,
  `ori_order_number` STRING,
  `biz_flow_number` STRING,
  `shoufudai_cyx` STRING,
  `flow_number` STRING,
  `biz_first_created` STRING,
  `created_time_old` DATETIME,
  `created_time` DATETIME,
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
  `marital_status` STRING,
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
  `personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6` DOUBLE,
  `审批评级` DOUBLE,
  `存量贷中风险等级` STRING,
  `personalloan_fd_creditlevel_level_user_group_v4_output` STRING,
  `personalloan_fd_creditlevel_level_user_group_v5_output` STRING,
  `提额卡用户分组` STRING,
  `会员卡用户分组` STRING,
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
  `apisd_appfd_flag` INT,
  `decisionid` STRING,
  `decision_time` DATETIME,
  `result` STRING,
  `context` STRING,
  `track` STRING,
  `result_v5_old` STRING,
  `result_v4_old` STRING,
  `result_v5_tek` STRING,
  `result_v4_tek` STRING,
  `result_v5_vip` STRING,
  `result_v4_vip` STRING,
  `decision_date` DATE,
  `cross_api_12_b4` STRING,
  `cross_api_6_b4` STRING,
  `cross_api_3_b4` STRING,
  `cross_12_b4` STRING,
  `cross_6_b4` STRING,
  `cross_3_b4` STRING,
  `cross_vip_12_b4` STRING,
  `cross_vip_6_b4` STRING,
  `cross_vip_3_b4` STRING,
  `cross_tek_12_b4` STRING,
  `cross_tek_6_b4` STRING,
  `cross_tek_3_b4` STRING,
  `cross_result_v4` STRING,
  `cross_result_v4_vip` STRING,
  `cross_result_v4_tek` STRING,
  `new_ssrh_b4` STRING,
  `hcrh_b4` STRING,
  `cross_api_12_b5` STRING,
  `cross_api_6_b5` STRING,
  `cross_api_3_b5` STRING,
  `cross_12_b5` STRING,
  `cross_6_b5` STRING,
  `cross_3_b5` STRING,
  `cross_vip_12_b5` STRING,
  `cross_vip_6_b5` STRING,
  `cross_vip_3_b5` STRING,
  `cross_tek_12_b5` STRING,
  `cross_tek_6_b5` STRING,
  `cross_tek_3_b5` STRING,
  `cross_result_v5` STRING,
  `cross_result_v5_vip` STRING,
  `cross_result_v5_tek` STRING,
  `new_ssrh_b5` STRING,
  `hcrh_b5` STRING,
  `cross_api_12_b4_adj` STRING,
  `cross_api_6_b4_adj` STRING,
  `cross_api_3_b4_adj` STRING,
  `cross_api_12_b5_adj` STRING,
  `cross_api_6_b5_adj` STRING,
  `cross_api_3_b5_adj` STRING,
  `v4_laohui_tag` STRING,
  `v5_laohui_tag` STRING,
  `v4_laohui_tag_tek` STRING,
  `v5_laohui_tag_tek` STRING,
  `v4_laohui_tag_vip` STRING,
  `v5_laohui_tag_vip` STRING,
  `tek_apl_amt_rte` STRING,
  `vip_apl_amt_rte` STRING,
  `vip_tek_apl_amt_rte_max` STRING,
  `vip_tek_dec_grp_reloan` STRING,
  `order_amount` STRING,
  `result_v4` STRING,
  `result_v5` STRING,
  `model_result_v4` STRING,
  `model_result_v5` STRING,
  `v4_laohui_tag_total` STRING,
  `v5_laohui_tag_total` STRING,
  `审批评级_多模型` STRING,
  `存量评级` STRING,
  `swap_tag` STRING,
  `swap_tag_model` STRING,
  `会员卡分组` STRING,
  `提额卡分组` STRING,
  `权益卡分组` STRING,
  `边界分组_v4` STRING,
  `边界分组_v5` STRING,
  `cross结果_v4` STRING,
  `cross结果_v5` STRING,
  `边界分组` STRING,
  `cross结果` STRING,
  `老客客群分组` STRING,
  `老客客群分组_old` STRING,
  `策略版本` STRING,
  `personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob` DOUBLE,
  `rh_good_label` STRING,
  `bairong_als_402` DOUBLE,
  `monthly_income` STRING,
  `education` STRING,
  `收入` INT,
  `学历` INT,
  `label_sum_wgt_app` DOUBLE,
  `label_sum_wgt_api` DOUBLE,
  `label_sum_wgt` DOUBLE
)
TBLPROPERTIES (
  'storagetier' = 'standard'
)
STORED AS AliOrc
```

### 抽样数据
| order_number | ori_order_number | biz_flow_number | shoufudai_cyx | flow_number | biz_first_created | created_time_old | created_time | draw_day | draw_week | draw_month | id_card_number | mobile | app_user_id | cust_no | app | inner_app | draw_chanl | asset_type | risk_price | loan_type | period | loan_time | amount | status | risk_status | remit_status | failed_reason | fund_source | 新老借款流程 | zs_profit_amount | draw_mob_first | 账龄 | first_order_number | first_draw_date | first_flag | draw_chanl_1 | cust_type_01 | first_inner_app | shoudaiperiod | edu_total | edu_zaidai | edu_available | edu_init_credit | credit_expire_date | edu_credit | edu_temp | rejected_1dpast | rejected_3dpast | rejected_7dpast | rejected_10dpast | rejected_14dpast | rejected_20dpast | rejected_25dpast | rejected_30dpast | rejected_60dpast | rejected_90dpast | bairong_7d_fy | bairong_15d_fy | bairong_1m_fy | bairong_3m_fy | bairong_6m_fy | bairong_12m_fy | huarong2_10 | huarong2_17 | huarong2_22 | huarong2_24 | xinyan_1 | age | gender | race | marital_status | id_number_province | id_number_city | id_number_city_rank | has_house | has_car | rule_set_id | rule_id | rule_name | rule_set_name | last_temp_amt_adjust_time | rejust_date | tiaoe_label | mob | max_overdue_days | os | source | appl_chanel | register_source | fenzu_lb | 新多模型分组 | random_1 | random_2 | personalloan_jfd_draw_creditlevel_ssrh_v2_1 | personalloan_jfd_draw_creditlevel_ssrh_v3_2 | personalloan_jfd_draw_creditlevel_ssrh_v3_2_1 | personalloan_jfd_draw_creditlevel_ssrh_v2_2_3 | personalloan_jfd_draw_creditlevel_ssrh_v2_2_4 | personalloan_jfd_draw_creditlevel_ssrh_v4 | 多模型_cross_审批评级_v4 | personalloan_jfd_draw_creditlevel_ssrh_v5 | 多模型_cross_审批评级_v5 | personalloan_jfd_draw_creditlevel_ssrh_v6 | personalloan_jfd_draw_creditlevel_ssrh_v6_2 | personalloan_jfd_draw_creditlevel_ssrh_v7 | personalloan_jfd_stock_creditlevel_hcrh_v2_2_2 | personalloan_jfd_stock_creditlevel_hcrh_v2_2_3 | 存量v4贷中风险等级 | 存量v5贷中风险等级 | 存量v6贷中风险等级 | 存量v7贷中风险等级 | 存量v8贷中风险等级 | personalloan_jfd_draw_creditlevel_ssrh_v7_1 | personalloan_jfd_draw_creditlevel_ssrh_v8 | personalloan_jfd_stock_creditlevel_detail_hcrh_start_from_v6 | 审批评级 | 存量贷中风险等级 | personalloan_fd_creditlevel_level_user_group_v4_output | personalloan_fd_creditlevel_level_user_group_v5_output | 提额卡用户分组 | 会员卡用户分组 | 飞跃会员卡用户分组 | fy_vip_apl_amt_rte | vip_fk_ord_flg_1 | 复贷细分客群 | 复贷客群分组 | 复贷客群分组2 | 飞跃客群分组 | risk_freeze_amt_now | f_risk_freeze_amt_rate | f_risk_freeze_amt_rate_group | freeze_apply_flag | freeze_risk_result | freeze_rule_set_id | freeze_rule_set_name | freeze_rule_id | freeze_rule_name | risk_freeze_amt_after | freeze_order_number | freeze_order_created_time | y0_1_1 | y1_1_1 | y2_1_1 | y3_1_1 | y0_1_2 | y1_1_2 | y2_1_2 | y3_1_2 | y0_1_3 | y1_1_3 | y2_1_3 | y3_1_3 | y0_1_4 | y1_1_4 | y2_1_4 | y3_1_4 | y0_1_7 | y1_1_7 | y2_1_7 | y3_1_7 | y0_1_15 | y1_1_15 | y2_1_15 | y3_1_15 | y0_1_30 | y1_1_30 | y2_1_30 | y3_1_30 | y4_1_30 | y4_2_30 | y4_3_30 | y4_4_30 | y4_5_30 | y4_6_30 | y4_7_30 | y4_8_30 | y4_9_30 | y4_10_30 | y4_11_30 | y4_12_30 | y0_1_60 | y1_1_60 | y2_1_60 | y3_1_60 | y0_1_90 | y1_1_90 | y2_1_90 | y3_1_90 | y0_2_7 | y1_2_7 | y2_2_7 | y3_2_7 | y0_2_15 | y1_2_15 | y2_2_15 | y3_2_15 | y0_2_30 | y1_2_30 | y2_2_30 | y3_2_30 | y0_3_7 | y1_3_7 | y2_3_7 | y3_3_7 | y0_3_15 | y1_3_15 | y2_3_15 | y3_3_15 | y0_3_30 | y1_3_30 | y2_3_30 | y3_3_30 | y0_4_7 | y1_4_7 | y2_4_7 | y3_4_7 | y0_4_30 | y1_4_30 | y2_4_30 | y3_4_30 | y0_5_7 | y1_5_7 | y2_5_7 | y3_5_7 | y0_5_30 | y1_5_30 | y2_5_30 | y3_5_30 | y0_6_7 | y1_6_7 | y2_6_7 | y3_6_7 | y0_6_30 | y1_6_30 | y2_6_30 | y3_6_30 | y0_7_7 | y1_7_7 | y2_7_7 | y3_7_7 | y0_7_30 | y1_7_30 | y2_7_30 | y3_7_30 | y0_8_7 | y1_8_7 | y2_8_7 | y3_8_7 | y0_8_30 | y1_8_30 | y2_8_30 | y3_8_30 | y0_9_7 | y1_9_7 | y2_9_7 | y3_9_7 | y0_9_30 | y1_9_30 | y2_9_30 | y3_9_30 | y0_10_7 | y1_10_7 | y2_10_7 | y3_10_7 | y0_10_30 | y1_10_30 | y2_10_30 | y3_10_30 | y0_11_7 | y1_11_7 | y2_11_7 | y3_11_7 | y0_11_30 | y1_11_30 | y2_11_30 | y3_11_30 | y0_12_7 | y1_12_7 | y2_12_7 | y3_12_7 | y0_12_30 | y1_12_30 | y2_12_30 | y3_12_30 | y0_13_30 | y1_13_30 | y3_13_30 | y0_14_30 | y1_14_30 | y3_14_30 | y0_15_30 | y1_15_30 | y3_15_30 | y0_16_30 | y1_16_30 | y3_16_30 | y0_17_30 | y1_17_30 | y3_17_30 | y0_18_30 | y1_18_30 | y3_18_30 | apisd_appfd_flag | decisionid | decision_time | result | context | track | result_v5_old | result_v4_old | result_v5_tek | result_v4_tek | result_v5_vip | result_v4_vip | decision_date | cross_api_12_b4 | cross_api_6_b4 | cross_api_3_b4 | cross_12_b4 | cross_6_b4 | cross_3_b4 | cross_vip_12_b4 | cross_vip_6_b4 | cross_vip_3_b4 | cross_tek_12_b4 | cross_tek_6_b4 | cross_tek_3_b4 | cross_result_v4 | cross_result_v4_vip | cross_result_v4_tek | new_ssrh_b4 | hcrh_b4 | cross_api_12_b5 | cross_api_6_b5 | cross_api_3_b5 | cross_12_b5 | cross_6_b5 | cross_3_b5 | cross_vip_12_b5 | cross_vip_6_b5 | cross_vip_3_b5 | cross_tek_12_b5 | cross_tek_6_b5 | cross_tek_3_b5 | cross_result_v5 | cross_result_v5_vip | cross_result_v5_tek | new_ssrh_b5 | hcrh_b5 | cross_api_12_b4_adj | cross_api_6_b4_adj | cross_api_3_b4_adj | cross_api_12_b5_adj | cross_api_6_b5_adj | cross_api_3_b5_adj | v4_laohui_tag | v5_laohui_tag | v4_laohui_tag_tek | v5_laohui_tag_tek | v4_laohui_tag_vip | v5_laohui_tag_vip | tek_apl_amt_rte | vip_apl_amt_rte | vip_tek_apl_amt_rte_max | vip_tek_dec_grp_reloan | order_amount | result_v4 | result_v5 | model_result_v4 | model_result_v5 | v4_laohui_tag_total | v5_laohui_tag_total | 审批评级_多模型 | 存量评级 | swap_tag | swap_tag_model | 会员卡分组 | 提额卡分组 | 权益卡分组 | 边界分组_v4 | 边界分组_v5 | cross结果_v4 | cross结果_v5 | 边界分组 | cross结果 | 老客客群分组 | 老客客群分组_old | 策略版本 | personalloan_sd_6mceng30_nozy_lgb_rh_v2_prob | rh_good_label | bairong_als_402 | monthly_income | education | 收入 | 学历 | label_sum_wgt_app | label_sum_wgt_api | label_sum_wgt |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 2024070100001700000000907716 | 2024070100001700000000907716 | 2024070100001700000000907716 | 加复贷 | 2024070100001700000000907716 | 2024070100001700000000907716 | 2024-07-01 15:03:08 | 2024-07-01 15:03:08 | 2024-07-01 | 2024-06-28 | 2024-07 | P9olP8Lz+8xoDRbrRXMbqTi6yZsfx/KaakSqFxkmcM4= | FKOSqfhW/4yrLkvM3tN0/Q== | 1103939361 | CTL01da7b1401fd0f6b6c3114715147cc507 | xyf01 | xyf01 | APP流量 |  | I36 | personal_loan | 12 |  | 190000 | reject | reject | failed | 风控审核失败 | temp_cash_w_b |  |  | 376 | 长账龄 | 202306210735309482285502 | 2023-06-21 07:42:34 | 其他 | APP流量 | 首借APP | xyf01 | 12 | 4375.0 | 2434.31 | 1940.69 | 3000.0 | 2026-01-20 00:00:00 | 4375.0 | 0.0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 3.0 | 7.0 | 10.0 | 33.0 | 37.0 | 52.0 | 0.0 | 0.0 | 5.0 | 5.0 | 0.3 | 33 | 1 | 汉 | 已婚 | 江苏省 | 扬州市 | 三线 |  | 0 | jcl_20230728000001_169 | fzgz_20240626000021 | 多模型截尾&审批评级拒绝 | 人行征信提现决策V5 |  | 2024-03-21 04:15:55 | 非调额组 | -1 | 0 | android | android | 信息流 | APP流量 | V5 | B4评级 | 78 | 7830427051921053956960780699632130124696166300888815911714738534820298325007646929415048057013492607 |  |  |  |  | 10.0 | 8.0 | 8.0 | 9.0 | 9.0 |  |  |  | D | J | I |  |  |  |  |  |  |  | 9.0 |  |  |  |  |  |  |  | 非额外放开 | 有APP放款 | 老客其他 | 老客其他 | 非飞跃测试客户 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 20240701153413060withdraw_approval_personalloan72397_1_1 | 2024-07-01 15:34:13 | REJECT | {"_innerResult":"null","activate_inner_app":"xyf01","adj_risk_price_reason_input":"2001","age":33,"app":"xyf01","baihang_maxOverdueStatus":"0","baihang_p2pEscapeDebtStatus":"0","baihang_supremeCourtExecutedStatus":"0","bairong_als_145":9,"bairong_als_158_15d_status":"7.0","bairong_als_261":13,"bairong_als_274":10,"bairong_als_274_30d_status":"19.0","bairong_als_274_adj_limit_status":"10.0","bairong_als_389":58,"bairong_als_402_30d_status":"33.0","bairong_als_402_adj_limit_status":"15.0","bairong_als_554_90d_status":"34.0","biz_flow_number":"2024070100001700000000907716","biz_type":"xjd_withdraw","blacklist_risk_level":-999,"cashloan_bill_clear_period":-999,"cashloan_order_periods":12,"cashloan_white_list":false,"company_position":"公司员工","count_success_cash_order":4,"count_success_cash_order_without_app":4,"count_unpaid_loan_cash_not_current_app_no_M":0,"count_unpaid_loan_cash_with_app_no_M":3,"count_unpaid_loan_cash_without_app_no_M":3,"created_time":"2024-07-01 15:03:08","credit_channel":"xinfeirongdan","cum_vip_ctr_amt":"0.0","cum_vip_ctr_amt_v2":"0.0","cum_vip_ctr_amt_v3":"0.0","current_day_withdraw_count":1,"current_loan_type":"personal_loan","cust_no":"CTL01da7b1401fd0f6b6c3114715147cc507","days_activation_success":376,"debit_amt_cash_not_current_app":0,"device_id":"20230621a8d1abbd5b","device_id_blacklist":false,"dianhuabang_s113":"0.3161","draw_mob_loan_type":376,"face_verify_full_sourcetype":true,"fd_multiple_draw_creditlevel_stock_creditlevel_cross_12":"F","fd_multiple_draw_creditlevel_stock_creditlevel_cross_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_6":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_12":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_6":"SSP","fd_multiple_model_creditlevel_b4_cross_risk_level":"8","fd_multiple_model_creditlevel_cross_l":"F","fd_multiple_model_creditlevel_cross_s":"F","final_score":49,"first_loan_inner_app_loan_type":"xyf01","first_loan_max_paid_period_number_with_app":12,"first_loan_max_paid_period_number_with_loan_type":12,"flow_number":"2024070100001700000000907716","huarong2_13":"0.0","huarong2_15":"0.0","huarong2_17":"0.0","huarong2_22":"5.0","huarong2_337":"0.0","huarong2_338":"0.0","huarong2_340":"0.0","huarong2_341":"0.0","huarong2_342":"0.0","huarong2_343":"0.0","huarong2_345":"0.0","huarong2_346":"0.0","huarong2_347":"0.0","huarong5_1336":"88.0","huarong5_1337":"213.0","huarong5_1338":"226.0","huarong6_38":"0.0","huarong6_39":"0.0","huarong6_40":"0.0","id_card_number":"321088199104052956","id_card_number_blacklist":false,"id_card_number_count_this_device":0,"id_card_valid_date":true,"id_fsovdtotal30d":0,"id_qryorg0d":1,"id_qryorg1h":1,"id_qryorg7d":3,"init_risk_price_input":"I36","innerResult":"REJECT","inner_app":"xyf01","interGroup":"jcl_20230728000001_169","ip":"49.94.114.89","is_supplemental_loan_new":true,"jcl_20230728000001_129_NextNodeCode":"jcl_20230728000001_120","jcl_20230728000001_129_classify_name":"老客其他","jcl_20230728000001_141_NextNodeCode":"jcl_20230728000001_167","jcl_20230728000001_141_classify_name":"非会员卡放开","jcl_20230728000001_15_NextNodeCode":"jcl_20230728000001_61","jcl_20230728000001_15_classify_name":"结清180 以内","jcl_20230728000001_167_NextNodeCode":"jcl_20230728000001_169","jcl_20230728000001_167_classify_name":"V5策略","jcl_20230728000001_75_NextNodeCode":"jcl_20230728000001_58","jcl_20230728000001_75_classify_name":"IRR36","jcl_20230728000001_90_NextNodeCode":"jcl_20230728000001_91","jcl_20230728000001_90_classify_name":"测试组","jcl_20230728000001_95_NextNodeCode":"jcl_20230728000001_74","jcl_20230728000001_95_classify_name":"非白名单用户","jcl_20230807000002_3_NextNodeCode":"jcl_20230807000002_4","jcl_20230807000002_3_classify_name":"个人分期","jcl_20230807000003_5_NextNodeCode":"jcl_20230807000003_9","jcl_20230807000003_5_classify_name":"加复贷","last_credit_agreement_success_inner_app":"xyf01","loan_type":"personal_loan","loan_type_last_loan_inner_app":"xyf01","loan_type_last_reject_date":3,"main_order_created_time":"2024-07-01 15:03:08","min_no_paid_period_number_without_app":4,"mingzhu_member_draw_group":"-999","mobile":"18952766430","mobile_blacklist":false,"mod_b_batch_personalloan_jfd_stock_creditlevel_hcrh_v5_3_1":"9.0","name":"刘明","order_amount":"190000","order_asset_type_input":"1","order_loan_periods":"12","order_number":"2024070100001700000000907716","overdue_current_cash":0,"overdue_current_consume":0,"overdue_past_cash":0,"overdue_past_cash_30_45":0,"overdue_past_consume":0,"overdue_past_consume_30_45":0,"overdue_past_max_cash":0,"period_borrow_average":15833,"personalloan_fd_6mceng30_b4_jy_v1_1_rev_prob":"0.133725","personalloan_fd_6mceng30_b4_jy_v1_rev_prob":"0.133725","personalloan_fd_dt_risk_price_random_v1":31,"personalloan_fd_multiple_model_rej_v2__lift2":"1.841949411543192","personalloan_fd_multiple_model_rej_v2_lift2_round":"1.8","personalloan_fd_multiple_model_rej_v3__lift1":"2.966895297010927","personalloan_fd_multiply_model_laohui_v1_l1":"0.0","personalloan_jfd_account_current_level":"A","personalloan_jfd_draw_creditlevel_ssrh_v2_2_4":"10.0","personalloan_jfd_draw_creditlevel_ssrh_v4":"8","personalloan_jfd_draw_creditlevel_ssrh_v5":"9","personalloan_jfd_overdue_past_level":1,"personalloan_jfd_stock_creditlevel_hcrh_v2_2_3":"10.0","personalloan_jfd_stock_creditlevel_hcrh_v4_2_1":"9.0","personalloan_reloan_overdue_past_callback":"1","pl_fd_dt_multi_model_random_v1":10,"product_name":"xinyongfei","product_type":"L3","random2":"7830427051921053956960780699632130124696166300888815911714738534820298325007646929415048057013492607","random2_zx_test_rate":"1.0","rate_level":"I001","report_id":"fb201496dce7457ab1946925a18ff1a7","requestId":"20240701153413060withdraw_approval_personalloan72397_1_1","requester":"lendtrade","rlt_risk_gecision_tek_paid_card_amount":"0.0","ruleHitNum":1,"ruleHitResult":"hit","ruleHitScore":1000,"ruleTotalScore":1000,"same_source_type":true,"seq_id":"2024070100001700000003294620","sms_bad_1m":0,"sms_fraud_1m":0,"sms_lost_1m":0,"source_type":"android","source_type_native":true,"stage":"02","tek_apl_amt_rte":"0.0","tongdun_1":1,"tongdun_10":8,"tongdun_16":1,"tongdun_19":19,"tongdun_cash_score":43,"tongdun_i_cnt_mobile_v3_Loan_all_90day":1,"uid":"44836799","user_id":"44836799","user_no":"1103939361","vip_apl_amt_rte":"0.0","vip_tek_dec_grp_reloan":"nvip","withdraw_amount":190000,"xinyan_1":"0.3","xinyongfei_crawler_discredit":false,"xyf_api_tx_source_v1":"-1.0","xyf_app_source_v1":"10.0","xyf_withdraw_channel_attr_source":"加复贷"} | {"jcl_20230728000001":[{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_1","nodeName":"开始","nodeType":"start"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_95","nodeName":"白名单用户判断","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_74","nodeName":"科技输出拒绝","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_14","nodeName":"免费规则集","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_15","nodeName":"是否结清180天","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_61","nodeName":"收费规则集 _V2","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_75","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_58","nodeName":"收费规则V2陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_90","nodeName":"外数测试分组","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_91","nodeName":"外数测试组","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_77","nodeName":"征信Stage输出","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_24","nodeName":"人行组件","nodeType":"creditReport"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_132","nodeName":"严重逾期捞回标签","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_101","nodeName":"多模型截尾_审批评级_cross_短账龄","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_102","nodeName":"多模型截尾_审批评级_cross_长账龄","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_119","nodeName":"多模型审批评级决策表","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_137","nodeName":"明珠会员贷多模型截尾","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_79","nodeName":"人行征信提现决策_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_134","nodeName":"人行征信提现决策V2.1_新陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_129","nodeName":"老客用户分组","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_120","nodeName":"存量评级cross_12期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_135","nodeName":"存量评级cross_6期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_121","nodeName":"存量评级cross_3期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_163","nodeName":"评级cross_v5_12期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_164","nodeName":"评级cross_v5_6期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_165","nodeName":"评级cross_v5_3期","nodeType":"decisionTable"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_157","nodeName":"人行征信提现决策V5_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_166","nodeName":"人行征信提现决策V4_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_140","nodeName":"是否会员卡审批放开","nodeType":"decisionTree"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_141","nodeName":"是否会员卡放开","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_167","nodeName":"策略版本分组","nodeType":"classify"},{"decisionId":"20240701153413060withdraw_approval_personalloan72397_1_1","nodeCode":"jcl_20230728000001_169","nodeName":"人行征信提现决策V5","nodeType":"ruleBase"}]} |  |  |  |  |  |  | 2024-07-01 |  |  |  | F | SSP | SSP |  |  |  |  |  |  |  |  |  | 8 | 9.0 |  |  |  | SSP | SSP | SSP |  |  |  |  |  |  |  |  |  | 9 | 9.0 |  |  |  |  |  |  |  |  |  |  |  |  | 0.0 | 0.0 |  | nvip | 190000 | reject | reject |  |  |  |  | 9 | 9.0 | out-out |  |  |  |  | F | SSP |  |  | SSP |  | 老客其他 | 老客其他 | V5 | 0.13008382067756358 | 非征信好人 | 33.0 | 10,000~20,000 | 高中/中专/技校 | 4 | 1 | 0.0 | 0.0 | 0.0 |
| 2024070100001700000001215130 | 2024070100001700000098745234 | 2024070100001700000001215130 | 加复贷 | 2024070100001700000098745234 | 2024070100001700000098745234 | 2024-07-01 15:08:01 | 2024-07-01 14:34:32 | 2024-07-01 | 2024-06-28 | 2024-07 | CEwQY0ndre+jK1Wt7My/qy4UmcYZPUi6Nao75nxycXk= | s2bhvO+6/bb+UvrdgX+adw== | 1046651098 | CTL0f8550849c851ab6698d94507eb868009 | xyf01 | xyf01 | APP流量 | 1 | I36 | personal_loan | 3 | 2024-07-01 15:19:06 | 120000 | pass | pass | success |  | syxj_cash |  |  | 420 | 长账龄 | 202305080946060240685019 | 2023-05-08 09:46:06 | 其他 | API流量 | 首借API | xyf01_nwd | 12 | 16406.25 | 15128.48 | 1277.77 | 10000.0 | 2026-04-03 00:00:00 | 16406.25 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 6.0 | 12.0 | 24.0 | 31.0 | 40.0 | 53.0 | 0.0 | 0.0 | 6.0 | 5.0 | 0.4 | 46 | 1 | 汉 | 已婚 | 广东省 | 汕头市 | 三线 |  | 1 |  |  | 风控通过 | 风控通过 |  | 2023-11-08 09:18:05 | 非调额组 | -1 | 1 | android | android | API流量 | APP流量 | V4 | B4评级 | 36 | 3660806222252445750022272964370631658835882260137512241837352389524930578986688292882104291090906615 |  |  |  |  | 3.2 | 3.1 | 3.1 | 7.0 | 7.0 |  |  |  | D | C2 | E |  |  |  |  |  |  |  | 3.1 | E |  |  |  |  |  |  | 非额外放开 | 有APP放款 | 老客其他 | 老客其他 | 非飞跃测试客户 |  |  |  |  |  |  |  |  |  |  |  |  | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |  |  | 0.0 |  |  | 0.0 |  |  | 0 | 20240701150616514withdraw_approval_personalloan69160_1_1 | 2024-07-01 15:06:16 | PASS | {"_innerResult":"null","activate_inner_app":"xyf01_nwd","adj_risk_price_reason_input":"2001","age":46,"app":"xyf01","baihang_maxOverdueStatus":"0","baihang_p2pEscapeDebtStatus":"0","baihang_supremeCourtExecutedStatus":"0","bairong_als_145":16,"bairong_als_158_15d_status":"12.0","bairong_als_261":32,"bairong_als_274":24,"bairong_als_274_30d_status":"16.0","bairong_als_274_adj_limit_status":"16.0","bairong_als_389":63,"bairong_als_402_30d_status":"26.0","bairong_als_402_adj_limit_status":"26.0","bairong_als_554_90d_status":"41.0","biz_flow_number":"2024070100001700000098745234","biz_type":"xjd_withdraw","blacklist_risk_level":-999,"cashloan_bill_clear_period":-999,"cashloan_order_periods":3,"cashloan_white_list":false,"company_position":"事业单位","count_success_cash_order":15,"count_success_cash_order_without_app":15,"count_unpaid_loan_cash_not_current_app_no_M":0,"count_unpaid_loan_cash_with_app_no_M":6,"count_unpaid_loan_cash_without_app_no_M":6,"created_time":"2024-07-01 14:34:32","credit_channel":"xinfeirongdan","cum_vip_ctr_amt":"0.0","cum_vip_ctr_amt_v2":"0.0","cum_vip_ctr_amt_v3":"0.0","current_day_withdraw_count":1,"current_loan_type":"personal_loan","cust_no":"CTL0f8550849c851ab6698d94507eb868009","days_activation_success":421,"debit_amt_cash_not_current_app":0,"device_id":"202305089d4a7f212a","device_id_blacklist":false,"dianhuabang_s113":"0.1928","draw_mob_loan_type":420,"face_verify_full_sourcetype":true,"fd_multiple_draw_creditlevel_stock_creditlevel_cross_12":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_3":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_6":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_12":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_3":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_6":"P","fd_multiple_model_creditlevel_b4_cross_risk_level":"3.1","fd_multiple_model_creditlevel_cross_l":"P","fd_multiple_model_creditlevel_cross_s":"P","final_score":81,"first_loan_inner_app_loan_type":"xyf01_nwd","first_loan_max_paid_period_number_with_app":12,"first_loan_max_paid_period_number_with_loan_type":12,"flow_number":"2024070100001700000098745234","huarong2_13":"0.0","huarong2_15":"0.0","huarong2_17":"0.0","huarong2_22":"6.0","huarong2_337":"0.0","huarong2_338":"0.0","huarong2_340":"0.0","huarong2_341":"0.0","huarong2_342":"0.0","huarong2_343":"1.0","huarong2_345":"0.0","huarong2_346":"0.0","huarong2_347":"1.0","huarong5_1336":"69.0","huarong5_1337":"181.0","huarong5_1338":"231.0","huarong6_38":"11.0","huarong6_39":"43.0","huarong6_40":"103.0","id_card_number":"440506197804070039","id_card_number_blacklist":false,"id_card_number_count_this_device":0,"id_card_valid_date":true,"id_fsovdtotal30d":0,"id_qryorg0d":1,"id_qryorg1h":1,"id_qryorg7d":0,"init_risk_price_input":"I36","innerResult":"","inner_app":"xyf01","interGroup":"jcl_20230728000001_51","ip":"183.4.58.173","is_supplemental_loan_new":true,"jcl_20230728000001_129_NextNodeCode":"jcl_20230728000001_120","jcl_20230728000001_129_classify_name":"老客其他","jcl_20230728000001_141_NextNodeCode":"jcl_20230728000001_167","jcl_20230728000001_141_classify_name":"非会员卡放开","jcl_20230728000001_15_NextNodeCode":"jcl_20230728000001_61","jcl_20230728000001_15_classify_name":"结清180 以内","jcl_20230728000001_167_NextNodeCode":"jcl_20230728000001_117","jcl_20230728000001_167_classify_name":"V4策略","jcl_20230728000001_42_NextNodeCode":"jcl_20230728000001_51","jcl_20230728000001_42_classify_name":"I36","jcl_20230728000001_75_NextNodeCode":"jcl_20230728000001_58","jcl_20230728000001_75_classify_name":"IRR36","jcl_20230728000001_90_NextNodeCode":"jcl_20230728000001_91","jcl_20230728000001_90_classify_name":"测试组","jcl_20230728000001_95_NextNodeCode":"jcl_20230728000001_74","jcl_20230728000001_95_classify_name":"非白名单用户","jcl_20230807000002_3_NextNodeCode":"jcl_20230807000002_4","jcl_20230807000002_3_classify_name":"个人分期","jcl_20230807000003_5_NextNodeCode":"jcl_20230807000003_9","jcl_20230807000003_5_classify_name":"加复贷","last_credit_agreement_success_inner_app":"xyf01_nwd","loan_type":"personal_loan","loan_type_last_loan_inner_app":"xyf01","loan_type_last_reject_date":53,"main_order_created_time":"2024-07-01 14:34:32","min_no_paid_period_number_without_app":1,"mingzhu_member_draw_group":"P","mobile":"13536881887","mobile_blacklist":false,"mod_b_batch_personalloan_jfd_stock_creditlevel_hcrh_v5_3_1":"3.1","name":"黄遂濠","order_amount":"120000","order_asset_type_input":"1","order_loan_periods":"3","order_number":"2024070100001700000098745234","overdue_current_cash":0,"overdue_current_consume":0,"overdue_past_cash":0,"overdue_past_cash_30_45":0,"overdue_past_consume":0,"overdue_past_consume_30_45":0,"overdue_past_max_cash":1,"period_borrow_average":40000,"personalloan_fd_6mceng30_b4_jy_v1_1_rev_prob":"0.042512","personalloan_fd_6mceng30_b4_jy_v1_rev_prob":"0.042512","personalloan_fd_dt_risk_price_random_v1":43,"personalloan_fd_multiple_model_rej_v2__lift2":"1.5125458253807054","personalloan_fd_multiple_model_rej_v2_lift2_round":"1.5","personalloan_fd_multiple_model_rej_v3__lift1":"2.0304492083451846","personalloan_fd_multiply_model_laohui_v1_l1":"1.0","personalloan_jfd_account_current_level":"A","personalloan_jfd_draw_creditlevel_ssrh_v2_2_4":"3.2","personalloan_jfd_draw_creditlevel_ssrh_v4":"3.1","personalloan_jfd_draw_creditlevel_ssrh_v5":"7","personalloan_jfd_overdue_past_level":1,"personalloan_jfd_stock_creditlevel_hcrh_v2_2_3":"3.2","personalloan_jfd_stock_creditlevel_hcrh_v4_2_1":"5.0","personalloan_reloan_overdue_past_callback":"1","pl_fd_dt_multi_model_random_v1":21,"product_name":"xinyongfei","product_type":"L3","random2":"3660806222252445750022272964370631658835882260137512241837352389524930578986688292882104291090906615","random2_zx_test_rate":"16.0","rate_level":"I001","report_id":"3fcbeb16dfc249cbba8631739e0a22f8","requestId":"20240701150616514withdraw_approval_personalloan69160_1_1","requester":"lendtrade","rlt_risk_gecision_tek_paid_card_amount":"0.0","ruleHitNum":0,"ruleHitResult":"hit","ruleHitScore":1,"ruleTotalScore":0,"same_source_type":true,"seq_id":"2024070100001700000001153948","sms_bad_1m":0,"sms_fraud_1m":0,"sms_lost_1m":0,"source_type":"android","source_type_native":true,"stage":"02","tek_apl_amt_rte":"0.0","tongdun_1":6,"tongdun_10":13,"tongdun_16":1,"tongdun_19":23,"tongdun_cash_score":73,"tongdun_i_cnt_mobile_v3_Loan_all_90day":1,"uid":"29389704","user_asset_type_output":"36","user_id":"29389704","user_no":"1046651098","vip_apl_amt_rte":"0.0","vip_tek_dec_grp_reloan":"nvip","withdraw_amount":120000,"xinyan_1":"0.4","xinyongfei_crawler_discredit":false,"xyf_api_tx_source_v1":"30.0","xyf_app_source_v1":"20.0","xyf_withdraw_channel_attr_source":"加复贷"} | {"jcl_20230728000001":[{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_1","nodeName":"开始","nodeType":"start"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_95","nodeName":"白名单用户判断","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_74","nodeName":"科技输出拒绝","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_14","nodeName":"免费规则集","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_15","nodeName":"是否结清180天","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_61","nodeName":"收费规则集 _V2","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_75","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_58","nodeName":"收费规则V2陪跑","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_90","nodeName":"外数测试分组","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_91","nodeName":"外数测试组","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_77","nodeName":"征信Stage输出","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_24","nodeName":"人行组件","nodeType":"creditReport"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_132","nodeName":"严重逾期捞回标签","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_101","nodeName":"多模型截尾_审批评级_cross_短账龄","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_102","nodeName":"多模型截尾_审批评级_cross_长账龄","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_119","nodeName":"多模型审批评级决策表","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_137","nodeName":"明珠会员贷多模型截尾","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_79","nodeName":"人行征信提现决策_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_134","nodeName":"人行征信提现决策V2.1_新陪跑","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_129","nodeName":"老客用户分组","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_120","nodeName":"存量评级cross_12期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_135","nodeName":"存量评级cross_6期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_121","nodeName":"存量评级cross_3期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_163","nodeName":"评级cross_v5_12期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_164","nodeName":"评级cross_v5_6期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_165","nodeName":"评级cross_v5_3期","nodeType":"decisionTable"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_157","nodeName":"人行征信提现决策V5_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_166","nodeName":"人行征信提现决策V4_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_140","nodeName":"是否会员卡审批放开","nodeType":"decisionTree"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_141","nodeName":"是否会员卡放开","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_167","nodeName":"策略版本分组","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_117","nodeName":"人行征信提现决策V4","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_42","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_51","nodeName":"i36必过","nodeType":"ruleBase"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_115","nodeName":"复贷特征因子陪跑","nodeType":"action"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_98","nodeName":"新模型平台陪跑节点","nodeType":"action"},{"decisionId":"20240701150616514withdraw_approval_personalloan69160_1_1","nodeCode":"jcl_20230728000001_2","nodeName":"结束","nodeType":"end"}]} |  |  |  |  |  |  | 2024-07-01 |  |  |  | P | P | P |  |  |  |  |  |  |  |  |  | 3.1 | 5.0 |  |  |  | P | P | P |  |  |  |  |  |  |  |  |  | 7 | 3.1 |  |  |  |  |  |  |  |  |  |  |  |  | 0.0 | 0.0 |  | nvip | 120000 | pass | pass |  |  |  |  | 3.1 | 5.0 | in-in |  |  |  |  | P | P |  |  | P |  | 老客其他 | 老客其他 | V4 | 0.03652036163297057 | 征信好人 | 31.0 | 10,000~20,000 | 本科 | 4 | 3 | 6.9821523235111 | 6.318115337450769 | 6.318115337450769 |
| 2024070100001700000003687205 | 2024070100001700000003687205 | 2024070100001700000003687205 | 加复贷 | 2024070100001700000003687205 | 2024070100001700000003687205 | 2024-07-01 15:39:17 | 2024-07-01 15:39:17 | 2024-07-01 | 2024-06-28 | 2024-07 | N5Zf3GHOvAOkhQHcgXwFpnSKhF7DOsi1SxfvU5GVrVs= | X1Nh/n0nxY4fgVez8BCGxA== | 1017117840 | CTL009699cd029c17c91f4a5f3fee18c0188 | xyf01 | xyf01 | APP流量 |  | I36 | personal_loan | 12 |  | 1030000 | reject | reject | failed | 风控审核失败 | temp_cash_w_b |  |  | 1018 | 长账龄 | 202109171022380214766245 | 2021-09-17 10:22:38 | 其他 | APP流量 | 首借APP | xyf01 | 11 | 30000.0 | 19656.25 | 10343.75 | 10000.0 | 2026-04-03 00:00:00 | 30000.0 | 0.0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 |  | 4.0 | 6.0 | 24.0 | 26.0 | 46.0 | 0.0 | 0.0 | 5.0 | 5.0 | 0.3 | 34 | 0 | 汉 | 已婚 | 陕西省 | 延安市 | 五线 |  | 0 | jcl_20230728000001_169 | fzgz_20240626000021 | 多模型截尾&审批评级拒绝 | 人行征信提现决策V5 |  | 2024-02-02 07:02:46 | 非调额组 | -1 | 1 | android | android | APP流量 | APP流量 | V5 | B4评级 | 58 | 5899547473230123052223243102723212255577996339443866275181198595155392080695218275906965234794534308 | 6 |  |  |  | 8.0 | 10.0 | 10.0 | 10.0 | 10.0 |  |  |  | D | H | H |  |  |  |  |  |  |  | 10.0 |  |  |  |  |  |  |  | 非额外放开 | 有APP放款 | 老客其他 | 老客其他 | 非飞跃测试客户 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 20240701153918870withdraw_approval_personalloan72985_1_1 | 2024-07-01 15:39:18 | REJECT | {"_innerResult":"null","activate_inner_app":"xyf01","adj_risk_price_reason_input":"2001","age":34,"app":"xyf01","baihang_maxOverdueStatus":"0","baihang_p2pEscapeDebtStatus":"0","baihang_supremeCourtExecutedStatus":"0","bairong_als_145":4,"bairong_als_158_15d_status":"4.0","bairong_als_261":8,"bairong_als_274":6,"bairong_als_274_30d_status":"17.0","bairong_als_274_adj_limit_status":"6.0","bairong_als_389":38,"bairong_als_402_30d_status":"23.0","bairong_als_402_adj_limit_status":"24.0","bairong_als_554_90d_status":"28.0","biz_flow_number":"2024070100001700000003687205","biz_type":"xjd_withdraw","blacklist_risk_level":-999,"cashloan_bill_clear_period":-999,"cashloan_order_periods":12,"cashloan_white_list":false,"company_position":"私营业主","count_success_cash_order":18,"count_success_cash_order_without_app":19,"count_unpaid_loan_cash_not_current_app_no_M":0,"count_unpaid_loan_cash_with_app_no_M":5,"count_unpaid_loan_cash_without_app_no_M":5,"created_time":"2024-07-01 15:39:17","credit_channel":"xinfeirongdan","cum_vip_ctr_amt":"0.0","cum_vip_ctr_amt_v2":"0.0","cum_vip_ctr_amt_v3":"0.0","current_day_withdraw_count":1,"current_loan_type":"personal_loan","cust_no":"CTL009699cd029c17c91f4a5f3fee18c0188","days_activation_success":1121,"debit_amt_cash_not_current_app":0,"device_id":"202008161b23be07bd","device_id_blacklist":false,"dianhuabang_s113":"0.3127","draw_mob_loan_type":1018,"face_verify_full_sourcetype":true,"fd_multiple_draw_creditlevel_stock_creditlevel_cross_12":"F","fd_multiple_draw_creditlevel_stock_creditlevel_cross_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_6":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_12":"F","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_6":"F","fd_multiple_model_creditlevel_b4_cross_risk_level":"10","fd_multiple_model_creditlevel_cross_l":"F","fd_multiple_model_creditlevel_cross_s":"F","final_score":58,"first_loan_inner_app_loan_type":"xyf01","first_loan_max_paid_period_number_with_app":11,"first_loan_max_paid_period_number_with_loan_type":11,"flow_number":"2024070100001700000003687205","huarong2_13":"0.0","huarong2_15":"0.0","huarong2_17":"0.0","huarong2_22":"5.0","huarong2_337":"0.0","huarong2_338":"0.0","huarong2_340":"0.0","huarong2_341":"0.0","huarong2_342":"0.0","huarong2_343":"0.0","huarong2_345":"0.0","huarong2_346":"0.0","huarong2_347":"0.0","huarong5_1336":"73.0","huarong5_1337":"219.0","huarong5_1338":"274.0","huarong6_38":"15.0","huarong6_39":"60.0","huarong6_40":"126.0","id_card_number":"610625199006031284","id_card_number_blacklist":false,"id_card_number_count_this_device":0,"id_card_valid_date":true,"id_fsovdtotal30d":0,"id_qryorg0d":0,"id_qryorg1h":0,"id_qryorg7d":0,"init_risk_price_input":"I36","innerResult":"REJECT","inner_app":"xyf01","interGroup":"jcl_20230728000001_169","ip":"171.82.3.236","is_supplemental_loan_new":true,"jcl_20230728000001_129_NextNodeCode":"jcl_20230728000001_120","jcl_20230728000001_129_classify_name":"老客其他","jcl_20230728000001_141_NextNodeCode":"jcl_20230728000001_167","jcl_20230728000001_141_classify_name":"非会员卡放开","jcl_20230728000001_15_NextNodeCode":"jcl_20230728000001_61","jcl_20230728000001_15_classify_name":"结清180 以内","jcl_20230728000001_167_NextNodeCode":"jcl_20230728000001_169","jcl_20230728000001_167_classify_name":"V5策略","jcl_20230728000001_75_NextNodeCode":"jcl_20230728000001_58","jcl_20230728000001_75_classify_name":"IRR36","jcl_20230728000001_90_NextNodeCode":"jcl_20230728000001_92","jcl_20230728000001_90_classify_name":"非测试组","jcl_20230728000001_95_NextNodeCode":"jcl_20230728000001_74","jcl_20230728000001_95_classify_name":"非白名单用户","jcl_20230807000002_3_NextNodeCode":"jcl_20230807000002_4","jcl_20230807000002_3_classify_name":"个人分期","jcl_20230807000003_5_NextNodeCode":"jcl_20230807000003_9","jcl_20230807000003_5_classify_name":"加复贷","last_credit_agreement_success_inner_app":"xyf01","loan_type":"personal_loan","loan_type_last_loan_inner_app":"xyf01","loan_type_last_reject_date":1,"main_order_created_time":"2024-07-01 15:39:17","min_no_paid_period_number_without_app":3,"mingzhu_member_draw_group":"F","mobile":"13720327717","mobile_blacklist":false,"mod_b_batch_personalloan_jfd_stock_creditlevel_hcrh_v5_3_1":"10.0","name":"张海丽","order_amount":"1030000","order_asset_type_input":"1","order_loan_periods":"12","order_number":"2024070100001700000003687205","overdue_current_cash":0,"overdue_current_consume":0,"overdue_past_cash":0,"overdue_past_cash_30_45":0,"overdue_past_consume":0,"overdue_past_consume_30_45":0,"overdue_past_max_cash":1,"period_borrow_average":85833,"personalloan_fd_6mceng30_b4_jy_v1_1_rev_prob":"0.200915","personalloan_fd_6mceng30_b4_jy_v1_rev_prob":"0.200915","personalloan_fd_dt_risk_price_random_v1":31,"personalloan_fd_multiple_model_rej_v2__lift2":"2.574014605413121","personalloan_fd_multiple_model_rej_v2_lift2_round":"2.6","personalloan_fd_multiple_model_rej_v3__lift1":"4.574777497669087","personalloan_fd_multiply_model_laohui_v1_l1":"0.0","personalloan_jfd_account_current_level":"A","personalloan_jfd_draw_creditlevel_ssrh_v2_2_4":"8.0","personalloan_jfd_draw_creditlevel_ssrh_v4":"10","personalloan_jfd_draw_creditlevel_ssrh_v5":"10","personalloan_jfd_overdue_past_level":1,"personalloan_jfd_stock_creditlevel_hcrh_v2_2_3":"8.0","personalloan_jfd_stock_creditlevel_hcrh_v4_2_1":"8.0","personalloan_reloan_overdue_past_callback":"1","pl_fd_dt_multi_model_random_v1":2,"product_name":"xinyongfei","product_type":"L3","random2":"5899547473230123052223243102723212255577996339443866275181198595155392080695218275906965234794534308","random2_zx_test_rate":"22.0","rate_level":"I001","report_id":"be965ea7c920408c9e8e105f021ec0a3","requestId":"20240701153918870withdraw_approval_personalloan72985_1_1","requester":"lendtrade","rlt_risk_gecision_tek_paid_card_amount":"0.0","ruleHitNum":1,"ruleHitResult":"hit","ruleHitScore":1000,"ruleTotalScore":1000,"same_source_type":true,"seq_id":"2024070100001700000003689912","sms_bad_1m":0,"sms_fraud_1m":0,"sms_lost_1m":0,"source_type":"android","source_type_native":true,"stage":"02","tek_apl_amt_rte":"0.0","tongdun_1":2,"tongdun_10":14,"tongdun_16":1,"tongdun_19":18,"tongdun_cash_score":43,"tongdun_i_cnt_mobile_v3_Loan_all_90day":1,"uid":"10927161","user_id":"10927161","user_no":"1017117840","vip_apl_amt_rte":"0.0","vip_tek_dec_grp_reloan":"nvip","withdraw_amount":1030000,"xinyan_1":"0.3","xinyongfei_crawler_discredit":false,"xyf_api_tx_source_v1":"-1.0","xyf_app_source_v1":"20.0","xyf_withdraw_channel_attr_source":"加复贷"} | {"jcl_20230728000001":[{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_1","nodeName":"开始","nodeType":"start"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_95","nodeName":"白名单用户判断","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_74","nodeName":"科技输出拒绝","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_14","nodeName":"免费规则集","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_15","nodeName":"是否结清180天","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_61","nodeName":"收费规则集 _V2","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_75","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_58","nodeName":"收费规则V2陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_90","nodeName":"外数测试分组","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_92","nodeName":"非测试组必过","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_77","nodeName":"征信Stage输出","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_24","nodeName":"人行组件","nodeType":"creditReport"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_132","nodeName":"严重逾期捞回标签","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_101","nodeName":"多模型截尾_审批评级_cross_短账龄","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_102","nodeName":"多模型截尾_审批评级_cross_长账龄","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_119","nodeName":"多模型审批评级决策表","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_137","nodeName":"明珠会员贷多模型截尾","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_79","nodeName":"人行征信提现决策_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_134","nodeName":"人行征信提现决策V2.1_新陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_129","nodeName":"老客用户分组","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_120","nodeName":"存量评级cross_12期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_135","nodeName":"存量评级cross_6期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_121","nodeName":"存量评级cross_3期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_163","nodeName":"评级cross_v5_12期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_164","nodeName":"评级cross_v5_6期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_165","nodeName":"评级cross_v5_3期","nodeType":"decisionTable"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_157","nodeName":"人行征信提现决策V5_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_166","nodeName":"人行征信提现决策V4_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_140","nodeName":"是否会员卡审批放开","nodeType":"decisionTree"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_141","nodeName":"是否会员卡放开","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_167","nodeName":"策略版本分组","nodeType":"classify"},{"decisionId":"20240701153918870withdraw_approval_personalloan72985_1_1","nodeCode":"jcl_20230728000001_169","nodeName":"人行征信提现决策V5","nodeType":"ruleBase"}]} |  |  |  |  |  |  | 2024-07-01 |  |  |  | F | SSP | SSP |  |  |  |  |  |  |  |  |  | 10 | 8.0 |  |  |  | F | F | SSP |  |  |  |  |  |  |  |  |  | 10 | 10.0 |  |  |  |  |  |  |  |  |  |  |  |  | 0.0 | 0.0 |  | nvip | 1030000 | reject | reject |  |  |  |  | 10 | 10.0 | out-out |  |  |  |  | F | F |  |  | F |  | 老客其他 | 老客其他 | V5 | 0.10751909658010508 | 非征信好人 | 24.0 | 20,000~50,000 | 本科 | 5 | 3 |  |  |  |
| 2024070100001700000004394817 | 2024070100001700000004394817 | 2024070100001700000004394817 | 加复贷 | 2024070100001700000004394817 | 2024070100001700000004394817 | 2024-07-01 15:48:48 | 2024-07-01 15:48:48 | 2024-07-01 | 2024-06-28 | 2024-07 | R6cPRC1ies3BRqvaJQ4qCJKERb9osGcb/O6dbhDv0nY= | FNlRb5EBDcbeiqnx+I/tvQ== | 1119357657 | CTL015063883366756c890472a02c8b367d8 | xyf01 | xyf01 | APP流量 |  | I36 | personal_loan | 12 |  | 930000 | reject | reject | failed | 风控审核失败 | temp_cash_w_b |  |  | 252 | 长账龄 | 202310231847040261485369 | 2023-10-23 18:47:04 | 其他 | API流量 | 首借API | xyf01_rs03 | 8 | 13500.0 | 4114.39 | 9385.61 | 12000.0 | 2025-04-08 00:00:00 | 13500.0 | 0.0 | 0 | 0 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 3.0 | 13.0 | 19.0 | 23.0 | 38.0 | 53.0 | 0.0 | 0.0 | 5.0 | 2.0 | 0.5 | 34 | 0 | 汉 | 离异 | 湖北省 | 恩施土家族苗族自治州 | 五线 |  | 0 | jcl_20230728000001_117 | fzgz_20240327000011 | 多模型截尾&审批评级拒绝 | 人行征信提现决策V4 |  |  | 非调额组 | -1 | 0 | ios | ios | APP流量 | APP流量 | V4 | B4评级 | 77 | 7778276448575027002310856931421324208579696113183875152592709641309900105981179292997724927682389867 |  |  |  |  | 9.0 | 9.0 | 9.0 | 9.0 | 9.0 |  |  |  | H | H | J |  |  |  |  |  |  |  | 9.0 | J |  |  |  |  |  |  | 非额外放开 | 有APP放款 | 老客其他 | 老客其他 | 非飞跃测试客户 |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  |  | 0 | 20240701154849417withdraw_approval_personalloan74051_1_1 | 2024-07-01 15:48:49 | REJECT | {"_innerResult":"null","activate_inner_app":"xyf01_rs03","adj_risk_price_reason_input":"2001","age":34,"app":"xyf01","baihang_maxOverdueStatus":"0","baihang_p2pEscapeDebtStatus":"0","baihang_supremeCourtExecutedStatus":"0","bairong_als_145":13,"bairong_als_158_15d_status":"13.0","bairong_als_261":20,"bairong_als_274":19,"bairong_als_274_30d_status":"8.0","bairong_als_274_adj_limit_status":"8.0","bairong_als_389":36,"bairong_als_402_30d_status":"27.0","bairong_als_402_adj_limit_status":"27.0","bairong_als_554_90d_status":"47.0","biz_flow_number":"2024070100001700000004394817","biz_type":"xjd_withdraw","blacklist_risk_level":-999,"cashloan_bill_clear_period":-999,"cashloan_order_periods":12,"cashloan_white_list":false,"company_position":"私营业主","count_success_cash_order":2,"count_success_cash_order_without_app":2,"count_unpaid_loan_cash_not_current_app_no_M":0,"count_unpaid_loan_cash_with_app_no_M":1,"count_unpaid_loan_cash_without_app_no_M":1,"created_time":"2024-07-01 15:48:48","credit_channel":"xinfeirongdan","cum_vip_ctr_amt":"0.0","cum_vip_ctr_amt_v2":"0.0","cum_vip_ctr_amt_v3":"0.0","current_day_withdraw_count":1,"current_loan_type":"personal_loan","cust_no":"CTL015063883366756c890472a02c8b367d8","days_activation_success":252,"debit_amt_cash_not_current_app":0,"device_id":"20231106d79f20e692","device_id_blacklist":false,"dianhuabang_s113":"0.2928","draw_mob_loan_type":252,"face_verify_full_sourcetype":true,"fd_multiple_draw_creditlevel_stock_creditlevel_cross_12":"F","fd_multiple_draw_creditlevel_stock_creditlevel_cross_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_6":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_12":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_3":"SSP","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_6":"SSP","fd_multiple_model_creditlevel_b4_cross_risk_level":"9","fd_multiple_model_creditlevel_cross_l":"F","fd_multiple_model_creditlevel_cross_s":"F","final_score":35,"first_loan_inner_app_loan_type":"xyf01_rs03","first_loan_max_paid_period_number_with_app":8,"first_loan_max_paid_period_number_with_loan_type":8,"flow_number":"2024070100001700000004394817","huarong2_13":"0.0","huarong2_15":"0.0","huarong2_17":"0.0","huarong2_22":"5.0","huarong2_337":"0.0","huarong2_338":"0.0","huarong2_340":"0.0","huarong2_341":"0.0","huarong2_342":"0.0","huarong2_343":"0.0","huarong2_345":"0.0","huarong2_346":"0.0","huarong2_347":"0.0","huarong5_1336":"35.0","huarong5_1337":"84.0","huarong5_1338":"122.0","huarong6_38":"17.0","huarong6_39":"62.0","huarong6_40":"99.0","id_card_number":"422828199006065720","id_card_number_blacklist":false,"id_card_number_count_this_device":0,"id_card_valid_date":true,"id_fsovdtotal30d":0,"id_qryorg0d":2,"id_qryorg1h":1,"id_qryorg7d":0,"init_risk_price_input":"I36","innerResult":"REJECT","inner_app":"xyf01","interGroup":"jcl_20230728000001_117","ip":"123.147.252.119","is_supplemental_loan_new":true,"jcl_20230728000001_129_NextNodeCode":"jcl_20230728000001_120","jcl_20230728000001_129_classify_name":"老客其他","jcl_20230728000001_141_NextNodeCode":"jcl_20230728000001_167","jcl_20230728000001_141_classify_name":"非会员卡放开","jcl_20230728000001_15_NextNodeCode":"jcl_20230728000001_61","jcl_20230728000001_15_classify_name":"结清180 以内","jcl_20230728000001_167_NextNodeCode":"jcl_20230728000001_117","jcl_20230728000001_167_classify_name":"V4策略","jcl_20230728000001_75_NextNodeCode":"jcl_20230728000001_58","jcl_20230728000001_75_classify_name":"IRR36","jcl_20230728000001_90_NextNodeCode":"jcl_20230728000001_92","jcl_20230728000001_90_classify_name":"非测试组","jcl_20230728000001_95_NextNodeCode":"jcl_20230728000001_74","jcl_20230728000001_95_classify_name":"非白名单用户","jcl_20230807000002_3_NextNodeCode":"jcl_20230807000002_4","jcl_20230807000002_3_classify_name":"个人分期","jcl_20230807000003_5_NextNodeCode":"jcl_20230807000003_9","jcl_20230807000003_5_classify_name":"加复贷","last_credit_agreement_success_inner_app":"xyf01_rs03","loan_type":"personal_loan","loan_type_last_loan_inner_app":"xyf01","loan_type_last_reject_date":4,"main_order_created_time":"2024-07-01 15:48:48","min_no_paid_period_number_without_app":9,"mingzhu_member_draw_group":"F","mobile":"15570538225","mobile_blacklist":false,"mod_b_batch_personalloan_jfd_stock_creditlevel_hcrh_v5_3_1":"8.0","name":"苏琳琳","order_amount":"930000","order_asset_type_input":"1","order_loan_periods":"12","order_number":"2024070100001700000004394817","overdue_current_cash":0,"overdue_current_consume":0,"overdue_past_cash":0,"overdue_past_cash_30_45":0,"overdue_past_consume":0,"overdue_past_consume_30_45":0,"overdue_past_max_cash":0,"period_borrow_average":77500,"personalloan_fd_6mceng30_b4_jy_v1_1_rev_prob":"0.163043","personalloan_fd_6mceng30_b4_jy_v1_rev_prob":"0.163043","personalloan_fd_dt_risk_price_random_v1":99,"personalloan_fd_multiple_model_rej_v2__lift2":"2.0852062479003943","personalloan_fd_multiple_model_rej_v2_lift2_round":"2.1","personalloan_fd_multiple_model_rej_v3__lift1":"2.4259468471872765","personalloan_fd_multiply_model_laohui_v1_l1":"0.0","personalloan_jfd_account_current_level":"A","personalloan_jfd_draw_creditlevel_ssrh_v2_2_4":"9.0","personalloan_jfd_draw_creditlevel_ssrh_v4":"9","personalloan_jfd_draw_creditlevel_ssrh_v5":"9","personalloan_jfd_overdue_past_level":1,"personalloan_jfd_stock_creditlevel_hcrh_v2_2_3":"8.0","personalloan_jfd_stock_creditlevel_hcrh_v4_2_1":"10.0","personalloan_reloan_overdue_past_callback":"1","pl_fd_dt_multi_model_random_v1":28,"product_name":"xinyongfei","product_type":"L3","random2":"7778276448575027002310856931421324208579696113183875152592709641309900105981179292997724927682389867","random2_zx_test_rate":"42.0","rate_level":"I001","report_id":"1d5284723038489bbd2adf1743e3c06d","requestId":"20240701154849417withdraw_approval_personalloan74051_1_1","requester":"lendtrade","rlt_risk_gecision_tek_paid_card_amount":"0.0","ruleHitNum":1,"ruleHitResult":"hit","ruleHitScore":1000,"ruleTotalScore":1000,"same_source_type":true,"seq_id":"2024070100001700000004395766","sms_bad_1m":0,"sms_fraud_1m":0,"sms_lost_1m":0,"source_type":"ios","source_type_native":true,"stage":"02","tek_apl_amt_rte":"0.0","tongdun_1":3,"tongdun_10":6,"tongdun_16":1,"tongdun_19":11,"tongdun_cash_score":19,"tongdun_i_cnt_mobile_v3_Loan_all_90day":1,"uid":"53356584","user_id":"53356584","user_no":"1119357657","vip_apl_amt_rte":"0.0","vip_tek_dec_grp_reloan":"nvip","withdraw_amount":930000,"xinyan_1":"0.5","xinyongfei_crawler_discredit":false,"xyf_api_tx_source_v1":"30.0","xyf_app_source_v1":"20.0","xyf_withdraw_channel_attr_source":"加复贷"} | {"jcl_20230728000001":[{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_1","nodeName":"开始","nodeType":"start"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_95","nodeName":"白名单用户判断","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_74","nodeName":"科技输出拒绝","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_14","nodeName":"免费规则集","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_15","nodeName":"是否结清180天","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_61","nodeName":"收费规则集 _V2","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_75","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_58","nodeName":"收费规则V2陪跑","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_90","nodeName":"外数测试分组","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_92","nodeName":"非测试组必过","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_77","nodeName":"征信Stage输出","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_24","nodeName":"人行组件","nodeType":"creditReport"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_132","nodeName":"严重逾期捞回标签","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_101","nodeName":"多模型截尾_审批评级_cross_短账龄","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_102","nodeName":"多模型截尾_审批评级_cross_长账龄","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_119","nodeName":"多模型审批评级决策表","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_137","nodeName":"明珠会员贷多模型截尾","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_79","nodeName":"人行征信提现决策_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_134","nodeName":"人行征信提现决策V2.1_新陪跑","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_129","nodeName":"老客用户分组","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_120","nodeName":"存量评级cross_12期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_135","nodeName":"存量评级cross_6期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_121","nodeName":"存量评级cross_3期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_163","nodeName":"评级cross_v5_12期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_164","nodeName":"评级cross_v5_6期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_165","nodeName":"评级cross_v5_3期","nodeType":"decisionTable"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_157","nodeName":"人行征信提现决策V5_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_166","nodeName":"人行征信提现决策V4_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_140","nodeName":"是否会员卡审批放开","nodeType":"decisionTree"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_141","nodeName":"是否会员卡放开","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_167","nodeName":"策略版本分组","nodeType":"classify"},{"decisionId":"20240701154849417withdraw_approval_personalloan74051_1_1","nodeCode":"jcl_20230728000001_117","nodeName":"人行征信提现决策V4","nodeType":"ruleBase"}]} |  |  |  |  |  |  | 2024-07-01 |  |  |  | F | SSP | SSP |  |  |  |  |  |  |  |  |  | 9 | 10.0 |  |  |  | SSP | SSP | SSP |  |  |  |  |  |  |  |  |  | 9 | 8.0 |  |  |  |  |  |  |  |  |  |  |  |  | 0.0 | 0.0 |  | nvip | 930000 | reject | reject |  |  |  |  | 9 | 10.0 | out-out |  |  |  |  | F | SSP |  |  | F |  | 老客其他 | 老客其他 | V4 | 0.1334123307954337 | 非征信好人 | 23.0 | 10,000~20,000 | 高中/中专/技校 | 4 | 1 |  | 2.48736429090286 |  |
| 2024070100001700000009370424 | 2024070100001700000006554835 | 2024070100001700000009370424 | 加复贷 | 2024070100001700000006554835 | 2024070100001700000006554835 | 2024-07-01 16:58:00 | 2024-07-01 16:17:44 | 2024-07-01 | 2024-06-28 | 2024-07 | lIZRXz1eEYQqlPif/PcCch9IGRdRHJeNG9z4oJ/j8zI= | zw+Eleh++RZ//7i6/EcVXw== | 1022613170 | CTL08bec40c97090c20949847d150a120e30 | xyf01 | xyf01 | APP流量 | 1 | I36 | personal_loan | 12 | 2024-07-01 17:10:18 | 110000 | pass | pass | success |  | syxj_cash |  |  | 151 | 短账龄 | 202402011653310279410939 | 2024-02-01 16:53:31 | 其他 | API流量 | 首借API | xyf01_jdd | 5 | 2000.0 | 888.04 | 1111.96 | 1500.0 | 2026-04-03 00:00:00 | 2000.0 | 0.0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10.0 | 14.0 | 19.0 | 31.0 | 38.0 | 54.0 | 0.0 | 0.0 | 5.0 | 5.0 | 0.1 | 26 | 0 | 汉 | 未婚 | 广东省 | 揭阳市 | 三线 |  | 1 |  |  | 风控通过 | 风控通过 |  |  | 非调额组 | -1 | 0 | android | android | API流量 | APP流量 | V4 | B4评级 | 45 | 4576591008187624144506775712234083055826410524249608747642469942714221837412394074360133912448699190 |  |  |  |  | 7.0 | 3.1 | 3.1 | 3.2 | 3.2 |  |  |  |  | G | C2 |  |  |  |  |  |  |  | 3.1 | C2 |  |  |  |  |  |  | 非额外放开 | 无APP放款 | API拉回APP | API拉回APP | 非飞跃测试客户 |  |  |  |  |  |  |  |  |  |  |  |  | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 1.0 | 0.0 | 0.0 | 0.0 |  |  | 0.0 |  |  | 0.0 |  |  | 1 | 20240701164909904withdraw_approval_personalloan80812_1_1 | 2024-07-01 16:49:09 | PASS | {"_innerResult":"null","activate_inner_app":"xyf01_jdd","adj_risk_price_reason_input":"2001","age":26,"app":"xyf01","baihang_maxOverdueStatus":"0","baihang_p2pEscapeDebtStatus":"0","baihang_supremeCourtExecutedStatus":"0","bairong_als_145":15,"bairong_als_158_15d_status":"14.0","bairong_als_261":25,"bairong_als_274":19,"bairong_als_274_30d_status":"17.0","bairong_als_274_adj_limit_status":"20.0","bairong_als_389":70,"bairong_als_402_30d_status":"27.0","bairong_als_402_adj_limit_status":"32.0","bairong_als_554_90d_status":"31.0","biz_flow_number":"2024070100001700000006554835","biz_type":"xjd_withdraw","blacklist_risk_level":-999,"cashloan_bill_clear_period":-999,"cashloan_order_periods":12,"cashloan_white_list":false,"company_position":"事业单位","count_success_cash_order":1,"count_success_cash_order_without_app":1,"count_unpaid_loan_cash_not_current_app_no_M":0,"count_unpaid_loan_cash_with_app_no_M":1,"count_unpaid_loan_cash_without_app_no_M":1,"created_time":"2024-07-01 16:17:44","credit_channel":"xinfeirongdan","cum_vip_ctr_amt":"0.0","cum_vip_ctr_amt_v2":"0.0","cum_vip_ctr_amt_v3":"0.0","current_day_withdraw_count":1,"current_loan_type":"personal_loan","cust_no":"CTL08bec40c97090c20949847d150a120e30","days_activation_success":151,"debit_amt_cash_not_current_app":0,"device_id":"202204096f5500b83e","device_id_blacklist":false,"dianhuabang_s113":"0.2433","draw_mob_loan_type":151,"face_verify_full_sourcetype":true,"fd_multiple_draw_creditlevel_stock_creditlevel_cross_api_12":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_api_3":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_api_6":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_api_12":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_api_3":"P","fd_multiple_draw_creditlevel_stock_creditlevel_cross_v5_api_6":"P","fd_multiple_model_creditlevel_b4_cross_risk_level":"3.1","fd_multiple_model_creditlevel_cross_l":"P","fd_multiple_model_creditlevel_cross_s":"ST","final_score":90,"first_loan_inner_app_loan_type":"xyf01_jdd","first_loan_max_paid_period_number_with_app":5,"first_loan_max_paid_period_number_with_loan_type":5,"flow_number":"2024070100001700000006554835","huarong2_13":"0.0","huarong2_15":"0.0","huarong2_17":"0.0","huarong2_22":"5.0","huarong2_337":"0.0","huarong2_338":"0.0","huarong2_340":"0.0","huarong2_341":"0.0","huarong2_342":"0.0","huarong2_343":"0.0","huarong2_345":"0.0","huarong2_346":"0.0","huarong2_347":"0.0","huarong5_1336":"104.0","huarong5_1337":"248.0","huarong5_1338":"316.0","huarong6_38":"3.0","huarong6_39":"12.0","huarong6_40":"13.0","id_card_number":"445281199707034105","id_card_number_blacklist":false,"id_card_number_count_this_device":0,"id_card_valid_date":true,"id_fsovdtotal30d":0,"id_qryorg0d":0,"id_qryorg1h":0,"id_qryorg7d":1,"init_risk_price_input":"I36","innerResult":"","inner_app":"xyf01","interGroup":"jcl_20230728000001_51","ip":"120.229.227.166","is_supplemental_loan_new":true,"jcl_20230728000001_129_NextNodeCode":"jcl_20230728000001_125","jcl_20230728000001_129_classify_name":"api拉回","jcl_20230728000001_145_NextNodeCode":"jcl_20230728000001_130","jcl_20230728000001_145_classify_name":"V4策略","jcl_20230728000001_15_NextNodeCode":"jcl_20230728000001_61","jcl_20230728000001_15_classify_name":"结清180 以内","jcl_20230728000001_42_NextNodeCode":"jcl_20230728000001_51","jcl_20230728000001_42_classify_name":"I36","jcl_20230728000001_75_NextNodeCode":"jcl_20230728000001_58","jcl_20230728000001_75_classify_name":"IRR36","jcl_20230728000001_90_NextNodeCode":"jcl_20230728000001_92","jcl_20230728000001_90_classify_name":"非测试组","jcl_20230728000001_95_NextNodeCode":"jcl_20230728000001_74","jcl_20230728000001_95_classify_name":"非白名单用户","jcl_20230807000002_3_NextNodeCode":"jcl_20230807000002_4","jcl_20230807000002_3_classify_name":"个人分期","jcl_20230807000003_5_NextNodeCode":"jcl_20230807000003_9","jcl_20230807000003_5_classify_name":"加复贷","last_credit_agreement_success_inner_app":"xyf01_jdd","loan_type":"personal_loan","loan_type_last_loan_inner_app":"xyf01_jdd","loan_type_last_reject_date":-9999,"main_order_created_time":"2024-07-01 16:17:44","min_no_paid_period_number_without_app":6,"mingzhu_member_draw_group":"P","mobile":"15766763246","mobile_blacklist":false,"mod_b_batch_personalloan_jfd_stock_creditlevel_hcrh_v5_3_1":"4.0","name":"魏玉婷","order_amount":"110000","order_asset_type_input":"1","order_loan_periods":"12","order_number":"2024070100001700000006554835","overdue_current_cash":0,"overdue_current_consume":0,"overdue_past_cash":0,"overdue_past_cash_30_45":0,"overdue_past_consume":0,"overdue_past_consume_30_45":0,"overdue_past_max_cash":0,"period_borrow_average":9166,"personalloan_fd_6mceng30_b4_jy_v1_1_rev_prob":"0.040958","personalloan_fd_6mceng30_b4_jy_v1_rev_prob":"0.040958","personalloan_fd_dt_risk_price_random_v1":76,"personalloan_fd_multiple_model_rej_v2__lift2":"1.3990141338056503","personalloan_fd_multiple_model_rej_v2_lift2_round":"1.4","personalloan_fd_multiple_model_rej_v3__lift1":"1.4304310139622556","personalloan_fd_multiply_model_laohui_v1_l1":"0.0","personalloan_jfd_account_current_level":"A","personalloan_jfd_draw_creditlevel_ssrh_v2_2_4":"7.0","personalloan_jfd_draw_creditlevel_ssrh_v4":"3.1","personalloan_jfd_draw_creditlevel_ssrh_v5":"3.2","personalloan_jfd_overdue_past_level":1,"personalloan_jfd_stock_creditlevel_hcrh_v2_2_3":"7.0","personalloan_jfd_stock_creditlevel_hcrh_v4_2_1":"3.2","personalloan_reloan_overdue_past_callback":"1","pl_fd_dt_multi_model_random_v1":23,"product_name":"xinyongfei","product_type":"L3","random2":"4576591008187624144506775712234083055826410524249608747642469942714221837412394074360133912448699190","random2_zx_test_rate":"30.0","rate_level":"I001","report_id":"cc12e7a820f4433eb03819b43f9a3151","requestId":"20240701164909904withdraw_approval_personalloan80812_1_1","requester":"lendtrade","rlt_risk_gecision_tek_paid_card_amount":"0.0","ruleHitNum":0,"ruleHitResult":"hit","ruleHitScore":1,"ruleTotalScore":0,"same_source_type":true,"seq_id":"2024070100001700000008821335","sms_bad_1m":0,"sms_fraud_1m":0,"sms_lost_1m":0,"source_type":"android","source_type_native":true,"stage":"02","tek_apl_amt_rte":"0.0","tongdun_1":6,"tongdun_10":14,"tongdun_16":2,"tongdun_19":22,"tongdun_cash_score":77,"tongdun_i_cnt_mobile_v3_Loan_all_90day":1,"uid":"13168489","user_asset_type_output":"36","user_id":"13168489","user_no":"1022613170","vip_apl_amt_rte":"0.0","withdraw_amount":110000,"xinyan_1":"0.1","xinyongfei_crawler_discredit":false,"xyf_api_tx_source_v1":"30.0","xyf_app_source_v1":"20.0","xyf_withdraw_channel_attr_source":"加复贷"} | {"jcl_20230728000001":[{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_1","nodeName":"开始","nodeType":"start"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_95","nodeName":"白名单用户判断","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_74","nodeName":"科技输出拒绝","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_14","nodeName":"免费规则集","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_15","nodeName":"是否结清180天","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_61","nodeName":"收费规则集 _V2","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_75","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_58","nodeName":"收费规则V2陪跑","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_90","nodeName":"外数测试分组","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_92","nodeName":"非测试组必过","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_77","nodeName":"征信Stage输出","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_24","nodeName":"人行组件","nodeType":"creditReport"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_132","nodeName":"严重逾期捞回标签","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_101","nodeName":"多模型截尾_审批评级_cross_短账龄","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_102","nodeName":"多模型截尾_审批评级_cross_长账龄","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_119","nodeName":"多模型审批评级决策表","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_137","nodeName":"明珠会员贷多模型截尾","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_79","nodeName":"人行征信提现决策_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_134","nodeName":"人行征信提现决策V2.1_新陪跑","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_129","nodeName":"老客用户分组","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_125","nodeName":"存量评级cross_api拉回_12期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_126","nodeName":"存量评级cross_api拉回_6期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_127","nodeName":"存量评级cross_api拉回_3期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_159","nodeName":"评级cross_v5_api拉回_12期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_160","nodeName":"评级cross_v5_api拉回_6期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_161","nodeName":"评级cross_v5_api拉回_3期","nodeType":"decisionTable"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_155","nodeName":"人行征信提现决策V5_api拉回_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_158","nodeName":"人行征信提现决策V4_api拉回_陪跑","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_145","nodeName":"策略版本分组","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_130","nodeName":"人行征信提现决策V4","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_42","nodeName":"定价分组","nodeType":"classify"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_51","nodeName":"i36必过","nodeType":"ruleBase"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_115","nodeName":"复贷特征因子陪跑","nodeType":"action"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_98","nodeName":"新模型平台陪跑节点","nodeType":"action"},{"decisionId":"20240701164909904withdraw_approval_personalloan80812_1_1","nodeCode":"jcl_20230728000001_2","nodeName":"结束","nodeType":"end"}]} |  |  |  |  |  |  | 2024-07-01 | P | P | P |  |  |  |  |  |  |  |  |  |  |  |  | 3.1 | 3.2 | P | P | P |  |  |  |  |  |  |  |  |  |  |  |  | 3.2 | 4.0 |  |  |  |  |  |  |  |  |  |  |  |  | 0.0 | 0.0 |  |  | 110000 | pass | pass |  |  |  |  | 3.1 | 3.2 | in-in |  |  |  |  | P | P |  |  | P |  | api拉回app | api拉回app | V4 | 0.0849986862438567 | 非征信好人 | 32.0 | 4,000~6,000 | 专科 | 2 | 2 |  | 1.15315759624138 | 1.15315759624138 |

### 同步来源
- `odps`
