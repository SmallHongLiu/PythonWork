# coding=utf-8
'''
Author: Small_Hong
date: 2019-05-23 $ {TIME}
'''
from copyheaders import headers_raw_to_dict
from bs4 import BeautifulSoup
import requests
import time
import re

headers = b"""
accept:text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8
accept-encoding:gzip, deflate, br
accept-language:zh-CN,zh;q=0.9
cache-control:max-age=0
upgrade-insecure-requests:1
user-agent:Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36
"""


# 将请求头字符串转化为字典
headers = headers_raw_to_dict(headers)

# 第一页有热门评论,拿取信息较麻烦,这里偷个懒~
for i in range(2, 4):
    print('第' + str(i) + '页')
    time.sleep(5)
    # 请求网址
    url = 'https://weibo.cn/comment/HjNyl82IU?uid=5852861043&rl=0&page=' + str(i)
    response = requests.get(url=url, headers=headers)
    html = response.text
    print(html)
    soup = BeautifulSoup(html, 'html.parser')
    # 评论信息
    # 评论信息
    result_1 = soup.find_all(class_='ctt')
    # 点赞数
    result_2 = soup.find_all(class_='cc')
    # 评论时间
    result_3 = soup.find_all(class_='ct')
    # 获取用户名
    result_4 = re.findall('id="C_.*?href="/.*?">(.*?)</a>', html)

    print(len(result_1), len(result_2), len(result_3), len(result_4))

    try:
        for j in range(len(result_1)):
            # 获取点赞数
            res = re.findall('(\d+)', result_2[j*2].get_text())
            print(len(res))
            if len(res) > 0:
                praise = res[0]
                name = result_4[j]
                text = result_1[j].get_text().replace(',', '，')
                date = result_3[j].get_text().split(' ')[0]
                if '@' in text:
                    if ':' in text:
                        # 去除@及用户信息
                        comment = text.split(':')[-1]
                        print(name, comment, praise, date)
                        # 写入csv
                        with open('101.csv', 'a+') as f:
                            f.write(name + ',' + comment + ',' + praise + ',' + date + '\n')
                        f.close()
                    else:
                        # 无评论信息时
                        print(name, '无', praise, date)
                        with open('ycy.csv', 'a+') as f:
                            f.write(name + ',' + '无' + ',' + praise + ',' + date + '\n')
                        f.close()
                else:
                    # 只有评论信息
                    print(name, text, praise, date)
                    # 写入csv
                    with open('101.csv', 'a+') as f:
                        f.write(name + ',' + text + ',' + praise + ',' + date + '\n')
                    f.close()
            else:
                pass
    # 出现字符编码报错
    except:
        print('字符编码报错')
        continue

