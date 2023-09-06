from apps.exts import mongo
import datetime
import json



class layout_result:
    def __init__(self, db):
        self.collection = db['layout_result']



    def insert_layout_result(self, user_data):
        print(user_data)
        try:
            #print(user_data['form_code'])
            obj = self.collection.find_one({"project_no": user_data['project_no']})
            if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: layout_result Document'
            else:
                oriquery = {"project_no": user_data['project_no'] }
                newvalues = { "$set": {
                    "hw_approve_flag"       : user_data['hw_approve_flag'],        #主管簽核
                    "hw_back_reason"        : user_data['hw_back_reason'],         #主管退回原因
                    "hw_back_memo"          : user_data['hw_back_memo'],           #主管退回說明                    
                    "updated_at"          : datetime.datetime.now()} 
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: layout_result Document'

        except Exception as e:
            return '一筆資料無法建立於: layout_form Document, 錯誤:{}'.format(str(e))



    def get_layout_result(self, user_data):
        try:
            obj = self.collection.find_one({"project_no": user_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = [] 
            print(obj)
            return obj 

        except Exception as e:
            return 'new_layout_result 資料無法取得, 錯誤:{}'.format(str(e))



   
        


