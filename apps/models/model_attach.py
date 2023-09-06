from apps.exts import mongo
import datetime
import json


class Attach:
    def __init__(self, db):
        self.collection = db['attach']


    def insert_attach(self, pam_data):
        try:
            obj = self.collection.find_one({"uuid": pam_data['uuid']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: attach Document'
            else:
                oriquery = {"uuid": pam_data['uuid']}
                newvalues = { "$set": {
                    "attach_code"  : pam_data['attach_code'],
                    "attach_cname" : pam_data['attach_cname'],
                    "attach_ename" : pam_data['attach_ename'],
                    "attach_link"  : pam_data['attach_link'],
                    "attach_file"  : pam_data['attach_file'],
                    "enable" : True,
                    "updated_at": datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: attach Document'

        except Exception as e:
            return '一筆資料無法建立於: attach Document, 錯誤:{}'.format(str(e))
        
        
        
    # 取所有 Attach 資料
    def read_attach_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'Attach 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'Attach 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []
        
        
     # 修改一筆 Attach 資料
    def update_one_attach(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "attach_code":  pam['attach_code'],
                "attach_cname": pam['attach_cname'],
                "attach_ename": pam['attach_ename'],
                "attach_link":  pam['attach_link'],
                "attach_file":  pam['attach_file'],
                "enable":       pam['enable'],
                "memo":         pam['memo'],
                "updated_at":   datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆 Attach 資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 Attach 資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 刪除一筆Attach資料
    def delete_attach_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆Attach資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆Attach資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg