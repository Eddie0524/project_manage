from apps.exts import mongo
import datetime
import json
from operator import itemgetter
from itertools import groupby


class feedback_rule:
    def __init__(self, db):
        self.collection = db['feedback_rule']



    def insert_feedback_rule(self, pam):
        print(pam)
        try:
            obj = self.collection.find_one({"uuid": pam['uuid']})

            if obj == None:
                res = self.collection.insert_one(pam)
                return '一筆資料已成功建立於: feedback_rule Document'
            else:
                oriquery  = {"uuid": pam['uuid']}
                newvalues = { "$set": {
                    "rule_code":        pam['rule_code'],
                    "rule_cname":       pam['rule_cname'],
                    "rule_ename":       pam['rule_ename'],
                    "rule_type":        pam['rule_type'],
                    "form_type":        pam['form_type'],
                    "rule_situation":   pam['rule_situation'],
                    "rule_description": pam['rule_description'],
                    "task_uuid":        pam['task_uuid'],
                    "task_code":        pam['task_code'],
                    "task_cname":       pam['task_cname'],
                    "task_ename":       pam['task_ename'],
                    "task_index":       pam['task_index'],
                    "milestone_uuid":   pam['task_uuid'],
                    "milestone_code":   pam['milestone_code'],
                    "milestone_cname":  pam['milestone_cname'],
                    "milestone_ename":  pam['milestone_ename'],
                    "milestone_index":  pam['milestone_index'],
                    "status_uuid":      pam['status_uuid'],
                    "status_code":      pam['status_code'],
                    "status_cname":     pam['status_cname'],
                    "status_ename":     pam['status_ename'],
                    "status_index":     pam['status_index'],
                    "attach_list":      pam['attach_list'],
                    "event_node":       pam['event_node'],
                    "status":           pam['status'],
                    "enable":           True,
                    "updated_at":       datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: feedback_rule Document'

        except Exception as e:
            return '一筆資料無法建立於: feedback_rule Document, 錯誤:{}'.format(str(e))



    # 取所有 feedback_rule 資料
    def read_feedback_rule_all(self):
        try:
            objs = self.collection.find()
            result = []
            for item in objs:
                #print(item)
                item['_id'        ] = str(item['_id'])
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at' ] = str(item['updated_at'])
                result.append(item)
            strMsg = 'feedback_rule 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'feedback_rule 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []
        
     # 取指定form_type 及 rule_type 的 feedback_rule 資料
    def read_feedback_rule_by_form_type(self,pam):
        try:
            
        
            objs = self.collection.find({"form_type" : pam['form_type'] ,"rule_type" : str.upper(pam['rule_type'])},{"_id" : 0, "inserted_at" : 0 , "updated_at" : 0} )
            result = []

             

            for item in objs:


                dictObj = {
                    "task_uuid"       : item['task_uuid'],
                    "task"            : item['task_cname'],                    
                    "milestone"       : item['milestone_cname'],
                    "status"          : item['status_cname'],
                }  
                             
                result.append(dictObj)
               
            print(result)

            
           
        

            
            strMsg = 'feedback_rule 資料查詢成功'
            return 'ok', strMsg, result
        except Exception as e:
            strMsg = 'feedback_rule 資料查詢失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg, []
        
        
        
    # 修改一筆 feedback_rule 資料
    def update_one_feedback_rule(self, pam):
        #print("-------修改-------")
        #print(pam)
        try:
            db_query = { "uuid": pam['uuid'] }
            new_values = { "$set":{ 
                "rule_code":        pam['rule_code'],
                "rule_cname":       pam['rule_cname'],
                "rule_ename":       pam['rule_ename'],
                "rule_type":        pam['rule_type'],
                "form_type":        pam['form_type'],
                "rule_situation":   pam['rule_situation'],
                "rule_description": pam['rule_description'],
                "task_uuid":        pam['task_uuid'],
                "task_code":        pam['task_code'],
                "task_cname":       pam['task_cname'],
                "task_ename":       pam['task_ename'],
                "task_index":       pam['task_index'],
                "milestone_uuid":   pam['task_uuid'],
                "milestone_code":   pam['milestone_code'],
                "milestone_cname":  pam['milestone_cname'],
                "milestone_ename":  pam['milestone_ename'],
                "milestone_index":  pam['milestone_index'],
                "status_uuid":      pam['status_uuid'],
                "status_code":      pam['status_code'],
                "status_cname":     pam['status_cname'],
                "status_ename":     pam['status_ename'],
                "status_index":     pam['status_index'],
                "attach_list":      pam['attach_list'],
                "event_node":       pam['event_node'],
                "enable":           pam['enable'],
                "memo":             pam['memo'],
                "updated_at": datetime.datetime.now()
            }}
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆 feedback_rule 資料已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 feedback_rule 資料更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg


    # 刪除一筆Status資料
    def delete_feedback_rule_by_uuid(self, pam_uuid):
        try:
            db_query = { "uuid": pam_uuid }
            self.collection.delete_one(db_query)
            strMsg = '一筆 feedback_rule 資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆 feedback_rule 資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg