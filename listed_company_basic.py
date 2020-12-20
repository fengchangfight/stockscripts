import tushare as ts

token="****"
ts.set_token(token)
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,name,area,industry,list_date')
col_names=['ts_code','name','area','industry','list_date']
col_map={
    "ts_code":"代码",
"name":"名称",
"area":"地区",
"industry":"行业",
"list_date":"上市日期"
}
cust_header = [ col_map[x] for x in col_names]
data.to_excel("/Users/xiefengchang/life/stockbasic_info.xlsx", header=cust_header, index=False) 
