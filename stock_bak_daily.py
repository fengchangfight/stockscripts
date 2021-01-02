# 跟stock daily类似，包含一些额外维度的股票信息
import tushare as ts
import datetime
from datetime import date
import pandas as pd
import sys


def formatDate(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def normalizeDate(dt):
    _, _, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


todayStr = formatDate(normalizeDate(date.today()))

if(len(sys.argv) > 1 and sys.argv[1] != None):
    todayStr = sys.argv[1]


token = "***"
ts.set_token(token)


pro = ts.pro_api()
df = pro.bak_daily(ts_code='', trade_date=todayStr,
                   fields='ts_code,name,trade_date,vol_ratio,selling,buying,open,close,high,low,total_mv,strength,activity')

name_map = {'ts_code': '代码',
            'name': '股票名称',
            'trade_date': '交易日',
            'vol_ratio': '量比',
            'selling': '内盘',
            'buying': '外盘',
            'open': '开盘价',
            'close': '收盘价',
            'high': '最高价',
            'low': '最低价',
            'total_mv': '总市值',
            'strength': '强弱度',
            'activity': '活跃度'
            }
col_order = ['ts_code', 'name', 'trade_date', 'vol_ratio', 'selling',
             'buying', 'open', 'close', 'high', 'low', 'total_mv', 'strength', 'activity']
custom_header = [name_map[r] for r in col_order]
df.to_excel("/Users/xiefengchang/life/stockdaily_bak_output_"+todayStr +
            ".xlsx", index=False, columns=col_order, header=custom_header)
