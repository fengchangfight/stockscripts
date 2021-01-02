# 每日股票信息大全

import tushare as ts
import datetime
from datetime import date
import pandas as pd
import sys
from collections import defaultdict
# 本文件依赖stock_basic_info.py和stock_bak_daily.py的产出文件作为输入


def formatDate(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def normalize2weekday(dt):
    _, _, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


todayStr = formatDate(normalize2weekday(date.today()))
if(len(sys.argv) > 1 and sys.argv[1] != None):
    todayStr = sys.argv[1]

basic_info_file = '/Users/xiefengchang/life/stockbasic_info_'+todayStr+'.xlsx'
stock_bak_info = '/Users/xiefengchang/life/stockdaily_bak_output_'+todayStr+'.xlsx'
# yesterdayStr = formatDate(normalize2weekday(
#     date.today() - datetime.timedelta(days=1)))

date_str = todayStr
token = "c0b191a58ac95478267a597abbcf656bec52aa9ec52afa3d1228bfbf"
ts.set_token(token)
pro = ts.pro_api()


def inner_def_value():
    return ''


def def_value():
    return defaultdict(inner_def_value)


def get_code_map_from_basic_info():
    result_dict = defaultdict(def_value)
    excel_data_df = pd.read_excel(basic_info_file, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['代码', '名称', '地区', '行业', '上市日期'])
    for _, row in df.iterrows():
        code = row['代码']
        result_dict[code] = row
    return result_dict


def get_stock_bak_dict():
    result_dict = defaultdict(def_value)
    excel_data_df = pd.read_excel(stock_bak_info, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['代码',
                                              '内盘', '外盘', '开盘价', '最高价', '最低价', '总市值', '强弱度', '活跃度'])
    for _, row in df.iterrows():
        code = row['代码']
        result_dict[code] = row
    return result_dict


print("the base date used is:{0}".format(date_str))
df = pro.daily_basic(ts_code='', trade_date=date_str,
                     fields='ts_code,trade_date,total_mv,volume_ratio,pe,pe_ttm,pb,dv_ratio,total_share,turnover_rate,close')

name_map = {'ts_code': '代码',
            'trade_date': '交易日期',
            'total_mv': '总市值',
            'volume_ratio': '量比',
            'pe': '市盈率',
            'pe_ttm': 'TTM市盈率',
            'pb': '市净率',
            'dv_ratio': '股息率',
            'total_share': '总股本',
            'turnover_rate': '换手率',
            'name': '名称',
            'close': '当日收盘价',
            'industry': '行业',
            'selling': '内盘',
            'open': '开盘价',
            'low': '最低价',
            'high': '最高价',
            'strength': '强弱度',
            'activity': '活跃度'
            }
col_order = ['ts_code', 'name', 'industry', 'trade_date', 'total_mv',
             'volume_ratio', 'pe', 'pe_ttm', 'pb', 'dv_ratio', 'total_share', 'turnover_rate', 'close', 'selling', 'open', 'low', 'high', 'strength', 'activity']
custom_header = [name_map[r] for r in col_order]
basic_dict = get_code_map_from_basic_info()
bak_dict = get_stock_bak_dict()


def row_property_extractor(row_dict, ts_code, property_name):
    return row_dict[ts_code][property_name]


#df.columns = ['代码','交易日期','总市值','量比','市盈率','市净率','换手率']
df['name'] = df.apply(lambda row: row_property_extractor(
    basic_dict, row.ts_code, '名称'), axis=1)
df['industry'] = df.apply(lambda row: row_property_extractor(
    basic_dict, row.ts_code, '行业'), axis=1)
df['selling'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '内盘'), axis=1)
df['open'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '开盘价'), axis=1)
df['low'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '最低价'), axis=1)
df['high'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '最高价'), axis=1)
df['strength'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '强弱度'), axis=1)
df['activity'] = df.apply(lambda row: row_property_extractor(
    bak_dict, row.ts_code, '活跃度'), axis=1)
df.to_excel("/Users/xiefengchang/life/stockdaily_merged_output_"+date_str +
            ".xlsx", index=False, columns=col_order, header=custom_header)
