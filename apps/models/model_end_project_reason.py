from apps.exts import mongo
import datetime
import json



class end_project_reason:
    def __init__(self, db):
        self.collection = db['end_project_reason']



    def insert_end_project_reason(self, user_data):
        print(user_data)
        try:

            obj = self.collection.find_one({"index": user_data['index']})
            if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: end_project_reason Document'
            else:
                oriquery = {"Index": user_data['index'] }
                newvalues = { "$set": { "reason":user_data['reason'],"enable" : True,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: end_project_reason Document'

        except Exception as e:
            return '一筆資料無法建立於: end_project_reason Document, 錯誤:{}'.format(str(e))



    def get_end_project_reason(self):
       
        try:
            dataRes = []
            objs = self.collection.find({"enable": True},{"_id" : 0, "reason" : 1})
            for item in objs :
                #print(item)
                dataRes = item
            return json.dumps(dataRes)

        except Exception as e:
            return 'end_project_reason 資料無法取得, 錯誤:{}'.format(str(e))



    def delete_end_project_reason(self, user_data):
        print(user_data)
        try:

            obj = self.collection.find_one({"Index": user_data['Index']})
            if obj != None:
                oriquery = {"index": user_data['index'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: end_project_reason Document'

        except Exception as e:
            return '一筆資料無法刪除於: end_project_reason Document, 錯誤:{}'.format(str(e))


