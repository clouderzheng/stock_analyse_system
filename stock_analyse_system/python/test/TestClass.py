from python.service import snow_ball_service,strategy_analyse_service
from python.mysql import  mysql_pool
from python.redis import redis_pool,redis_key_constants
import time
from python.util import date_time_util
import datetime
from python.dao import stock_strategy_dao
"""测试爬取雪球数据"""
# import requests
# from python.service import crawl_html_url
# import json
# headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
#                          'Chrome/51.0.2704.63 Safari/537.36'}
# session = requests.session()
# session.get(crawl_html_url.snow_ball_main_url, headers=headers)
# """获取真正有效数据"""
# html_data = session.get("https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SH600376&begin=1573285956000&period=day&type=before&count=-60&indicator=kline", headers=headers)
# data = json.loads(html_data.text)
# print((str(data)))


"""测试记录插入"""
# stock_info = ["光大银行","SH601818",4.09,3.81,"5"]
# sql = "insert into trade_strategy_record(stock_code,create_date,strategy_category) values (%s,%s,%s) ON DUPLICATE KEY UPDATE  strategy_category = CONCAT(strategy_category,'5')"
# result = mysql_pool.sql_pool().insert(sql,('SZ10200727','2019-11-27','5'))
# print(result)

"""sql测试"""
# pool = mysql_pool.sql_pool()
# con = pool.get_connection()
# cursor = con.cursor()
# cursor.execute("select * from trade_strategy_mapping where id = 1")
# fetchone = cursor.fetchone()
# print(fetchone)

"""测试获取5日前日期"""
# print(date_time_util.get_date(-5))
# print(datetime.datetime.now().weekday())

"""测试获取策略选中表"""
# data = stock_strategy_dao.stock_strategy().get_strategy_stock(1,1)
# print(data)
# create_date = data[0]['create_date']
# print(create_date+ datetime.timedelta(0))

"""测试获取策略选中表总数"""
# data = stock_strategy_dao.stock_strategy().get_strategy_count()
# print(data)

"""测试获取策略选股信息"""
# stock = strategy_analyse_service.strategy_analyse().get_strategy_stock(1, 1)
# print(stock[0])

"""测试redis过期时间"""
# pool = redis_pool.RedisPool()
# pool.setStringExpire("name","night",redis_key_constants.strategy_lock_time)
# print(pool.getString("name"))
# time.sleep(6)
# print(pool.getString("name"))

# import platform
# print(platform.system().lower())