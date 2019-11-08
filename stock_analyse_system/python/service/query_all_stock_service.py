from scrapy.cmdline import execute
import _thread
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
    data = requests.get("http://localhost:5000/spider/get_every_signal")
    print(data.text)
    # subprocess.check_output(execute(['scrapy', 'crawl', 'hotel']))