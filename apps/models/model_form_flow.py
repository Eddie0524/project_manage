from apps.exts import mongo
import datetime
import json



class form_flow:
    def __init__(self, db):
        self.collection = db['form_flow']



    def insert_form_flow(self, user_data):
        print(user_data)
        try:
            #print(user_data['form_code'])
            #obj = self.collection.find_one({"form_no": user_data['form_no'], "fs_code" : user_data['fs_code'], "user" : user_data['fs_code'] })
            #if obj == None:
            self.collection.insert_one(user_data)
            return 'ok','一筆資料已成功建立於: form_flow Document'
            # else:
            #     oriquery = {"project_no": user_data['project_no'] , "type" : user_data['type']  }
            #     newvalues = { "$set": {                   
            #         "sign_flow"             : user_data['sign_flow'],          
            #         "updated_at"            : datetime.datetime.now()} 
            #     }
            #     res = self.collection.update_one(oriquery,newvalues)
            #return 'ok','已存在相同紀錄於: form_flow Document'

        except Exception as e:
            return 'fail','一筆資料無法建立於: form_sign_flow Document, 錯誤:{}'.format(str(e))



    def get_form_flow(self, user_data):
        print(user_data)
        try:
            list = []
            obj = self.collection.find({"form_no": user_data['form_no']},{"_id": 0,"updated_at" : 0, "enable" : 0}).sort("inserted_at",-1)
            for item in obj:
                tmp_str  = str(item['inserted_at'])
                split_str = tmp_str.split('.')
                item['inserted_at'] = split_str[0]
                list.append(item)
            print(list)

            if (len(list) != 0):
                return 'ok',list
            else:            
                return 'ok',list

        except Exception as e:
            return 'fail','查無資料於: form_flow Document, 錯誤:{}'.format(str(e))