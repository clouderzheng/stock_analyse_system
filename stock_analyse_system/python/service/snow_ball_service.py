import requests
import crawl_html_url
import json
import time
import snow_ball_bean

"""获取雪球仓位组合"""
def get_stock_position_combination(begin_time,end_time,page = 1,total = 1):

    begin_time_timestamp = int(time.mktime(time.strptime(begin_time , "%Y-%m-%d %H:%M:%S"))) * 1000
    end_time_timestamp = int(time.mktime(time.strptime(end_time , "%Y-%m-%d %H:%M:%S"))) * 1000

    """禁止直接访问模拟 浏览器请求"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
                             'Chrome/51.0.2704.63 Safari/537.36'}

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
    return result


combination = get_stock_position_combination("2019-09-05 00:15:23", "2019-09-06 14:15:23", total=60)
for key in combination:
    print(key,":",combination[key].stock_name,combination[key].stock_code,combination[key].stock_count,)
