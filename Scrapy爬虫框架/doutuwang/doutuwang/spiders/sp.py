# -*- coding: utf-8 -*-
import scrapy


class SpSpider(scrapy.Spider):  # 该Spider继承的是基础的Spider
    name = 'sp'
    allowed_domains = ['spbeen.com']
    start_urls = ['http://www.spbeen.com/']

    def parse(self, response):
        pass
