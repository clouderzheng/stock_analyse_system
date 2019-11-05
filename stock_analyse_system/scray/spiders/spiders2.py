# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request,FormRequest
from python.service import crawl_html_url

class PachSpider(scrapy.Spider):                            #定义爬虫类，必须继承scrapy.Spider
    name = 'spiders2'                                           #设置爬虫名称
    # allowed_domains = ['edu.iqianyue.com']                  #爬取域名
    # start_urls = ['http://edu.iqianyue.com/index_user_login.html']     #爬取网址,只适于不需要登录的请求，因为没法设置cookie等信息

    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0'}  #设置浏览器用户代理

    def start_requests(self):       #用start_requests()方法,代替start_urls
        """第一次请求一下登录页面，设置开启cookie使其得到cookie，设置回调函数"""
        return [Request(crawl_html_url.snow_ball_main_url,meta={'cookiejar':1},callback=self.parse)]

    def parse(self, response):     #parse回调函数

        data = { }

        # 响应Cookie
        Cookie1 = response.headers.getlist('Set-Cookie')   #查看一下响应Cookie，也就是第一次访问注册页面时后台写入浏览器的Cookie
        print(Cookie1)

        print('登录中')
        """第二次用表单post请求，携带Cookie、浏览器代理、用户登录信息，进行登录给Cookie授权"""
        return [FormRequest.from_response(response,
                                          url=crawl_html_url.snow_ball_main_url,   #真实post地址
                                          meta={'cookiejar':response.meta['cookiejar']},
                                          headers=self.header,
                                          formdata=data,
                                          callback=self.next,
                                          )]
    def next(self,response):
        a = response.body.decode("utf-8")   #登录后可以查看一下登录响应信息
        # print(a)
        """登录后请求需要登录才能查看的页面，如个人中心，携带授权后的Cookie请求"""
        yield Request('https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300272&begin=1571062931000&period=day&type=before&count=-60&indicator=kline',meta={'cookiejar':True},callback=self.next2)
    def next2(self,response):
        # 请求Cookie
       print(response.text)
        # body = response.body  # 获取网页内容字节类型
        # unicode_body = response.body_as_unicode()  # 获取网站内容字符串类型
        #
        # a = response.xpath('/html/head/title/text()').extract()  #得到个人中心页面
        # print(a)