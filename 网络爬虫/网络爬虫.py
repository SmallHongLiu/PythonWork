'''请求一个网页并打印内容'''

from urllib import request

if __name__ == '__main__':
    url = ''
    # 打开相应url并把相应页面作为返回
    rsp = request.urlopen(url)
    # 把返回结果读取出来
    # 读取出来内容类型为bytes
    html = rsp.read()
    print(type(html))

    # 如果想把bytes内容转换为字符串，则需要解码
    html = html.decode()
    print(html)


'''
利用request下载页面
自动检测
'''

import urllib
import chardet

if __name__ == '__main__':
    url = ''

    rsp = urllib.request.urlopen(url)

    html = rsp.read()

    # 利用chardet自动检测
    cs = chardet.detect(html)
    print(type(cs))
    print(cs)

    # 使用get取值保证不会出错，参数二表示没有时，默认使用utf-8
    html = html.decode(cs.get('encoding', 'utf-8'))
    print(html)



'''

'''
import urllib
import chardet

if __name__ == '__main__':
    url = ''

    rsp = urllib.request.urlopen(url)
    print(type(rsp))
    print(rsp)

    print('URL: {0}'.format(rsp.geturl))
    print('Info: {0}'.format(rsp.info()))
    print('Code: {0}'.format(rsp.getcode()))

    html = rsp.read()

    # 使用get取值保证不会出错，参数二表示没有时，默认使用utf-8
    html = html.decode(cs.get('encoding', 'utf-8'))
    print(html)


'''
掌握对url进行参数编码的方法
需要使用parse模块
'''
from urllib import request, parse
if __name__ == '__main__':
    url = 'http://www.baidu.com/s?'
    wd = input('Input your keyword:')

    # 要想使用data，需要使用字典结构
    qs = {
        'wd': wd
    }

    # 转换url编码
    qs = parse.urlencode(qs)
    print(qs)

    fullurl = url + qs
    print(fullurl)

    # 如果直接用可读的带参数的url，是不能访问的，如：fullurl='http://www.baidu.com/s?wd=大熊猫'
    rsp = request.urlopen(fullurl)

    html = rsp.read()

    # 使用get取值保证不会出错，参数二表示没有时，默认使用utf-8
    html = html.decode()
    print(html)


'''
利用parse模块模拟post请求
分析百度词典
分析步骤：
1. 打开F12
2. 尝试输入单词girl, 发现每敲打一个字母后都有请求
3. 请求地址是：http://fanyi.baidu.com/sug
4. 利用Network-All-Headers  查看   发现FormData的值是kw.girl
5. 检查返回内容格式，发现返回的是json格式内容  -->  需要用到json包
'''


from urllib import request, parse
import json
'''
1. 利用data构造呢绒，然后urlopen打开
2. 返回一个json格式的结果
3. 结果就应该是girl的释义
'''

baseurl = 'http://fanyi.baidu.com/sug'

# c存放用来模拟form的数据一定是dict格式
data = {
    # girl是编译输入的英文内容，应该由用户输入，此处使用硬编码
    'kw': 'girl'
}

# 需要使用parse模块对data进行编码, 注意：urlencode之后是str类型，而需要的是bytes，所以需要再次编码
data = parse.urlencode(data).encode()

# 构造一个请求头，请求头部应该至少包含传入的数据的长度
# request要求传入的请求头是一个dict格式
headers = {
    # 因为使用post，至少应该包含content-length字段, 注意区分大小写
    'Content-Length': len(data)
}

# 发出请求
rsp = request.urlopen(baseurl, data=data)

json_data = rsp.read().decode('utf-8')
print(type(json_data))
print(json_data)

# 把json字符串转化为字典
json_data = json.loads(json_data)
print(type(json_data))
print(json_data)

for item in json_data['data']:
    print(item['k'], item['v'])


'''
使用request.Request
'''
baseurl = 'http://fanyi.baidu.com/sug'

# c存放用来模拟form的数据一定是dict格式
data = {
    # girl是编译输入的英文内容，应该由用户输入，此处使用硬编码
    'kw': 'girl'
}

# 需要使用parse模块对data进行编码, 注意：urlencode之后是str类型，而需要的是bytes，所以需要再次编码
data = parse.urlencode(data).encode()

# 构造一个请求头，请求头部应该至少包含传入的数据的长度
# request要求传入的请求头是一个dict格式
headers = {
    # 因为使用post，至少应该包含content-length字段, 注意区分大小写
    'Content-Length': len(data)
}

# 构造一个Request的实例
req = request.Request(url=baseurl, data=data, headers=headers)

# 因为已经构造了一个Request的请求实例，则所有的请求信息都可以封装在Request实例中
rsp = request.urlopen(req)

json_data = rsp.read().decode('utf-8')
print(type(json_data))
print(json_data)

# 把json字符串转化为字典
json_data = json.loads(json_data)
print(type(json_data))

for item in json_data['data']:
    print(item['k'], item['v'])
print(json_data)


'''
URLError的使用
'''

from urllib import request, error

if __name__ == '__main__':
    url = 'http://www.baidu.com'

    try:
        # 构造request
        req = request.Request(url)
        # 请求
        rsp = request.urlopen(req)
        # 解析html
        html = rsp.read.decode()
        print(html)
    except error.URLError as e:
        print('URLError: {0}'.format(e.reason))
        print('URLError: {0}'.format(e))
    except Exception as e:
        print(e)



'''
HTTPError的使用
'''
if __name__ == '__main__':
    url = 'http://www.baidu.com'

    try:
        # 构造request
        req = request.Request(url)
        # 请求
        rsp = request.urlopen(req)
        # 解析html
        html = rsp.read.decode()
        print(html)
    except error.HTTPError as e:
        print('HTTPError: {0}'.format(e.reason))
        print('HTTPError: {0}'.format(e))
    except error.URLError as e:
        print('URLError: {0}'.format(e.reason))
        print('URLError: {0}'.format(e))
    except Exception as e:
        print(e)



'''
访问一个网址
更改自己的UserAgent进行伪装
'''
from urllib import request, error

if __name__ == '__main__':
    url = 'http://www.baidu.com'

    try:
        # 方法1：使用header方法伪装UA
        headers = {}
        headers['User-Agent'] = '......'
        req = request.Request(url, headers=headers)

        # 方法2：使用add_header方法
        req = request.Request(url)
        req.add_header('......')

        # 正常访问
        rsp = request.urlopen(req)
        html = rsp.read().decode()
        print(html)

    except error.HTTPError as e:
        print(e)
    except error.URLError as e:
        print(e)
    except Exception as e:
        print(e)




'''
使用代理访问百度
'''
from urllib import request, error

if __name__ == '__main__':
    url = 'http://www.baidu.com'

    # 使用代理步骤
    # 1. 设置代理地址
    proxy = {'http': '120:194.18:81'}
    # 2. 创建ProxyHandler
    proxy_handler = request.ProxyHandler(proxy)
    # 3. 创建Opener
    opener = request.build_opener(proxy_handler)
    # 4. 安装Opener
    request.install_opener(opener)

    # 现在如果访问url，则使用代理服务器
    try:
        rsp = request.urlopen(url)
        html = rsp.read().decode()
        print(html)
    except Exception as e:
        print(e)




'''
没有cookie的案例
'''
from urllib import request
if __name__ == '__main__':
    url = 'http://www.renren.com/965187997/profile'

    rsp = request.urlopen(url)

    html = rsp.read().decode()

    with open('rsp.html', 'w') as f:
        f.write(html)



'''
使用cookie的案例
'''
if __name__ == '__main__':
    url = 'http://www.renren.com/965187997/profile'

    headers = {
        'Cookie': '......'
    }

    req = request.Request(url, headers=headers)

    rsp = request.urlopen(req)

    html = rsp.read().decode()

    with open('rsp.html', 'w') as f:
        f.write(html)




'''
CookieJar案例
'''
from http import cookiejar
# 创建cookie
cookie = cookiejar.CookieJar()
# 生成cookie的管理器
cookie_handler = request.HTTPCookieProcessor(cookie)
# 创建http请求管理器
http_handler = request.HTTPHandler()
# 创建https管理器
https_handler = request.HTTPSHandler()
# 创建请求管理器
opener = request.build_opener(http_handler, https_handler, cookie_handler)

def login():
    '''
    负责初次登录
    需要输入用户名密码，用来获取登录cookie凭证
    :return:
    '''
    # 此url需要从登录form的action属性中提取
    url = 'http://www.renren.com/PLogin.do'

    # 此键值需要从登录form的两个对应input中提取name属性
    data = {
        'email': '13119144223',
        'password': '123456'
    }

    # 把数据进行编码
    data = parse.urlencode(data)

    # 创建一个请求对象
    req = request.Request(urllib, data=data.encode())

    # 使用opener发起请求
    rsp = opener.open(req)

def getHomePage():
    url = 'http://www.renren.com/965187997/profile'

    # 如果已经执行了login函数，则opener自动已经包含了相应的cookie值
    rsp = opener.open(url)

    # 保存cookie到文件
    # ignore_discard表示即使cookie将要被丢弃也要被保留下来
    # ignore_expires表示即使cookie已经过期了也要被保留下来
    cookie.save(ignore_discard=True, ignore_expires=True)

    html = rsp.read().decode()
    with open('rsp.html', 'w') as f:
        f.write(html)
if __name__ == '__main__':
    login()
    print(cookie)
    for item in cookie:
        print(type(item))
        print(item)
        for i in dir(item):
            print(i)
    getHomePage()



'''
cookie的读取
'''
# 读取保存的cookie
cookie = cookiejar.MozillaCookieJar()
cookie.load('cookie.txt', ignore_discard=True, ignore_expires=True)
# 生成cookie的管理器
cookie_handler = request.HTTPCookieProcessor(cookie)
# 创建http请求管理器
http_handler = request.HTTPHandler()
# 创建https管理器
https_handler = request.HTTPSHandler()
# 创建请求管理器
opener = request.build_opener(http_handler, https_handler, cookie_handler)

def getHomePage():
    url = 'http://www.renren.com/965187997/profile'

    # 如果已经执行了login函数，则opener自动已经包含了相应的cookie值
    rsp = opener.open(url)

    html = rsp.read().decode()
    with open('rsp.html', 'w') as f:
        f.write(html)

if __name__ == '__main__':
    getHomePage()


'''
忽略不信任证书的案例
'''
# 导入python ssl处理模块
import ssl

# 创建非认证上下文环境铁环认证的上下文环境
ssl._create_default_https_context = ssl._create_unverified_context

url = 'https://www.12306.cn/mormhweb/'
rsp = request.urlopen(url)

html = rsp.read().decode()

print(html)

'''
js破解有道词典
'''
from urllib import request, parse

def youdao(key):
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    data = {
        '1': 'girl',
        'from': 'AUTO',
        'to': 'AUTO',
        'smartreuslt': 'dict',
        'client': 'fanyideskweb',
        'salt': '1523100789'
    }



'''
爬取豆瓣的电影数据
ajax的案例
'''
from urllib import request
import json

url = 'https://movie.douban.com/j/chart/top_list?type=11&interval_id=......'

rsp = request.urlopen(url)
data = rsp.read().decode()

data = json.loads(data)
print(data)

'''
Request案例
'''
import requests

url = 'http://www.baidu.com'
# 两种请求方式
# 方法1：使用get请求
rsp = requests.get(url)
print(rsp.text)

# 方法2：使用request请求
rsp = requests.request('get', url)
print(rsp.text)

'''
使用参数headers和params
'''

# 完整访问url是下面url加上参数构成
url = 'http://www.baidu.com/s?'

kw = {
    'kw': 'SmallHong'
}

headers = {
    'User-Agent': '......'
}

rsp = requests.get(url, params=kw, headers= headers)

print(rsp.text)
print(rsp.content)
print(rsp.url)
print(rsp.encoding)
print(rsp.status_code) # 请求返回码

'''
post案例
'''
import requests
from urllib import parse
import json

baseurl = 'http://'

data = {
    'kw': 'girl'
}

headers = {
    'Content-Length': str(len(data))
}

rsp = requests.post(baseurl, data=data, headers=headers)
print(rsp.text)
print(rsp.json())


'''
正则结果Match的使用案例
'''
import re

# 以下正则分成了两个组，以小括号为单位
S = r'([a-z]+) ([a-z]+)'

pattern = re.compile(S, re.I)  # s.I表示忽略大小写

m = pattern.match('Hello world wide web')

# group(0)表示返回匹配成功的整个子串
s = m.group(0)

print(s)

a = m.span(0)  #返回匹配成功的 这个那个子串的跨度
print(s)

# group（1）表示返回的第一个分组匹配成功的子串
s = m.group(1)
print(s)

a = m.span(1)  #返回匹配成功的第一个子串的跨度
print(a)

# 等价于m.group(1), m.group(2)......
s = m.groups()
print(s)


'''
search案例
'''

import re

s = r'\d+'

pattern = re.compile(s)

m = pattern.search('one12two34three56')
print(m.group())

m = pattern.search('one12two34three56', 10, 40)
print(m.group())


'''
findall案例
'''
import re

pattern = re.compile(r'\d+')

s = pattern.findall('i am 18 years old and 185 high')

print(s)

'''
中文unicode案例
'''
import re

hello = u'你好，世界'

pattern = re.compile(r'[\u4e00-\u9fa5]+')

m = pattern.findall(hello)


'''
lxml库
'''
from lxml import etree

'''
用其解析HTML代码
'''
text = '''
<div>
    <ul>
        <li class='item-0'> <a href='0.html'> first item </a></li>
        <li class='item-1'> <a href='1.html'> first item </a></li>
        <li class='item-2'> <a href='2.html'> first item </a></li>
        <li class='item-3'> <a href='3.html'> first item </a></li>
        <li class='item-4'> <a href='4.html'> first item </a></li>
        <li class='item-5'> <a href='5.html'> first item </a></li>
    </ul>
</div>
'''
# 利用etree.HTML把字符串解析成HTML文档
html = etree.HTML(text)
s = etree.tostring(html)
print(s)

'''
用其读取文件
'''
# 只能读取xml格式的文件
html = etree.parse('./test.html')

rst = etree.tostring(html, pretty_print=True)
print(rst)


'''
entree和XPath的配合使用
'''
# 只能读取xml格式的文件
html = etree.parse('./test.html')
print(type(html))

rst = html.xpath('//book')
print(type(rst))
print(rst)

# xpath的意识是，查找带有category属性值为sport的book元素
rst = html.xpath('//book[@category="sport"]')
print(type(rst))
print(rst)

# xpath的意识是，查找带有category属性值为sport的book元素下的year元素
rst = html.xpath('//book[@category="sport"]/year')
rst = rst[0]
print(type(rst))
print(rst.tag)
print(rst.text)

rst = etree.tostring(html, pretty_print=True)
print(rst)


'''
beautifulSoup4的案例
'''
from urllib import request
from bs4 import BeautifulSoup

url = 'http://www.baidu.com'

rsp = request.urlopen(url)
content = rsp.read()

soup = BeautifulSoup(content, 'lxml')

# bs自动转码
content = soup.prettify()
print(content)

'''
通过BeautifulSoup4获取tag
'''
print('==' * 12)
print(soup.head)

print('==' * 12)
print(soup.meta)

print('==' * 12)
print(soup.link)
print(soup.link.name)
print(soup.link.attrs)
print(soup.link.attrs['type'])

print('==' * 12)
print(soup.name)
print(soup.attrs)

'''
遍历文档对象
'''
print('==' * 12)
for node in soup.head.contents:
    print(node)
    if node.name == 'title':
        print('title node')

'''
搜索文档
'''
print('==' * 12)
tags = soup.find_all(name='meta')
tags = soup.find_all(re.compile('^me'))  # 查找以me开头的标签
print(tags)

'''
查找案例
'''
print('==' * 12)
titles = soup.select('title')
print(titles[0])

print('==' * 12)
metas = soup.select('meta[content="always"]')
print(metas[0])


'''
通过WebDriver操作
'''
from selenium import webdriver
import time

# 通过keys模拟键盘
from selenium.webdriver.common.keys import Keys

# 操作哪个浏览器就对哪个浏览器建一个实例
# 自动按照环境变量查找对应的浏览器
driver = webdriver.PhantomJS()

# 如果浏览器没有在相应环境变量中，需要指定浏览器位置

driver.get('http://www.baidu.com')

# 通过函数查找title标签
print('Title: {0}'.format(driver.title))


# 可能需要手动添加路径
driver = webdriver.Chrome()

url = 'http://www.baidu.com'

driver.get(url)

text = driver.find_element_by_id('wrapper').text
print(text)
print(driver.title)
# 得到页面的快照（截图）
driver.save_screenshot('index.png')

# id='kw'的百度的输入框，我们得到输入框的UI元素后直接输入'大熊猫'
driver.find_element_by_id('kw').send_keys(u'大熊猫')

# id='su'是百度搜索的按钮，click模拟点击
driver.find_element_by_id('su').click()

time.sleep(5)

driver.save_screenshot('大熊猫.png')

# 获取当前页面的cookie
print(driver.get_cookies())

# 模拟输入两个按键 ctrl + a
driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'a')

# ctrl + x 是剪切的快捷键
driver.find_element_by_id('kw').send_keys(Keys.CONTROL, 'x')

driver.find_element_by_id('kw').send_keys(u'航空母舰')
driver.save_screenshot('航空母舰.png')

driver.find_element_by_id('su').send_keys(Keys.RETURN)

time.sleep(5)
driver.save_screenshot('航空母舰2.png')

# 关闭浏览器
driver.quit()


import pytesseract as pt

from PIL import Image

# 生成图片实例
image = Image.open('......')

# 调用pytesseract，把图片转换成文字
# 返回结果就是转换后的结果
text = pt.image_to_string(image)
print(text)


