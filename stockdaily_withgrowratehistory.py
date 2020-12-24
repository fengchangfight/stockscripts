import tushare as ts
import datetime
from datetime import date
import pandas as pd
import time

basic_info_file = '/Users/xiefengchang/life/stockbasic_info.xlsx'


def get_code_map_from_basic_info():
    result_dict = {}
    excel_data_df = pd.read_excel(basic_info_file, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['代码', '名称', '地区', '行业', '上市日期'])
    for _, row in df.iterrows():
        code = row['代码']
        result_dict[code] = row
    return result_dict


def formatDate(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def goBack1Year(dt):
    oneYearAgo = dt - datetime.timedelta(days=1*365)
    return oneYearAgo


def get_price_of_date(ts_code, dt):
    dtstr = formatDate(dt)
    df = pro.daily(ts_code=ts_code, start_date=dtstr, end_date=dtstr)
    if(df.shape[0] < 1):
        return -1
    avg_price = (df.loc[0].open+df.loc[0].close)/2
    # print("getting price of {0} at {1} at avg_price: {2}".format(
    #     ts_code, dt, avg_price))
    return avg_price


def normalize2weekday(dt):
    _, _, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


def gobackcheck(ts_code):
    dt = normalize2weekday(date.today())
    previous_price = None
    price = None
    cnt = 0
    grow = 0
    while(True):
        if(cnt != 0 and cnt % 100 == 0):
            print("waiting for 10 secs as reaching cnt {0}".format(cnt))
            time.sleep(20)
        if(previous_price == None):
            previous_price = get_price_of_date(ts_code, dt)
            dt = normalize2weekday(goBack1Year(dt))
        else:
            price = get_price_of_date(ts_code, dt)
            if(price == -1):
                break
            if(previous_price > price):
                grow += 1
            previous_price = price
            dt = normalize2weekday(goBack1Year(dt))
            cnt += 1
    if(cnt == 0):
        print("less than one year stock: {0}, skip".format(ts_code))
        return -1
    grow_rate = grow/cnt
    print("stock: {0}, growrate: {1}, {2} grow in {3} years".format(
        ts_code, "{0:.1%}".format(grow_rate), grow, cnt))
    return grow_rate


todayStr = formatDate(normalize2weekday(date.today()))
yesterdayStr = formatDate(normalize2weekday(
    date.today() - datetime.timedelta(days=1)))

date_str = yesterdayStr

token = "c0b191a58ac95478267a597abbcf656bec52aa9ec52afa3d1228bfbf"
ts.set_token(token)


pro = ts.pro_api()
print("yesterday is:{0}".format(date_str))
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
            'consec_grow_years': '连续增长年'
            }
col_order = ['ts_code', 'name', 'industry', 'trade_date', 'total_mv',
             'volume_ratio', 'pe', 'pe_ttm', 'pb', 'dv_ratio', 'total_share', 'turnover_rate', 'close', 'consec_grow_years']
custom_header = [name_map[r] for r in col_order]
basic_dict = get_code_map_from_basic_info()
#df.columns = ['代码','交易日期','总市值','量比','市盈率','市净率','换手率']
df['name'] = df.apply(lambda row: basic_dict[row.ts_code]['名称'], axis=1)
df['industry'] = df.apply(lambda row: basic_dict[row.ts_code]['行业'], axis=1)
df['consec_grow_years'] = df.apply(
    lambda row: gobackcheck(row.ts_code), axis=1)
df.to_excel("/Users/xiefengchang/life/stockdaily_output_"+date_str +
            ".xlsx", index=False, columns=col_order, header=custom_header)
