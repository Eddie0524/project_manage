from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import FILE_PATH
from apps.settings import SMTP_INFO
from apps.settings import SERVER_IP
import json
import time
from apps.exts import mongo
from apps.models.model_new_technology_form import new_technology_form
from apps.models.model_new_technology_review import new_technology_review
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_new_technology_task import new_technology_task
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from datetime import datetime
from apps.settings import MAIL_RECEIVER


blue_new_technology_result = Blueprint('blue_new_technology_result', __name__)



def init_new_technology_result(app):
    app.register_blueprint(blueprint=blue_new_technology_result)



@blue_new_technology_result.route("/page/v0/new_technology_result/", methods=['GET'])
def new_technology_result_index():


    button_status   = request.args.get('status')
    project_no      = request.args.get('project_no'  )
    project_name    = request.args.get('project_name')
    form_no         = request.args.get('form_no')
    mode = 'new_technology_result'


    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
    #group_no = request.cookies.get('group_no')
    
    #print(group_no)
    new_technology_form_model = new_technology_form(mongo.db)
    new_technology_form_review_model = new_technology_review(mongo.db)
    param = { 'project_no' :   project_no }
    new_technology_model = new_technology_form_model.get_new_technology_form(param)
    new_technology_review_model = new_technology_form_review_model.get_new_technology_review(param)
    print(new_technology_review_model)
       
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

        return render_template('new_technology_result.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            FILE_PATH=FILE_PATH,
            USER=member,
            PHOTO=avatar,
            PROJECT_NO=project_no,
            RECEIVER=MAIL_RECEIVER,
            PROJECT_NAME=project_name ,
            USER_CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            BUTTON_STATUS=button_status,
            NEW_TECH_MODEL=new_technology_model,
            IS_LEADER=isleader,
            NEW_TECH_REVIEW_MODEL=new_technology_review_model)
    



# 新產品技術評估結果開案通知信
@blue_new_technology_result.route("/api/v0/send/new_technology_form_result/open/", methods=['post'])
def send_result_open_email():
    # 參數

    project_name                = request.json.get('project_name')
    project_no                  = request.json.get('project_no') 
    reason                      = request.json.get('reason')  
    memo                        = request.json.get('memo')  
    project_status              = request.json.get('project_status') 
    estimate_deadline           = request.json.get('estimate_deadline') 
    estimate_final_date         = datetime.now().strftime("%Y-%m-%d") 
    sender_mail   = request.json.get('sender')       # 寄件者
    receiver_list = request.json.get('receiver')     # 收件者 (陣列)
    cc_list       = request.json.get('cc')           # CC5者  (陣列)

    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')



    receiver_mail = receiver_list
    cc_mail = cc_list

    member_model = Member(mongo.db)
    #leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '評估案結果通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-{}</h1>'.format(project_name,project_status) + \
                '<ul>' + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>評估期限 : {}</li>'.format(estimate_deadline) + \
                '<li>完成評估日期 : {}</li>'.format(estimate_final_date) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_display/?project_no={}">新產品技術評估單</a>'.format(DOMAIN_PATH,project_no) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_form/?new_tech_project_no={}">新產品開發申請單</a>'.format(DOMAIN_PATH,project_no) + \
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

# 新產品技術評估結果待確認 通知信
@blue_new_technology_result.route("/api/v0/send/new_technology_form_result/pending/", methods=['post'])
def send_result_pending_email():
    # 參數
    project_name                = request.json.get('project_name')
    project_no                  = request.json.get('project_no') 
    reason                      = request.json.get('reason')  
    memo                        = request.json.get('memo')  
    project_status              = request.json.get('project_status') 
    estimate_deadline           = request.json.get('estimate_deadline') 
    estimate_final_date         = datetime.now().strftime("%Y-%m-%d")   
    sender_mail   = request.json.get('sender')       # 寄件者
    receiver_list = request.json.get('receiver')     # 收件者 (陣列)
    cc_list       = request.json.get('cc')           # CC5者  (陣列)

    print(project_no)

    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')



    receiver_mail = receiver_list
    cc_mail = cc_list

    member_model = Member(mongo.db)
    #leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '評估案結果通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-{}</h1>'.format(project_name,project_status) + \
                '<ul>' + \
                 '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>評估期限 : {}</li>'.format(estimate_deadline) + \
                '<li>完成評估日期 : {}</li>'.format(estimate_final_date) + \
                '<li>原因 : {}</li>'.format(reason) + \
                '<li>說明 : {}</li>'.format(memo) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_display/?project_no={}">新產品技術評估單</a>'.format(DOMAIN_PATH,project_no) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_result/?project_no={}&status=1">新產品技術評估結果單</a>'.format(DOMAIN_PATH,project_no) + \
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



# 新產品技術評估結果指定結案通知信
@blue_new_technology_result.route("/api/v0/send/new_technology_form_result/close/", methods=['post'])
def send_result_close_email():
    # 參數

    project_name                = request.json.get('project_name')
    project_no                  = request.json.get('project_no') 
    reason                      = request.json.get('reason')  
    memo                        = request.json.get('memo')  
    project_status              = request.json.get('project_status') 
    estimate_deadline           = request.json.get('estimate_deadline') 
    estimate_final_date         = datetime.now().strftime("%Y-%m-%d")     
    sender_mail   = request.json.get('sender')       # 寄件者
    receiver_list = request.json.get('receiver')     # 收件者 (陣列)
    cc_list       = request.json.get('cc')           # CC5者  (陣列)

    print(project_no)

    # SMTP服务器的配置
    smtp_server   = SMTP_INFO.get('SMTP_SERVER')
    smtp_port     = SMTP_INFO.get('SMTP_PORT')
    smtp_username = SMTP_INFO.get('SMTP_USERNAME')
    smtp_password = SMTP_INFO.get('SMTP_PASSWORD')



    receiver_mail = receiver_list
    cc_mail = cc_list

    member_model = Member(mongo.db)
    #leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '評估案結果通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-{}</h1>'.format(project_name,project_status) + \
                '<ul>' + \
                 '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>評估期限 : {}</li>'.format(estimate_deadline) + \
                '<li>完成評估日期 : {}</li>'.format(estimate_final_date) + \
                '<li>原因 : {}</li>'.format(reason) + \
                '<li>說明 : {}</li>'.format(memo) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_display/?project_no={}">新產品技術評估單</a>'.format(DOMAIN_PATH,project_no) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_result/?project_no={}&status=1">新產品技術評估結果單</a>'.format(DOMAIN_PATH,project_no) + \
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