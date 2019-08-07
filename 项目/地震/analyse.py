# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-07 14:27
'''

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pyecharts.charts import Bar

earth_quake_20 = pd.read_csv('./data/1999-2019.csv')
earth_quake_1 = pd.read_csv('./data/earthquake.csv')
earth_sichuan = pd.read_csv('./data/sichuan.csv')

# print(earth_quake_20.sample(5))
# print(earth_quake_20.columns)


# 选取需要的字段
cols = ['time', 'latitude', 'longitude', 'depth', 'mag',
        'magType', 'id', 'place', 'type', 'status']
earth_quake_20 = earth_quake_20[cols]
earth_quake_1 = earth_quake_1[cols]
earth_sichuan = earth_sichuan[cols]

# 数据类型转换
earth_quake_20['time'] = pd.to_datetime(earth_quake_20['time'])
earth_quake_1['time'] = pd.to_datetime(earth_quake_1['time'])
earth_sichuan['time'] = pd.to_datetime(earth_sichuan['time'])


# 问题1：最近地震越来越频繁了吗？还是报道的比较多而已？
# print(earth_quake_20.sample(5))  # 随机取5个数据

earth_quake_20.index = earth_quake_20['time']
earth_quake_20['year'] = earth_quake_20['time'].dt.year
earth_quake_20['time'].describe()

# 选取2000年1月1日到2019年6月24日的数据
earth_quake_20 = earth_quake_20[earth_quake_20['time'] > pd.to_datetime('2000-01-01 00:00:00')]
earth_quake_20['mag'].plot()

# 选取近20年地震发生的次数（以年为单位）
earth_quake_by_years = earth_quake_20['id'].groupby(earth_quake_20['year']).count()
earth_quake_by_years[:-1].mean()  # 求取均值

# 选取近20年7级以上的地震发生的次数（以年为单位）
earth_quake_7_years = earth_quake_20[earth_quake_20['mag'] > 7].groupby('year')['id'].count()
earth_quake_7_years[:-1].mean()

earth_quake_by_month = earth_quake_20['id'].resample('M').count().reset_index()
earth_quake_by_month['year'] = earth_quake_by_month['time'].dt.year
earth_quake_by_month.tail(6) # 返回后6条数据

from pyecharts.charts import Bar
from pyecharts import options as opts


# 绘制近20年全球4.5级以上地震发生次数
def bar(x_values, y_values, title, subtitle, y_line) -> Bar:
    c = (
        Bar()
        .add_xaxis(x_values)
        .add_yaxis('', y_values, category_gap='40%', stack=True)
        .set_global_opts(title_opts=opts.TitleOpts(title=title,
                                                  subtitle=subtitle))
        .set_series_opts(
            markline_opts=opts.MarkLineOpts(
                data=[opts.MarkLineItem(y=y_line, name=f'yAxis={y_line}')]
            ),
        )
    )
    return c


from pyecharts.charts import Line
month_name = ['1月', '2月', '3月', '4月', '5月', '6月', '7月', '8月', '9月', '10月', '11月', '12月']

def line() -> Line:
    line = (
        Line()
        .add_xaxis(month_name)
        .add_yaxis('2015', earth_quake_by_month[earth_quake_by_month['year'] == 2015]['id'].tolist(), is_smooth=True)
        .add_yaxis('2016', earth_quake_by_month[earth_quake_by_month['year'] == 2016]['id'].tolist())
        .add_yaxis('2017', earth_quake_by_month[earth_quake_by_month['year'] == 2017]['id'].tolist())
        .add_yaxis('2018', earth_quake_by_month[earth_quake_by_month['year'] == 2018]['id'].tolist())
        .add_yaxis('2019', [654, 560, 617, 636, 521, 359, None, None, None, None, None, None])
        .set_global_opts(title_opts=opts.TitleOpts(title='近5年全球每月4.5级以上地震次数'),
                         legend_opts=opts.LegendOpts(pos_top=30))
    )
    return line


# 问题2：引发地震的因素有哪些？
from pyecharts.charts import Sankey
nodes = [
    {'name': '构造地震'}, {'name': '天然地震'}, {'name': '火山喷发'},
    {'name': '火山地震'}, {'name': '冰震'}, {'name': '塌陷地震'},
    {'name': '矿井塌陷'}, {'name': '岩爆'}, {'name': '采石场爆破'},
    {'name': '爆炸'}, {'name': '煤矿爆炸'}, {'name': '化学爆炸'},
    {'name': '人工地震'}, {'name': '水库地震'}, {'name': '油田注水'},
    {'name': '诱发地震'}
]

links = [
    {'source': '构造地震', 'target': '天然地震', 'value': 5000},  #为了图形显示，这里重置了构造地震真实值
    {'source': '火山喷发', 'target': '火山地震', 'value': 28},
    {'source': '火山地震', 'target': '天然地震', 'value': 28},
    {'source': '冰震', 'target': '塌陷地震', 'value': 776},
    {'source': '矿井塌陷', 'target': '塌陷地震', 'value': 2},
    {'source': '岩爆', 'target': '塌陷地震', 'value': 2},
    {'source': '塌陷地震', 'target': '天然地震', 'value': 780},
    {'source': '采石场爆破', 'target': '人工地震', 'value': 1173},
    {'source': '爆炸', 'target': '人工地震', 'value': 1023},
    {'source': '煤矿爆炸', 'target': '人工地震', 'value': 214},
    {'source': '化学爆炸', 'target': '人工地震', 'value': 15},
    {'source': '水库地震', 'target': '诱发地震', 'value': 50},
    {'source': '油田注水', 'target': '诱发地震', 'value': 50},
]
def sankey() -> Sankey:
    sankey = (
        Sankey()
        .add(
            '',
            nodes,
            links,
            linestyle_opt=opts.LineStyleOpts(opacity=0.2, curve=0.5, color='source'),
            label_opts=opts.LabelOpts(position='right')
        )
        .set_global_opts(title_opts=opts.TitleOpts(title='近一年全球所有地震的地震类型',
                                                   subtitle='时间: 2018年6月25日至2019年6月24日'))
    )
    return sankey

# 问题3：全世界地震频发的地区有哪些？
# 近20年全球4.5级以上地震次数最多的国家/地区
r = ['印尼', '日本', '新几内亚', '智利', '菲律宾', '汤加', '瓦努阿图', '新西兰', '所罗门群岛', '阿拉斯加州']
num = [15661, 9646+2522, 7827, 5249, 4379, 4167, 3489, 2982, 2958, 2700]

# 问题4：近20年有哪些引发全世界舆情关注的大地震




if __name__ == '__main__':
    """
    bar(earth_quake_by_years.index.tolist(), earth_quake_by_years.values.tolist(),
        '近20年全球4.5级以上地震发生次数', '时间: 2000年1月1日-2019年6月24日',
        6764).render('近20年全球4.5级以上地震发生次数.html')

    bar(earth_quake_7_years.index.tolist(), earth_quake_7_years.values.tolist(),
        '近20年全球7级以上地震发生次数', '时间: 2000年1月1日-2019年6月24日',
        12.8).render('近20年全球7级以上地震发生次数.html')
        
    """

    # line().render('近5年全球每月4.5级以上地震次数.html')

    # sankey().render('近一年全球所有地震的地震类型.html')

    bar(r, num, '近20年全球4.5级以上地震次数最多的国家/地区', '', 2).render('近20年全球4.5级以上地震次数最多的国家.html')







