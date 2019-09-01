import get_index_service
from flask import Blueprint
import system_code
blueprint = Blueprint('home', __name__, url_prefix='/home')

@blueprint.route('/index', methods=['POST'])
def get_home_index():
    result = {"code":system_code.success_code}
    """获取纳斯达克指数信息"""
    get_index_service.get_NASDAQ_index(result)
    get_index_service.get_SSE_50_index(result)
    return result

