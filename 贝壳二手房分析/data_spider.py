# coding: utf-8
# author: Small_Hong
# @Time: 2019/5/20 下午9:30

import requests
from bs4 import BeautifulSoup
import pymongo


# 获取网页源码，生成soup对象
def getSoup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    return BeautifulSoup(response.content, 'lxml')


# 解析详情页数据
def get_detail_info(soup):
    detail_info = soup.find('div', attrs={'class': 'sellDetailPage'})
    area_name = detail_info.find('div', attrs={'class': 'areaName'}).find_all('a')
    base_content = detail_info.find('div', attrs={'class': 'introContent'}).find('div', attrs={'class': 'content'})
    span_list = base_content.find_all('span')
    span_list = [content.text for content in span_list]
    li_text_list = [content.get_text() for content in base_content.find_all('li')]
    real_area = None
    house_orientation = None
    decoration = None
    property = None
    house_type = None
    house_year = None
    if "套内面积" in span_list:
        real_area_index = span_list.index('套内面积')
        real_area = li_text_list[real_area_index][4:]
    if '房屋朝向' in span_list:
        house_orientation_index = span_list.index('房屋朝向')
        house_orientation = li_text_list[house_orientation_index][4:]
    if '装修情况' in span_list:
        decoration_index = span_list.index('装修情况')
        decoration = li_text_list[decoration_index][4:]
    if '产权年限' in span_list:
        property_index = span_list.index('产权年限')
        property = li_text_list[property_index][4:-1]

    transaction = detail_info.find('div', attrs={'class', 'transaction'})  # 交易属性
    transaction_span_list = [content.text for content in transaction.find_all('span')]
    transaction_li_text_list = [content.get_text() for content in transaction.find_all('li')]
    if '房屋用途' in transaction_span_list:
        house_type_index = transaction_span_list.index('房屋用途')
        house_type = transaction_li_text_list[house_type_index][4:]
    if '房屋年限' in transaction_span_list:
        house_year_index = transaction_span_list.index('房屋年限')
        house_year = transaction_li_text_list[house_year_index][4:]
    return area_name[0].text, area_name[1].text, real_area, house_orientation, decoration, property, house_type, house_year


# 解析数据
def getData(soup):
    home_list = soup.find_all('div', attrs={'class': "info clear"})
    for home in home_list:
        title = home.find('div', attrs={'class': 'title'}).find('a')
        flood = home.find('div', attrs={'class': 'positionInfo'}).find('a').text  # 小区名字
        house_info = home.find('div', attrs={'class': 'houseInfo'}).text.replace('\n', ',').replace(' ', '').strip(',')
        label_area = house_info.split('|')[-2][:-3]  # 标注面积
        follow_info = home.find('div', attrs={'class': 'followInfo'}).text.replace('\n', '').replace(' ', '')
        tags = home.find('div', attrs={'class': 'tag'}).text.replace('\n', ',').strip(',')
        total_price = home.find('div', attrs={'class': 'totalPrice'}).text[:-1]
        unit_price = home.find('div', attrs={'class': 'unitPrice'}).text[3:-5]
        # 获取详情页信息
        detail_url = title.attrs['href'] + '?fb_expo_id=' + title.attrs['data-maidian']
        detail_soup = getSoup(detail_url)
        area, area_detail, real_area, house_orientation, decoration, property, house_type, house_year = get_detail_info(detail_soup)

        # 添加到数据库
        house = {'title': title.text, 'flood': flood, 'total_price(万)': total_price, 'unit_price(元)': unit_price,
                 'label_area(㎡)': label_area, 'real_area': real_area, 'house_orientation': house_orientation,
                 'area': area, 'area_detail': area_detail, 'decoration': decoration, 'property(年)': property,
                 'house_type': house_type, 'house_year': house_year, 'house_info': house_info,
                 'follow_info': follow_info, 'tags': tags}
        house_list.insert(house)


BASE_URL = 'https://cd.ke.com/ershoufang/pg'
# url列表
URL_LIST = []

for i in range(1, 10):
    url = BASE_URL + str(i) + '/'
    URL_LIST.append(url)

# 连接数据库
client = pymongo.MongoClient('localhost', 27017)
# 获取数据库
house_db = client.house_data
# 获取房屋集合
house_list = house_db.house_info


def main():
    # 删除所有数据
    house_list.remove({})

    count = 1
    for url in URL_LIST:
        soup = getSoup(url)
        getData(soup)
        print('第{}页数据爬取完成'.format(count))
        count = count + 1

    """
    detail_url = 'https://cd.ke.com/ershoufang/19050817710100247126.html?fb_expo_id=183326137201094662'
    detail_soup = getSoup(detail_url)
    get_detail_info(detail_soup)
    """


if __name__ == '__main__':
    main()

