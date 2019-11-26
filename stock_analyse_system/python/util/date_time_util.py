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

"""获取基于指定日期的前几个工作日的日期"""
def get_work_date(interval,current_day = None):
    # 往前追溯时间索引
    current_index = -1
    # 没有传入指定日期 默认使用当天日期
    if current_day == None:
        # 获取当天时间
        current_day = datetime.datetime.today()
    last_day = None
    for index in range(7):
        # 获取追溯日期
        last_day = current_day + datetime.timedelta(current_index)
        # 追溯日期索引减1
        current_index = current_index - 1
        # 计算当天是星期几
        week_day  = last_day.weekday()
        # 不是休息日 追溯日期减一
        if(week_day < 6):
            interval = interval -1
        # 追溯日期小于1  结束
        if(interval < 0):
            break
    return last_day.strftime("%Y-%m-%d")

"""获取基于指定日期的后几个工作日的日期"""
def get_work_date_after(interval,current_day = None):
    # 往前追溯时间索引
    current_index = 1
    # 没有传入指定日期 默认使用当天日期
    if current_day == None:
        # 获取当天时间
        current_day = datetime.datetime.today()
    last_day = None
    for index in range(7):
        # 获取追溯日期
        last_day = current_day + datetime.timedelta(current_index)
        # 追溯日期索引减1
        current_index = current_index + 1
        # 计算当天是星期几
        week_day  = last_day.weekday()
        # 不是休息日 追溯日期减一
        if(week_day < 6):
            interval = interval -1
        # 追溯日期小于1  结束
        if(interval < 0):
            break
    return last_day.strftime("%Y-%m-%d")

