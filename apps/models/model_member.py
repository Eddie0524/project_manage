from apps.exts import mongo
import json
from bson import ObjectId
import datetime


class Member:
    def __init__(self, db):
        self.collection = db['member']



    # 建立一筆人員資料
    def create_member(self, user_data):
        #print(user_data)
        try:
            obj = self.collection.find_one({"account": user_data['account']})
            #print(obj)
            if obj is None:
                self.collection.insert_one(user_data)
            else:
                db_query = {"account": user_data['account'] }
                new_values = { "$set": {
                    "uuid"      : user_data['uuid'],
                    "account"   : user_data['account'],
                    "password"  : user_data['password'],
                    "pretor"    : user_data['pretor'],        # 直屬主管
                    "relation"  : user_data['relation'],      # 平行單位
                    "role"      : user_data['role'],          # 角色 (員工/主管/管理者) staff / leader / admin
                    "position"  : user_data['position'],      # 職務 (工程師/副理/總經理)
                    "organize"  : user_data['organize'],
                    "org_no"    : user_data['org_no'],
                    "department": user_data['department'] ,
                    "dpt_no"    : user_data['dpt_no'],
                    "group_name": user_data['group_name'],
                    "group_no"  : user_data['group_no'],
                    "region"    : user_data['region'],
                    "cname"     : user_data['cname'],
                    "ename"     : user_data['ename'],
                    "full_name" : user_data['full_name'],
                    "staff_no"  : user_data['staff_no'],
                    "ext"       : user_data['ext'],
                    "sex"       : user_data['sex'],
                    "avatar"    : user_data['avatar'],
                    "enable"    : user_data['enable'],
                    "memo"      : user_data['memo'],
                    "updated_at": datetime.datetime.now()
                }}
                self.collection.update_one(db_query, new_values)
            strMsg = '一筆人員資料已成功建立'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆人員資料建立失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # 查詢一筆人員資料(依據account)
    def read_member_by_account(self, pam_account):
        db_query = { "account":pam_account }
        try:
            cursor = self.collection.find(db_query)
            member = cursor.next()
            #print(member)
            member['_id'] = str(member['_id'])
            member['inserted_at'] = str(member['inserted_at'])
            return 'ok', member
        except Exception as e:
            cursor = self.collection.find(db_query)
            documents = list(cursor)
            if documents == []:
                return 'fail', '查詢無人員資料'
            else:
                strMsg = '一筆人員資料查詢失敗,錯誤訊息:{}'.format(str(e))
                return 'fail', strMsg



    # 修改一筆人員資料(group)
    def update_group_of_member(self, pam_account, pam_group_name, pam_group_no):
        try:
            db_query = { "account":pam_account }
            new_values = { "$set":{ "group_name":pam_group_name, "group_no":pam_group_no } }
            self.collection.update_one( db_query, new_values)
            strMsg = '一筆人員資料(group_name 和 group_no)已成功更新'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆人員資料(group_name 和 group_no)更新失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # 刪除一筆人員資料(依據account)
    def delete_member_by_account(self, account):
        try:
            db_query = { "account": account }
            self.collection.delete_one(db_query)
            strMsg = '一筆人員資料已成功刪除'
            return 'ok', strMsg
        except Exception as e:
            strMsg = '一筆人員資料刪除失敗,錯誤訊息:{}'.format(str(e))
            return 'fail', strMsg



    # 判斷人員是否存在
    def check_login_status(self, pam_account, pam_pwd):
        try:
            db_query = {'account':pam_account, 'password':pam_pwd}
            cursor = self.collection.find(db_query)
            print(cursor)
            documents = list(cursor)
            if documents == []:
                return False
            else:
                return True
        except Exception as e:
            print(str(e))
            return False



    # 查詢登入人員資料(依據account/password)
    def find_by_account(self, pam_account, pam_pwd):
        try:
            db_query = {'account':pam_account, 'password':pam_pwd}
            cursor = self.collection.find(db_query)
            member = cursor.next()
            member['_id'] = str(member['_id'])
            return member
        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    # 判斷是否為主管(依帳號)
    def check_leader_by_account(self, pam_account):
        try:
            obj = self.collection.find_one({"account":pam_account, "enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            if obj != None: 
                if obj['role'] == 'leader':
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False



    # 判斷是否為主管(依人名)
    def check_leader_by_cname(self, pam_cname):
        try:
            obj = self.collection.find_one({"cname":pam_cname, "enable" : True},{"_id" : 0,"inserted_at" : 0 ,"updated_at" : 0})
            if obj != None: 
                if obj['role'] == 'leader':
                    return True
                else:
                    return False
            else:
                return False
        except Exception as e:
            return False


    # 取回所屬部門
    def find_department_by_cname(self, pam_cname):
        try:
            obj = self.collection.find_one({"cname":pam_cname})
            if obj != None: 
               return obj['department']
            else:
                return ""
        except Exception as e:
            return ""


    # 取回所屬組織
    def find_organize_by_cname(self, pam_cname):
        try:
            obj = self.collection.find_one({"cname":pam_cname})
            if obj != None: 
               return obj['organize']
            else:
                return ""
        except Exception as e:
            return ""


    # 取回所屬群組  ee/me/ld  /pm 
    def find_group_no_by_cname(self, pam_cname):
        try:
            obj = self.collection.find_one({"cname":pam_cname})
            if obj != None: 
               return obj['group_no']
            else:
                return ""
        except Exception as e:
            return ""


    # 查詢人員直屬主管名
    def find_leader_name_by_account(self, pam_account):
        try:
            #print(pam_account)
            matching_members = self.collection.find({'account': pam_account})
            member = matching_members.next()
            #print(member)
            member['_id'] = str(member['_id'])
            return  member['pretor'] #json.dumps(member)

        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    # 查詢人員直屬主管信箱
    def find_leader_email_by_name(self, pam_cname):
        try:
            matching_members = self.collection.find({'cname': pam_cname})
            member = matching_members.next()
            leader_account = self.find_email_by_name(member['pretor'])
            #print(leader_account)
            #leader['_id'] = str(leader['_id'])
            #leader['account'] #json.dumps(member)
            return  leader_account

        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    # 查詢人員主管信箱
    def find_email_by_name(self, pam_cname):
        try:
            #print(pam_account)
            matching_members = self.collection.find({'cname': pam_cname})
            member = matching_members.next()
            #print(member)
            member['_id'] = str(member['_id'])
            return  member['account']  #json.dumps(member)

        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    # 取得人員名(依照部門)
    def find_cname_by_organize(self, pam_organize):
        try:
            objs = self.collection.find({'organize': pam_organize})
            print(objs)
            result = []
            for item in objs:
                print(item)
                #dataObj = {}
                #dataObj['cname'] = item['cname']
                #dataObj['ename'] = item['ename']
                #dataObj['mail']  = item['account']
                #dataObj['group'] = item['group_no']
                result.append(item['cname'])
            return result
        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))



    # 取得人員名與信箱依照部門
    def find_member_by_organize(self, pam_organize):
        try:
            objs = self.collection.find({'organize': pam_organize})
            result = []
            for item in objs:
                print(item)
                dataObj = {}
                dataObj['cname'] = item['cname']
                dataObj['ename'] = item['ename']
                dataObj['mail']  = item['account']
                dataObj['group']  = item['group_no']
                result.append(dataObj)
            return result
        except Exception as e:
            return '人員資料無法取得, 錯誤:{}'.format(str(e))