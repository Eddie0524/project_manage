from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
import json
import time
import uuid
from apps.exts import mongo
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random
from apps.models.model_member import Member
from apps.models.model_new_project_form import new_project_form
from apps.models.model_new_project_task import new_project_task





blue_internal_project_task = Blueprint('blue_internal_project_task', __name__)


def init_internal_project_task(app):
    app.register_blueprint(blueprint=blue_internal_project_task)



@blue_internal_project_task.route("/page/v0/internal_project_task/", methods=['GET'])
def internal_project_task_index():

    mode = 'internal_project_task'
    #leader = request.args.get('leader')
    form_no = request.args.get('form_no')
    project_no = request.args.get('project_no')
    

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    print(account)
    print(cname)
    print(avatar)
    #print(form_no)

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no ))
    else:
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)
        return render_template(
            'internal_project_task.html',
            DOMAIN_PATH=DOMAIN_PATH,
            MODE=mode,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            NEW_PROJECT_MODEL=new_project_model)
    


    
@blue_internal_project_task.route("/api/v0/db/new_project_task/", methods=['post'])
def insert_new_project_task():
    

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
       "uuid":                      form_uuid,
        "form_no":                  request.json.get('form_no'),
        "project_no":               request.json.get('project_no'),
        "product_name":             request.json.get('product_name'),
        "project_name":             request.json.get('project_name'),
        "product_no":               request.json.get('product_no'),
        "bu":                       request.json.get('bu'),
        "member_list":              request.json.get('member_list'),
        "expected_start_date":      request.json.get('expected_start_date'),
        "expected_finish_date":     request.json.get('expected_finish_date'),
        "status":                   request.json.get('status'),
        "task":                     request.json.get('task'),
        "mile_stone":               request.json.get('mile_stone'),
        "reason":                   request.json.get('reason'),
        "memo":                     request.json.get('memo'),
        "actual_date":              datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "back_reason":              request.json.get('back_reason'),
        "back_memo":                request.json.get('back_memo'),
        "enable" :                  True,
        "inserted_at" :             datetime.datetime.now() ,
        "updated_at" :              datetime.datetime.now() ,
    }
    
    new_technology_task_model = new_project_task(mongo.db)
    result = new_technology_task_model.insert_new_project_task(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_internal_project_task.route("/api/v0/db/internal_project_task/by/project_no/", methods=['post'])
def get_internal_project_task():
       
    form_uuid = request.json.get('uuid')
    param = { 
        "uuid":         form_uuid,
        "form_no":      request.json.get('form_no'),
    }
    new_technology_task_model = new_project_task(mongo.db)
    result = new_technology_task_model.get_new_project_task(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_internal_project_task.route("/api/v0/db/internal_project_task/by/project_no/lastest/", methods=['get'])
def get_new_project_task_by_project_no_latest():

    param = {
        "project_no":  request.args.get('project_no'),
    }
    new_technology_task_model = new_project_task(mongo.db)
    result = new_technology_task_model.get_new_project_task_by_project_no_latest(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#生成專案代號
@blue_internal_project_task.route("/api/v0/db/internal_project_no/", methods=['get'])
def generate_internal_project_no():

        SerialNum = "AAA-R-OA" + "{}{:02d}{:02d}{:03d}".format((int(datetime.datetime.now().year) - 1911), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,99))
        #result = get_form_sn(db)
        #print(result)
        return Response(json.dumps(SerialNum), mimetype='application/json'), 200


#生成表單編號
@blue_internal_project_task.route("/api/v0/db/internal_project_form_no/", methods=['get'])
def generate_internal_project_form_no():

        SerialNum = "D" + "{}{:02d}{:02d}{:04d}".format((int(datetime.datetime.now().year)), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,100))
        #result = get_form_sn(db)
        #print(result)
        return Response(json.dumps(SerialNum), mimetype='application/json'), 200


# 指派工作送出指派通知信
@blue_internal_project_task.route("/api/v0/send/internal_project_task/", methods=['post'])
def send_require_email_by_project_no():
    # 參數
    project_no    = request.json.get('project_no')
    project_name  = request.json.get('project_name')
    project_start = request.json.get('project_start')
    project_end   = request.json.get('project_end')
    sender_mail   = request.json.get('sender')       # 寄件者
    receiver_list = request.json.get('receiver')     # 收件者 (陣列)
    cc_list       = request.json.get('cc')           # CC5者  (陣列)
     
    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')

    #receiver_mail = ','.join(receiver_list)
    receiver_mail = receiver_list
    
    #print(receiver_mail)
    #print("\'{}\'".format(receiver_mail))

    #cc_mail = ','.join(cc_list)
    cc_mail = cc_list
    #print(cc_mail)
    #print("\'{}\'".format(cc_mail))

    member_model = Member(mongo.db)
    leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '任務指派通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>任務指派通知-{}</h1>'.format(project_name) + \
                '<ul>' + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>預計執行開始時間:{}</li>'.format(project_start) + \
                '<li>預計執行結束時間:{}</li>'.format(project_end) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/internal_project_display/?project_no={}">RD內部開案申請單</a>'.format(DOMAIN_PATH,project_no)+ \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/?project_no={}">新開案回報清單</a>'.format(DOMAIN_PATH,project_no)+ \
                '</body>' + \
                '</html>'
    print('---------------')
    print(sender)
    print(receiver)
    print(message)
    msg = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = receiver
    msg['Subject'] = subject
    msg["Cc"]      = cc_mail
    #msg.attach(MIMEText(message, 'plain', 'utf-8'))
    msg.attach(MIMEText(message, 'html', 'utf-8'))

    strJson = {}
    try:
        to_addr = receiver_list
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        #smtp_obj.starttls()  # 使用TLS加密
        smtp_obj.login(smtp_username, smtp_password)
        #smtp_obj.sendmail(sender, to_addr, msg.as_string())
        smtp_obj.send_message(msg)
        print('指派郵件發送成功')
        strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': '指派郵件發送成功' }}
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        strJson = { 'result': 'fail', 'code':'', 'data': { 'msg': '指派郵件發送失败' }}
        print('指派郵件發送失败:', str(e))
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 指派工作送出指派通知信(layout表單指派)
@blue_internal_project_task.route("/api/v0/send/new_project_task/layout/", methods=['post'])
def send_assign_email_by_layout():
    # 參數
    project_no      = request.json.get('project_no')
    product_no      = request.json.get('product_no')
    form_no         = request.json.get('form_no')
    project_start   = request.json.get('project_start')
    project_end     = request.json.get('project_end')
    sender_mail     = request.json.get('sender')       # 寄件者
    receiver_list   = request.json.get('receiver')     # 收件者 (陣列)
    cc_list         = request.json.get('cc')           # CC5者  (陣列)
     
    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')
    
   
    #receiver_mail = ','.join(receiver_list)
    receiver_mail = receiver_list
    
    #print(receiver_mail)
    #print("\'{}\'".format(receiver_mail))

    #cc_mail = ','.join(cc_list)
    cc_mail = cc_list
    #print(cc_mail)
    #print("\'{}\'".format(cc_mail))

    member_model = Member(mongo.db)
    leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '{}-新產品開案指派通知'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開案指派通知</h1>' + \
                '<ul>' + \
                '<li>申請案號:{}</li>'.format(project_no) + \
                '<li>產品型號:{}</li>'.format(product_no) + \
                '<li>預計執行開始時間:{}</li>'.format(project_start) + \
                '<li>預計執行結束時間:{}</li>'.format(project_end) + \
                '</ul><br/>' + \
                '<h3>請收到此通知點擊下方連結查看指派任務</h3><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/?project_no={}">查看</a><br/><br/>'.format(DOMAIN_PATH,project_no)+ \
                '<a href="http://{}/page/v0/layout_result/?project_no={}&form_no={}&status=1">Layout表單連結</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
                '</body>' + \
                '</html>'
    print('---------------')
    print(sender)
    print(receiver)
    print(message)
    msg = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = receiver
    msg['Subject'] = subject
    msg["Cc"]      = cc_mail
    #msg.attach(MIMEText(message, 'plain', 'utf-8'))
    msg.attach(MIMEText(message, 'html', 'utf-8'))

    strJson = {}
    try:
        to_addr = receiver_list
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        #smtp_obj.starttls()  # 使用TLS加密
        smtp_obj.login(smtp_username, smtp_password)
        #smtp_obj.sendmail(sender, to_addr, msg.as_string())
        smtp_obj.send_message(msg)
        print('指派郵件發送成功')
        strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': '指派郵件發送成功' }}
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        strJson = { 'result': 'fail', 'code':'', 'data': { 'msg': '指派郵件發送失败' }}
        print('指派郵件發送失败:', str(e))
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 指派工作送出指派通知信(pcb表單指派)
@blue_internal_project_task.route("/api/v0/send/new_project_task/pcb/", methods=['post'])
def send_assign_email_by_pcb():
    # 參數
    project_no      = request.json.get('project_no')
    product_no      = request.json.get('product_no')
    form_no         = request.json.get('form_no')
    project_start   = request.json.get('project_start')
    project_end     = request.json.get('project_end')
    sender_mail     = request.json.get('sender')       # 寄件者
    receiver_list   = request.json.get('receiver')     # 收件者 (陣列)
    cc_list         = request.json.get('cc')           # CC5者  (陣列)
     
    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')
    
   
    #receiver_mail = ','.join(receiver_list)
    receiver_mail = receiver_list
    
    #print(receiver_mail)
    #print("\'{}\'".format(receiver_mail))

    #cc_mail = ','.join(cc_list)
    cc_mail = cc_list
    #print(cc_mail)
    #print("\'{}\'".format(cc_mail))

    member_model = Member(mongo.db)
    leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '{}-新產品開案指派通知'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開案指派通知</h1>' + \
                '<ul>' + \
                '<li>申請案號:{}</li>'.format(project_no) + \
                '<li>產品型號:{}</li>'.format(product_no) + \
                '<li>預計執行開始時間:{}</li>'.format(project_start) + \
                '<li>預計執行結束時間:{}</li>'.format(project_end) + \
                '</ul><br/>' + \
                '<h3>請收到此通知點擊下方連結查看指派任務</h3><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/?project_no={}">查看</a><br/><br/>'.format(DOMAIN_PATH,project_no)+ \
                '<a href="http://{}/page/v0/pcb_result/?project_no={}&form_no={}&status=1">pcb表單連結</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
                '</body>' + \
                '</html>'
    print('---------------')
    print(sender)
    print(receiver)
    print(message)
    msg = MIMEMultipart()
    msg['From']    = sender
    msg['To']      = receiver
    msg['Subject'] = subject
    msg["Cc"]      = cc_mail
    #msg.attach(MIMEText(message, 'plain', 'utf-8'))
    msg.attach(MIMEText(message, 'html', 'utf-8'))

    strJson = {}
    try:
        to_addr = receiver_list
        smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
        #smtp_obj.starttls()  # 使用TLS加密
        smtp_obj.login(smtp_username, smtp_password)
        #smtp_obj.sendmail(sender, to_addr, msg.as_string())
        smtp_obj.send_message(msg)
        print('指派郵件發送成功')
        strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': '指派郵件發送成功' }}
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        strJson = { 'result': 'fail', 'code':'', 'data': { 'msg': '指派郵件發送失败' }}
        print('指派郵件發送失败:', str(e))
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#主管同意(電路設計、layout、pcb)審核 自動更新狀態(審核中->已完成)
@blue_internal_project_task.route("/api/v0/db/new_project_task/update_status/", methods=['get'])
def update_new_project_task_status():
       
    
    param = { 
        "project_no":  request.args.get('project_no'),
        
    }
    new_technology_task_model = new_project_task(mongo.db)
    result = new_technology_task_model.update_new_project_task_status(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#主管指派(layout、pcb)人員工作項目
@blue_internal_project_task.route("/api/v0/db/new_project_task/update_memberlist/", methods=['post'])
def update_new_project_task_memberlist():
       
    
    param = { 
        "project_no":   request.json.get('project_no'),
        "member_list":  request.json.get('member_list'),
        
    }
    
    new_technology_task_model = new_project_task(mongo.db)
    result = new_technology_task_model.update_new_project_task_memberlist(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200
