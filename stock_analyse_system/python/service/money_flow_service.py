from python.util import date_time_util
from python.service import crawl_html_url
from python.dao import capital_dao
import requests
import json
"""资金流向service"""
class money_flow:

    def __init__(self):
        self.capital_dao = capital_dao.capital_dao()


    """获取每日活跃营业部 买卖股票信息"""
    def get_active_sale_department(self):

        current_day = date_time_util.get_date(0)
        count = "500"
        # 查询当日活跃营业部
        url = crawl_html_url.east_money_active_sale_department.format(count,current_day,current_day)
        data = requests.get(url)
        sales_department = json.loads(data.text[15:])["data"]
        # 遍历每个营业部买卖股票
        for sale_department in sales_department:
            department_code = sale_department["YybCode"]
            stocks = sale_department["SName"]
            if stocks == '':
                continue
            stock_arry = json.loads(stocks)

            #查询改营业部下 每个股票的资金流入
            single_stocks_capital = json.loads(requests.get(crawl_html_url.east_money_active_sale_department_trade_stock_money.format(len(stock_arry),department_code)).text[13:])["data"]
            for stock_capital in single_stocks_capital:
                param = []
                param.append(stock_capital["SalesName"])
                param.append(stock_capital["SalesCode"])
                param.append(stock_capital["SName"])
                param.append(stock_capital["SCode"])
                param.append(stock_capital["TDate"])
                param.append(stock_capital["CTypeDes"])
                param.append( 0 if stock_capital["BMoney"] == '' else stock_capital["BMoney"])
                param.append(0 if stock_capital["SMoney"] == '' else stock_capital["SMoney"])
                param.append(0 if stock_capital["PBuy"] == '' else stock_capital["PBuy"])
                self.capital_dao.add_sale_department_trade(param)

    """查询营业部买卖股票资金流情况"""
    def query_sale_department_capital_flow(self):
        data = self.capital_dao.query_sale_department_capital()
        return data

# a = money_flow()
# a.get_active_sale_department()

