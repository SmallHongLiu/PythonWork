# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 18:18
'''

import pandas as pd
import numpy as np

# 数据源1: 从csv文件中读取数据
df_2013 = pd.read_csv('./data/data_forbes_2013.csv', encoding='gbk', header=None)
print('the shape of DataFrame: ', df_2013.shape)
print(df_2013.dtypes)
df_2013.head()

# 数据源2: Economy Watch数据获取
df_2013_economy = pd.read_csv('./data/data_forbes_2013_economywatch.csv', encoding='gbk')
print('the shape of DataFrame: ', df_2013_economy.shape)
print(df_2013_economy.dtypes)
df_2013_economy.head()

# 数据源3: excel文件
df_2013_all = pd.read_excel('./data/data_forbes_2013_all.xlsx')
print('the shape of DataFrame: ', df_2013_all.shape)
print(df_2013_all.dtypes)
df_2013_all.head()

# 数据清洗
# 更新列名
df_2013_all.columns = ['Rank', 'Company_cn_en', 'Country_cn', 'Sales', 'Profits', 'Assets', 'Market_value']
# 拆分"Company_cn_en"列，新生成两列，分别为公司英文名称和中文名称
df_2013_all['Company_cn'],df_2013_all['Company_en'] = df_2013_all['Company_cn_en'].str.split('/', 1).str
# print(df_2013_all['Company_cn'][:5])
# print(df_2013_all['Company_en'] [-5:])

# 将数据单位转换成十亿美元
df_2013_all[['Sales','Profits','Assets','Market_value']] = df_2013_all[['Sales','Profits','Assets','Market_value']].apply(lambda x: x/10)

# 添加年份2013
df_2013_all['Year'] = 2013

# 添加空白列
df_2013_all['Country_en'], df_2013_all['Country_cn_en'], df_2013_all['Industry_cn'], df_2013_all['Industry_en'] = ['','','','']

df_2013_all['Rank'] = pd.to_numeric(df_2013_all['Rank'])

# 按指定list重新将columns进行排序
columns_sort = ['Year', 'Rank', 'Company_cn_en','Company_en',
                'Company_cn', 'Country_cn_en', 'Country_cn',
                'Country_en', 'Industry_cn', 'Industry_en',
                'Sales', 'Profits', 'Assets', 'Market_value']
df_2013_all = df_2013_all.reindex(columns=columns_sort)

print(df_2013_all.shape)
print(df_2013_all.dtypes)
df_2013_all.head()


# 2015年的个别情况处理
# 数据有2020行，有重复行，需要去除重复行
# inplace=True，使去重生效
df_2015.drop_duplicates('Company_cn_en', inplace=True)

# 查看'Company_cn_en'是否还有重复行
df_2015[df_2015['Company_cn_en'].duplicated()]








