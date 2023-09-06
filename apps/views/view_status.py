from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_status import status
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import json
import datetime
import uuid



blue_status = Blueprint('blue_status', __name__)


def init_blue_status(app):
    app.register_blueprint(blueprint=blue_status)
    
    
    
@blue_status.route("/page/v0/status/", methods=['GET'])
def status_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "status"

    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
    #group_no = request.cookies.get('group_no')
    
    #print(group_no)

    if account is None:
        return redirect(url_for('blue_main.login_fun'))

    else:
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)

        #param = { "type": group_no }
        status_model = status(mongo.db)
        status_model = status_model.read_status_all()
        
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        return render_template(
            'status.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            STATUS_MODEL=status_model)



# 新增單筆
@blue_status.route("/api/v0/db/data/status/one/", methods=['post'])
def insert_status_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        status_uuid = str(uuid.uuid4())
    else:
        status_uuid = request.json.get('uuid')

    param = {
        "uuid"         : status_uuid,
        "status_code"  : request.json.get('status_code'),
        "status_cname" : request.json.get('status_cname'),
        "status_ename" : request.json.get('status_ename'),
        "inserted_at"  : datetime.datetime.now(),
        "updated_at"   : datetime.datetime.now(),
        "enable"       : True,
        "memo"         : request.json.get('memo')
    }
    print(param)
    status_model = status(mongo.db)
    result = status_model.insert_status(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有Status資料
@blue_status.route("/api/v0/db/data/status/all/", methods=['get'])
def get_status_all():

    status_model = status(mongo.db)
    res, msg, data = status_model.read_status_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆Status資料
@blue_status.route("/api/v0/delete/status/", methods=['delete'])
def delete_one_status():
    
    param = request.json.get('uuid')
    status_model = status(mongo.db)
    res, msg = status_model.delete_status_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 刪除多筆Status資料
@blue_status.route("/api/v0/delete/status/multi/", methods=['delete'])
def delete_multi_status():
    
    param_list = request.json.get('uuids')
    status_model = status(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = status_model.delete_status_by_uuid(param)

        strMsg = "多筆Status刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆Status資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 修改一筆Status資料
@blue_status.route("/api/v0/update/status/", methods=['post'])
def update_one_status():

    param = {
        "uuid"         : request.json.get('uuid'),
        "status_code"  : request.json.get('status_code'),
        "status_cname" : request.json.get('status_cname'),
        "status_ename" : request.json.get('status_ename'),
        "enable"       : request.json.get('enable'),
        "memo"         : request.json.get('memo'),
    }
    print(param)
    status_model = status(mongo.db)
    res, msg = status_model.update_one_status(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200