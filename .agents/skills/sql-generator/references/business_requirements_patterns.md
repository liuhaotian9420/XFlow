# 常见业务需求模式

这个文件不是表结构说明，而是给 `sql-generator` 提示“用户真正想要什么”的需求模板。

## 1. 监控看板类

典型说法：
- 看今天/本月放款情况
- 看完成度
- 看风险通过和资金通过
- 看余额和在贷

适合输出：
- 日报 SQL
- 月累计 SQL
- 分渠道/分客群监控 SQL

优先参考：
- `ads_inloan_loan_monitor_screen_df.sql`
- `ads_inloan_loan_pass_monitor_df.sql`
- `ads_inloan_loan_balance_mthly_df.sql`

## 2. 漏斗转化类

典型说法：
- 看注册到授信
- 看授信到提现
- 看提现到放款
- 看不同渠道转化率

适合输出：
- 分阶段漏斗 SQL
- 渠道转化 SQL
- 分层转化 SQL

优先参考：
- `APP新客转化-注册口径.ipynb`
- `APP新客转化-授信口径.ipynb`
- `授信口径转化率_虚假给额.ipynb`

## 3. 专项策略评估类

典型说法：
- 看虚假给额影响
- 看额外放开效果
- 看 API 拉回 APP 表现
- 看不同价格带效果

适合输出：
- 对照组/实验组比较 SQL
- 标签分层效果 SQL
- 人群拆分 SQL

优先参考：
- `授信口径转化率_虚假给额.ipynb`
- `老客月会sql代码.ipynb`
- `xyf_jingying.weekly_analysis_report_df_lss.txt`

## 4. 月会/周会复盘类

典型说法：
- 做月会分析
- 做周报
- 做专题复盘
- 做经营汇报材料

适合输出：
- 多段 SQL 组合
- 同一主题下多个结果表
- 宽口径复盘 SQL

优先参考：
- `老客月会sql代码.ipynb`
- `xyf_jingying.weekly_analysis_report_df_lss.txt`
- `xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt`

## 5. 商业化收入类

典型说法：
- 看会员卡收入
- 看退款和净收入
- 看 T0/T7/T30/T60 累计收入

适合输出：
- 收入动态 SQL
- 周/月累计 SQL
- 产品类型对比 SQL

优先参考：
- `xyf_jingying.weekly_analysis_report_vip_dynamic_income_lss.txt`
- `老客月会sql代码.ipynb`
