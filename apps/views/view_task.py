from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_task import task
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import json
import datetime
import uuid



blue_task = Blueprint('blue_task', __name__)


def init_blue_task(app):
    app.register_blueprint(blueprint=blue_task)


@blue_task.route("/page/v0/task/", methods=['GET'])
def task_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "task"

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
            'task.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            IS_LEADER=isleader,
            GROUP_NO=group_no)
            #TASK_MILESTONE_MODEL=model)
            
            
# 新增單筆
@blue_task.route("/api/v0/db/data/task/one/", methods=['post'])
def insert_task_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        task_uuid = str(uuid.uuid4())
    else:
        task_uuid = request.json.get('uuid')

    param = {
        "uuid"        : task_uuid,
        "task_code"   : request.json.get('task_code'),
        "task_cname"  : request.json.get('task_cname'),
        "task_ename"  : request.json.get('task_ename'),
        "inserted_at" : datetime.datetime.now(),
        "updated_at"  : datetime.datetime.now(),
        "enable"      : True,
        "memo"        : request.json.get('memo')
    }
    #print(param)
    task_model = task(mongo.db)
    result = task_model.insert_task(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有Task資料
@blue_task.route("/api/v0/db/data/task/all/", methods=['get'])
def get_task_all():

    task_model = task(mongo.db)
    res, msg, data = task_model.read_task_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆Task資料
@blue_task.route("/api/v0/delete/task/", methods=['delete'])
def delete_one_task():
    
    param = request.json.get('uuid')
    task_model = task(mongo.db)
    res, msg = task_model.delete_task_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 刪除多筆Task資料
@blue_task.route("/api/v0/delete/task/multi/", methods=['delete'])
def delete_multi_task():
    
    param_list = request.json.get('uuids')
    task_model = task(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = task_model.delete_task_by_uuid(param)

        strMsg = "多筆Task刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆Task資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 修改一筆Task資料
@blue_task.route("/api/v0/update/task/", methods=['post'])
def update_one_task():

    param = {
        "uuid"       : request.json.get('uuid'),
        "task_code"  : request.json.get('task_code'),
        "task_cname" : request.json.get('task_cname'),
        "task_ename" : request.json.get('task_ename'),
        "enable"     : request.json.get('enable'),
        "memo"       : request.json.get('memo'),
    }
    #print(param)
    task_model = task(mongo.db)
    res, msg = task_model.update_one_task(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200