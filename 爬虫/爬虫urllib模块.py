import urllib.request
import re

# urllib基础
sock = urllib.request.urlopen('https://www.baidu.com/')
data = sock.read().decode('utf-8')
urllib.request.urlretrieve("https://www.baidu.com/", "D:\\python\\1.html")
urllib.request.urlcleanup()
print(sock.info())
print(sock.getcode())
print(sock.geturl)
sock.close()


'''超时设置'''
# 语法：超时设置就是在urlopen()方法中多加一个timeout参数，所接的数字就是几秒响应
sock = urllib.request.urlopen('https://www.baidu.com/', timeout=0.1)

# 通常超时设置与异常处理一起用
for i in range(1, 100):
    try:
        data = urllib.request.urlopen('https://www.baidu.com/', timeout=0.1).read().decode('utf-8')
        print(len(data))
    except Exception as err:
        print('网页响应超时!')


# 简写爬虫缩写，自动爬取网页信息
keywd = 'python'
# 如果关键字是汉字，则需要对汉字进行转码，因为浏览器不能识别汉字
keywd = urllib.request.quote(keywd)  # 对关键字进行编码，若不是汉字则可以省略这一步
for i in range(1, 11):
    url = "https://www.so.com/s?q=" + keywd + "&pn=" + str(i)
    data = urllib.request.urlopen(url).read().decode('utf-8')
    pat = 'data-source="[234]">(.*?)</a>'
    res = re.compile(pat).findall(data)
    for x in res:
        print(x)


# 模拟post请求
post_url = 'http://www.iqianyue.com/mypost'
post_data = urllib.parse.urlencode({'name':'asdasd', 'pass':'1123'}).encode('utf-8')
url = urllib.request.Request(post_url, post_data)
data = urllib.request.urlopen(url).read().decode('utf-8')
print(data)


# 爬虫的异常处理
try:
    pass
except urllib.error.HTTPError as e:
    if hasattr(e, 'code'):
        print(e.code)
    if hasattr(e, 'reason'):
        print(e.reason)


'''伪装浏览器'''
# 要爬取的网站
url = 'https://www.zhihu.com/'
# 设置请求报头，头文件格式 headers = ('User-Agent', 用户具体代理值)
headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5558.400 QQBrowser/10.1.1695.400")
# 创建一个opener
opener = urllib.request.build_opener()
# 将headers添加到opener中
opener.addheaders = [headers]
# 用opener.open()打开网页
data = opener.open(url).read().decode('utf-8')
print(len(data))

'''上面伪装浏览器的代码优化'''
# 要爬取的网站
url = 'https://www.zhihu.com/'
# 设置请求报头，头文件格式 headers = ('User-Agent', 用户具体代理值)
headers = ("User-Agent", "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.26 Safari/537.36 Core/1.63.5558.400 QQBrowser/10.1.1695.400")
# 创建一个opener
opener = urllib.request.build_opener()
# 将headers添加到opener中
opener.addheaders = [headers]
# 将opener安装为全局
urllib.request.install_opener(opener)
# 用opener.open()打开网页
data = opener.open(url).read().decode('utf-8')
print(len(data))


