from flask import Blueprint
from flask import request
from flask import Response
from apps.exts import mongo
from apps.models.model_member import Member
import uuid
import json
import datetime
import time



blue_member = Blueprint('blue_member', __name__)


def init_blue_member(app):
    app.register_blueprint(blueprint=blue_member)



# 建立一筆人員資料
@blue_member.route("/api/v0/init/member/", methods=['post'])
def insert_oen_member():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        member_uuid = str(uuid.uuid4())
    else:
        member_uuid = request.json.get('uuid')
    param = {
        "uuid"        : member_uuid,
        "account"     : request.json.get('account'),
        "password"    : request.json.get('password'),
        "pretor"      : request.json.get('pretor'),
        "relation"    : request.json.get('relation'),
        "role"        : request.json.get('role'),
        "position"    : request.json.get('position'),
        "organize"    : request.json.get('organize'),
        "org_no"      : request.json.get('org_no'),
        "department"  : request.json.get('department'),
        "dpt_no"      : request.json.get('dpt_no'),
        "group_name"  : request.json.get('group_name'),
        "group_no"    : request.json.get('group_no'),
        "region"      : request.json.get('region'),
        "cname"       : request.json.get('cname'),
        "ename"       : request.json.get('ename'),
        "full_name"   : request.json.get('full_name'),
        "staff_no"    : request.json.get('staff_no'),
        "ext"         : request.json.get('ext'),
        "sex"         : request.json.get('sex'),
        "avatar"      : request.json.get('avatar'),
        "enable"      : request.json.get('enable'),
        "memo"        : request.json.get('memo'),
        "inserted_at" : datetime.datetime.now()
    }
    member_model = Member(mongo.db)
    res, msg = member_model.create_member(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 查詢一筆人員資料
@blue_member.route("/api/v0/get/member/", methods=['get'])
def find_one_member():
    param = request.args.get('account')
    print(param)
    member_model = Member(mongo.db)
    res, data = member_model.read_member_by_account(param)
    print(data)
    strJson = ''
    if res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':'一筆人員資料查詢成功', 'data':data }
    elif res == 'fail':
        strJson = { 'result':'fail', 'code':'', 'msg':data, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 刪除一筆人員資料
@blue_member.route("/api/v0/delete/member/", methods=['delete'])
def delete_one_member():
    param = request.json.get('account')
    member_model = Member(mongo.db)
    res, msg = member_model.delete_member_by_account(param)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 修改一筆人員資料(group)
@blue_member.route("/api/v0/update/member/by/group/", methods=['post'])
def update_one_member():
    account    = request.json.get('account')
    group_name = request.json.get('group_name')
    group_no   = request.json.get('group_no')
    member_model = Member(mongo.db)
    res, msg = member_model.update_group_of_member(account, group_name, group_no)
    strJson = ''
    if  res == 'ok':
        strJson = { 'result':'ok', 'code':'', 'msg':msg, 'data':{}}
    else:
        strJson = { 'result':'fail', 'code':'', 'msg':msg, 'data':{}}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_member.route("/api/v0/db/data/get/member/", methods=['post'])
def select_oen_member():
    member_model = Member(mongo.db)
    result  = member_model.find_by_account(request.json.get('account'), request.json.get('password'))

    strJson = { 'result': 'ok', 'code':'01003', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_member.route("/api/v0/db/data/get/login_status/", methods=['post'])
def select_member_status():
    member_model = Member(mongo.db)
    result  = member_model.check_login_status(request.json.get('account'), request.json.get('password'))
    
    strJson = { 'result': 'ok', 'code':'01003', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_member.route("/api/v0/db/data/get/member/by_organize/", methods=['post'])
def select_member_by_organize():
    member_model = Member(mongo.db)
    result  = member_model.find_member_by_organize(request.json.get('organize'))
    strJson = { 'result': 'ok', 'code':'01003', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 取得組織名
def get_organize_by_cname(cname):

    member_model = Member(mongo.db)
    result  = member_model.find_organize_by_cname(cname)
    #print(result)
    return result



# 取得群組名
def get_group_no_by_cname(cname):

    member_model = Member(mongo.db)
    result  = member_model.find_group_no_by_cname(cname)
    #print(result)
    return result



#  取得中文名(依組織)
def get_cname_by_organize(organize):
    member_model = Member(mongo.db)
    result  = member_model.find_cname_by_organize(organize)
    for item in result:
        print(item)
    return result


@blue_member.route("/api/v0/db/data/get/cname/", methods=['GET'])
def select_cname_by_organize():
    member_model = Member(mongo.db)
    param = request.args.get('organize')
    result  = member_model.find_cname_by_organize(param)
    strJson = { 'result': 'ok', 'code':'', 'msg':'', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#透過中文名找直屬主管email
@blue_member.route("/api/v0/db/data/get/leader_email/by_name/", methods=['post'])
def select_leader_email_by_name():
    member_model = Member(mongo.db)
    result  = member_model.find_leader_email_by_name(request.json.get('member_cname'))
    strJson = { 'result': 'ok', 'code':'01003', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#透過中文名找email
@blue_member.route("/api/v0/db/data/get/email/by_name/", methods=['post'])
def select_email_by_name():
    member_model = Member(mongo.db)
    result  = member_model.find_email_by_name(request.json.get('member_cname'))
    strJson = { 'result': 'ok', 'code':'01003', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


