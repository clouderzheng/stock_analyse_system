# -*- coding: utf-8 -*-
import scrapy
import snow_ball_service
import date_time_util
urls = ['https://www.cnblogs.com/mahailuo/p/8315865.html']

class HotelSpider(scrapy.Spider):
    name = 'hotel'
    # allowed_domains = ['www.cnblogs.com']
    start_urls = urls

    def parse(self, response):
        # html = response.text
        html = response.selector.xpath('//title').get()
        print("first title - --------------",html)


        # stock["name"],stock["symbol"],stock["current"],stock["percent"],stock["symbol"],time.time(),time.time(),1)
        stock = ("title1","symbol",12,5,date_time_util.get_date_time(0),date_time_util.get_date_time(1),4)
        snow_ball_service.save_strategy_stock_info(stock)
        yield scrapy.Request("https://www.cnblogs.com/flora5/p/7152556.html",callback= self.personal_parse)
        pass

    def personal_parse(self,response):
        html = response.selector.xpath('//title').get()
        stock = ("title2", "symbol", 22, 4, date_time_util.get_date_time(0), date_time_util.get_date_time(1),5)
        snow_ball_service.save_strategy_stock_info(stock)
        print("second title - --------------", html)