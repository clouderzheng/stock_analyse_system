from python.mysql import mysql_pool
import xlwt
from python.test import Tushare
import tushare as ts
from decimal import *
import traceback
from python.util import scale_util

limit_date = "2020-06-01"

def get_stock_data(time):
    # 查询最近2板股票
    sql = "SELECT stock_code,stock_name,create_date,current_price from stock_limit_up_analyse WHERE continuous_time = "+time+" AND stock_name not like '%ST%' and create_date < '" +limit_date+"' "
    pool = mysql_pool.sql_pool()
    data = pool.selectMany(sql)
    writebook = xlwt.Workbook()  # 打开excel
    test = writebook.add_sheet('two_time_stock')

    # 定义时间格式
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy-mm-dd'

    # 定义表头
    test.write(0, 0, "股票代码")
    test.write(0, 1, "股票名称")
    test.write(0, 2, "涨停时间")
    test.write(0, 3, "1进2竞价量")
    test.write(0, 4, "2进3竞价量")
    test.write(0, 5, "一字板（1是2否）")
    test.write(0, 6, "开盘幅度")
    test.write(0, 7, "最高幅度")
    test.write(0, 8, "最低幅度")
    test.write(0, 9, "收盘幅度")
    test.write(0, 10, "3板成功（1是2否）")



    index = 1
    for stock in data:
        try:
            test.write(index, 0, stock["stock_code"])
            test.write(index, 1, stock["stock_name"])
            test.write(index, 2, stock["create_date"],dateFormat)
            # 查询1进2 竞价量
            two_volume = Tushare.get_tick_data(stock["stock_code"][0:6],str(stock["create_date"])).iloc[0,3]
            test.write(index, 3, int(two_volume))

            # 查询下个交易日
            sql = "select create_date from stock_limit_up_analyse where create_date > '"+ str(stock["create_date"])+"' group by create_date order by create_date limit 1"
            next_date = str(pool.selectOne(sql)["create_date"])
            # 查询2进3 竞价信息
            three_data = Tushare.get_tick_data(stock["stock_code"][0:6],next_date)
            # 查询2进3 竞价量
            three_volume = three_data.iloc[0,3]
            test.write(index, 4, int(three_volume))

            limit_up_price = scale_util.round_up((float(stock["current_price"]) * 1.1) ,2)
            # 获取2进3开盘价
            three_open_price = three_data.iloc[0,1]

            if limit_up_price == three_open_price:
                test.write(index, 5, 1)
            else:
                test.write(index, 5, 2)

            # 获取2进3 价格信息
            day_data = ts.get_hist_data(stock["stock_code"][0:6], start=next_date, end=next_date)

            three_open_price = day_data.iloc[0,0]
            three_max_price = day_data.iloc[0,1]
            three_close_price = day_data.iloc[0,2]
            three_min_price = day_data.iloc[0,3]
            last_price = float(stock["current_price"])
            test.write(index, 6,  scale_util.round_up(((three_open_price - last_price)/last_price) ,2))
            test.write(index, 7,  scale_util.round_up(((three_max_price - last_price)/last_price ) ,2))
            test.write(index, 8,  scale_util.round_up(((three_min_price - last_price)/last_price ) ,2))
            test.write(index, 9,  scale_util.round_up(((three_close_price - last_price)/last_price) ,2))
            if limit_up_price == three_close_price:
                test.write(index, 10, 1)
            else:
                test.write(index, 10, 2)
        except Exception as e:
            print("异常信息---->",stock)
            traceback.print_exc()
        index += 1
    writebook.save('stock.xls')

get_stock_data("2")


# 尾盘竞价买入1进2失败策略
def after_bid_strategy(time):
    # 查询指定连板数的股票信息
    sql = "SELECT stock_code,stock_name,create_date,current_price from stock_limit_up_analyse WHERE continuous_time = " + time + " AND stock_name not like '%ST%' and create_date < '" + limit_date + "' "
    pool = mysql_pool.sql_pool()
    stocks = pool.selectMany(sql)

    writebook = xlwt.Workbook()  # 打开excel
    test = writebook.add_sheet('after_bid_stock')

    # 定义时间格式
    dateFormat = xlwt.XFStyle()
    dateFormat.num_format_str = 'yyyy-mm-dd'

    # 定义表头
    test.write(0, 0, "股票代码")
    test.write(0, 1, "股票名称")
    test.write(0, 2, "涨停时间")
    test.write(0, 6, "第二天开盘幅度")
    test.write(0, 7, "第二天最高幅度")
    test.write(0, 8, "第二天最低幅度")
    test.write(0, 9, "第二天收盘幅度")
    test.write(0, 10, "第二天涨停（1是2否）")
    test.write(0, 6, "第三天开盘幅度")
    test.write(0, 7, "第三天最高幅度")
    test.write(0, 8, "第三天最低幅度")
    test.write(0, 9, "第三天收盘幅度")

    # 依此遍历复盘股票
    # for stock in stocks:




# day_data = ts.get_hist_data("300576", start="2020-05-20", end="2020-05-20")
# print(day_data)
# print(day_data.iloc[0,0])