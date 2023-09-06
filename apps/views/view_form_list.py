from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
import json
import datetime
import uuid
from apps.exts import mongo
from apps.models.model_new_technology_form import new_technology_form
from apps.models.model_new_project_form    import new_project_form
from apps.models.model_layout_form         import layout_form
from apps.models.model_pcb_form            import pcb_form
from apps.models.model_internal_project_form  import internal_project_form
from apps.models.model_form_flow           import form_flow
from apps.models.model_flow_step           import Flow_Step
from apps.views.view_member                import get_cname_by_organize
from apps.views.view_member                import get_organize_by_cname
from apps.models.model_member              import Member



blue_form_list = Blueprint('blue_form_list', __name__)



def init_blue_form_list(app):
    app.register_blueprint(blueprint=blue_form_list)



@blue_form_list.route("/page/v0/form_list/", methods=['GET'])
def form_list_index():

    mode = "form_list"
    
    project_no = request.args.get('project_no')

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    if account is None:
        return redirect(url_for('blue_main.login_fun'))
    else:
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isLeader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)

        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        return render_template(
            'form_list.html',
            MODE=mode,
            GROUP_NO=group_no,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            IS_LEADER=isLeader,
            PROJECT_NO=project_no)



# 取得所有 form_list 資料(依據部門) 主管視角
@blue_form_list.route("/api/v0/db/data/form_list/by/leader/", methods=['GET'])
def get_form_list_by_leader():
    
    leader = request.args.get('user')
    
    # 先取得部門組織
    organize = get_organize_by_cname(leader)
    #print(organize)

    #  先取得相關人員
    member_list = get_cname_by_organize(organize)
    print(member_list)
    
    result_obj = {}
    result_list = []
    
    # 依照人員將資料找出
    for cname in member_list:
        list_info = []
        # 新技術評估
        # 取回評估案資料(by 申請者)表單查詢用
        new_technology_model = new_technology_form(mongo.db)
        result_technology = new_technology_model.get_new_technology_info_by_member(cname)

        if len(result_technology) > 0:
            for tec_item in result_technology:
                tec_info_obj = {}
                tec_info_obj['uuid']         = tec_item['uuid']
                tec_info_obj['form_no']      = tec_item['form_no']
                tec_info_obj['project_no']   = tec_item['project_no']
                tec_info_obj['project_name'] = tec_item['project_name']
                tec_info_obj['project_type'] = '新產品技術評估申請單'
                tec_info_obj['bu']           = tec_item['bu']
                tec_info_obj['product_name'] = tec_item['product_name']
                tec_info_obj['member_cname'] = tec_item['member_cname']
                tec_info_obj['apply_date']   = tec_item['apply_date']
                tec_info_obj['inserted_at']  = tec_item['inserted_at']
                #tec_info_obj['status']       = process_form_status(tec_item['form_no'])
                list_info.append(tec_info_obj)
        
            # 新開案
            new_project_model = new_project_form(mongo.db)
            result_project = new_project_model.get_new_project_info_by_member(cname)
            if len(result_project) > 0:
                for pro_item in result_project:

                    if tec_item['project_type'] == 'project':
                        project_type = '新產品開發申請單'

                    pro_info_obj = {}
                    pro_info_obj['uuid']         = pro_item['uuid']
                    pro_info_obj['form_no']      = pro_item['form_no']
                    pro_info_obj['project_no']   = pro_item['project_no']
                    pro_info_obj['project_name'] = pro_item['project_name']
                    pro_info_obj['project_type'] = '新產品開發申請單'
                    pro_info_obj['bu']           = pro_item['bu']
                    pro_info_obj['product_name'] = pro_item['product_name']
                    pro_info_obj['member_cname'] = pro_item['member_cname']
                    pro_info_obj['apply_date']   = pro_item['apply_date']
                    pro_info_obj['inserted_at']  = pro_item['inserted_at']
                    #pro_info_obj['status']       = process_form_status(pro_item['form_no'])
                    list_info.append(pro_info_obj)


             # RD內部開案
            internal_project_model = internal_project_form(mongo.db)
            result__internal= internal_project_model.get_internal_project_info_by_member(cname)
            if len(result__internal) > 0:
                for int_item in result__internal:

                    int_info_obj = {}
                    int_info_obj['uuid']         = int_item['uuid']
                    int_info_obj['form_no']      = int_item['form_no']
                    int_info_obj['project_no']   = int_item['project_no']
                    int_info_obj['project_name'] = int_item['project_name']
                    int_info_obj['project_type'] = '內部開案單'
                    int_info_obj['bu']           = int_item['bu']
                    int_info_obj['product_name'] = int_item['product_name']
                    int_info_obj['member_cname'] = int_item['member_cname']
                    int_info_obj['apply_date']   = int_item['apply_date']
                    pro_info_obj['inserted_at']  = pro_item['inserted_at']
                    #pro_info_obj['status']       = process_form_status(pro_item['form_no'])
                    list_info.append(int_info_obj)

            # Layout 
            layout_model = layout_form(mongo.db)
            result_layout = layout_model.get_layout_info_by_member(cname)
            #print(result_layout)
            if len(result_layout) > 0:
                for layout_item in result_layout:
                    layout_info_obj = {}
                    layout_info_obj['uuid']         = layout_item['uuid']
                    layout_info_obj['form_no']      = layout_item['form_no']
                    layout_info_obj['project_no']   = layout_item['project_no']
                    layout_info_obj['project_name'] = layout_item['project_name']
                    layout_info_obj['project_type'] = 'Layout申請工程規格聯絡單'
                    layout_info_obj['bu']           = layout_item['bu']
                    layout_info_obj['product_name'] = layout_item['product_name']
                    layout_info_obj['member_cname'] = layout_item['member_cname']
                    layout_info_obj['apply_date']   = layout_item['apply_date']
                    layout_info_obj['inserted_at']  = layout_item['inserted_at']
                    #layout_info_obj['status']       = process_form_status(layout_item['form_no'])
                    list_info.append(layout_info_obj)
        
            # PCB
            pcb_model = pcb_form(mongo.db)
            result_pcb =  pcb_model.get_pcb_info_by_member(cname)
            #print(result_pcb)
            if len(result_pcb) > 0:
                for pcb_item in result_pcb:
                    pcb_info_obj = {}
                    pcb_info_obj['uuid']         = pcb_item['uuid']
                    pcb_info_obj['form_no']      = pcb_item['form_no']
                    pcb_info_obj['project_no']   = pcb_item['project_no']
                    pcb_info_obj['project_name'] = pcb_item['project_name']
                    pcb_info_obj['project_type'] = 'PCB打樣申請工程規格聯絡單'
                    pcb_info_obj['bu']           = pcb_item['bu']
                    pcb_info_obj['product_name'] = pcb_item['product_name']
                    pcb_info_obj['member_cname'] = pcb_item['member_cname']
                    pcb_info_obj['apply_date']   = pcb_item['apply_date']
                    pcb_info_obj['inserted_at']  = pcb_item['inserted_at']
                    #pcb_info_obj['status']       = process_form_status(pcb_item['form_no'])
                    list_info.append(pcb_info_obj)

            # for info in list_info:
            #     print(info['form_no'])
        
            # 過濾重複 form_no 值
            unique_form_nos = set()
            filtered_data = []

            for item in list_info:
                form_no = item["form_no"]
                if form_no not in unique_form_nos:
                    unique_form_nos.add(form_no)
                    item['status'] = process_form_status(form_no)
                    filtered_data.append(item)

            print(filtered_data)
            #result_list.append(filtered_data)
            if filtered_data != []:
                #result_obj[cname] = filtered_data
                result_list += filtered_data
    
    return result_list



# 取得所有 form_list 資料(依據人員)
@blue_form_list.route("/api/v0/db/data/form_list/all/", methods=['GET'])
def get_form_list_all():
    
    # 申請者
    applicant = request.args.get('user')
    print(applicant)
  
    
    list_info = []
    
    # 新技術評估
    # 取回評估案資料(by 申請者)表單查詢用
    new_technology_model = new_technology_form(mongo.db)
    result_technology = new_technology_model.get_new_technology_info_by_member(applicant)
    #print(result_technology)
    
    if len(result_technology) > 0:
        for tec_item in result_technology:

            tec_info_obj = {}
            tec_info_obj['uuid']         = tec_item['uuid']
            tec_info_obj['form_no']      = tec_item['form_no']
            tec_info_obj['project_no']   = tec_item['project_no']
            tec_info_obj['project_name'] = tec_item['project_name']
            tec_info_obj['project_type'] = '新產品技術評估申請單'
            tec_info_obj['bu']           = tec_item['bu']
            tec_info_obj['product_name'] = tec_item['product_name']
            tec_info_obj['member_cname'] = tec_item['member_cname']
            tec_info_obj['apply_date']   = tec_item['apply_date']
            tec_info_obj['inserted_at']  = tec_item['inserted_at']
            #tec_info_obj['status']       = process_form_status(tec_item['form_no'])
            list_info.append(tec_info_obj)
    
    # 新開案
    new_project_model = new_project_form(mongo.db)
    result_project = new_project_model.get_new_project_info_by_member(applicant)
    if len(result_project) > 0:
        for pro_item in result_project:

            pro_info_obj = {}
            pro_info_obj['uuid']         = pro_item['uuid']
            pro_info_obj['form_no']      = pro_item['form_no']
            pro_info_obj['project_no']   = pro_item['project_no']
            pro_info_obj['project_name'] = pro_item['project_name']
            pro_info_obj['project_type'] = '新產品開發申請單'
            pro_info_obj['bu']           = pro_item['bu']
            pro_info_obj['product_name'] = pro_item['product_name']
            pro_info_obj['member_cname'] = pro_item['member_cname']
            pro_info_obj['apply_date']   = pro_item['apply_date']
            pro_info_obj['inserted_at']  = pro_item['inserted_at']
            #pro_info_obj['status']       = process_form_status(pro_item['form_no'])
            list_info.append(pro_info_obj)


      # RD內部開案
    internal_project_model = internal_project_form(mongo.db)
    result__internal= internal_project_model.get_internal_project_info_by_member(applicant)
    if len(result__internal) > 0:
        for int_item in result__internal:
           
           
            int_info_obj = {}
            int_info_obj['uuid']         = int_item['uuid']
            int_info_obj['form_no']      = int_item['form_no']
            int_info_obj['project_no']   = int_item['project_no']
            int_info_obj['project_name'] = int_item['project_name']
            int_info_obj['project_type'] = '內部開案單'
            int_info_obj['bu']           = int_item['bu']
            int_info_obj['product_name'] = int_item['product_name']
            int_info_obj['member_cname'] = int_item['member_cname']
            int_info_obj['apply_date']   = int_item['apply_date']
            pro_info_obj['inserted_at']  = pro_item['inserted_at']
            #pro_info_obj['status']       = process_form_status(pro_item['form_no'])
            list_info.append(int_info_obj)

    # Layout 
    layout_model = layout_form(mongo.db)   
    result_layout = layout_model.get_layout_info_by_member(applicant)
    
    if len(result_layout) > 0:
        for layout_item in result_layout:
          
            layout_info_obj = {}
            layout_info_obj['uuid']         = layout_item['uuid']
            layout_info_obj['form_no']      = layout_item['form_no']
            layout_info_obj['project_no']   = layout_item['project_no']
            layout_info_obj['project_name'] = layout_item['project_name']
            layout_info_obj['project_type'] = 'Layout申請工程規格聯絡單'
            layout_info_obj['bu']           = layout_item['bu']
            layout_info_obj['product_name'] = layout_item['product_name']
            layout_info_obj['member_cname'] = layout_item['member_cname']
            layout_info_obj['apply_date']   = layout_item['apply_date']
            layout_info_obj['inserted_at']  = layout_item['inserted_at']
            #layout_info_obj['status']       = process_form_status(layout_item['form_no'])
            list_info.append(layout_info_obj)
    
    # PCB
    pcb_model = pcb_form(mongo.db)
    result_pcb =  pcb_model.get_pcb_info_by_member(applicant)
    if len(result_pcb) > 0:
        for pcb_item in result_pcb:
            #print(pcb_item)
            
            pcb_info_obj = {}
            pcb_info_obj['uuid']         = pcb_item['uuid']
            pcb_info_obj['form_no']      = pcb_item['form_no']
            pcb_info_obj['project_no']   = pcb_item['project_no']
            pcb_info_obj['project_name'] = pcb_item['project_name']
            pcb_info_obj['project_type'] = 'PCB打樣申請工程規格聯絡單'
            pcb_info_obj['bu']           = pcb_item['bu']
            pcb_info_obj['product_name'] = pcb_item['product_name']
            pcb_info_obj['member_cname'] = pcb_item['member_cname']
            pcb_info_obj['apply_date']   = pcb_item['apply_date']
            pcb_info_obj['inserted_at']   = pcb_item['inserted_at']
            #pcb_info_obj['status']       = process_form_status(pcb_item['form_no'])
            list_info.append(pcb_info_obj)

    # for info in list_info:
    #     print(info['form_no'])
    
    # 過濾重複 form_no 值
    unique_form_nos = set()
    filtered_data = []

    for item in list_info:
        form_no = item["form_no"]
        if form_no not in unique_form_nos:
            unique_form_nos.add(form_no)
            item['status'] = process_form_status(form_no)
            filtered_data.append(item)

    #print(filtered_data)
    return filtered_data




# 取得目前表單執行最新狀況
@blue_form_list.route("/api/v0/db/data/form_flow_last_status/", methods=['GET'])
def get_form_flow_step_last_status():
    
    pam_form_no = request.args.get('form_no')
    
    flow_log_model = form_flow(mongo.db)
    msg, result_log = flow_log_model.get_form_flow({"form_no": pam_form_no })
    
    result_log.sort(key=lambda x: x['fs_code'], reverse=True)
    print(result_log[0])
    
    flow_step_model = Flow_Step(mongo.db)
    res = flow_step_model.find_one_by_code(result_log[0]['fs_code'])
    print(result_log[0]['fs_code'])
    
    pam_group  = result_log[0]['fs_code'][5:7]
    print(pam_group)
    
    pam_count = int(result_log[0]['fs_code'][7:9])
    print(pam_count)
    
    print(result_log[0]['fs_code'][2:5])
    
    pam_class = "new_technology"
    if result_log[0]['fs_code'][2:5] == "pro":
        pam_class = "new_project"
    elif result_log[0]['fs_code'][2:5] == "lay":
        pam_class = "layout"
    elif result_log[0]['fs_code'][2:5] == "pcb":
        pam_class = "pcb"
    elif result_log[0]['fs_code'][2:5] == "int":
        pam_class = "int"
        
    step_count = flow_step_model.find_step_count_by_group(pam_class, pam_group)
    
    print('***** count *****')
    print(step_count)
    print(pam_count)
    print(result_log[0]['status'])
    
    pam_status = "未簽核"
    if step_count <= pam_count:
        if result_log[0]['status'] == "核准" or result_log[0]['status'] == "開案":
            pam_status = "已簽核"
   
    res_obj = {}
    res_obj['step_cname']  = res['cname']
    res_obj['form_no']     = pam_form_no
    res_obj['form_status'] = pam_status
    res_obj['form_class']  = pam_class
    return res_obj




def process_form_status(pam_no):
    
    pam_form_no = pam_no
    
    flow_log_model = form_flow(mongo.db)
    msg, result_log = flow_log_model.get_form_flow({"form_no": pam_form_no })
    #print('****************')
    #print(len(result_log))
    
    if len(result_log) > 0:
        result_log.sort(key=lambda x: x['fs_code'], reverse=True)
        print(result_log[0])

        flow_step_model = Flow_Step(mongo.db)
        res = flow_step_model.find_one_by_code(result_log[0]['fs_code'])
        #print(result_log[0]['fs_code'])
        
        pam_group  = result_log[0]['fs_code'][5:7]
        #print(pam_group)
        
        pam_count = int(result_log[0]['fs_code'][7:9])
        #print(pam_count)

        pam_class = "new_technology"
        if result_log[0]['fs_code'][2:5] == "pro":
            pam_class = "new_project"
        elif result_log[0]['fs_code'][2:5] == "lay":
            pam_class = "layout"
        elif result_log[0]['fs_code'][2:5] == "pcb":
            pam_class = "pcb"
        elif result_log[0]['fs_code'][2:5] == "int":
            pam_class = "internal_project"


        step_count = flow_step_model.find_step_count_by_group(pam_class, pam_group)
        
        print('***** count *****')
        print(step_count)
        print(pam_count)
        
        pam_status = "未簽核"
        if step_count <= pam_count:
            if result_log[0]['status'] == "核准" or result_log[0]['status'] == "開案":
                pam_status = "已簽核"
                
            elif result_log[0]['status'] == "退回":
                pam_status = "退回"
        return pam_status

    else:
        return "未簽核"




# 取得目前表單所有 log資料(用於顯示到達哪個歷程)
@blue_form_list.route("/api/v0/db/data/form_flow_step/log/all/", methods=['GET'])
def get_form_flow_step_log_all():
    
    param = request.args.get('form_no')
    print(param)

    list_info = []
    flow_log_model = form_flow(mongo.db)
    msg, result_log = flow_log_model.get_form_flow({"form_no": param })
    return result_log



# 取得目前表單到達哪個關卡(index)
@blue_form_list.route("/api/v0/db/data/form_flow_step/log/last/index/", methods=['GET'])
def get_form_flow_step_log_last_index():
    
    param = request.args.get('form_no')
    print(param)

    flow_log_model = form_flow(mongo.db)
    msg, result_log = flow_log_model.get_form_flow({"form_no": param })
    if len(result_log) > 0:
        result_log.sort(key=lambda x: x['fs_code'], reverse=True)
        print(result_log[0])
        
        pam_project_no = result_log[0]['project_no']
        
        pam_group  = result_log[0]['fs_code'][5:7]
        
        pam_class = "new_technology"
        if result_log[0]['fs_code'][2:5] == "pro":
            pam_class = "new_project"
        elif result_log[0]['fs_code'][2:5] == "lay":
            pam_class = "layout"
        elif result_log[0]['fs_code'][2:5] == "pcb":
            pam_class = "pcb"
        elif result_log[0]['fs_code'][2:5] == "int":
            pam_class = "internal_project"
            
        flow_step_model = Flow_Step(mongo.db)
        step_count = flow_step_model.find_step_count_by_group(pam_class, pam_group)
        pam_count = int(result_log[0]['fs_code'][7:9]) + 1
        
        if pam_count >= step_count:
            pam_count = step_count
        print(pam_count)
        
        tempNumber = '{0:02d}'.format(pam_count)
        print(tempNumber)
        
        tempClass = result_log[0]['fs_code'][2:5]
        print(tempClass)
        
        tempCode = 'fs{}{}{}'.format( tempClass, pam_group, tempNumber )
        print(tempCode)
        
        res = flow_step_model.find_one_by_code(tempCode)
        
        res_obj = {}
        res_obj['current_index'] = pam_count
        res_obj['step_cname'] = res['cname']
        
        if pam_class == "new_technology":
            if res['cname'] == 'RD主管指派': 
                res_obj['link'] = 'http://{}/page/v0/new_technology_task/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no , param)
            elif res['cname'] == 'RD主管核准':
                res_obj['link'] = 'http://{}/page/v0/new_technology_review/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param )
            elif res['cname'] == 'PM核准':
                res_obj['link'] = 'http://{}/page/v0/new_technology_result/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
                
        elif pam_class == "new_project":
            if res['cname'] == 'PM主管核准':
                res_obj['link'] = 'http://{}/page/v0/new_project_approve/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
            elif res['cname'] == 'RD主管指派':
                res_obj['link'] = 'http://{}/page/v0/new_project_task/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
            elif res['cname'] == 'RD主管核准':
                res_obj['link'] = 'http://{}/page/v0/new_project_review/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
                
        elif pam_class == "layout":
            if res['cname'] == 'RD主管核准':
                res_obj['link'] = 'http://{}/page/v0/layout_result/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
            
        elif pam_class == "pcb":
            if res['cname'] == 'RD主管核准':
                res_obj['link'] = 'http://{}/page/v0/pcb_result/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)
                
        elif pam_class == "internal_project":
            if res['cname'] == 'RD主管核准':
                res_obj['link'] = 'http://{}/page/v0/new_project_review/?project_no={}&form_no={}'.format(DOMAIN_PATH, pam_project_no, param)


    return res_obj