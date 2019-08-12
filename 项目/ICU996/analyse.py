# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-08 18:14
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
plt.reParams['figure.dpi'] = mpl.rcParams['axes.unicode_minus'] = False # 解决保存图像是负号'-'显示为方块的问题

conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化MongoClient
db = conn.get_database('Github996')  # 连接到Github996数据库

users = db.get_collection('users')
data = users.find()  # 查询这个集合下的所有记录
user_data = json_normalize([record for record in data])

issues = db.get_collection('issues')
data = issues.find()  # 查询这个集合下的所有记录
issues_data = json_normalize([record for record in data])

user_data.info()

user_data.to_csv('users_data.csv', index=False)
issues_data.to_csv('issues_data.csv', index=False)


'''数据清洗'''
user_data.sample(5)
user_data.iloc[666]
user_data.columns

# 先去除对于分析无用的字段
user_data.drop(columns=['_id', 'avatar_url', 'events_url', 'followers_url', 'following_url',
                         'gists_url', 'gravatar_id', 'html_url', 'node_id', 'public_gists',
                          'received_events_url', 'repos_url', 'site_admin', 'starred_url',
                         'subscriptions_url', 'type'],
               inplace=True)
user_data.info()

# 时间类型转换
user_data['created_at'] = pd.to_datetime(user_data['created_at'])
user_data['updated_at'] = pd.to_datetime(user_data['updated_at'])

# issue数据清洗
issues_data.info()
issues_data.sample(5)
issues_data.iloc[888]
# 由于字段太多，直接抽取想要的字段
issues_data = issues_data[['comments', 'id', 'title', 'updated_at', 'user.id']]
issues_data.info()
# 时间类型转换
issues_data['updated_at'] = pd.to_datetime(issues_data['updated_at'])

# 单位字段太乱了，先提取前50
user_data['company'].value.counts()[:50]

def get_company(data):
    for com in ['encent', '腾讯']:
        if com in data:
            return "腾讯"
    for com1 in ['aidu', '百度']:
        if com1 in data:
            return '百度'
    for com2 in ['libaba', '淘宝', 'aobao', 'lipay', '阿里巴巴', 'liyun', '阿里云']:
        if com2 in data:
            return '阿里系'
    for com3 in ['JD', 'jd', '京东']:
        if com3 in data:
            return '京东'
    for com4 in ['etease', 'etEase', '网易']:
        if com4 in data:
            return '网易'
    for com6 in ['ytedance', '字节', '头条']:
        if com6 in data:
            return '头条'
    for com7 in ['eleme', '饿了么']:
        if com7 in data:
            return '饿了么'
    for com8 in ['uawei', '华为']:
        if com8 in data:
            return '华为'
    for com9 in ['didi', 'DiDi', '滴滴', '嘀嘀']:
        if com9 in data:
            return '滴滴'


user_data['company_top'] = user_data.loc[user_data['company'].notna(), 'company'].apply(get_company)
top10_com = user_data['company_top'].value_counts()


from pyecharts.charts import Bar
from pyecharts import options as opts


def bar() -> Bar:
    bar = (
        Bar()
        .add_xaxis(top10_com.index)
        .add_yaxis('', top10_com.values)
        .set_global_opts(
            title_opts=opts.TitleOpts(title='关注996工作制的程序员所在公司Top10'),
            xaxis_opts=opts.AxisOpts(axislabel_opts=opts.LabelOpts(rotate=30)))
    )
    return bar


def get_uni(data):
    for uni in ['hejiang', 'ZJU', 'zju', '浙江大学', '浙大']:
        if uni in data:
            return '浙大'
    for uni2 in ['singhua', '清华大学']:
        if uni2 in data:
            return '清华'
    for uni3 in ['Shanghai Jiao Tong', 'SJTU', '上海交大', '上海交通大学']:
        if uni3 in data:
            return '上海交大'
    for uni4 in ['UESTC', '电子科大', '电子科技大学']:
        if uni4 in data:
            return '电子科大'
    for uni5 in ['Wuhan', '武大', '武汉大学']:
        if uni5 in data:
            return '武大'
    for uni6 in ['USTC', '中科大', '中国科学技术大学']:
        if uni6 in data:
            return '中科大'
    for uni7 in ['Fudan', '复旦']:
        if uni7 in data:
            return '复旦'
    for uni8 in ['arbin', '哈']:
        if uni8 in data:
            return '哈工大'
    for uni9 in ['BUPT', '北邮', '北京邮电']:
        if uni9 in data:
            return '北邮'


# 关注996的程序员都来自哪些大学
user_data['uni_top'] = user_data.loc[user_data['company'].notna(), 'company'].apply(get_uni)
top10_uni = user_data['uni_top'].value_counts()


# 关注996的程序员都来自哪些城市
user_data['location'].value_counts()[:50]


def get_city(data):
    for city in ['eijing', '北京']:
        if city in data:
            return '北京'
    for city1 in ['hanghai', '上海']:
        if city1 in data:
            return '上海'
    for city2 in ['Hangzhou', 'hangzhou', '杭州']:
        if city2 in data:
            return '杭州'
    for city3 in ['henzhen', '深圳']:
        if city3 in data:
            return '深圳'
    for city4 in ['Guangzhou', 'guangzhou', '广州']:
        if city4 in data:
            return '广州'
    for city5 in ['hengdu', '成都']:
        if city5 in data:
            return '成都'
    for city6 in ['anjing', '南京']:
        if city6 in data:
            return '南京'
    for city7 in ['ingapore', '新加坡']:
        if city7 in data:
            return '新加坡'
    for city8 in ['Hong Kong', 'hong kong', '香港']:
        if city8 in data:
            return '香港'
    for city9 in ['uhan', '武汉']:
        if city9 in data:
            return '武汉'


user_data['city_top'] = user_data.loc[user_data['location'].notna(), 'location'].apply(get_city)
top10_city = user_data['city_top'].value_counts()


# 关注996的程序员的画像
# 关注996工作制的程序员Github平均粉丝数，关注数，仓库数
user_mean = user_data[['followers', 'following', 'public_repos']].mean()

# 关注996工作制的程序员Github粉丝数分布图
sns.set(font_scale=1.5)
sns.distplot(user_data.loc[user_data['followers'] < 50, 'followers'], kde=False)

# 关注996工作制的程序员注册Github时长
user_data['time'] = pd.to_datetime('2019-03-28')- user_data['created_at']

user_data['time'].mean()  # 均值


def get_days(data):
    return data.days


user_data['time_days'] = user_data['time'].apply(get_days)/365


# 关注996工作制的程序员注册Github时长分布图
sns.set(font_scale=1.5)
ax = sns.distplot(user_data['time_days'], kde=False)
ax.set_xlabel('Year')

# 关注996工作制的程序员大牛
user_data.loc[user_data['followers'] > 3000, ['login', 'followers','url', 'bio']]

# 大家所关注的问题都有哪些
issues_data.iloc[issues_data['comments'].nlargest(10).index][['title', 'comments']]


# 大家都在讨论什么东西呢？
import jieba
from collections import Counter
from pyecharts.charts import WordCloud

jieba.add_word('996')
jieba.add_word('996制度')
jieba.add_word('ICU')

swords = [x.strip() for x in open ('stopwords.txt')]


def plot_word_cloud(data, swords):
    text = ''.join(data['title'])
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word)>1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word':list(c.keys()), 'counts':list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    wordcloud = WordCloud(width=1300, height=620)
    wordcloud.add("", wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    return wordcloud


plot_word_cloud(issues_data, swords=swords)


# 关注996的程序员简介词云图
def plot_word_cloud(data, swords):
    text = ''.join(data['bio'].astype('str'))
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word) > 1 and (word not in swords):
            ex_sw_words.append(word)
    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word': list(c.keys()), 'counts': list(c.values())})\
        .sort_values(by='counts', ascending=False).head(100)
    word_cloud = WordCloud()
    word_cloud.add('', wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    return word_cloud


swords.extend(['the', 'is', 'and', 'of', 'be', 'to', 'in', 'for', 'from', 'am'])
plot_word_cloud(user_data, swords=swords)












