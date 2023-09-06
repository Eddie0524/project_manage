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
from apps.settings import FILE_PATH
from flask import send_from_directory
import urllib.parse
import uuid
from datetime import datetime
from apps.exts import mongo
from apps.models.model_new_technology_review import new_technology_review
from apps.models.model_new_technology_review import new_technology_form_review_log
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_new_technology_task import new_technology_task
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_new_technology_form import new_technology_form
from apps.settings import MAIL_RECEIVER



blue_new_technology_review = Blueprint('blue_new_technology_review', __name__)



def init_new_technology_review(app):
    app.register_blueprint(blueprint=blue_new_technology_review)



@blue_new_technology_review.route("/page/v0/new_technology_review/", methods=['GET'])
def new_technology_review_index():

    project_no   = request.args.get('project_no')
    project_name = request.args.get('project_name')
    form_no = request.args.get('form_no')
    mode = 'new_technology_review'


    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
    #group_no = request.cookies.get('group_no')
    
    #print(group_no)

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
        new_technology_review_model = new_technology_review(mongo.db)
      
        param = {'project_no' :   project_no}
        new_technology_model = new_technology_form_model.get_new_technology_form(param)
        new_technology_review_model = new_technology_review_model.get_new_technology_review(param)
       
        print(new_technology_model)
        print(new_technology_review_model)
    
        
        return render_template(
            'new_technology_review.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            FILE_PATH = FILE_PATH,
            USER=member,
            PHOTO=avatar,
            PROJECT_NO=project_no,
            PROJECT_NAME=project_name,
            USER_CNAME=cname,
            RECEIVER=MAIL_RECEIVER,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            NEW_TECH_MODEL=new_technology_model,
            NEW_TECH_REVIEW_MODEL=new_technology_review_model)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)  # 1 MB = 1024 * 1024 bytes
    return mb

# 依照資料夾路徑找出檔案名
def find_files_from_folder(folder_path):

    if os.path.exists(folder_path):
        file_list = []
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            print(file_name)
            file_list.append(file_name)
        return file_list
    else:
        print("資料夾不存在")
        return []


@blue_new_technology_review.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        project_no = request.args.get('project_no')
        file = request.files['file']

        #建立專案名稱資料夾
        folderpath = os.path.join(UPLOAD_FOLDER, project_no + "\\")
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)


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
            strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': strMsg  }}

    return Response(json.dumps(strJson))



@blue_new_technology_review.route('/upload/temp/form_no/<filename>/', methods=['GET'] )
def open_uploaded_file(filename):
    return send_from_directory(UPLOAD_FOLDER, filename )



# 取得特定路徑下所有檔案列表
@blue_new_technology_review.route('/api/v0/upload/files/<folder>/', methods=['GET'] )
def get_upload_file_list_from_folder(folder):
    
    folder_path = os.path.join(UPLOAD_FOLDER, folder)
    res = find_files_from_folder(folder_path)
    strJson = { 'result': 'ok', 'code':'', 'data': res }
    return Response(json.dumps(strJson))



@blue_new_technology_review.route("/api/v0/db/new_technology_review/", methods=['post'])
def insert_new_technology_review():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),
        "project_name":             request.json.get('project_name'),
        "member_list":              request.json.get('member_list'),
        "hw_apporve_flag":          request.json.get('hw_apporve_flag'),
        "hw_reason":                request.json.get('hw_reason'),
        "hw_memo":                  request.json.get('hw_memo'),         
        "project_status":           request.json.get('project_status'),
        "pm_reason":                request.json.get('pm_reason'),
        "pm_memo":                  request.json.get('pm_memo'),
        "pm_expected_date":         request.json.get('pm_expected_date'),
        "appendix_path":            'http://{}/upload/temp/'.format(SERVER_IP), #UPLOAD_FOLDER + "\\{}\\".format(request.json.get('project_no')),                   
        "enable" :                  True ,
        "inserted_at" :             datetime.now() ,
        "updated_at" :              datetime.now() ,
    }
    print("REVIEW")
    print(param)
    new_technology_form_review_model = new_technology_review(mongo.db)
    result = new_technology_form_review_model.insert_new_technology_review(param)
    strJson = { 'result': 'ok', 'code':'01001', 'data': { 'msg': result }}
    return Response(json.dumps(strJson), mimetype='application/json'), 200


@blue_new_technology_review.route("/api/v0/db/new_technology_review/", methods=['get'])
def get_new_technology_form_review():
     

    param = {         
        "project_no":               request.args.get('project_no'),       
    }
    new_technology_form_review_model = new_technology_review(mongo.db)
    result = new_technology_form_review_model.get_new_technology_review(param)
    strJson = { 'result': 'ok', 'code':'01001','msg' : '', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#記錄機構(me)填寫的review log
@blue_new_technology_review.route("/api/v0/db/new_technology_form_review_log/me/", methods=['post'])
def insert_new_technology_form_review_log_me():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),    
        "project_name":             request.json.get('project_name'), 
        "workdays_ee_flag":         request.json.get('workdays_ee_flag'),
        "workdays_me_flag":         request.json.get('workdays_me_flag'),
        "upload_ee_flag":           request.json.get('upload_ee_flag'),
        "upload_me_flag":           request.json.get('upload_me_flag'),  
        "group":                    "me", 
        "hw_apporve_flag":          False,
        "hw_reason":                '', 
        "hw_memo":                  '',                              
        "enable" :                  True ,
        "inserted_at" :             datetime.now() ,
        "updated_at" :              datetime.now() ,
        }
    new_technology_form_review_model = new_technology_form_review_log(mongo.db)
    result = new_technology_form_review_model.insert_new_technology_form_review_log(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' :'', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#記錄電子部(ee)填寫的review log
@blue_new_technology_review.route("/api/v0/db/new_technology_form_review_log/ee/", methods=['post'])
def insert_new_technology_form_review_log_ee():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid":                     form_uuid,
        "project_no":               request.json.get('project_no'),    
        "project_name":             request.json.get('project_name'), 
        "workdays_ee_flag":         request.json.get('workdays_ee_flag'),
        "workdays_me_flag":         request.json.get('workdays_me_flag'),
        "upload_ee_flag":           request.json.get('upload_ee_flag'),
        "upload_me_flag":           request.json.get('upload_me_flag'),
        "group":                    "ee", 
        "hw_apporve_flag":          False,
        "hw_reason":                '',  
        "hw_memo":                  '',                 
        "enable" :                  True ,
        "inserted_at" :             datetime.now() ,
        "updated_at" :              datetime.now() ,
        }
    new_technology_form_review_model = new_technology_form_review_log(mongo.db)
    result = new_technology_form_review_model.insert_new_technology_form_review_log(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' :'', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#記錄hw主管(hw)填寫的review log
@blue_new_technology_review.route("/api/v0/db/new_technology_form_review_log/hw/", methods=['post'])
def insert_new_technology_form_review_log_hw():
    
    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                      :form_uuid,  
        "project_no"                :request.json.get('project_no'),   
        "group"                     :"hw",
        "hw_apporve_flag"           : request.json.get('hw_apporve_flag'),
        "hw_reason"                 : request.json.get('hw_reason') ,
        "hw_memo"                 : request.json.get('hw_memo')         
       
        }
    new_technology_form_review_model = new_technology_form_review_log(mongo.db)
    result = new_technology_form_review_model.insert_new_technology_form_review_log(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' :'', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


#查詢目前ee跟me回報天數及上傳檔案的狀態
@blue_new_technology_review.route("/api/v0/db/check_review_log_status/", methods=['get'])
def check_review_log_status():    
   
    param = {         
        "project_no":               request.args.get('project_no'), 
    }
    print(param)
    
    new_technology_form_review_model = new_technology_form_review_log(mongo.db)
    result = new_technology_form_review_model.check_review_log_status(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' :'', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

#查詢目前回報天數及上傳檔案的狀態
@blue_new_technology_review.route("/api/v0/db/check_review_status/", methods=['get'])
def check_review_status():    
   
    param = {         
        "project_no":               request.args.get('project_no'), 
    }
    print(param)
    
    new_technology_form_review_model = new_technology_review(mongo.db)
    result = new_technology_form_review_model.check_review_status(param)
   
   
    strJson = { 'result': 'ok', 'code':'01001', 'msg' :'', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200


# 新產品技術評估結果通知信
@blue_new_technology_review.route("/api/v0/send/new_technology_review/", methods=['post'])
def send_review_email_by_project_no():
    # 參數

    project_no                  = request.json.get('project_no') 
    project_name                = request.json.get('project_name')  
    expected_workdays_ee        = request.json.get('expected_workdays_ee')
    expected_workdays_me        = request.json.get('expected_workdays_me')
    evaluate_deadline           = request.json.get('evaluate_deadline')
    evaluate_date               = datetime.now().strftime("%Y-%m-%d")
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
    subject  =  '評估案回報通知-{}'.format(project_name)
   
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-評估案回報</h1>'.format(project_name) + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>專案名稱: {}</li>'.format(project_name) + \
                '<li>完成評估日期: {}</li>'.format(evaluate_date) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_review/?project_no={}">新產品技術評估單</a>'.format(DOMAIN_PATH,project_no)+ \
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





# 新產品技術評估結果hw主管同意or退回通知信
@blue_new_technology_review.route("/api/v0/send/new_technology_review/hw/", methods=['post'])
def send_review_email_by_hw():
    # 參數

    project_no                  = request.json.get('project_no') 
    project_name                = request.json.get('project_name')  
    expected_workdays_ee        = request.json.get('expected_workdays_ee')
    expected_workdays_me        = request.json.get('expected_workdays_me')
    hw_apporve_flag             = request.json.get('hw_apporve_flag')
    hw_reason                   = request.json.get('hw_reason')
    hw_memo                     = request.json.get('hw_memo')
    evaluate_deadline           = request.json.get('evaluate_deadline')
    evaluate_date               = datetime.now().strftime("%Y-%m-%d")
  
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
    subject  =  '評估案回報通知-{}'.format(project_name)

    if hw_apporve_flag  == True:
   
        message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>{}-評估案回報</h1>'.format(project_name) + \
                '<ul>' + \
                '<li>專案代號:{}</li>'.format(project_no) + \
                '<li>專案名稱:{}</li>'.format(project_name) + \
                '<li>完成評估日期:{}</li>'.format(evaluate_date) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_technology_result/?project_no={}">新產品技術評估單 </a>'.format(DOMAIN_PATH,project_no)+ \
                '</body>' + \
                '</html>'
    else :
        message  =  '<!DOCTYPE html>' + \
                    '<html leng="en">' + \
                    '<head><meta charset="utf-8"></head>' + \
                    '<body>' + \
                    '<h1>{}-評估案回報「退回」</h1>'.format(project_name) + \
                    '<ul>' + \
                    '<li>專案代號:{}</li>'.format(project_no) + \
                    '<li>專案名稱:{}</li>'.format(project_name) + \
                    '<li>評估期限:{}</li>'.format(evaluate_deadline) + \
                    '<li>退回原因:{}</li>'.format(hw_reason) + \
                    '</ul><br/>' + \
                    '<a href="http://{}/page/v0/new_technology_feedback/">新產品技術評估單</a>'.format(DOMAIN_PATH) + \
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


#取回評估單指派名單
@blue_new_technology_review.route("/api/v0/db/new_technology_review/member_list/", methods=['get'])
def get_new_technology_review_member_list():     

    param = {         
        "project_no":               request.args.get('project_no'),       
    }   
    
    new_technology_form_review_model = new_technology_review(mongo.db)
    data = new_technology_form_review_model.get_new_technology_review(param)


    print(data)
    result = {"member_list" : data['member_list'] }   
    strJson = { 'result': 'ok', 'code':'01001','msg' : '', 'data':  result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#主管指派人員工作項目
@blue_new_technology_review.route("/api/v0/db/new_tech_review/update_memberlist/", methods=['post'])
def update_new_project_form_memberlist():
       
    
    param = { 
        "project_no":         request.json.get('project_no'),
        "member_list":        request.json.get('member_list'),
        
    }
    
   
    new_technology_review_model = new_technology_review(mongo.db)
    result = new_technology_review_model.update_new_tech_review_memberlist(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200  