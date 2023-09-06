from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_feedback_rule import feedback_rule
from apps.models.model_task import task
from apps.models.model_milestone import milestone
from apps.models.model_status import status
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_member      import Member
import json
import datetime
import uuid



blue_feedback_rule = Blueprint('blue_feedback_rule', __name__)


def init_blue_feedback_rule(app):
    app.register_blueprint(blueprint=blue_feedback_rule)



@blue_feedback_rule.route("/page/v0/feedback_rule/", methods=['GET'])
def feedback_rule_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "feedback_rule"

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
        task_model = task(mongo.db)
        res_task, msg_task, data_task = task_model.read_task_all()
        print(data_task)
        
        milestone_model = milestone(mongo.db)
        res_milestone, msg_milestone, data_milestone = milestone_model.read_milestone_all()
        print(data_milestone)
        
        status_model = status(mongo.db)
        res_status, msg_status, data_status = status_model.read_status_all()
        print(data_status)
        

        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        return render_template(
            'feedback_rule.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            TASK_MODEL=data_task,
            MILESTONE_MODEL=data_milestone,
            IS_LEADER=isleader,
            STATUS_MODEL=data_status)



# 新增單筆
@blue_feedback_rule.route("/api/v0/db/data/feedback_rule/one/", methods=['post'])
def insert_feedback_rule_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        feedback_rule_uuid = str(uuid.uuid4())
    else:
        feedback_rule_uuid = request.json.get('uuid')

    param = {
        "uuid":             feedback_rule_uuid,
        "rule_code":        request.json.get('rule_code'),
        "rule_cname":       request.json.get('rule_cname'),
        "rule_ename":       request.json.get('rule_ename'),
        "rule_description": request.json.get('rule_description'),
        "rule_type":        request.json.get('rule_type'),           # me #ee
        "rule_situation":   request.json.get('rule_situation'),      # 情境
        "form_type":        request.json.get('form_type'),           # 單據
        "task_uuid":        request.json.get('task_uuid'),
        "task_code":        request.json.get('task_code'),
        "task_cname":       request.json.get('task_cname'),
        "task_ename":       request.json.get('task_ename'),
        "task_index":       request.json.get('task_index'),
        "milestone_uuid":   request.json.get('milestone_uuid'),
        "milestone_code":   request.json.get('milestone_code'),
        "milestone_cname":  request.json.get('milestone_cname'),
        "milestone_ename":  request.json.get('milestone_ename'),
        "milestone_index":  request.json.get('milestone_index'),
        "status_uuid":      request.json.get('status_uuid'),
        "status_code":      request.json.get('status_code'),
        "status_cname":     request.json.get('status_cname'),
        "status_ename":     request.json.get('status_ename'),
        "status_index":     request.json.get('status_index'),
        "attach_list":      request.json.get('attach_list'),
        "event_node":       request.json.get('event_node'),
        "inserted_at":      datetime.datetime.now(),
        "updated_at":       datetime.datetime.now(),
        "enable":           True,
        "memo":             request.json.get('memo')
    }
    #print(param)
    rule_model = feedback_rule(mongo.db)
    result = rule_model.insert_feedback_rule(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有 feedback_rule 資料
@blue_feedback_rule.route("/api/v0/db/data/feedback_rule/all/", methods=['get'])
def get_feedback_rule_all():

    rule_model = feedback_rule(mongo.db)
    res, msg, data = rule_model.read_feedback_rule_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200

 #取得指定 feedback_rule 資料
@blue_feedback_rule.route("/api/v0/db/data/feedback_rule/by/param/", methods=['post'])
def read_feedback_rule_by_form_type():

    pam = {
        "form_type" :        request.json.get('form_type'),
        "rule_type" :        request.json.get('rule_type'),
    }
    rule_model = feedback_rule(mongo.db)
    res, msg, data = rule_model.read_feedback_rule_by_form_type(pam)
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆feedback_rule資料
@blue_feedback_rule.route("/api/v0/delete/feedback_rule/", methods=['delete'])
def delete_one_feedback_rule():
    
    param = request.json.get('uuid')
    rule_model = feedback_rule(mongo.db)
    res, msg = rule_model.delete_feedback_rule_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除多筆feedback_rule資料
@blue_feedback_rule.route("/api/v0/delete/feedback_rule/multi/", methods=['delete'])
def delete_multi_feedback_rule():
    
    param_list = request.json.get('uuids')
    rule_model = feedback_rule(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = rule_model.delete_feedback_rule_by_uuid(param)

        strMsg = "多筆feedback_rule刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆feedback_rule資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 修改一筆feedback_rule資料
@blue_feedback_rule.route("/api/v0/update/feedback_rule/", methods=['post'])
def update_one_feedback_rule():

    param = {
        "uuid":             request.json.get('uuid'),
        "rule_code":        request.json.get('rule_code'),
        "rule_cname":       request.json.get('rule_cname'),
        "rule_ename":       request.json.get('rule_ename'),
        "rule_type":        request.json.get('rule_type'),
        "form_type":        request.json.get('form_type'),
        "rule_situation":   request.json.get('rule_situation'),
        "rule_description": request.json.get('rule_description'),
        "task_uuid":        request.json.get('task_uuid'),
        "task_code":        request.json.get('task_code'),
        "task_cname":       request.json.get('task_cname'),
        "task_ename":       request.json.get('task_ename'),
        "task_index":       request.json.get('task_index'),
        "milestone_uuid":   request.json.get('milestone_uuid'),
        "milestone_code":   request.json.get('milestone_code'),
        "milestone_cname":  request.json.get('milestone_cname'),
        "milestone_ename":  request.json.get('milestone_ename'),
        "milestone_index":  request.json.get('milestone_index'),
        "status_uuid":      request.json.get('status_uuid'),
        "status_code":      request.json.get('status_code'),
        "status_cname":     request.json.get('status_cname'),
        "status_ename":     request.json.get('status_ename'),
        "status_index":     request.json.get('status_index'),
        "attach_list":      request.json.get('attach_list'),
        "event_node":       request.json.get('event_node'),
        "enable":           request.json.get('enable'),
        "memo":             request.json.get('memo'),
    }
    #print(param)
    rule_model = feedback_rule(mongo.db)
    res, msg = rule_model.update_one_feedback_rule(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200