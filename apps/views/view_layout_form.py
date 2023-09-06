from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import SERVER_IP
from apps.settings import FILE_PATH
import json
import time
import os
from werkzeug.utils import secure_filename
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import UPLOAD_FOLDER
from apps.settings import MAIL_RECEIVER
from flask import send_from_directory
import urllib.parse
import uuid
import datetime
from apps.exts import mongo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_layout_form import layout_form,modify_layout_form,layout_form_product_version
from apps.models.model_new_project_form import new_project_form
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import random





blue_layout_form = Blueprint('blue_layout_form', __name__)



def init_layout_form(app):
    app.register_blueprint(blueprint=blue_layout_form)



@blue_layout_form.route("/page/v0/layout_form/", methods=['GET'])
def layout_form_index():

    form_no = request.args.get('form_no')
    project_no = request.args.get('project_no')
    mode = "layout_form"

    # check cookie
    account    = request.cookies.get('account' )
    avatar     = request.cookies.get('avatar'  )
    member     = request.cookies.get('eName'   )
    sex        = request.cookies.get('sex'     )
    cname      = request.cookies.get('cName'   )
    group_no   = request.cookies.get('group_no')
    department = request.cookies.get('department')
    
    #print(group_no)

    if account is None:
        return redirect(url_for('blue_main.login_fun'))

    else:
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
                
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
        print(department)

        return render_template(
            'layout_form.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            DEPARTMENT=department,
            PROJECT_NO=project_no,
            RECEIVER=MAIL_RECEIVER,
            IS_LEADER=isleader,
            NEW_PROJECT_MODEL=new_project_model)



@blue_layout_form.route("/api/v0/db/layout_form/", methods=['post'])
def insert_layout_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = {
        "uuid"                : form_uuid,                                  #識別編碼
        "project_type":        "新產品開發申請單",
        "project_name"        : request.json.get('project_name'),
        "form_type"           :request.json.get('form_type'),             #申請單種類
        "project_no"          : request.json.get('project_no'),             #專案代號
        "bu"                  : request.json.get('bu'),                     #歸屬部門
        "department"          : request.json.get('department'),             #申請部門
        "form_no"             : request.json.get('form_no'),                #表單編號
        "product_no"          : request.json.get('product_no'),             #產品型號
        "product_name"        : request.json.get('product_name'), 
        "pcb_name"            : request.json.get('pcb_name'),               #PCB名稱
        "version"             : request.json.get('version'),                #版本
        "version_mode"        : request.json.get('version_mode'),           #版本類型(大/小)改版
        "apply_date"          : request.json.get('apply_date'),             #申請日期
        "product_apply"       : request.json.get('product_apply'),          #產品申請or修改
        "product_describe"    : request.json.get('product_describe'),       #產品說明
        "spec_2Layer"         : request.json.get('spec_2Layer'),            #板材規格spec_2Layer
        "spec_4Layer"         : request.json.get('spec_4Layer'),            #板材規格spec_4Layer
        "spec_6Layer"         : request.json.get('spec_6Layer'),            #板材規格spec_6Layer
        "spec_other"          : request.json.get('spec_other'),             #板材規格其他
        "impedance_require"   : request.json.get('impedance_require'),      #阻抗需求
        "impedance_diff"      : request.json.get('impedance_diff'),         #阻抗誤差
        "impedance_memo"      : request.json.get('impedance_memo'),         #阻抗備註
        "dimensional_drawing" : request.json.get('dimensional_drawing'),    #成型尺寸圖
        "logo_require"        : request.json.get('logo_require'),           #Logo需求
        "logo_memo"           : request.json.get('logo_memo'),              #Logo需求其他
        "component"           : request.json.get('component'),              #零件擺放
        "font"                : request.json.get('font'),                   #文字
        "goldfinger"          : request.json.get('goldfinger'),             #金手指規範
        "file"                : request.json.get('file'),                   #提供文檔
        "gerber"              : request.json.get('gerber'),                 #gerber
        "work_file_format"    : request.json.get('work_file_format'),       #工作檔格式
        "gerber_format"       : request.json.get('gerber_format'),          #gerber格式
        "fulldata_date"       : request.json.get('fulldata_date'),          #提供完整資料日期
        "gerber_date"         : request.json.get('gerber_date'),            #gerber需求日期
        "member_cname"        : request.json.get('member_cname'),           #申請人
        "inserted_at"         : datetime.datetime.now(),
        "updated_at"          : datetime.datetime.now(),
        "enable"              : True
    }

    layout_form_model = layout_form(mongo.db)
    result = layout_form_model.insert_layout_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_layout_form.route("/api/v0/db/modify_layout_form/", methods=['post'])
def insert_modify_layout_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = {
        "uuid"                : form_uuid,                                  #識別編碼
        "form_type"           :request.json.get('form_type'),             #申請單種類
        "project_no"          : request.json.get('project_no'),             #專案代號
        "bu"                  : request.json.get('bu'),                     #歸屬部門
        "project_name"        : request.json.get('project_name'),
        "department"          : request.json.get('department'),             #申請部門
        "form_no"             : request.json.get('form_no'),                #表單編號
        "product_no"          : request.json.get('product_no'),             #產品型號
        "product_name"        : request.json.get('product_name'), 
        "pcb_name"            : request.json.get('pcb_name'),               #PCB名稱
        "version"             : request.json.get('version'),                #版本
        "version_mode"        : request.json.get('version_mode'),           #版本類型(大/小)改版
        "apply_date"          : request.json.get('apply_date'),             #申請日期
        "product_apply"       : request.json.get('product_apply'),          #產品申請or修改
        "product_describe"    : request.json.get('product_describe'),       #產品說明
        "spec_2Layer"         : request.json.get('spec_2Layer'),            #板材規格spec_2Layer
        "spec_4Layer"         : request.json.get('spec_4Layer'),            #板材規格spec_4Layer
        "spec_6Layer"         : request.json.get('spec_6Layer'),            #板材規格spec_6Layer
        "spec_other"          : request.json.get('spec_other'),             #板材規格其他
        "impedance_require"   : request.json.get('impedance_require'),      #阻抗需求
        "impedance_diff"      : request.json.get('impedance_diff'),         #阻抗誤差
        "impedance_memo"      : request.json.get('impedance_memo'),         #阻抗備註
        "dimensional_drawing" : request.json.get('dimensional_drawing'),    #成型尺寸圖
        "logo_require"        : request.json.get('logo_require'),           #Logo需求
        "logo_memo"           : request.json.get('logo_memo'),              #Logo需求其他
        "component"           : request.json.get('component'),              #零件擺放
        "font"                : request.json.get('font'),                   #文字
        "goldfinger"          : request.json.get('goldfinger'),             #金手指規範
        "file"                : request.json.get('file'),                   #提供文檔
        "gerber"              : request.json.get('gerber'),                 #gerber
        "work_file_format"    : request.json.get('work_file_format'),       #工作檔格式
        "gerber_format"       : request.json.get('gerber_format'),          #gerber格式
        "fulldata_date"       : request.json.get('fulldata_date'),          #提供完整資料日期
        "gerber_date"         : request.json.get('gerber_date'),            #gerber需求日期
        "member_cname"        : request.json.get('member_cname'),           #申請人
        "inserted_at"         : datetime.datetime.now(),
        "updated_at"          : datetime.datetime.now(),
        "enable"              : True
    }

    modify_layout_form_model = modify_layout_form(mongo.db)
    result = modify_layout_form_model.insert_modify_layout_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

#生成單據編號
@blue_layout_form.route("/api/v0/db/layout_form_no/", methods=['get'])
def generate_layout_form_no():

        SerialNum = "L" + "{}{:02d}{:02d}{:04d}".format(
            (int(datetime.datetime.now().year)),
            datetime.datetime.now().month ,
            datetime.datetime.now().day,
            random.randint(1,99))

        return Response(json.dumps(SerialNum), mimetype='application/json'), 200



#生成單據編號
@blue_layout_form.route("/api/v0/db/layout_form_version/", methods=['get'])
def generate_layout_form_version():

       version = ''
       if request.args.get('version') == 'large':
            version =  'v1.0'
       else :
            version = 'v0.1'
       return Response(json.dumps(version), mimetype='application/json'), 200



@blue_layout_form.route("/api/v0/db/layout_form_task/", methods=['post'])
def insert_layout_form_task():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                 : form_uuid,
        "form_no"              : request.json.get('form_no'),
        "project_name"         : request.json.get('project_name'),
        "bu"                   : request.json.get('bu'),
        "member_cname"         : request.json.get('member_cname'),
        "expected_start_date"  : request.json.get('expected_start_date'),
        "expected_finish_date" : request.json.get('expected_finish_date'),
        "status"               : request.json.get('status'),
        "task"                 : request.json.get('task'),
        "mile_stone"           : request.json.get('mile_stone'),
        "reason"               : request.json.get('reason'),
        "memo"                 : request.json.get('memo'),
        "actual_date"          : datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "back_reason"          : request.json.get('back_reason'),
        "back_memo"            : request.json.get('back_memo'),
        "enable"               : True,
        "inserted_at"          : datetime.datetime.now(),
        "updated_at"           : datetime.datetime.now(),
        }
    
    layout_form_model = layout_form(mongo.db)
    result = layout_form_model.insert_layout_form_task(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#寫入layout表單 產品版本
@blue_layout_form.route("/api/v0/db/layout_form_product_version/", methods=['post'])
def insert_layout_form_product_version():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                 : form_uuid,
        "project_no"           : request.json.get('project_no'),
        "product_no"           : request.json.get('product_no'),
        "major_version"        : request.json.get('major_version'),
        "minor_version"        : request.json.get('minor_version'),
        "enable"               : True,
        "inserted_at"          : datetime.datetime.now(),
        "updated_at"           : datetime.datetime.now(),
    }
    
    layout_form_model = layout_form_product_version(mongo.db)
    result = layout_form_model.insert_layout_form_product_version(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#取回layout表單 產品版本
@blue_layout_form.route("/api/v0/db/layout_form_product_version/", methods=['get'])
def get_layout_form_product_version():
    
    param = {
        "project_no" : request.args.get("project_no")
    }
    layout_form_model = layout_form_product_version(mongo.db)
    result = layout_form_model.get_layout_form_product_version(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#取回layout表單 (專案代號、產品型號、PCB名稱、版本、bu)
@blue_layout_form.route("/api/v0/db/all_layout_form/", methods=['get'])
def get_all_layout_form():
       
    layout_form_model = layout_form(mongo.db)
    result = layout_form_model.get_all_layout_form()
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# layout申請通知信
@blue_layout_form.route("/api/v0/send/layout_form/", methods=['post'])
def send_require_email_by_project_no():

    # 參數
    project_no      = request.json.get('project_no')
    product_no      = request.json.get('product_no')
    form_no         = request.json.get('form_no')
    version         = request.json.get('version')
    
  
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
    subject  =  'Layout申請工程規格聯絡單-{}'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>Layout申請工程規格聯絡單-請您簽核</h1>' + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>版本: {}</li>'.format(version) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/layout_result/?project_no={}&form_no={}">Layout申請工程規格聯絡單連結</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
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





#取回產品版本所有專案代號
@blue_layout_form.route("/api/v0/db/get/project_no/layout_form_product_version/", methods=['get'])
def get_project_no_from_layout_form_product_version():
    
   
    layout_form_model = layout_form_product_version(mongo.db)
    result = layout_form_model.get_project_no_from_layout_form_product_version()
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200