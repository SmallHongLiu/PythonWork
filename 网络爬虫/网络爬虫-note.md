# 爬虫准备工作
- 参考资料
    - python网络数据采集，图灵工业出版社
    - 精通Python爬虫框架Scrapy，人民邮电出版社
    
- 前提知识
    - url
    - http协议
    - web前端, html, css, js
    - ajax
    - re, xpath
    - xml
    
# 1. 爬虫简介
- 爬虫定义：网络爬虫（又称网页蜘蛛，网络机器人，在FOAF社区中间，更经常的称为网页追逐者），是一种按照一定的规则，自动的抓取万维网信息的程序或者脚本
- 两大特征
    - 能按作者要求下载数据或者内容
    - 能自动在网络上流窜
    
- 三大步骤：
    - 下载网页信息
    - 提取正确的信息
    - 根据一定规则自动跳到另外的网页上执行以上两步内容，依次类推
    
- 爬虫的分类
    - 通用爬虫
    - 专用爬虫（聚焦爬虫）
    
- Python网络包简介
    - Python 2.x: urllib, urllib2, urllib3, httplib, httplib2, requests
    - Python 3.x: urllib, urllib3, httplib2, request
    - python2: urllib + urlib2配合使用，或者request
    - python3: urllib + request
    
# 2. urllib
- 包含模块
    - urllib.request: 打开和读取urls
    - urllib.error: 包含urllib.request产生的常见的错误，使用try捕捉
    - urllib.parse: 包含解析url的方法
    - urllib.robotparse: 解析robots.txt文件
    
- 网页编码问题解决
    - charset：可以自动检测页面文件的编码格式，但是，可能存在问题
    - 需要按照，conda install chardet
    
- urlopen的返回对象
    - geturl: 返回请求对象的url
    - info: 请求反馈对象的meta信息
    - getcode: 返回的http code
- request.data的使用
    - 访问网络的两种方法
        - get
            - 利用参数给服务器传递信息
            - 参数为dict， 然后用parse编码
        - post
            - 一般向服务器传递参数使用
            - post是把信息自动加密处理
            - 我们如果想使用post信息，需要用到data参数
            - 使用post，意味着http的请求头可能需要更改：
                - Content-Type: application/x-www.form-urlencode
                - Content-Length: 数据长度
                - 简而言之，一旦更改请求方法，请注意其它请求头部信息相适应
            - urllib.parse.urlencode可以将字符串自动转换为上面需要的格式
            - 为了更多的设置请求信息，单纯的通过urlopen函数已经不太好用了
            - 需要利用request.Request类
            
            
- urllib.error
    - URLError产生的原因：
        - 没网
        - 服务器链接失败
        - 找不到指定服务器
        - 是OSError的子类
    - HTTPError，是URLError的一个子类
    
    - 两者的区别：
        - HTTPError是对应的HTTP请求的返回码错误，如果返回错误码是400以上的，则引发HTTPError
        - URLError对应的一般则是网络出现问题，包括url问题
        - 关系区别：OSError - URLError - HTTPError
        
- UserAgent
    - UserAgent：用户代理，简称UA，属于Header的一部分，服务器通过UA来判断访问者身份
    - 常见的UA值，使用的时候可以直接复制粘贴，也可以用浏览器访问的时候抓包
    - 设置UA可以通过两种方式
        - headers
        - add_header
    
- ProxyHandler处理（代理服务器）
    - 使用代理IP，是拍从的常用手段
    - 获取代理服务器的地址   
        - www.xicidaili.com
        - www.goubanjia.com
    - 代理用来隐藏真实访问中，代理也不允许频繁访问某一个固定网站，所以，代理一定要很多很多
    - 基本使用步骤
        1. 设置代理地址
        2. 创建ProxyHandler
        3. 创建Opener
        4. 安装Opener
        
- cookie & session
    - 由于http协议的无记忆性，人们为了弥补这个缺憾，所采用的一个补充协议
    - cookie是发放给用户（即http浏览器）的一段信息，色色死哦你是保存在服务器上的对应的另一半信息，用来记录用户信息
- cookie后色色死哦你的区别
    - 存放位置不同
    - cookie不安全
    - 色色死哦你会保存在服务器上一定时间，会过期
    - 单个cookie保存数据不超过4k，很多浏览器限制一个站点最多保存20个
    
- session的存放位置
    - 存在服务器端
    - 一般情况下，session是放在内存中或者数据库中
    - 没有cookie登录
    
- 使用cookie登录
    - 直接把cookie复制下来，然后手动放入请求头
    - http模块包含一些关于cookie的模块，通过他们可以自动使用cookie
        - CookieJar
            - 管理存储cookie，向传出的http请求添加cookie
            - cookie存储在内存中，CookieJar实例回收后cookie将消失
        - FileCookieJar（filename, delayload=None, policy=None)
            - 使用文件管理cookie
            - filename是保存cookie的文件
        - MozillaCookieJarr（filename, delayload=None, policy=None)
            - 创建与mocilla浏览器cookie.txt兼容的FileCookieJar实例
        - LwpCookieJarr（filename, delayload=None, policy=None)
            - 创建与libwww-perl标准兼容的Set-Cookie3格式的FileCookieJar实例
        - 它们之间的关系：CookieJar --> FileCookieJar --> MozillaCookieJar & LwpCookieJar
        
        - 自动使用cookieJar登录的大致流程：
            - 打开登录页面后自动通过用户名密码登录
            - 自动提取反馈回来的cookie
            - 利用提取的cookie登录隐私页面
        - handler是Handler的实例，常用的有
            - cookie_handler
            - http_handler
            - https_handler
        - 创立handler后，使用opener打开，打开后相应的业务由相应的handler处理
        - cookie作为一个变量，打印出来
            - cookie的属性
                - name: 名称
                - value: 值
                - domain: 可以访问此cookie的域名
                - path: 剋呀访问此cookie的页面路径
                - expires: 过期时间
                - size: 大小
                - Http字段
                
        - cookie的保存-FileCookieJar
        - cookie的读取
        
- SSL
    - SSL证书就是指遵守SSL安全套阶层协议的服务器数字证书（SecureSocketLayer）
    - 美国网景公司开发
    - CA（CertificateAuthority）是数字证书认证中心，是发放,管理,废除数字证书的收信人的第三方机构
    - 遇到不信任的SSL证书，需要单独处理，
    
- js加密
    - 有的反爬虫策略采用js对需要传输的数据进行加密处理（通常是取md5值）
    - 经过加密，传输的就是密文
    - 加密函数或者过程一定是在浏览器完成，也就是一定会把代码（js代码）暴露给使用者
    - 通过阅读加密算法，就可以模拟出加密过程，从而达到破解
    
- ajax
    - 异步请求
    - 一定会有url，请求方法，可能有数据
    - 一般使用json格式
    
# Requests - 献给人类
- HTTTP for Humans, 更简洁友好
- 继承了urllib的所有特性
- 底层使用的是urllib3
- 开源地址：https://github.com/requests/requests
- 中文文档：http://docs.python-request.org/zh_CN/latest/index.html
- get请求
    - requests.get(url)
    - requests.request('get', url)
    - 可以带有header和params参数
- get返回内容

- post
    - rsp = requests.post(url, data=data) ，post就是为了发送数据，所以有一个data参数
    
- proxy  代理
    proxies = {
        'http': 'address of proxy',
        'https': 'address of proxy'
    }
    
    rsp = requests.request('get', 'http:xxxxxx', proxies=proxies)
    
    - 代理可能报错，如果使用人数多，考虑安全问题，则可能被强行关闭
    
- 用户验证
    - 代理验证
        # 可能需要使用HTTP basic auth
        # 格式为  用户名:密码@代理地址: 端口地址
        proxy = {'htp": 'china:123456@192.168.1.123:4444'}
        rsp = requests.get('http://baidu.com'. proxies=proxy)
        
- web 客户端验证
    - 如果遇到web客户端验证，需要添加auth=（用户名，密码）
        auth = ('test', '12345') # 授权信息
        rsp = requests.get('http://www.baidu.com', auth=auth)
        
- cookie
    - requests可以自动处理cookie信息
    
             rsp = requests.get('http://www.baidu.com')
             # 如果对方服务器给传送过来cookie信息，则可以通过反馈的cookie属性得到
             # 返回一个cookiejar案例
             cookiejar = rsp.cookies
             
             # 可以请cookiejar转换成字典
             cookiedict = requests.utils.dict_from_cookiejar(cookiejar)
             
- session
    - 跟服务器session不是一个东西
    - 模拟一次会话，从客户端浏览器链接服务器开始，到客户端浏览器断开
    - 能让我们跨请求保持某些参数，比如在同一个session实例发出的所有请求之间保持cookie
    
        # 创建session对象，可以保持cookie值
        ss = requests.session()
        
        headers = {'User-Agent': '......'}
        
        data = {'name': '......'}
        
        # 此时，由创建的session管理请求，负责发出请求
        ss.post('http:www.baidu.com', data=data, headers=headers)
        
        rsp = ss.get('......')
    
- https请求验证ssl证书
    - 参数verity负责表示是否需要验证ssl证书，默认是true
    - 如果不需要验证ssl证书，则设置成false表示关闭
    
        rsp = requests.get('http://www.baidu.com', verity=False)
        # 如果用verify=True访问12306，会报错，因为它证书有问题
        
    
# 页面解析和数据提取
- 结构化数据：先有结构，再谈数据
    - json文件
        - json path
        - 转换成python类型进行操作（json类）
    - xml文件
        - 转换为python类型（xml to dict)
        - XPath
        - CSS选择器
        - 正则
- 非结构化数据：先有数据，再谈结构
    - 文本
    - 电话号码
    - 邮件地址
    - 通常处理此类数据，使用正则表达式
    - Html文件
        - 正则
        - XPath
        - CSS选择器
        
# 正则表达式
- 一套规则，可以在字符串文本中进行搜索替换等
- 正则常用方法：
    - match：从开始位置开始查找，一次匹配
    - search：从任何位置查找，一次匹配
    - findall：全部匹配，返回列表
    - finditer：全部匹配，返回迭代器
    - spilt：分割字符串，返回列表
    - sub：替换
- 匹配中文
    - 中文unicode范围主要在[u4e00 - u9fa5]
    
- 贪婪与非贪婪模式
    - 贪婪模式：在整个表达式匹配成功的前提下，尽可能多的匹配
    - 非贪婪模式：在整个表达式匹配成功的前提下，尽可能少的匹配
    - python中数量词默认是贪婪模式
    - 例如：
    - 查找文本abbbbbbbccc
    - re是 ab*
    - 贪婪模式：结果是abbbbbb
    - 非贪婪模式：结果是a
    
# XML
- XML(ExtensibleMarkupLanguage)
- 概念：父节点，子节点，先辈节点，兄弟节点，后代节点 

# XPath
- XPath（XML Path Language), 是一门在xml文档中查找信息的语言
- XPath开发工具
    - 开源的XPath表达式工具: XMLQuire
    - chrome插件：XPath Helper
    - Firefox插件：XPath Checker
    
- 常用路径表达式
    - nodename：选取此节点的所有子节点
    - /：从根结点开始选
    - //：选取元素，而不考虑元素的具体位置
    - .：当前节点
    -..：父节点
    - @：选取属性
    
- 谓语（Predicates)
    - 谓语用来查找某个特定的节点，被镶嵌在方括号中
    - 例如：/bookstore/book[1]: 选取第一个属于bookstore下叫book的元素，这里[1]就是谓语
    
- 通配符
    - '*'：任何元素节点
    - @*：匹配任何属性节点
    - node()：匹配任何类型的节点
- 选取多个路径
    - //book/title | //book/author：选取book元素中的title和author元素
    - //title | price：选取文档中所有的title和price元素
    
# lxml库
- python的HTML/XML的解析器
- 作用    
    - 解析HTML
    - 文件读取
    
# CSS选择器 BeautifulSoup4
- 现在使用BeautifulSoup4
- 官网地址：http://beautifulSoup.readthedocs.io/zh_CN/v4.4.0/
- 几个常用提取信息工具的比较
    - 正则：很快，不好用，不需安装
    - beautifulSoup：慢，使用简单，安装简单
    - lxml：比较快，使用简单，安装一般
    
- 四大对象
    - Tag
    - NavigableString
    - BeautifulSoup
    - Comment
- Tag
    - 对应html中的标签
    - 可以通过soup.tag_name获取
    - tag两个重要属性
        - name
        - attrs
- NavigableString
    - 对应内容值
- BeautifulSoup
    - 表示的是一个文档的内容，大部分可以把它当作tag对象
    - 一般我们可以用soup表示
- Comment
    - 特殊类型的NavigableString对象
    - 对其输出，则内容不爆扣注释内容
- 遍历文档对象
    - contents：tag的子节点以列表的方式给出
    - children：子节点以迭代器形式返回
    - descendants：所有子孙节点
    - string
- 搜索文档
    - find_all(name, attrs, recursive, text, ** kwargs)
        - name：按照那个字符串搜索，可以传入的内容为
            - 字符串
            - 正则表达式
            - 列表
        - keyword参数：可以用来表示属性
        - text：对应tag的文本值
        
- css选择器
    - 使用soup.select, 返回一个列表
    - 通过标签名：soup.select('title')
    - 通过类名：soup.select('.content')
    - id查找：soup.select('#name_id')
    - 组合查找：soup.select('div #input_content')
    - 属性查找：soup.select('img[class="photo"]')
    - 获取tag内容：tag.get_text
    
# 动态html

## 爬虫跟反爬虫

## 动态html介绍
- JavaScript
- jQuery
- Ajax
- DHTML
- Python采集动态数据
    - 从JavaScript代码入手采集
    - python第三方库运行JavaScript，直接采集你在浏览器看到的页面
    
## Selenium + PhantomJS
- Selenium: web自动化测试工具
    - 自动加载页面
    - 获取数据
    - 截屏
- PhantomJS（幽灵）
    - 基于Webkit的无界面的浏览器
- Selenium库有一个WebDriver的API
- WebDriver可以跟页面上的元素进行各种交互，用它可以来进行爬取

- chrome + chromedriver

- Selenium操作主要分为两大类：
    - 得到UI元素
        - find_element_by_id
        - ......
    - 基于UI元素操作的模拟
        - 单击
        - 右键
        - 拖拽
        - 输入
        - 可以通过导热油ActionsChains类来做到
        
# 验证码问题
- 验证码：防止机器人或者爬虫
- 分类：
    - 简单图片
    - 极验，官网www.geetest.com
    - 12306
    - 电话
    - Google验证
    
- 验证码破解：
    - 通用方法：
        - 下载网页和验证码
        - 手动输入验证号码
    - 简单图片
        - 使用图像识别软件或者文件识别软件
        - 可以使用第三方图像验证码破解网站， www.chaojiying.com
    - 极验
        - 破解比较麻烦
        - 可以模拟鼠标等移动
        - 一直在进化
    - 12306
    - 电话
    - Google验证
    
# Tesseract
- 机器视觉领域的基础软件
- OCR：OpticalCharacterRecognition，光学文字识别
- Tesseract: 一个ocr库，有Google赞助


    
    


    


    
    
    