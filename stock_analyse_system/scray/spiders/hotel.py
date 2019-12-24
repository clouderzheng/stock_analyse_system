# -*- coding: utf-8 -*-
import scrapy
from python.service import stock_service,strategy_service,crawl_html_url,strategy_track_service

import json
from python.util import date_time_util
from scrapy.http import Request
import traceback
from python.redis import redis_pool,redis_key_constants
import logging
class HotelSpider(scrapy.Spider):
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  # 设置浏览器用户代理
    name = 'hotel'
    # allowed_domains = ['www.cnblogs.com']
    # start_urls  = []

    def __init__(self):
        # 获取所有需要爬取股票信息
        self.stocks = stock_service.get_stock_info()
        # 爬取股票页面链接地址模板
        # self.template = crawl_html_url.snow_ball_single_stock_info_url
        self.template = crawl_html_url.east_money_single_stock

        # 爬取时间戳
        self.timestamp = date_time_util.get_timestamp_mill_second()
        self.redis = redis_pool.RedisPool()
        self.strategy_track_service = strategy_track_service.strategy_track()
        # 获取策略锁
        self.strategy_lock = self.redis.getString(redis_key_constants.strategy_lock)
        # 锁不存在 重新加上锁
        if self.strategy_lock == None:
            self.redis.setStringExpire(redis_key_constants.strategy_lock,"lock",redis_key_constants.strategy_lock_time)

    #     # self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571063050000&period=day&type=before&count=-60&indicator=kline','https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300273&begin=1571063050000&period=day&type=before&count=-60&indicator=kline']
    #     self.start_urls = [crawl_html_url.snow_ball_main_url,'https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571062931000&period=day&type=before&count=-60&indicator=kline']        #     self.start_urls.append(crawl_html_url.snow_ball_single_stock_info_url.format(stock['area_stock_code'],date_time_util.get_timestamp_mill_second(),-60))
    #     print(self.start_urls)
        # self.start_urls = urls

    def start_requests(self):  # 用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(crawl_html_url.snow_ball_main_url, meta={'cookiejar': 1}, callback=self.parse,headers=self.header)]

    # start_urls  = url
    def parse(self, response):
        for stock in self.stocks:
            code = stock['code_short']
            if str(code).startswith("3") | str(code).startswith("0"):
                code = code+"2"
            else:
                code = code +"1"
            yield Request(self.template.format(code,self.timestamp),callback=self.strategy_parse,headers=self.header,meta={'cookiejar':True})

        pass

    """回调策略"""
    def strategy_parse(self,response):


        try:
            jsonp = str(response.text)
            jsonp = jsonp[19:-1]
            data = json.loads(jsonp)
            if (len(data["data"]) < 60):
                return
            """"这里缓存在当天数据在redis"""
            code = str(data['code'])
            if code.startswith("0") | code.startswith("3"):
                code = "SZ" + code
            else:
                code = "SH" + code
            data['code'] = code
            self.redis.hset(redis_key_constants.current_day_stock_map,code,str(data["data"][-1]))
            """策略分类 有些策略不需要每天跑"""
            # if self.strategy_lock == None:
            # strategy_service.call_back_support_stock(data)
            strategy_service.get_up_wave(data)
            strategy_service.year_average_choose(data)
            # strategy_service.get_average_bond(data)
        except Exception as e:
            traceback.print_exc()
        pass

    def close(self,spider, reason):
        logging.info("爬取关闭，关闭爬虫")
        self.strategy_track_service.get_track_stock()
        closed = getattr(spider, 'closed', None)
        if callable(closed):
            return closed(reason)