import re
import urllib.request

"""
# 糗事百科官网网址
url = 'https://www.qiushibaike.com'
data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
print(len(data))

'''伪装浏览器'''
headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5558.400 QQBrowser/10.1.1695.400')
# 设置开启工具
opener = urllib.request.build_opener()
# 添加报头，将爬虫伪装成浏览器成功
opener.addheaders = [headers]

for i in range(0, 20):
    # 构造每一页的网址
    this_url = 'https://www.qiushibaike.com/text/page/' + str(i) + '/'
    # 读取每一页的数据
    data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')

# 设置正则表达式
pat = '<div class="content">.*?<span>(.*?)</span>'
# 进行信息抓取，因为有换行符，所以要用re.S按.能匹配换行符
this_data = re.compile(pat, re.S).findall(data)
"""


'''最终代码'''
url = 'https://www.qiushibaike.com/text/'
# 采用浏览器伪装技术，先设置报头
headers = ('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5558.400 QQBrowser/10.1.1695.400')
# 设置开启工具
opener = urllib.request.build_opener()
# 添加报头，将爬虫伪装成浏览器成功
opener.addheaders = [headers]
# 将opener安装为全局
urllib.request.install_opener(opener)
# 爬取前20网页信息
for i in range(0, 20):
    # 异常处理
    try:
        # 构造每一页的网址
        this_url = 'https://www.qiushibaike.com/text/page/' + str(i + 1) + '/'
        # 读取每一页的数据
        data = urllib.request.urlopen(url).read().decode('utf-8', 'ignore')
        # 设置正则表达式
        pat = '<div class="content">.*?<span>(.*?)</span>'
        # 进行信息提取，因为有换行符，所以用re.S按.能匹配换行符
        this_data = re.compile(pat, re.S).findall(data)
        for d in this_data:
            print(d.strip())  # 字符串的前面和后面有的有换行符，可以用strip()方法去掉字符串首位处的换行符和空格
            print('---------------------')
    except urllib.error.HTTPError as e:
        if hasattr(e, 'code'):
            print(e.code)
        if hasattr(e, 'reason'):
            print(e.reason)

