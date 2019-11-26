from flask import Blueprint
import json
from flask import request
from python.service import strategy_analyse_service,strategy_info_service
from python.util import personal_encoder
blueprint = Blueprint('analyse', __name__, url_prefix='/analyse')

"""分页查询策略选中股票"""
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

"""查询策略信息"""
@blueprint.route('/query_strategy_info', methods=['get'])
def query_strategy_info():
    strategy_id = request.args.get("strategy_ids")
    strategy_info = strategy_info_service.strategy_info()
    data = strategy_info.query_strategy_by_id(strategy_id)
    result = {}
    result["code"] = "0000"
    result["data"] = data
    return result