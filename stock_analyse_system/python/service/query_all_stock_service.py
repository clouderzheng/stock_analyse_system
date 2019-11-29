from python.mysql import mysql_config
import requests
"""执行异步爬虫获取信息"""
def query_stock():
    # runner = crawlerRunner.crawlerRunner()
    # spider = hotel.HotelSpider
    # deferred = runner.crawl(spider)
    # deferred.addCallback(crawlerRunner.return_spider_output)
    # print(deferred)

    # execute(['scrapy', 'crawl', 'hotel'])
    # _thread.start_new_thread(execute(['scrapy', 'crawl', 'hotel']),())
    # 模拟 自我请求 触发定时任务爬虫  爬虫不能在定时任务中运行
    data = requests.get(mysql_config.trigger_scrapy)
    # subprocess.check_output(execute(['scrapy', 'crawl', 'hotel']))