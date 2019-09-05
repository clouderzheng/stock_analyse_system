import requests
import crawl_html_url
import datetime
from bs4 import BeautifulSoup
"""爬取指定时间的大盘评论"""
def get_comment(begin_time = datetime.date.today(),end_time = datetime.date.today()):
    for num in range(1):
        comment_brief = requests.get(crawl_html_url.sina_comment_url.format(str(num + 1)))
        comment_brief.encoding="utf-8"
        data = BeautifulSoup(comment_brief.text,"html.parser")
        comments = data.select(".list_009 a ")
        for comment in comments:
            href = comment.attrs["href"]
            """去除参数 避免二次跳转"""
            if(href.find("?")>0):
                href = href[:href.index("?")]
            detail_comment = requests.get(href)
            detail_comment.encoding = "utd-8"
            detail_comment_content = BeautifulSoup(detail_comment.text,"html.parser").select(".articalContent")[0].text
            out = open("comment.txt","a+",encoding="utf-8")
            detail_comment_content = deal_invalid_word(detail_comment_content)
            out.write(detail_comment_content)

"""去除无效字符 避免影响正确市场判断"""
def deal_invalid_word(detail_comment_content):
    detail_comment_content = detail_comment_content.replace("行情","")
    detail_comment_content = detail_comment_content.replace("指数","")
    detail_comment_content = detail_comment_content.replace("今天","")
    detail_comment_content = detail_comment_content.replace("市场","")
    return detail_comment_content
get_comment()
# data = requests.get("http://blog.sina.com.cn/s/blog_7fa236e50102z7q7.html")
# data.encoding = "utf-8"
# print(data.text)
# param = "http://blog.sina.com.cn/s/blog_7fa236e50102z7q7.html?tj=fina"
# print(param.index("r"))
# print(param[:param.index("r")])

