# 股票基础信息，每日变动不大，但是碰到新公司上市等可能会有一些变更

import tushare as ts
import datetime
from datetime import date
import pandas as pd
import sys


def formatDate(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def normalize_date2weekday(dt):
    _, _, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


todayStr = formatDate(normalize_date2weekday(date.today()))
if(len(sys.argv) > 1 and sys.argv[1] != None):
    todayStr = sys.argv[1]

token = "***"
ts.set_token(token)
pro = ts.pro_api()
data = pro.stock_basic(exchange='', list_status='L',
                       fields='ts_code,name,area,industry,list_date')
col_names = ['ts_code', 'name', 'area', 'industry', 'list_date']
col_map = {
    "ts_code": "代码",
    "name": "名称",
    "area": "地区",
    "industry": "行业",
    "list_date": "上市日期"
}
cust_header = [col_map[x] for x in col_names]
data.to_excel("/Users/xiefengchang/life/stockbasic_info_"+todayStr+".xlsx",
              header=cust_header, index=False)
