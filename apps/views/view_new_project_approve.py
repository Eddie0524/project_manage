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
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_new_project_form import new_project_form
from apps.exts import logger


blue_new_project_approve = Blueprint('blue_new_project_approve', __name__)



def init_new_project_approve(app):
    app.register_blueprint(blueprint=blue_new_project_approve)



@blue_new_project_approve.route("/page/v0/new_project_approve/", methods=['GET'])
def new_project_approve_index():

    form_no    = request.args.get('form_no')
    project_no = request.args.get('project_no')
    mode = "internal_project_approve"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    # print(account)
    # print(cname)
    # print(avatar)
    # print(form_no)

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO=form_no ))
    else:
        
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)
        
        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)
        print(new_project_model)
        print("\\\\\\\\\\\\\\\\\\\\\\\\")
        
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
                
        return render_template(
            'internal_project_approve.html',
            DOMAIN_PATH=DOMAIN_PATH,
            MODE=mode,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            FORM_NO=form_no,
            IS_LEADER=isleader,
            RECEIVER=MAIL_RECEIVER,
            NEW_PROJECT_MODEL=new_project_model)



# 新開案申請單退回送出PM通知信(PM主管發信給PM)
@blue_new_project_approve.route("/api/v0/send/new_project/reject/", methods=['post'])
def send_reject_email_to_pm():


    logger.info("{} - {} - {}".format(request.remote_addr, request.user_agent, '新開案申請單退回(PM主管發信給PM)'))
        # 參數
    project_no    = request.json.get('project_no')
    product_no  = request.json.get('product_no')
    reject_reason = request.json.get('reject_reason')
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
    print(cc_mail)
    #print("\'{}\'".format(cc_mail))

    member_model = Member(mongo.db)
    #leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '申請退回通知-{}'.format(product_no)
    
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-新產品開發申請單「退回」</h1>'.format(product_no) + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>申請退回原因: {}</li>'.format(reject_reason) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_edit/?project_no={}">新產品開發申請單</a>'.format(DOMAIN_PATH, project_no) + \
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
    



# 新開案申請單同意送出HW主管通知信(PM主管發信給HW主管)
@blue_new_project_approve.route("/api/v0/send/new_project/agree/", methods=['post'])
def send_agree_email_to_hw_leader():


    logger.info("{} - {} - {}".format(request.remote_addr, request.user_agent, '新開案申請單核准(PM主管發信給HW主管)'))
    # 參數
    project_no          = request.json.get('project_no')
    product_no          = request.json.get('product_no')
    first_product_date  = request.json.get('first_product_date')
    sender_mail   = request.json.get('sender')   # 寄件者
    receiver_list = request.json.get('receiver') # 收件者 (陣列)
    cc_list       = request.json.get('cc')       # CC5者  (陣列)
     
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
    print(cc_mail)
    #print("\'{}\'".format(cc_mail))

    member_model = Member(mongo.db)
    #leader_name  = member_model.find_leader_name_by_account(sender_mail)
    time.sleep(1)

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '{}-新產品開發申請表-請您簽核'.format(product_no)
    
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開發申請表-請您簽核</h1>' + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(product_no) + \
                '<li>產品型號: {}</li>'.format(project_no) + \
                '<li>產品預計上市日期: {}</li>'.format(first_product_date) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_task/?project_no={}">新產品開案申請表連結​</a>'.format(DOMAIN_PATH, project_no) + \
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