from flask import Blueprint
from flask import request
from flask import Response
from apps.exts import mongo
from apps.models.model_end_project_reason import end_project_reason
import json
import uuid
from datetime import datetime


blue_end_project_reason = Blueprint('blue_end_project_reason', __name__)

def init_blue_end_project_reason(app):
    app.register_blueprint(blueprint=blue_end_project_reason)


@blue_end_project_reason.route("/api/v0/db/data/end_project_reason/", methods=['post'])
def insert_end_project_reason():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        end_project_reason_uuid = str(uuid.uuid4())
    else:
        end_project_reason_uuid = request.json.get('uuid')

    
    param = { 
        "uuid" :        end_project_reason_uuid,
        "index":        request.json.get('index'),
        "reason":       request.json.get('reason'),
        "inserted_at" : datetime.now() ,
        "updated_at" :  datetime.now() ,
        "enable" :      True 
        }
    EndProjectReason_model = end_project_reason(mongo.db)
    result = EndProjectReason_model.insert_end_project_reason(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_end_project_reason.route("/api/v0/db/data/end_project_reason/", methods=['get'])
def get_end_project_reason():
    
    #param = { "Index": request.json.get('Index'), "Reason":  request.json.get('Reason'),"insertAt" : datetime.now() ,"updateAt" : datetime.now() ,"Enable" : True }
    EndProjectReason_model = end_project_reason(mongo.db)
    result = EndProjectReason_model.get_end_project_reason()
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_end_project_reason.route("/api/v0/db/data/end_project_reason/", methods=['delete'])
def delete_end_project_reason():    
    param = {
        "index":    request.json.get('index'),
        "reason":   request.json.get('reason')
        }
    EndProjectReason_model = end_project_reason(mongo.db)
    result = EndProjectReason_model.delete_end_project_reason(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200