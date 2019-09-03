from flask import Blueprint,request
blueprint = Blueprint('snowball', __name__, url_prefix='/snowball')

@blueprint.route('/get_position_combination', methods=['POST'])
def get_position_combination():
    begin_time = request.form.get("begin_time")
    end_time = request.form.get("end_time")
    print(begin_time,end_time)
    return "0000"