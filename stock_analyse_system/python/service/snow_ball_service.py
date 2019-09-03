import requests
import crawl_html_url
import json
def get_stock_position_combination():
    """禁止直接访问模拟 浏览器请求"""
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) '\
                             'Chrome/51.0.2704.63 Safari/537.36'}
    """使用会话连接 每次访问必须先访问主页"""
    session = requests.session()
    session.get(crawl_html_url.snow_ball_main_url,headers = headers)
    """获取真正有效数据"""
    html_data = session.get(crawl_html_url.snow_ball_position_url,headers = headers)
    data = json.loads(html_data.text)
    combinations_list = data['list']
    for conbination in combinations_list:
        print(conbination)


print(get_stock_position_combination())