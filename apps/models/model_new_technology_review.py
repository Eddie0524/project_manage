from apps.exts import mongo
import datetime
import json
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby   #itertool还包含有其他很多函数，比如将多个list联合起来
import pymongo
from pymongo.collection import ReturnDocument

class new_technology_review:

    def __init__(self, db):
        self.collection = db['new_technology_review']


    def insert_new_technology_review(self, user_data):
        #print(user_data)
        try:
            print(user_data)
            obj = self.collection.find_one({"project_no": user_data['project_no']})

            if obj == None:
                res = self.collection.insert_one(user_data)
                return '一筆資料已成功建立於: new_technology_review Document'
            else:
                oriquery = {"project_no": user_data['project_no']}               
               
                newvalues = { "$set": {
                        "member_list"           : user_data['member_list'],
                        "hw_apporve_flag"       : user_data['hw_apporve_flag'],
                        "hw_reason"             : user_data['hw_reason'],
                        "hw_memo"               : user_data['hw_memo'],
                        "project_status"        : user_data['project_status'],
                        "pm_reason"             : user_data['pm_reason'],
                        "pm_memo"               : user_data['pm_memo'],
                        "pm_expected_date"      : user_data['pm_expected_date'],
                        "updated_at"            : datetime.datetime.now()}
                    }

                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: new_technology_review Document'
            
        except Exception as e:
            return '一筆資料無法建立於: new_technology_review Document, 錯誤:{}'.format(str(e))



    def get_new_technology_review(self, user_data):
        try:
            print(user_data['project_no'])

            obj = self.collection.find_one(
                {"project_no" : user_data['project_no'], "enable" : True},
                {"_id" : 0, "inserted_at" : 0, "updated_at" : 0})
            
            if obj != None:           
                return obj
            else:
                return []

        except Exception as e:
            return 'new_technology_review 資料無法取得, 錯誤:{}'.format(str(e))



    def delete_new_technology_form_review(self, user_data):
        print(user_data)
        try:

            obj = self.collection.find_one({"uuid": user_data['uuid']})
            if obj != None:
                oriquery = {"uuid": user_data['uuid'] }
                newvalues = { "$set" : { "enable" : False,"updated_at" : datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: new_technology_form_task Document'

        except Exception as e:
            return '一筆資料無法刪除於: new_technology_form_task Document, 錯誤:{}'.format(str(e))



    def get_new_technology_forms_by_member(self, member_name):
        try:
            objs = self.collection.find({"member_cname" : member_name, "enable" : True}, {"_id" : 0}).sort("inserted_at",-1)
            result  = []
            reslist = []
            keylist = []
            for item in objs:
                print(item)
                dataObj = {}
                dataObj['uuid']                 = item['uuid']
                dataObj['form_no']              = item['form_no']
                dataObj['project_name']         = item['project_name']
                dataObj['member_cname']         = item['member_cname']
                dataObj['expected_start_date']  = item['expected_start_date']
                dataObj['expected_finish_date'] = item['expected_finish_date']
                dataObj['status']               = item['status']
                dataObj['task']                 = item['task']
                dataObj['mile_stone']           = item['mile_stone']
                dataObj['actual_date']          = item['actual_date']
                dataObj['enable']               = item['enable']
                dataObj['inserted_at']          = str(item['inserted_at'])
                dataObj['updated_at']           = str(item['updated_at'])
                result.append(dataObj)

            #調整成只取同單號 同名子
            result.sort(key=itemgetter('form_no')) #需要先排序，然后才能groupby。lst排序后自身被改变
            lstg = groupby(result,itemgetter('form_no'))

            for key,group in lstg:
                for g in group: #group是一个迭代器，包含了所有的分组列表
                    #print(key,g)
                    if key not in keylist:
                        keylist.append(key)
                        reslist.append(g)
            #print("**********************************")
            print(reslist)
            #print("**********************************")
            return reslist

        except Exception as e:
            return 'new_technology_form_review 資料無法取得, 錯誤:{}'.format(str(e))
        
    def check_review_status(self, user_data):
        print(user_data)
        try:

            print(user_data['project_no'])
            obj = self.collection.find_one({"project_no": user_data['project_no']})

            member_list = [] 
            member_list = obj['member_list']
           

            data = []
            result = True
            for item in member_list: 
                if(item['callback'] == False):
                    result  = False
              
            return result         
        except Exception as e:
                return 'check_review_status  錯誤:{}'.format(str(e))
        



    #加入專案指派人員
    def update_new_tech_review_memberlist(self, user_data):
        
        try:
            # print(user_data)
            # print("UUUUUUUUUUUUUUUUUUUUUUUUU")
            obj = self.collection.find({"project_no": user_data['project_no']})
            new_data = user_data['member_list']
            member_list = []
            member_name_list = []

            # print(obj)
            # print("UUUUUUUUUUUUUUUUUUUUUUUUU")

            if obj != None:
                for item in obj:
                    for m_data in item['member_list']:
                        member_list.append(m_data)

                    member_name_list = new_technology_review.find_all_values_by_key(member_list,'cName')
                    
                   

                for data in new_data:                    
                    if new_technology_review.has_string(member_name_list,data['cName']) : 
                        index = new_technology_review.find_index_by_key_value(member_list,'cName',data['cName'])                       
                        if index != None:

                            new_technology_review.update_value_by_key(member_list,index,'task',data['task'])
                            new_technology_review.update_value_by_key(member_list,index,'callback',data['callback'])
                            new_technology_review.update_value_by_key(member_list,index,'mile_stone',data['mile_stone'])
                            new_technology_review.update_value_by_key(member_list,index,'status',data['status'])
                            new_technology_review.update_value_by_key(member_list,index,'form_no',data['form_no'])
                            new_technology_review.update_value_by_key(member_list,index,'form_type',data['form_type'])
                            new_technology_review.update_value_by_key(member_list,index,'work_days',data['work_days'])
                            
                            print("update")
                    else: 
                        member_list.append(data)
                        print("add")
                print(member_list)

                oriquery = {"project_no": user_data['project_no'] }
                filter = {"project_no": user_data['project_no'] }
                newvalues = { "$set": {
                    "member_list"   : member_list,
                    "updated_at"    : datetime.datetime.now()} 
                }

                #只更新最新一筆task紀錄的狀態
                sort =[('updated_at',pymongo.DESCENDING)]
                updated_doc = self.collection.find_one_and_update(filter,newvalues,sort=sort,return_document=ReturnDocument.AFTER)
                # #print(updated_doc)
                return '一筆資料已成功更新於: new_tech_review Document'

            else :
                return ''

        except Exception as e:
            return '一筆資料無法建立於: new_tech_review Document, 錯誤:{}'.format(str(e))
        

      # 使用列表生成式，逐一取得陣列中每個字典的特定key的值  
    def find_all_values_by_key(arr, key):
      
        values = [item[key] for item in arr if key in item]
        return values
    
     # 檢查目標字串是否在陣列中
    def has_string(arr, target_string):
        return target_string in arr
    

         #找出陣列指定key value的index
    def find_index_by_key_value(arr, key, value):
            # 使用enumerate函式來同時取得索引和元素
        for index, item in enumerate(arr):
            # 檢查字典是否有指定的key，並且該key的值等於指定的value
            if key in item and item[key] == value:
                return index
        # 若找不到符合條件的字典，回傳None或者其他你希望的預設值
        return None
    
        # 更新指定字典的key值
    def update_value_by_key(arr, index, key, new_value):
        if 0 <= index < len(arr):
            arr[index][key] = new_value

        




class new_technology_form_review_log:
    def __init__(self, db):
        self.collection = db['new_technology_form_review_log']



    # def insert_new_technology_form_review_log(self, user_data):
    #     #print(user_data)
    #     try:

    #         print(user_data['group'])
    #         obj = self.collection.find_one({"project_no": user_data['project_no']})

    #         if obj == None:
    #             res = self.collection.insert_one(user_data)
    #             return '一筆資料已成功建立於: new_technology_form_review_log Document'
    #         else:
    #             if user_data['group'] == "me":
    #                 oriquery = {"project_no": user_data['project_no']}
    #                 newvalues = { "$set" : {
    #                 "workdays_me_flag" : user_data['workdays_me_flag'],
    #                 "upload_me_flag"   : user_data['upload_me_flag'],
    #                 "updated_at"       : datetime.datetime.now()}
    #                 }
    #             elif user_data['group'] == "ee":
    #                 oriquery = {"project_no": user_data['project_no']}
    #                 newvalues = { "$set": {
    #                 "workdays_ee_flag" : user_data['workdays_ee_flag'],
    #                 "upload_ee_flag"   : user_data['upload_ee_flag'],
    #                 "updated_at"       : datetime.datetime.now()}
    #                 }
    #             else:
    #                 oriquery = {"project_no": user_data['project_no']}
    #                 newvalues = { "$set": {
    #                 "hw_apporve_flag" : user_data['hw_apporve_flag'],
    #                 "hw_reason"       : user_data['hw_reason'],
    #                 "hw_memo"         : user_data['hw_memo'],
    #                 "updated_at"      : datetime.datetime.now()}
    #                 }
    #             res = self.collection.update_one(oriquery, newvalues)
    #             return '一筆資料已成功更新於: new_technology_form_review_log Document'

    #     except Exception as e:
    #         return '一筆資料無法建立於: new_technology_form_review_log Document, 錯誤:{}'.format(str(e))



    # def check_review_log_status(self, user_data):
    #     print(user_data)
    #     try:

    #         print(user_data['project_no'])
    #         obj = self.collection.find_one({"project_no": user_data['project_no']})

    #         if obj["workdays_ee_flag"] == True and obj["upload_ee_flag"] == True and obj["workdays_me_flag"] == True and  obj["upload_ee_flag"] == True:
    #             return True
    #         else:
    #             return False

    #     except Exception as e:
    #         return False 
