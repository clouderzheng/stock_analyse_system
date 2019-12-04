import requests
from python.service import crawl_html_url
import json
import time
from python.domain import snow_ball_bean
from python.service import stock_service
from python.util import get_characters_letters,date_time_util
import logging
from python.redis import redis_pool,redis_key_constants
from python.dao import stock_strategy_dao

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/51.0.2704.63 Safari/537.36'}

"""获取雪球仓位组合"""
def get_stock_position_combination(begin_time = date_time_util.get_date_time(-1),end_time = date_time_util.get_date_time(0),page = 1,total = 100):

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
                    stock_info = [postion["stock_name"], postion["stock_symbol"], postion["price"], 0,2]
                    stock_strategy_dao.stock_strategy().save_other_strategy_choose(stock_info)

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
            stock_info = [stock["name"], stock["symbol"], stock["current"], stock["percent"], 1]
            stock_strategy_dao.stock_strategy().save_other_strategy_choose(stock_info)
    return result

"""获取最新股票信息 判断是否需要更新数据库存储"""
def get_stock_last_info():

    logging.info("开始同步最新股票信息")
    session = requests.session()
    session.get(crawl_html_url.snow_ball_main_url, headers=headers)
    html = session.get(crawl_html_url.snow_ball_stock_all_info.format(2), headers=headers)
    last_count = json.loads(html.text)['data']['count']

    local_count = stock_service.get_stock_count()

    # 判断本地与 最新股票数量是否相等 不相等删除原信息 重新 插入

    if(local_count != last_count):
        # 删除原信息
        # stock_service.delete_stock()
        new_count = last_count - local_count
        logging.info("-------------有"+str(new_count)+"支新股上市 开始更新--------------")
        html = session.get(crawl_html_url.snow_ball_stock_all_info.format(new_count), headers=headers)
        data_list = json.loads(html.text)['data']['list']
        stock_list = []

        redis = redis_pool.RedisPool()
        """更新最新信息到数据库"""
        for stock in data_list:
            stock_list.append((stock['name'],stock['symbol'],stock['symbol'][2:],get_characters_letters.getPinyin(stock['name'])))
            """保存股票代码与名称到redis"""
            redis.hset(redis_key_constants.stock_name_code_mapping,stock['symbol'],stock['name'])
        stock_service.add_stock_list(stock_list)

