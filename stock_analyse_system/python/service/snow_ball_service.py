import requests
import crawl_html_url
import json
import time
import snow_ball_bean
import stock_service
from mysql_pool import  sql_pool
import datetime
import get_characters_letters

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/51.0.2704.63 Safari/537.36'}

"""获取雪球仓位组合"""
def get_stock_position_combination(begin_time,end_time,page = 1,total = 50):

    begin_time_timestamp = int(time.mktime(time.strptime(begin_time , "%Y-%m-%d %H:%M:%S"))) * 1000
    end_time_timestamp = int(time.mktime(time.strptime(end_time , "%Y-%m-%d %H:%M:%S"))) * 1000

    """禁止直接访问模拟 浏览器请求"""

    """使用会话连接 每次访问必须先访问主页"""
    session = requests.session()
    session.get(crawl_html_url.snow_ball_main_url,headers = headers)
    """获取真正有效数据"""
    html_data = session.get(crawl_html_url.snow_ball_position_url.format(str(page),str(total)),headers = headers)
    data = json.loads(html_data.text)
    combinations_list = data['list']

    result = {}
    """遍历投资者"""
    for conbination in combinations_list:
        """更新时间在指定时间内的才进行查询仓位操作"""
        if(conbination["updated_at"] > begin_time_timestamp and conbination["updated_at"] < end_time_timestamp):
            user_id = str(conbination["last_user_rb_gid"])
            """获取仓位数据"""
            investor_html_data = session.get(crawl_html_url.snow_ball_investor_url.format(user_id),headers = headers)
            investor_data = json.loads(investor_html_data.text)
            position_list = investor_data["rebalancing"]["rebalancing_histories"]
            """遍历仓位变动数据"""
            for postion in position_list:
                """volume表示买进"""
                if(postion["volume"] > 0):

                    stock_name = postion["stock_name"]
                    stock_code = postion["stock_symbol"]
                    bean = result.get(stock_name)
                    if(None == bean):
                        bean = snow_ball_bean.snowball_stock_info(stock_name,stock_code,1)
                        result[stock_name] = bean
                    else:
                        bean.count = bean.stock_count + 1
                    stock_info = (postion["stock_name"], postion["stock_symbol"], postion["price"], 0, datetime.datetime.today(), \
                    datetime.datetime.today(), 2)
                    save_strategy_stock_info(stock_info)

    return result
"""获取早盘竞价信息"""
def get_biding_info(count = 30,max_gain = 4,min_gain = 2):
    session = requests.session()
    session.get(crawl_html_url.snow_ball_main_url, headers=headers)
    html_data = session.get(crawl_html_url.snow_ball_stock_info_url.format(4000), headers=headers)
    data = json.loads(html_data.text)
    stock_list = data["data"]["list"]
    result = []

    sort_array = []
    """去除停盘的 停盘的没有交易量 无法比较"""
    for stock  in stock_list:
        if(stock['volume'] != None):
            sort_array.append(stock)
    """根据成交量排序"""
    sorts_list = sorted(sort_array,key=lambda x : x['volume'],reverse=True)
    """获取指定排名前面的数据"""
    before_list = sorts_list[0:count]
    for stock in before_list:
        percent = stock["percent"]
        """判断该股票涨幅是否在 指定区间内"""
        if(percent > min_gain and percent < max_gain):
            result.append(stock)
            #持久化数据到mysql
            stock_info = (stock["name"], stock["symbol"], stock["current"], stock["percent"],datetime.datetime.today(),datetime.datetime.today(), 1)
            save_strategy_stock_info(stock_info)
    return result


"""持久化策略数据"""
def save_strategy_stock_info(stock_info):
    # stock_info = (stock["name"],stock["symbol"],stock["current"],stock["percent"],stock["symbol"],time.time(),time.time(),1)
    sql = "insert into trade_strategy_record (stock_name,stock_code,current_price,current_rate,strategy_category ) \
          value (%s,%s,%s,%s,%s) "
    con = sql_pool().get_connection()
    cursor = con.cursor()
    cursor.execute(sql, stock_info)
    cursor.connection.commit()
    con.close()

# stock_info = ("光大银行","SH601818",4.09,3.81,datetime.datetime.today(),datetime.datetime.today(),1)
# save_strategy_stock_info(stock_info)
"""获取回调到支撑位的股票"""
def get_call_back_support_stock(call_back_day = 60,exclude_day = 20,float_per = 2):
    # 获取所有股票
    stock_list = stock_service.get_stock_info()

    # 获取此时时间
    current_time = int(time.time() * 1000)


    stock_array = []
    for stock in stock_list:
        try:
            session = requests.session()
            session.get(crawl_html_url.snow_ball_main_url, headers=headers)
            html_data = session.get(crawl_html_url.snow_ball_single_stock_info_url.format(stock["area_stock_code"],current_time,call_back_day), headers=headers)
            data = json.loads(html_data.text)
            items = data["data"]["item"]

            """查询结果小于回溯天数 可能是新股 跳过"""
            if(len(items) < call_back_day):
                continue
            #获取此时最低价
            current_low_price = items[call_back_day - 1][4]
            #获取此时最新报价
            current_new_price = items[call_back_day - 1][5]
            # 获取此时最低价时间
            current_low_day = items[call_back_day - 1][0]

            # 将排除之后的日期根据最高价排序
            last_days = items[:(call_back_day - exclude_day)]
            sorts_list = sorted(last_days, key=lambda x: x[3], reverse=True)
            # 获取上个高点价格
            last_high_price = sorts_list[0][3]
            # 获取上个高点时间
            last_high_day = sorts_list[0][0]

            # 计算两个价格之间的相差波动率
            percent = (current_low_price - last_high_price)/ last_high_day
            # 判断计算结果是否在指定区间内
            if(percent < float_per):
                stock_info = {"current_new_price" : current_new_price,"current_low_price" : current_low_price,"current_low_day":current_low_day,"last_high_price":last_high_price,"last_high_day":last_high_day,\
                              "stock_name":stock["stock_name"],"area_stock_code":stock["area_stock_code"],"percent":round(percent * 100,2)}

                stock_array.append(stock_info)
        except Exception:
            print(stock)
    return stock_array


"""获取最新股票信息 判断是否需要更新数据库存储"""
def get_stock_last_info():
    # html = requests.get(crawl_html_url.snow_ball_stock_all_info.format(2))
    session = requests.session()
    session.get(crawl_html_url.snow_ball_main_url, headers=headers)
    html = session.get(crawl_html_url.snow_ball_stock_all_info.format(2), headers=headers)
    last_count = json.loads(html.text)['data']['count']

    local_count = stock_service.get_stock_count()

    # 判断本地与 最新股票数量是否相等 不相等删除原信息 重新 插入
    if(local_count != last_count):
        # 删除原信息
        stock_service.delete_stock()
        html = session.get(crawl_html_url.snow_ball_stock_all_info.format(last_count), headers=headers)
        data_list = json.loads(html.text)['data']['list']
        stock_list = []
        for stock in data_list:
            stock_list.append((stock['name'],stock['symbol'],stock['symbol'][2:],get_characters_letters.getPinyin(stock['name'])))
        stock_service.add_stock_list(stock_list)

# get_stock_last_info()

# list = get_biding_info(30,4,2)
# for stock in list:
#     print(stock["name"])
# combination = get_stock_position_combination("2019-09-05 00:15:23", "2019-09-06 14:15:23", total=60)
# for key in combination:
#     print(key,":",combination[key].stock_name,combination[key].stock_code,combination[key].stock_count,)
#
# import time
# current = int(time.time())
#
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current)))
#
# current = current - 60 * 60 * 24 * 5
# print(current)
# print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(current)))

# session = requests.session()
# session.get(crawl_html_url.snow_ball_main_url, headers=headers)
# html_data = session.get("https://stock.xueqiu.com/v5/stock/chart/kline.json?symbol=SZ300085&begin=1569310406000&period=day&type=before&count=-60&indicator=kline,pe,pb,ps,pcf,market_capital,agt,ggt,balance", headers=headers)
# data = json.loads(html_data.text)
# items = data["data"]["item"]
# current_low_price = items[60 - 1][4]
# print(current_low_price)
# last_days = items[:(60 - 20)]
#
# print(last_days)
# sorts_list = sorted(last_days, key=lambda x: x[3], reverse=True)
# print(sorts_list)

# result = {"name":"night","age":25}
# print(result.get("name1"))