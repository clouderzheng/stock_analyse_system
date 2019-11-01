from flask import Blueprint,request
blueprint = Blueprint('sina', __name__, url_prefix='/sina')
from python.service import sina_service
from python.util import word_nephogram

"""爬取新浪股票大盘评论 生成词云图"""
@blueprint.route('/get_word_nephogram', methods=['POST'])
def get_word_nephogram():
    begin_day = request.form.get("begin_time")
    end_day = request.form.get("end_time")
    """爬取评论"""
    comment_txt = sina_service.get_comment(begin_day, end_day)
    """生成词云图"""
    word_nephogram.generate_word_nephogram(comment_txt)
    """保存词云图信息"""
    sina_service.save_word_nephogram(begin_day,end_day,comment_txt)

    result = {"code" : "0000","picture_url" : comment_txt.split(".")[0]+".jpg"}
    return result


"""添加屏蔽词汇"""
@blueprint.route('/add_shield_word', methods=['POST'])
def add_shield_word():
    field_word = request.form.get("field_word")

    sina_service.add_field_word(field_word)
    result = {"code" : "0000"}
    return result


"""获取历史图片轮播"""
@blueprint.route('/get_history_picture', methods=['POST'])
def get_history_picture():
    pictures = sina_service.get_history_picture()
    result = {"code" : "0000","pictures":pictures}
    return result


