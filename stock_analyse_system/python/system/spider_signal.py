from flask import Blueprint
import subprocess

blueprint = Blueprint('spider', __name__, url_prefix='/spider')

"""获取仓位组合接口"""
@blueprint.route('/get_every_signal', methods=['get'])
def spider_signal():
    subprocess.check_output(['scrapy','crawl','hotel'])
    return "success"