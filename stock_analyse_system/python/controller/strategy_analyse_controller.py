from flask import Blueprint
import json
from flask import request
from python.service import strategy_analyse_service
from python.util import personal_encoder
blueprint = Blueprint('analyse', __name__, url_prefix='/analyse')

@blueprint.route('/query', methods=['get'])
def query_strategy_stock():
    page = int(request.args.get("page"))
    limit = int(request.args.get("limit"))
    strategy_ids = request.args.get("strategy_ids")
    analyse = strategy_analyse_service.strategy_analyse()
    data = analyse.get_strategy_stock(page,limit,strategy_ids)
    count = analyse.get_strategy_stock_count(strategy_ids)
    result = {}
    result["code"] = "0000"
    result["data"] = data
    result["count"] = count
    return result