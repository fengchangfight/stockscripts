import tushare as ts

token="****"
ts.set_token(token)
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
# output to excel of type <class 'pandas.core.frame.DataFrame'>
data.to_excel("/tmp/stockbasic_output.xlsx") 

