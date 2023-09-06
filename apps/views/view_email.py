from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_email import EMail
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_member      import Member
import json
import datetime
import uuid



blue_email = Blueprint('blue_email', __name__)



def init_blue_email(app):
    app.register_blueprint(blueprint=blue_email)



@blue_email.route("/page/v0/email/", methods=['GET'])
def email_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "email"

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
            'email.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            IS_LEADER=isleader,
            GROUP_NO=group_no)



# 新增單筆
@blue_email.route("/api/v0/db/data/email/one/", methods=['post'])
def insert_email_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        email_uuid = str(uuid.uuid4())
    else:
        email_uuid = request.json.get('uuid')

    param = {
        "uuid"        : email_uuid,
        "code"        : request.json.get('code'),
        "cname"       : request.json.get('cname'),
        "ename"       : request.json.get('ename'),
        "type"        : request.json.get('type'),       # 通知/提醒
        "main_title"  : request.json.get('main_title'), # 主標題
        "sub_title"   : request.json.get('sub_title'),  # 副標題
        "sender"      : request.json.get('sender'),     # 發信人
        "receiver"    : request.json.get('receiver'),   # 收件人(list)
        "cc"          : request.json.get('cc'),         # 副本收件人(list)
        "label"       : request.json.get('label'),      # 內文標題
        "content"     : request.json.get('content'),    # 內文內容 <html 格式>
        "param_list"  : request.json.get('param_list'), # 參數定義(json list)
        "page_link"   : request.json.get('page_link'),  # 頁面連結
        "file_link"   : request.json.get('file_link'),  # 檔案連結
        "inserted_at" : datetime.datetime.now(),
        "updated_at"  : datetime.datetime.now(),
        "enable"      : True,
        "memo"        : request.json.get('memo')
    }
    print(param)
    email_model = EMail(mongo.db)
    result = email_model.insert_email(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有 email 資料
@blue_email.route("/api/v0/db/data/email/all/", methods=['get'])
def get_email_all():

    rule_model = EMail(mongo.db)
    res, msg, data = rule_model.read_email_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆feedback_rule資料
@blue_email.route("/api/v0/delete/email/", methods=['delete'])
def delete_one_feedback_rule():
    
    param = request.json.get('uuid')
    rule_model = EMail(mongo.db)
    res, msg = rule_model.delete_email_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除多筆Milestone資料
@blue_email.route("/api/v0/delete/email/multi/", methods=['delete'])
def delete_multi_email():
    
    param_list = request.json.get('uuids')
    rule_model = EMail(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = rule_model.delete_email_by_uuid(param)

        strMsg = "多筆 email 刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆 email 資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 修改一筆 Email 資料
@blue_email.route("/api/v0/update/email/", methods=['post'])
def update_one_email():

    param = {
        "uuid"       : request.json.get('uuid'),
        "code"       : request.json.get('code'),
        "cname"      : request.json.get('cname'),
        "ename"      : request.json.get('ename'),
        "type"       : request.json.get('type'),
        "main_title" : request.json.get('main_title'),
        "sub_title"  : request.json.get('sub_title'),
        "sender"     : request.json.get('sender'),
        "receiver"   : request.json.get('receiver'),
        "cc"         : request.json.get('cc'),
        "label"      : request.json.get('label'),
        "content"    : request.json.get('content'),
        "param_list" : request.json.get('param_list'),
        "page_link"  : request.json.get('page_link'),
        "file_link"  : request.json.get('file_link'),
        "enable"     : request.json.get('enable'),
        "memo"       : request.json.get('memo'),
    }
    #print(param)
    email_model = EMail(mongo.db)
    res, msg = email_model.update_one_email(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200