# coding=utf-8
'''
Author: Small_Hong
date: 2019-08-06 16:01
'''

import requests
from bs4 import BeautifulSoup
import csv

# 模块：页面download
def download(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return response.text


# 模块：企业表格信息
def get_content_first_page(html, country='China'):
    '''获取China的公司列表，且包含表头'''
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    label_div = body.find('div', {'class': 'content post'})
    tables = label_div.find_all('table')

    # tables一共有2个，第一个才是我们想要的数据
    trs = tables[0].find_all('tr')

    # 获取标题行信息
    row_title = [td.text for td in trs[0].find_all('td')]
    row_title.insert(2, 'Country')

    data_list = []
    data_list.append(row_title)
    for i, tr in enumerate(trs):
        if i == 0:
            continue
        tds = tr.find_all('td')

        # 获取公司排名及列表
        row = [item.text.strip() for item in tds]
        row.insert(2, country)
        data_list.append(row)
    return data_list


# 模块：其它国家的网页链接
def get_country_info(html):
    '''获取除China外其它国家的网页链接及国家名称'''
    soup = BeautifulSoup(html, 'lxml')
    body = soup.body
    label_div = body.find('div', {'class': 'content post'})
    tables = label_div.find_all('table')

    label_a = tables[1].find_all('a')
    country_names = [item.text for item in label_a]
    page_urls = [item.get('href') for item in label_a]
    country_info = list(zip(country_names, page_urls))
    return country_info


# 模块：信息保存
def save_data_to_csv_file(data, file_name):
    '''保存数据到csv文件中'''
    with open(file_name, 'a', errors='ignore', newline='') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(data)


# 编写网页爬取主函数文件
def get_forbes_global_year_2013():
    url = 'http://www.economywatch.com/companies/forbes-list/china.html'
    html = download(url)

    data_first_page = get_content_first_page(html)
    print('saving data ...', 'China')
    save_data_to_csv_file(data_first_page, 'forbes_economy_watch_2013.csv')

    country_info = get_country_info(html)

    for item in country_info:
        country_name = item[0]
        country_url = item[1]

        if country_name == 'China':
            continue

        html = download(country_url)
        data_other_country = get_content_other_country(html, country_name)
        print('saving data ...', country_name)
        save_data_to_csv_file(data_other_country, 'forbes_economy_watch_2013.csv')


if __name__ == '__main__':
    get_forbes_global_year_2013()





