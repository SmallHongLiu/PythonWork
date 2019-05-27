import requests
from bs4 import BeautifulSoup
from pyecharts.charts import Bar
from pyecharts import options as opts

ALL_DATA = []


def parse_page(url):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
    }
    response = requests.get(url, headers=headers)
    content = response.content.decode('utf-8')
    # 这里使用html5lib标签进行解析
    soup = BeautifulSoup(content, 'html5lib')
    con_mid_tab = soup.find('div', attrs={'class': 'conMidtab'})
    tables = con_mid_tab.find_all('table')
    for table in tables:
        trs = table.find_all('tr')[2:]  # 去除title，从第二个开始
        for index, tr in enumerate(trs):
            tds = tr.find_all('td')
            city_td = tds[0]
            if index == 0:
                city_td = tds[1]
            city = list(city_td.stripped_strings)[0]
            temp_td = tds[-5]
            max_temp = list(temp_td.stripped_strings)[0]
            ALL_DATA.append({'city': city, 'max_temp': int(max_temp)})


def main():
    urls = [
        'http://www.weather.com.cn/textFC/hb.shtml',
        'http://www.weather.com.cn/textFC/db.shtml',
        'http://www.weather.com.cn/textFC/hd.shtml',
        'http://www.weather.com.cn/textFC/hn.shtml',
        'http://www.weather.com.cn/textFC/xb.shtml',
        'http://www.weather.com.cn/textFC/xn.shtml',
        'http://www.weather.com.cn/textFC/gat.shtml'
    ]
    for url in urls:
        parse_page(url)

    '''分析数据'''
    # 根据最低气温进行排序
    ALL_DATA.sort(key=lambda data: data['max_temp'])

    # 获取前10
    data = ALL_DATA[0:10]
    cities = list(map(lambda x: x['city'], data))
    min_temps = list(map(lambda x: x['max_temp'], data))
    print(min_temps)
    chart = (
        Bar()
            .add_xaxis(cities)
            .add_yaxis('', min_temps)
            .set_global_opts(title_opts=opts.TitleOpts(title='中国天气最低气温Top10排行榜'))
    )

    chart.render('Top10 max_temp.html')  # 渲染


if __name__ == '__main__':
    main()
