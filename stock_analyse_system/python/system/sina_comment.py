from flask import Blueprint,request
blueprint = Blueprint('sina', __name__, url_prefix='/sina')
import sina_service
import word_nephogram

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

