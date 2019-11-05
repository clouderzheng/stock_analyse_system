# -*- coding: utf-8 -*-
import scrapy
from python.service import stock_service,strategy_service,crawl_html_url
import json
from python.util import date_time_util
from scrapy.http import Request,FormRequest
import traceback

class HotelSpider(scrapy.Spider):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  # 设置浏览器用户代理
    name = 'hotel'
    # allowed_domains = ['www.cnblogs.com']
    # start_urls  = []

    def __init__(self):
        self.stocks = stock_service.get_stock_info()
        self.index = -1
        self.template = crawl_html_url.snow_ball_single_stock_info_url
        self.timestamp = date_time_util.get_timestamp_mill_second()
    #     # self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571063050000&period=day&type=before&count=-60&indicator=kline','https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300273&begin=1571063050000&period=day&type=before&count=-60&indicator=kline']
    #     self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571062931000&period=day&type=before&count=-60&indicator=kline']        #     self.start_urls.append(crawl_html_url.snow_ball_single_stock_info_url.format(stock['area_stock_code'],date_time_util.get_timestamp_mill_second(),-60))
    #     print(self.start_urls)
        # self.start_urls = urls

    def start_requests(self):  # 用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(crawl_html_url.snow_ball_main_url, meta={'cookiejar': 1}, callback=self.parse,headers=self.header)]

    # start_urls  = url
    def parse(self, response):
        self.index += 1
        for stock in self.stocks:
           yield Request(self.template.format(stock['area_stock_code'],self.timestamp,-60),callback=self.strategy_parse,headers=self.header,meta={'cookiejar':True})

        pass

    """回调策略"""
    def strategy_parse(self,response):

        data = json.loads(response.text)
        if (len(data["data"]["item"]) < 60):
            return
        try:
            strategy_service.call_back_support_stock(data)
            strategy_service.get_up_wave(data)
        except Exception as e:
            traceback.print_exc()
        pass