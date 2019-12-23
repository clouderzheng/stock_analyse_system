from python.mysql import mysql_pool
from python.redis import redis_pool,redis_key_constants
from python.util import date_time_util
from python.service import crawl_html_url

"""策略跟踪dao层"""

class stock_strategy_record:
    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()
        self.redis = redis_pool.RedisPool()

    """插入跟踪记录"""
    def save_stock_strategy_record(self,stock_code,data):
        record = []
        data = data.split(",")
        record.append(stock_code)
        record.append(self.redis.hget(redis_key_constants.stock_name_code_mapping,stock_code))
        record.append(date_time_util.get_date(0))
        record.append(data[crawl_html_url.open_price_index])
        record.append(data[crawl_html_url.low_price_index])
        record.append(data[crawl_html_url.high_price_index])
        record.append(data[crawl_html_url.close_price_index])
        record.append(0)
        sql = "insert ignore into trade_strategy_track_record (area_stock_code,stock_name,`current_date`,open_price,high_price,low_price,close_price,close_rate) \
               value (%s,%s,%s,%s,%s,%s,%s,%s) "
        self.mysqlService.insert(sql,record)

    """获取跟踪时间内股票信息"""
    def get_track_stock_by_date(self,stock_code,begin_date,end_date):
        param = []
        param.append(stock_code)
        param.append(begin_date)
        param.append(end_date)
        sql = "select * from trade_strategy_track_record where area_stock_code = %s and  `current_date` > %s and  `current_date` < %s  ORDER BY `current_date` "
        return self.mysqlService.selectMany(sql,param)
