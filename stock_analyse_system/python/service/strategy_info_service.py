from python.dao import strategy_dao
"""策略信息逻辑层"""
class strategy_info():

    def __init__(self):
        self.strategy_info = strategy_dao.strategy_dao()


    """根据策略id查询策略信息"""
    def query_strategy_by_id(self,strategy_id):
        return self.strategy_info.query_strategy_by_id(strategy_id)