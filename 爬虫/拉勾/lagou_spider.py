import requests
from bs4 import BeautifulSoup
import json
import time


def crawl_detail(id):
    url = 'https://www.lagou.com/jobs/%s.html' % id
    headers = {
        'Host': 'www.lagou.com',
        'Referer': 'https: // www.lagou.com / jobs / list_python?labelWords = & fromSearch = true & suginput =',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Upgrade - Insecure - Requests': '1'
    }

    req = requests.get(url, headers=headers)
    print('crawl_detail: ', req.content)
    soup = BeautifulSoup(req.content, 'lxml')
    job_bt = soup.find('dd', attrs={'class': 'job_bt'})
    if job_bt is None:
        print('重新爬取: ', id)
        time.sleep(10)
        crawl_detail(id)
    else:
        content = job_bt.text  # text：提取该标签下面的所有文本信息
        return content


def main():
    url_start = 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput='
    url_parse = 'https://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC&needAddtionalResult=false'
    headers = {
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
        'Host': 'www.lagou.com',
        'Referer': 'https://www.lagou.com/jobs/list_python?labelWords=&fromSearch=true&suginput=',
        'X-Anit-Forge-Code': '0',
        'X-Anit-Forge-Token': None,
        'X-Requested-With': 'XMLHttpRequest'
    }

    positions = []
    for i in range(1, 2):
        print('开始爬取第%d页数据' % i)
        form_data = {
            'first': 'true',
            'pn': str(i),
            'kd': 'python'
        }
        s = requests.Session()
        s.get(url_start, headers=headers)  # 请求首页获取cookies
        cookie = s.cookies  # 为此次获取的cookies
        response = s.post(url_parse, data=form_data, headers=headers, cookies=cookie, timeout=3)
        time.sleep(5)
        response.encoding = response.apparent_encoding
        json_result = json.loads(response.text)
        curr_page_positions = json_result['content']['positionResult']['result']  # 当前页的职位信息
        print(curr_page_positions)
        #
        for position in curr_page_positions:
            print(position)
            # 获取某个职位的某些需要的信息
            position_dict = {
                'position_name': position['positionName'],
                'work_year': position['workYear'],
                'salary': position['salary'],
                'district': position['district'],
                'company_name': position['companyFullName']  # 公司全称
            }
            position_id = position['positionId']
            print(position_id)
            # 爬取某个职位的详情页面的信息
            time.sleep(10)
            position_detail = crawl_detail(position_id)
            position_dict['position_detail'] = position_detail
            positions.append(position_dict)
        print('爬取完第%s页数据: ' % i, positions)
        # 出现您操作太频繁，请稍后再试额解决方法
        # 1，要么把sleep的时间改大点儿
        # 2，每次请求不要太多，分多次请求
        time.sleep(5)

    line = json.dumps(positions, ensure_ascii=False)
    print(line)
    with open('lagou.json', 'wb') as f:
        f.write(line.encode('utf-8'))


if __name__ == '__main__':
    main()
    # content = crawl_detail('5525089')
    # print(content)