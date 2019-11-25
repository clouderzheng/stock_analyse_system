import redis
from python.mysql import myql_config

"""redis 连接池"""
class RedisPool():

    """初始化redis连接"""
    def __init__(self):
        pool = redis.ConnectionPool(host=myql_config.REDIS_HOST,port= 6379,password = myql_config.REDIS_PASSWORD,db=myql_config.REDIS_DB,decode_responses=True)
        self.service = redis.Redis(connection_pool=pool)

    """保存字符串"""
    def setString(self,key,value):
        return self.service.set(key,value)
    """获取字符串"""
    def getString(self,key):
        return self.service.get(key)
    """删除字符串"""
    def delString(self,key):
        return self.service.delete(key)

    """map存储"""
    def hset(self,name,key,value):
        return self.service.hset(name,key,value);

    """map单个删除"""
    def hdel(selef,name,key):
        return selef.service.hdel(name,key)
    """map获取单个"""
    def hget(self,name,key):
        return self.service.hget(name,key)

# redis =  RedisPool()
# print(redis.hset("student","night","good"))
# print(redis.hset("student","tom","not bad"))
# print(redis.hset("student","jim"," bad"))
# print(redis.hdel("student","jim"))

# print(redis.getString("age"))
# print(redis.setString("address","四川"))
# print(redis.getString("address"))
# print(redis.delString("address"))
# print(redis.getString("address"))

