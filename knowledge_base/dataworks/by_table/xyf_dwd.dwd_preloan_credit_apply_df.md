# xyf_dwd.dwd_preloan_credit_apply_df

## 来源文件
- ads_inloan_loan_pass_monitor_df.sql
- APP新客转化-授信口径.ipynb
- APP新客转化-注册口径.ipynb
- dws_inloan_loan_channel_stat_df.sql
- dws_inloan_loan_risk_stat_df.sql
- 授信口径转化率_虚假给额.ipynb

- `CASE WHEN lower(inner_app) IN ('xyf01','fxk','cxh') THEN "app" ELSE "api" END AS ap_flg`
- `DATE(created_time) AS row_crt_ts_date`
- `MAX(CASE WHEN STATUS = 2 THEN 1 ELSE 0 END) AS shouxin_cnt`
- `MAX(created_time) AS created_time`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| id | BIGINT | column | 自增id |  |
| apply_id | STRING | column | 授信申请流水id,标识唯一一次申请 |  |
| apply_source | STRING | column | 授信申请来源标识 | Y |
| account_no | STRING | column | 账户号，从ams获取 |  |
| cust_no | STRING | column | 客户号（身份证号维度） | Y |
| app | STRING | column | app名 | Y |
| user_no | STRING | column | 用户号（手机号+APP维度） |  |
| inner_app | STRING | column | inner_app | Y |
| reject_code | STRING | column | 拒绝原因码 |  |
| biz_flow_number | STRING | column | 业务流水号 |  |
| status | BIGINT | column | 审核状态 0等待中，1审核中，2审批通过，3审批拒绝，4超时，6执行错误 |  |
| status_name | STRING | column | 审核状态 0等待中，1审核中，2审批通过，3审批拒绝，4超时，6执行错误 |  |
| agreement_no | STRING | column | 授信协议号(授信成功后生成) |  |
| loan_type | STRING | column | 申请类型 |  |
| utm_source | STRING | column | 申请渠道类型 |  |
| product_type | STRING | column | 申请类型 |  |
| created_time | DATETIME | column | 创建时间 | Y |
| updated_time | DATETIME | column | 更新时间 |  |
| mobile | STRING | column | 手机号密文 |  |
| device_id | STRING | column | 设备id |  |
| ip | STRING | column | 申请ip |  |
| source_type | STRING | column | 设备类型 |  |
| init_credit_line | BIGINT | column | 初始授信额度(分) |  |
| credit_expire_date | DATETIME | column | 授信失效日期 |  |
| credit_success_time | DATETIME | column | 授信成功时间 |  |
| credit_renew_time | DATETIME | column | 授信协议续签时间 |  |
| risk_price | STRING | column | 风险定价 |  |
| risk_level | STRING | column | 风险等级 |  |
| rate_level | STRING | column | 费率等级 |  |
| user_asset_type | STRING | column | 用户资产类型 |  |
| client_code | STRING | column | 端码 |  |
| request | STRING | column | 进件参数 |  |
| is_multiple_apply | BIGINT | column |  |  |
| app_activation_type | STRING | column | 激活类型「首复贷标识」 |  |
| is_exists_agreementno | INT | column | 是否重新给额度(1:是，0:否) |  |
| id_card_number | STRING | column | 身份证号 |  |
| user_name | STRING | column | 用户姓名(用户申请时) |  |
| recoup_flag | BIGINT | column | 是否跨域回捞  1：是 0：否 |  |
| recoup_success | BIGINT | column | 是否回捞通过 1：是 0：否 |  |
| report_id | STRING | column | report_id |  |
| os | STRING | column | 操作系统 |  |
| app_version | STRING | column | app版本号 |  |
| biz_type | STRING | column | 业务类型 |  |
| credit_mode | STRING | column | 授信模式  normal：普通模式，simple：极简模式 |  |
| is_deleted | BIGINT | column | 当前授信记录用户是否注销账户(1 是 0 否) |  |
| standard_scene | STRING | column | 标准场景码 |  |
| audit_result | STRING | column | 审核结果 |  |
| extension | STRING | column | 拓展字段 |  |
| pt | STRING | column |  | Y |
| pt | STRING | partition |  | Y |

#### DDL
```sql
CREATE TABLE xyf_dwd.`dwd_preloan_credit_apply_df` (
  `id` BIGINT COMMENT '自增id',
  `apply_id` STRING COMMENT '授信申请流水id,标识唯一一次申请',
  `apply_source` STRING COMMENT '授信申请来源标识',
  `account_no` STRING COMMENT '账户号，从ams获取',
  `cust_no` STRING COMMENT '客户号（身份证号维度）',
  `app` STRING COMMENT 'app名',
  `user_no` STRING COMMENT '用户号（手机号+APP维度）',
  `inner_app` STRING COMMENT 'inner_app',
  `reject_code` STRING COMMENT '拒绝原因码',
  `biz_flow_number` STRING COMMENT '业务流水号',
  `status` BIGINT COMMENT '审核状态 0等待中，1审核中，2审批通过，3审批拒绝，4超时，6执行错误',
  `status_name` STRING COMMENT '审核状态 0等待中，1审核中，2审批通过，3审批拒绝，4超时，6执行错误',
  `agreement_no` STRING COMMENT '授信协议号(授信成功后生成)',
  `loan_type` STRING COMMENT '申请类型',
  `utm_source` STRING COMMENT '申请渠道类型',
  `product_type` STRING COMMENT '申请类型',
  `created_time` DATETIME COMMENT '创建时间',
  `updated_time` DATETIME COMMENT '更新时间',
  `mobile` STRING COMMENT '手机号密文',
  `device_id` STRING COMMENT '设备id',
  `ip` STRING COMMENT '申请ip',
  `source_type` STRING COMMENT '设备类型',
  `init_credit_line` BIGINT COMMENT '初始授信额度(分)',
  `credit_expire_date` DATETIME COMMENT '授信失效日期',
  `credit_success_time` DATETIME COMMENT '授信成功时间',
  `credit_renew_time` DATETIME COMMENT '授信协议续签时间',
  `risk_price` STRING COMMENT '风险定价',
  `risk_level` STRING COMMENT '风险等级',
  `rate_level` STRING COMMENT '费率等级',
  `user_asset_type` STRING COMMENT '用户资产类型',
  `client_code` STRING COMMENT '端码',
  `request` STRING COMMENT '进件参数',
  `is_multiple_apply` BIGINT,
  `app_activation_type` STRING COMMENT '激活类型「首复贷标识」',
  `is_exists_agreementno` INT COMMENT '是否重新给额度(1:是，0:否)',
  `id_card_number` STRING COMMENT '身份证号',
  `user_name` STRING COMMENT '用户姓名(用户申请时)',
  `recoup_flag` BIGINT COMMENT '是否跨域回捞  1：是 0：否',
  `recoup_success` BIGINT COMMENT '是否回捞通过 1：是 0：否',
  `report_id` STRING COMMENT 'report_id',
  `os` STRING COMMENT '操作系统',
  `app_version` STRING COMMENT 'app版本号',
  `biz_type` STRING COMMENT '业务类型',
  `credit_mode` STRING COMMENT '授信模式  normal：普通模式，simple：极简模式',
  `is_deleted` BIGINT COMMENT '当前授信记录用户是否注销账户(1 是 0 否)',
  `standard_scene` STRING COMMENT '标准场景码',
  `audit_result` STRING COMMENT '审核结果',
  `extension` STRING COMMENT '拓展字段'
)
COMMENT '授信有效期变更日志表'
PARTITIONED BY (
  `pt` STRING NOT NULL
)
STORED AS AliOrc
LIFECYCLE 365
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C671D432E7475A6BE67FE3 Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - lowfrequency, longterm and coldarchive tier is not support to read now.
