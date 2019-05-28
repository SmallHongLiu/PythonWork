# coding=utf-8
'''
Author: Small_Hong
date: 2019-05-27 17:52
'''

import requests
from bs4 import BeautifulSoup


def get_soup(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36'
    }
    req = requests.get(url, headers=headers)
    soup = BeautifulSoup(req.content, 'lxml')
    return soup


article_list = []


def get_data(soup):
    content = soup.find('div', attrs={'class': 'search-list-con'})
    data_list = content.find_all('dl', attrs={'class': 'search-list J_search'})
    for item in data_list:
        title = item.find('div', attrs={'class': 'limit_width'}).text.replace('\n', '')
        tag = item.select('dl[class="search-list J_search"] span')[0]
        if tag is not None:
            if tag.text == '博客' or tag.text == '论坛' or tag.text == '问答' or tag.text == '图文课':
                detail_content = item.find('dd', attrs={'class': 'search-detail'}).text
                author = item.find('span', attrs={'class': 'author'}).text
                date = item.find('span', attrs={'class': 'date'}).text[3:]
                student = None
                link = item.find('span', attrs={'class': 'link'}).text
                count = item.find('span', attrs={'class': 'down fr'}).text[:-3]
            elif tag.text == '学院':
                print(item)
                detail_content = item.find('dd', attrs={'class': 'search-detail'}).text
                author = item.find('a', attrs={'class': 'teacher'}).text
                date = None
                student = item.find('a', attrs={'class': 'num'}).text[:-4]
                link = item.find('span', attrs={'class': 'linking'}).text
                count = None
            elif tag.text == '下载':
                detail_content = item.find('dd', attrs={'class': 'search-detail'}).text
                author = item.find('span', attrs={'class': 'author'}).text
                date = item.find('span', attrs={'class': 'date'}).text[3:]
                student = None
                link = item.find('span', attrs={'class': 'link super'}).text
                count = None
            article = {
                'title': title,
                'tag': tag.text,
                'detail_content': detail_content,
                'author': author,
                'date': date,
                'student': student,
                'link': link,
                'count': count
            }
            article_list.append(article)
        else:
            continue


def main():
    soup = get_soup('https://so.csdn.net/so/search/s.do?p=2&q=数据分析&t=&domain=&o=&s=&u=&l=&f=')
    get_data(soup)


if __name__ == '__main__':
    main()
    print(len(article_list))


