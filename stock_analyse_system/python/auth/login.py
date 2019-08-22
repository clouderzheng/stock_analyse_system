from flask import render_template,Blueprint
blueprint = Blueprint('auth', __name__, url_prefix='/auth')

@blueprint.route('/login/', methods=['GET', 'POST'])
def login():
    return render_template('login.html')
