from apps.exts import mongo
import datetime
import json




class all_kinds_reason:
    def __init__(self, db):
        self.collection = db['all_kinds_reason']
        
    # 建立一筆原因資料
    def create_one_reason(self, pam_data):
        #print(pam_data)
        try:
            obj = self.collection.find_one({"uuid": pam_data['uuid']})
            #print(obj)
            if obj is None:
                self.collection.insert_one(pam_data)
            else:
                db_query = {"reason": pam_data['reason'], "type": pam_data['type'] }
                new_values = { "$set": {
                    "uuid":       pam_data['uuid'],
                    "reason":     pam_data['reason'],
                    "type":       pam_data['type'],    # reject / pending / other
                    "form_type":  pam_data['form_type'],
                    "mode":       pam_data['mode'],    # new_technology / new_project / layout  / pcb
                    "enable":     pam_data['enable'],
                    "memo":       pam_data['memo'],
                    "updated_at": datetime.datetime.now()
                }}
                self.collection.update_one(db_query, new_values)
            strMsg = '一筆原因資料已成功建立'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆原因資料建立失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # 取得所有原因資料
    def read_all_kinds_reason(self):
        try:
            #objs = self.collection.find({"_id" : 0, "reason" : 1})
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            
            strMsg = '原因資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = '原因資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []



    # 修改一筆原因資料
    def update_one_reason(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "reason":     pam['reason'],
                "type":       pam['type'],
                "form_type":  pam['form_type'],
                "mode":       pam['mode'],
                "enable":     pam['enable'],
                "memo":       pam['memo'],
                "updated_at": datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆原因資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆原因資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # 刪除一筆原因資料
    def delete_reason_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆原因資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆原因資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg