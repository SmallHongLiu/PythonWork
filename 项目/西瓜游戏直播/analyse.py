# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-08 11:43
'''


# 弹幕评论的词云图
import pandas as pd
import jieba
from collections import Counter
from pyecharts.charts import WordCloud

swords = [x.strip() for x in open('./data/stopwords.txt')]


def plot_word_cloud(data, swords):
    text = ''.join(data)
    words = list(jieba.cut(text))
    ex_sw_words = []
    for word in words:
        if len(word) > 1 and (word not in swords):
            ex_sw_words.append(word)

    c = Counter()
    c = Counter(ex_sw_words)
    wc_data = pd.DataFrame({'word': list(c.keys()), 'counts': list(c.values())}).sort_values(by='counts', ascending=False).head(100)
    word_cloud = WordCloud(width=1300, height=620)
    word_cloud.add('', wc_data['word'], wc_data['counts'], word_size_range=[20, 100])
    return word_cloud
