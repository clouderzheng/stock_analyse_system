class snowball_stock_info():

    def __init__(self,stock_name,stock_code,count):
        self.stock_name = stock_name
        self.stock_code = stock_code
        self.stock_count = count


    def snowball_stock_info_tostring(obj):
        return {"stock_name" : obj.stock_name,"stock_code" : obj.stock_code,"count" : obj.stock_count}