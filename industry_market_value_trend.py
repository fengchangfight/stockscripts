import matplotlib.pyplot as plt

import pandas as pd
import datetime
import matplotlib.dates as mdates

# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


# Year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
# Unemployment_Rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
# love_Rate = [9.1, 13, 5, 7, 6, 3, 6.2, 6, 5, 6.9]

# plt.plot(Year, Unemployment_Rate, label='un')
# plt.plot(Year, love_Rate, label='love')


input_file = "/Users/xiefengchang/life/industry_market_value_stats.xlsx"


def draw_line(key, list_of_tuple_in_order):
    x, y = map(list, zip(*list_of_tuple_in_order))
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y%m%d'))
    plt.gca().xaxis.set_major_locator(mdates.DayLocator())
    plt.plot([datetime.datetime.strptime(str(dt), '%Y%m%d')
              for dt in x], y, '--o', label=key)
    plt.gcf().autofmt_xdate()

    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)


industries_to_check = ['综合类',
                       '装修装饰',
                       # 专用机械
                       # 种植业
                       # 中成药
                       # 证券
                       # 造纸
                       # 运输设备
                       # 园区开发
                       # 元器件
                       #    '渔业',
                       # 影视音像
                       # 银行
                       '医药商业',
                       # 医疗保健
                       # 新型电力
                       # 小金属
                       # 橡胶
                       # 文教休闲
                       # 铜
                       # 通信设备
                       # 铁路
                       # 特种钢
                       # 陶瓷
                       # 塑料
                       # 饲料
                       # 水运
                       # 水务
                       # 水泥
                       # 水力发电
                       # 食品
                       # 石油贸易
                       # 石油开采
                       # 石油加工
                       # 生物制药
                       # 商品城
                       # 商贸代理
                       # 软饮料
                       # 软件服务
                       # 乳制品
                       # 日用化工
                       # 染料涂料
                       # 全国地产
                       # 区域地产
                       # 轻工机械
                       # 铅锌
                       # 汽车整车
                       # 汽车配件
                       # 汽车服务
                       # 其他商业
                       # 其他建材
                       # 普钢
                       # 啤酒
                       # 批发业
                       # 农用机械
                       # 农业综合
                       # 农药化肥
                       # 摩托车
                       # 煤炭开采
                       # 铝
                       # 旅游景点
                       # 旅游服务
                       # 路桥
                       # 林业
                       # 矿物制品
                       # 空运
                       # 酒店餐饮
                       # 焦炭加工
                       # 建筑工程
                       # 家用电器
                       # 家居用品
                       # 机械基件
                       # 机床制造
                       # 机场
                       # 火力发电
                       # 黄金
                       # 环境保护
                       # 化学制药
                       # 化纤
                       # 化工原料
                       # 化工机械
                       # 互联网
                       # 红黄酒
                       # 航空
                       # 广告包装
                       # 供气供热
                       # 公路
                       # 公共交通
                       # 工程机械
                       # 港口
                       # 钢加工
                       # 服饰
                       # 纺织机械
                       # 纺织
                       # 房产服务
                       # 多元金融
                       # 电信运营
                       # 电器仪表
                       # 电器连锁
                       # 电气设备
                       # 船舶
                       # 出版业
                       # 超市连锁
                       # 仓储物流
                       # 玻璃
                       # 保险
                       # 半导体
                       # 百货
                       # 白酒,
                       #    'IT设备'
                       ]

if __name__ == "__main__":
    excel_data_df = pd.read_excel(input_file, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['日期', '行业', '总市值'])
    dict = {}
    plt.title('行业市值走向')
    plt.xlabel('日期')
    plt.ylabel('市值')
    for index, row in df.iterrows():
        dt = row['日期']
        industry = row['行业']
        market_value = row['总市值']
        dict[industry] = dict.get(industry, [])+[(dt, market_value)]

    for key in dict.keys():
        if key in industries_to_check:
            draw_line(key, dict[key])
    plt.legend()

    plt.show()
