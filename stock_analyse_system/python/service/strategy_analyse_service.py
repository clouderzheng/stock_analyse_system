from python.dao import stock_strategy_dao

"""策略分析"""
class strategy_analyse():

    def __init__(self):
        self.stock_strategy_dao = stock_strategy_dao.stock_strategy()
        pass

    """分页查询策略选择股票信息"""
    def get_strategy_stock(self,page = 1,limit = 10,strategy_ids = None):

        self.stock_strategy_dao.get_strategy_stock(page,limit,strategy_ids)