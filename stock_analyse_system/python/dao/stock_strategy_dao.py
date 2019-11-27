from python.mysql import mysql_pool
from python.redis import redis_pool,redis_key_constants
from python.util import date_time_util
from python.dao import stock_strategy_record_dao
"""策略选股记录"""
class stock_strategy:
    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()
        self.redis = redis_pool.RedisPool()
        self.stock_strategy_record_dao =  stock_strategy_record_dao.stock_strategy_record()

    """保存策略选择的股票信息到策略选择表"""
    def save_strategy_choose(self,data,stock_code,strategy_id):
        strategy_id = str(strategy_id) + ","
        stock_info = []
        stock_info.append(self.redis.hget(redis_key_constants.stock_name_code_mapping,stock_code))
        stock_info.append(stock_code)
        stock_info.append(data[5])
        stock_info.append(data[7])
        stock_info.append("," + strategy_id)
        stock_info.append(date_time_util.get_date(0))

        sql = "insert into trade_strategy_record (stock_name,stock_code,current_price,current_rate,strategy_category ,`create_date`) \
                 value (%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE  strategy_category = CONCAT(strategy_category,'" + strategy_id + "');"

        self.mysqlService.insert(sql,stock_info )
        """保存数据到策略跟踪表"""
        self.stock_strategy_record_dao.save_stock_strategy_record(stock_code,data)

    """查询在指定日期内需要跟踪的股票"""
    def get_stock_track(self, param):
        sql = "SELECT * from trade_strategy_record  WHERE create_date > %s and  create_date < %s GROUP BY stock_code"
        return self.mysqlService.selectMany(sql, param)
    """持久化策略数据
    这里优化下 逻辑 
    多条策略的数据合并为一条
    code与date组合唯一索引  有更新添加策略
    """
    def save_other_strategy_choose(self,stock_info):
        strategy_id = str(stock_info[4]) + ","
        stock_info[4] = "," + strategy_id
        stock_info.append(date_time_util.get_date(0))
        sql = "insert into trade_strategy_record (stock_name,stock_code,current_price,current_rate,strategy_category ,`create_date`) \
              value (%s,%s,%s,%s,%s,%s)  ON DUPLICATE KEY UPDATE  strategy_category = CONCAT(strategy_category,'" + strategy_id + "');"
        self.mysqlService.insert(sql, stock_info)

    """分页查询策略选中表"""
    def get_strategy_stock(self,page,limit,strategy_ids = None):
        begin_index = (page - 1) * limit
        sql = "select * from trade_strategy_record  where 1 = 1"

        if strategy_ids != None:
            for strategy_id in strategy_ids:
                sql = sql + " and strategy_category  like  '%%," + str(strategy_id) +",%%'  "
        sql = sql + " order by create_time desc limit "+ str(begin_index) + "," + str(limit)
        result = self.mysqlService.selectMany(sql)
        return result

    def get_strategy_count(self,strategy_ids = None):
        sql = "select count(1) as count from trade_strategy_record  where 1 = 1"

        if strategy_ids != None:
            for strategy_id in strategy_ids:
                sql = sql + " and strategy_category  like  '%%," + str(strategy_id) + ",%%'  "
        sql = sql + " order by create_time desc  "
        result = self.mysqlService.selectOne(sql)
        return result