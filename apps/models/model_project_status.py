from apps.exts import mongo
import datetime
import json


class ProjectStatus:
    def __init__(self, db):
        self.collection = db['project_status']



    def insert_project_status(self, user_data):
        print(user_data)
        #print("==================")
        try:

            obj = self.collection.find_one({"index": user_data['index']})
            if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: project_status Document'
            else:
                oriquery = {"index": user_data['index'] }
                newvalues = { "$set": { "status":user_data['status'],"enable" : True,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: project_status Document'

        except Exception as e:
            return '一筆資料無法建立於: project_status Document, 錯誤:{}'.format(str(e))



    def get_project_status(self):
       
        try:    
            dataRes = []
            objs = self.collection.find({"enable": True},{"_id" : 0, "status" : 1})
            

            for item in objs :
                #print(item)
                dataRes = item

            return json.dumps(dataRes)

        except Exception as e:
            return 'project_status 資料無法取得, 錯誤:{}'.format(str(e))



    def delete_project_status(self, user_data):
        print(user_data)
        try:    
            obj = self.collection.find_one({"index": user_data['index']})

            if obj != None:

                oriquery = {"index": user_data['index'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: project_status Document'
            
        except Exception as e:
            return '一筆資料無法刪除於: project_status Document, 錯誤:{}'.format(str(e))




