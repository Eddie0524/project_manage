from apps.exts import mongo
import datetime
import json


### 紀錄流水號
class serial_number:
    def __init__(self, db):
        self.collection = db['serial_number']


    # 建立一筆流水號(依據模式類型)
    def insert_serial_number(self, pam):
        print(pam)
        try:
            obj = self.collection.find_one({"mode": pam['mode']})
            if obj == None:
                res = self.collection.insert_one(pam)
                return '一筆 serial_number 資料已成功建立於: serial_number Document'
            else:
                oriquery  = {"mode": pam['mode']}
                newvalues = { "$set": {
                    "sn"         : pam['sn'],
                    "mode"       : pam['mode'],
                    "pre_text"   : pam['pre_text'],
                    "memo"       : pam['memo'],
                    "updated_at" : datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery, newvalues)
                return '一筆 serial_number 資料已成功建立於: serial_number Document'

        except Exception as e:
            return '一筆 serial_number 資料無法建立於: serial_number Document, 錯誤:{}'.format(str(e))



    # 取得一筆流水號資料
    def get_one_serial_number(self, pam):

        try:
            obj= self.collection.find_one({"mode": pam['mode']})
            return json.dumps(obj)

        except Exception as e:
            return 'form_sn 資料無法取得, 錯誤:{}'.format(str(e))



    # 修改一筆流水號資料
    def update_one_serial_number(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "mode": pam['mode'] }
            new_values = { "$set":{ 
                "sn"         : pam['sn'],
                "mode"       : pam['mode'],
                "pre_text"   : pam['pre_text'],
                "memo"       : pam['memo'],
                "updated_at" : datetime.datetime.now()
                }
            }
            res = self.collection.update_one(db_query, new_values)
            return '一筆 serial_number 資料已成功更新於: serial_number Document'
        except Exception as e:
            return '一筆 serial_number 資料無法更新於: serial_number Document, 錯誤:{}'.format(str(e))