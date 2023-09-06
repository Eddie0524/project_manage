from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_attach import Attach
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import json
import datetime
import uuid



blue_attach = Blueprint('blue_attach', __name__)


def init_blue_attach(app):
    app.register_blueprint(blueprint=blue_attach)



@blue_attach.route("/page/v0/attach/", methods=['GET'])
def attach_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "attach"

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
        #task_milestone_model = task_milestone(mongo.db)
        #model = task_milestone_model.get_task_milestone(param)
        
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"


        return render_template(
            'attach.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            IS_LEADER=isleader,
            GROUP_NO=group_no)



# 新增單筆
@blue_attach.route("/api/v0/db/data/attach/one/", methods=['post'])
def insert_attach_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        attach_uuid = str(uuid.uuid4())
    else:
        attach_uuid = request.json.get('uuid')

    param = {
        "uuid":         attach_uuid,
        "attach_code":  request.json.get('attach_code'),
        "attach_cname": request.json.get('attach_cname'),
        "attach_ename": request.json.get('attach_ename'),
        "attach_link":  request.json.get('attach_link'),
        "attach_file":  request.json.get('attach_file'),
        "inserted_at":  datetime.datetime.now(),
        "updated_at":   datetime.datetime.now(),
        "enable":       True,
        "memo":         request.json.get('memo')
    }
    #print(param)
    attach_model = Attach(mongo.db)
    result = attach_model.insert_attach(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有Attach資料
@blue_attach.route("/api/v0/db/data/attach/all/", methods=['get'])
def get_attach_all():

    attach_model = Attach(mongo.db)
    res, msg, data = attach_model.read_attach_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆Attach資料
@blue_attach.route("/api/v0/delete/attach/", methods=['delete'])
def delete_one_attach():
    
    param = request.json.get('uuid')
    attach_model = Attach(mongo.db)
    res, msg = attach_model.delete_attach_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 刪除多筆Attach資料
@blue_attach.route("/api/v0/delete/attach/multi/", methods=['delete'])
def delete_multi_attach():
    
    param_list = request.json.get('uuids')
    attach_model = Attach(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = attach_model.delete_attach_by_uuid(param)

        strMsg = "多筆Attach刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆Attach資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 修改一筆Attach資料
@blue_attach.route("/api/v0/update/attach/", methods=['post'])
def update_one_attach():

    param = {
        "uuid":         request.json.get('uuid'),
        "attach_code":  request.json.get('attach_code'),
        "attach_cname": request.json.get('attach_cname'),
        "attach_ename": request.json.get('attach_ename'),
        "attach_link":  request.json.get('attach_link'),
        "attach_file":  request.json.get('attach_file'),
        "enable":       request.json.get('enable'),
        "memo":         request.json.get('memo'),
    }
    #print(param)
    attach_model = Attach(mongo.db)
    res, msg = attach_model.update_one_attach(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200