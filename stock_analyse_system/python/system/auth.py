from flask import render_template,Blueprint
blueprint = Blueprint('system', __name__, url_prefix='/auth')

@blueprint.route('/login', methods=['GET'])
def login_page():
    print("login")
    return render_template('login.html')


@blueprint.route('/home', methods=['GET'])
def home_page():
    return render_template('home.html')

# @blueprint.route('/verify/', methods=['POST'])
# def home_page():
#     return render_template('home.html')

