from flask import Blueprint
from flask import request
from python.service import strategy_analyse_service
blueprint = Blueprint('analyse', __name__, url_prefix='/analyse')

@blueprint.route('/query', methods=['get'])
def query_strategy_stock():
    page = request.args.get("page")
    limit = request.args.get("limit")
    strategy_ids = request.args.get("strategy_ids")
    data = strategy_analyse_service.strategy_analyse().get_strategy_stock(page,limit,strategy_ids)
    result = []
    result["code"] = "0000"
    result["data"] = data
    return result