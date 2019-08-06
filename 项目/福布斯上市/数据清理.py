# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 16:49
'''

import pandas as pd
import numpy as np

df_2007 = pd.read_csv('./data/data_forbes_2007.csv', encoding='gbk', thousands=',')
# print(df_2007.dtypes)
# df_2007.head(3)

# 更改columns的命名
column_update = ['Year', 'Rank', 'Company_cn_en', 'Country_cn_en', 'Industry_cn', 'Sales', 'Profits', 'Assets', 'Market_value']
df_2007.columns = column_update

# 将字符串转换为数字类型
df_2007[df_2007['Sales'].str.contains('.*[A-Za-z]', regex=True)]

# 用replace替换
df_2007['Sales'] = df_2007['Sales'].replace('([A-Za-z])', '', regex=True)

df_2007['Assets'] = df_2007['Assets'].replace('([A-Za-z])', '', regex=True)

df_2007['Assets'] = df_2007['Assets'].replace(',', '', regex=True)

# 检测NaN值
df_2007[pd.isnull(df_2007['Profits'])]

# 替换NaN为0
df_2007['Profits'].fillna(0, inplace=True)

# 替换非数字内容
df_2007['Profits'] = df_2007['Profits'].replace('([A-Za-z])', '', regex=True)

# 将string类型的数字转换为数据类型
df_2007['Sales'] = pd.to_numeric(df_2007['Sales'])
df_2007['Profits'] = pd.to_numeric(df_2007['Profits'])
df_2007['Assets'] = pd.to_numeric(df_2007['Assets'])

# 拆分Company_cn_en列
df_2007['Company_en'], df_2007['Company_cn'] = df_2007['Company_cn_en'].str.split('/', 1).str

# 拆分Country_cn_en列
df_2007['Country_cn'], df_2007['Country_en'] = df_2007['Country_cn_en'].str.split('(', 1).str

# 去掉）
df_2007['Country_en'] = df_2007['Country_en'].str.slice(0, -1)

# 区分中国大陆，中国香港，中国台湾
# 查找含"中国"的数据
df_2007[df_2007['Country_cn']].str.contains('中国', regex=True)
# 替换并查看结果
df_2007['Country_en'] = df_2007['Country_en'].replace(['HK.*', 'TA'], ['CN-HK', 'CN-TA'],regex=True)
df_2007[df_2007['Country_en'].str.contains('CN', regex=True)]

# 添加一行英文的行业名称
df_2007['Industry_en'] = ''

# 列名重新排序
columns_sort = ['Year', 'Rank', 'Company_cn_en','Company_en',
                'Company_cn', 'Country_cn_en', 'Country_cn',
                'Country_en', 'Industry_cn', 'Industry_en',
                'Sales', 'Profits', 'Assets', 'Market_value']

# 按指定list重新将columns进行排序
df_2007 = df_2007.reindex(columns=columns_sort)

print(df_2007.shape)
print(df_2007.dtypes)
df_2007.head(3)





















