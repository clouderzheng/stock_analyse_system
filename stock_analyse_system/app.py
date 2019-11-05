from flask import Flask,request,redirect,session,render_template
from python.system import auth,home_index,snow_ball,sina_comment

from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
from python.service import snow_ball_service,query_all_stock_service
from python.util import logger_util


app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(home_index.blueprint)
app.register_blueprint(snow_ball.blueprint)
app.register_blueprint(sina_comment.blueprint)

app.jinja_env.auto_reload = True
app.secret_key = "123"
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SECRET_KEY'] = '123'

logger_util.logger_init()

scheduler = BackgroundScheduler()
# scheduler = APScheduler()
# scheduler.init_app(app)

# 添加定时任务查询竞价信息 每天 9:25
scheduler.add_job(snow_ball_service.get_biding_info, 'cron', hour=21,minute=11)
# scheduler.add_job(snow_ball_service.get_biding_info(), 'interval', seconds=5)
#
# 添加定时任务查询雪球仓位组合 23:40
scheduler.add_job(snow_ball_service.get_stock_position_combination, 'cron', hour=23,minute=40)
"""定时任务更新最新股票信息 每天下午4点"""
scheduler.add_job(snow_ball_service.get_stock_last_info, 'cron', hour=21,minute=9)
"""定时任务爬取所有股票信息"""
scheduler.add_job(query_all_stock_service.query_stock, 'cron', hour=23,minute=26)
manager = Manager(app)
scheduler.start()
if __name__ == '__main__':



    app.run(host = '0.0.0.0' ,port = 9112)
    manager.run()

@app.before_request
def filter_request():
    path = request.path

    if(path != "/auth/login" and not path.startswith("/static") and path != "/auth/verify" ):
        token = request.args.get("token")
        if (token == None):
            token = request.form.get("token")
        if((token == None)  | (len(token) == 0)):
            # return redirect("/auth/login")
            return render_template("login.html")
        else:
            cache_toekn = session.get(token)
            if (cache_toekn == None):
                return redirect("/auth/login")

"""获取项目路径"""
def get_path():
    return app.root_path