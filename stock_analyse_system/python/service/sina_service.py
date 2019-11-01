import requests
from python.service import crawl_html_url
import datetime
from bs4 import BeautifulSoup
from python.mysql import mysql_pool
import re
import time
import traceback
import app
import platform
from python.domain import sina_comment_picture

"""爬取指定时间的大盘评论"""
def get_comment(begin_day ,end_day ):

    path = app.get_path()
    system_name = platform.system()
    if("Windows" ==  system_name):
        path.replace("\\\\","/")
    comment_txt_name = str(int(time.time()))+".txt"
    for num in range(1):
        """解析时间"""
        begin_time =  datetime.datetime.strptime(begin_day,"%Y-%m-%d %H:%M:%S")
        end_time =  datetime.datetime.strptime(end_day,"%Y-%m-%d %H:%M:%S")
        beginMonth = begin_time.month
        beginDay = begin_time.day
        endMonth = end_time.month
        endDay = end_time.day

        """爬取评论"""
        comment_brief = requests.get(crawl_html_url.sina_comment_url.format(str(num + 1)))
        comment_brief.encoding="utf-8"
        data = BeautifulSoup(comment_brief.text,"html.parser")
        comments = data.select(".list_009 li ")

        comment_times = data.select(".list_009 span ")
        """获取第一条数据时间 早于开始 时间 结束"""
        page_begin_time = re.findall("(\d+)月(\d+)日", comment_times[0].text)[0]
        page_begin_month = int(page_begin_time[0])
        page_begin_day = int(page_begin_time[1])
        """小于开始 月份 日期 结束页面爬取 页面是时间倒叙 爬到之间去了 可以直接结束"""
        if(page_begin_month < beginMonth):
            break

        if(page_begin_day < beginDay):
            break
        """获取最后一条数据时间 超过结束 时间 结束"""
        page_end_time = re.findall("(\d+)月(\d+)日", comment_times[len(comment_times) - 1].text)[0]
        page_end_month = int(page_end_time[0])
        page_end_day = int(page_end_time[1])
        """最后一条时间大于结束 月份 日期 结束页面爬取 页面是时间倒叙 跳过此次  没有有效的 直接开始下个页面爬取"""
        if(page_end_month > endMonth):
            continue

        if(page_end_day > endDay):
            continue


        """遍历每一条"""
        for comment in comments:
            try:
                href = comment.contents[0].attrs["href"]
                comment_time = comment.contents[1].text
                comment_lsit = re.findall("(\d+)月(\d+)日", comment_time)[0]

                """评论时间小于选择开始时间  结束 不需要之下的"""
                if(beginMonth > int(comment_lsit[0])):
                    break;
                if(beginDay > int(comment_lsit[1])):
                    break;
                """评论时间大于选择结束时间  跳过该条 找下一条"""
                if(endMonth < int(comment_lsit[0])):
                    continue;
                if(endDay < int(comment_lsit[1])):
                    continue;

                """去除参数 避免二次跳转"""
                if(href.find("?")>0):
                    href = href[:href.index("?")]

                """获取日期"""

                detail_comment = requests.get(href)
                detail_comment.encoding = "utd-8"
                """获取具体描述内容写入临时文件"""
                comment_content = BeautifulSoup(detail_comment.text,"html.parser");
                # shtml结尾链接特殊处理
                if(href.endswith("shtml")):
                    detail_comment_content = comment_content.select("meta")[6].attrs["content"]
                else:
                    detail_comment_content =  comment_content.select(".articalContent")[0].text
                out = open(path+"/static/comment_picture/"+comment_txt_name,"a+",encoding="utf-8")
                detail_comment_content = deal_invalid_word(detail_comment_content)
                out.write(detail_comment_content)
            except Exception as e:
                traceback.print_exc()
                print(href)
    return comment_txt_name

"""去除无效字符 避免影响正确市场判断"""
def deal_invalid_word(detail_comment_content):
    pool = mysql_pool.sql_pool()
    connection = pool.get_connection()
    sql = "select invalid_word from trade_invalid_word"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()
    for row in result:
        detail_comment_content = detail_comment_content.replace(row["invalid_word"],"")

    return detail_comment_content

    print(result)

"""保存生成词云图信息到数据库 便于 后面翻阅"""
def save_word_nephogram(begin_day,end_day,comment_txt_name):
    pool = mysql_pool.sql_pool()
    connection = pool.get_connection()
    sql = "insert into trade_word_nephogram(begin_time,end_time,picture_name) value (%s,%s,%s)"
    cursor = connection.cursor()
    comment_txt_name = comment_txt_name.replace("txt","jpg")
    cursor.execute(sql,(begin_day,end_day,comment_txt_name))
    cursor.connection.commit()
    result = cursor.fetchone()
    connection.close()
    print(result)

"""添加无效词汇"""
def add_field_word(field_word):
    """分隔字符 获取多个词汇"""
    field_words = field_word.split(",")
    words_list = []
    for word in field_words:
        words_list.append((word,))
    pool = mysql_pool.sql_pool()
    connection = pool.get_connection()
    sql = "insert into trade_invalid_word(invalid_word) values (%s)"
    cursor = connection.cursor()
    cursor.executemany(sql,tuple(words_list))
    cursor.connection.commit()
    result = cursor.fetchone()
    print(result)
    connection.close()

"""获取历史查询图片"""
def get_history_picture():
    pool = mysql_pool.sql_pool()
    connection = pool.get_connection()
    sql = "select begin_time,end_time,picture_name from trade_word_nephogram order by id desc limit 10"
    cursor = connection.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    res = []

    for row in result:
        picture = sina_comment_picture.picture(row["begin_time"],row["end_time"],row["picture_name"])
        res.append(picture.picture_to_string(picture))
    # print(result)
    return res


# picture = get_history_picture()
# print(picture)
# add_field_word("")
# save_word_nephogram("2017-01-01 08:45:45","2017-01-01 08:45:45","das,txt")

# print(platform.system())

# dat = requests.get("https://finance.sina.com.cn/stock/jsy/2019-09-09/doc-iicezzrq4598453.shtml")
# dat.encoding = "utf-8"
# format = BeautifulSoup(dat.text,"html.parser")
# find = format.find(name="description")
# print(find)

# pool = mysql_pool.sql_pool()
# connection = pool.get_connection()
# # sql = "insert into zjy_21_20190628153041_0 (离职时间) value (%s)"
# sql = "select code_short,code_full,stock_name,stock_letters,area_stock_code from trade_stock"
# sql = sql +" where area_stock_code like %s or stock_name like %s or stock_letters like %s"
# cursor = connection.cursor()
#
# cursor.execute(sql,("STXL","STXL","STXL"))
# print(cursor.fetchall())
# cursor.connection.commit()