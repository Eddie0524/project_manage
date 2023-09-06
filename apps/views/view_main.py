from flask import Blueprint
from flask import request
from flask import Response
from flask import render_template
from apps.exts import current_datetime
from apps.settings import DOMAIN_PATH
from apps.exts import mongo
from apps.models.model_member import Member
import json
from apps.exts import logger


blue_main = Blueprint('blue_main', __name__)


def init_blue_main(app):
    app.register_blueprint(blueprint=blue_main)


@blue_main.route("/", methods=['GET'])
def get_system_info():
    logger.info("{} - {} - {}".format(request.remote_addr, request.user_agent, '取得系統建立時間及版號'))
    str_json = {
        'result': 'ok', 
        'code': '00000', 
        'data':{ 
            'system': 'Sunix Work Assist Platform', 
            'created_at': current_datetime,
            'version': '1.0.0'
        }
    }
    return Response(json.dumps(str_json), mimetype='application/json')



# 登入頁面(未登入)(一般)
@blue_main.route("/page/", methods=['GET', 'POST'])
@blue_main.route("/page/v0/login/", methods=['GET', 'POST'])
def login_fun():

    if request.method == "GET":
        return render_template('login.html', DOMAIN_PATH=DOMAIN_PATH, MODE="home")

    elif request.method == "POST":

        account  = request.json.get('account',  None)
        password = request.json.get('password', None)
        print(account)
        print(password)
        # 查詢人員資料( 帳號, 密碼 )是否存在, 且是否啟用
        member_model = Member(mongo.db)
        #print( str(member_model.check_login_status(account, password)))
        
        if(member_model.check_login_status(account, password) == False):
            # 登入失敗
            logger.error("{} - {} - {}{}".format(request.remote_addr, request.user_agent, account,'(一般)登入失敗'))
            strJson = {'result':'fail', 'code':'', 'msg':'登入失敗', 'data': {}}
            resp = Response(json.dumps(strJson), mimetype="application/json")
            return resp, 200

        else:
            # 登入成功
            logger.info("{} - {} - {}{}".format(request.remote_addr, request.user_agent, account,'(一般)登入成功'))
            strJson = {'result':'ok', 'code':'', 'msg':'登入成功', 'data': {}}
            resp = Response(json.dumps(strJson), mimetype="application/json")
            result = member_model.find_by_account(account, password)

            resp.set_cookie('account',  account            )
            resp.set_cookie('password', password           )
            resp.set_cookie('avatar',   result['avatar']   )
            resp.set_cookie('cName',    result['cname']    )
            resp.set_cookie('eName',    result['ename']    )
            resp.set_cookie('sex',      result['sex']      )
            resp.set_cookie('group_no', result['group_no'] )
            resp.set_cookie('department', result['department'] )
            return resp, 200



# 登入頁面(未登入)(指定)
@blue_main.route("/page/v0/login/<MODE>/<PROJECT_NO>/", methods=['GET', 'POST'])
@blue_main.route("/page/v0/login/<MODE>/<PROJECT_NO>/<FORM_NO>/", methods=['GET', 'POST'])
def assign_login_fun(MODE, PROJECT_NO, FORM_NO=None):

    print(MODE)
    print(PROJECT_NO)

    if request.method == "GET":
        return render_template('login.html', DOMAIN_PATH=DOMAIN_PATH, MODE=MODE, PROJECT_NO=PROJECT_NO, FORM_NO=FORM_NO)

    elif request.method == "POST":

        account  = request.json.get('account',  None)
        password = request.json.get('password', None)
        print(account)
        print(password)
        # 查詢人員資料( 帳號, 密碼 )是否存在, 且是否啟用
        member_model = Member(mongo.db)

        if(member_model.check_login_status(account, password) == False):
            # 登入失敗
            logger.error("{} - {} - {}{}".format(request.remote_addr, request.user_agent, account,'(指定)登入失敗'))
            strJson = {'result':'fail', 'code':'', 'msg':'登入失敗', 'data':{} }
            resp = Response(json.dumps(strJson), mimetype="application/json")
            return resp, 200

        else:
            # 登入成功
            logger.info("{} - {} - {}{}".format(request.remote_addr, request.user_agent, account,'(指定)登入成功'))
            strJson = {'result':'ok', 'code':'', 'msg':'登入成功', 'data':{'mode':MODE, 'no':PROJECT_NO}}
            resp = Response(json.dumps(strJson), mimetype="application/json")
            result = member_model.find_by_account(account, password)
            resp.set_cookie('account',  account            )
            resp.set_cookie('password', password           )
            resp.set_cookie('avatar',   result['avatar']   )
            resp.set_cookie('cName',    result['cname']    )
            resp.set_cookie('eName',    result['ename']    )
            resp.set_cookie('sex',      result['sex']      )
            resp.set_cookie('group_no', result['group_no'] )
            return resp, 200





# 登出(導入登入)
@blue_main.route("/page/v0/logout/", methods=['POST'])
def logout_fun():
    logger.info("{} - {} - {}{}".format(request.remote_addr, request.user_agent, request.cookies.get('account'),'成功登出系統'))
    strJson = { 'result':'ok', 'code':'', 'msg':'成功登出系統', 'data':{}}
    resp = Response(json.dumps(strJson), mimetype='application/json')
    resp.delete_cookie('account' )
    resp.delete_cookie('password')
    resp.delete_cookie('avatar'  )
    resp.delete_cookie('cName'   )
    resp.delete_cookie('eName'   )
    resp.delete_cookie('sex'     )
    return resp, 200