from apps.exts import mongo
import datetime
import json



class task_milestone:
    def __init__(self, db):
        self.collection = db['task_milestone']


    def insert_task_milestone(self, user_data):
        print(user_data)
        try:
            # obj = self.collection.find_one({"index": user_data['index'],"type": user_data['type']})

            # if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: task_milestone Document'
            # else:
            #     oriquery = {"index": user_data['index'],"type": user_data['type']} 
            #     newvalues = { "$set": { "task":user_data['task'],"milestone" : user_data['milestone'],"enable" : True,"updated_at": datetime.datetime.now()} }            
            #     res = self.collection.update_one(oriquery,newvalues)
            #     return '一筆資料已成功更新於: task_milestone Document'

        except Exception as e:
            return '一筆資料無法建立於: task_milestone Document, 錯誤:{}'.format(str(e))



    def get_task_milestone(self,user_data):
       
        try:
            dataRes = []
            objs = self.collection.find({"type" : user_data['type'],"form_type" : user_data['form_type'],"enable": True},{"_id" : 0, "uuid" : 0 ,"inserted_at" : 0,"updated_at" : 0 , "enable" : 0 }).sort("index")
            #objs = self.collection.find({"enable": True},{"_id" : 0, "uuid" : 0 ,"inserted_at" : 0,"updated_at" : 0 , "enable" : 0 }).sort("index")
            for item in objs :
                print("*****")
                print(item)
                dataRes.append(item)

            return dataRes

        except Exception as e:
            return 'task_milestone 資料無法取得, 錯誤:{}'.format(str(e))



    def get_task_milestone_by_type(self, user_data):
        try:
            print(user_data)
            dataRes = []
            objs = self.collection.find({'type': user_data['type'] })
            #objs = self.collection.find({"enable": True})
            for item in objs :
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                dataRes.append(item)
            return dataRes

        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    def delete_task_milestone_by_type(self, user_data):
        try:
            filter = {'type': user_data}
            result = self.collection.delete_many(filter)
            print(result)
            return '資料已成功刪除於: task_milestone Document'
        
        except Exception as e:
            return '資料無法刪除於: task_milestone Document, 錯誤:{}'.format(str(e))


    def delete_task_milestone(self, user_data):
        print(user_data)
        try:    
            obj = self.collection.find_one({"index": user_data['index']})
            if obj != None:  
                oriquery = {"index": user_data['index'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: task_milestone Document  '

        except Exception as e:
            return '一筆資料無法刪除於: task_milestone Document, 錯誤:{}'.format(str(e))




    def update_milestone_of_task(self, pam_type, pam_task, pam_milestone ):
        #print(pam_type)
        #print(pam_task)
        #print(pam_milestone)
        try:
            db_query   = { "task" : pam_task, "type": pam_type }
            #print(db_query)
            new_values = { "$set": { "milestone": pam_milestone } }
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆task-milestone資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆task-milestone資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


class task_milestone_reason:
    def __init__(self, db):
        self.collection = db['task_milestone_reason']


    def insert_task_milestone_reason(self, user_data):
        print(user_data)
        try:
            # obj = self.collection.find_one({"index": user_data['index'],"type": user_data['type']})

            # if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: task_milestone_reason Document'
            # else:
            #     oriquery = {"index": user_data['index'],"type": user_data['type']} 
            #     newvalues = { "$set": { "task":user_data['task'],"milestone" : user_data['milestone'],"enable" : True,"updated_at": datetime.datetime.now()} }            
            #     res = self.collection.update_one(oriquery,newvalues)
            #     return '一筆資料已成功更新於: task_milestone Document'

        except Exception as e:
            return '一筆資料無法建立於: task_milestone_reason Document, 錯誤:{}'.format(str(e))
        


    def get_task_milestone_reason(self,user_data):
       
        try:
            dataRes = []
            objs = self.collection.find({"type" : user_data['type'],"form_type" : user_data['form_type'],"enable": True},{"_id" : 0, "uuid" : 0 ,"inserted_at" : 0,"updated_at" : 0 , "enable" : 0 }).sort("index")
            #objs = self.collection.find({"enable": True},{"_id" : 0, "uuid" : 0 ,"inserted_at" : 0,"updated_at" : 0 , "enable" : 0 }).sort("index")
            for item in objs :
                print("*****")
                print(item)
                dataRes.append(item)

            return dataRes

        except Exception as e:
            return 'task_milestone_reason 資料無法取得, 錯誤:{}'.format(str(e))
