from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_all_kinds_reason import all_kinds_reason
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import json
import datetime
import uuid



blue_all_kinds_reason = Blueprint('blue_all_kinds_reason', __name__)


def init_blue_all_kinds_reason(app):
    app.register_blueprint(blueprint=blue_all_kinds_reason)



@blue_all_kinds_reason.route("/page/v0/all_kinds_reason/", methods=['GET'])
def all_kinds_reason_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "all_kinds_reason"

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
        #param = { "type": group_no }
        #task_milestone_model = task_milestone(mongo.db)
        #model = task_milestone_model.get_task_milestone(param)
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)

        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
        
        return render_template(
            'all_kinds_reason.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            IS_LEADER=isleader,
            GROUP_NO=group_no)



# 建立一筆原因
@blue_all_kinds_reason.route("/api/v0/db/data/all_kinds_reason/", methods=['post'])
def insert_one_kinds_reason():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        all_kinds_reason_uuid = str(uuid.uuid4())
    else:
        all_kinds_reason_uuid = request.json.get('uuid')

    param = { 
        "uuid"        : all_kinds_reason_uuid,
        "reason"      : request.json.get('reason'),
        "type"        : request.json.get('type'),      # new_technology / new_project
        "form_type"   : request.json.get('form_type'), # 評估單 /PM開案單 /RD開案單 / LAYOUT申請單 /PCB申請單 /試產單/ 技轉單
        "mode"        : request.json.get('mode'),      # 申請單退回原因 / 設計審查退回原因 / 暫停原因 / 指定結案原因
        "memo"        : request.json.get('memo'),
        "inserted_at" : datetime.datetime.now(),
        "updated_at"  : datetime.datetime.now(),
        "enable"      : request.json.get('enable')
        }
    print(param)
    all_kinds_reason_model = all_kinds_reason(mongo.db)
    res, msg = all_kinds_reason_model.create_one_reason(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200
    


# 查詢所有原因資料
@blue_all_kinds_reason.route("/api/v0/get/all_kinds_reason/all/", methods=['get'])
def find_all_kinds_reason():
   
    reason_model = all_kinds_reason(mongo.db)
    res, msg, data = reason_model.read_all_kinds_reason()
    #print('---------------------')
    #print(data)
    
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆原因資料
@blue_all_kinds_reason.route("/api/v0/delete/all_kinds_reason/", methods=['delete'])
def delete_one_all_kinds_reason():
    
    param = request.json.get('uuid')
    reason_model = all_kinds_reason(mongo.db)
    res, msg = reason_model.delete_reason_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除多筆原因資料
@blue_all_kinds_reason.route("/api/v0/delete/all_kinds_reason/multi/", methods=['delete'])
def delete_multi_all_kinds_reason():
    
    param_list = request.json.get('uuids')
    
    reason_model = all_kinds_reason(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = reason_model.delete_reason_by_uuid(param)

        strMsg = "多筆刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆原因資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 修改一筆原因資料
@blue_all_kinds_reason.route("/api/v0/update/all_kinds_reason/", methods=['post'])
def update_one_reason():

    param = {
        "uuid":      request.json.get('uuid'),
        "type":      request.json.get('type'),
        "form_type": request.json.get('form_type'),
        "mode":      request.json.get('mode'),
        "reason":    request.json.get('reason'),
        "enable":    request.json.get('enable'),
        "memo":      request.json.get('memo'),
    }
    print(param)
    reason_model = all_kinds_reason(mongo.db)
    res, msg = reason_model.update_one_reason(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200