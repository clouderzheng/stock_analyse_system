from python.mysql import mysql_pool
from python.util import  scale_util


pool = mysql_pool.sql_pool()


# 尾盘竞价
def afternoon_bid():
    # 统计二板晋级失败的  尾盘竞价买入盈利
    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数，盈利比率：",res["total"],res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  >= 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（纯盈利），盈利比率：",res["total"],res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  < 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（纯亏损），盈利比率：",res["total"],res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  >= 0  and ((two_close_price - one_close_price ) / one_close_price)  >= 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（收盘价为正纯盈利），盈利比率：", res["total"], res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  >= 0  and ((two_close_price - one_close_price ) / one_close_price)  < 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（收盘价为负纯盈利），盈利比率：", res["total"], res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  < 0 and ((two_close_price - one_close_price ) / one_close_price)  >= 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（收盘价为正纯亏损），盈利比率：", res["total"], res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  < 0 and ((two_close_price - one_close_price ) / one_close_price)  < 0"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（收盘价为正纯亏损），盈利比率：", res["total"], res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and two_max_price = two_limit_up_price"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（破板的），盈利比率：",res["total"],res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  >= 0 and two_max_price = two_limit_up_price"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（破板的盈利），盈利比率：",res["total"],res["profit"])

    sql = "select count(1) total,sum((third_max_price - two_close_price ) / two_close_price) profit from stock_limit_up_statistics where two_close_price != two_limit_up_price  and ((third_max_price - two_close_price ) / two_close_price)  < 0 and two_max_price = two_limit_up_price"
    res = pool.selectOne(sql)
    print("2板尾盘买入，第三天最高价卖出，操作个数（破板的亏损），盈利比率：",res["total"],res["profit"])



# 基本信息统计
def base_statistics():
    # 2板个数
    basesql = "select count(1) total from stock_limit_up_statistics"
    total_ = pool.selectOne(basesql)["total"]

    print("2板个数",total_)
    # 3板个数
    sql = basesql + " where  two_close_price = two_limit_up_price"
    total_ = pool.selectOne(sql)["total"]

    print("3板个数", total_)
    # 2板未晋级个数
    sql = basesql + " where  two_close_price != two_limit_up_price"

    total_ = pool.selectOne(sql)["total"]

    print("2板失败个数", total_)

base_statistics()
print("以下统计都是基于2进3失败的")
afternoon_bid()