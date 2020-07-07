from python.mysql import mysql_pool
from python.util import scale_util
import decimal

pool = mysql_pool.sql_pool()

print("分析涨停板数据，时间范围2016-02-02 ---- 2020-04-27")

# 查询最高价等于2板的个数
continuous_time = "2"
# sql = "select count(1) as total from stock_limit_up_history WHERE continuous_time = "+continuous_time+"  and  `current_date`  > '2016-02-02' "
#
# max_price_total = pool.selectOne(sql)["total"]
# print("最高价涨停" +continuous_time+"板:"+ str(max_price_total))
#
# sql = sql +" and close_price = max_price"
# close_price_total = pool.selectOne(sql)["total"]
# print("收盘价涨停" +continuous_time+"板:"+ str(close_price_total))
# print(continuous_time+"板破板率:",round(decimal.Decimal( max_price_total - close_price_total).__truediv__(max_price_total),2))
def get_limit_up():
    # 爬取指定板数的涨停板分析
    sql = "select stock_name,stock_code,`current_date`,`open_price`,`min_price`,`max_price`,`close_price` from stock_limit_up_history WHERE continuous_time = "+continuous_time+"  and  `current_date`  >= '2019-12-02'    and close_price = max_price"
    stocks = pool.selectMany(sql)
    for stock in stocks:
        sql = "select open_price,max_price,min_price,close_price from stock_hostory_data where stock_code = " + stock["stock_code"] + " and `current_date` > '" +stock["current_date"] +"' order by `current_date` limit 2"
        _stocks = pool.selectMany(sql)
        if(len(_stocks) < 2):
            continue
        sql = "insert into stock_limit_up_statistics(stock_code,stock_name,`create_date`, `continuous_time`,\
        `one_open_price`,`one_max_price`,`one_min_price`,`one_close_price`,\
        `two_open_price`,`two_max_price`,`two_min_price`,`two_close_price`,\
        `third_open_price`,`third_max_price`,`third_min_price`,`third_close_price`) values( \
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        param = []
        param.append(stock["stock_code"])
        param.append(stock["stock_name"])
        param.append(stock["current_date"])
        param.append(continuous_time)
        param.append(stock["open_price"])
        param.append(stock["max_price"])
        param.append(stock["min_price"])
        param.append(stock["close_price"])

        param.append(_stocks[0]["open_price"])
        param.append(_stocks[0]["max_price"])
        param.append(_stocks[0]["min_price"])
        param.append(_stocks[0]["close_price"])
        param.append(_stocks[1]["open_price"])
        param.append(_stocks[1]["max_price"])
        param.append(_stocks[1]["min_price"])
        param.append(_stocks[1]["close_price"])
        pool.insert(sql,param)

def analyse_limit_up():
    basesql = "select count(1) as total from stock_limit_up_statistics"
    continuous_count = pool.selectOne(basesql)["total"]
    print(continuous_time,"板个数",continuous_count)

    print("-----以下统计包含一字板-------")
    # 最高涨停
    sql = basesql + " where two_limit_up_price = two_max_price"
    max_limit_up = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1, "板个数（最高价涨停）", max_limit_up)

    # 收盘价涨停
    sql = basesql +" where two_limit_up_price = two_close_price"
    _continuous_count = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1,"板个数（收盘价涨停）",_continuous_count)


    sql = basesql +" where two_open_price = two_limit_up_price"
    wordboard = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1,"板一字板开盘个数",wordboard)

    sql = basesql +" where two_open_price = two_limit_up_price and two_limit_up_price = two_close_price "
    wordboard = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1,"板一字板收盘个数",wordboard)

    print("-----以下统计不包含一字板-------")
    print("-----2板盈利粗略统计-------")
    basesql = "select count(1) as total from stock_limit_up_statistics where  two_open_price != two_limit_up_price "
    continuous_count = pool.selectOne(basesql)["total"]
    print(continuous_time, "板个数（排除一字板分析）", continuous_count)
    # 最高涨停
    sql = basesql + " and two_limit_up_price = two_max_price"
    max_limit_up = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1, "板个数（最高价涨停）", max_limit_up)

    # 收盘价涨停
    sql = basesql + " and  two_limit_up_price = two_close_price"
    _continuous_count = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1, "板个数（收盘价涨停）", _continuous_count)


    sql = basesql + " and third_open_price > two_open_price"
    morning_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买早卖）买卖策略：盈利个数：", morning_bid)

    _base_sql = "select sum( (third_open_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  "
    morning_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买早卖）买卖策略：盈利幅度：",morning_bid_rate)

    sql = basesql + " and third_close_price > two_open_price"
    afternoon_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买晚卖）买卖策略：盈利个数：",afternoon_bid)

    _base_sql = "select sum( (third_close_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  "
    afternoon_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买晚卖）买卖策略：盈利幅度：",afternoon_bid_rate)


    sql = basesql + " and third_max_price > two_open_price"
    halfway_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买中途择机卖（即有最高价大于买入价））买卖策略：盈利个数：",halfway_bid)

    _base_sql = "select sum( (third_max_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  "
    halfway_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买中途择机卖（即有最高价大于买入价））买卖策略：盈利幅度：", halfway_bid_rate)


    # max_rate = "-0.05"
    # min_rate = "-0.1"
    # statistics_diff_rate(min_rate,max_rate)
    #
    # max_rate = "0"
    # min_rate = "-0.05"
    # statistics_diff_rate(min_rate, max_rate)
    #
    #
    # max_rate = "0.05"
    # min_rate = "0"
    # statistics_diff_rate(min_rate, max_rate)
    #
    # max_rate = "0.1"
    # min_rate = "0.05"
    # statistics_diff_rate(min_rate, max_rate)
    #
    # max_rate = "0.02"
    # min_rate = "-0.02"
    # statistics_diff_rate(min_rate, max_rate)
    #
    # max_rate = "0.01"
    # min_rate = "-0.01"
    # statistics_diff_rate(min_rate, max_rate)
    #
    # max_rate = "0.03"
    # min_rate = "0"
    # statistics_diff_rate(min_rate, max_rate)
    #
    # max_rate = "0.01"
    # min_rate = "-0.02"
    # statistics_diff_rate(min_rate, max_rate)

    max_rate = "-0.01"
    min_rate = "-0.05"
    statistics_diff_rate(min_rate, max_rate)

    max_rate = "-0"
    min_rate = "-0.05"
    statistics_diff_rate(min_rate, max_rate)



    max_rate = "-0.005"
    min_rate = "-0.05"
    statistics_diff_rate(min_rate, max_rate)


#不同 买入区间范围统计
def statistics_diff_rate(min_rate,max_rate):
    print("-----2板竞价买卖策略（指定区间：" + min_rate + "%  -  " + max_rate + "%））-----------")
    condition = "	AND ( ( two_open_price - one_close_price ) / one_close_price ) <=  " + max_rate + " and ( ( two_open_price - one_close_price ) / one_close_price ) >= " + min_rate
    basesql = "select count(1) as total from stock_limit_up_statistics where  two_open_price != two_limit_up_price  " + condition

    continuous_count = pool.selectOne(basesql)["total"]
    print(continuous_time, "板个数", continuous_count)
    # 最高涨停
    sql = basesql + " and two_limit_up_price = two_max_price"
    max_limit_up = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1, "板个数（最高价涨停）", max_limit_up)

    # 收盘价涨停
    sql = basesql + " and  two_limit_up_price = two_close_price"
    _continuous_count = pool.selectOne(sql)["total"]
    print(int(continuous_time) + 1, "板个数（收盘价涨停）", _continuous_count)

    sql = basesql + " and third_open_price > two_open_price"
    morning_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买早卖）买卖策略：盈利个数：", morning_bid,"盈利率：",  morning_bid/continuous_count)

    _base_sql = "select sum( (third_open_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  " + condition
    morning_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买早卖）买卖策略：盈利幅度：", morning_bid_rate)

    sql = basesql + " and third_close_price > two_open_price"
    afternoon_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买晚卖）买卖策略：盈利个数：", afternoon_bid,"盈利率：", afternoon_bid/continuous_count)

    _base_sql = "select sum( (third_close_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  " + condition
    afternoon_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买晚卖）买卖策略：盈利幅度：", afternoon_bid_rate)

    sql = basesql + " and third_max_price > two_open_price"
    halfway_bid = pool.selectOne(sql)["total"]
    print("2板竞价（早买中途择机卖（即有最高价大于买入价））买卖策略：盈利个数：", halfway_bid,"盈利率：",  halfway_bid/continuous_count)

    _base_sql = "select sum((third_max_price - two_open_price) / two_open_price ) as ss from stock_limit_up_statistics  where two_open_price != two_limit_up_price  " + condition
    halfway_bid_rate = pool.selectOne(_base_sql)["ss"]
    print("2板竞价（早买中途择机卖（即有最高价大于买入价））买卖策略：盈利幅度：", halfway_bid_rate)





analyse_limit_up()

def turnup():
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停个数",total)
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and third_open_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停,第三天开盘价高于上一天收盘价个数",total)
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and third_close_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停,第三天收盘价高于上一天收盘价个数",total)

    sql = "select sum(( third_close_price - two_close_price) / two_close_price) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and third_close_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停,第三天收盘价卖出盈利幅度", total)
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and third_max_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停,第三天最高价高于上一天收盘价个数", total)

    sql = "select sum(( third_max_price - two_close_price) / two_close_price) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and third_close_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停,第三天收盘价卖出盈利幅度", total)

    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price "
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红个数", total)

    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_open_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天早盘竞价卖出盈利个数", total)

    sql = "select sum( ( third_open_price - two_close_price )/ two_close_price) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_open_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天早盘竞价卖出盈利幅度", total)
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_close_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天收盘竞价卖出盈利个数", total)
    sql = "select sum( ( third_close_price - two_close_price )/ two_close_price) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_open_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天收盘竞价卖出盈利幅度", total)
    sql = "select count(1) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_max_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天最高价卖出盈利个数", total)
    sql = "select sum( ( third_max_price - two_close_price )/ two_close_price) total from stock_limit_up_statistics where one_open_price = one_close_price and two_close_price != two_limit_up_price and two_close_price > one_close_price and third_open_price > two_close_price"
    total = pool.selectOne(sql)["total"]
    print("2板一字板，当天未涨停，收红，第三天最高价卖出盈利幅度", total)

# turnup()

