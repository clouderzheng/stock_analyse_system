import snow_ball_service

"""
测试实现方法
"""




"""回调支撑方法
原理：股票到达高点之后开始回调 落到前一个高点会获得支撑
参数：回溯天数 需要查询时间

排除天数  ： 除去最近多少天  找出回溯剩余时间最高点
相差幅度  ： 上个高点 与当前 收盘价 相差幅度

"""
def call_back_support_stock(data):

    # 回溯时间
    call_back_day = 60
    # 排除时间周期
    exclude_day = 20
    # 相差幅度
    float_per = 2
    items = data["data"]["item"]

    # 截取回溯天数数据
    items = items[-call_back_day:]

    """查询结果小于回溯天数 可能是新股 跳过"""
    if (len(items) < call_back_day):
        return
    # 获取此时最低价
    current_low_price = items[call_back_day - 1][4]
    # 获取此时最新报价
    current_new_price = items[call_back_day - 1][5]
    # 获取此时最低价时间
    current_low_day = items[call_back_day - 1][0]
    # 获取此时波动幅度
    current_percent = items[call_back_day - 1][7]


    # 获取上个高点周期数据
    last_days = items[:(call_back_day - exclude_day)]
    # 获取上个周期 最高价排序
    sorts_list = sorted(last_days, key=lambda x: x[3], reverse=True)
    # 获取上个高点价格
    last_high_price = sorts_list[0][3]
    # 获取上个高点时间
    last_high_day = sorts_list[0][0]

    # 计算两个价格之间的相差波动率
    percent = (current_low_price - last_high_price) / last_high_day
    # 判断计算结果是否在指定区间内
    if (percent < float_per):
        # stock_info = {"current_new_price": current_new_price, "current_low_price": current_low_price,
        #               "current_low_day": current_low_day, "last_high_price": last_high_price,
        #               "last_high_day": last_high_day, \
        #               "stock_name": stock["stock_name"], "area_stock_code": stock["area_stock_code"],
        #               "percent": round(percent * 100, 2)}
        stock_info = ('',data['data']['symbol'],current_new_price,current_percent,3)
        snow_ball_service.save_strategy_stock_info(stock_info)


"""获取主升浪形态股票 
原理： 主升浪基本沿5日线上方盘旋即大于5日线 
参数 ：回溯值  从今天开始 往前查询天数   容错天数： 允许几天落下5日线下 
"""
def get_up_wave(data):

    """回溯天数"""
    call_back_day = 10
    """容错天数"""
    fault_day = 2

    """计算5日线回溯天数"""
    five_average_day = call_back_day + 5

    """获取最近5日数据"""
    items = data["data"]["item"][-five_average_day:]


    for index in range(call_back_day):
        """获取当天收盘价 多了5天计算平均值 所有位移5位 """
        current_day_close_price = items[index + 5][5]
        """获取计算5日价的 天数"""
        calculate_five_day = items[index:5]
        count = 0
        for every_day in calculate_five_day:
            count += every_day[5]

        five_average_value = round(count / 5,2)
        """判断收盘价是否低于5日线  低于5日线 容错日减一"""
        if( current_day_close_price < five_average_value):
            fault_day -= 1
    """最终容错日大于-1  证明该股票符合策略"""
    if( fault_day > -1):
        current_day_data = items[-1]
        stock_info = ('', data['data']['symbol'], current_day_data[5], current_day_data[7], 4)
        snow_ball_service.save_strategy_stock_info(stock_info)


# array = [1,2,3,4,5,6]
# print(array[-1])
# for i in range(10,15):
#     print(i)