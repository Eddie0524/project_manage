from apps.exts import mongo
import datetime
import json



class form_sn:
    def __init__(self, db):
        self.collection = db['form_sn']



    def insert_form_sn(self, user_data):
        print(user_data)
        try:

            obj = self.collection.find_one()
            print(obj)
            if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: form_sn Document'
            else:
                oriquery = {}
                newvalues = { "$set": { "sn":user_data['sn'], "enable" : True, "updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: form_sn Document'

        except Exception as e:
            return '一筆資料無法建立於: form_sn Document, 錯誤:{}'.format(str(e))



    def get_form_sn(self):

        try:
            dataRes = ""
            objs = self.collection.find({"enable": True},{"_id" : 0, "sn" : 1})
            for item in objs :
                #print(item)
                dataRes = item
            return json.dumps(dataRes)

        except Exception as e:
            return 'form_sn 資料無法取得, 錯誤:{}'.format(str(e))



    def delete_form_sn(self):

        try:

            obj = self.collection.find_one()
            print(obj)
            if obj != None:
                oriquery = {}
                newvalues = { "$set": {  "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(obj,newvalues)
                return '一筆資料已成功刪除於: form_sn Document'

        except Exception as e:
            return '一筆資料無法刪除於: form_sn Document, 錯誤:{}'.format(str(e))


