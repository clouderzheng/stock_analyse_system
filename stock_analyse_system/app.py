from flask import Flask,request,redirect,session
from system import auth
from flask_script import Manager


app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.jinja_env.auto_reload = True
app.run(debug=True)
app.secret_key = "night"
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
            if(token == None):
                return redirect("/auth/login")
            else:
                cache_toekn = session[token]
                if (cache_toekn == None):
                    return redirect("/auth/login")