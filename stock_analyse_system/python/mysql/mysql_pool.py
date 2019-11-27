import pymysql
from DBUtils.PooledDB import PooledDB
from pymysql.cursors import DictCursor
from python.mysql import mysql_config
class sql_pool():


    def __init__(self):
      # self.pool = PooledDB(pymysql, 5, host='localhost', user='root', passwd='111', db='test', port=3306)  # 5为连接池里的最少连接数
      self.pool = PooledDB(pymysql, mincached = 1, maxcached = 20, \
                           host = mysql_config.DBHOST, port = mysql_config.DBPORT, user = mysql_config.DBUSER, passwd = mysql_config.DBPWD, \
                           db =mysql_config.DBNAME, use_unicode = True, charset = mysql_config.DBCHAR, cursorclass = DictCursor)

    def get_connection(self):
        return self.pool.connection()

    def close_connection(self,con):
        con.close()

    """插入信息"""
    def insert(self,sql,param):
        con = self.get_connection()
        cursor = con.cursor()
        cursor.execute(sql, tuple(param))
        cursor.connection.commit()
        result = cursor.fetchone()
        con.close()
        return result

    """单个查询"""
    def selectOne(self,sql,param = None):
        con = self.get_connection()
        cursor = con.cursor()
        if param == None:
          cursor.execute(sql)
        else:
          cursor.execute(sql, param)
        result = cursor.fetchone()
        con.close()
        return result

    """多个查询"""
    def selectMany(self,sql,param = None):
        con = self.get_connection()
        cursor = con.cursor()

        if param == None:
            cursor.execute(sql)
        else:
            cursor.execute(sql, param)
        result = cursor.fetchall()
        con.close()
        return result