import requests
import json
import time
import matplotlib.pyplot as plt



headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                         'Chrome/51.0.2704.63 Safari/537.36'}

def get_minute_data():
    session = requests.session()

    """爬取其他网页必须先首页登陆"""
    session.get("https://xueqiu.com/",headers = headers)
    """爬取上证指数"""
    url_data = session.get("https://stock.xueqiu.com/v5/stock/chart/minute.json?symbol=SH000001&period=1d", headers=headers)

    print(url_data)
    data = json.loads(url_data.text)
    items = data["data"]["items"]

    y_data = []
    x_data = []
    for item in items:
        """指数"""
        y_data.append(item["current"])
        """时间"""
        x_data.append(time.strftime("%H:%M", time.localtime(item["timestamp"]/1000)).format("%h:%m"))

    print(y_data)
    print(x_data)
    plt.plot(x_data, y_data, label='上证分时图')
    plt.xlabel('指数')
    plt.ylabel('time')
    plt.title('上证指数分时图')
    plt.legend()
    plt.show()

    print(data)

get_minute_data()
