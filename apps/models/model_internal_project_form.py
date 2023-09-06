from apps.exts import mongo
import datetime
import json
import os
from pathlib import Path
from apps.settings import FILE_PATH
from apps.settings import FILE_URL
from flask import  send_file

class internal_project_form:
    def __init__(self, db):
        self.collection = db['internal_project_form']



    def insert_internal_project_form(self, pam_data):
        #print(pam_data)
        try:

            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: internal_project_form Document'
            else:
                oriquery = {"project_no": pam_data['project_no'] }
                newvalues = { "$set": {                  
                    "project_name":           pam_data['project_name'],
                    "form_type" :            '內部開案單',
                    "project_type":          'project',                  
                    "project_describe":       pam_data['product_describe'],                
                    "spec_describe":          pam_data['spec_describe'],                   
                    "expected_finished_date": pam_data['expected_finished_date'],
                    "cost":                   pam_data['cost'],
                    "estimate_date":          pam_data['estimate_date'],
                    "apply_date":             pam_data['apply_date'],
                    "updated_at":             datetime.datetime.now()
                    }
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: internal_project_form Document'

        except Exception as e:
            return '一筆資料無法建立於: new_technology_form Document, 錯誤:{}'.format(str(e))



    def get_internal_project_form(self, pam_data):
        try:
            print(pam_data)
           
            obj = self.collection.find_one({"project_no": pam_data['project_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
           
            print(obj)        

            return obj

        except Exception as e:
            return 'new_technology_form 資料無法取得, 錯誤:{}'.format(str(e))



    # 取得全部新技術評估資料(依據人員)
    def get_internal_project_info_by_member(self, pam_cname):
        try:
            #print(pam_cname)
            #print("**************************")
            db_query = {'member_cname':pam_cname, 'enable': True }
            objs = self.collection.find(db_query)
            result = []
            for item in objs:
                # print(item)
             
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
            print('internal_project_form 資料無法取得, 錯誤:{}'.format(str(e)))
            return []



    