# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-14 18:11
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pymongo import MongoClient
from pandas.io.json import json_normalize
from pylab import mpl
from pyecharts.charts import Bar, Map, WordCloud
from collections import Counter

plt.style.use('ggplot')
mpl.rcParams['font.sans-serif'] = ['SimHei']  # 解决seaborn中文字体显示问题
plt.rc('figure', figsize=(10, 10))  # 把plt默认的图片size调大一点
plt.rcParams['figure.dpi'] = mpl.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题


conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('DingXing')  # 连接到DingXiang数据库

erke = db.get_collection('erke')  # 儿科
mon_data = erke.find()  # 查询这个集合下的所有记录

erke_data = json_normalize([record for record in mon_data])


def get_data(department):
    col = db.get_collection(department)
    mon_data = col.find()
    return json_normalize([record for record in mon_data])


neike_data = get_data('neike')
waike_data = get_data('waike')
yanke_data = get_data('yanke')
fuchanke_data = get_data('fuchanke')

erke_data.iloc[754]


# 1.数据清理
# 1.1 由于丁香人才会推荐其它科室的工作，所以需要选出属于本科室的工作
all_data = pd.concat([erke_data, neike_data, waike_data, yanke_data, fuchanke_data], ignore_index=True)

erke_data = all_data[all_data['name'].str.contains('儿')]
neike_data = all_data[all_data['name'].str.contains('内')]
waike_data = all_data[all_data['name'].str.contains('外')]
yanke_data = all_data[all_data['name'].str.contains('眼')]
fuchanke_data = all_data[all_data['name'].str.contains('妇')]

erke_data['depType'] = '儿科'
neike_data['depType'] = '内科'
waike_data['depType'] = '外科'
yanke_data['depType'] = '眼科'
fuchanke_data['depType'] = '妇产科'

all_data = pd.concat([erke_data, neike_data, waike_data, yanke_data, fuchanke_data],
                    ignore_index=True)
all_data.to_csv('./data/all_data.csv', index=False)

# 1.2 把无用的字段删去
all_data.drop(columns=['_id', 'entLogo', 'region'], inplace=True)

# 1.3 根据id去重
all_data.drop_duplicates(subset='id', inplace=True)
all_data.shape

# 1.4 创建时间、更新时间 数据类型转换
all_data['createTime'] = pd.to_datetime(all_data['createTime'])
all_data['updateTime'] = pd.to_datetime(all_data['updateTime'])

# 1.5 由于儿科的数据是按照市为单位爬取的，而其它科是按省爬取的，所以area没有参考意义，需要清理出省
all_data['locationText'].unique()
all_data.loc[all_data['depType'] != '儿科', 'province'] = all_data.loc[all_data['depType'] != '儿科', 'area']
all_data.loc[(all_data['locationText'].str.contains('北京|上海|天津|重庆|自治区|省')) & (all_data['depType'] == '儿科'), 'province'] = \
    all_data.loc[(all_data['locationText'].str.contains('北京|上海|天津|重庆|自治区|省'))& (all_data['depType'] == '儿科'), 'locationText'].str.split('省|自治区|市', expand=True)[0]

all_data['city'] = all_data['locationText'].str.extract(r'(.{2}市')

# 1.6 工资字段很乱，需要定义一个函数处理
all_data['salaryText'].unique()

def process_k(data):
    if '千' in data:
        return float(data.replace('千', '')) * 1000
    elif '万' in data:
        return float(data.replace('万', '')) * 10000


def process_salary(data):
    if data == '面议':
        return np.nan
    if '万以上' in data:
        return float(data.replace('万以上', '')) * 10000
    if '千以下' in data:
        return float(data.replace('千以下', '')) * 1000
    if '-' in data:
        low, high = data.split('-')
        return (process_k(low) + process_k(high)) / 2


all_data['salary'] = all_data['salaryText'].apply(process_salary)

all_data = all_data[-(all_data['salary'] > 100000)]


'''问题'''
# 1.儿科医生的需求现状怎么样？
all_data[all_data['depType'] == '儿科'].shape[0]
# 招聘儿科医生的单位类型占比
type_pct = all_data.loc[all_data['dapType'] == '儿科', 'typeText'].value_counts() / all_data[all_data['depType'] == '儿科'].shape[0] * 100

bar = Bar("各类型单位招聘儿科岗位数百分比", width = 700,height=500)
bar.add("", type_pct.index, np.round(type_pct.values, 1), is_stack=True,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True,
       xaxis_rotate=20)

# 公立／民营医院儿科医生招聘经验要求百分比
np.round(all_data.loc[all_data['depType'] == '儿科', 'jobYearText'].value_counts() / all_data[all_data['depType'] == '儿科'].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院'), 'jobYearText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院')].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院'), 'jobYearText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院')].shape[0] * 100, 1)

exp = ['应届生', '1-3年', '3-5年', '5-10年', '10年以上', '经验不限']
exp1 = [1.6, 12.9, 14.4, 14.8, 6.4, 49.4]
exp2 = [2.5, 9.2, 7.7, 8.1, 3.7, 68]
exp3 = [0.5, 17.8, 22.3, 21.1, 9.7, 28.7]
bar = Bar("公立/民营医院儿科医生招聘工作经验要求百分比", width = 600,height=500)
bar.add("平均",exp, exp1, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("公立医院",exp, exp2, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("民营医院",exp, exp3, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)

# 公立／民营医院儿科医生招聘职称要求百分比
np.round(all_data.loc[all_data['depType'] == '儿科', 'positText'].value_counts() / all_data[all_data['depType'] == '儿科'].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院'), 'positText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院')].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院'), 'positText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院')].shape[0] * 100, 1)
level = ['初级', '中级', '副高', '高级', '不限']
level1 = [27.6, 17.2, 10.5, 2.5, 36.4]
level2 = [25, 8.1, 10.7, 3, 46.6]
level3 = [33.2, 26.3, 10.3, 1.9, 23.7]
bar = Bar("公立/民营医院儿科医生招聘职称要求百分比", width = 600,height=500)
bar.add("平均",level, level1, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("公立医院",level, level2, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("民营医院",level, level3, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)

# 公立／民营医院儿科医生招聘学历要求百分比
np.round(all_data.loc[all_data['depType'] == '儿科', 'gradeText'].value_counts() /
         all_data[all_data['depType'] == '儿科'].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院'), 'gradeText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '公立医院')].shape[0] * 100, 1)
np.round(all_data.loc[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院'), 'gradeText'].value_counts()
         / all_data[(all_data['depType'] == '儿科') & (all_data['typeText'] == '民营医院')].shape[0] * 100, 1)
grade = ['大专', '本科', '硕士', '博士', '学历不限']
grade1 = [15.7, 51.7, 21.6, 4.7, 6.2]
grade2 = [4.1, 49.1, 34, 8.1, 4.7]
grade3 = [30, 54.7, 6.1, 0.6, 8.5]
bar = Bar("公立/民营医院儿科医生招聘学历要求百分比", width = 600,height=500)
bar.add("平均",grade, grade1, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("公立医院",grade, grade2, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)
bar.add("民营医院",grade, grade3, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)

# 不同科室招聘持续时间
all_data['time_delta'] = pd.to_timedelta(all_data['updateTime'] - all_data['createTime'])
all_data.loc[all_data['depType'] == '儿科', 'time_delta'].mean()
all_data.loc[all_data['depType'] == '妇产科', 'time_delta'].mean()
all_data.loc[all_data['depType'] == '眼科', 'time_delta'].mean()
all_data.loc[all_data['depType'] == '内科', 'time_delta'].mean()
all_data.loc[all_data['depType'] == '外科', 'time_delta'].mean()
bar = Bar("各科室招聘平均已持续时间", width = 500,height=400)
bar.add("", ['儿科', '妇产科', '眼科', '内科', '外科'],
        [73, 68, 67, 62, 50], is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14,
        is_label_show=True, legend_top=30, xaxis_rotate=20)

# 2.2 儿科的工资待遇怎么样
mean_salary = all_data.groupby('depType')['salary'].mean().sort_values()
bar = Bar("儿科平均工资与其它科室对比", width = 600,height=400)
bar.add("", mean_salary.index, np.round(mean_salary.values, 0), is_stack=True,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, )
mean_salary_1 = all_data[all_data['typeText'] == '公立医院'].groupby(['typeText', 'depType'])['salary'].mean()
mean_salary_2 = all_data[all_data['typeText'] == '民营医院'].groupby(['typeText', 'depType'])['salary'].mean()
bar = Bar("公立/民营医院各科室平均工资", width = 600,height=600)
bar.add("公立医院",['儿科', '内科', '外科', '妇产科', '眼科'], np.round(mean_salary_1.values, 0), is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)
bar.add("民营医院", ['儿科', '内科', '外科', '妇产科', '眼科'], np.round(mean_salary_2.values, 0), is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)

fig, ax = plt.subplots(figsize=(12, 6))
sns.violinplot(x='salary', y='typeText',
               data=all_data[(all_data['typeText'].isin(['公立医院', '民营医院'])) & (all_data['depType'] == '儿科')], ax=ax)

all_data[all_data['depType'] == '儿科'].groupby('typeText')['salary'].count()

# 各类型单位儿科平均工资
erke_salary = all_data[all_data['depType'] == '儿科'].groupby('typeText')['salary'].mean().drop(index='科研院校').sort_values()
bar = Bar("各类型单位儿科平均工资", width = 600,height=500)
bar.add("",erke_salary.index, np.round(erke_salary.values, 0), is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, xaxis_rotate=20)

# 2.3 相同工资水平下，公立与民营对医生的学历，职称等要求如何？
all_data[(all_data['depType'] == '儿科') & (all_data['salary'] > 8000) & (all_data['salary'] < 10000) &
         (all_data['typeText'].isin(['公立医院', '民营医院']))].groupby(['typeText', 'gradeText'])['id'].counts()
grade_same1 = np.round(np.array([3, 31, 12, 1, 0]) / (3+31+12+1)*100, 1)
grade_same2 = np.round(np.array([18, 21, 2, 0, 8]) / (18+21+2+8)*100, 1)
bar = Bar("相同工资水平下公立/民营医院对学历的要求百分比(8k-10k)", width = 600,height=600)
bar.add("公立医院",grade, grade_same1, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)
bar.add("民营医院", grade, grade_same2, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)

all_data[(all_data['depType'] == '儿科') & (all_data['salary'] > 8000) & (all_data['salary'] < 10000) &
         (all_data['typeText'].isin(['公立医院', '民营医院']))].groupby(['typeText', 'positText'])['id'].count()
level_same1 = np.round(np.array([15, 5, 2, 2, 23]) / (15+5+2+2+23)*100, 1)
level_same2 = np.round(np.array([24, 6, 2, 0, 17]) / (24+6+2+17)*100, 1)
bar = Bar("相同工资水平下公立/民营医院对职称的要求百分比(8k-10k)", width = 600,height=600)
bar.add("公立医院",level, level_same1, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)
bar.add("民营医院", level, level_same2, is_stack=False,
       xaxis_label_textsize=20, yaxis_label_textsize=14, is_label_show=True, legend_top=30)


# 2.4 全国各区域对于儿科医生的需求
# 对于province的处理结果还不是很满意，再处理以下
def get_province(data):
    province = ['北京', '天津', '河北', '山西', '内蒙古', '辽宁', '吉林', '黑龙江', '上海', '江苏',
            '浙江', '安徽', '福建', '江西', '山东', '河南', '湖北', '湖南', '广东', '广西',
            '海南', '重庆', '四川', '贵州', '云南', '西藏', '陕西', '甘肃', '青海', '宁夏',
            '新疆', '台湾', '香港', '澳门', '国外']
    for i in province:
        if i in data:
            return i


all_data.loc[all_data['depType'] == '儿科', 'province2'] = all_data.loc[all_data['depType'] == '儿科', 'locationText'].apply(get_province)
demand = all_data.loc[all_data['depType'] == '儿科', 'province2'].value_counts()

province = list(demand.index)
value = list(demand.values)
province.extend(['内蒙古', '山西', '青海'])
value.extend([1, 1, 1])


# 儿科医生全国各区域需求量
map = Map('儿科医生全国各区域需求量', width=600, height=600)
map.add(
    '',
    province,
    value,
    maptype='china',
    is_visualmap=True,
    visual_text_color='#000'
)


# 2.5 儿科医生的要求和福利
all_data.iloc[888]
grade = all_data.loc[all_data['depType'] == '儿科', 'gradeText'].value_counts()
year = all_data.loc[all_data['depType'] == '儿科', 'jobYearText'].value_counts()
level = all_data.loc[all_data['depType'] == '儿科', 'levelText'].value_counts()
name = all_data.loc[all_data['depType'] == '儿科', 'name'].value_counts()
positText = all_data.loc[all_data['depType'] == '儿科', 'positText'].value_counts()
type = all_data.loc[all_data['depType'] == '儿科', 'typeText'].value_counts()

welfare = []
for i in all_data.loc[all_data['depType'] == '儿科', 'welfare']:
    if len(i) > 0:
        welfare.extend(i)

w = pd.Series(Counter(welfare))
all = pd.concat([grade, year, level, name, positText, type, welfare])
name, value = all.index, all.values
word_cloud = WordCloud(width=800, height=800)
word_cloud.add('', name, value, word_size_range=[20, 80])

















































