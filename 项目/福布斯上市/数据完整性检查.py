# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 14:36
'''
import pandas as pd


df_2007 = pd.read_csv('./data/data_forbes_2015.csv', encoding='gbk', thousands=',')
print('the shape of DataFrame: ', df_2007.shape)