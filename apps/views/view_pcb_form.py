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
from apps.models.model_layout_form import layout_form
from apps.models.model_pcb_form import pcb_form
from apps.models.model_pcb_form import modify_pcb_form
from apps.models.model_pcb_form import pcb_form_product_version
from apps.models.model_member   import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname
import random




blue_pcb_form = Blueprint('blue_pcb_form', __name__)



def init_pcb_form(app):
    app.register_blueprint(blueprint=blue_pcb_form)




@blue_pcb_form.route("/page/v0/pcb_form/", methods=['GET'])
def pcb_form_index():
    
    form_no = request.args.get('form_no')
    project_no = request.args.get('project_no')
    mode = "pcb_form"

    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
    #group_no = request.cookies.get('group_no')
    department = request.cookies.get('department')
   
    #print(group_no)

    if account is None:
        return redirect(url_for('blue_main.login_fun'))

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
            'project_no'    : project_no,
            'form_no'       : form_no
        }

       
        pcb_model    = pcb_form_model.get_pcb_form(param)        
        layout_form_model = layout_form(mongo.db)
        layout_model = layout_form_model.get_layout_form(param)
        print(pcb_model)
        print(department)

        return render_template(
            'pcb_form.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            DEPARTMENT=department,
            RECEIVER=MAIL_RECEIVER,
            IS_LEADER=isleader,
            PCB_MODEL=pcb_model,
            LAYOUT_MODEL=layout_model
        )



@blue_pcb_form.route("/api/v0/db/pcb_form/", methods=['post'])
def insert_pcb_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                : form_uuid,
        "form_type"           :request.json.get('form_type'),             #申請單種類
        "project_type":        "新產品開發申請單",                          #申請單種類
        "project_name"        :request.json.get('project_name'),           
        "project_no"          : request.json.get('project_no'),           #專案代號
        "bu"                  :request.json.get('bu'),                  #BU       
        "department"          : request.json.get('department'),           #申請部門
        "member_cname"        : request.json.get('member_cname'),            #申請人 
        "form_no"             : request.json.get('form_no'),            #表單編號
        "pcb_name"            : request.json.get('pcb_name'),             #PCB名稱
        "apply_date"          : request.json.get('apply_date'),           #申請日期
        "require_date"        : request.json.get('require_date'),         #需求日期
        "product_no"          : request.json.get('product_no'),           #產品型號
        "product_name"        : request.json.get('product_name'),           #產品型號
        "version"             : request.json.get('version'),              #版本
        "pcb_type"            : request.json.get('pcb_type'),             #打樣類型(新產品打樣/舊有產品修改/其他)
        "gerber_name"         : request.json.get('gerber_name'),          #gerber_name 
        "place_of_production" : request.json.get('place_of_production'),  #製作地區
        "place_of_deliver"    : request.json.get('place_of_deliver'),     #交付地區
        "deliver_count"       : request.json.get('deliver_count'),        #交付數量
        "purpose_pcb"         : request.json.get('purpose_pcb'),          #洗板目的 
        "board_spec"          : request.json.get('board_spec'),           #板材規格
        "board_diff"          : request.json.get('board_diff'),           #板厚誤差
        "impedance_diff"      : request.json.get('impedance_diff'),       #阻抗誤差
        "surface_treatment"   : request.json.get('surface_treatment'),    #表面處理
        "enig"                : request.json.get('enig'),                 #化金厚度
        "process"             : request.json.get('process'),              #製程
        "dimensional_drawing" : request.json.get('dimensional_drawing'),  #成型尺寸圖
        "weld_color"          : request.json.get('weld_color'),           #防焊顏色
        "ul_mark"             : request.json.get('ul_mark'),              #UL_MARK
        "date_code"           : request.json.get('date_code'),            #date_code
        "font"                : request.json.get('font'),                 #文字
        "font_color"          : request.json.get('font_color'),           #文字顏色
        "goldfinger_angle"    : request.json.get('goldfinger_angle'),     #金手指導繳
        "angle_depth"         : request.json.get('angle_depth'),          #導角深度
        "via_general"         : request.json.get('via_general'),          #過孔阻焊方式(一般)
        "via_bga"             : request.json.get('via_bga'),              #過孔阻焊方式(BGA)
        "via_special"         : request.json.get('via_special'),          #過孔阻焊方式(特殊)
        "sample_require"      : request.json.get('sample_require'),       #樣品需求數
        "sample_bad"          : request.json.get('sample_bad'),           #樣品不良板
        "sample_vcut"         : request.json.get('sample_vcut'),          #樣品vcut
        "attach"              : request.json.get('attach'),               #交貨附件
        "pcb_back_date"       : request.json.get('pcb_back_date'),        #PCB回廠日期
        "inserted_at"         : datetime.datetime.now(),
        "updated_at"          : datetime.datetime.now(),
        "enable"              : True 
    }

    
    pcb_form_model = pcb_form(mongo.db)
    result = pcb_form_model.insert_pcb_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': ''  , 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

@blue_pcb_form.route("/api/v0/db/modify_pcb_form/", methods=['post'])
def insert_modify_pcb_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                : form_uuid,
        "form_type"           :request.json.get('form_type'),             #申請單種類
        "project_no"          : request.json.get('project_no'),           #專案代號
        "department"          : request.json.get('department'),           #申請部門
        "member_cname"        : request.json.get('member_cname'),            #申請人 
        "form_no"             : request.json.get('form_no'),            #表單編號
        "pcb_name"            : request.json.get('pcb_name'),             #PCB名稱
        "apply_date"          : request.json.get('apply_date'),           #申請日期
        "require_date"        : request.json.get('require_date'),         #需求日期
        "product_no"          : request.json.get('product_no'),           #產品型號
        "version"             : request.json.get('version'),              #版本
        "pcb_type"            : request.json.get('pcb_type'),             #打樣類型(新產品打樣/舊有產品修改/其他)
        "gerber_name"         : request.json.get('gerber_name'),          #gerber_name 
        "place_of_production" : request.json.get('place_of_production'),  #製作地區
        "place_of_deliver"    : request.json.get('place_of_deliver'),     #交付地區
        "deliver_count"       : request.json.get('deliver_count'),        #交付數量
        "purpose_pcb"         : request.json.get('purpose_pcb'),          #洗板目的 
        "board_spec"          : request.json.get('board_spec'),           #板材規格
        "board_diff"          : request.json.get('board_diff'),           #板厚誤差
        "impedance_diff"      : request.json.get('impedance_diff'),       #阻抗誤差
        "surface_treatment"   : request.json.get('surface_treatment'),    #表面處理
        "enig"                : request.json.get('enig'),                 #化金厚度
        "process"             : request.json.get('process'),              #製程
        "dimensional_drawing" : request.json.get('dimensional_drawing'),  #成型尺寸圖
        "weld_color"          : request.json.get('weld_color'),           #防焊顏色
        "ul_mark"             : request.json.get('ul_mark'),              #UL_MARK
        "date_code"           : request.json.get('date_code'),            #date_code
        "font"                : request.json.get('font'),                 #文字
        "font_color"          : request.json.get('font_color'),           #文字顏色
        "goldfinger_angle"    : request.json.get('goldfinger_angle'),     #金手指導繳
        "angle_depth"         : request.json.get('angle_depth'),          #導角深度
        "via_general"         : request.json.get('via_general'),          #過孔阻焊方式(一般)
        "via_bga"             : request.json.get('via_bga'),              #過孔阻焊方式(BGA)
        "via_special"         : request.json.get('via_special'),          #過孔阻焊方式(特殊)
        "sample_require"      : request.json.get('sample_require'),       #樣品需求數
        "sample_bad"          : request.json.get('sample_bad'),           #樣品不良板
        "sample_vcut"         : request.json.get('sample_vcut'),          #樣品vcut
        "attach"              : request.json.get('attach'),               #交貨附件
        "pcb_back_date"       : request.json.get('pcb_back_date'),        #PCB回廠日期
        "inserted_at"         : datetime.datetime.now(),
        "updated_at"          : datetime.datetime.now(),
        "enable"              : True 
    }

    
    modify_pcb_form_model = modify_pcb_form(mongo.db)
    result = modify_pcb_form_model.insert_modify_pcb_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': ''  , 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#生成單據編號
@blue_pcb_form.route("/api/v0/db/pcb_form_no/", methods=['get'])
def generate_layout_form_no():

        SerialNum = "P" + "{}{:02d}{:02d}{:04d}".format(
            (int(datetime.datetime.now().year)),
            datetime.datetime.now().month ,
            datetime.datetime.now().day,
            random.randint(1,99))

        return Response(json.dumps(SerialNum), mimetype='application/json'), 200


#寫入pcb表單 產品版本
@blue_pcb_form.route("/api/v0/db/pcb_form_product_version/", methods=['post'])
def insert_pcb_form_product_version():

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
    
    pcb_form_model = pcb_form_product_version(mongo.db)
    result = pcb_form_model.insert_pcb_form_product_version(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#取回pcb表單 產品版本
@blue_pcb_form.route("/api/v0/db/pcb_form_product_version/", methods=['get'])
def get_pcb_form_product_version():
    
    param = {
        "project_no" : request.args.get("project_no")
    }
    pcb_form_model = pcb_form_product_version(mongo.db)
    result = pcb_form_model.get_pcb_form_product_version(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

# pcb申請通知信
@blue_pcb_form.route("/api/v0/send/pcb_form/", methods=['post'])
def send_require_email_by_project_no():
    # 參數
    project_no      = request.json.get('project_no')
    form_no         = request.json.get('form_no')
    product_no      = request.json.get('product_no')
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
    subject  =  'PCB打樣申請工程規格聯絡單-{}'.format(product_no)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>PCB打樣申請工程規格聯絡單-請您簽核</h1>' + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>版本: {}</li>'.format(version) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/pcb_result/?project_no={}&form_no={}">PCB打樣申請工程規格聯絡單</a>'.format(DOMAIN_PATH,project_no,form_no)+ \
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
@blue_pcb_form.route("/api/v0/db/get/project_no/pcb_form_product_version/", methods=['get'])
def get_project_no_from_layout_form_product_version():
    
   
    pcb_form_model = pcb_form_product_version(mongo.db)
    result = pcb_form_model.get_project_no_from_pcb_form_product_version()
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' ,'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

