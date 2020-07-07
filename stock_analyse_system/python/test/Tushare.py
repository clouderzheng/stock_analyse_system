import tushare as ts

def get_tick_data(stock_code,date):
    data = ts.get_tick_data(stock_code, date, src='tt')

    return data
# data = get_tick_data("002137","2020-06-02")
#
# print(data.head(10))
# print(data.iloc[0,3])



# data = get_tick_data("002309","2020-03-24")
# print(data)

import json
import requests



res = requests.get("https://flash-api.xuangubao.cn/api/pool/detail?pool_name=limit_up&date=2020-03-18")
res.encoding = "utf-8"
datas = json.loads(res.text)
datas = datas["data"]
for data in datas:
    print(data["stock_chi_name"])