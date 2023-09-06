from apps.exts import mongo
import datetime
import json
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby   #itertool还包含有其他很多函数，比如将多个list联合起来
from pymongo.collection import ReturnDocument
import pymongo
from collections import Counter

class new_project_task:
    def __init__(self, db):
        self.collection = db['new_project_task']



    def insert_new_project_task(self, user_data):
        print(user_data)
        try:
            print(user_data['project_no'])
            # obj = self.collection.find_one({"project_no": user_data['project_no']})

            # if obj == None:
            res = self.collection.insert_one(user_data)
            return '一筆資料已成功建立於: new_project_task Document'
            # else:
                # oriquery = {"project_no": user_data['project_no'] }
                # newvalues = { "$set": {
                #     "product_name":                   user_data['product_name'],                   #產品名稱
                #     "product_series":                 user_data['product_series'],                 #產品系列
                #     "spec_describe":                  user_data['spec_describe'],                  #規格說明  
                #     "place_of_production":            user_data['place_of_production'],            #投產地
                #     "product_count_first":            user_data['product_count_first'],            #第一批試產數量
                #     "markting_evaluate":              user_data['markting_evaluate'],              #行銷單位評估
                #     "updated_at": datetime.datetime.now()} 
                #     }
                # res = self.collection.update_one(oriquery,newvalues)
                # return '一筆資料已成功更新於: new_project_task Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_task Document, 錯誤:{}'.format(str(e))



    def get_new_project_task(self, user_data):
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
            return 'new_project_task 資料無法取得, 錯誤:{}'.format(str(e))
        
        
    # 取得RD內部開案指定人員List
    def get_internal_project_task_member(self, pam_data):
        try:
            obj = self.collection.find_one(
                { "project_no": pam_data['project_no'], "enable": True},
                { "_id": 0,"inserted_at": 0, "updated_at": 0})
            print(obj)
            task_member_list = []
            if obj is not None:
                for item in obj['member_list']:
                    print(item['cname'])
                    task_member_list.append(item['cname'])
            return task_member_list
            
        except Exception as e:
            print('new_project_task 資料無法取得, 錯誤:{}'.format(str(e)))
            return []
        


    def delete_new_project_form(self, user_data):
        print(user_data)
        try:
            obj = self.collection.find_one({"uuid": user_data['uuid']})

            if obj != None:
                oriquery = {"uuid": user_data['uuid'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: new_project_form Document'

        except Exception as e:
            return '一筆資料無法刪除於: new_project_task Document, 錯誤:{}'.format(str(e))



    def get_new_project_task_by_member(self, member_name):
        try:
            objs = self.collection.find({"member_list.cName": member_name, "enable" : True},{"_id" : 0}).sort("inserted_at", -1)
            result  = []
            reslist = []
            keylist = []
            for item in objs:
                # print(item)
                item['inserted_at'] = str(item['inserted_at'])
                item['updated_at']  = str(item['updated_at'])
                # dataObj = {}
                # dataObj['uuid']                 = item['uuid']
                # dataObj['form_no']              = item['form_no']
                # dataObj['project_name']         = item['project_name']
                # dataObj['bu']                   = item['bu']
                # dataObj['member_cname']         = item['member_cname']
                # dataObj['expected_start_date']  = item['expected_start_date']
                # dataObj['expected_finish_date'] = item['expected_finish_date']
                # dataObj['status']               = item['status']
                # dataObj['task']                 = item['task']
                # dataObj['mile_stone']           = item['mile_stone']
                # dataObj['actual_date']          = item['actual_date']
                # dataObj['reason']               = item['reason']
                # dataObj['memo']                 = item['memo']
                # dataObj['enable']               = item['enable']
                # dataObj['inserted_at']          = str(item['inserted_at'])
                # dataObj['updated_at']           = str(item['updated_at'])
                result.append(item)

            #調整成只取同單號 同名子
            result.sort(key=itemgetter('form_no')) #需要先排序，然后才能groupby。lst排序后自身被改变
            lstg = groupby(result,itemgetter('form_no'))

            for key,group in lstg:
                for g in group: #group是一个迭代器，包含了所有的分组列表
                    #print(key,g)
                    if key not in keylist:
                        keylist.append(key)
                        reslist.append(g)
           

            #將取回的task、milestone、status跟member_list中的狀態同步
            for item in reslist:               
                for data in item['member_list']:                   
                    if data['cName'] == member_name:
                        item['status'] = data['status'] 
                        item['task'] = data['task']     
                        item['mile_stone'] = data['mile_stone']                       
            #         print(reslist)
            # print("----------------------------------")
            return reslist

        except Exception as e:
            print('new_project_task 資料無法取得, 錯誤:{}'.format(str(e)))
            return []



    #加入專案工作人員 or 更新task
    def update_new_project_task_memberlist(self, user_data):
        
        try:
            #print(user_data['project_no'])
            obj = self.collection.find({"project_no": user_data['project_no']}).sort('updated_at', -1).limit(1)
            new_data = user_data['member_list']
            member_list = []
            member_name_list = []


            if obj != None:
                for item in obj:
                    for m_data in item['member_list']:
                        member_list.append(m_data)

                    member_name_list = new_project_task.find_all_values_by_key(member_list,'cName')
                    
                   

                for data in new_data:                    
                    if new_project_task.has_string(member_name_list,data['cName']) : 
                        index = new_project_task.find_index_by_key_value(member_list,'cName',data['cName'])                       
                        if index != None:

                            new_project_task.update_value_by_key(member_list,index,'task',data['task'])
                            new_project_task.update_value_by_key(member_list,index,'mile_stone',data['mile_stone'])
                            new_project_task.update_value_by_key(member_list,index,'status',data['status'])
                            new_project_task.update_value_by_key(member_list,index,'form_no',data['form_no'])
                            new_project_task.update_value_by_key(member_list,index,'form_type',data['form_type'])
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
            return '一筆資料已成功更新於: new_project_task Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_task Document, 錯誤:{}'.format(str(e))

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

   


     #將ee狀態更新成已完成
    def update_new_project_task_status(self, user_data):
        
        try:
            print(user_data['project_no'])
            obj = self.collection.find({"project_no": user_data['project_no']}).sort('updated_at', -1).limit(1)
            new_member_list = []

            if obj != None:  
                for item in obj:
                    for m_data in item['member_list']:
                        if m_data['group'] == 'ee':
                            m_data['status'] = '已完成'
                        new_member_list.append(m_data)
                    # print(new_member_list)

            #oriquery = {"project_no": user_data['project_no'] }
            filter = {"project_no": user_data['project_no'] }
            newvalues = { "$set": {
                "member_list"   : new_member_list,
                "updated_at"    : datetime.datetime.now()}
            }

            #只更新最新一筆task紀錄的狀態
            sort =[('updated_at',pymongo.DESCENDING)]
            updated_doc = self.collection.find_one_and_update(filter,newvalues,sort=sort,return_document=ReturnDocument.AFTER)
            print(updated_doc)
            return '一筆資料已成功更新於: new_project_task Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_task Document, 錯誤:{}'.format(str(e))



    def get_new_project_task_by_project_no_latest(self, user_data):
        try:

            obj = self.collection.find({"project_no": user_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0,"updated_at" : 0,"enable" : 0}).sort("inserted_at",pymongo.DESCENDING).limit(1)
            dataRes = []
            print(obj)
            for item in obj :
                print(item)
                dataRes.append(item)
            return dataRes

        except Exception as e:
            return 'new_project_task 資料無法取得, 錯誤:{}'.format(str(e))
