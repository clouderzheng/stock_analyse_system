from python.service import snow_ball_service
from python.mysql import  mysql_pool

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
# snow_ball_service.save_strategy_stock_info(stock_info)

"""sql测试"""
# pool = mysql_pool.sql_pool()
# con = pool.get_connection()
# cursor = con.cursor()
# cursor.execute("select * from trade_strategy_mapping where id = 1")
# fetchone = cursor.fetchone()
# print(fetchone)