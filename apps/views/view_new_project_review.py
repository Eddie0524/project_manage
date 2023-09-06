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
from apps.models.model_new_project_review import new_project_review
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
from apps.views.view_member   import get_cname_by_organize
from apps.views.view_member   import get_organize_by_cname
from apps.models.model_new_project_form import new_project_form
from apps.models.model_layout_form import layout_form



blue_new_project_review = Blueprint('blue_new_project_review', __name__)



def init_new_project_review(app):
    app.register_blueprint(blueprint=blue_new_project_review)



@blue_new_project_review.route("/page/v0/new_project_review/", methods=['GET'])
def new_project_review_index():

    flow_name   = request.args.get('flow_name')
    form_type   = request.args.get('form_type')
    project_no  = request.args.get('project_no')
    form_no     = request.args.get('form_no')
    mode = "new_project_review"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

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



        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)

        lay_form_model = layout_form(mongo.db)
        param = {
            'project_no'    : project_no,
            'form_no'       : form_no
        }      
        layout_model = lay_form_model.get_layout_form(param)
       
        
        return render_template(
            'new_project_review.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER=MAIL_RECEIVER,
            FORM_TYPE=form_type,
            FLOW_NAME=flow_name,
            GROUP_NO=group_no,
            IS_LEADER=isleader,           
            NEW_PROJECT_MODEL=new_project_model,
            LAYOUT_MODEL = layout_model)

    

@blue_new_project_review.route("/api/v0/db/new_project_review/", methods=['post'])
def insert_new_project_review():
    

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
       "uuid"                       :form_uuid,       
        "project_no"                :request.json.get('project_no'),
        "type"                      :request.json.get('type'),
        "status"                    :request.json.get('status'),
        "back_reason"               :request.json.get('back_reason'),
        "back_memo"                 :request.json.get('back_memo'),
        "enable"                    :True ,
        "inserted_at"               :datetime.datetime.now() ,
        "updated_at"                :datetime.datetime.now() ,
    }
    
    new_project_review_model = new_project_review(mongo.db)
    result = new_project_review_model.insert_new_project_review(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



# 主管審查通過通知信
@blue_new_project_review.route("/api/v0/send/new_project_review/approve/", methods=['post'])
def send_project_review_approve_email():
    # 參數

    form_no       = request.json.get('form_no')
    version       = request.json.get('version')
    product_no    = request.json.get('product_no')   
    project_no    = request.json.get('project_no')   
    next_apply    = request.json.get('next_apply')   #下一階段的表單名稱
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

    url = ''
    url_name = ''
    if next_apply == 'layout':
        url = "http://{}/page/v0/layout_form/?project_no={}".format(DOMAIN_PATH,project_no) 
        url_name = 'Layout申請工程規格聯絡單連結'
    elif next_apply == 'pcb':
        url = "http://{}/page/v0/pcb_form/?project_no={}&form_no={}".format(DOMAIN_PATH,project_no,form_no) 
        url_name = 'PCB打樣申請工程規格聯絡單連結'

    print(url)
    print(url_name)
  

    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '設計審查結果通知-{}'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-設計審查「核准」</h1>'.format(product_no) + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>版本: {}</li>'.format(version) + \
                '</ul><br/>' + \
                '<a href="{}">{}</a>'.format(url,url_name) + \
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



# 主管審核退回通知信
@blue_new_project_review.route("/api/v0/send/new_project_review/reject/", methods=['post'])
def send_project_review_reject_email():
    # 參數

    version       = request.json.get('version')
    product_no    = request.json.get('product_no')   
    project_no      = request.json.get('project_no')   
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
    subject  =  '設計審查結果通知-{}'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-設計審查「退回」</h1>'.format(product_no) + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>版本: {}</li>'.format(version) + \
                '<li>退回原因: {}</li>'.format(back_reason) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/">新產品開案回報單清單</a>'.format(DOMAIN_PATH) + \
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



# 主管審核layout通過通知信
@blue_new_project_review.route("/api/v0/send/new_project_review/layout/approve/", methods=['post'])
def send_project_review_layout_approve_email():
    # 參數
    form_no       = request.json.get('form_no')   
    product_no    = request.json.get('product_no')   
    project_no    = request.json.get('project_no')   
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
    subject  =  '{}-新產品開案Layout審核通過通知'.format(project_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開案Layout審核通過通知</h1>' + \
                '<ul>' + \
                '<li>產品型號:{}</li>'.format(product_no) + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '</ul><br/>' + \
                '<h3>點擊下方連結查詢專案狀態</h3><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/">新產品開案回報清單</a>'.format(DOMAIN_PATH) + \
                '<br/>' + \
                '<h3>點擊下方連結進行pcb申請</h3><br/>' + \
                '<a href="http://{}/page/v0/pcb_form/?project_no={}&form_no={}">連結</a>'.format(DOMAIN_PATH,project_no,form_no) + \
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



    
# 主管審核layout退回通知信
@blue_new_project_review.route("/api/v0/send/new_project_review/layout/reject/", methods=['post'])
def send_project_review_layout_reject_email():
    # 參數
    project_no      = request.json.get('project_no')   
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
    subject  =  '{}-新產品開案Layout審核退回通知'.format(project_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開案Layout審核退回通知</h1>' + \
                '<ul>' + \
                '<li>申請案名:{}</li>'.format(project_no) + \
                '<li>退回原因:{}</li>'.format(back_reason) + \
                '<li>退回說明:{}</li>'.format(back_memo) + \
                '</ul><br/>' + \
                '<h3>點擊下方連結查詢專案狀態</h3><br/>' + \
                '<a href="http://{}/page/v0/new_project_feedback/">新產品開案回報清單</a>'.format(DOMAIN_PATH) + \
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







