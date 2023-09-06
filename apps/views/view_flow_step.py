from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.exts import mongo
from apps.models.model_flow_step import Flow_Step
import json
import datetime
import uuid


blue_flow_step = Blueprint('blue_flow_step', __name__)


def init_blue_flow_step(app):
    app.register_blueprint(blueprint=blue_flow_step)



# 新增單筆
@blue_flow_step.route("/api/v0/db/data/flow_step/one/", methods=['post'])
def insert_flow_step_one():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        flow_step_uuid = str(uuid.uuid4())
    else:
        flow_step_uuid = request.json.get('uuid')

    param = {
        "uuid":           flow_step_uuid,
        "code":           request.json.get('code'),
        "cname":          request.json.get('cname'),
        "ename":          request.json.get('ename'),
        "index":          request.json.get('index'),
        "user":           request.json.get('user'),
        "action":         request.json.get('action'),
        "group":          request.json.get('group'),
        "classification": request.json.get('classification'),
        "inserted_at":    datetime.datetime.now(),
        "updated_at":     datetime.datetime.now(),
    }
    print(param)
    flow_step_model = Flow_Step(mongo.db)
    result = flow_step_model.create_flow_step(param)
    strJson = { 'result': 'ok', 'code':'', 'msg': result, 'data': {}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200




# 取得流程資料
@blue_flow_step.route("/api/v0/db/data/get/flow_step/", methods=['GET'])
def get_flow_step_by_classification():
    
    flow_step_model = Flow_Step(mongo.db)
    param = request.args.get('class')
    result  = flow_step_model.find_by_classification(param)

    strJson = { 'result': 'ok', 'code':'', 'msg':'', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

