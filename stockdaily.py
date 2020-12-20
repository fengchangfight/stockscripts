import tushare as ts
import datetime
from datetime import date

def formatDate(dt):
    format = "%Y%m%d";
    return dt.strftime(format)
def normalizeDate(dt):
    year, week_num, day_of_week = dt.isocalendar()
    if(day_of_week==6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week==7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt

todayStr = formatDate(normalizeDate(date.today()))

token="****"
ts.set_token(token)
    

pro = ts.pro_api()
df = pro.daily_basic(ts_code='', trade_date=todayStr, fields='ts_code,trade_date,total_mv,volume_ratio,pe,pb,turnover_rate')

col_order=['ts_code','trade_date','total_mv','volume_ratio','pe','pb','turnover_rate']
#df.columns = ['代码','交易日期','总市值','量比','市盈率','市净率','换手率']
df.to_excel("/tmp/stockbasic_output_"+todayStr+".xlsx", index=False, columns=col_order) 
