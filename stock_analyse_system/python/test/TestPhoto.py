
from python.mysql import mysql_pool
from python.util import scale_util
import matplotlib.pyplot as plt
import numpy as np

pool = mysql_pool.sql_pool()

# 统计 2板 开盘价格区间 买入盈利幅度
def get_diff_rate_photo():

    #按照开盘价分类  最高价卖出盈利分类
    sql = "SELECT ((two_open_price - one_close_price ) / one_close_price ) open_rate,((third_max_price - two_open_price) / two_open_price ) profit_rate  from stock_limit_up_statistics  WHERE two_open_price != two_limit_up_price HAVING open_rate >= -0.1 AND open_rate <= 0.1 ORDER BY open_rate; "
    datas = pool.selectMany(sql)

    open_rate_list = {}
    profit_rate_list = {}
    for data in datas:
        open_rate = scale_util.round_up(float(data["open_rate"]),2)
        profit_rate = scale_util.round_up(float(data["profit_rate"]),2)

        open_rate_count = open_rate_list.get(open_rate)
        profit_rate_sum = profit_rate_list.get(open_rate)
        if(open_rate_count == None):
            open_rate_list[open_rate] = 1
            profit_rate_list[open_rate] = profit_rate
        else:
            open_rate_list[open_rate] = open_rate_count+1
            profit_rate_list[open_rate] = profit_rate_sum + profit_rate

    positions = np.arange(len(open_rate_list.keys()))
    # 区间
    section = list(open_rate_list.keys())
    # 个数
    count = list(open_rate_list.values())
    # 幅度
    profit = list(profit_rate_list.values())

    # 平均涨幅
    average = []
    for i in range(len(count)):
        average.append(scale_util.round_up(profit[i] / count[i], 4) * 100)

    fig, ax1 = plt.subplots()

    # 成绩直方图
    ax1.bar(positions, count, width=0.5, align='center', color='r', label=u"count")
    ax1.set_xticks(positions)
    ax1.set_xticklabels(section, rotation=90)
    # ax1.set_xlim(-0.1,0.1)
    ax1.set_xlabel("section")
    ax1.set_ylabel("count")
    max_score = max(count)
    ax1.set_ylim(0, int(max_score * 1.2))
    # 成绩标签
    for x, y in zip(positions, count):
        ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

    # 变动折线图
    profit = average
    ax2 = ax1.twinx()
    ax2.plot(positions, profit, 'o-', label=u"profit")
    max_proges = max(profit)
    # 变化率标签
    for x, y in zip(positions, profit):
        ax2.text(x, y + max_proges * 0.02, ('%.1f%%' % y), ha='center', va='bottom', fontsize=13)
    # 设置纵轴格式
    ax2.set_ylim(0, int(max_proges * 1.2))
    ax2.set_ylabel(u"profit")


    # 图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

    plt.show()


# 统计 2板 价格区间 开盘价与最低价之间平均幅度
def get_diff_range_rate_photo():

    #按照开盘价分类  最高价卖出盈利分类
    sql = "SELECT ((two_open_price - one_close_price ) / one_close_price ) open_rate,((two_min_price - two_open_price) / two_open_price ) range_rate  from stock_limit_up_statistics  WHERE two_open_price != two_limit_up_price HAVING open_rate >= -0.1 AND open_rate <= 0.1 ORDER BY open_rate"
    datas = pool.selectMany(sql)

    open_rate_list = {}
    range_rate_list = {}
    for data in datas:
        open_rate = scale_util.round_up(float(data["open_rate"]),2)
        range_rate = scale_util.round_up(float(data["range_rate"]),2)

        open_rate_count = open_rate_list.get(open_rate)
        range_rate_sum = range_rate_list.get(open_rate)
        if(open_rate_count == None):
            open_rate_list[open_rate] = 1
            range_rate_list[open_rate] = range_rate
        else:
            open_rate_list[open_rate] = open_rate_count+1
            range_rate_list[open_rate] = range_rate_sum + range_rate

    positions = np.arange(len(open_rate_list.keys()))
    # 区间
    section = list(open_rate_list.keys())
    # 个数
    count = list(open_rate_list.values())
    # 幅度
    profit = list(range_rate_list.values())

    temp = []
    for i in range(len(profit)):
        temp.append(scale_util.round_up(profit[i]/count[i],4) * 100)

    profit = temp

    fig, ax1 = plt.subplots()

    # 成绩直方图
    ax1.bar(positions, count, width=0.5, align='center', color='r', label=u"count")
    ax1.set_xticks(positions)
    ax1.set_xticklabels(section, rotation=90)
    # ax1.set_xlim(-0.1,0.1)
    ax1.set_xlabel("section")
    ax1.set_ylabel("count")
    max_score = max(count)
    ax1.set_ylim(0, int(max_score * 1.2))
    # 成绩标签
    for x, y in zip(positions, count):
        ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

    # 变动折线图
    ax2 = ax1.twinx()
    ax2.plot(positions, profit, 'o-', label=u"profit")
    max_proges = max(profit)
    min_proges = min(profit)
    # 变化率标签
    for x, y in zip(positions, profit):
        ax2.text(x, y + max_proges * 0.02, ('%.1f%%' % y), ha='center', va='bottom', fontsize=13)
    # 设置纵轴格式
    ax2.set_ylim(int(min_proges * 1.2 ), int(max_proges * 1.2))
    ax2.set_ylabel(u"profit")


    # 图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

    plt.show()



# 统计 2板 最低价 价格区间买入  第三天最高价卖出盈利
def get_diff_min_rate_photo():

    #按照开盘价分类  最高价卖出盈利分类
    sql = "SELECT ((two_min_price - one_close_price ) / one_close_price ) min_rate,((third_max_price - two_min_price) / two_min_price ) profit_rate  from stock_limit_up_statistics  WHERE two_open_price != two_limit_up_price HAVING min_rate >= -0.1 AND min_rate <= 0.1 ORDER BY min_rate"
    datas = pool.selectMany(sql)

    open_rate_list = {}
    range_rate_list = {}
    for data in datas:
        open_rate = scale_util.round_up(float(data["min_rate"]),2)
        range_rate = scale_util.round_up(float(data["profit_rate"]),2)

        open_rate_count = open_rate_list.get(open_rate)
        range_rate_sum = range_rate_list.get(open_rate)
        if(open_rate_count == None):
            open_rate_list[open_rate] = 1
            range_rate_list[open_rate] = range_rate
        else:
            open_rate_list[open_rate] = open_rate_count+1
            range_rate_list[open_rate] = range_rate_sum + range_rate

    positions = np.arange(len(open_rate_list.keys()))
    # 区间
    section = list(open_rate_list.keys())
    # 个数
    count = list(open_rate_list.values())
    # 幅度
    profit = list(range_rate_list.values())

    temp = []
    for i in range(len(profit)):
        temp.append(scale_util.round_up(profit[i]/count[i],4) * 100)

    profit = temp

    fig, ax1 = plt.subplots()

    # 成绩直方图
    ax1.bar(positions, count, width=0.5, align='center', color='r', label=u"count")
    ax1.set_xticks(positions)
    ax1.set_xticklabels(section, rotation=90)
    # ax1.set_xlim(-0.1,0.1)
    ax1.set_xlabel("section")
    ax1.set_ylabel("count")
    max_score = max(count)
    ax1.set_ylim(0, int(max_score * 1.2))
    # 成绩标签
    for x, y in zip(positions, count):
        ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

    # 变动折线图
    ax2 = ax1.twinx()
    ax2.plot(positions, profit, 'o-', label=u"profit")
    max_proges = max(profit)
    min_proges = min(profit)
    # 变化率标签
    for x, y in zip(positions, profit):
        ax2.text(x, y + max_proges * 0.02, ('%.1f%%' % y), ha='center', va='bottom', fontsize=13)
    # 设置纵轴格式
    ax2.set_ylim(int(min_proges * 1.2 ), int(max_proges * 1.2))
    ax2.set_ylabel(u"profit")


    # 图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

    plt.show()



# 统计 2板 收盘价 价格区间买入  第三天最高价卖出盈利
def get_diff_close_rate_photo():

    #按照开盘价分类  最高价卖出盈利分类
    sql = "SELECT ((two_close_price - one_close_price ) / one_close_price ) min_rate,((third_max_price - two_close_price) / two_min_price ) profit_rate  from stock_limit_up_statistics  WHERE two_open_price != two_limit_up_price HAVING min_rate >= -0.1 AND min_rate <= 0.1 ORDER BY min_rate"
    datas = pool.selectMany(sql)

    open_rate_list = {}
    range_rate_list = {}
    for data in datas:
        open_rate = scale_util.round_up(float(data["min_rate"]),2)
        range_rate = scale_util.round_up(float(data["profit_rate"]),2)

        open_rate_count = open_rate_list.get(open_rate)
        range_rate_sum = range_rate_list.get(open_rate)
        if(open_rate_count == None):
            open_rate_list[open_rate] = 1
            range_rate_list[open_rate] = range_rate
        else:
            open_rate_list[open_rate] = open_rate_count+1
            range_rate_list[open_rate] = range_rate_sum + range_rate

    positions = np.arange(len(open_rate_list.keys()))
    # 区间
    section = list(open_rate_list.keys())
    # 个数
    count = list(open_rate_list.values())
    # 幅度
    profit = list(range_rate_list.values())

    temp = []
    for i in range(len(profit)):
        temp.append(scale_util.round_up(profit[i]/count[i],4) * 100)

    profit = temp

    fig, ax1 = plt.subplots()

    # 成绩直方图
    ax1.bar(positions, count, width=0.5, align='center', color='r', label=u"count")
    ax1.set_xticks(positions)
    ax1.set_xticklabels(section, rotation=90)
    # ax1.set_xlim(-0.1,0.1)
    ax1.set_xlabel("section")
    ax1.set_ylabel("count")
    max_score = max(count)
    ax1.set_ylim(0, int(max_score * 1.2))
    # 成绩标签
    for x, y in zip(positions, count):
        ax1.text(x, y + max_score * 0.02, y, ha='center', va='center', fontsize=13)

    # 变动折线图
    ax2 = ax1.twinx()
    ax2.plot(positions, profit, 'o-', label=u"profit")
    max_proges = max(profit)
    min_proges = min(profit)
    # 变化率标签
    for x, y in zip(positions, profit):
        ax2.text(x, y + max_proges * 0.02, ('%.1f%%' % y), ha='center', va='bottom', fontsize=13)
    # 设置纵轴格式
    ax2.set_ylim(int(min_proges * 1.2 ), int(max_proges * 1.2))
    ax2.set_ylabel(u"profit")


    # 图例
    handles1, labels1 = ax1.get_legend_handles_labels()
    handles2, labels2 = ax2.get_legend_handles_labels()
    plt.legend(handles1 + handles2, labels1 + labels2, loc='upper right')

    plt.show()




# get_diff_rate_photo()
#
# get_diff_range_rate_photo()

# get_diff_min_rate_photo()

get_diff_close_rate_photo()
