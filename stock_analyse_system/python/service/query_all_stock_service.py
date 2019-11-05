from scrapy.cmdline import execute
import subprocess
from scray.spiders import  crawlerRunner,hotel

"""执行异步爬虫获取信息"""
def query_stock():
    # runner = crawlerRunner.crawlerRunner()
    # spider = hotel.HotelSpider
    # deferred = runner.crawl(spider)
    # deferred.addCallback(crawlerRunner.return_spider_output)
    # print(deferred)
    execute(['scrapy', 'crawl', 'hotel'])
    # subprocess.check_output(execute(['scrapy', 'crawl', 'hotel']))