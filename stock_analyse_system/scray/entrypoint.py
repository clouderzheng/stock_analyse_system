from scrapy.cmdline import execute
from hotel import HotelSpider
import hotel
# HotelSpider.start_urls = ["https://blog.csdn.net/sf131097/article/details/79463912"]
hotel.urls =  ["https://blog.csdn.net/sf131097/article/details/79463912"]
execute(['scrapy','crawl','hotel'])