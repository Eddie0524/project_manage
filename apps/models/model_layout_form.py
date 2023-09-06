from apps.exts import mongo
import datetime
import json



class layout_form:
    def __init__(self, db):
        self.collection = db['layout_form']


    def insert_layout_form(self, pam_data):
        print(pam_data)
        try:
            #print(pam_data['form_code'])
            obj = self.collection.find_one({"project_no": pam_data['project_no'],"form_no": pam_data['form_no']})
            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: layout_form Document'
            else:
                oriquery = {"project_no": pam_data['project_no'] }
                newvalues = { "$set": {
                    "project_name":         pam_data['project_name'],
                    "member_cname":         pam_data['member_cname'],            #申請者
                    "form_no":              pam_data['form_no'],
                    "product_no":           pam_data['product_no'],           #產品型號
                    "product_name":         pam_data['product_name'],
                    "pcb_name":             pam_data['pcb_name'],             #PCB名稱
                    "version":              pam_data['version'],              #版本
                    "version_mode":         pam_data['version_mode'],         #版本類型(大/小)改版
                    "product_apply":        pam_data['product_apply'],        #產品申請or修改
                    "apply_date":           pam_data['apply_date'],           #申請日期
                    "product_describe":     pam_data['product_describe'],     #產品說明
                    "spec_2Layer":          pam_data['spec_2Layer'],          #板材規格spec_2Layer
                    "spec_4Layer":          pam_data['spec_4Layer'],          #板材規格spec_4Layer
                    "spec_6Layer":          pam_data['spec_6Layer'],          #板材規格spec_6Layer
                    "spec_other":           pam_data['spec_other'],           #板材規格其他
                    "impedance_require":    pam_data['impedance_require'],    #阻抗需求
                    "impedance_diff":       pam_data['impedance_diff'],       #阻抗誤差
                    "impedance_memo":       pam_data['impedance_memo'],       #阻抗備註
                    "dimensional_drawing":  pam_data['dimensional_drawing'],  #成型尺寸圖
                    "logo_require":         pam_data['logo_require'],         #Logo需求
                    "logo_memo":            pam_data['logo_memo'],            #Logo需求其他
                    "component":            pam_data['component'],            #零件擺放
                    "font":                 pam_data['font'],                 #文字
                    "goldfinger":           pam_data['goldfinger'],           #金手指規範
                    "file":                 pam_data['file'],                 #提供文檔
                    "gerber":               pam_data['gerber'],               #gerber
                    "work_file_format":     pam_data['work_file_format'],     #工作檔格式
                    "gerber_format":        pam_data['gerber_format'],        #gerber格式
                    "fulldata_date":        pam_data['fulldata_date'],        #提供完整資料日期
                    "gerber_date":          pam_data['gerber_date'],          #gerber需求日期
                    "updated_at":           datetime.datetime.now()} 
                }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: layout_form Document'

        except Exception as e:
            return '一筆資料無法建立於: layout_form Document, 錯誤:{}'.format(str(e))



    def get_layout_form(self, user_data):
        try:
            print('-----user_data-----')
            print(user_data['project_no'])
            print(user_data['form_no'])
            obj = self.collection.find_one({"project_no": user_data['project_no'],"form_no": user_data['form_no'],"enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = []
            print(obj)
            return obj

        except Exception as e:
            return 'layout_form 資料無法取得, 錯誤:{}'.format(str(e))



    # 取得全部Layout資料(依據人員)
    def get_layout_info_by_member(self, pam_cname):

        try:
            #print(pam_cname)
            #print("**************************")
            db_query = {'member_cname':pam_cname, 'enable': True }
            objs = self.collection.find(db_query)
            result = []
            for item in objs:
               
                dataObj = {}
                dataObj['uuid'                  ] = item['uuid'                     ]
                dataObj['form_no'               ] = item['form_no'                  ]     #表單編號
                dataObj['project_no'            ] = item['project_no'               ]     #專案編號
                dataObj['project_name'          ] = item['project_name'             ]     #專案名稱
                dataObj['project_type'          ] = item['project_type'             ]     #專案類型(新技術評估/新開案)
                dataObj['bu'                    ] = item['bu'                       ]
                dataObj['product_name'          ] = item['product_name'             ]     #產品名稱
                dataObj['member_cname'          ] = item['member_cname'             ]     #專案執行者
                dataObj['apply_date'            ] = item['apply_date'               ]     #申請日期
                dataObj['inserted_at'           ] = item['inserted_at'              ]
                result.append(dataObj)

            return result

        except Exception as e:
            print('new_project_form 資料無法取得, 錯誤:{}'.format(str(e)))
            return []



    def insert_layout_form_task(self, pam_data):
        #print(pam_data)
        try:
            #if obj == None:
            res = self.collection.insert_one(pam_data)
            return '一筆資料已成功建立於: layout_form_task Document'
            # else:
            #     oriquery = {"form_no": user_data['form_no'],"member_cname" : user_data['member_cname']}
            #     newvalues = { "$set": {
            #         "status"      : user_data['status'],
            #         "task"        : user_data['task'],
            #         "mile_stone"  : user_data['mile_stone'],
            #         "actual_date" : datetime.datetime.now(),
            #         "updated_at"  : datetime.datetime.now()} 
            #         }
            #     res = self.collection.update_one(oriquery,newvalues)
            #     return '一筆資料已成功更新於: new_technology_form_detail Document'

        except Exception as e:
            return '一筆資料無法建立於: layout_form_task Document, 錯誤:{}'.format(str(e))


    def get_all_layout_form(self):        
        try:
            obj = self.collection.find({"enable": True},{"_id" : 0, "project_no" : 1,"product_no" : 1,"pcb_name" : 1,"bu": 1,"uuid" : 1})

            data =  [] 
            print(obj)
            for item in obj :
                #print(item['project_no'])
                #data.append(item['project_no'])
                data.append(item)
            dataRes = data
            return dataRes

        except Exception as e:
            return 'get_ayout_form 資料無法取得, 錯誤:{}'.format(str(e))


class layout_form_product_version:
    def __init__(self, db):
        self.collection = db['layout_form_product_version']


    def insert_layout_form_product_version(self, pam_data):        
        try:
            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: layout_form_product_version Document'
            
            else:
                oriquery = {"project_no": pam_data['project_no']}
                newvalues = { "$set": {
                    "major_version":  pam_data['major_version'],
                    "minor_version":  pam_data['minor_version'],
                    "updated_at":     datetime.datetime.now()
                    } 
                }
                self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: layout_form_product_version Document'

        except Exception as e:
            return '一筆資料無法建立於: layout_form_product_version Document, 錯誤:{}'.format(str(e))


    def get_layout_form_product_version(self, user_data):        
        try:
            obj = self.collection.find_one({"project_no": user_data['project_no']},{"_id" : 0, "uuid" : 0,"inserted_at": 0 , "enable" : 0 , "updated_at" : 0})
            print(obj)
            return obj

        except Exception as e:
            return 'layout_form_product_version 資料無法取得, 錯誤:{}'.format(str(e))

      
    def get_project_no_from_layout_form_product_version(self):        
        try:
            objs = self.collection.find({"enable": True},{"_id" : 0, "uuid" : 0,"inserted_at": 0 , "enable" : 0 , "updated_at" : 0})
            result = []

            for item in objs:
                result.append(item)

            return result

        except Exception as e:
            return 'layout_form_product_version 資料無法取得, 錯誤:{}'.format(str(e))
        


class modify_layout_form:
    def __init__(self, db):
        self.collection = db['modify_layout_form']   


    def insert_modify_layout_form(self, pam_data):      
        try:
                
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: modify_layout_form Document'           

        except Exception as e:
            return '一筆資料無法建立於: modify_layout_form Document, 錯誤:{}'.format(str(e))

    
