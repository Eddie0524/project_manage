from apps.exts import mongo
import datetime
import json



class pcb_form:
    def __init__(self, db):
        self.collection = db['pcb_form']



    def insert_pcb_form(self, pam_data):
        #print(pam_data)
        try:

            obj = self.collection.find_one({"project_no": pam_data['project_no'],"form_no": pam_data['form_no']})

            if obj == None:
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: pcb_form Document'
            else:
                oriquery = {"project_no": pam_data['project_no'] }
                newvalues = { "$set": {
                    "pcb_name":            pam_data['pcb_name'],            #PCB名稱
                    "project_name":        pam_data['project_name'],        #專案名
                    "apply_date":          pam_data['apply_date'],          #申請日期
                    "member_cname":        pam_data['member_cname'],           #申請者
                    "require_date":        pam_data['require_date'],        #需求日期
                    "product_no":          pam_data['product_no'],          #產品型號
                    "product_name":        pam_data['product_name'],       
                    "version":             pam_data['version'],             #版本
                    "gerber_name":         pam_data['gerber_name'],         #gerber_name
                    "place_of_production": pam_data['place_of_production'], #製作地區
                    "place_of_deliver":    pam_data['place_of_deliver'],    #交付地區
                    "deliver_count":       pam_data['deliver_count'],       #交付數量
                    "pcb_type":            pam_data['pcb_type'],            #新產品打樣
                    "purpose_pcb":         pam_data['purpose_pcb'],         #洗板目的
                    "board_spec":          pam_data['board_spec'],          #板材規格
                    "board_diff":          pam_data['board_diff'],          #板厚誤差
                    "impedance_diff":      pam_data['impedance_diff'],      #阻抗誤差
                    "surface_treatment":   pam_data['surface_treatment'],   #表面處理
                    "enig":                pam_data['enig'],                #化金厚度
                    "process":             pam_data['process'],             #製程
                    "dimensional_drawing": pam_data['dimensional_drawing'], #成型尺寸圖
                    "weld_color":          pam_data['weld_color'],          #防焊顏色
                    "ul_mark":             pam_data['ul_mark'],             #UL_MARK
                    "date_code":           pam_data['date_code'],           #date_code
                    "font":                pam_data['font'],                #文字
                    "goldfinger_angle":    pam_data['goldfinger_angle'],    #金手指導繳
                    "angle_depth":         pam_data['angle_depth'],         #導角深度
                    "via_general":         pam_data['via_general'],         #過孔阻焊方式(一般)
                    "via_bga":             pam_data['via_bga'],             #過孔阻焊方式(BGA)
                    "via_special":         pam_data['via_special'],         #過孔阻焊方式(特殊)
                    "sample_require":      pam_data['sample_require'],      #樣品需求數
                    "sample_bad":          pam_data['sample_bad'],          #樣品不良板
                    "sample_vcut":         pam_data['sample_vcut'],         #樣品vcut
                    "attach":              pam_data['attach'],              #交貨附件
                    "pcb_back_date":       pam_data['pcb_back_date'],       #PCB回廠日期
                    "updated_at":          datetime.datetime.now()} 
                    }
                res = self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: pcb_form Document'

        except Exception as e:
            return '一筆資料無法建立於: pcb_form Document, 錯誤:{}'.format(str(e))



    def get_pcb_form(self, pam_data):
        try:
            obj = self.collection.find_one(
                {"project_no": pam_data['project_no'],"form_no": pam_data['form_no'], "enable" : True},
                {"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            #dataRes = []
            print(obj)
            return obj
        except Exception as e:
            return 'pcb_form 資料無法取得, 錯誤:{}'.format(str(e))
        
        
        
    # 取得全部PCB資料(依據人員)
    def get_pcb_info_by_member(self, pam_cname):
        try:
            #print(pam_cname)
            #print("**************************")
            db_query = {'member_cname':pam_cname, 'enable': True }
            objs = self.collection.find(db_query)
            result = []
            for item in objs:
                print(item)
                dataObj = {}
                dataObj['uuid'                  ] = item['uuid'                     ]
                dataObj['form_no'               ] = item['form_no'                  ]
                dataObj['project_no'            ] = item['project_no'               ]
                dataObj['project_name'          ] = item['project_name'             ]
                dataObj['project_type'          ] = item['project_type'             ]
                dataObj['bu'                    ] = item['bu'                       ]
                dataObj['product_name'          ] = item['product_name'             ]
                dataObj['member_cname'          ] = item['member_cname'             ]
                dataObj['apply_date'            ] = item['apply_date'               ]
                dataObj['inserted_at'           ] = item['inserted_at'              ]
                result.append(dataObj)
            return result
        except Exception as e:
            return 'pcb_form 資料無法取得, 錯誤:{}'.format(str(e))
        



class modify_pcb_form:
    def __init__(self, db):
        self.collection = db['modify_pcb_form']   


    def insert_modify_pcb_form(self, pam_data):      
        try:
                
                res = self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: modify_pcb_form Document'           

        except Exception as e:
            return '一筆資料無法建立於: modify_pcb_form Document, 錯誤:{}'.format(str(e))
        


class pcb_form_product_version:
    def __init__(self, db):
        self.collection = db['pcb_form_product_version']


    def insert_pcb_form_product_version(self, pam_data):        
        try:
            obj = self.collection.find_one({"project_no": pam_data['project_no']})

            if obj == None:
                self.collection.insert_one(pam_data)
                return '一筆資料已成功建立於: pcb_form_product_version Document'
            
            else:
                oriquery = {"project_no": pam_data['project_no']}
                newvalues = { "$set": {
                    "major_version":  pam_data['major_version'],
                    "minor_version":  pam_data['minor_version'],
                    "updated_at":     datetime.datetime.now()
                    } 
                }
                self.collection.update_one(oriquery,newvalues)
                return '一筆資料已成功更新於: pcb_form_product_version Document'

        except Exception as e:
            return '一筆資料無法建立於: pcb_form_product_version Document, 錯誤:{}'.format(str(e))


    def get_pcb_form_product_version(self, user_data):        
        try:
            obj = self.collection.find_one({"project_no": user_data['project_no']},{"_id" : 0, "uuid" : 0,"inserted_at": 0 , "enable" : 0 , "updated_at" : 0})
            print(obj)
            return obj

        except Exception as e:
            return 'pcb_form_product_version 資料無法取得, 錯誤:{}'.format(str(e))

      
    def get_project_no_from_pcb_form_product_version(self):        
        try:
            objs = self.collection.find({"enable": True},{"_id" : 0, "uuid" : 0,"inserted_at": 0 , "enable" : 0 , "updated_at" : 0})
            result = []

            for item in objs:
                result.append(item)

            return result

        except Exception as e:
            return 'pcb_form_product_version 資料無法取得, 錯誤:{}'.format(str(e))