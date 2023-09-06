from apps.exts import mongo
import datetime
import json
import pymongo

# 關於流程關卡的定義
class Flow_Step:
    def __init__(self, db):
        self.collection = db['flow_step']
        
        
    # 建立一筆 flow_step 資料
    def create_flow_step(self, pam_data):
        try:
            obj = self.collection.find_one({"uuid": pam_data['uuid']})
            #print(obj)
            if obj is None:
                self.collection.insert_one(pam_data)
            else:
                db_query = {"uuid": pam_data['uuid'] }
                new_values = { "$set": {
                    "code":           pam_data['code'],
                    "cname":          pam_data['cname'],
                    "ename":          pam_data['ename'],
                    "index":          pam_data['index'],           # 關卡順序
                    "user":           pam_data['user'],            # 跟此關卡有關人員
                    "action":         pam_data['action'],          # application / approval / assign
                    "group":          pam_data['group'],           # 群組名稱(評估一般)           
                    "classification": pam_data['classification'],  # new_technology / new_project / layout / pcb
                    "updated_at":     datetime.datetime.now()
                    }
                }
                self.collection.update_one(db_query, new_values)
            strMsg = '一筆 flow_step 資料已成功建立'
            return 'ok', strMsg
                
        except Exception as e:
            strMsg = '一筆 flow_step 資料建立失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg
        
        
    # 取所有 flow_step 資料
    def read_flow_step_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'flow_step 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'flow_step 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []


    # 取得一筆 flow_step資料(依code)
    def find_one_by_code(self, pam):
        try:
            obj = self.collection.find_one({"code":pam}, {"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            if obj != None: 
               return obj
            else:
                return {}
        except Exception as e:
            return {}
        

    # 查詢 flow_step 資料(依據classification)
    def find_by_classification(self, pam_class):
        try:

            db_query = {'classification':pam_class }
            objs = self.collection.find(db_query)
            #flow_step = cursor.next()
            
            result = []
            if objs != None:
                print(objs)
                for item in objs:
                    print(item)
                    item['_id'        ] = str(item['_id'])
                    item['inserted_at'] = str(item['inserted_at'])
                    item['updated_at' ] = str(item['updated_at'])
                    result.append(item)
            return result

        except Exception as e:
            return 'flow_step 資料無法取得, 錯誤:{}'.format(str(e))


    # 修改一筆 flow_step 資料
    def update_one_flow_step(self, pam):
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "code":           pam['code'],
                "cname":          pam['cname'],
                "ename":          pam['ename'],
                "index":          pam['index'],
                "user":           pam['user'],
                "action":         pam['action'],
                "group":          pam['group'],
                "classification": pam['classification'],
                "updated_at":     datetime.datetime.now()
                }
            }
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆 flow_step 資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 flow_step 資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 取得某流程關卡總數(總共幾關)
    def find_step_count_by_group(self, pam_class, pam_group):
        try:
            db_query = {'classification':pam_class, 'group': pam_group }
            objs = self.collection.find(db_query)
            result = []
            if objs != None:
                print(objs)
                for item in objs:
                    print(item)
                    item['_id'        ] = str(item['_id'])
                    item['inserted_at'] = str(item['inserted_at'])
                    item['updated_at' ] = str(item['updated_at'])
                    result.append(item)
            return len(result)
        
        except Exception as e:
            return 0


    # 刪除一筆 flow_step 資料
    def delete_flow_step_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆 flow_step 資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 flow_step 資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg
