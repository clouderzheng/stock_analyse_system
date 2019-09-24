from mysql_pool import sql_pool


"""获取数据库股票信息"""
def get_stock_info(key_word = None):
    sql = "select code_short,code_full,stock_name,stock_letters,area_stock_code from trade_stock"
    con = sql_pool().get_connection()
    cursor = con.cursor()
    """判断是否条件查询"""
    if(key_word != None):
        sql = sql + " where area_stock_code like %s or stock_name like %s or stock_letters like %s"
        cursor.execute(sql,(key_word,key_word,key_word))
    else:
        cursor.execute(sql)
    return cursor.fetchall()


# info = get_stock_info("STXL")
# for key in info:
#     print(key["stock_name"])
