# URL 管理器
class URLManager(object):
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        # 判断是否有未爬取的URL
        return self.new_url_size() != 0

    def get_new_url(self):
        # 获取一个未爬取的链接
        new_url = self.new_urls.pop()
        # 提取之后，将其添加到已爬取的链接中
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        # 将新链接添加到未爬取的集合中（单个链接)
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        # 将新链接添加到未爬取的集合中
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def new_url_size(self):
        # 获取未爬取的url大小
        return len(self.new_urls)

    def old_url_size(self):
        # 获取已爬取的url大小
        return len(self.old_urls)


# HTML下载器
import requests
class HTMLDownload(object):
    def download(self, url):
        if url is None:
            return
        s = requests.Session()
        s.headers['User-Agent'] = 'Mozilla / 5.0(Windows NT 10.0;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 63.0.3239.132Safari / 537.36'
        res = s.get(url)

        # 判断是否正常获取
        if res.status_code == 200:
            res.encoding = 'utf-8'
            res = res.text
            return res
        return None


# HTML解释器
import re
from bs4 import BeautifulSoup

class HTMLParser(object):

    def parser(self, page_url, html_cont):
        '''
        用于解析网页内容，抽取URL喝数据
        :param page_url: 下载页面的URL
        :param html_cont: 下载的网页内容
        :return: 返回url和数据
        '''
        if page_url is None or html_cont is None:
            return
        soup = BeautifulSoup(html_cont, 'html.parse')
        new_urls = self.get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        '''
        抽取新的url集合
        :param page_url: 下载页面的URL
        :param soup: soup数据
        :return: 返回新的URL集合
        '''
        new_urls = set()
        for link in range(1, 100):
            # 添加新的URL
            new_url = "http://www.runoob.com/w3cnote/page/"+str(link)
            new_urls.add(new_url)
            print(new_urls)
        return new_urls

    def _get_new_data(self, page_url, soup):
        '''
        抽取有效数据
        :param page_url: 下载页面的url
        :param soup:
        :return: 返回有效数据
        '''
        data = {}
        data['url'] = page_url
        title = soup.find('div', class_='post_intro').find('h2')
        print(title)
        data['title'] = title.get_text()
        summary = soup.find('div', class_='post_intro').find('p')
        data['summary'] = summary.get_text()
        return data


# 数据存储器
import codecs

class DataOutput(object):
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        fout = codecs.open('baike.html', 'a', encoding='utf-8')
        fout.write('<html>')
        fout.write('<head><meta charset="utf-8" /></head>')
        fout.write('<body>')
        fout.write('<table>')
        for data in self.datas:
            fout.write('<tr>')
            fout.write("<td>%s</td>"%data['url'])
            fout.write("<td>《%s》</td>" % data['title'])
            fout.write("<td>[%s]</td>" % data['summary'])
            fout.write('</tr>')
            self.datas.remove(data)
            fout.write('</table>')
            fout.write('</body>')
            fout.write('</html>')
            fout.close()


# 爬虫调度器
from base.DataOutput import DataOutput
from base.HTMLParser import HTMLParser
from base.HTMLDownload import HTMLDownload
from base.URLManager import URLManager

class SpiderMan(object):
    def __init__(self):
        self.manager = URLManager()
        self.downloader = HTMLDownload()
        self.parser = HTMLParser()
        self.output = DataOutput()


    def crawl(self, root_url):
        # 添加入口URL
        self.manager.add_new_url(root_url)
        # 判断url管理器中是否有新的url，同时判断抓取多少个url
        while(self.manager.has_new_url() and self.manager.old_url_size()<100):
            try:
                # 从URL管理器获取新的URL
                new_url = self.manager.get_new_url()
                print(new_url)
                # HTML下载器下载网页
                html = self.downloader.download(new_url)
                # HTML解析器抽取网页数据
                new_urls, data = self.parser.parser(new_url, html)
                print(new_urls)
                # 将抽取的url添加到URL管理器中
                self.manager.add_new_urls(new_urls)
                # 数据存储器存储文件
                self.output.store_data(data)
                print("已经抓取%s个链接" % self.manager.old_url_size())
            except Exception as e:
                print("failed")
                print(e)
            # 数据存储器将文件输出成指定的格式
            self.output.output_html()


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl('http://www.runoob.com/wscnote/page/1')



