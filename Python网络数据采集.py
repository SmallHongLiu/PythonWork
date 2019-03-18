from urllib.request import urlopen
from bs4 import BeautifulSoup

"""
html = urlopen('http://www.pythonscraping.com/pages/page1.html')
bsObj = BeautifulSoup(html.read())
print(bsObj.h1)

'''
处理异常
'''
try:
    html = urlopen('http://www.pythonscraping.com/pages/page1.html')
except HTTPError as e:
    print(e)
    # 返回控制，中断程序，或者执行另一个方案
else:
    # 程序继续，注意：如果你已经在上面异常捕捉那一段代码里返回或中断（break）
    # 那么就不需要使用else语句了，这段代码也不会执行

if html is None:
    print('URL is no found')
else:
    # 程序继续执行

try:
    badContent = bsObj.nonExistingTag.anotherTag
except AttributeError as e:
    print('Tag was not found')
else:
    if badContent == None:
        print('Tag was not found')
    else:
        print(badContent)

'''
上面代码块的综合写法
'''
def getTitle(url):
    try:
        html = urlopen(url)
    except HTTPError as e:
        return None
    try:
        bsObj = BeautifulSoup(html.read())
        title = bsObj.body.h1
    except AttributeError as e:
        return None
    return title

title = getTitle('http://www.pythonscraping.com/pages/page1.html')
if title == None:
    print('Title could not be found')
else:
    print(title)

html = urlopen('http://www.pythonscraping.com/pages/warandpeace.html')
bsObj = BeautifulSoup(html)
nameList = bsObj.findAll('span', {'class': 'green'})
for name in nameList:
    print(name.get_text())



'''
只查找子标签
'''
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bsObj = BeautifulSoup(html)

# for child in bsObj.find('table', {'id': 'giftList'}).children:
    # print(child)

for sibling in bsObj.find('table', {'id': 'giftList'}).tr.next_siblings:
    print(sibling)


'''
父标签处理
'''
html = urlopen('http://www.pythonscraping.com/pages/page3.html')
bsObj = BeautifulSoup(html)
print(bsObj.find('img', {'src': '../img/gifts/img1.jpg'}).parent.previous_sibling.get_text())

# 邮箱地址正则表达式
# [A-Za-z0-9\._+]+@[A-Za-z]+\.(com|org|edu|net)

'''
正则表达式的使用
'''
import re
# 这里匹配的是以 ../img/gifts/img 开头,以 .jpg 结尾
images = bsObj.findAll('img', {'src': re.compile('\.\.\/img\/gifts/img.*\.jpg')})
for image in images:
    print(image['src'])

'''
爬取维基百科
'''
html = urlopen("https://en.wikipedia.org/wiki/Kevin_Bacon")
bsObj = BeautifulSoup(html)
# for link in bsObj.findAll('a'):
#     if 'href' in link.attrs:
#         print(link.attrs['href'])

# 获取词条链接
import re
for link in bsObj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$')):
    if 'href' in link.attrs:
        print(link.attrs['href'])


'''
循环获取维基百科的词条链接
'''
import datetime
import random
import re

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("https://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    return bsObj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile('^(/wiki/)((?!:).)*$'))

links = getLinks('/wiki/Kevin_Bacon')
while len(links) > 0:
    newArticleUrl = links[random.randint(0, len(links) - 1)].attrs['href']
    print(newArticleUrl)
    links = getLinks(newArticleUrl)

import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("https://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    for link in bsObj.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 新页面
                newPage = link.attrs['href']
                print(newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks('')

import re

pages = set()
def getLinks(pageUrl):
    global pages
    html = urlopen("https://en.wikipedia.org"+pageUrl)
    bsObj = BeautifulSoup(html)
    try:
        print(bsObj.h1.get_text())
        print(bsObj.find(id='mw-content-text').findAll('p')[0])
        print(bsObj.find(id='ca-edit').find('span').find('a').attrs['href'])
    except AttributeError:
        print('页面缺少一些属性，不过不用担心')

    for link in bsObj.findAll('a', href=re.compile('^(/wiki/)')):
        if 'href' in link.attrs:
            if link.attrs['href'] not in pages:
                # 我们遇到了新页面
                newPage = link.attrs['href']
                print('-------------\n' + newPage)
                pages.add(newPage)
                getLinks(newPage)
getLinks('')

from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

pages = set()
random.seed(datetime.datetime.now())

# 获取页面所有内链的列表
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    # 找到所有以'/'开头的链接
    for link in bsObj.findAll('a', href=re.compile('^(/|.*"+includeUrl+")')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks

# 获取页面所有外链的列表
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    # 找出所有以'http'或'www'开头且不包含当前url的链接
    for link in bsObj.findAll('a', href=re.compile('^(http|www)((?!"+excludeUrl+").)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace('http://', '').split('/')
    return addressParts

def getRandomExternalLink(startingPage):
    html = urlopen(startingPage)
    bsObj = BeautifulSoup(html)
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    if len(externalLinks) == 0:
        internalLinks = getInternalLinks(startingPage)
        return getNextExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks) - 1)]

def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink('http://oreilly.com')
    print('随机外链是：' + externalLink)
    followExternalOnly(externalLink)

followExternalOnly('http://oreilly.com')

# 收集网站上发现的所有外链列表
allExtlinks = set()
allIntLinks = set()

def getAllExternalLinks(siteUrl):
    html = urlopen(siteUrl)
    bsObj = BeautifulSoup(html)
    internalLinks = getInternalLinks(bsObj, splitAddress(siteUrl)[0])
    externalLinks = getExternalLinks(bsObj, splitAddress(siteUrl)[0])
    for link in externalLinks:
        if link not in allExtlinks:
            allExtlinks.add(link)
            print(link)

    for link in internalLinks:
        if link not in allIntLinks:
            print("即将获取链接的URL是：" + link)
            allIntLinks.add(link)
            getAllExternalLinks(link)

getAllExternalLinks('http://oreilly.com')


from scrapy import Item, Field

class Article(Item):
    title = Field()

from scrapy.selector import Selector
from scrapy import Spider

class ArticleSpider(Spider):
    name = 'article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ["http://en.wikipedia.org/wiki/Main_Page",
                    "http://en.wikipedia.org/wiki/Python_%28programming_language%29"]

    def parse(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        print('Title is: ' + title)
        item['title'] = title
        return item

from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

class ArticleSpider(CrawlSpider):
    name='article'
    allowed_domains = ['en.wikipedia.org']
    start_urls = ["http://en.wikipedia.org/wiki/Python_%28programming_language%29"]
    rules = [Rule(SgmlLinkExtractor(allow=('(/wiki/)((?!:).)*$'),), callback="parse_item", follow=True)]

    def parse_item(self, response):
        item = Article()
        title = response.xpath('//h1/text()')[0].extract()
        print('Title is: ' + title)
        item['title'] = title
        return item

import json
def getCountry(ipAddress):
    try:
        response = urlopen("http://freegeoip.net/json/"+ipAddress).read().decode('utf-8')
    except HTTPError:
        return None
    responseJson = json.loads(response)
    return responseJson.get('country_code')

'''
下载指定网页的logo图片
'''
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://www.pythonscraping.com')
bsObj = BeautifulSoup(html)
imageLocation = bsObj.find('a', {'id': 'logo'}).find('img')['src']
urlretrieve(imageLocation, 'logo.jpg')

'''
下载某个网站的所有src属性的文件
'''
import os
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup

downloadDirectory = "downloaded"
baseUrl = "http://pythonscraping.com"

def getAbsoluteURL(baseUrl, source):
    if source.startswith('http://www.'):
        url = 'http://' + source[11:]
    elif source.startswith('http://'):
        url = source
    elif source.startswith('www.'):
        url = source[4:]
        url = 'http://' + source
    else:
        url = baseUrl + '/' + source

    if baseUrl not in url:
        return None
    return url

def getDownloadPath(baseUrl, absoluteUrl, downloadDirectory):
    path = absoluteUrl.replace('www.', '')
    path = path.replace(baseUrl, '')
    path = downloadDirectory + path
    directory = os.path.dirname(path)

    if not os.path.exists(directory):
        os.makedirs(directory)
    return path

html = urlopen('http://www.pythonscraping.com')
bsObj = BeautifulSoup(html)
downloadList = bsObj.findAll(src=True)

for download in downloadList:
    fileUrl = getAbsoluteURL(baseUrl, download['src'])
    if fileUrl is not None:
        print(fileUrl)

urlretrieve(fileUrl, getDownloadPath(baseUrl, fileUrl, downloadDirectory))

import csv

csvFile = open('../files/test.csv', 'w+')
try:
    writer = csv.writer(csvFile)
    writer.writerow(('number', 'number plus 2', 'number times 2'))
    for i in range(10):
        writer.writerow((i, i+2, i*2))
finally:
    csvFile.close()

import csv
from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen('http://en.wikipedia.org/wiki/Comparison_of_text_editors')
bsObj = BeautifulSoup(html)

# 主对比表格是当前页面上的第一个表格
table = bsObj.findAll('table', {'class': 'wikitable'})[0]
rows = table.findAll('tr')

csvFile = open("../files/editors.csv", 'wt', newline="", encoding='utf-8')
writer = csv.writer(csvFile)
try:
    for row in rows:
        csvRow = []
    for cell in row.findAll(['td', 'th']):
        csvRow.append(cell.get_text())
        writer.writerow(csvRow)
finally:
    csvFile.close()

'''
mysql数据库案例1
'''
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql')

cur = conn.cursor()
cur.execute('use scraping')

cur.execute('select * from pages where id=1')
print(cur.fetchone())
cur.close()
conn.close()

'''
mysql存储下载数据
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql', charset='utf8')

cur = conn.cursor()
cur.execute('use scraping')

random.seed(datetime.datetime.now())

def store(title, content):
    cur.execute('insert into pages (title, content) values (\"%s\", \"%s\")', (title, content))
    cur.connection.commit()

def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html)
    title = bsObj.find('h1').get_text()
    content = bsObj.find('div', {'id': 'mw-content-text'}).find('p').get_text()
    store(title, content)
    return bsObj.find('div', {'id': 'bodyContent'}).findAll('a', href=re.compile("^(/wiki/)((?!:).)*$"))

links = getLinks('/wiki/Kevin_Bacon')

try:
    while len(links) > 0:
        newArticle = links[random.randint(0, len(links) - 1)].attrs['href']
        print(newArticle)
        links = getLinks(newArticle)
finally:
    cur.close()
    conn.close()

'''
用python发送邮件
'''
import smtplib
from email.mime.text import MIMEText

msg = MIMEText('The body of the email is here')

msg['Subject'] = 'An Email Alert'
msg['From'] = '***@pythonscraping.com'
msg['To'] = '***@pythonscraping.com'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

'''
用python发送邮件的封装实现
'''
import smtplib
from email.mime.text import MIMEText
from bs4 import BeautifulSoup
from urllib.request import urlopen
import time

def sendMail(subject, body):
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = '***@pythonscraping.com'
    msg['To'] = '***@pythonscraping.com'

s = smtplib.SMTP('localhost')
s.send_message(msg)
s.quit()

bsObj = BeautifulSoup(urlopen('https://isitchristmas.com/'))
while(bsObj.find('a', {'id': 'answer'}).attrs['title'] == 'NO'):
    print('It is not Christmas yet.')
    time.sleep(3600)

bsObj = BeautifulSoup(urlopen('https://isitchristmas.com/'))
sendMail("It's Christmas!", 'According to http://itischristmas.com, it is Christmas!')

'''
从网上获取一个CSV文件
'''
from urllib.request import urlopen
from io import StringIO
import csv

data = urlopen("http://pythonscraping.com/files/MontyPythonAlbums.csv").read().decode('ascii', 'ignore')
dataFile = StringIO(data)
csvReader = csv.reader(dataFile)

for row in csvReader:
    print(row)


'''
把任意的PDF读成字符串，然后用StringIO转换成文件对象
'''
from urllib.request import urlopen
from pdfminer.pdfinterp import PDFResourceManager, process_pdf from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from io import StringIO
from io import open

def readPDF(pdfFile):
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, laparams=laparams)

    process_pdf(rsrcmgr, device, pdfFile)
    device.close()

    content = retstr.getvalue()
    retstr.close()
    return content

pdfFile = urlopen("http://pythonscraping.com/pages/warandpeace/chapter1.pdf")
outputString = readPDF(pdfFile)
print(outputString)
pdfFile.close()

'''
读取Microsoft Office文件的正文内容
'''
from zipfile import ZipFile
from urllib.request import urlopen
from io import BytesIO

wordFile = urlopen("http://pythonscraping.com/pages/AWordDocument.docx").read()
wordFile = BytesIO(wordFile)
document = ZipFile(wordFile)
xml_content = document.read('word/document.xml')
print(xml_content.decode('utf-8'))

wordObj = BeautifulSoup(xml_content.decode('utf-8'))
textStrings = wordObj.findAll('w:t')

for textElem in textStrings:
    print(textElem.text)

'''
2-gram的使用
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import string

def cleanInput(input):
    # 通过正则表达式移除转移字符(\n), 再把Unicode字符过滤掉
    input = re.sub('\n+', ' ', input)
    input = re.sub('\[[0-9]*\]', '', input)
    input = re.sub(' +', ' ', input)
    input = bytes(input, 'utf-8')
    input = input.decode('ascii', 'ignore')
    cleanInput = []
    input = input.split(' ')
    for item in input:
        item = item.strip(string.punctuation)
        if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):
            cleanInput.append(item)
    return cleanInput

def ngrams(content, n):
    input = cleanInput(input)
    output = []

    for i in range(len(input) - n + 1):
        output.append(input[i : i+n])
    return output

html = urlopen("http://en.wikipedia.org/wiki/Python_(programming_language)")
bsObj = BeautifulSoup(html)
content = bsObj.find('div', {'id': 'mw-content-text'}).get_text()
ngrams = ngrams(content, 2)
print(ngrams)
print('2-grams count is: ' + str(len(ngrams)))

'''
分析威廉 ·亨利 ·哈里森的就职演讲内容
'''
from urllib.request import urlopen
from random import randint

def wordListSum(wordList):
    sum = 0
    for word, value in wordList.items():
        sum += value
    return sum

def retrieveRandomWord(wordList):
    randIndex = randint(1, wordListSum(wordList))
    for word, value in wordList.items():
        randIndex -= value
        if randIndex <= 0:
            return word

def buildWordDict(text):
    # 剔除换行符和引号
    text = text.replace('\n', ' ')
    text = text.replace('\"', '')

    # 保证每个标点符号都和前面的单词在一起
    # 这样就不会被剔除，保留在马尔可夫链中
    punctuation = [',', '.', ', ', ';', ':']
    for symbol in punctuation:
        text = text.replace(symbol, ' ' + symbol + ' ')

    words = text.split(' ')
    # 过滤空单词
    words = [word for word in words if word != '']

    wordDict = {}
    for i in range(1, len(words)):
        if words[i - 1] not in wordDict:
            # 为单词新建一个词典
            wordDict[words[i - 1]] = {}
        if words[i] not in wordDict[words[i - 1]]:
            wordDict[words[i-1][words[i]]] = 0
        wordDict[words[i-1]][words[i]] = wordDict[words[i-1]][words[i]] + 1

    return wordDict

text = str(urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read(), 'utf-8')

wordDict = buildWordDict(text)

# 生成链长为100的马尔可夫链
length = 100
chain = ''
currentWord = 'I'

for i in range(0, length):
    chain += currentWord + ' '
    currentWord = retrieveRandomWord(wordDict[currentWord])

print(chain)

'''
广度优先搜索算法
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import pymysql

conn = pymysql.connect(host='127.0.0.1', unix_socket='/tmp/mysql.sock', user='root', passwd=None, db='mysql', charset='utf-8')
cur = conn.cursor()

cur.execute('use wikipedia')

class SolutionFound(RuntimeError):
    def __index__(self, message):
        self.message = message

    def getLinks(fromPageId):
        cur.execute('select toPageId from links where fromPageId = %s', (fromPageId))
        if cur.rowcount == 0:
            return None
        else:
            return [x[0] for x in cur.fetchall()]

    def constructDict(currentPageId):
        links = getLinks(currentPageId)

        if links:
            return dict(zip(links, [{}] * len(links)))
        return {}

    # 链接树要么为空，要么包含多个链接
    def searchDepth(targetPageId, currentPageId, linkTree, depth):
        if depth == 0:
            # 停止递归，返回结果
            return linkTree
        if not linkTree:
            linkTree = constructDict(currentPageId)
            if not linkTree:
                # 若此节点页面无链接，则跳过此节点
                return {}

        if targetPageId in linkTree.keys():
            print('Target ' + str(targetPageId) + 'found!')
            raise SolutionFound('Page: ' + str(currentPageId))

        for branchKey, branchValue in linkTree.items():
            try:
                # 递归建立链接树
                linkTree[branchKey] = searchDepth(targetPageId, branchKey, branchValue, depth - 1)
            except SolutionFound as e:
                print(e.message)
                raise SolutionFound('Page: ' + str(currentPageId))
        return linkTree

    try:
        searchDepth(134951, 1, {}, 4)
        print('No solution found')
    except SolutionFound as e:
        print(e.message)

'''
获取Ajax之后的内容
'''
from selenium import webdriver
import time

driver = webdriver.PhantomJS(executable_path='')
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()

'''
不断检查某个元素是否存在
'''
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.PhantomJS(executable_path='')
driver.get('http://pythonscraping.com/pages/javascript/ajaxDemo.html')
try:
    element = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'loadedButton')))
finally:
    print(driver.find_element_by_id('content').text)
    driver.close()

'''
检测重定向
'''
from selenium import webdriver
import time
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException

def waitForLoad(driver):
    elem = driver.find_element_by_tag_name('html')
    count = 0
    while True:
        count += 1
        if count > 20:
            print('Timing out after 10 seconds and returning')
            return
        time.sleep(.5)
        try:
            elem = driver.find_element_by_tag_name('html')
        except StaleElementReferenceException:
            return

driver = webdriver.PhantomJS(executable_path='<Path to Phantom Js>')
driver.get('http://pythonscraping.com/pages/javascript/redirectDemo1.html')
waitForLoad(driver)
print(driver.page_source)

'''
图像处理
'''
from PIL import Image, ImageFilter

kitten = Image.open('kitten.jpg')
blurryKitten = kitten.filter(ImageFilter.GaussianBlur)
blurryKitten.save('Kitten_blurred.jpg')
blurryKitten.show()

'''
图片清理
'''
from PIL import Image
import subprocess

def cleanFile(filePath, newFilePath):
    image = Image.open(filePath)

    # 对图片进行阀值过滤，然后保存
    image = image.point(lambda x: 0 if x < 143 else 255)
    image.save(newFilePath)

    # 调用系统的tesseract命令对图片进行OCR识别
    subprocess.call(['tesseract', newFilePath, 'output'])

    # 打开文件读取结果
    outputFile = open('output.txt', 'r')
    print(outputFile.read())
    outputFile.close()

cleanFile('text_2.jpg', 'text_2_clean.png')
"""

'''
从网站图片中抓取文字的案例
'''
import time
from urllib.request import urlretrieve
import subprocess
from selenium import webdriver

# 创建新的Selenium driver
driver = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
# 有时我发现PhantomJS查找元素有问题，但是Firefox没有
# 如果运行程序的时候出现问题，去掉下面这行注释
# 用Selenium调试FireFox浏览器
# driver = webdriver.Firefox()

driver.get('http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200')
time.sleep(2)

# 单击图书预览按钮
driver.find_element_by_id('sitbLogoImg').click()
imageList = set()

# 等待页面加载完毕
time.sleep(5)
# 当向右箭头可以点击时，开始翻页
while 'pointer' in driver.find_element_by_id('sitbReaderRightPageTurner').get_attribute('style'):
    driver.find_element_by_id('stibReaderRightPageTurner').click()
    time.sleep(2)

    # 获取已经加载的新页面（一次可以加载多个页面，但是重复的页面不能加载到集合中)
    pages = driver.find_element_by_xpath('//div[@class="pageImage"]/div/img')
    for page in pages:
        image = page.get_attribute('src')
        imageList.add(image)

driver.quit()

# 用Tesseract处理我们收集的图片URL连接
for image in sorted(imageList):
    urlretrieve(image, 'page.jpg')
    p = subprocess.Popen(['tesseract', 'page.jpg', 'page'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)

    p.wait()
    f = open('page.txt', 'r')
    print(f.read())

'''
用网络机器人破解验证码
'''
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import subprocess
import requests
from PIL import Image
from PIL import ImageOps

def cleanImage(imagePath):
    image = Image.open(imagePath)
    image = image.point(lambda x: 0 if x < 143 else 255)
    borderImage = ImageOps.expand(image, border=20, fill='white')
    borderImage.save(imagePath)

html = urlopen("http://www.pythonscraping.com/humans-only")
bsObj = BeautifulSoup(html)
# 收集许哟啊处理的表单数据（包括验证码和输入字段）
imageLocation = bsObj.find('img', {"title": 'Image CAPTCHA'})['src']
formBuildId = bsObj.find('input', {'name': 'form_build_id'})['value']
captchaSid = bsObj.find('input', {'name': 'captcha_sid'})['value']
captchaToken = bsObj.find('input', {'name': 'captcha_token'})['value']

captchaUrl = "http://pythonscraping.com"+imageLocation
urlretrieve(captchaUrl, 'captcha.jpg')
cleanImage('captcha.jpg')

p = subprocess.Popen(['tesseract', 'captcha.jpg', 'captcha'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
p.wait()
f = open('captcha.txt', 'r')

# 清理识别结果中的空格和换行符
captchaResponse = f.read().replace(' ', '').replace('\n', '')
print('Captcha solution attempt: ' + captchaResponse)

if len(captchaResponse) == 5:
    params = {'captcha_token': captchaToken, 'captcha_sid': captchaSid,
              'form_id': 'comment_node_page_form', 'form_build_id': formBuildId,
              'captcha_response': captchaResponse, 'name': 'Ryan Mitchell',
              'subject': 'I come to seek the Grail',
              'comment_body[und][0][value]': '...and I am definitely not a bot'}
    r = requests.post("http://www.pythonscraping.com/comment/reply/10", data=params)

    responseObj = BeautifulSoup(r.text)
    if responseObj.find('div', {'class': 'messages'}) is not None:
        print(responseObj.find('div', {'class': 'messages'}).get_text())
    else:
        print('There was a problem reading the CAPTCHA correctly!')

'''
验证浏览器的cookie设置
'''
import requests
from bs4 import BeautifulSoup

session = requests.Session()
headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_5) AppleWebKit 537.36 (KHTML, like Gecko) CHrome',
           'Accept': 'text/html, application/xhtml+xml, application/xml; q=0.9, image/webp, */*; q=0.8'}
url = "https://www.whatismybrowser.com/developers/what-http-headers-is-my-browser-sending"

req = session.get(url, headers=headers)

bsObj = BeautifulSoup(req.texxt)
print(bsObj.find('table', {'class': 'table-striped'}).get_text)

'''
调用webDriver的get_cookie方法查看cookie
'''
from selenium import webdriver

driver = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
driver.get("http://pythonscraping.com")
driver.implicitly_wait(1)

saveCookies = driver.get_cookies()
print(saveCookies)

driver2 = webdriver.PhantomJS(executable_path='<Path to Phantom JS>')
driver2.get("http://pythonscraping.com")
driver2.delete_all_cookies()

for cookie in saveCookies:
driver2.add_cookie(cookie)

driver2.get("http://pythonscraping.com")
driver.implicitly_wait(1)
print(driver2.get_cookies())

'''
查找隐含链接和隐含输入字段
'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement

driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/itsatrap.html")

links = driver.find_element_by_tag_name('a')

for link in links:
if not link.is_displayed():
print('The link ' + link.get_attribute('href') + ' is a trap')

fields = driver.find_element_by_tag_name('input')

for field in fields:
if not field.is_displayed():
print('Do not change value of ' + field.get_attribute('name'))


'''
单元测试模块unittest
'''
import unittest

class TestAddition(unittest.TestCase):
    def setUp(self):
    print('Setting up the test')

    def tearDown(self):
    print('Tearing down the test')

    def test_twoPlusTwo(self):
    total = 2 + 2
    self.assertEqual(4, total)

if __name__ == '__main__':
    unittest.main()

'''
测试维基百科
'''
from urllib.request import urlopen
from bs4 import BeautifulSoup
import unittest

class TestWikipedia(unittest.TestCase):
    bsObj = None

    def setUpClass(cls):
        global bsObj
        url = 'http://en.wikipedia.org/wiki/Monty_Python'
        bsObj = BeautifulSoup(urlopen(url))

    def test_titleText(self):
        global bsObj
        pageTitle = bsObj.find('h1').get_text()
        self.assertEqual('Monty Python', pageTitle)

    def test_contentExists(self):
        global bsObj
        content = bsObj.find('div', {'id': 'mw-content-text'})
        self.assertIsNone(content)

if __name__ == '__main__':
    unittest.main()

'''
循环执行一个测试
'''
class TestWikipedia(unittest.TestCase):
    bsObj = None
    url = None

    def test_PageProperties(self):
        global bsObj
        global url

        url = 'http://en.wikipedia.org/wiki/Monty_Python'
        # 测试遇到的前100个页面
        for i in range(1, 100):
        bsObj = BeautifulSoup(urlopen(url))
        titles = self.titleMatchesURL()
        self.assertEquals(titles[0], titles[1])
        self.assertTrue(self.contentExists())
        url = self.getNextLink()
        print('Done!')

    def titleMatchesURL(self):
        global bsObj
        global url
        pageTitle = bsObj.find('h1').get_text()
        urlTitle = url[(url.index('/wiki/')+6):]
        urlTitle = urlTitle.replace('_', ' ')
        urlTitle = unquote(urlTitle)
        return [pageTitle.lower(), urlTitle.lower()]

    def contentExists(self):
        global bsObj
        content = bsObj.find('div', {'id': 'mw-content-text'})
        if content is not None:
            return True
        return False

    def getNextLink(self):
        # 返回随机链接

if __name__ == '__main__':
    unittest()


'''
填写表单并提交
'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS(executable_path='')
driver.get("http://pythonscraping.com/pages/files/form.html")

firstnameField = driver.find_element_by_name('firstname')
lastnameField = driver.find_element_by_name('lastname')
submitButton = driver.find_element_by_id('submit')



# 方法1
firstnameField.send_keys('Ryan')
lastnameField.send_keys('Mitchell')
submitButton.click()

# 方法2
actions = ActionChains(driver).click(firstnameField).send_keys('Ryan')\
.click(lastnameField).send_keys('Mitchell')\
.send_keys(Keys.RETURN)
actions.perform()

print(driver.find_element_by_tag_name('body').text)

driver.close()

'''
鼠标拖拽
'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains

driver = webdriver.PhantomJS(executable_path='')
driver.get('http://pythonscraping.com/pages/javascript/draggableDemo.html')

print(driver.find_element_by_id('message').text)

element = driver.find_element_by_id('draggable')
target = driver.find_element_by_id('div2')
actions = ActionChains(driver)
actions.drag_and_drop(element, target).perform()

print(driver.find_element_by_id('message').text)


'''
截屏
'''
driver = webdriver.PhantomJS()
driver.get('http://www.pythonscraping.com/')
driver.get_screenshot_as_file('python_scraping.png')


'''
带拖放动作的网站单元测试
'''
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver import ActionChains
import unittest

class TestAddition(unittest.TestCase):
    driver = None
    def setUp(self):
        global driver
        driver = webdriver.PhantomJS(executable_path='')
        url = 'http://pythonscraping.com/pages/javascript/draggableDemo.html'
        driver.get(url)

    def tearDown(self):
        print('Tearing down the test')

    def test_drag(self):
        global driver
        element = driver.find_element_by_id('draggable')
        target = driver.find_element_by_id('div2')
        actions = ActionChains(driver)
        actions.drag_and_drop(element, target).perform()

        self.assertEqual('You are definitely not a bot!', driver.find_element_by_id('message').text)

if __name__ == '__main__':
    unittest.main()

'''
PySocks和Tor配合使用
'''
import socks
import socket
from urllib.request import urlopen

socks.set_default_proxy(socks.SOCKSS, 'localhost', 9150)
socket.socket = socks.socksocket
print(urlopen('http://icanhazip.com').read())

'''
Selenium，PhantomJS，和Tor配合使用案例，这里则不再需要PySocks
'''
from selenium import webdriver

service_args = ['--proxy=localhost:9150', '--proxy-type=socks5', ]
driver = webdriver.PhantomJS(executable_path='', service_args=service_args)

driver.get('http://icanhazip.com')
print(driver.page_source)
driver.close()
























driver.close()