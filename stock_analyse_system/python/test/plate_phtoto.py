from python.mysql import mysql_pool
import matplotlib.pyplot as plt
pool = mysql_pool.sql_pool()
import traceback

""""
获取所有版块
"""
def get_all_plate():
    sql = "select stock_name,stock_code from stock_plate_info  "
    datas = pool.selectMany(sql)
    return datas


"""
获取指定版块  2014-7.22 - 2015.6.12
2019.1.4 - 2019.4.19
"""
def get_special_plate(stockcode,begindate = "2014-7.22",enddate = "2015.6.12"):
    sql = "select close_price from stock_plate_hostory_data where stock_code = %s and  `current_date` > %s  and  `current_date` < %s order  by  `current_date` "
    datas = pool.selectMany(sql,(stockcode,begindate,enddate))
    return  datas
"""
获取区间内时间  2014-7.22 - 2015.6.12
2019.1.4 - 2019.4.19
"""
def get_time(begindate = "2014-7.22",enddate = "2015.6.12"):
    sql = "select `current_date` from stock_plate_hostory_data where   `current_date` > %s  and  `current_date` < %s group  by `current_date` order  by  `current_date` "
    datas = pool.selectMany(sql,(begindate,enddate))
    times = []
    for time in datas:
        times.append(time['current_date'])
    return  times


"""
获取所有版块数据
"""
def get_all_plate_info():
    plates = get_all_plate()
    plate_infos = {}
    for plate in plates:
        stocks = get_special_plate(plate["stock_code"])
        prices = []
        for  price in stocks:
            prices.append(price['close_price'])
        plate_infos[plate["stock_name"]] = prices
    return plate_infos

plate_infos = get_all_plate_info()
plate_times = get_time()
for plate_info in plate_infos:
    try:
        plt.plot(plate_times, plate_infos[plate_info], label=plate_info)
    except  Exception as e:
        print(plate_info)
        traceback.print_exc()

plt.legend() # 显示图例

plt.xlabel('iteration times')
plt.ylabel('rate')
plt.show()
