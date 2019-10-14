import datetime
import time
"""获取基于当天时间间隔的时间字符串
负数表示历史时间
整数表示未来时间
当天时间0
"""
def get_date_time(interval):
    return (datetime.datetime.today() + datetime.timedelta(interval)).strftime("%Y-%m-%d %H:%M:%S")

def get_date(interval):
    return (datetime.datetime.today() + datetime.timedelta(interval)).strftime("%Y-%m-%d")
def get_date_time_line(interval):
    return (datetime.datetime.today() + datetime.timedelta(interval)).strftime("%Y-%m-%d-%H-%M-%S")

"""获取毫秒时间戳"""
def get_timestamp_mill_second():
    return int(time.time()) * 1000