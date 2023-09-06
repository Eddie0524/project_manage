from apps.exts import mongo
import datetime
import json


class milestone:
    def __init__(self, db):
        self.collection = db['milestone']


    def insert_milestone(self, pam_data):
        try:
            obj = self.collection.find_one({"uuid": pam_data['uuid']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: milestone Document'
            else:
                oriquery = {"uuid": pam_data['uuid']}
                newvalues = { "$set": {
                    "milestone_code"  : pam_data['milestone_code'],
                    "milestone_cname" : pam_data['milestone_cname'],
                    "milestone_ename" : pam_data['milestone_ename'],
                    "enable" : True,
                    "updated_at": datetime.datetime.now()
                    }
                }
            res = self.collection.update_one(oriquery,newvalues)
            return '一筆資料已成功更新於: milestone Document'

        except Exception as e:
            return '一筆資料無法建立於: milestone Document, 錯誤:{}'.format(str(e))


    # 取所有Milestone 資料
    def read_milestone_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'Milestone 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'Milestone 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []
        
        
    # 修改一筆Milestone資料
    def update_one_milestone(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "milestone_code"  : pam['milestone_code'],
                "milestone_cname" : pam['milestone_cname'],
                "milestone_ename" : pam['milestone_ename'],
                "enable"          : pam['enable'],
                "memo"            : pam['memo'],
                "updated_at"      : datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆Milestone資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆Milestone資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 刪除一筆Status資料
    def delete_milestone_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆Milestone資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆Milestone資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg