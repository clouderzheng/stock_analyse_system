# -*- coding: utf-8 -*-
import scrapy
import stock_service
import json
import crawl_html_url
import date_time_util
from scrapy.http import Request,FormRequest

class HotelSpider(scrapy.Spider):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  # 设置浏览器用户代理
    name = 'hotel'
    # allowed_domains = ['www.cnblogs.com']
    # start_urls  = []

    def __init__(self):
        self.stocks = stock_service.get_stock_info()
        self.index = -1
        self.template = 'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol={}&begin=1571063050000&period=day&type=before&count=-60&indicator=kline'
    #     # self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571063050000&period=day&type=before&count=-60&indicator=kline','https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300273&begin=1571063050000&period=day&type=before&count=-60&indicator=kline']
    #     self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571062931000&period=day&type=before&count=-60&indicator=kline']        #     self.start_urls.append(crawl_html_url.snow_ball_single_stock_info_url.format(stock['area_stock_code'],date_time_util.get_timestamp_mill_second(),-60))
    #     print(self.start_urls)
        # self.start_urls = urls

    def start_requests(self):  # 用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(crawl_html_url.snow_ball_main_url, meta={'cookiejar': 1}, callback=self.parse,headers=self.header,)]

    # start_urls  = url
    def parse(self, response):
        # html = response.selector.xpath('//title').get()
        # print("first title - --------------",html)


        # stock["name"],stock["symbol"],stock["current"],stock["percent"],stock["symbol"],time.time(),time.time(),1)
        # stock = ("title1","symbol",12,5,date_time_util.get_date_time(0),date_time_util.get_date_time(1),4)
        # snow_ball_service.save_strategy_stock_info(stock)
        # yield scrapy.Request("https://www.cnblogs.com/flora5/p/7152556.html",callback= self.personal_parse)

        print(response.text)

        self.index += 1
        yield Request(self.template.format(self.stocks[self.index]['area_stock_code']),callback=self.parse,meta={'cookiejar':True})


        if 1==1:
            return
        data = json.loads(response.text)
        items = data["data"]["item"]

        """查询结果小于回溯天数 可能是新股 跳过"""
        if (len(items) < 60):
            return
        # 获取此时最低价
        current_low_price = items[60 - 1][4]
        # 获取此时最新报价
        current_new_price = items[60 - 1][5]
        # 获取此时最低价时间
        current_low_day = items[60 - 1][0]

        # 将排除之后的日期根据最高价排序
        last_days = items[:(60 - 20)]
        sorts_list = sorted(last_days, key=lambda x: x[3], reverse=True)
        # 获取上个高点价格
        last_high_price = sorts_list[0][3]
        # 获取上个高点时间
        last_high_day = sorts_list[0][0]

        # 计算两个价格之间的相差波动率
        percent = (current_low_price - last_high_price) / last_high_day
        # 判断计算结果是否在指定区间内
        if (percent < 2):
            stock_info = {"current_new_price": current_new_price, "current_low_price": current_low_price, \
                          "current_low_day": current_low_day, "last_high_price": last_high_price, \
                          "last_high_day": last_high_day, \
                          "area_stock_code": data["data"]["symbol"], \
                          "percent": round(percent * 100, 2)}

            print(stock_info)
        pass

    def personal_parse(self,response):
        html = response.selector.xpath('//title').get()
        # stock = ("title2", "symbol", 22, 4, date_time_util.get_date_time(0), date_time_util.get_date_time(1),5)
        # snow_ball_service.save_strategy_stock_info(stock)
        print("second title - --------------", html)