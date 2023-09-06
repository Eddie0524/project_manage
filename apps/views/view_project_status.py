from flask import Blueprint
from flask import request
from flask import Response
from apps.exts import mongo
from apps.models.model_project_status import ProjectStatus
import json
import datetime
import uuid


blue_project_status = Blueprint('blue_project_status', __name__)

def init_blue_project_status(app):
    app.register_blueprint(blueprint=blue_project_status)


@blue_project_status.route("/api/v0/db/data/project_status/", methods=['post'])
def insert_project_status():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        project_status_uuid = str(uuid.uuid4())
    else:
        project_status_uuid = request.json.get('uuid')

    param = {
        "uuid":         project_status_uuid,    
        "index":        request.json.get('index'),
        "status":       request.json.get('status'),
        "inserted_at" : datetime.datetime.now() ,
        "updated_at" :  datetime.datetime.now() ,
        "enable" :      True 
        }
    ProjectStatus_model = ProjectStatus(mongo.db)
    result = ProjectStatus_model.insert_project_status(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_project_status.route("/api/v0/db/data/project_status/", methods=['get'])
def get_project_status():
    
    #param = { "Index": request.json.get('Index'), "Status":  request.json.get('Status'),"insertAt" : datetime.now() ,"updateAt" : datetime.now() ,"Enable" : True }
    ProjectStatus_model = ProjectStatus(mongo.db)
    result = ProjectStatus_model.get_project_status()
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_project_status.route("/api/v0/db/data/project_status/", methods=['delete'])
def delete_project_status():
    param = {
        "index":    request.json.get('index'),
        "status":   request.json.get('status')
        }
    ProjectStatus_model = ProjectStatus(mongo.db)
    result = ProjectStatus_model.delete_project_status(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200