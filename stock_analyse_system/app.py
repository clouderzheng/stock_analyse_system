from flask import Flask
from auth import login
from flask_script import Manager
app = Flask(__name__)
app.register_blueprint(login.blueprint)
app.jinja_env.auto_reload = True
app.run(debug=True)
manager = Manager(app)

if __name__ == '__main__':
    manager.run()
