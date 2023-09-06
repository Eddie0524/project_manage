from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import MAIL_RECEIVER
import json
import time
import uuid
from apps.exts import mongo
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_new_technology_task import new_technology_task
from apps.models.model_member import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_new_technology_form import new_technology_form



blue_new_technology_task = Blueprint('blue_new_technology_task', __name__)


def init_new_technology_task(app):
    app.register_blueprint(blueprint=blue_new_technology_task)



@blue_new_technology_task.route("/page/v0/new_technology_task/", methods=['GET'])
def new_technology_task_index():

    #leader = request.args.get('leader')
    form_no = request.args.get('form_no')
    project_no = request.args.get('project_no')
    
    mode = 'new_technology_task'

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    # print(account)
    # print(cname)
    # print(avatar)

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no ))
    else:
        
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)
       
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
        
        new_technology_form_model = new_technology_form(mongo.db)
      
        param = {'project_no' :   project_no}
        new_technology_model = new_technology_form_model.get_new_technology_form(param)

        return render_template(
            'new_technology_task.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER=MAIL_RECEIVER,
            PROJECT_NO=project_no,
            IS_LEADER=isleader,
            NEW_TECH_MODEL=new_technology_model)


@blue_new_technology_task.route("/api/v0/db/new_technology_task/", methods=['post'])
def insert_new_technology_task():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),
        "project_name":             request.json.get('project_name'),       
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
        "enable" :                  True ,
        "inserted_at" :             datetime.datetime.now() ,
        "updated_at" :              datetime.datetime.now() ,
        }
    new_technology_task_model = new_technology_task(mongo.db)
    result = new_technology_task_model.insert_new_technology_task(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_new_technology_task.route("/api/v0/db/new_technology_task/by/project_no/lastest/", methods=['get'])
def get_new_technology_task_by_project_no_latest():
       
   
    param = {        
        "project_no":      request.args.get('project_no'),
    }
    new_technology_task_model = new_technology_task(mongo.db)
    result = new_technology_task_model.get_new_technology_task_by_project_no_latest(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_new_technology_task.route("/api/v0/db/new_technology_task/", methods=['delete'])
def delete_new_technology_form_task():

    param = { 
        "uuid":          request.json.get('uuid'),
        "project_no":       request.json.get('project_no'),
        }
    new_technology_task_model = new_technology_task(mongo.db)
    result = new_technology_task_model.delete_new_technology_task(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200




# 指派工作送出指派通知信
@blue_new_technology_task.route("/api/v0/send/new_technology_task/", methods=['post'])
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
                '<li>評估案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>預計開始日期:{}</li>'.format(project_start) + \
                '<li>預計結束日期:{}</li>'.format(project_end) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_display/?project_no={}">新產品技術評估申請單</a>'.format(DOMAIN_PATH,project_no)+ \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_feedback/?project_no={}">新產品技術評回報單</a>'.format(DOMAIN_PATH,project_no)+ \
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


# 退回指派通知信
@blue_new_technology_task.route("/api/v0/send/new_technology_task/back/", methods=['post'])
def send_back_email_by_project_no():
    # 參數
    product_memo    = request.json.get('product_memo')
    form_no         = request.json.get('form_no')
    product_no      = request.json.get('product_no')
    project_no      = request.json.get('project_no')
    project_name    = request.json.get('project_name')
    back_reason     = request.json.get('back_reason')
    back_memo       = request.json.get('back_memo')
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
    subject  =  '申請退回通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品技術評估退回通知</h1>' + \
                '<ul>' + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>產品型號:{}</li>'.format(product_memo) + \
                '<li>退回原因:{}</li>'.format(back_reason) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_edit/?project_no={}&form_no={}">新產品技術評估申請單</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
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
        print('郵件發送成功')
        strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': '郵件發送成功' }}
        smtp_obj.quit()
    except smtplib.SMTPException as e:
        strJson = { 'result': 'fail', 'code':'', 'data': { 'msg': '郵件發送失败' }}
        print('郵件發送失败:', str(e))
        
    return Response(json.dumps(strJson), mimetype='application/json'), 200

        




