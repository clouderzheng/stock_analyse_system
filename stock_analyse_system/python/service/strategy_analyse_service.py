from python.dao import stock_strategy_dao,stock_strategy_record_dao
from python.util import date_time_util
"""策略分析"""
class strategy_analyse():

    def __init__(self):
        self.stock_strategy_dao = stock_strategy_dao.stock_strategy()
        self.stock_strategy_record_dao = stock_strategy_record_dao.stock_strategy_record()
        pass

    """分页查询策略选择股票信息"""
    def get_strategy_stock(self,page = 1,limit = 10,strategy_ids = None):
        # 查询出分页数据
        strategy_stock_list = self.stock_strategy_dao.get_strategy_stock(page, limit, strategy_ids)
        # 遍历每一条记录后续5天跟踪记录
        for strategy_stock in strategy_stock_list:
            # 获取入选日期
            choose_date = strategy_stock['create_date']
            end_date = date_time_util.get_work_date_after(5,choose_date)
            result = self.stock_strategy_record_dao.get_track_stock_by_date(strategy_stock['stock_code'],choose_date,end_date)
            strategy_stock["track_info"] = result

        return strategy_stock_list
    """查询策略选择股票总数"""
    def get_strategy_stock_count(self,strategy_ids = None):

        return self.stock_strategy_dao.get_strategy_count(strategy_ids)["count"]