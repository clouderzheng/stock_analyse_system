from flask import Flask,request,redirect,session,render_template
from system import auth,home_index,snow_ball,sina_comment

from flask_script import Manager


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

manager = Manager(app)
if __name__ == '__main__':
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
                cache_toekn = session[token]
                if (cache_toekn == None):
                    return redirect("/auth/login")

"""获取项目路径"""
def get_path():
    return app.root_path