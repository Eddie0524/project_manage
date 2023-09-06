from apps.exts import mongo
import datetime
import json



class task:
    def __init__(self, db):
        self.collection = db['task']


    def insert_task(self, pam_data):
        try:
            obj = self.collection.find_one({"uuid": pam_data['uuid']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: task Document'
            else:
                oriquery = {"uuid": pam_data['uuid']}
                newvalues = { "$set": {
                    "task_code"  : pam_data['task_code'],
                    "task_cname" : pam_data['task_cname'],
                    "task_ename" : pam_data['task_ename'],
                    "enable" : True,
                    "updated_at": datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: task Document'

        except Exception as e:
            return '一筆資料無法建立於: task Document, 錯誤:{}'.format(str(e))
        
        
        
    # 取所有Task 資料
    def read_task_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'Task 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'Task 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []
        
        
     # 修改一筆Task資料
    def update_one_task(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "task_code"  : pam['task_code'],
                "task_cname" : pam['task_cname'],
                "task_ename" : pam['task_ename'],
                "enable"       : pam['enable'],
                "memo"         : pam['memo'],
                "updated_at"   : datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆Task資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆Task資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 刪除一筆Task資料
    def delete_task_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆Task資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆Task資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg