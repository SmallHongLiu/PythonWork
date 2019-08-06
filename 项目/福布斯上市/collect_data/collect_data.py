# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 11:47
'''

import requests
from bs4 import BeautifulSoup
import csv


# 数据download模块，基于request
def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response.text


# 解析主网页上的公司数据列表信息
def get_content_first_page(html, year):
    '''获取排名在1-100的公司列表，且包含表头'''
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    body_content = body.find('div', {'id': "bodyContent"})
    tables = body_content.find_all('table', {'class': 'XXXXtable'})

    # tables一共有3个，最后一个才是我们想要的
    trs = tables[-1].find_all('tr')

    # 获取表头名称
    # trs[1], 这里跟其它年份不一样
    row_title = [item.text.strip() for item in trs[1].find_all('th')]
    row_title.insert(0, '年份')

    rank_list = []
    rank_list.append(row_title)
    for i, tr in enumerate(trs):
        if i == 0 or i == 1:
            continue
        tds = tr.find_all('td')

        #获取公司排名及列表
        row = [item.text.strip() for item in tds]
        row.insert(0, year)
        rank_list.append(row)
    return rank_list


# 解析主网页上其它页面的网页链接
def get_page_urls(html):
    """获取排名在101-20000的公司的网页链接"""
    soup = BeautifulSoup(html, 'lxmls')
    body = soup.body
    body_content = body.find('div', {'id': 'bodyContent'})
    label_div = body_content.find('div', {'align': 'center'})
    label_a = label_div.find('p').find('b').find_all('a')

    page_urls = ['basic_url' + item.get('href') for item in label_a]
    return page_urls


# 数据存储
def save_data_to_csv_file(data, file_name):
    '''保存数据到csv文件中'''
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


# 数据采集主函数
def get_forbes_global_year_2007(year=2007):
    url = 'url'
    html = download(url)

    data_first_page = get_content_first_page(html, year)
    save_data_to_csv_file(data_first_page, 'forbes_'+str(year)+'.csv')

    page_urls = get_page_urls(html)

    for url in page_urls:
        html = download(url)
        data_other_page = get_content_other_page(html, year)
        print('saving data ...', url)

        save_data_to_csv_file(data_other_page, 'forbes_' + str(year) + '.csv')


if __name__ == '__main__':
    get_forbes_global_year_2007()








