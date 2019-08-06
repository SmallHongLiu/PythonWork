# coding=utf-8
'''
Author: Small_Hong
date: 2019-06-03 17:31
'''
import pandas as pd
from pyecharts import Pie, Bar, Line, Scatter, EffectScatter, Geo
from pyecharts import Page
from pyecharts import Style


# 读取数据
def read_data():
    house_list = pd.read_excel("house_list.xlsx")
    return house_list


# 区域饼状图分析
def pie():
    house_list = read_data()
    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    # 生成饼状图
    attr = area_com['区域']
    v1 = area_com['count']
    pie = Pie('房屋区域分布情况', title_pos='center', title_top=20)
    pie.add('', attr, v1, label_text_color=None, is_label_show=True,
            radius=[0, 50], legend_pos='bottom', legend_top='%10')
    pie.render('房屋区域分布情况-饼状图.html')


# 区域柱状图分析
def bar():
    house_list = read_data()
    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    attr = area_com['区域']
    v1 = area_com['count']
    chart = Bar('房屋区域分布情况', title_pos='center', title_top=20, title_color='#ff7f50')
    chart.add('', attr, v1, is_label_show=True, is_datazoom_show=True, xaxis_interval=0, yaxis_rotate=0,
              xaxis_line_color='#000000', label_text_color='#ff7f50', yaxis_label_textcolor='#c23531',
              line_color='#ff7f50',
              datazoom_type='inside', datazoom_range=[10, 60], mark_point=['min', 'max'],
              tooltip_background_color='#61a0a8', tooltip_text_color='#749f83')
    chart.print_echarts_options()
    chart.render('房屋区域分布情况－柱状图.html')


# 折线图
def line():
    house_list = read_data()
    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    attr = area_com['区域']
    v1 = area_com['count']
    chart = Line('房屋区域分布情况', title_pos='center')
    chart.add('', attr, v1, xaxis_interval=0,
              mark_point=['min', 'max', 'average'], mark_point_symbol='diamond',
              is_datazoom_show=True, datazoom_type='inside', is_datazoom_extra_show=False)
    chart.render('房屋区域分布情况-折线图.html')


# 散点图
def scatter():
    house_list = read_data()
    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    attr = area_com['区域']
    v1 = area_com['count']
    chart = Scatter('房屋区域分布情况', title_pos='center')
    chart.add('', attr, v1,
              xaxis_interval=0, xaxis_type='category',
              is_yaxis_show=False,
              is_datazoom_show=True, datazoom_type='inside',
              visual_type='size')
    chart.render('房屋区域分许情况-散点图.html')


# 动态散点图
def effect_scatter():
    house_list = read_data()
    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    attr = area_com['区域']
    v1 = area_com['count']
    chart = EffectScatter('房屋区域分布情况', title_pos='center')
    chart.add('', attr, v1, xaxis_interval=0, xaxis_type='category',
              is_datazoom_show=True, datazoom_type='inside')
    chart.render('房屋区域分布情况-动态散点图.html')


# 地理坐标系
def geo():
    """
    house_list = read_data()

    area_group = house_list.groupby(['区域'])
    area_com = area_group['区域'].agg(['count'])
    area_com.reset_index(inplace=True)

    # attr = area_com['区域']
    # for area in attr:
    #     if area is '武侯' or '成华' or '青羊' or '金牛' or '锦江' or '龙泉驿' or '温江' or '郫都' or ''
    attr = area_com['区域']
    for i in range(0, len(attr)):
        if attr[i] == '双流':
            attr[i] += '县'
        elif attr[i] == '郫都' or attr[i] == '高新西':
            attr[i] = '郫县'
        elif attr[i] == '彭州' or attr[i] == '崇州' or attr[i] == '都江堰':
            attr[i] += '市'
        elif attr[i] == '天府新区' or attr[i] == '高新':
            attr[i] = '武侯区'
        else:
            attr[i] += '区'

    v1 = area_com['count']
    print(attr)
    print(v1)
    """

    style = Style(
        title_color='#fff',
        title_pos='center',
        width=1200,
        height=600,
        background_color='#404a59')

    data = [('澄海区', 30), ('南澳县', 40), ('龙湖区', 50), ('金平区', 60)]
    chart = Geo('房屋区域分布情况', **style.init_style)
    attr, value = chart.cast(data)
    chart.add("", attr, value, maptype="汕头", is_visualmap=True,
              is_legend_show=False,
              tooltip_formatter='{b}',
              label_emphasis_textsize=15,
              label_emphasis_pos='right')
    page = Page()
    page.add(chart)
    page.render()


if __name__ == '__main__':
    # pie()
    # bar()
    # line()
    # scatter()
    # effect_scatter()
    geo()