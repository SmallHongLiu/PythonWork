# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-12 14:48
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pyecharts.charts import Line, Bar, Geo

data = pd.read_csv('./data/aqi_data.csv')
data.head()

# 数据清洗
data['time'] = pd.to_datetime(data['time'])
data = data[data['time'] <= pd.to_datetime('2019-02-11 23:59:59')]  # 选取2月4日－2月12日的数据
data.set_index(data['time'], inplace=True)
data = data.replace('-', np.nan)

for col in ['AQI', 'PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']:
    data[col] = data[col].astype(float)
data.head()

len(data['city'].unique())

data.to_csv('data_clean.csv', index=False)


'''问题'''
# 1.燃放烟花爆竹真的对空气质量有影响吗？
AQI_total_mean = data[data['time'] <= pd.to_datetime('2019-02-06 23:59:59')].groupby(['time'])['AQI'].mean()
line = Line("全国春节期间空气质量指数总体趋势", "2019年除夕到初二", width=800)
line.add("", AQI_total_mean.index, np.round(AQI_total_mean.values,0), is_smooth=True,
         legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
         xaxis_rotate=20, yaxis_min=8, mark_point=["max"])


def city_AQI(data, cities):
    line = Line("春节期间空气质量指数", "2019年除夕到初二", width=800)
    for city in cities:
        city_aqi = data[(data['city'] == city) & (data['time'] <= pd.to_datetime('2019-02-06 23:59:59'))]
        line.add(city, city_aqi.index, np.round(city_aqi['AQI'].values, 0), is_smooth=True,
                 legend_text_size=18, xaxis_label_textsize=14, yaxis_label_textsize=18,
                 xaxis_rotate=20, yaxis_min=8, mark_point=["max"])
    return line


city_AQI(data=data, cities=['北京市', '天津市'])
city_AQI(data=data, cities=['长沙市', '南宁市'])

# 2.烟花爆竹对空气质量的影响体现在哪些指标上
data_total_idx = data[data['time'] <= pd.to_datetime('2019-02-06 23:59:59')].groupby(['time']).mean()
data_total_idx.columns
line = Line("全国春节期间空气质量各指标（2019年除夕到初二）", "单位:μg/m3(CO为mg/m3)", width=800)
for idx in data_total_idx.columns[1:]:
    line.add(idx, data_total_idx.index, np.round(data_total_idx[idx].values,0), is_smooth=True,
             legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
             xaxis_rotate=20, yaxis_min=8, legend_top=30)

tianjin_idx = data[(data['city'] == '石家庄市') & (data['time'] <= pd.to_datetime('2019-02-06 23:59:59'))]
line = Line("石家庄市春节期间空气质量各指标（2019年除夕到初二）", "单位:μg/m3(CO为mg/m3)", width=800)
for idx in tianjin_idx.columns[2:8]:
    line.add(idx, tianjin_idx.index, np.round(tianjin_idx[idx].values,0), is_smooth=True,
             legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
             xaxis_rotate=20, yaxis_min=8, legend_top=30)


main_pol = data.loc[data['time'] == pd.to_datetime('2019-02-05 02:00:00'), 'main_pollution'].value_counts()
bar = Bar("全国城市首要污染物", "2019年2月5日凌晨2点", width=600)
bar.add("", main_pol.index, main_pol.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'], label_text_size=18,
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)


# 3. 烟花爆竹对空气质量的污染程序有多大？
data2 = data[data['time'] <= pd.to_datetime('2019-02-05 23:59:59')]
data_AQI_min = data2.groupby('city')['AQI'].min()
data_AQI_max = data2.groupby('city')['AQI'].max()
data_AQI_times = np.round(data_AQI_max / data_AQI_min, 1)  # 四舍五入，保留一位小数
data_AQI_times_top10 = data_AQI_times.nlargest(10)
bar = Bar("全国除夕和春节期间空气质量最高最低比Top10城市", "时间：2019年除夕至初一", width=600)
bar.add("", data_AQI_times_top10.index, data_AQI_times_top10.values, is_stack=True,
        is_label_show=True,bar_category_gap='40%', label_color = ['#130f40'], label_text_size=18,
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18, xaxis_rotate=30)

city_AQI(data=data, cities=['伊春市','鸡西市', '大兴安岭地区'])
city_AQI(data=data, cities=['盘锦市','葫芦岛市','瓦房店市','锦州市'])

data_AQI_times_counts = data_AQI_times.value_counts(bins=[1,5,10,15,20,25])
bar = Bar("全国除夕和春节期间空气质量最高最低比的城市数量", "时间：2019年除夕至初一", width=600)
times = ['1-5倍','5-10倍','10-15倍','15-20倍','20-25倍']
bar.add("", times, data_AQI_times_counts.values, is_stack=True,
        is_label_show=True,bar_category_gap='40%', label_color = ['#130f40'], label_text_size=18,
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

# 4. 哪些区域污染最严重（轻）？
start_time = pd.to_datetime('2019-02-04 20:00:00')
end_time = pd.to_datetime('2019-02-05 04:00:00')
AQI_by_city = data[(data['time'] >= start_time) & (data['time'] <= end_time)].groupby('city')['AQI'].mean()


geo = Geo(
    "全国各城市空气质量指数",
    "除夕晚上20点至初一凌晨4点平均值",
    title_color="#fff",
    title_pos="center",
    width=800,
    height=500,
    background_color="#404a59",
)
attr, value = AQI_by_city.index, AQI_by_city.values
geo.add(
    '',
    attr,
    value,
    visual_range=[0, 500],
    visual_text_color='#fff',
    symbol_size=10,
    is_visualmap=True,
    is_piecewise=True,
    visual_split_number=10,
)

AQI_by_city.nlargest(10)

city_AQI(data=data, cities=['呼和浩特市', '包头市', '咸阳市'])
AQI_by_city.nsmallest(5)
AQI_by_city[AQI_by_city <= 50]

# 5.哪些城市属于一秒破功型
city1 = data.loc[(data['time'] == pd.to_datetime('2019-02-05 02:00:00')) & (data['AQI'] < 100), 'city']
data3 = data[(data['time'] >= pd.to_datetime('2019-02-05 18:00:00')) & (data['time'] <= pd.to_datetime('2019-02-06 23:59:59'))]
city2 = data3.loc[data3['AQI'] > 200, 'city']
list(set(city1).intersection(set(city2)))  # 求city1和city2的交集
city_AQI(data=data, cities=['郑州市', '长春市', '忻州市', '晋城市'])

# 6.除夕中午到初一中午的超标城市个数
start_time = pd.to_datetime('2019-02-04 12:00:00')
end_time = pd.to_datetime('2019-02-05 12:00:00')
city_over_new_year = data.loc[(data['time'] >= start_time) & (data['time'] <= end_time) &
                              (data['AQI'] > 100)].groupby('time')['AQI'].count()
bar = Bar("全国除夕中午至初一中午空气质量超标城市数量", "时间: 2019年  总城市数: 367", width=1000)
new_year_time = ['除夕12点','除夕13点','除夕14点','除夕15点','除夕16点','除夕17点','除夕18点','除夕19点',
        '除夕20点','除夕21点','除夕22点','除夕23点','春节0点','春节1点','春节2点','春节3点',
        '春节4点','春节5点','春节6点','春节7点','春节8点','春节9点','春节10点','春节11点','春节12点']
bar.add("", new_year_time, city_over_new_year.values, is_stack=True,
        is_label_show=True,bar_category_gap='40%', label_color = ['#130f40'], label_text_size=18,
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18, xaxis_rotate=90)

line = Line("", width=1000)
line.add("", new_year_time, city_over_new_year.values+5, is_smooth=True)
bar.overlap(line)

# 7.除夕到初七的超标城市个数
city_over_count = (data.groupby('city')['AQI'].resample('D').mean() > 100).unstack(level=-1).sum()
bar = Bar("全国除夕至初七期间空气质量超标城市数量", "时间: 2019年  总城市数: 367", width=800)
date = ['02-04(除夕)','02-05(初一)','02-06(初二)','02-07(初三)',
        '02-08(初四)','02-09(初五)','02-10(初六)','02-11(初七)']
bar.add("", date, city_over_count.values, is_stack=True,
        is_label_show=True,bar_category_gap='40%', label_color = ['#130f40'], label_text_size=18,
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18, xaxis_rotate=20)

line = Line("", width=800)
line.add("", date, city_over_count.values+5, is_smooth=True)
bar.overlap(line)




