from flask import Blueprint
from flask import request
from flask import Response
from apps.exts import mongo
from apps.models.model_form_sn import form_sn
import json
from datetime import datetime


blue_form_sn = Blueprint('blue_form_sn', __name__)

def init_blue_form_sn(app):
    app.register_blueprint(blueprint=blue_form_sn)


@blue_form_sn.route("/api/v0/db/form_sn/", methods=['post'])
def insert_form_sn():

    param = {
        "sn":  request.json.get('sn'),
        "inserted_at" : datetime.now() ,
        "updated_at" : datetime.now() ,
        "enable" : True 
        }
    form_sn_model = form_sn(mongo.db)
    result = form_sn_model.insert_form_sn(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_form_sn.route("/api/v0/db/form_sn/", methods=['get'])
def get_form_sn():

    #param = { "Index": request.json.get('Index'), "Status":  request.json.get('Status'),"insertAt" : datetime.now() ,"updateAt" : datetime.now() ,"Enable" : True }
    form_sn_model = form_sn(mongo.db)
    result = form_sn_model.get_form_sn()
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_form_sn.route("/api/v0/db/form_sn/", methods=['delete'])
def delete_form_sn():

    form_sn_model = form_sn(mongo.db)
    result = form_sn_model.delete_form_sn()
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200