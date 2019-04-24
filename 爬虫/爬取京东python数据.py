import requests
from lxml import etree
import time
import re
import os
import csv
from fake_useragent import UserAgent

# 实例化一个ua 对象
ua = UserAgent()


class PythonBookSpider(object):
    '''爬取京东商场前20页的python书籍'''
    def __init__(self):
        self.base = "https://search.jd.com/Search?keyword=python&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&wq=python&page={}"
        self.comment_url = "https://sclub.jd.com/comment/productCommentSummaries.action?referenceIds={}&callback=jQuery5954857&_={}"
        self.rank_url = "https://c.3.cn/book?skuId={}&cat=1713,3287,3797&area=1_72_2799_0&callback=book_jsonp_callback"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) "
                          "Chrome/22.0.1207.1 Safari/537.1",
            "authority": "search.jd.com"
        }

    def _send_request(self, url):
        '''
        发送请求, 获取响应
        :param url: 请求路径
        :return：
        '''
        self.headers['User-Agent'] = ua.random
        time.sleep(0.5)
        response = requests.get(url=url, headers=self.headers, timeout=5)
        return response

    def send_request(self, url):
        '''主要是对请求响应进行处理'''
        try:
            response = self._send_request(url)
        except Exception as e:
            print('requests error: {}'.format(e))
            return None

        if response.status_code != 200:
            content = None
        else:
            content = response.content
        return content

    def get_comment_count(self, sku_id):
        ''''获取评论数'''
        response = self.send_request(self.comment_url.format(sku_id, int(time.time())))
        if not response:
            return '', ''
        # 响应的编码方式可以在响应中查看
        response = response.decode('GBK')
        good_rate = re.findall(r'"GoodRate":(\d.\d+)', response)[0] if re.findall(r'"GoodRate":(\d.\d+)', response) else ""
        comment_count = re.findall(r'"CommentCount":(\d+)', response)[0] if re.findall(r'"CommentCount":(\d+)', response) else ""
        return good_rate, comment_count

    def parse_book_rank(self, sku_id):
        '''
        获取京东自营书籍销量排行榜名次
        :param sku_id: int 书籍的sku_id
        :return:
        '''
        response = self.send_request(self.rank_url.format(sku_id))
        if not response:
            return False, None
        print('b_rank:{}'.format(response.decode()))
        b_rank = re.findall(r'"rank":[-|0-9][0-9]*', response.decode())
        b_rank = b_rank[0].split(":") if b_rank else ""
        return True, b_rank

    def save_book_info(self, books_list):
        '''
        保存书籍信息
        :param books_list: 每一页的书籍信息
        :return:
        '''
        if not os.path.exists('PythonBookInfo.csv'):
            with open('PythonBookInfo.csv', 'a+', newline="") as file:
                writer = csv.writer(file)
                writer.writerow(['name', 'price', 'is_self_operated', 'comment_counts', 'good_comments_rate',
                                 'good_comments_rate', 'sale_rank'])
            with open('PythonBookInfo.csv', 'a+', newline='') as file:
                writer = csv.writer(file)
                for books_list in books_list:
                    try:
                        writer.writerows(books_list)
                    except:
                        continue

    def parse_index_page(self, response):
        '''
        解析首页的界面信息
        :param response: type: str 搜索页面的响应
        :return: type: list 每一页的全部书籍相关信息
        '''
        index_selector = etree.HTML(response)
        books_list = index_selector.xpath('//div[@id="J_goodsList"]/ul/li')  # 解析每一页的书籍列表
        py_book_info_list = []
        for book in books_list:
            # 书籍详情地址
            b_url = book.xpath('.//div[@class="p-img"]/a/@href')
            # 图书价格
            b_price = book.xpath('.//div[@class="p-price"]//i/text()')
            # 卖家方式
            b_seller = book.xpath('//div[@class="p-icons"]/i[1]/text()')
            # 书名称
            b_name = book.xpath('.//div[@class="p-name"]//em')
            b_name = [] if not b_name else b_name[0].xpath("string(.)").strip()
            # 书的评论数：通过js加载的
            sku_id = book.xpath('./@data-sku')[0]
            if not sku_id:
                continue
            good_rate, comment_count = self.get_comment_count(sku_id)
            if not all([b_url, b_price, good_rate, comment_count, b_name]):
                continue
            detail_url = 'https:' + b_url[0] if not b_url[0].startswith('https') else b_url[0]
            '''如果是京东自营的话，在抓取对应的自营排名，出版社'''
            if b_seller[0] == '自营':
                # 获取书籍销售排行榜名次
                rank_response = self.parse_book_rank(sku_id)
                print('parse_index_page rank_response: ', response)
                if not rank_response:
                    continue
                b_rank = rank_response[1]
                b_seller = b_seller[0]
            else:
                b_rank = ""
                b_seller = ""
            py_book_info_list.append([b_name, b_price[0], b_seller, comment_count, good_rate, b_rank, detail_url])
        return py_book_info_list

    def spider(self):
        '''spider的主要逻辑业务'''
        for page in range(1, 21):
            # 1, 请求搜索页，获取书籍列表页面信息，这里请求前20页
            first_response = self.send_request(self.base.format(2 * page - 1))
            if not first_response:
                continue
            # 2, 解析搜索页书籍的相关信息
            py_book_info_list = self.parse_index_page(first_response)
            if not py_book_info_list:
                continue
            # 3, 保存爬取书籍信息
            self.save_book_info(py_book_info_list)
            print('第{}页爬取完成'.format(page))
        print('抬头 望天')


if __name__ == '__main__':
    py_spider = PythonBookSpider()
    py_spider.spider()

