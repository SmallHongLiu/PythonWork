# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 17:36
'''

import pandas as pd
import numpy as np

# 从csv文件中读取数据
df_2008 = pd.read_csv('./data/data_forbes_2008.csv', encoding='gbk', thousands=',')

print('the shape of DataFrame: ', df_2008.shape)
print(df_2008.dtypes)
df_2008.head()

# 更新列名
df_2008.columns = ['Year', 'Rank', 'Company_en', 'Company_cn','Country_en', 'Industry_en', 'Sales', 'Profits', 'Assets', 'Market_value']
df_2008.head()

# 添加空白列，使之与其他年份的格式保持一致
df_2008['Company_cn_en'], df_2008['Country_cn_en'], df_2008['Country_cn'], df_2008['Industry_cn'] = ['','','','']
df_2008.head()

# 将字符串转换为数字类型
col_digit = ['Sales', 'Profits', 'Assets', 'Market_value']

for col in col_digit:
    # 将数字后面的字母进行替换
    df_2008[col] = df_2008[col].replace('([A-Za-z])', '', regex=True)
    # 千分位数字的逗号被识别为string了，需要替换
    df_2008[col] = df_2008[col].replace(',', '', regex=True)
    # 将数字型字符串转换为可进行计算的数据类型
    df_2008[col] = pd.to_numeric(df_2008[col])

# 按指定list重新将columns进行排序
columns_sort = ['Year', 'Rank', 'Company_cn_en','Company_en',
                'Company_cn', 'Country_cn_en', 'Country_cn',
                'Country_en', 'Industry_cn', 'Industry_en',
                'Sales', 'Profits', 'Assets', 'Market_value']

df_2008 = df_2008.reindex(columns=columns_sort)
print(df_2008.shape)
print(df_2008.dtypes)
df_2008.head()



