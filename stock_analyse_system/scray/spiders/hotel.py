# -*- coding: utf-8 -*-
import scrapy


class HotelSpider(scrapy.Spider):
    name = 'hotel'
    allowed_domains = ['www.cnblogs.com']
    start_urls = ['https://www.cnblogs.com/mahailuo/p/8315865.html']

    def parse(self, response):
        # html = response.text
        html = response.selector.xpath('//title').get()
        print("title - --------------",html)
        pass
