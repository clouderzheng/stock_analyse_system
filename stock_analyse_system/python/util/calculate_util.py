"""计算5日均线
5日均线为5日收盘价的平均值
"""
def calculate_average(items,days):
    five_days = items[-days:]
    count = 0
    for day in five_days:
        count += day[5]
    return round(count / days,2)

"""计算当前价格与参考价格的相差差 百分比 乘以100"""
def calculate_rate(currentPrice,referencePrice):
    return abs(round(((referencePrice - currentPrice  ) / currentPrice ) * 100 ,2))