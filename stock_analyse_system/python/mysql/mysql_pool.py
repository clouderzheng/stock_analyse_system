import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor
from  python.mysql import  myql_config
class sql_pool():


    def __init__(self):
      # self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='111', db='test', port=3306)  # 5为连接池里的最少连接数
      self.pool = PooledDB(pymysql, mincached = 1, maxcached = 20, \
               host = myql_config.DBHOST, port = myql_config.DBPORT, user = myql_config.DBUSER, passwd = myql_config.DBPWD, \
                      db =myql_config.DBNAME, use_unicode = True, charset = myql_config.DBCHAR, cursorclass = DictCursor)

    def get_connection(self):
        return self.pool.connection()

    def close_connection(self,con):
        con.close()
# pool = sql_pool()
# con = pool.get_connection()
# cursor = con.cursor()
# cursor.execute("insert into txt (date) values %")
# print(cursor.fetchone())