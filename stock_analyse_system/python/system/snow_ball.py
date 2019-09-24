from flask import Blueprint,request
import snow_ball_service
import json
from snow_ball_bean import  snowball_stock_info
blueprint = Blueprint('snowball', __name__, url_prefix='/snowball')

"""获取仓位组合接口"""
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

"""获取早盘竞价情况"""
@blueprint.route('/get_bidding_info', methods=['POST'])
def get_bidding_info():
    count = int(request.form.get("count"))
    max_gain = float(request.form.get("max_gain"))
    min_gain = float(request.form.get("min_gain"))
    result = snow_ball_service.get_biding_info(count=count,max_gain=max_gain,min_gain=min_gain)
    res= {"code":"0000","result":result}
    return res

"""获取回调支撑位股票"""
@blueprint.route('/get_call_back_support_stock', methods=['POST'])
def get_call_back_support_stock():
    call_back_day = int(request.form.get("call_back_day"))
    exclude_day = int(request.form.get("exclude_day"))
    float_per = float(request.form.get("float_per"))
    result = snow_ball_service.get_call_back_support_stock(call_back_day = call_back_day,exclude_day=exclude_day,float_per=float_per)
    res = {"code":"0000","result":result}
    return res