import re

"""针对没有地区名的code添加地区名"""
def complete_stock_code(stock_code):
    if re.match("^[6,9]\d+",stock_code):
        return "SH"+stock_code
    return "SZ" + stock_code