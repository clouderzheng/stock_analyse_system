from flask import Blueprint,request
import snow_ball_service
import json
from snow_ball_bean import  snowball_stock_info
blueprint = Blueprint('snowball', __name__, url_prefix='/snowball')

@blueprint.route('/get_position_combination', methods=['POST'])
def get_position_combination():
    begin_time = request.form.get("begin_time")
    end_time = request.form.get("end_time")
    count = request.form.get("count")
    page = request.form.get("page")
    result = snow_ball_service.get_stock_position_combination(begin_time, end_time, page = page,total=count)
    stock_list = []
    for key in result:
        stock_list.append(snowball_stock_info.snowball_stock_info_tostring(result[key]))

    res= {"code":"0000","stock_list":stock_list}
    return res