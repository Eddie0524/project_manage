from apps.exts import mongo
import json
from bson import ObjectId
from apps.settings import DOMAIN_PATH
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


class EMail:
    def __init__(self, db):
        self.collection = db['email']


    def insert_email(self, pam):
        print(pam)
        try:
            obj = self.collection.find_one({"uuid": pam['uuid']})

            if obj == None:
                res = self.collection.insert_one(pam)
                return '一筆資料已成功建立於: email Document'
            else:
                oriquery  = {"uuid": pam['uuid']}
                newvalues = { "$set": {
                    "code"       : pam['code'],
                    "cname"      : pam['cname'],
                    "ename"      : pam['ename'],
                    "type"       : pam['type'],       # 通知/提醒
                    "main_title" : pam['main_title'], # 主標題
                    "sub_title"  : pam['sub_title'],  # 副標題
                    "sender"     : pam['sender'],     # 發信人
                    "receiver"   : pam['receiver'],   # 收件人(list)
                    "cc"         : pam['cc'],         # 副本收件人(list)
                    "label"      : pam['label'],      # 內文標題
                    "content"    : pam['content'],    # 內文內容 <html 格式>
                    "param_list" : pam['param_list'], # 參數定義(json list)
                    "page_link"  : pam['page_link'],  # 頁面連結
                    "file_link"  : pam['file_link'],  # 檔案連結
                    "enable"     : True,
                    "memo"       : pam['memo'],
                    "updated_at" : datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: email Document'

        except Exception as e:
            return '一筆資料無法建立於: email Document, 錯誤:{}'.format(str(e))
        


    # 取所有 email 資料
    def read_email_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'email 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'email 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []


    # 修改一筆 email 資料
    def update_one_email(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "code"        : pam['code'],
                "cname"       : pam['cname'],
                "ename"       : pam['ename'],
                "type"        : pam['type'],
                "main_title"  : pam['main_title'],
                "sub_title"   : pam['sub_title'],
                "sender"      : pam['sender'],
                "receiver"    : pam['receiver'],
                "cc"          : pam['cc'],
                "label"       : pam['label'],
                "content"     : pam['content'],
                "param_list"  : pam['param_list'],
                "page_link"   : pam['page_link'],
                "file_link"   : pam['file_link'],
                "enable"      : pam['enable'],
                "memo"        : pam['memo'],
                "updated_at"  : datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆 feedback_rule 資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 feedback_rule 資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 刪除一筆 email 資料
    def delete_email_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆 email 資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 email 資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # def send_new_technology_msg(self, pam_no, pam_name, pam_sender):
    #     #project_no   = request.json.get('project_no')
    #     #project_name = request.json.get('project_name')
     
    #     # SMTP服务器的配置
    #     smtp_server = '220.130.3.61'
    #     smtp_port = 25
    #     smtp_username = 'marktord'
    #     smtp_password = '6d64iryqx5'
    
    #     sender = pam_sender #'Max.Liu@Sunix.com'
    #     receiver = 'Eddie.Hsieh@sunix.com, lumark@sunix.com, Max.Liu@Sunix.com'
    #     subject = '{}-新產品技術評估申請通知'.format(pam_name)
    #     #message = '申請案名:{}\n申請案號:{} \n新產品技術評估申請通知\n請收到通知點擊下方連結進行回報作業:\nhtttp://{}/page/v0/new_technology_feedback/'.format(project_name, project_no, DOMAIN_PATH)
    #     message = '<p>申請案名:{}</p><br/>' + '<p>申請案號:{}</p><br/><p>新產品技術評估申請通知</p><br/><p>請收到通知點擊下方連結進行回報作業:</p><br/><a href="http://{}/page/v0/new_technology_feedback/">回報作業</a>'.format(pam_name, pam_no, DOMAIN_PATH)

    #     msg = MIMEMultipart()
    #     msg['From'] = sender
    #     msg['To'] = receiver
    #     msg['Subject'] = subject
    #     msg["Cc"] = "lumark@sunix.com"
    
    #     #msg.attach(MIMEText(message, 'plain', 'utf-8'))
    #     msg.attach(MIMEText(message, 'html', 'utf-8'))

    #     strJson = {}
    #     try:
    #         to_addr = ["Eddie.Hsieh@sunix.com", "lumark@sunix.com","Max.Liu@Sunix.com"]
    #         smtp_obj = smtplib.SMTP(smtp_server, smtp_port)
    #         #smtp_obj.starttls()  # 使用TLS加密
    #         smtp_obj.login(smtp_username, smtp_password)  
    #         smtp_obj.sendmail(sender, to_addr, msg.as_string())
    #         print('郵件發送成功')
    #         strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': '郵件發送成功' }}
    #         smtp_obj.quit()
    #     except smtplib.SMTPException as e:
    #         strJson = { 'result': 'fail', 'code':'', 'data': { 'msg': '郵件發送失败' }}
    #         print('郵件發送失败:', str(e))
            
    #     return strJson