from python.mysql import mysql_pool
"""策略信息数据层"""
class strategy_dao():

    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()

    """根据策略id查询策略信息"""
    def query_strategy_by_id(self,strategy_id):
        sql = "SELECT a.strategy,a.remark,b.strategy_param,b.strategy_value,b.remark as param_desc FROM trade_strategy  a join  trade_strategy_param  b on a.id  =b.strategy_id WHERE a.id  = " + strategy_id
        return self.mysqlService.selectMany(sql)