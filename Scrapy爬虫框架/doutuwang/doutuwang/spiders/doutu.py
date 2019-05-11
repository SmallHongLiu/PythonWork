# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy.pipelines.images import ImagesPipeline

class DoutuSpider(CrawlSpider):  # 继承特殊模版的Spider
    name = 'doutu'
    allowed_domains = ['doutula.com']
    start_urls = ['http://www.doutula.com/article/list/?page=2']

    rules = (
        # Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        # 请求符合规则的url，拿到响应并交给回调函数parse_item，
        # 其中参数follow如果为True，当拿到响应后，除了会给回调函数，还会提取响应里面的url, 并进行提取url和匹配rules规则
        # follow为False，拿到响应后，不对响应进行链接提取和分析
        Rule(LinkExtractor(allow=r'http://www.doutula.com/article/detail/\d+'), callback='parse_item', follow=True),  # \d：正则表达式中的数字, \d+: 无限个数字的组合
    )
    # 分析http://www.doutula.com/ 的响应，提取全部的url

    def parse_item(self, response):
        item = {}
        item['image_urls'] = []
        item['images'] = []
        item['image_urls'] = response.xpath('.//div[@class="pic-content"]//img/@src').extract()  # 这里也可以使用bs4对response.text进行结构化解析
        print(len(item['image_urls']), response.url)
        return item

        """
        # 找到下一页的url地址，实现翻页请求
        next_url = response.xpath('.//a[@class="page-link"][@rel="next"]/@href').extract_first()
        print(next_url)
        if next_url != ' javascript:;':
            next_url = 'http://www.doutula.com/' + next_url
            yield scrapy.Request(
                next_url,
                callback=self.parse()
            )
        """

        #item['domain_id'] = response.xpath('//input[@id="sid"]/@value').get()
        #item['name'] = response.xpath('//div[@id="name"]').get()
        #item['description'] = response.xpath('//div[@id="description"]').get()
