import tushare as ts
import datetime
from datetime import date
import pandas as pd

basic_info_file = '/Users/xiefengchang/life/stockbasic_info.xlsx'


def get_code_map_from_basic_info():
    result_dict = {}
    excel_data_df = pd.read_excel(basic_info_file, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['代码', '名称', '地区', '行业', '上市日期'])
    for index, row in df.iterrows():
        code = row['代码']
        result_dict[code] = row
    return result_dict


def formatDate(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def normalizeDate(dt):
    year, week_num, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


todayStr = formatDate(normalizeDate(date.today()))

token = "c0b191a58ac95478267a597abbcf656bec52aa9ec52afa3d1228bfbf"
ts.set_token(token)


pro = ts.pro_api()
df = pro.daily_basic(ts_code='', trade_date=todayStr,
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
            'industry': '行业'
            }
col_order = ['ts_code', 'name', 'industry', 'trade_date', 'total_mv',
             'volume_ratio', 'pe', 'pe_ttm', 'pb', 'dv_ratio', 'total_share', 'turnover_rate', 'close']
custom_header = [name_map[r] for r in col_order]
basic_dict = get_code_map_from_basic_info()
#df.columns = ['代码','交易日期','总市值','量比','市盈率','市净率','换手率']
df['name'] = df.apply(lambda row: basic_dict[row.ts_code]['名称'], axis=1)
df['industry'] = df.apply(lambda row: basic_dict[row.ts_code]['行业'], axis=1)
df.to_excel("/Users/xiefengchang/life/stockdaily_output_"+todayStr +
            ".xlsx", index=False, columns=col_order, header=custom_header)
