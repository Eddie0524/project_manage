from apps.exts import mongo
import datetime
import json
from operator import itemgetter #itemgetter用来去dict中的key，省去了使用lambda函数
from itertools import groupby   #itertool还包含有其他很多函数，比如将多个list联合起来
import pymongo


class new_technology_task:
    def __init__(self, db):
        self.collection = db['new_technology_task']



    def insert_new_technology_task(self, user_data):
        print(user_data)
        try:    
            #print(user_data['form_no'])
            #obj = self.collection.find_one({"form_no": user_data['form_no'],"member_cname" : user_data['member_cname'],"task" : user_data['task']})
            #if obj == None:
            res = self.collection.insert_one(user_data)

            return '一筆資料已成功建立於: new_technology_task Document'
            # else:
            #     oriquery = {"form_no": user_data['form_no'],"member_cname" : user_data['member_cname']}
            #     newvalues = { "$set": {
            #         "status":                   user_data['status'],
            #         "task":                     user_data['task'],
            #         "mile_stone":               user_data['mile_stone'],
            #         "actual_date":              datetime.now() ,
            #         "updated_at":               datetime.now()} 
            #         }
            #     res = self.collection.update_one(oriquery,newvalues)
            #     return '一筆資料已成功更新於: new_technology_form_detail Document'

        except Exception as e:
            return '一筆資料無法建立於: new_technology_task Document, 錯誤:{}'.format(str(e))



    def get_new_technology_task_by_project_no_latest(self, user_data):
        try:
            obj = self.collection.find({"project_no": user_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0,"updated_at" : 0,"enable" : 0}).sort("inserted_at",pymongo.DESCENDING).limit(1)
            dataRes = []
            print(obj)
            for item in obj :
                print(item)
                dataRes.append(item)
            return dataRes

        except Exception as e:
            print('new_technology_task 資料無法取得, 錯誤:{}'.format(str(e)))
            return []



    def delete_new_technology_task(self, user_data):
        print(user_data)
        try:
            obj = self.collection.find_one({"uuid": user_data['uuid']})

            if obj != None:
                oriquery = {"uuid": user_data['uuid'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: new_technology_form_task Document'

        except Exception as e:
            return '一筆資料無法刪除於: new_technology_form_task Document, 錯誤:{}'.format(str(e))



    def get_new_technology_forms_by_member(self, member_name):
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
            result.sort(key=itemgetter('project_no')) #需要先排序，然后才能groupby。lst排序后自身被改变
            lstg = groupby(result,itemgetter('project_no'))

            for key,group in lstg:
                for g in group: #group是一个迭代器，包含了所有的分组列表
                    #print(key,g)
                    if key not in keylist:
                        keylist.append(key)
                        reslist.append(g)
            print("**********************************")
            print(reslist)

            #0717 測試(將取回的task、milestone、status跟 member_list中的狀態同步)
            for item in reslist:               
                for data in item['member_list']:
                    if data['cName'] == member_name:
                        item['status']     = data['status']
                        item['task']       = data['task']
                        item['mile_stone'] = data['mile_stone']
            #         print(reslist)
            # print("----------------------------------")
            return reslist

        except Exception as e:
            print( 'new_technology_form_task 資料無法取得, 錯誤:{}'.format(str(e)) )
            return []
        

