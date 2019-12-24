from python.util import date_time_util
from python.service import crawl_html_url
import requests
import json

"""资金流向service"""
class money_flow:

    def __init__(self):
        pass


    """获取每日活跃营业部"""
    def get_active_sale_department(self):

        current_day = date_time_util.get_date(0)
        count = "500"
        url = crawl_html_url.east_money_active_sale_department.format(count,current_day,current_day)
        data = requests.get(url)
        data = json.loads(data.text[15:])
        print(data["data"])
        pass

a = money_flow()
a.get_active_sale_department()

