from flask import Blueprint,request
import snow_ball_service
blueprint = Blueprint('snowball', __name__, url_prefix='/snowball')

@blueprint.route('/get_position_combination', methods=['POST'])
def get_position_combination():
    begin_time = request.form.get("begin_time")
    end_time = request.form.get("end_time")
    count = request.form.get("count")
    result = snow_ball_service.get_stock_position_combination(begin_time, end_time, total=count)
    result["code"] = "0000"
    return result