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
from apps.models.model_new_project_form import new_project_form
from apps.models.model_new_project_form import new_project_form_log
from apps.models.model_new_project_form import modify_new_project_form
from apps.models.model_new_technology_form import new_technology_form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
import random
from apps.exts import logger



blue_new_project_form = Blueprint('blue_new_project_form', __name__)



def init_new_project_form(app):
    app.register_blueprint(blueprint=blue_new_project_form)



@blue_new_project_form.route("/page/v0/new_project_form/", methods=['GET'])
def new_project_form_index():
    

    mode = "new_project_form"
    form_no    = request.args.get('form_no')
    project_no = request.args.get('new_tech_project_no')
    
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
        
        new_tech_form_model = new_technology_form(mongo.db)
        param = {
            'project_no' : project_no
        }

        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)       
        new_technology_model = new_tech_form_model.get_new_technology_form(param)
    

        return render_template(
            'new_project_form.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER = MAIL_RECEIVER,
            NEW_TECH_MODEL=new_technology_model)



#PM填寫新開案申請單
@blue_new_project_form.route("/api/v0/db/new_project_form/", methods=['post'])
def insert_new_project_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')


    param = { 
        "uuid":                           form_uuid,
        "new_tech_project_no":            request.json.get('new_tech_project_no'),             #關聯評估案代號
        "form_no":                        request.json.get('form_no'),                         #單號
        "project_type":                   'project',                   
        "form_type":                      request.json.get('form_type'),                       #申請單種類
        "bu":                             request.json.get('bu'),                              #部門
        "project_no":                     request.json.get('project_no'),                      #專案代號
        "project_name":                   request.json.get('project_name'),               
        "product_no":                     request.json.get('product_no'),                      #產品型號
        "product_name":                   request.json.get('product_name'),                    #產品名稱
        "product_check":                  request.json.get('product-check'),                   #產品判定
        "product_series":                 request.json.get('product_series'),                  #產品系列
        "spec_describe":                  request.json.get('spec_describe'),                   #規格說明
        "product_certified":              request.json.get('product_certified'),               #認證
        "target_markting":                request.json.get('target_markting'),                 #目標市場
        "estimate_price":                 request.json.get('estimate_price'),                  #預估銷售價
        "estimate_pcs":                   request.json.get('estimate_pcs'),                    #預估銷數量
        "estimate_sale_performance_year": request.json.get('estimate_sale_performance_year'),  #預估年銷售業績
        "estimate_profit_margin":         request.json.get('estimate_profit_margin'),          #預估毛利率
        "replace_product_flag":           request.json.get('replace_product_flag'),            #是否有取代舊有產品
        "replace_product":                request.json.get('replace_product'),                 #取代的產品型號
        "compete_status":                 request.json.get('compete_status'),                  #競爭狀態
        "patent_evaluate":                request.json.get('patent_evaluate'),                 #專利評估
        "work_hour_ee":                   request.json.get('work_hour_ee'),                    #電子開發部工時
        "cost_ee":                        request.json.get('cost_ee'),                         #電子開發部開發成本
        "start_date_ee":                  request.json.get('start_date_ee'),                   #電子預計開始日期
        "end_date_ee":                    request.json.get('end_date_ee'),                     #電子預計結束日其
        "work_hour_me":                   request.json.get('work_hour_me'),                    #機構開發部工時
        "cost_me":                        request.json.get('cost_me'),                         #機構開發部開發成本
        "start_date_me":                  request.json.get('start_date_me'),                   #機構開發部預計開始日期
        "end_date_me":                    request.json.get('end_date_me'),                     #機構開發部預計結束日其
        "work_hour_sw":                   request.json.get('work_hour_sw'),                  #軟體開發部工時
        "cost_sw":                        request.json.get('cost_sw'),                       #軟體開發部開發成本
        "start_date_sw":                  request.json.get('start_date_sw'),                 #軟體開發部預計開始日期
        "end_date_sw":                    request.json.get('end_date_sw'),                   #軟體開發部預計結束日其
        "work_hour_ds":                   request.json.get('work_hour_ds'),                #設計驗證部工時
        "cost_ds":                        request.json.get('cost_ds'),                     #設計驗證部開發成本 
        "start_date_ds":                  request.json.get('start_date_ds'),               #設計驗證部預計開始日期
        "end_date_ds":                    request.json.get('end_date_ds'),                 #設計驗證部預計結束日其
        "develop_unit":                   request.json.get('develop_unit'),                    #開發單位
        "place_of_production":            request.json.get('place_of_production'),             #投產地
        "product_count_first":            request.json.get('product_count_first'),             #第一批試產數量
        "markting_evaluate":              request.json.get('markting_evaluate'),               #行銷單位評估
        "first_product_date":             request.json.get('first_product_date'),              #預計上市日期
        "member_cname":                   request.json.get('member_cname'),                    #申請人
        "member_list":                    request.json.get('member_list'),                      #指派清單       
        "apply_date":                     request.json.get('apply_date'),                      #申請日期
        "inserted_at":                    datetime.datetime.now(),
        "updated_at":                     datetime.datetime.now(),
        "enable":                         True
    }
    # print(param)
    # print("*************************")
    new_project_form_model = new_project_form(mongo.db)
    result = new_project_form_model.insert_new_project_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200

#PM填寫編輯修改新開案申請單
@blue_new_project_form.route("/api/v0/db/modify_new_project_form/", methods=['post'])
def insert_modify_new_project_form():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid":                           form_uuid,
        "new_tech_project_no":            request.json.get('new_tech_project_no'),             #關聯評估案代號
        "form_no":                        request.json.get('form_no'),                         #單號
        "project_type":                   'project',                   
        "form_type":                      request.json.get('form_type'),                       #申請單種類
        "bu":                             request.json.get('bu'),                              #部門
        "project_no":                     request.json.get('project_no'),                      #專案代號
        "project_name":                   request.json.get('project_name'),               
        "product_no":                     request.json.get('product_no'),                      #產品型號
        "product_name":                   request.json.get('product_name'),                    #產品名稱
        "product-check":                  request.json.get('product-check'),                   #產品判定
        "product_series":                 request.json.get('product_series'),                  #產品系列
        "spec_describe":                  request.json.get('spec_describe'),                   #規格說明
        "product_certified":              request.json.get('product_certified'),               #認證
        "target_markting":                request.json.get('target_markting'),                 #目標市場
        "estimate_price":                 request.json.get('estimate_price'),                  #預估銷售價
        "estimate_pcs":                   request.json.get('estimate_pcs'),                    #預估銷數量
        "estimate_sale_performance_year": request.json.get('estimate_sale_performance_year'),  #預估年銷售業績
        "estimate_profit_margin":         request.json.get('estimate_profit_margin'),          #預估毛利率
        "replace_product_flag":           request.json.get('replace_product_flag'),            #是否有取代舊有產品
        "replace_product":                request.json.get('replace_product'),                 #取代的產品型號
        "compete_status":                 request.json.get('compete_status'),                  #競爭狀態
        "patent_evaluate":                request.json.get('patent_evaluate'),                 #專利評估
        "work_hour_ee":                   request.json.get('work_hour_ee'),                    #電子開發部工時
        "cost_ee":                        request.json.get('cost_ee'),                         #電子開發部開發成本
        "start_date_ee":                  request.json.get('start_date_ee'),                   #電子預計開始日期
        "end_date_ee":                    request.json.get('end_date_ee'),                     #電子預計結束日其
        "work_hour_me":                   request.json.get('work_hour_me'),                    #機構開發部工時
        "cost_me":                        request.json.get('cost_me'),                         #機構開發部開發成本
        "start_date_me":                  request.json.get('start_date_me'),                   #機構開發部預計開始日期
        "end_date_me":                    request.json.get('end_date_me'),                     #機構開發部預計結束日其
        "work_hour_soft":                 request.json.get('work_hour_soft'),                  #軟體開發部工時
        "cost_soft":                      request.json.get('cost_soft'),                       #軟體開發部開發成本
        "start_date_soft":                request.json.get('start_date_soft'),                 #軟體開發部預計開始日期
        "end_date_soft":                  request.json.get('end_date_soft'),                   #軟體開發部預計結束日其
        "work_hour_verify":               request.json.get('work_hour_verify'),                #設計驗證部工時
        "cost_verify":                    request.json.get('cost_verify'),                     #設計驗證部開發成本 
        "start_date_verify":              request.json.get('start_date_verify'),               #設計驗證部預計開始日期
        "end_date_verify":                request.json.get('end_date_verify'),                 #設計驗證部預計結束日其
        "develop_unit":                   request.json.get('develop_unit'),                    #開發單位
        "place_of_production":            request.json.get('place_of_production'),             #投產地
        "product_count_first":            request.json.get('product_count_first'),             #第一批試產數量
        "markting_evaluate":              request.json.get('markting_evaluate'),               #行銷單位評估
        "first_product_date":             request.json.get('first_product_date'),              #預計上市日期
        "member_cname":                   request.json.get('member_cname'),                    #申請人
        "apply_date":                     request.json.get('apply_date'),                      #申請日期
        "inserted_at":                    datetime.datetime.now(),
        "updated_at":                     datetime.datetime.now(),
        "enable":                         True
    }

    modify_new_project_form_model = modify_new_project_form(mongo.db)
    result = modify_new_project_form_model.insert_modify_new_project_form(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200



@blue_new_project_form.route("/api/v0/db/new_project_form/", methods=['get'])
def get_new_technology_form():
   
    param = {
        "project_no": request.args.get('project_no')
    }
    new_project_form_model = new_project_form(mongo.db)
    result = new_project_form_model.get_new_project_form(param)
    strJson = { 'result': 'ok', 'code':'01001','msg': '' , 'data': result}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#新開案申請單簽核Log
@blue_new_project_form.route("/api/v0/db/new_project_form/log/", methods=['post'])
def insert_new_project_form_log():

    if request.json.get('uuid') == "" or request.json.get('uuid') is None:
        form_uuid = str(uuid.uuid4())
    else:
        form_uuid = request.json.get('uuid')

    param = { 
        "uuid"                           : form_uuid,
        "form_no"                        : request.json.get('form_no'),                         #單號
        "bu"                             : request.json.get('bu'),                              #部門
        "project_no"                     : request.json.get('project_no'),                      #專案代號
        "project_name"                   : request.json.get('project_name'),
        "product_no"                     : request.json.get('product_no'),                      #產品型號
        "product_name"                   : request.json.get('product_name'),                    #產品名稱 
        "role"                           : request.json.get('role'),                            #目前簽核的人員(pm 或 hw 主管) 
        "pm_approve_flag"                : request.json.get('pm_approve_flag'),                 #PM主管是否核准旗標
        "pm_back_reason"                 : request.json.get('pm_back_reason'),                  #PM主管退回原因
        "pm_back_memo"                   : request.json.get('pm_back_memo'),                    #PM主管退回說明
        "hw_approve_flag"                : request.json.get('hw_approve_flag'),                 #HW主管是否核准旗標
        "hw_back_reason"                 : request.json.get('hw_back_reason'),                 #HW主管退回原因
        "hw_back_memo"                   : request.json.get('hw_back_memo'),                    #HW主管退回說明 
        "member_cname"                   : request.json.get('member_cname'),                    #申請人
        "apply_date"                     : request.json.get('apply_date'),                      #申請日期
        "inserted_at"                    : datetime.datetime.now(),
        "updated_at"                     : datetime.datetime.now(),
        "enable"                         : True
    }

    new_project_form_log_model = new_project_form_log(mongo.db)
    result = new_project_form_log_model.insert_new_project_form_log(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg': '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200




#生成單據編號
@blue_new_project_form.route("/api/v0/db/new_project_form_no/", methods=['get'])
def generate_new_project_form_code():

        SerialNum = "IA" + "{}{:02d}{:02d}{:03d}".format((int(datetime.datetime.now().year) - 1911), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,99))
        return Response(json.dumps(SerialNum), mimetype='application/json'), 200




#生成專案代號
@blue_new_project_form.route("/api/v0/db/new_project_no/", methods=['get'])
def generate_new_project_no():

        SerialNum = "AA{}".format(ReturnCode(request.args.get('bu')) ) +"-R-IA" + "{}{:02d}{:02d}{:03d}".format((int(datetime.datetime.now().year) - 1911), datetime.datetime.now().month , datetime.datetime.now().day,random.randint(1,99))
        #result = get_form_sn(db)
        #print(result)
        return Response(json.dumps(SerialNum), mimetype='application/json'), 200



# 新開案申請單送出申請通知信(PM發信給PM主管)
@blue_new_project_form.route("/api/v0/send/new_project_form/", methods=['post'])
def send_require_email_by_project_no():


    logger.info("{} - {} - {}".format(request.remote_addr, request.user_agent, '新開案申請單送出申請通知信'))
    # 參數
    project_no          = request.json.get('project_no')
    product_no          = request.json.get('product_no')
    first_product_date  = request.json.get('first_product_date')    
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
    subject  =  '申請簽核通知-{}'.format(product_no)
    
    message  =  '<!DOCTYPE html>' + \
                '<html leng="en">' + \
                '<head><meta charset="utf-8"></head>' + \
                '<body>' + \
                '<h1>新產品開發申請表-請您簽核</h1>' + \
                '<ul>' + \
                '<li>專案代號: {}</li>'.format(project_no) + \
                '<li>產品型號: {}</li>'.format(product_no) + \
                '<li>產品預計上市日期: {}</li>'.format(first_product_date) + \
                '</ul><br/>' + \
                '<a href="http://{}/page/v0/new_project_approve/?project_no={}">新產品開案申請表​</a>'.format(DOMAIN_PATH, project_no) + \
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



#取得目前所有專案代號
@blue_new_project_form.route("/api/v0/db/all_new_project_no/", methods=['get'])
def get_all_new_project_no():
      
    new_project_form_model = new_project_form(mongo.db)
    result = new_project_form_model.get_all_new_project_no()
    strJson = { 'result': 'ok', 'code':'01001','msg': '' , 'data': result}
    return Response(json.dumps(strJson), mimetype='application/json'), 200



#取得目前所有產品型號
@blue_new_project_form.route("/api/v0/db/all_new_product_no/", methods=['get'])
def get_all_new_product_no():
      
    new_project_form_model = new_project_form(mongo.db)
    result = new_project_form_model.get_all_new_product_no()
    strJson = { 'result': 'ok', 'code':'01001','msg': '' , 'data': result}
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
    
#主管指派人員工作項目
@blue_new_project_form.route("/api/v0/db/new_project_form/update_memberlist/", methods=['post'])
def update_new_project_form_memberlist():
       
    
    param = { 
        "project_no":         request.json.get('project_no'),
        "member_list":        request.json.get('member_list'),
        
    }
   
    new_project_form_model = new_project_form(mongo.db)
    result = new_project_form_model.update_new_project_form_memberlist(param)
    strJson = { 'result': 'ok', 'code':'01001', 'msg' : '' , 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200
    


    
