import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import datetime
import matplotlib.dates as mdates
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
# 解决中文显示问题
plt.rcParams['font.sans-serif'] = ['Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

image_path_base="/Users/xiefengchang/life/stock_images"

# Year = [1920, 1930, 1940, 1950, 1960, 1970, 1980, 1990, 2000, 2010]
# Unemployment_Rate = [9.8, 12, 8, 7.2, 6.9, 7, 6.5, 6.2, 5.5, 6.3]
# love_Rate = [9.1, 13, 5, 7, 6, 3, 6.2, 6, 5, 6.9]

# plt.plot(Year, Unemployment_Rate, label='un')
# plt.plot(Year, love_Rate, label='love')


input_file = "/Users/xiefengchang/life/industry_market_value_stats.xlsx"


def draw_line( key, list_of_tuple_in_order):
    fig, ax = plt.subplots()
    plt.title(key+'行业市值走向')
    plt.xlabel('日期')
    plt.ylabel('市值')
    list_of_tuple_in_order = sorted(list_of_tuple_in_order, key=lambda x: x[0])
    x, y = map(list, zip(*list_of_tuple_in_order))
    #以下两行很重要，设置x轴的刻度间隔和显示格式
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.MonthLocator())
    # plt.plot([datetime.datetime.strptime(str(dt), '%Y%m%d')
    #           for dt in x], y, '--', label=key)

    #绘图
    ax.plot([datetime.datetime.strptime(str(dt), '%Y%m%d') for dt in x],y,label=key)

    #y轴不要用科学计数法显示
    plt.gcf().axes[0].yaxis.get_major_formatter().set_scientific(False)

    #该行用于显示图表中线的名字
    plt.legend()
    #设置x轴label的旋转角度和尺寸
    plt.xticks(rotation=60,size=8)
    # 做实验时uncomment以下这行
    # plt.show()
    plt.tight_layout()
    print("保存 {0} 行业...".format(key))
    plt.savefig(image_path_base+'/'+key+'.png', dpi=300)
    plt.close(fig)

    


industries_to_check = [
    '白酒',
    '种植业',
    '医疗保健',
    '新型电力',
    '小金属',
    '塑料',
    '饲料',
    '水运',
    '食品',
    '乳制品',
    '啤酒',
    '旅游服务',
    '矿物制品',
    '家用电器',
    '火力发电',
    '化学制药',
    '化纤',
    '红黄酒',
    '航空',
    '工程机械',
    '电气设备',
    '玻璃',


    '综合类',
    '装修装饰',
    '专用机械',
    '中成药',
    '证券',
    '造纸',
    '元器件',
    '渔业',
    '文教休闲',
    '铜',
    '生物制药',
    '商品城',
    '商贸代理',
    '软饮料',
    '软件服务',
    '日用化工',
    '轻工机械',
    '铅锌',
    '汽车整车',
    '汽车配件',
    '其他建材',
    '普钢',
    '农用机械',
    '农药化肥',
    '摩托车',
    '煤炭开采',
    '铝',
    '旅游景点',
    '路桥',
    '林业',
    '焦炭加工',
    '家居用品',
    '机械基件',
    '机床制造',
    '黄金',
    '化工原料',
    '化工机械',
    '供气供热',
    '公路',
    '港口',
    '钢加工',
    '房产服务',
    '电器仪表',
    '仓储物流',
    '半导体',
    'IT设备'


    '运输设备',
    '园区开发',
    '影视音像',
    '银行',
    '医药商业',
    '橡胶',
    '通信设备',
    '铁路',
    '水务',
    '水泥',
    '水力发电',
    '石油贸易',
    '石油开采',
    '石油加工',
    '染料涂料',
    '全国地产',
    '区域地产',
    '汽车服务',
    '其他商业',
    '批发业',
    '农业综合',
    '空运',
    '酒店餐饮',
    '建筑工程',
    '机场',
    '环境保护',
    '互联网',
    '广告包装',
    '公共交通',
    '服饰',
    '纺织机械',
    '纺织',
    '多元金融',
    '电信运营',
    '电器连锁',
    '船舶',
    '出版业',
    '超市连锁',
    '保险',
    '百货',
    '特种钢',
    '陶瓷',


]

ind = industries_to_check[0]

if __name__ == "__main__":
    excel_data_df = pd.read_excel(input_file, sheet_name='Sheet1')
    df = pd.DataFrame(excel_data_df, columns=['日期', '行业', '总市值'])
    dict = {}

    for index, row in df.iterrows():
        dt = row['日期']
        industry = row['行业']
        if(industry not in industries_to_check):
            continue
        market_value = row['总市值']
        dict[industry] = dict.get(industry, [])+[(dt, market_value)]

    for key in dict.keys():
        if key in industries_to_check:
            draw_line(key, dict[key])
