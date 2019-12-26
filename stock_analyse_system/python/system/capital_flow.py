from flask import Blueprint
from python.service import money_flow_service
blueprint = Blueprint('capital', __name__, url_prefix='/capital')

@blueprint.route('/sale_department_capital', methods=['POST'])
def get_sale_department_capital():
    capital_flow_service = money_flow_service.money_flow()
    data = capital_flow_service.query_sale_department_capital_flow()
    result = {"code" : "0000","data" : data}
    return result
