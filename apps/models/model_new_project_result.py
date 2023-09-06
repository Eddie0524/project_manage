from apps.exts import mongo
import datetime
import json
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby   #itertool还包含有其他很多函数，比如将多个list联合起来



class new_project_result:
    
    def __init__(self, db):
        self.collection = db['new_project_result']
        
        
    def get_new_project_form(self, user_data):
        try:
            obj = self.collection.find_one(
                { "project_no" : user_data['project_no'], "enable" : True},
                {"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = []
            print(obj)
            # for item in obj :
            #     print(item)
            #     dataRes.append(item)
            return obj

        except Exception as e:
            return 'new_project_form 資料無法取得, 錯誤:{}'.format(str(e))