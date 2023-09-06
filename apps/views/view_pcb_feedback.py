from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import smtplib
import json
import time
from apps.settings import SMTP_INFO
from apps.exts import mongo

blue_pcb_feedback = Blueprint('blue_pcb_feedback', __name__)



def init_pcb_feedback(app):
    app.register_blueprint(blueprint=blue_pcb_feedback)
    
    
    

@blue_pcb_feedback.route("/page/v0/pcb_feedback/", methods=['GET'])
def pcb_feedback_index():
    
    mode = 'pcb_feedback'
    
    project_no = request.args.get('project_no')
    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    cname   = request.cookies.get('cName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName')
    #group_no = request.cookies.get('group_no')
    
    #print(account)
    #print(avatar)
    
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO=project_no))

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
                
        return render_template(
            'pcb_feedback.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            ACCOUNT=account)
    

    # 新開案PCB申請單通知(發信給RD提醒申請pcb表單)
@blue_pcb_feedback.route("/api/v0/send/new_project_feedback/pcb/", methods=['post'])
def send_require_email_by_project_no():
    # 參數
    project_no    = request.json.get('project_no')
    product_no  = request.json.get('product_no')
    # project_start = request.json.get('project_start')
    # project_end   = request.json.get('project_end')
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
    subject  =  '{}-新產品開案PCB聯絡單申請通知'.format(product_no)
    
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開案PCB聯絡單申請通知</h1>' + \
                '<ul>' + \
                '<li>產品型號:{}</li>'.format(product_no) + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '</ul><br/>' + \
                '<h3>請收到此通知點擊下方連結進行PCB聯絡單申請</h3><br/>' + \
                '<a href="http://{}/page/v0/page/PCB_form/">連結</a>'.format(DOMAIN_PATH) + \
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