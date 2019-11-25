from python.mysql import mysql_pool
from python.redis import redis_pool,redis_key_constants
from python.util import date_time_util

"""策略跟踪dao层"""

class stock_strategy_record:
    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()
        self.redis = redis_pool.RedisPool()

    """插叙跟踪记录"""
    def save_stock_strategy_record(self,stock_code,data):
        record = []
        record.append(stock_code)
        record.append(self.redis.hget(redis_key_constants.stock_name_code_mapping,stock_code))
        record.append(date_time_util.get_date(0))
        record.append(data[2])
        record.append(data[3])
        record.append(data[4])
        record.append(data[5])
        record.append(data[7])
        sql = "insert into trade_strategy_track_record (area_stock_code,stock_name,current_date,open_price,high_price,low_price,close_price,close_rate) \
               value (%s,%s,%s,%s,%s,%s,%s,%s) "
        self.mysqlService.insert(sql,record)

    """查询在指定日期内需要跟踪的股票"""
    def get_stock_track(self,param):
        sql = "SELECT * from trade_strategy_record  GROUP BY stock_code WHERE create_date > %s and  create_date < %s GROUP BY stock_code"
        return self.mysqlService.selectMany(sql,param)
