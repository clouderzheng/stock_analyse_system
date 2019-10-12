from flask import Flask,request,redirect,session,render_template
from system import auth,home_index,snow_ball,sina_comment

from flask_script import Manager
from apscheduler.schedulers.background import BackgroundScheduler
import snow_ball_service
import date_time_util
import logger_util

app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.register_blueprint(home_index.blueprint)
app.register_blueprint(snow_ball.blueprint)
app.register_blueprint(sina_comment.blueprint)

app.jinja_env.auto_reload = True
app.run(debug=True)
app.secret_key = "123"
app.config['SESSION_TYPE'] = 'filesystem'
# app.config['SECRET_KEY'] = '123'

logger_util.logger_init()

scheduler = BackgroundScheduler()


scheduler.start()

manager = Manager(app)
if __name__ == '__main__':

    # 添加定时任务查询竞价信息 每天 9:25
    scheduler.add_job(snow_ball_service.get_biding_info(), 'cron', hour=9,minute=25)
    # 添加定时任务查询雪球仓位组合 23:40
    scheduler.add_job(snow_ball_service.get_stock_position_combination(date_time_util.get_date_time(-1),date_time_util.get_date_time(0)), 'cron', hour=23,minute=40)
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