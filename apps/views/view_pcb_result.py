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
from apps.models.model_member import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname
from apps.models.model_pcb_result import pcb_result
from apps.models.model_pcb_form import pcb_form



blue_pcb_result = Blueprint('blue_pcb_result', __name__)



def init_pcb_result(app):
    app.register_blueprint(blueprint=blue_pcb_result)



@blue_pcb_result.route("/page/v0/pcb_result/", methods=['GET'])
def pcb_result_index():

    form_no = request.args.get('form_no')
    button_status = request.args.get('status')
    project_no = request.args.get('project_no')
    mode = "pcb_result"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(cname)
    #print(avatar)
    #print(form_code)
    

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no))
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

        pcb_form_model = pcb_form(mongo.db)
        param = {
            'project_no' : project_no,
            'form_no'    : form_no
        }
       
        pcb_form_model = pcb_form_model.get_pcb_form(param)
        print(pcb_form_model)
            
        return render_template(
            'pcb_result.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER=MAIL_RECEIVER,
            GROUP_NO=group_no,
            BUTTON_STATUS=button_status,
            IS_LEADER=isleader,
            PCB_FORM_MODEL=pcb_form_model)
    

@blue_pcb_result.route("/api/v0/db/pcb_result/", methods=['post'])
def insert_pcb_result():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = {
        "uuid"                  : form_uuid,                                  #識別編碼
        "project_no"            : request.json.get('project_no'),             #專案代號       
        "form_no"               : request.json.get('form_no'),              #表單編號
        "product_no"            : request.json.get('product_no'),             #產品型號
        "pcb_name"              : request.json.get('pcb_name'),               #PCB名稱
        "hw_approve_flag"       : request.json.get('hw_approve_flag'),        #主管簽核
        "hw_back_reason"        : request.json.get('hw_back_reason'),         #主管退回原因
        "hw_back_memo"          : request.json.get('hw_back_memo'),           #主管退回說明
        "apply_date"            : request.json.get('apply_date'),             #申請日期       
        "member_cname"          : request.json.get('member_cname'),           #申請人
        "inserted_at"           : datetime.datetime.now(),
        "updated_at"            : datetime.datetime.now(),
        "enable"                : True
    }

    pcb_result_model = pcb_result(mongo.db)
    result = pcb_result_model.insert_pcb_result(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200




# PCB申請退回通知
@blue_pcb_result.route("/api/v0/send/pcb_result/reject/", methods=['post'])
def send_pcb_result_reject_mail():
    # 參數
    project_no      = request.json.get('project_no')
    product_no      = request.json.get('product_no')
    form_no         = request.json.get('form_no')
    reason          = request.json.get('reason')
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
                '<h1>{}-PCB申請單「退回」</h1>'.format(product_no) + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>退回原因: {}</li>'.format(reason) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/pcb_edit/?project_no={}&form_no={}">PCB打樣申請工程規格聯絡單</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
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