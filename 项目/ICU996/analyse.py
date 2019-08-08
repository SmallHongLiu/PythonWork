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














