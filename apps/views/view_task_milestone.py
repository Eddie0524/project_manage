from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_task_milestone import task_milestone
from apps.models.model_task_milestone import task_milestone_reason
from apps.models.model_member import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname
import json
import datetime
import uuid



blue_task_milestone = Blueprint('blue_task_milestone', __name__)


def init_blue_task_milestone(app):
    app.register_blueprint(blueprint=blue_task_milestone)



@blue_task_milestone.route("/page/v0/task_milestone/", methods=['GET'])
def task_milestone_index():
    
    #form_code = request.args.get('form_code')
    #project_no = request.args.get('project_no')
    
    mode = "task_milestone"

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

        param = { "type": group_no }
        
        task_milestone_model = task_milestone(mongo.db)
        model = task_milestone_model.get_task_milestone(param)
        
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
                
        return render_template(
            'task_milestone.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            TASK_MILESTONE_MODEL=model)


## 新增單筆
@blue_task_milestone.route("/api/v0/db/data/task_milestone/", methods=['post'])
def insertTaskAndMileStone():


    itemList = request.json.get('items')
   

    for item in itemList:
        print(item)
       
        task_milestone_uuid = str(uuid.uuid4())
        param = { 
            "uuid"              :task_milestone_uuid,
            "form_type"         :item['form_type'],
            "type"              :item['type'],
            "index"             :item['index'],
            "task"              :item['task'],
            "milestone"         :item['milestone'] ,
            "status"            :item['status'] ,
            "inserted_at"       :datetime.datetime.now() ,
            "updated_at"        :datetime.datetime.now() ,
            "enable"            :True 
        }
        task_milestone_model = task_milestone(mongo.db)
        result = task_milestone_model.insert_task_milestone(param)
        strJson = { 'result': 'ok', 'code':'01001',  'msg': '','data': result}


    # if request.json.get('uuid') == "" or request.json.get('uuid') is None:
    #     task_milestone_uuid = str(uuid.uuid4())
    # else:
    #     task_milestone_uuid = request.json.get('uuid')

    # param = { 
    #     "uuid"              :task_milestone_uuid,
    #     "form_type"         :request.json.get('form_type'),
    #     "type"              :request.json.get('type'),
    #     "index"             :request.json.get('index'),
    #     "task"              :request.json.get('task'),
    #     "milestone"         :request.json.get('milestone') ,
    #     "status"            :request.json.get('status') ,
    #     "inserted_at"       :datetime.datetime.now() ,
    #     "updated_at"        :datetime.datetime.now() ,
    #     "enable"            :True 
    # }
    # task_milestone_model = task_milestone(mongo.db)
    # result = task_milestone_model.insert_task_milestone(param)
    # strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 新增多筆
@blue_task_milestone.route("/api/v0/db/data/task_milestones/", methods=['post'])
def insert_multi_task_milestone():
    
    itemList = request.json.get('items')
    #print(itemList)
    
    group_no = request.cookies.get('group_no')
    task_milestone_model = task_milestone(mongo.db)
    task_milestone_model.delete_task_milestone_by_type(group_no)
    
    for item in itemList:
        print(item)
        
        if item['uuid'] == "" or item['uuid'] is None:
            task_milestone_uuid = str(uuid.uuid4())
        else:
            task_milestone_uuid = item['uuid']
            
        if item['inserted_at'] == "":
            task_milestone_inserted_at = datetime.datetime.now()
        else:
            task_milestone_inserted_at = item['inserted_at']

        param = {
            #"_id" :         item['_id'],
            "uuid":         task_milestone_uuid,
            "type":         item['type'],
            "index":        item['index'],
            "task":         item['task'],
            "milestone":    item['milestone'],
            "inserted_at" : task_milestone_inserted_at,
            "updated_at" :  datetime.datetime.now(),
            "enable" :      item['enable']
        }

        result = task_milestone_model.insert_task_milestone(param)

    strJson = { 'result': 'ok', 'code':'', 'msg': '多筆Taskt儲存成功', 'data': { }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 修改一筆Task資料
@blue_task_milestone.route("/api/v0/update/milestone/by/task/", methods=['post'])
def update_one_task():
    
    group_no = request.cookies.get('group_no')
    param_type = group_no
    param_task = request.json.get('task')
    param_milestone = request.json.get('milestone')
    
    task_milestone_model = task_milestone(mongo.db)
    res, msg = task_milestone_model.update_milestone_of_task(param_type, param_task, param_milestone)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_task_milestone.route("/api/v0/db/data/find/task_milestone/", methods=['post'])
def getTaskAndMileStone():

    group_no = request.json.get('type')
    form_type = request.json.get('form_type')
    param = { "type": group_no, "form_type" : str.lower(form_type) }
    print(param)
    task_milestone_model = task_milestone(mongo.db)
    result = task_milestone_model.get_task_milestone(param)
    
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_task_milestone.route("/api/v0/db/data/task_milestone/by/<type>/", methods=['get'])
def get_task_milestone_by_type(type):
    
    #group_no = request.cookies.get('group_no')
    param = { "type": type }
    task_milestone_model = task_milestone(mongo.db)
    result = task_milestone_model.get_task_milestone_by_type(param)

    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_task_milestone.route("/api/v0/db/data/task_milestone/", methods=['delete'])
def deleteTaskAndMileStone():   

    param = { "index":      request.json.get('index'),
              "task":       request.json.get('task'),
              "milestone":  request.json.get('milestone')
            }
    task_milestone_model = task_milestone(mongo.db)
    result = task_milestone_model.delete_task_milestone(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



## 新增單筆
@blue_task_milestone.route("/api/v0/db/data/task_milestone_reason/", methods=['post'])
def insert_task_milestone_reason():


    itemList = request.json.get('items')
   

    for item in itemList:
        print(item)
       
        task_milestone_uuid = str(uuid.uuid4())
        param = { 
            "uuid"                  :task_milestone_uuid,
            "form_type"             :item['form_type'],
            "type"                  :item['type'],
            "task"                  :item['task'],
            "milestone"             :item['milestone'] ,
            "apply_reject_reason"   :item['apply_reject_reason'] ,
            "design_reject_reason"  :item['design_reject_reason'] ,
            "pause_reason"          :item['pause_reason'] ,
            "end_reason"            :item['end_reason'] ,
            "inserted_at"           :datetime.datetime.now() ,
            "updated_at"            :datetime.datetime.now() ,
            "enable"                :True 
        }
        task_milestone_reason_model = task_milestone_reason(mongo.db)
        result = task_milestone_reason_model.insert_task_milestone_reason(param)
        strJson = { 'result': 'ok', 'code':'01001',  'msg': '','data': result}

 
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_task_milestone.route("/api/v0/db/data/find/task_milestone_reason/", methods=['post'])
def get_task_milestone_reason():

    group_no = request.json.get('type')
    form_type = request.json.get('form_type')
    param = { "type": group_no, "form_type" : str.lower(form_type) }
    print(param)
    task_milestone_reason_model = task_milestone_reason(mongo.db)
    result = task_milestone_reason_model.get_task_milestone_reason(param)
    
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200