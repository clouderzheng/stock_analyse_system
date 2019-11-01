from python.mysql.mysql_pool import  sql_pool
class user_service():

    def __init__(self):
        self.con = sql_pool().get_connection()

    """获取用户信息"""
    def get_user_info(self,account):
        cursor = self.con.cursor()
        sql = " select id,account,password from system_user where account = %s"
        cursor.execute(sql,account)
        return cursor.fetchone()

