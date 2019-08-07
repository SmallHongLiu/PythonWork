# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 18:56
'''

import pandas as pd
import numpy as np
from 数据处理4 import pro_col

df_2017 = pd.read_csv('./data/data_forbes_2017.csv', encoding='gbk')

# 更新列名
df_2017.columns = ['Year', 'Rank', 'Company_cn','Company_en',
                   'Country_en', 'Sales', 'Profits', 'Assets', 'Market_value']

print('the shape of DataFrame: ', df_2017.shape)
df_2017.head()

cols = ['Sales', 'Profits', 'Assets', 'Market_value']
for col in cols:
    pro_col(df_2017, col)

print('the shape of DataFrame: ', df_2017.shape)
print(df_2017.dtypes)
df_2017.head()

# 添加空白列
df_2017['Company_cn_en'],df_2017['Country_cn_en'], df_2017['Country_cn'], df_2017['Industry_cn'], df_2017['Industry_en'] = ['','','','','']

# 按指定list重新将columns进行排序
columns_sort = ['Year', 'Rank', 'Company_cn_en','Company_en',
                'Company_cn', 'Country_cn_en', 'Country_cn',
                'Country_en', 'Industry_cn', 'Industry_en',
                'Sales', 'Profits', 'Assets', 'Market_value']
df_2017 = df_2017.reindex(columns=columns_sort)

print(df_2017.shape)
df_2017.head()


# 数据合并
df_concat = pd.concat([df_2007, df_2008, df_2009,
                       df_2010, df_2011, df_2012,
                       df_2013_all, df_2014,
                       df_2015, df_2016, df_2017], ignore_index=True)

# 保存数据
# df_concat.to_csv('data_forbes_concat.csv')
df_concat.head()


# 国家英文名称为空值的处理
df_concat.loc[df_concat['Country_en'] == '', 'Country_en'] = df_concat.loc[df_concat['Country_en'] == '', 'Country_cn']

# 将国家名称统一为英文
list_origin = [']','AR', 'AS','AU', 'US', 'BE', 'BR', 'BS', 'BU', 'CA', 'CH', 'CI',
              'CN-HK', 'CN-TA', 'CO', 'CZ', 'DE', 'EG', 'FI', 'FR', 'GE',
              'GR', 'Hong Kong', 'Hong Kong/China', 'HU', 'IC', 'ID', 'IN', 'IR',
              'IS','IT', 'JA', 'JO', 'KO','LI', 'LU', 'MX', 'NL', 'NO', 'NZ',
               'PA', 'PE', 'PH', 'PK', 'PL', 'PO', 'RU', 'SI', 'SP', 'SU',
              'SW', 'SZ', 'Taiwan', 'TH', 'TU', 'UK', 'VE', '阿根廷', '阿联酋',
              '阿曼', '埃及', '爱尔兰', '奥地利', '澳大利亚', '巴基斯坦', '巴林',
              '巴拿马', '巴西', '百慕大', '比利时', '波多黎各', '波兰', '丹麦',
              '德国', '多哥', '俄罗斯', '法国', '菲律宾', '芬兰', '哥伦比亚',
              '哈萨克斯坦', '海峡群岛', '韩国', '荷兰', '加拿大', '捷克共和国',
              '卡塔尔', '开曼群岛', '科威特', '克罗地亚', '黎巴嫩', '利比里亚',
              '列支敦士登', '列支敦斯登', '卢森堡', '马来西亚', '毛里求斯',
              '美国', '秘鲁', '摩洛哥', '墨西哥', '南非', '尼日利亚', '挪威',
              '葡萄牙', '日本', '瑞典', '瑞士', '塞浦路斯', '沙特$',
              '沙特阿拉伯', '斯洛伐克', '泰国', '土耳其', '委内瑞拉', '西班牙',
              '希腊', '新加坡', '新西兰', '匈牙利', '以色列', '意大利',
              '印度$', '印度尼西亚', '印尼', '英国', '约旦', '越南', '智利',
              '中国大陆', '中国台湾', '中国香港', 'CN$', '中国$', 'Netherlands']

list_replace = ['','Argentina', 'Austria','Australia', 'United States', 'Belgium',
                'Brazil', 'Bahamas', 'Bermuda', 'Canada', 'Chile', 'Cayman Islands',
               'China-HongKong', 'China-Taiwan', 'Colombia', 'Czech Republic',
               'Denmark', 'Egypt', 'Finland', 'France', 'Germany', 'Greece', 'China-HongKong',
               'China-HongKong', 'Hungary', 'Iceland', 'Indonesia', 'India', 'Ireland', 'Israel',
               'Italy', 'Japan', 'Jordan', 'South Korea','Liberia', 'Luxembourg', 'Mexico',
               'Netherland', 'Norway', 'New Zealand', 'Panama', 'Peru', 'Philippines',
               'Pakistan', 'Poland', 'Portugal', 'Russia', 'Singapore', 'Spain',
               'Saudi Arabia', 'Sweden', 'Switzerland', 'China-Taiwan',
               'Thailand', 'Turkey', 'United Kingdom', 'Venezuela', 'Argentina',
               'United Arab Emirates', 'Oman', 'Egypt', 'Ireland', 'Austria', 'Australia',
               'Pakistan', 'Bahrain', 'Panama', 'Brazil', 'Bermuda', 'Belgium',
               'Puerto Rico', 'Poland', 'Denmark', 'Germany', 'Togo', 'Russia',
               'France', 'Philippines', 'Finland', 'Colombia', 'Kazakhstan',
               'Channel Islands', 'South Korea', 'Netherland', 'Canada',
               'Czech Republic', 'Qatar', 'Cayman Islands', 'Kuwait', 'Croatia', 'Lebanon',
               'Liberia', 'Liechtenstein', 'Liechtenstein', 'Luxembourg', 'Malaysia',
               'Mauritius', 'United States', 'Peru', 'Morocco', 'Mexico', 'South Africa',
               'Nigeria', 'Norway', 'Portugal', 'Japan', 'Sweden', 'Switzerland', 'Cyprus',
               'Saudi Arabia', 'Saudi Arabia', 'Slovakia', 'Thailand', 'Turkey', 'Venezuela',
               'Spain', 'Greece', 'Singapore', 'New Zealand', 'Hungary', 'Israel', 'Italy',
               'India', 'Indonesia', 'Indonesia', 'United Kingdom', 'Jordan', 'Vietnam',
               'Chile',  'China', 'China-Taiwan', 'China-HongKong', 'China', 'China',
               'Netherland']

df_concat['Country_en'] = df_concat['Country_en'].replace(list_origin,list_replace, regex=True)

# 进一步替换，包括一家公司属于多个国家的情况
# 注意这里没有 regex=True
df_concat['Country_en'] = df_concat['Country_en'].replace(['China-China-Taiwan',r'China-HongKong/China', r'Australia)/United Kingdom(United Kingdom',
                                                          r'Netherland)/United Kingdom(United Kingdom', r'Panama)/United Kingdom(United Kingdom',
                                                          r'SA)/United Kingdom(United Kingdom', r'United Kingdom)/Australia(SA', r'United Kingdom)/Netherland(Netherland',
                                                          r'United Kingdom)/South Africa(SA' , 'Netherland/United Kingdom', 'Panama/United Kingdom',
                                                          'Australia/United Kingdom'],
                                                          ['China-Taiwan', 'China-HongKong', 'United Kingdom/Australia', 'United Kingdom/Netherland',
                                                          'United Kingdom/Panama', 'United Kingdom/Australia', 'United Kingdom/Australia',
                                                          'United Kingdom/Netherland', 'United Kingdom/South Africa', 'United Kingdom/Netherland',
                                                          'United Kingdom/Panama', 'United Kingdom/Australia'])

# 同一个英文缩写代表不同国家的情况
# 注意需要以 "$"结尾

df_concat['Country_en'] = df_concat['Country_en'].replace(['MA$','SA$'],['', ''], regex=True)

df_concat.loc[df_concat['Country_en'] == '', 'Country_en'] = df_concat.loc[df_concat['Country_en'] == '', 'Country_cn']

df_concat['Country_en'] = df_concat['Country_en'].replace(['澳大利亚','马来西亚', '摩洛哥', '南非'],
                                                          ['Australia', 'Malaysia', 'Morocco', 'South Africa'])

# 保存数据
df_concat.to_csv('data_forbes_concat.csv')


