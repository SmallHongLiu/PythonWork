# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-12 16:25
'''

import time
import datetime
import requests
import json
import csv
import pandas as pd
import matplotlib.pyplot as plt
import pylab as pl  # 用于修改x轴坐标
from wordcloud import WordCloud


def date_to_timestamp():
    ts = str(time.time() * 1000)
    ts = int(ts[:13])
    return ts


def get_page(i, ts):
    url = f"http://www.ceic.ac.cn/ajax/speedsearch?num=6&&page={i}&&callback=jQuery18006645167434821839_1565066006814&_={ts}"
    print(url)


# 1. 使用time
time_stamp = int(str(1565244347921)[:10])
time_array = time.localtime(time_stamp)
other_style_time = time.strftime("%Y--%m--%d %H:%M:%S", time_array)
print(other_style_time)

# 2. 使用datetime
time_stamp = int(str(1565244347921)[:10])
date_array = datetime.datetime.utcfromtimestamp(time_stamp)
other_style_time = date_array.strftime('%Y--%m--%d %H:%M:%S')
print(other_style_time)


def download(url):
    # 设置用户代理
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
    }
    response = requests.get(url, headers=headers)
    html = response.content.decode('utf-8')
    # 验证返回状态码是否为200
    if response.status_code == 200:
        return html


def parse_html(html):
    html = html['shuju']
    for item in html:
        yield {
            'CATA_ID': item["CATA_ID"],
            '震级(M)': item["M"],
            '发震时刻(UTC+8)': item["O_TIME"],
            '纬度(°)': item["EPI_LAT"],
            '经度(°)': item["EPI_LON"],
            '深度(千米)': item["EPI_DEPTH"],
            '参考位置': item["LOCATION_C"],
            '具体链接': f'http://news.ceic.ac.cn/{item["CATA_ID"]}.html',
        }


def save_to_csv(item):
    with open('最近一年世界地震情况-中国地震网.csv', 'a', encoding='utf_8_sig', newline='') as f:
        # 'a'为追加模式（添加）
        # utf_8_sig 格式导出csv不乱码
        fieldnames = ['CATA_ID', '震级(M)', '发震时刻(UTC+8)', '纬度(°)', '经度(°)', '深度(千米)', '参考位置', '具体链接']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerows(item)

def main(page):
    # 可知一年的地震信息共50页
    url = f'http://www.ceic.ac.cn/ajax/speedsearch?num=6&&page={page}'
    html = download(url)[1:-1]
    # 字符串转字典
    html = json.loads(html)
    for item in parse_html(html):
        save_to_csv(item)


if __name__ == '__main__':
    for page in range(60):
        main(page)

'''分析'''
columns = ['CATA_ID', 'Magnitude', 'Earthquake_Time', 'Latitude', 'Longitude', 'Depth', 'Earthquake_Location', 'Url']
df = pd.read_csv('最近一年世界地震情况-中国地震网.csv', encoding='utf-8', header=None, names=columns)  # 打开表格
df.head()  # 默认前5行数据

pl.rcParams['font.sans-serif'] = ['SimHei']  # 防中文显示成小方块
plt.style.use('ggplot')  # 默认绘图风格很难看，替换为好看的 ggplot 风格
fig = plt.figure(figsize=(8, 5))  # 设置图片大小
colorsl = '#FF8000'  #设置图表 title、text 标注的颜色

df_score = df.sort_values('Magnitude', ascending=False)  # 按得分降序排序

loc = df_score.Earthquake_Location[:10]  # x轴坐标
m = df_score.Magnitude[:10]  # y轴坐标
plt.bar(range(10), m, tick_label=loc)  #绘制条形图，用 range()能搞保持 x 轴正确顺序
plt.ylim((1, 10))  # 设置纵坐标轴范围
plt.title('近一年全球震级级别最高 top10', color=colorsl)  # 标题
plt.xlabel('地震具体位置', color=colorsl)   # x轴标题
plt.ylabel('震级级别', color=colorsl)  # y轴标题

# 为每个条形图添加数值标签
for x, y in enumerate(list(m)):
    plt.text(x, y+0.2, '%s'%round(y, 1), ha='center')

plt.xticks(rotation=290)  # x轴名称太长发生重叠，旋转为纵向显示
plt.tight_layout()  #自动控制空白边缘，以全部显示 x 轴名称
plt.show()


# 从日期中提取月份
df['Earthquake_Time'] = df['Earthquake_Time'].map(lambda x:x.split('-')[1])

# 统计各月发生地震次数
grouped_month = df.groupby('Earthquake_Time')
grouped_month_amount = grouped_month.Earthquake_Time.count()
top_month = grouped_month_amount.sort_values(ascending=False)
# 绘图
top_month.plot(kind='bar', color='#58ACFA')
for x, y in enumerate(list(top_month.values)):
    plt.text(x, y+0.8, '%s'%round(y, 1), ha='center', color='red')

plt.xticks(rotation=0)  # x轴名称太长发生重叠，旋转为纵向显示
plt.title('近一年全球每月发生地震次数排名', color=colorsl)
plt.xlabel('月份(年月)')
plt.ylabel('地震次数(此次)')
plt.tight_layout()
plt.show()


# 绘制饼图并保存
count = df['Earthquake_Location'].value_counts()
plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
plt.axis('equal')  # 使饼图为正圆形
plt.legend(loc='upper left', bbox_to_anchor=(-0.1, 1))
plt.show()

# 绘制饼图并保存
count = df['Magnitude'].value_counts()
plt.pie(count, labels=count.keys(), labeldistance=1.4, autopct='%2.1f%%')
plt.axis('equal')  # 使饼图为正圆形
plt.legend(loc='upper_left', bbox_to_anchor=(-0.1, 1))
plt.show()


# 绘制词云图
word_cloud = WordCloud()
word_cloud.generate('a boy is crying, a boy is smiling , a boy is faceless ')
word_cloud.to_image()

df = pd.read_csv('最近一年世界地震情况-中国地震网.csv', encoding='utf-8', header=None, names=columns)  # 打开表格
df = df.groupby(by='Depth').count()
df = df['Earthquake_Location'].sort_values(ascending=False)

font_path='simfang.ttf'  # 仿宋
word_cloud = WordCloud(
    background_color='#F3F3F3',
    font_path=font_path,
    width=1200,
    height=800,
    margin=2,
    max_font_size=200,
    random_state=42,
    scale=2,
    colormap='viridis',  # 默认virdis
)
word_cloud.fit_words(df)
plt.imshow(word_cloud, interpolation='bilinear')
plt.axis('off')
plt.show()







