from flask import render_template,Blueprint,request,session
from user_service import user_service
import uuid
blueprint = Blueprint('system', __name__, url_prefix='/auth')

@blueprint.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')


@blueprint.route('/home', methods=['POST',"GET"])
def home_page():
    return render_template('home.html')

@blueprint.route('/index_info', methods=['POST',"GET"])
def index_info():
    return render_template('index_info.html')


@blueprint.route('/verify', methods=['POST'])
def login_verify():
    account = request.form.get("account")
    password = request.form.get("password")

    user = user_service().get_user_info(account)
    result = {"code":"9999"}
    if(None == user):
        result['msg'] = "用户未注册"
        return result

    if(user["password"] != password):
        result['msg'] = "密码错误"
        return result

    token = str(uuid.uuid1())
    session[token] = str(user)
    print(session)
    result['code'] = "0000"
    result['token'] = token
    return result


# service = user_service()
# info = service.get_user_info("nigh1t")
# print(uuid.uuid4())
# result = {"code":"999"}
# result['code'] = "888"
# print(result)
