from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_milestone import milestone
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import json
import datetime
import uuid


blue_milestone = Blueprint('blue_milestone', __name__)


def init_blue_milestone(app):
    app.register_blueprint(blueprint=blue_milestone)
    
    
    
@blue_milestone.route("/page/v0/milestone/", methods=['GET'])
def milestone_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "milestone"

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
            'milestone.html',
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
@blue_milestone.route("/api/v0/db/data/milestone/one/", methods=['post'])
def insert_milestone_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        milestone_uuid = str(uuid.uuid4())
    else:
        milestone_uuid = request.json.get('uuid')

    param = {
        "uuid"            : milestone_uuid,
        "milestone_code"  : request.json.get('milestone_code'),
        "milestone_cname" : request.json.get('milestone_cname'),
        "milestone_ename" : request.json.get('milestone_ename'),
        "inserted_at"     : datetime.datetime.now(),
        "updated_at"      : datetime.datetime.now(),
        "enable"          : True,
        "memo"            : request.json.get('memo')
    }
    print(param)
    milestone_model = milestone(mongo.db)
    result = milestone_model.insert_milestone(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得所有Milestone資料
@blue_milestone.route("/api/v0/db/data/milestone/all/", methods=['get'])
def get_milestone_all():

    milestone_model = milestone(mongo.db)
    res, msg, data = milestone_model.read_milestone_all()
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':data}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆Milestone資料
@blue_milestone.route("/api/v0/delete/milestone/", methods=['delete'])
def delete_one_milestone():
    
    param = request.json.get('uuid')
    milestone_model = milestone(mongo.db)
    res, msg = milestone_model.delete_milestone_by_uuid(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 刪除多筆Milestone資料
@blue_milestone.route("/api/v0/delete/milestone/multi/", methods=['delete'])
def delete_multi_milestone():
    
    param_list = request.json.get('uuids')
    milestone_model = milestone(mongo.db)
    strJson = ''

    try:
        for param in param_list:
            _, _ = milestone_model.delete_milestone_by_uuid(param)

        strMsg = "多筆Milestone刪除成功"
        strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{}}
    except Exception as e:
        strMsg = '多筆Milestone資料刪除失敗,錯誤訊息:{}'.format(str(e))
        strJson = { 'result':'fail', 'code':'', 'msg':strMsg, 'data':{}}
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 修改一筆Milestone資料
@blue_milestone.route("/api/v0/update/milestone/", methods=['post'])
def update_one_milestone():

    param = {
        "uuid"            : request.json.get('uuid'),
        "milestone_code"  : request.json.get('milestone_code'),
        "milestone_cname" : request.json.get('milestone_cname'),
        "milestone_ename" : request.json.get('milestone_ename'),
        "enable"          : request.json.get('enable'),
        "memo"            : request.json.get('memo'),
    }
    #print(param)
    milestone_model = milestone(mongo.db)
    res, msg = milestone_model.update_one_milestone(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200