"""新浪大盘评论词云图实体"""
class picture():

    def __init__(self,begin_time,end_time,picture_name):
        self.begin_time = begin_time
        self.end_time = end_time
        self.picture_name = picture_name

    def picture_to_string(self,obj):
        return  {"begin_time" : obj.begin_time,"end_time" : obj.end_time,"picture_name" : obj.picture_name}