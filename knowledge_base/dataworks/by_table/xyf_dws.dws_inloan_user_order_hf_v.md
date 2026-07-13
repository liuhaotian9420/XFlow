# xyf_dws.dws_inloan_user_order_hf_v

## 来源文件
- 老客月会sql代码.ipynb

- `COUNT(DISTINCT CASE WHEN b.loan_status = 'success' THEN b.app_user_id END) loan_succeed_user_cnt`
- `COUNT(DISTINCT CASE WHEN b.risk_status = 'pass' THEN b.app_user_id END) risk_passed_user_cnt`
- `COUNT(DISTINCT b.app_user_id) applied_user_cnt`
- `COUNT(DISTINCT user_no) user_cnt`
- `SUM(CASE WHEN b.loan_status = 'success' THEN b.amount END) loan_succeed_amount`

### 表结构
| 字段名 | 数据类型 | 字段角色 | 注释 | Ground Truth |
| --- | --- | --- | --- | --- |
| order_number | STRING | column |  |  |
| first_order_number | STRING | column |  |  |
| first_order_time | DATETIME | column |  | Y |
| apply_time | DATETIME | column |  |  |
| app_user_id | BIGINT | column |  | Y |
| product_type | STRING | column |  |  |
| loan_type | STRING | column |  |  |
| app | STRING | column |  | Y |
| inner_app | STRING | column |  | Y |
| utm_source | STRING | column |  |  |
| fund_source | STRING | column |  |  |
| risk_status | STRING | column |  | Y |
| loan_status | STRING | column |  | Y |
| loan_time | DATETIME | column |  |  |
| period | BIGINT | column |  |  |
| amount | DECIMAL(38,18) | column |  | Y |
| loan_type_flag | STRING | column |  | Y |
| risk_price | STRING | column |  |  |
| rel_risk_price | STRING | column |  |  |
| asset_type | STRING | column |  |  |

#### DDL
```sql
CREATE VIEW xyf_dws.`dws_inloan_user_order_hf_v` (
  `order_number`,
  `first_order_number`,
  `first_order_time`,
  `apply_time`,
  `app_user_id`,
  `product_type`,
  `loan_type`,
  `app`,
  `inner_app`,
  `utm_source`,
  `fund_source`,
  `risk_status`,
  `loan_status`,
  `loan_time`,
  `period`,
  `amount`,
  `loan_type_flag`,
  `risk_price`,
  `rel_risk_price`,
  `asset_type`
)
AS SELECT 
	 t100.order_number 	as order_number  
	,t100.first_order_number as first_order_number
	,t100.first_order_time    as first_order_time
	,t100.first_order_time    as apply_time
	,t100.user_no 		as app_user_id	
	,t100.product_type  as product_type	 
	,t99.loan_flag 		as loan_type	
	,t100.app			as app			
	,t100.inner_app		as inner_app	
	,t100.utm_source 	as utm_source	
	,t100.fund_source 	as fund_source 	
	,t100.risk_status 	as risk_status
	,t100.loan_status 	as loan_status
	,t100.loan_time 	as loan_time
	,t100.period
	,t100.loan_amt*100 		as amount 
	,t99.loan_flag 		 as loan_type_flag	
		,t100.risk_price
		,t100.rel_risk_price 
		,t100.asset_type
FROM	(
		SELECT 
			 first_order_number
			,fund_order_number
			,first_order_time	
			,user_no 			
			,cust_no			
			,product_type 	
			,fund_source 		
			,period			
			,loan_amt			
			,loan_time     	
			,inner_app		
			,app				
			,utm_source
			,loan_status 		
			,failed_code 		
			,failed_reason 	
			,risk_status		
			,cnl_pd_code 		
			,biz_flow_number 	
			,coupon_id
			,out_order_number 
			,loan_req_poll_no_max as order_route
			,order_number
			,ori_loan_status
			,risk_price
			,rel_risk_price
			,asset_type
		from 
				(
        		    SELECT 
						 t1.ori_order_number		as first_order_number 		
						,t1.fund_order_number		as fund_order_number 		
						,t1.main_date_created		as first_order_time			
						,t1.user_no					as user_no 					
						,t1.cust_no					as cust_no					
						,t1.product_type			as product_type 			
						,t1.fund_source_old			as fund_source 				
						,t1.period					as period					
						,t1.loan_amt				as loan_amt					
						,t1.date_cash				as loan_time     			
						,t1.loan_source			as inner_app				
						,t1.old_app					as app						
						,t1.utm_source 				as utm_source

						,case when t1.main_status_code='03' then 'success' 
							  when t1.main_status_code='04' then 'failed'
						else 'process' end 			as loan_status	
						,t1.main_failed_code		as failed_code 			
						,t1.main_failed_reason		as failed_reason 		
						,t1.main_risk_status		as risk_status			
						,t1.cnl_pd_code				as cnl_pd_code 			
						,t1.main_biz_flow_number	as biz_flow_number 		
						,t1.coupon_id 				as coupon_id
						,t2.order_no 				as out_order_number 	
						,max(t1.loan_req_poll_no) OVER (PARTITION BY t1.ori_order_number) as loan_req_poll_no_max
						,t1.loan_req_poll_no 		as loan_req_poll_no
						,t1.order_number as order_number
						,t1.main_status_code		as ori_loan_status				
						,t1.main_risk_price_old    	as risk_price
            			,concat(t1.main_risk_price_type,t1.main_risk_price*100) as rel_risk_price 
            			,t1.main_asset_type         as asset_type
        		    from xyf_dwd.dwd_inloan_loan_apply_hf t1
				left join  xyf_dwd.dwd_apiopfcore_cash_out_apply_df t2
						on t1.order_number=t2.order_number
						and t2.pt=MAX_PT('xyf_dwd.dwd_apiopfcore_cash_out_apply_df') 
        		    WHERE t1.pt = MAX_PT('xyf_dwd.dwd_inloan_loan_apply_hf') 
					and t1.loan_req_poll_no is not null 
				) aa 
			where aa.loan_req_poll_no_max=aa.loan_req_poll_no
UNION all 
		 SELECT 
						 t1.ori_order_number		as first_order_number 		
						,t1.fund_order_number		as fund_order_number 		
						,t1.main_date_created		as first_order_time			
						,t1.user_no					as user_no 					
						,t1.cust_no					as cust_no					
						,t1.product_type			as product_type 			
						,t1.fund_source_old			as fund_source 				
						,t1.period					as period					
						,t1.loan_amt				as loan_amt					
						,t1.date_cash				as loan_time     			
						,t1.loan_source			as inner_app				
						,t1.old_app					as app						
						,t1.utm_source 				as utm_source

						,case when t1.main_status_code='03' then 'success' 
							  when t1.main_status_code='04' then 'failed'
								else 'process' end 			as loan_status	
						,t1.main_failed_code		as failed_code 			
						,t1.main_failed_reason		as failed_reason 		
						,t1.main_risk_status		as risk_status			
						,t1.cnl_pd_code				as cnl_pd_code 			
						,t1.main_biz_flow_number	as biz_flow_number 		
						,t1.coupon_id 				as coupon_id
						,t2.order_no 				as out_order_number 	
						,1 							as order_route
						,t1.ori_order_number		as order_number
						,t1.main_status_code		as ori_loan_status
						,t1.main_risk_price_old    	as risk_price
            			,concat(t1.main_risk_price_type,t1.main_risk_price*100) as rel_risk_price 
            			,t1.main_asset_type         as asset_type
        		    from xyf_dwd.dwd_inloan_loan_apply_hf t1
				left join  xyf_dwd.dwd_apiopfcore_cash_out_apply_df t2
						on t1.ori_order_number=t2.order_number
						and t2.pt=MAX_PT('xyf_dwd.dwd_apiopfcore_cash_out_apply_df') 
        		    WHERE t1.pt = MAX_PT('xyf_dwd.dwd_inloan_loan_apply_hf') 
					and t1.loan_req_poll_no is null 
UNION all   
                   		 SELECT 
						 t1.first_order_number		as first_order_number 		
						,t1.fund_order_number		as fund_order_number 		
						,t1.first_order_time		as first_order_time			
						,t1.app_user_id2			as user_no 					
						,t1.cust_no2				as cust_no					
						,t1.product_type			as product_type 			
						,t1.fund_source				as fund_source 				
						,t1.period					as period					
						,cast (t1.amount/100 as Decimal(38,18))		as loan_amt					
						,t1.loan_time				as loan_time     			
						,t1.inner_app				as inner_app				
						,t1.app						as app						
						,t1.utm_source 				as utm_source

						,t1.loan_status				as loan_status
						,t1.failed_code				as failed_code 			
						,t1.failed_reason			as failed_reason 		
						,t1.risk_status				as risk_status			
						,null						as cnl_pd_code 			
						,t1.biz_flow_number			as biz_flow_number 		
						,cast (t1.coupon_id as BIGINT )	as coupon_id
						,t2.order_no 				as out_order_number 	
						,t1.order_route				as order_route
						,t1.order_number 			as order_number
						,case when t1.loan_status='success' then '03' else '04' end as ori_loan_status 	
						,t1.risk_price  as risk_price
						,null 			as rel_risk_price 
						,cast(t1.asset_type2 as string) as asset_type
            from xyf_dwd.dwd_user_order_info_df_backup  t1
		left join  xyf_dwd.dwd_apiopfcore_cash_out_apply_df t2
				on t1.order_number=t2.order_number
				and t2.pt=MAX_PT('xyf_dwd.dwd_apiopfcore_cash_out_apply_df') 
            where date(t1.first_order_time)<'2020-01-01'
	) t100
left JOIN xyf_dwd.dwd_inloan_order_flag_hf t99
	on t100.first_order_number=t99.ori_order_number
	and t99.pt=MAX_PT("xyf_dwd.dwd_inloan_order_flag_hf")
```

### 抽样数据
- 未采样

### 同步来源
- `odps`

### 同步备注
- Sample rows unavailable: MethodNotAllowed: RequestId: 69C6721921C05CCC8FE970C2 Tag: ODPS Endpoint: https://service.cn-beijing.maxcompute.aliyun.com/api
ODPS-0422161: Fail to read VirtualView - View is not allowed to read.
