from apps.exts import mongo
import datetime
import json
import os
from pathlib import Path
from apps.settings import FILE_PATH
from apps.settings import FILE_URL
from flask import  send_file

class new_technology_form:
    def __init__(self, db):
        self.collection = db['new_technology_form']



    def insert_new_technology_form(self, pam_data):
        #print(pam_data)
        try:

            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: new_technology_form Document'
            else:
                oriquery = {"project_no": pam_data['project_no'] }
                newvalues = { "$set": {
                    "bu":                     pam_data['bu'],
                    "project_name":           pam_data['project_name'],
                    "form_type" :             pam_data['form_type'],
                    "project_type":           pam_data['project_type'],
                    "product_name":           pam_data['product_name'],
                    "product_describe":       pam_data['product_describe'],
                    "product_application":    pam_data['product_application'],
                    "spec_describe":          pam_data['spec_describe'],
                    "customer_require":       pam_data['customer_require'],
                    "expected_finished_date": pam_data['expected_finished_date'],
                    "cost":                   pam_data['cost'],
                    "estimate_date":          pam_data['estimate_date'],
                    "apply_date":             pam_data['apply_date'],
                    "updated_at":             datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: new_technology_form Document'

        except Exception as e:
            return '一筆資料無法建立於: new_technology_form Document, 錯誤:{}'.format(str(e))



    def get_new_technology_form(self, user_data):
        try:
            print(user_data)
           
            obj = self.collection.find_one({"project_no": user_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = []
            print(obj)
            # for item in obj :
            #     print(item)
            #     dataRes.append(item)

            return obj#json.dumps(obj, default=str)

        except Exception as e:
            return 'new_technology_form 資料無法取得, 錯誤:{}'.format(str(e))



    # 取得全部新技術評估資料(依據人員)
    def get_new_technology_info_by_member(self, pam_cname):
        try:
            #print(pam_cname)
            #print("**************************")
            db_query = {'member_cname':pam_cname, 'enable': True }
            objs = self.collection.find(db_query)
            result = []
            for item in objs:
                #print(item)
                dataObj = {}
                dataObj['uuid'                  ] = item['uuid'                  ]
                dataObj['form_no'               ] = item['form_no'               ]
                dataObj['project_no'            ] = item['project_no'            ]
                dataObj['project_name'          ] = item['project_name'          ]
                dataObj['project_type'          ] = item['project_type'          ]
                dataObj['bu'                    ] = item['bu'                    ]
                dataObj['product_name'          ] = item['product_name'          ]
                dataObj['member_cname'          ] = item['member_cname'          ]
                dataObj['apply_date'            ] = item['apply_date'            ]
                dataObj['inserted_at'           ] = item['inserted_at'           ]
                result.append(dataObj)
            return result
        except Exception as e:
            print('new_technology_form 資料無法取得, 錯誤:{}'.format(str(e)))
            return []



    def delete_new_technology_form(self, pam_data):
        print(pam_data)
        try:    
            obj = self.collection.find_one({"uuid": pam_data['uuid']})

            if obj != None:
                oriquery = {"uuid": pam_data['uuid'] }
                newvalues = { "$set": { "enable" : False,"updated_at": datetime.datetime.now()} }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功刪除於: new_technology_form Document'

        except Exception as e:
            return '一筆資料無法刪除於: new_technology_form Document, 錯誤:{}'.format(str(e))



    def get_all_new_tech_project_name(self):

        try:
            obj = self.collection.find({ "enable" : True},{"_id" : 0, "project_name" : 1 })
            data = []
            for item in obj:
                #print(item)
                data.append(item['project_name'])
            dataRes = {"project_name" : data}
            return dataRes

        except Exception as e:
            return 'project_name 資料無法取得, 錯誤:{}'.format(str(e))


    def get_new_tech_project_spec_describle(self, pam_data):
        try:
            obj = self.collection.find_one({"project_no": pam_data})
            spec_describe = "--"
            if obj != None:
                spec_describe = obj['spec_describe']
            return spec_describe
            
        except Exception as e:
            print('spec_describe 資料無法取得, 錯誤:{}'.format(str(e)))
            return "--"


    def get_new_tech_project_apply_date(self, pam_data):
        try:
            obj = self.collection.find_one({"project_no": pam_data})
            #print("----------------obj-------------")
            #print(obj)
            apply_date = "--"
            if obj != None:
                apply_date = obj['apply_date']
            return apply_date

        except Exception as e:
            print('apply_date 資料無法取得, 錯誤:{}'.format(str(e)))
            return "--"


    def get_new_tech_project_form_no(self, pam_data):
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


    def get_upload_file(self, pam_data):
        try:
            file_list = []
            if pam_data['project_no'] != '':
                network_path = r"\\{}\\upload\\temp\\{}\\".format(FILE_PATH,pam_data['project_no'])
                print(network_path)

                files = os.listdir(network_path)
                file_list = []
                
                for file in files:
                    file_path = os.path.join(network_path, file)
                    if os.path.isfile(file_path):                    
                        url = 'http://{}/upload/temp/{}/{}'.format(FILE_URL,pam_data['project_no'],file)
                        print(f"File : {file}")
                        print(f"File found: {url}")
                        file_list.append(url)
            return file_list

        except Exception as e:
            print('資料無法取得, 錯誤:{}'.format(str(e)))
            return []



class modify_new_technology_form:
    def __init__(self, db):
        self.collection = db['modify_new_technology_form']


    def insert_modify_new_technology_form(self, pam_data):
        try:
            res = self.collection.insert_one(pam_data)
            return '一筆資料已成功建立於: modify_new_technology_form Document'

        except Exception as e:
            return '一筆資料無法建立於: modify_new_technology_form Document, 錯誤:{}'.format(str(e))
