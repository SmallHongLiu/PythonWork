from urllib import request
from chardet import detect
from bs4 import BeautifulSoup
import pandas as pd
import time
import random

# 获取网页源码，生成soup对象
def getSoup(url):
    with request.urlopen(url) as fp:
        byt = fp.read()
        det = detect(byt)
        time.sleep(random.randrange(1, 5))
        return BeautifulSoup(byt.decode(det['encoding']), 'lxml')

# 解析数据
def getData(soup):
    ol = soup.find('tbody', attrs = {'class': "lister-list"})
    score_info = ol.find_all('td', attrs={'class': 'imdbRating'})
    film_scores = [k.text.replace('\n', '') for k in score_info]
    # 获取评分，电影名，导演，演员，上映年份，详情网页链接
    film_info = ol.find_all('td', attrs={'class': 'titleColumn'})
    film_names = [k.find('a').text for k in film_info]
    film_actors = [k.find('a').attrs['title'] for k in film_info]
    film_years = [k.find('span').text[1:5] for k in film_info]
    next_nurl = [url2 + k.find('a').attrs['href'][0:17] for k in film_info]
    data = pd.DataFrame({'name': film_names, 'year': film_years, 'socre': film_scores, 'actors':film_actors,'newurl':next_nurl})
    return data

# 获取详情页数据
def getNextUrl(detail, detail1):
    # 获取电影国家
    detail_list = detail.find('div', attrs={'id': 'titleDetails'}).find_all('div', attrs={'class': 'txt-block'})
    detail_str = [k.text.replace('\n', '') for k in detail_list]
    detail_str = [k for k in detail_str if k.find(':') >= 0]
    detail_dict = {k.split(':')[0] : k.split(':')[1] for k in detail_str}
    country = detail_dict['Country']
    # 获取电影类型
    detail_list1 = detail.find('div', attrs={'class': 'title_wrapper'})
    detail_str1 = [k.text for k in detail_list1.find_all('a')]
    movie_type = pd.DataFrame({'Type': detail_str1})
    # 获取以组划分的电影详细评分，人数
    div_list = detail1.find_all('td', attrs={'align': 'center'})
    value = [k.find('div', attrs={'class': 'bigcell'}).text.strip() for k in div_list]
    num = [k.find('div', attrs={'class': 'smallcell'}).text.strip() for k in div_list]
    scores = pd.DataFrame({'value': value, 'num': num})
    return country, movie_type, scores

if __name__ == '__main__':
    url = "https://www.imdb.com/chart/top"
    url2 = "https://www.imdb.com"
    soup = getSoup(url)
    movie_data = getData(soup)
    # print(movie_data)
    movie_data['Country'] = 'Unknown'
    movie_data['Type'] = 'Unknown'
    movie_data['scores'] = 'Unknown'
    movie_data['nums'] = 'Unknown'
    b = movie_data['newurl']
    print(len(b))
    this_country = movie_data['Country']
    this_type = movie_data['Type']
    this_score = movie_data['scores']
    soup3 = getSoup(b[0])
    soup4 = getSoup(b[0] + 'ratings')
    this_country, this_type, this_score = getNextUrl(soup3, soup4)
    for i in range(len(b)):  # 注意：在for in range()中
        soup3 = getSoup(b[i])
        soup4 = getSoup(b[i] + 'ratings')
        this_country, this_type, this_score = getNextUrl(soup3, soup4)
        print(this_score)
        movie_data['Country'][i] = this_country
        movie_data['Type'][i] = this_type['Type'][1 : this_type.size - 1]
        movie_data['scores'][i] = this_score['value']
        movie_data['nums'][i] = this_score['num']
        print(i)