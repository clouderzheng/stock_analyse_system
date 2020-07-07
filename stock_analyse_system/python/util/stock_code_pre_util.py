
"""根据股票code判断市场 添加后缀"""
def get_stock_code_suff(stock_code):

    stock_code = str(stock_code)
    market = None

    if stock_code.startswith("6"):
        stock_code = stock_code+"1"
        market = "1"
    else:
        stock_code = stock_code +"0"
        market = "0"

    return stock_code,market


# data = get_stock_code_suff("000222")
# print(data[0])