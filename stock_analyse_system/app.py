from flask import Flask,request,redirect,session,render_template
from python.system import auth,home_index,snow_ball,sina_comment,spider_signal

from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from python.service import snow_ball_service,query_all_stock_service,strategy_service
from python.util import logger_util,personal_encoder
from python.controller import strategy_analyse_controller
import socket,traceback

app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(home_index.blueprint)
app.register_blueprint(snow_ball.blueprint)
app.register_blueprint(sina_comment.blueprint)
app.register_blueprint(spider_signal.blueprint)
app.register_blueprint(strategy_analyse_controller.blueprint)



app.jinja_env.auto_reload = True
app.secret_key = "123"
app.config['SESSION_TYPE'] = 'filesystem'
app.json_encoder = personal_encoder.personal_encoder
# app.config['SECRET_KEY'] = '123'

logger_util.logger_init()

scheduler = BackgroundScheduler()
# scheduler = APScheduler()
# scheduler.init_app(app)

lock = open("scheduler_lock","wb")

try:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 47200))
except Exception as e:
    traceback.print_exc()
else:
    # 添加定时任务查询竞价信息 每天
    scheduler.add_job(snow_ball_service.get_biding_info, 'cron', hour=9,minute=27)
    """定时任务更新最新股票信息 """
    scheduler.add_job(snow_ball_service.get_stock_last_info, 'cron', hour=15,minute=8)
    # 添加定时任务查询尾盘主力资金流入
    scheduler.add_job(strategy_service.afternoon_bidding_choose, 'cron', hour=15,minute=10)
    """定时任务爬取所有股票信息"""
    scheduler.add_job(query_all_stock_service.query_stock, 'cron', hour=15,minute=20)
    # 添加定时任务查询雪球仓位组合 23:40
    scheduler.add_job(snow_ball_service.get_stock_position_combination, 'cron', hour=23,minute=40)
    scheduler.start()
manager = Manager(app)
if __name__ == '__main__':

    app.run(host = '0.0.0.0' ,port = 9112)
    manager.run()

@app.before_request
def filter_request():
    path = request.path

    if(path != "/auth/login" and not path.startswith("/static") and path != "/auth/verify" and path != "/spider/get_every_signal" ):
        token = request.args.get("token")
        if (token == None):
            token = request.form.get("token")
        if(token == None):
            # return redirect("/auth/login")
            return render_template("login.html")
        else:
            cache_toekn = session.get(token)
            if (cache_toekn == None):
                return redirect("/auth/login")

"""获取项目路径"""
def get_path():
    return app.root_path