
import requests
import json

from python.mysql import mysql_pool
from python.util import scale_util,date_time_util
def get_tick_data(stocks):

    for stock in stocks:
        stock_code = stock["stock_code"][:6]
        url = "http://push2ex.eastmoney.com/getStockFenShi?pagesize=14400&ut=7eea3edcaed734bea9cbfc24409ed989&dpt=wzfscj&pageindex=0&id=3007122&sort=1&ft=1&code={}&market={}&_=1589466838125"

        if stock_code.startswith("6"):
            url = url.format(stock_code,1)
        else:
            url = url.format(stock_code,0)

        data = json.loads(requests.get(url).text)["data"]["data"]

        _count_price = 0
        _count_amount = 0
        for _data in data:
            price = int(_data["p"])
            amount = int(_data["v"])
            _count_price += price * amount
            _count_amount += amount

        _price = scale_util.round_up((_count_price/_count_amount)/1000,2)
        _close_price = int(data[-1]["p"])/1000
        _profit = scale_util.round_up((_close_price - _price)/_price,2)
        print(stock["stock_name"]," 平均成交价格/收盘价/盈利率：",_price,_close_price,_profit)

# 获取当天2板涨停板数据
def get_today_two_limit_up():

    pool = mysql_pool.sql_pool()
    today = date_time_util.get_date(0)
    today = "2020-05-15"
    print(today)
    sql = "select stock_name,stock_code from stock_limit_up_analyse where continuous_time = 2  and stock_name not like '%ST%'and create_date = '" + today +"'"
    res = pool.selectMany(sql)

    return res


stocks = get_today_two_limit_up()

get_tick_data(stocks)

# stocks= []
# stocks.append({"stock_name":"智度股份","stock_code":"000676"})
# stocks.append({"stock_name":"亚翔集成","stock_code":"603929"})
# stocks.append({"stock_name":"乐心医疗","stock_code":"300562"})
# stocks.append({"stock_name":"智度股份","stock_code":"000676"})
# get_tick_data(stocks)