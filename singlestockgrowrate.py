import tushare as ts
import datetime
from datetime import date
import pandas as pd
import time

input_stock_basic = '/Users/xiefengchang/life/stockbasic_info.xlsx'

token = "c0b191a58ac95478267a597abbcf656bec52aa9ec52afa3d1228bfbf"
ts.set_token(token)

pro = ts.pro_api()


def normalize2weekday(dt):
    _, _, day_of_week = dt.isocalendar()
    if(day_of_week == 6):
        return dt - datetime.timedelta(days=1)
    elif(day_of_week == 7):
        return dt - datetime.timedelta(days=2)
    else:
        return dt


def goBack1Year(dt):
    oneYearAgo = dt - datetime.timedelta(days=1*365)
    # print("one year ago: {0} of date : {1}".format(oneYearAgo, dt))
    return oneYearAgo


def date2formatstring(dt):
    format = "%Y%m%d"
    return dt.strftime(format)


def get_price_of_date(ts_code, dt):
    dtstr = date2formatstring(dt)
    df = pro.daily(ts_code=ts_code, start_date=dtstr, end_date=dtstr)
    if(df.shape[0] < 1):
        avg_price = -1
    else:
        avg_price = (df.loc[0].open+df.loc[0].close)/2
    print("getting price of {0} at {1} at avg_price: {2}".format(
        ts_code, dt, avg_price))
    return avg_price


def gobackcheck(ts_code):
    dt = normalize2weekday(date.today())
    previous_price = None
    price = None
    cnt = 0
    grow = 0
    while(True):
        # if(cnt != 0 and cnt % 100 == 0):
        #     print("waiting for 10 secs as reaching cnt {0}".format(cnt))
        #     time.sleep(20)
        if(previous_price is None):
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
    grow_rate = grow/cnt
    print("stock: {0}, growrate: {1}, {2} grow in {3} years".format(
        ts_code, "{0:.1%}".format(grow_rate), grow, cnt))
    return grow_rate


def load_all_ts_code_and_analyze():
    excel_data_df = pd.read_excel(input_stock_basic, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['代码', '名称'])
    df['consec_grow_years'] = df.apply(
        lambda row: gobackcheck(row['代码']), axis=1)
    df.to_excel("/Users/xiefengchang/life/stock_consec_grow_"+todayStr +
                ".xlsx", index=False)


if __name__ == "__main__":
    # load_all_ts_code_and_analyze()
    gobackcheck('300061.SZ')
