from python.jq import get_index_service
from flask import Blueprint
from python.system import system_code
from python.jq import jq_config
blueprint = Blueprint('home', __name__, url_prefix='/home')

@blueprint.route('/index', methods=['POST'])
def get_home_index():
    result = {"code":system_code.success_code}
    """获取纳斯达克指数信息"""
    get_index_service.get_international_index(result,jq_config.jq_stock_ixic_code,jq_config.jq_stock_ixic_code_name)
    """获取道琼斯指数信息"""
    get_index_service.get_international_index(result,jq_config.jq_stock_dji_code,jq_config.jq_stock_dji_code_name)
    """获取标普500指数信息"""
    get_index_service.get_international_index(result,jq_config.jq_stock_inx_code,jq_config.jq_stock_inx_code_name)
    """获取纳斯达克指数信息"""
    get_index_service.get_international_index(result,jq_config.jq_stock_ixic_code,jq_config.jq_stock_ixic_code_name)
    """获取上证指数"""
    get_index_service.get_internal_index_service(result,jq_config.jq_stock_sse_code,jq_config.jq_stock_sse_code_name)
    """获取深证成指"""
    get_index_service.get_internal_index_service(result,jq_config.jq_stock_szcz_code,jq_config.jq_stock_szcz_code_name)
    """获取创业板指"""
    get_index_service.get_internal_index_service(result,jq_config.jq_stock_cybz_code,jq_config.jq_stock_cybz_code_name)
    return result

