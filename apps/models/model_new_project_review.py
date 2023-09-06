from apps.exts import mongo
import datetime
import json
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby   #itertool还包含有其他很多函数，比如将多个list联合起来



class new_project_review:
    
    def __init__(self, db):
        self.collection = db['new_project_review']
        
        
    def insert_new_project_review(self, user_data):
        try:

            obj = self.collection.find_one({ "project_no" : user_data['project_no'], "enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            
            if obj == None :
                self.collection.insert_one(user_data)
            
            else:
                oriquery = {"project_no": user_data['project_no'] }
                newvalues = { "$set": {                   
                    "status"                    : user_data['status'],            #審核狀態
                    "back_reason"               : user_data['back_reason'],       #退回原因
                    "back_memo"                 : user_data['back_memo'],         #退回原因
                    "updated_at": datetime.datetime.now()} 
                }
                res = self.collection.update_one(oriquery,newvalues)

          
            return obj

        except Exception as e:
            return 'new_project_review 資料無法取得, 錯誤:{}'.format(str(e))