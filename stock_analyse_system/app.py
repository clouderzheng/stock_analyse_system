from flask import Flask,request,redirect,session
from system import auth
from flask_script import Manager
app = Flask(__name__)
app.register_blueprint(auth.blueprint)
app.jinja_env.auto_reload = True
app.run(debug=True)
manager = Manager(app)
if __name__ == '__main__':
    manager.run()

@app.before_request
def filter_request():
    path = request.path
    token = request.form.get("token")
    if(token == None and path != "/auth/login" and not path.startswith("/static")):
        return redirect("/login.html")