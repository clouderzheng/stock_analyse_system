import snow_ball_service
def call_back_support_stock(data):

    print("开始解析:",data)
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


def get_up_wave(data):

    """获取最近5日数据"""
    items = data["data"]["item"]
    last_five_data = items[-5:]
    five_count = 0
    for every_day in last_five_data:
        five_count += every_day[5]

    last_five_close_average_price = five_count
    return

# array = [1,2,3,4,5,6]
# print(array[:3])