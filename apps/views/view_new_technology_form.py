from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import UPLOAD_FOLDER
from apps.settings import MAIL_RECEIVER
from flask import send_from_directory
from werkzeug.utils import secure_filename
import urllib.parse
import json
import time
import uuid
from apps.exts import mongo
from apps.models.model_new_technology_form import modify_new_technology_form
from apps.models.model_new_technology_form import new_technology_form
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random




blue_new_technology_form = Blueprint('blue_new_technology_form', __name__)


def init_new_technology_form(app):
    app.register_blueprint(blueprint=blue_new_technology_form)




@blue_new_technology_form.route("/page/v0/new_technology_form/", methods=['GET'])
def new_technology_form_index():
    
    project_no      = request.args.get('project_no')
    form_no         = request.args.get('form_no')
    mode            = "new_technology_form"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(avatar)

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
                
        return render_template(
            'new_technology_form.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            RECEIVER=MAIL_RECEIVER,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            PROJECT_NO=project_no)


@blue_new_technology_form.route("/api/v0/db/new_technology_form/", methods=['post'])
def insert_new_technology_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = {
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),
        "project_name":             request.json.get('project_name'),
        "form_type":                request.json.get('form_type'),                       #申請單種類
        "project_type":             'technology',                       
        "bu":                       request.json.get('bu'),
        "form_no":                  request.json.get('form_no'),
        "product_name":             request.json.get('product_name'),
        "product_describe":         request.json.get('product_describe'),
        "product_application":      request.json.get('product_application'),
        "spec_describe":            request.json.get('spec_describe'),
        "customer_require":         request.json.get('customer_require'),
        "expected_finished_date":   request.json.get('expected_finished_date'),
        "cost":                     request.json.get('cost'),
        "estimate_date":            request.json.get('estimate_date'),
        "apply_date":               request.json.get('apply_date'),
        "member_cname":             request.json.get('member_cname'),
        "inserted_at":              datetime.datetime.now(),
        "updated_at":               datetime.datetime.now(),
        "status":                   request.json.get('status'),
        "enable" :                  True 
    }
    new_technology_form_model = new_technology_form(mongo.db)
    result = new_technology_form_model.insert_new_technology_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_new_technology_form.route("/api/v0/db/modify_new_technology_form/", methods=['post'])
def insert_modify_new_technology_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = {
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),
        "project_name":             request.json.get('project_name'),
        "form_type":                request.json.get('form_type'),                       #申請單種類
        "project_type":             'technology',                       
        "bu":                       request.json.get('bu'),
        "form_no":                  request.json.get('form_no'),
        "product_name":             request.json.get('product_name'),
        "product_describe":         request.json.get('product_describe'),
        "product_application":      request.json.get('product_application'),
        "spec_describe":            request.json.get('spec_describe'),
        "customer_require":         request.json.get('customer_require'),
        "expected_finished_date":   request.json.get('expected_finished_date'),
        "cost":                     request.json.get('cost'),
        "estimate_date":            request.json.get('estimate_date'),
        "apply_date":               request.json.get('apply_date'),
        "member_cname":             request.json.get('member_cname'),
        "inserted_at":              datetime.datetime.now(),
        "updated_at":               datetime.datetime.now(),
        "status":                   request.json.get('status'),
        "enable" :                  True 
    }
    modifynew_technology_form_model = modify_new_technology_form(mongo.db)
    result = modifynew_technology_form_model.insert_modify_new_technology_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_new_technology_form.route("/api/v0/db/new_technology_form/by/project_no/", methods=['post'])
def get_new_technology_form():

    form_uuid = request.json.get('uuid')
    param = { 
        "uuid":    form_uuid,
        "project_no": request.json.get('project_no')
    }
    new_technology_form_model = new_technology_form(mongo.db)
    result = new_technology_form_model.get_new_technology_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_new_technology_form.route("/api/v0/db/new_technology_form/", methods=['delete'])
def delete_new_technology_form():

    param = { 
        "uuid":    request.json.get('uuid'),
        "form_no": request.json.get('form_no')
    }
    new_technology_form_model = new_technology_form(mongo.db)
    result = new_technology_form_model.delete_new_technology_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200

#取專案代號
@blue_new_technology_form.route("/api/v0/db/new_technology_project_no/", methods=['get'])
def generate_new_technology_form_no():

        SerialNum = "AA{}".format(ReturnCode(request.args.get('bu')) ) +"-R-OA" + "{}{:02d}{:02d}{:03d}".format((int(datetime.datetime.now().year) - 1911), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,99))
        #result = get_form_sn(db)
        #print(result)
        return Response(json.dumps(SerialNum), mimetype='application/json'), 200



#取表單編號
@blue_new_technology_form.route("/api/v0/db/new_technology_form_no/", methods=['get'])
def generate_new_technology_form_code():

    SerialNum = "E" + "{}{:02d}{:02d}{:04d}".format((int(datetime.datetime.now().year)), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,99))
    return Response(json.dumps(SerialNum), mimetype='application/json'), 200


@blue_new_technology_form.route("/api/v0/send/new_technology/task/",  methods=['post'])
def send_task_to_member():
    # project_no             = request.args.get('no')
    # account                = request.args.get('account')
    # project_expected_start = request.args.get('start')
    # project_expected_end   = request.args.get('end')
    selected_value = request.form['mySelect']
    # 在这里处理所选值，可以将其保存到数据库、发送电子邮件等。
    # 示例中仅打印所选值。
    print('选定值为:', selected_value)
    return '表单提交成功！'


# 申請單送出申請通知信
@blue_new_technology_form.route("/api/v0/send/new_technology_form/", methods=['post'])
def send_require_email_by_project_no():
    # 參數
    form_no         = request.json.get('form_no')
    project_no      = request.json.get('project_no')
    project_name    = request.json.get('project_name')
    project_start   = request.json.get('project_start')
    project_end     = request.json.get('project_end')
    sender_mail     = request.json.get('sender')       # 寄件者
    receiver_list   = request.json.get('receiver')     # 收件者 (陣列)
    cc_list         = request.json.get('cc')           # CC者  (陣列)
    file_list       = request.json.get('file_list')     
     
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


    # attach_str = ''
    # for item in file_list:
    #     str_split = item.split('/')
    #     print(str_split[len(str_split)-1])
    #     print('************************')
    #     attach_str += '<a href ={}>{}</a>'.format(item,str_split[len(str_split)-1 ]) + "\n"
    #print(attach_str)

    
    sender   =  sender_mail
    receiver =  receiver_mail
    subject  =  '申請通知-{}'.format(project_name)
    
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品技術評估單-請您協助評估​</h1>' + \
                '<ul>' + \
                '<li>專案代號​:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>評估期限日期:{}</li>'.format(project_end) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_task/?project_no={}&form_no={}">新產品技術評估申請單</a>'.format(DOMAIN_PATH, project_no,form_no) + \
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


def ReturnCode(BU : str):
    try: 
        if BU == "IO":
            return "01"
        elif BU == "IOT":
            return "02"
        elif BU == "IT":
            return "03"
        elif BU == "EMS":
            return "04" 
        else:
            return "00"
    except:
        return "00"


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)  # 1 MB = 1024 * 1024 bytes
    return mb

#上傳檔案
@blue_new_technology_form.route('/api/v0/spec/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        project_no = request.args.get('project_no')
        print('======================')
        print(project_no)
            
        if project_no == '':
            strJson = { 'result':'faile', 'code':'', 'msg':'上傳失敗', 'data':{}}
            return Response(json.dumps(strJson))
            
        else:
            #建立專案名稱資料夾
            folderpath = os.path.join(UPLOAD_FOLDER, project_no + "\\")
            if not os.path.exists(folderpath):
                os.makedirs(folderpath)

            print(request.files)
            file = request.files.get('file', None)
            filename = file.filename
            print(filename)
            
            if filename == '':
                strJson = { 'result':'fail', 'code':'', 'msg':'未選擇檔案', 'data':{}}
                return Response(json.dumps(strJson))

            else:
                file = request.files['file']

                if file and allowed_file(file.filename):
                    filename = secure_filename(urllib.parse.quote(file.filename.encode('utf-8')))
                    print(filename)
                    #print(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
                    # 儲存檔案
                    #file.save(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
                    file.save(os.path.join(folderpath + "\\" + file.filename))
                    #file_size_bytes = os.path.getsize(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
                    file_size_bytes = os.path.getsize(os.path.join(folderpath + "\\" + file.filename))
                    print(file_size_bytes)
                    file_size_mb = convert_bytes_to_mb(file_size_bytes)
                    print(file_size_mb)
                    strMsg = '[ {} ], 檔案大小 : {}  MB 上傳成功'.format(file.filename, round(file_size_mb, 2))
                    strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{ 'file_name': file.filename }}
                    resp = Response(json.dumps(strJson))
                    return resp, 200
                

#上傳檔案
@blue_new_technology_form.route('/api/v0/spec/remove/', methods=['GET'])
def remove_file():

    if request.method == 'GET':

        project_no = request.args.get('project_no')
        file_name = request.args.get('file_name') 
        print('======================')
        print(project_no)
        print(file_name)
        print("86868686868")
            
        if project_no == '':
            strJson = { 'result':'faile', 'code':'', 'msg':'刪除失敗', 'data':{}}
            return Response(json.dumps(strJson))
            
        else:
            #建立專案名稱資料夾
            folderpath = os.path.join(UPLOAD_FOLDER, project_no + "\\")
            if not os.path.exists(folderpath):
                strJson = { 'result':'faile', 'code':'', 'msg':'刪除失敗', 'data':{}}
                return Response(json.dumps(strJson))

           
            
                
        if file_name != '' :
            print(folderpath + "\\" + file_name)
            os.remove(folderpath + "\\" + file_name)
            strMsg = '[ {} ], 刪除成功'.format(file_name)
            strJson = { 'result':'ok', 'code':'', 'msg':strMsg, 'data':{ 'file_name': file_name }}
            resp = Response(json.dumps(strJson))
            return resp, 200
                




#取回全部評估案名稱
@blue_new_technology_form.route("/api/v0/db/all_new_tech_project_name/", methods=['GET'])
def get_all_new_tech_project_name():

    new_technology_form_model = new_technology_form(mongo.db)
    result = new_technology_form_model.get_all_new_tech_project_name()
    strJson = { 'result': 'ok', 'code':'01001','msg'  : ' ', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#取回全部評估案名稱
@blue_new_technology_form.route("/api/v0/db/find/upload_file/", methods=['GET'])
def get_upload_file():

    param = {
        'project_no' : request.args.get('project_no')
    }
    new_technology_form_model = new_technology_form(mongo.db)
    result = new_technology_form_model.get_upload_file(param)
    strJson = { 'result': 'ok', 'code':'01001','msg'  : ' ', 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



