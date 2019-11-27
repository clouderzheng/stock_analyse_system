from python.mysql import mysql_pool
import logging
"""日志记录类"""
class log_record():

    def __init__(self):
        self.mysqlService = mysql_pool.sql_pool()

    """添加日志"""
    def add_log(self,param):
        sql = " insert into trade_log (log_type,error_data,remark) values(%s,%s,%s)"
        logging.error(param[2])
        self.mysqlService.insert(sql,tuple(param))