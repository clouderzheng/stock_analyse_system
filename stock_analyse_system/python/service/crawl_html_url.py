# 雪球网站地址
"""获取投资者列表"""
snow_ball_position_url = "https://xueqiu.com/cubes/discover/rank/cube/list.json?category=14&page={}&count={}"
"""雪球首页 当做登陆 会话使用"""
snow_ball_main_url = "https://xueqiu.com/"
"""获取指定投资者仓位"""
snow_ball_investor_url = "https://xueqiu.com/cubes/rebalancing/show_origin.json?rb_id={}"

"""雪球股票信息数据"""
snow_ball_stock_info_url="https://xueqiu.com/service/v5/stock/screener/quote/list?page=1&size={}&order=desc&orderby=percent&order_by=percent&market=CN&type=sh_sz&_=1568860118055"



# 新浪地址
sina_comment_url= "http://finance.sina.com.cn/roll/index.d.html?cid=56589&page={}"