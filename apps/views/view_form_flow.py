from flask import Blueprint
from flask import request
from flask import Response
from apps.exts import mongo
from apps.models.model_form_flow import form_flow
import uuid
import json
import datetime
import time



blue_form_flow = Blueprint('blue_form_flow', __name__)


def init_form_flow(app):
    app.register_blueprint(blueprint=blue_form_flow)




# 建立一筆表單簽核流程資料
@blue_form_flow.route("/api/v0/db/form_flow/", methods=['post'])
def insert_form_flow():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        member_uuid = str(uuid.uuid4())
    else:
        member_uuid = request.json.get('uuid')
    param = {
        "uuid"                  : member_uuid,
        "form_no"               : request.json.get('form_no'),
        "type"                  : request.json.get('type'),
        "fs_code"               : request.json.get('fs_code'),
        "project_no"            : request.json.get('project_no'),
        "action"                : request.json.get('action'),
        "status"                : request.json.get('status'),
        "memo"                  : request.json.get('memo'),
        "user"                  : request.json.get('user'),
        "inserted_at"           : datetime.datetime.now(),
        "updated_at"            : datetime.datetime.now(),
        "enable"                : True
    }
    form_flow_model = form_flow(mongo.db)
    res, msg = form_flow_model.insert_form_flow(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得一筆表單簽核流程資料
@blue_form_flow.route("/api/v0/db/form_flow/", methods=['get'])
def get_form_flow():

    param = {
        "form_no" : request.args.get('form_no'),
    }
    
    form_flow_model = form_flow(mongo.db)
    res, data  = form_flow_model.get_form_flow(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':'', 'data':data}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':data, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


