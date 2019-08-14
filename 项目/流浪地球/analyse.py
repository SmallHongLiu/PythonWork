# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-14 14:24
'''

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pymongo import MongoClient
from pandas.io.json import json_normalize
from pyecharts.charts import Bar, Line, WordCloud
import jieba
from collections import Counter

conn = MongoClient(host='127.0.0.1', port=27017)  # 实例化Mongoclient
db = conn.get_database('maoyan')  # 连接到maoyan数据库

maoyan = db.get_collection('maoyan')  #连接到集合maoyan
mon_data = maoyan.find() # 查询这个集合下的所有记录

data = json_normalize([comment for comment in mon_data])

# 数据清洗
data = data.drop(columns='_id')
data = data.drop_duplicates(subset='userId')
data['time'] = pd.to_datetime(data['time'] / 1000, unit='s')
data = data[data['time'] >= pd.to_datetime('2019-02-05 00:00:00')]
data.set_index(data['time'], inplace=True)
data.head()

'''问题'''
# 1.总体评价如何
data['score'].mean()
score_total = data['score'].value_counts().sort_index()
bar = Bar("《流浪地球》各评分数量", width=700)
line = Line("", width=700)
bar.add("", score_total.index, score_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
line.add("", score_total.index, score_total.values+1000, is_smooth=True)
bar.overlap(line)

score_total[:5].sum() / score_total.sum() * 100  # 低分比例
score_total[:7].sum() / score_total.sum() * 100  # 高分比例
score_total[10:].sum() / score_total.sum() * 100  # 满分比例


# 2.总体评价的时间走向如何
score_by_time = data['score'].resample('H').mean()
line = Line("《流浪地球》平均评分时间走向", width=700)
line.add("", score_by_time.index.date, score_by_time.values, is_smooth=True,
         legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18,
         xaxis_rotate=20, yaxis_min=8)
score_by_time.nsmallest(6)

# 3.高分的评价理由是什么？
jieba.add_word('屈楚萧')
jieba.add_word('刘启')
jieba.add_word('吴京')
jieba.add_word('刘培强')
jieba.add_word('李光洁')
jieba.add_word('王磊')
jieba.add_word('吴孟达')
jieba.add_word('达叔')
jieba.add_word('韩子昂')
jieba.add_word('赵今麦')
jieba.add_word('韩朵朵')

swords = [x.strip() for x in open('stopwords.txt')]


def plot_word_cloud(data, sword):
    text = ''.join(data['content'])
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word) > 1 and (word not in swords):
            ex_sw_words.append(word)

    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word': list(c.keys()), 'counts': list(c.values())}).\
        sort_values(by='counts', ascending=False).head(100)
    word_cloud = WordCloud(width=1300, height=620)
    word_cloud.add('', wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    return word_cloud


# 高分的评价
plot_word_cloud(data=data[data['score'] > 6], swords=swords)

data[data['score'] > 6].nlargest(10, 'upCount')
for i in data[data['score'] > 6].nlargest(10, 'upCount')['content']:
    print(i + '\n')

# 4.低分的评价理由是什么？
# 低分的评价
plot_word_cloud(data=data[data['score'] < 5], swords=swords)
data[data['score'] < 5].nlargest(10, 'upCount')

# 5.低分的人群都有哪些特征（性别，等级）
# 总体的性别比例
gender_total = data['gender'].value_counts()  # 对Series每个值进行计数并默认为降序排序
bar = Bar("《流浪地球》观众性别", width=700)
bar.add("", ['未知', '男', '女'], gender_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

gender_total / gender_total.sum() * 100

# 低分的性别比例
gender_low = data.loc[data['score'] < 5, 'gender'].value_counts()
bar = Bar("《流浪地球》低分评论观众性别", width=700)
bar.add("", ['未知', '男', '女'], gender_low.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)
gender_low / gender_low.sum() * 100

# 总体的等级比例
level_total = data['userLevel'].value_counts().sort_index()
bar = Bar("《流浪地球》观众等级", width=700)
bar.add("", level_total.index, level_total.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

# 低分评论的观众等级比例
level_low = data.loc[data['score'] < 5, 'userLevel'].value_counts().sort_index()
bar = Bar("《流浪地球》低分评论的观众等级", width=700)
bar.add("", level_low.index, level_low.values, is_stack=True, is_label_show=True,
       bar_category_gap='40%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

# 6.高低分跟哪些演员有关？
mapping = {'liucixin':'刘慈欣|大刘', 'guofan':'郭帆', 'quchuxiao':'屈楚萧|刘启|户口', 'wujing':'吴京|刘培强',
           'liguangjie':'李光洁|王磊', 'wumengda':'吴孟达|达叔|韩子昂', 'zhaojinmai':'赵今麦|韩朵朵'}
for key, value in mapping.items():
    data[key] = data['content'].str.contains(value)

# 总体提及次数
staff_count = pd.Series({key: data.loc[data[key], 'score'].count() for key in mapping.keys()}).sort_values()
bar = Bar("《流浪地球》演职员总体提及次数", width=700)
bar.add("", ['李光洁','郭帆','赵今麦','吴孟达','屈楚萧','刘慈欣','吴京'], staff_count.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

average_score = pd.Series({key: data.loc[data[key], 'score'].mean() for key in mapping.keys()}).sort_values()
bar = Bar("《流浪地球》演职员平均分", width=700)
bar.add("", ['赵今麦','吴孟达','吴京','屈楚萧','李光洁','刘慈欣','郭帆'], np.round(average_score.values,2), is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

staff_count_low = pd.Series({key: data.loc[data[key] & (data['score'] < 5), 'score'].count() for key in mapping.keys()}).sort_values()

staff_count_pct = np.round(staff_count_low / staff_count * 100, 2).sort_values()
bar = Bar("《流浪地球》演职员低分评论提及百分比", width=700)
bar.add("", ['郭帆','刘慈欣','李光洁','屈楚萧','赵今麦','吴京','吴孟达'], staff_count_pct.values, is_stack=True, is_label_show=True,
       bar_category_gap='60%', label_color = ['#130f40'],
       legend_text_size=18,xaxis_label_textsize=18,yaxis_label_textsize=18)

# 吴孟达的低分评价
data[data['wumengda'] & (data['score'] < 5)].nlargest(5, 'upCount')
for i in data[data['wumengda']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')

# 吴京的低分评价
data[data['wujing'] & (data['score'] < 5)].nlargest(5, 'upCount')
for i in data[data['wujing']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')

# 赵今麦的低分评价
data[data['zhaojinmai'] & (data['score'] < 5)].nlargest(5, 'upCount')
for i in data[data['zhaojinmai']&(data['score']<5)].nlargest(5, 'upCount')['content']:
    print(i+'\n')














