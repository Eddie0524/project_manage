from apps.exts import mongo
import datetime
import json
import os
import pymongo
from pymongo.collection import ReturnDocument

class new_project_form:
    def __init__(self, db):
        self.collection = db['new_project_form']



    def insert_new_project_form(self, pam_data):
        #print(pam_data)
        try:
            print(pam_data)
            print("****************************")
            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: new_project_form Document'
            else:
                print(pam_data)
                oriquery = {"project_no": pam_data['project_no'] }
                newvalues = { "$set": {                    
                    "form_no"                        : pam_data['form_no'],
                    "form_type"                      : pam_data['form_type'],
                    "bu"                             : pam_data['bu'],
                    "project_no":                     pam_data['project_no'],       
                    "project_name":                   pam_data['project_name'],                   #專案名
                    "product_name":                   pam_data['product_name'],                   #產品名稱
                    "product_no":                     pam_data['product_no'],                   #產品型號
                    "product_series":                 pam_data['product_series'],                 #產品系列
                    "product_check":                  pam_data['product_check'],                 #產品系列
                    "spec_describe":                  pam_data['spec_describe'],                  #規格說明
                    "product_certified":              pam_data['product_certified'],              #認證
                    "compete_status":                 pam_data['compete_status'],                 #競爭狀況
                    "target_markting":                pam_data['target_markting'],                #目標市場
                    "estimate_price":                 pam_data['estimate_price'],                 #預估銷售價
                    "estimate_pcs":                   pam_data['estimate_pcs'],                   #預估銷數量
                    "estimate_sale_performance_year": pam_data['estimate_sale_performance_year'], #預估年銷售業績
                    "estimate_profit_margin":         pam_data['estimate_profit_margin'],         #預估毛利率
                    "replace_product_flag":           pam_data['replace_product_flag'],           #是否有取代舊有產品
                    "replace_product":                pam_data['replace_product'],                #取代的產品型號
                    "patent_evaluate":                pam_data['patent_evaluate'],                #專利評估
                    "work_hour_ee":                   pam_data['work_hour_ee'],                   #電子開發部工時
                    "cost_ee":                        pam_data['cost_ee'],                        #電子開發部開發成本
                    "start_date_ee":                  pam_data['start_date_ee'], 
                    "end_date_ee":                    pam_data['end_date_ee'], 
                    "work_hour_me":                   pam_data['work_hour_me'],                   #機構開發部工時
                    "cost_me":                        pam_data['cost_me'],                        #機構開發部開發成本
                    "start_date_me":                  pam_data['start_date_me'], 
                    "end_date_me":                    pam_data['end_date_me'], 
                    "work_hour_sw":                   pam_data['work_hour_sw'],                   #軟體開發部工時
                    "cost_sw":                        pam_data['cost_sw'],                        #軟體開發部開發成本
                    "start_date_sw":                  pam_data['start_date_sw'], 
                    "end_date_sw":                    pam_data['end_date_sw'], 
                    "work_hour_ds":                   pam_data['work_hour_ds'],                   #設計驗證部工時
                    "cost_ds":                        pam_data['cost_ds'],                        #設計驗證部開發成本
                    "start_date_ds":                  pam_data['start_date_ds'], 
                    "end_date_ds":                    pam_data['end_date_ds'], 
                    "place_of_production":            pam_data['place_of_production'],            #投產地
                    "develop_unit"                  : pam_data['develop_unit'],                     #開發單位               
                    "product_count_first":            pam_data['product_count_first'],            #第一批試產數量
                    "markting_evaluate":              pam_data['markting_evaluate'],              #行銷單位評估
                    "first_product_date":             pam_data['first_product_date'],              #預計上市日期
                    "member_list":                    pam_data['member_list'],                      #指派清單
                    "updated_at":                     datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: new_project_form Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_form Document, 錯誤:{}'.format(str(e))




    def get_new_project_form(self, pam_data):
        
        try:
            print(pam_data)
           
            obj = self.collection.find_one({"project_no": pam_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = []
            print(obj)
            # for item in obj :
            #     print(item)
            #     dataRes.append(item)
            return obj

        except Exception as e:
            print ('new_project_form 資料無法取得, 錯誤:{}'.format(str(e)))
            return {}



    # 取得全部新開案資料(依據人員)
    def get_new_project_info_by_member(self, pam_cname):
        try:
            db_query = {'member_cname':pam_cname, 'enable': True }
            objs = self.collection.find(db_query)
            result = []
            for item in objs:
                dataObj = {}
                dataObj['uuid'                  ] = item['uuid'                     ]
                dataObj['form_no'               ] = item['form_no'                  ]     #表單編號
                dataObj['project_no'            ] = item['project_no'               ]     #專案編號
                dataObj['project_name'          ] = item['project_name'             ]
                dataObj['project_type'          ] = item['project_type'             ]     #專案類型(新技術評估/新開案)
                dataObj['bu'                    ] = item['bu'                       ]
                dataObj['product_name'          ] = item['product_name'             ]     #產品名稱
                dataObj['member_cname'          ] = item['member_cname'             ]     #專案執行者
                dataObj['apply_date'            ] = item['apply_date'               ]     #申請日期
                dataObj['inserted_at'           ] = item['inserted_at'              ]
                result.append(dataObj)
            return result
        
        except Exception as e:
            return 'new_project_form 資料無法取得, 錯誤:{}'.format(str(e))
        
        
    def get_new_project_spec_describle(self, pam_data):
        try:
            obj = self.collection.find_one({"project_no": pam_data})
            spec_describe = "--"
            if obj != None:
                spec_describe = obj['spec_describe']
            return spec_describe
            
        except Exception as e:
            print('spec_describe 資料無法取得, 錯誤:{}'.format(str(e)))
            return "--"



    def get_new_project_apply_date(self, pam_data):
        try:
            obj = self.collection.find_one({"project_no": pam_data})
            print("----------------obj-------------")
            print(obj)
            apply_date = "--"
            if obj != None:
                apply_date = obj['apply_date']
            return apply_date
            
        except Exception as e:
            print('apply_date 資料無法取得, 錯誤:{}'.format(str(e)))
            return "--"


    def get_new_project_form_no(self, pam_data):
        try:
            obj = self.collection.find_one({"project_no": pam_data})
            #print("----------------obj-------------")
            #print(obj)
            form_no = "--"
            if obj != None:
                form_no = obj['form_no']
            return form_no
            
        except Exception as e:
            print('form_no 資料無法取得, 錯誤:{}'.format(str(e)))
            return "--"
            #return 'apply_date 資料無法取得, 錯誤:{}'.format(str(e))



    #從新開案申請單取得所有專案代號及產品型號
    def get_all_new_project_no(self):
        try:
            obj = self.collection.find(
                { "enable" : True},
                {"_id" : 0,"project_no" : 1 ,"product_no" : 1 ,"uuid" : 1 ,"bu" : 1 })
            data =  [] 
            print(obj)
            for item in obj :
                #print(item['project_no'])
                #data.append(item['project_no'])
                data.append(item)
            dataRes = data
            return dataRes 

        except Exception as e:
            return '資料無法取得, 錯誤:{}'.format(str(e))


    #從新開案申請單取得所有產品型號
    def get_all_new_product_no(self):
        try:
            obj = self.collection.find(
                { "enable" : True},
                {"_id" : 0,"product_no" : 1 })
            data =  [] 
            print(obj)
            for item in obj :
                print(item['product_no'])
                data.append(item['product_no'])
            dataRes = {"product_no" : data }
            return dataRes 

        except Exception as e:
            return '資料無法取得, 錯誤:{}'.format(str(e))



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
            return '一筆資料無法刪除於: new_project_form Document, 錯誤:{}'.format(str(e))
        



    #加入專案指派人員
    def update_new_project_form_memberlist(self, user_data):
        
        try:
            #print(user_data['project_no'])
            obj = self.collection.find({"project_no": user_data['project_no']})
            new_data = user_data['member_list']
            member_list = []
            member_name_list = []


            if obj != None:
                for item in obj:
                    for m_data in item['member_list']:
                        member_list.append(m_data)

                    member_name_list = new_project_form.find_all_values_by_key(member_list,'cName')
                    
                   

                for data in new_data:                    
                    if new_project_form.has_string(member_name_list,data['cName']) : 
                        index = new_project_form.find_index_by_key_value(member_list,'cName',data['cName'])                       
                        if index != None:

                            new_project_form.update_value_by_key(member_list,index,'task',data['task'])
                            new_project_form.update_value_by_key(member_list,index,'mile_stone',data['mile_stone'])
                            new_project_form.update_value_by_key(member_list,index,'status',data['status'])
                            new_project_form.update_value_by_key(member_list,index,'form_no',data['form_no'])
                            new_project_form.update_value_by_key(member_list,index,'form_type',data['form_type'])
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
            return '一筆資料已成功更新於: new_project_form Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_form Document, 錯誤:{}'.format(str(e))
        

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


class new_project_form_log:
    def __init__(self, db):
        self.collection = db['new_project_form_log']


    def insert_new_project_form_log(self, pam_data):
        print(pam_data)
        try:
            print(pam_data['project_no'])
            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: new_project_form_log Document'
            else:
                if pam_data['role'] == "pm":
                    oriquery = {"project_no": pam_data['project_no'] }
                    newvalues = { "$set": {
                        "pm_approve_flag":    pam_data['pm_approve_flag'],           #PM主管是否核准旗標
                        "pm_back_reason":     pam_data['pm_back_reason'],            #PM主管退回原因
                        "pm_back_memo":       pam_data['pm_back_memo'],              #PM主管退回說明 
                        "updated_at":         datetime.datetime.now()
                        } 
                    }
                elif pam_data['role'] == "hw":
                    oriquery = {"project_no": pam_data['project_no'] }
                    newvalues = { "$set": {                       
                        "hw_approve_flag":    pam_data['hw_approve_flag'],           #HW主管是否核准旗標
                        "hw_back_reason":     pam_data['hw_back_reason'],            #HW主管退回原因
                        "hw_back_memo":       pam_data['hw_back_memo'],              #HW主管退回說明  
                        "updated_at":         datetime.datetime.now()
                        } 
                    }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: new_project_form_log Document'

        except Exception as e:
            return '一筆資料無法建立於: new_project_form_log Document, 錯誤:{}'.format(str(e))
        



 
class modify_new_project_form:
    def __init__(self, db):
        self.collection = db['modify_new_project_form']   


    def insert_modify_new_project_form(self, pam_data):      
        try:
                
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: modify_new_project_form Document'           

        except Exception as e:
            return '一筆資料無法建立於: modify_new_project_form Document, 錯誤:{}'.format(str(e))
