# 首先导入模块
import re
import urllib.request
import urllib.error

# 要爬取的网页的网站
url = 'https://blog.csdn.net/'
# 获取网页当前信息
page = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')  # 参数'ignore'表示解码遇到异常时忽略异常
# 设置正则表达式
pat = '<a.*?href="(.*?)" target="_blank"'
# 从网页信息中获取匹配出我们要的信息
links = re.compile(pat).findall(page)
print(len(links))
# 爬取的过程中发现了异常，存在:<a href='/nav/ai' target='_blank'>这样的代码，获取的不是网址，所以要进行过滤
links = [link for link in links if link[:4] == 'http']
print(len(links))
# 存放爬取的新闻网站信息
for i in range(0, len(links)):
    # 防止出现异常，而停止信息抓取，采用异常处理措施
    try:
        urllib.request.urlretrieve(links[i], 'news/' + str(i) + '.html')
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)
print('爬取成功!')



