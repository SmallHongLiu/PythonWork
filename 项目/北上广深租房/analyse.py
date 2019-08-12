# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-10 16:21
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from pandas.io.json import json_normalize

plt.style.use('ggplot')
from pylab import mpl
mpl.rcParams['font.sans-serif'] = ['SimHei']  #解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))  #把plt默认的图片size调大一点
plt.rcParams["figure.dpi"] =mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('Lianjia')  # 连接到Lianjia数据库

zufang = db.get_collection('zufang') # 连接到集合zufang
mon_data = zufang.find()  # 查询这个集合下的所有记录

data = json_normalize([comment for comment in mon_data])
data.head()

# 每个城市各采样3000条数据，保存为csv文件
data_sample = pd.concat(data[data['city'] == city].sample(3000) for city in ['北京', '上海', '广州', '深圳'])
data_sample.to_csv('data_sample.csv', index=False)


# 数据清洗(按列清理)
# 1. 去掉“_id”列
data = data.drop(columns='_id')
# 2. bathroom_num
data['bathroom_num'].unique()
data[data['bathroom_num'].isin(['8', '9', '11'])]
# 除了55273行是异常数据外，其它数据都正常
data = data.drop([55273])

# 4. distance
data['frame_orientation'].unique()  # 这个数据太乱了，要用的时候再处理吧

# 5. hall_num
data['hall_num'].unique()

data[data['hall_num'].isin(['6', '11'])]

# 59223行是异常数据，删去
data = data.drop([59223])

# 6. rent_area
data.sample(5)['rent_area']


# rent_area字段有些填写的是一个范围，比如23-25平房米，后期转换成“float”类型的时候不好转换，考虑取平均值
def get_aver(data):
    if isinstance(data, str) and '-' in data:
        low, high = data.split('-')
        return (int(low)+int(high))/2
    else:
        return int(data)


data['rent_area'] = data['rent_area'].apply(get_aver)

data[data['rent_area'] < 5]

# 房间只有1平方米，是异常数据，删除
data = data.drop(data[data['rent_area'] < 5].index)
# 7.rent_price_unit
data['rent_price_unit'].unique()

# 租金都是以“元/月”计算的，所以这一列没用了，可以删了
data = data.drop(columns='rent_price_unit')

# 8.rent_price_listing
data[data['rent_price_listing'].str.contains('-')].sample(3)

# 价格是有区间的，需要按照处理rent_area一样的方法处理
data['rent_price_listing'] = data['rent_price_listing'].apply(get_aver)

# 数据类型转换
for col in ['bathroom_num', 'bedroom_num', 'hall_num', 'rent_price_listing']:
    data[col] = data[col].astype(int)


# 'distance', 'latitude', 'longitude'因为有None，需另外处理
def dw_None_dis(data):
    if data is None:
        return np.nan
    else:
        return int(data)


def dw_None_latlon(data):
    if data is None or data == '':
        return np.nan
    else:
        return float(data)


data['distance'] = data['distance'].apply(dw_None_dis)
data['latitude'] = data['latitude'].apply(dw_None_latlon)
data['longitude'] = data['longitude'].apply(dw_None_latlon)

# 查看数据概况
data.sample(5)

data.to_csv('data_clean.csv', index=False)


# 1. 各城市的租房分析怎么样

def get_city_zf_loc(city, city_short, col=['longitude', 'latitude', 'dist'], data=data):
    file_name = 'data_' + city_short + '_latlon.csv'
    data_latlon = data.loc[data['city'] == city, col].dropna(subset=['latitude', 'longitude'])
    data_latlon['longitude'] = data_latlon['longitude'].astype(str)
    data_latlon['latitude'] = data_latlon['latitude'].astype(str)
    data_latlon['latlon'] = data_latlon['longitude'].str.cat(data_latlon['latitude'], sep=',')
    data_latlon.to_csv(file_name, index=False)
    print(city + '的数据一共有{}条'.format(data_latlon.shape[0]))


get_city_zf_loc('北京', 'bj', ['longitude','latitude', 'dist'])
get_city_zf_loc('上海', 'sh', ['longitude','latitude', 'dist'])
get_city_zf_loc('广州', 'gz', ['longitude','latitude', 'dist'])
get_city_zf_loc('深圳', 'sz', ['longitude','latitude', 'dist'])

fig = plt.figure(dpi=300)
data.dropna(subset=['latitude', 'longitude'])[data['city'] == '北京']['dist'].value_counts(ascending=True).plot.barh()

fig = plt.figure(dpi=300)
data.dropna(subset=['latitude', 'longitude'])[data['city'] == '广州']['dist'].value_counts(ascending=True).plot.barh()

fig = plt.figure(dpi=300)
data.dropna(subset=['latitude', 'longitude'])[data['city'] == '深圳']['dist'].value_counts(ascending=True).plot.barh()

# 2. 城市各区域的房价分布怎么样
data['aver_price'] = np.round(data['rent_price_listing'] / data['rent_area'], 1)
g = sns.FacetGrid(data, row='city', height=4, aspect=2)
g = g.map(sns.kdeplot, 'aver_price')


# 由于平均租金基本上都集中在250元/平米/月以内，所以选取这部分数据绘制热力图
def get_city_zf_aver_price(city, city_short, col=['longitude', 'latitude', 'aver_price'], data=data):
    file_name = 'data_' + city_short + '_aver_price.csv'
    data_latlon = data.loc[(data['city']==city)&(data['aver_price']<=250), col].dropna(subset=['latitude', 'longitude'])
    data_latlon['longitude'] = data_latlon['longitude'].astype(str)
    data_latlon['latitude'] = data_latlon['latitude'].astype(str)
    data_latlon['latlon'] = data_latlon['longitude'].str.cat(data_latlon['latitude'], sep=',')
    data_latlon.to_csv(file_name, index=False)
    print(city+'的数据一共有{}条'.format(data_latlon.shape[0]))


get_city_zf_aver_price('北京', 'bj')
get_city_zf_aver_price('上海', 'sh')
get_city_zf_aver_price('广州', 'gz')
get_city_zf_aver_price('深圳', 'sz')

# 各城市租金Top10的商圈
bc_top10 = data.groupby(['city', 'bizcircle_name'])['aver_price'].mean().nlargest(50).reset_index()['city'].value_counts()

from pyecharts.charts import Bar

bar = Bar("每平米平均租金前50的北上广深商圈数量", width=400)
bar.add("", bc_top10.index, bc_top10.values, is_stack=True,
       xaxis_label_textsize=16, yaxis_label_textsize=16, is_label_show=True)


def get_top10_bc(city, data=data):
    top10_bc = data[(data['city']==city)&(data['bizcircle_name']!='')].groupby('bizcircle_name')['aver_price'].mean().nlargest(10)
    bar = Bar(city+"市每平米平均租金Top10的商圈", width=600)
    bar.add("", top10_bc.index, np.round(top10_bc.values, 0), is_stack=True,
       xaxis_label_textsize=16, yaxis_label_textsize=16, xaxis_rotate=30, is_label_show=True)
    return bar


# 北京每平米平均租金Top10的商圈
get_top10_bc('北京')
get_top10_bc('上海')
get_top10_bc('广州')
get_top10_bc('深圳')


# 3.距离地铁口远近有什么关系
from scipy import stats

def distance_price_relation(city, data=data):
    g = sns.jointplot(x='distance', y='aver_price', data=data[(data['city']==city)&
                            (data['aver_price']<=350)].dropna(subset=['distance']),
                      kind='reg',
                      stat_func=stats.pearsonr)
    g.fig.set_dpi(100)
    g.ax_joint.set_xlabel('最近地铁距离', fontweight='bold')
    g.ax_joint.set_ylabel('每平米租金', fontweight='bold')
    return g


distance_price_relation('北京')
distance_price_relation('上海')
distance_price_relation('广州')
distance_price_relation('深圳')

bins = [100 * i for i in range(13)]
data['bin'] = pd.cut(data.dropna(subset=['distance'])['distance'], bins)
bin_bj = data[data['city']=='北京'].groupby('bin')['aver_price'].mean()
bin_sh = data[data['city']=='上海'].groupby('bin')['aver_price'].mean()
bin_gz = data[data['city']=='广州'].groupby('bin')['aver_price'].mean()
bin_sz = data[data['city']=='深圳'].groupby('bin')['aver_price'].mean()


from pyecharts.charts import Line
line = Line('距离地铁远近跟每平米租金均价的关系')
for city, bin_data in {'北京':bin_bj, '上海':bin_sh, '广州':bin_gz, '深圳':bin_sz}.items():
    line.add(city, bin_data.index, bin_data.values,
             legend_text_size=18, xaxis_label_textsize=14, yaxis_label_textsize=18,
             xaxis_rotate=20, yaxis_min=8, legend_top=30)


# 4.房屋大小对每平米租金的影响如何？
def area_price_relation(city, data=data):
    fig = plt.figure(dpi=100)
    g = sns.lineplot(x='rent_area',
                     y='aver_price',
                     data=data[(data['city']==city)&(data['rent_area']<150)],
                     ci=None)
    g.set_xlabel('面积', fontweight='bold')
    g.set_ylabel('每平米均价', fontweight='bold')
    return g


area_price_relation('北京')
area_price_relation('上海')
area_price_relation('广州')
area_price_relation('深圳')


# 根据house_title和house_tag再造一个字段：is_dep，也就是“是否是公寓”
data['is_dep'] = (data['house_title'].str.contains('公寓') + data['house_tag'].str.contains('公寓')) > 0

# 每个城市房源的公寓占比
for city in ['北京', '上海', '广州', '深圳']:
    print(city+'的公寓占总房源量比重为:{}%。'.format(
        np.round(data[data['city'] == city]['is_dep'].mean()*100, 2)))


data[(data['city'] == '广州') & (data['rent_area'] > 0) & (data['rent_area'] < 60)
     & (data['aver_price'] > 100)]['is_dep'].mean()


# 5. 租个人房源好还是公寓好？
is_dep = data[(data['city'].isin(['广州', '深圳'])) &
              (data['is_dep'] == 1)].groupby('city')['aver_price'].mean()
not_dep = data[(data['city'].isin(['广州', '深圳'])) &
               (data['is_dep'] == 0)].groupby('city')['aver_price'].mean()
bar = Bar("个人房源和公寓的每平米租金差别", width=600)
bar.add("个人房源", not_dep.index, np.round(not_dep.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("公寓", is_dep.index, np.round(is_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)

# 6. 精装和简装对房子价格的影响
data['decorated'] = data[data['house_tag'].notna()]['house_tag'].str.contains('精装')
decorated = data[data['decorated'] == 1].groupby('city')['aver_price'].mean()
not_decorated = data[data['decorated'] == 0].groupby('city')['aver_price'].mean()

bar = Bar("各城市精装和简装的每平米租金差别", width=600)
bar.add("精装(刷过墙)", decorated.index, np.round(decorated.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("简装(破房子)", not_decorated.index, np.round(not_decorated.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)

is_dec_dep = data[(data['decorated'] == 1) &
                  (data['is_dep'] == 1) &
                  (data['city'].isin(['广州', '深圳']))].groupby('city')['aver_price'].mean()
is_dec_not_dep = data[(data['decorated'] == 1) &
                      (data['is_dep'] == 0) &
                      (data['city'].isin(['广州', '深圳']))].groupby('city')['aver_price'].mean()
not_dec_dep = data[(data['decorated'] == 0) &
                   (data['is_dep'] == 0) &
                   (data['city'].isin(['广州', '深圳']))].groupby('city')['aver_price'].mean()
bar = Bar("各城市装修和房源类型的每平米租金差别", width=600)
bar.add("精装公寓", is_dec_dep.index, np.round(is_dec_dep.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("精装个人房源", is_dec_not_dep.index, np.round(is_dec_not_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
bar.add("简装个人房源", not_dec_dep.index, np.round(not_dec_dep.values, 0),
       legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)

# 7.北方集中供暖对价格的影响
data['ct_heating'] = data['house_tag'].str.contains('集中供暖')
data[data['city'] == '北京'].groupby('ct_heating')['aver_price'].mean()

# 8.各城市房屋租售比
zs_ratio = [57036, 62779, 32039, 56758] / (data.groupby('city')['rent_price_listing'].sum() /
                                           data.groupby('city')['rent_area'].sum()) / 12
bar = Bar("各城市房屋租售比(租多少年可以在该城市买下一套房)", width=450)
bar.add("", zs_ratio.index, np.round(zs_ratio.values, 0),
        legend_text_size=18,xaxis_label_textsize=14,yaxis_label_textsize=18,
        xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)


# 9.北上广深租房时都看重什么？
def layout_top3(city, data):
    layout_data = data[data['city'] == city]['layout'].value_counts().nlargest(3)
    bar = Bar(city + "最受欢迎的户型", width=600)
    bar.add("", layout_data.index, layout_data.values,
            legend_text_size=18, xaxis_label_textsize=14, yaxis_label_textsize=18,
            xaxis_rotate=20, yaxis_min=8, legend_top=30, is_label_show=True)
    return bar


layout_top3('北京', data)
layout_top3('上海', data)
layout_top3('广州', data)
layout_top3('深圳', data)

from pyecharts.charts import WordCloud
from collections import Counter
bj_tag = []
for st in data[data['city'] == '北京'].dropna(subset=['house_tag'])['house_tag']:
    bj_tag.extend(st.split(' '))
name, value = WordCloud.cast(Counter(bj_tag))
word_cloud = WordCloud(width=500, height=500)
word_cloud.add("", name, value, word_size_range=[20, 100])


sh_tag = []
for st in data[data['city'] == '上海'].dropna(subset=['house_tag'])['house_tag']:
    sh_tag.extend(st.split(' '))
name, value = WordCloud.cast(Counter(sh_tag))
word_cloud = WordCloud(width=500, height=500)
word_cloud.add("", name, value, word_size_range=[20, 100])


gz_tag = []
for st in data[data['city'] == '广州'].dropna(subset=['house_tag'])['house_tag']:
    gz_tag.extend(st.split(' '))
name, value = WordCloud.cast(Counter(gz_tag))
word_cloud = WordCloud(width=500, height=500)
word_cloud.add("", name, value, word_size_range=[20, 100])


sz_tag = []
for st in data[data['city'] == '深圳'].dropna(subset=['house_tag'])['house_tag']:
    sz_tag.extend(st.split(' '))

name, value = WordCloud.cast(Counter(sz_tag))
word_cloud = WordCloud(width=500, height=500)
word_cloud.add("", name, value, word_size_range=[20, 100])





