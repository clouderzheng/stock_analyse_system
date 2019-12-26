from python.mysql import mysql_pool

""""资金流向"""
class capital_dao():

    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()


    """添加营业部股票资金流向"""
    def add_sale_department_trade(self,param):
        sql = "insert into trade_sale_department_capital_flow (sale_department_name,sale_department_code,stock_name,stock_code,create_date,`describe`,capital_in_flow,capital_out_flow,capital_net_flow) \
            values( %s,%s,%s,%s,%s,%s,%s,%s,%s)"
        self.mysqlService.insert(sql,param)

    """查询营业部买卖股票资金情况"""
    def query_sale_department_capital(self):
        sql = "SELECT stock_name,stock_code,create_date,SUM(capital_in_flow) as in_flow,SUM(capital_out_flow) as outflow, sum(capital_net_flow) as a1 from trade_sale_department_capital_flow  GROUP BY stock_code ORDER BY a1 desc"
        return self.mysqlService.selectMany(sql)