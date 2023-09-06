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
from apps.models.model_new_project_form import new_project_form
from apps.models.model_new_technology_task import new_technology_task
from apps.models.model_new_project_task import new_project_task
from apps.views.view_member import get_cname_by_organize
from apps.views.view_member import get_group_no_by_cname
from apps.models.model_member import Member




blue_project_list = Blueprint('blue_project_list', __name__)


def init_blue_project_list(app):
    app.register_blueprint(blueprint=blue_project_list)



@blue_project_list.route("/page/v0/project_list/", methods=['GET'])
def project_list_index():

    project_no = request.args.get('project_no')
    mode = "project_list"

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
        isleader = member_model.check_leader_by_cname(cname)
        print(isleader)
        
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)

        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        return render_template(
            'project_list.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            IS_LEADER=isleader,
            GROUP_NO=group_no,
            PROJECT_NO=project_no)



# 個人相關列表(一般查詢)
@blue_project_list.route("/api/v0/db/data/project_list/", methods=['GET'])
def get_project_list():

    cname = request.args.get('user')

    # 取得新技術評估專案
    tec_task_model  = new_technology_task(mongo.db)
    tec_task_result = tec_task_model.get_new_technology_forms_by_member(cname)
    #print(tec_task_result)

    # 取得新開案專案
    pro_model = new_project_task(mongo.db)
    pro_result = pro_model.get_new_project_task_by_member(cname)
    print(pro_result)

    result_list = []
    tec_form_model = new_technology_form(mongo.db)
    pro_form_model = new_project_form(mongo.db)
    
    
    for tec_mod in tec_task_result:
        
        tec_form_result    = tec_form_model.get_new_tech_project_apply_date(tec_mod['project_no'])
        tec_form_no_result = tec_form_model.get_new_tech_project_form_no(tec_mod['project_no'])
        tec_spec_result    = tec_form_model.get_new_tech_project_spec_describle(tec_mod['project_no'])

        dir_tec_mod = {}
        dir_tec_mod['uuid']                 = tec_mod['uuid']
        dir_tec_mod['project_no']           = tec_mod['project_no']
        dir_tec_mod['project_name']         = tec_mod['project_name']
        dir_tec_mod['project_type']         = "新技術評估"
        dir_tec_mod['bu']                   = tec_mod['bu']
        dir_tec_mod['form_no']              = tec_form_no_result
        dir_tec_mod['spec_describe']        = tec_spec_result
        dir_tec_mod['task']                 = tec_mod['task']
        dir_tec_mod['mile_stone']           = tec_mod['mile_stone']
        dir_tec_mod['status']               = tec_mod['status']
        dir_tec_mod['expected_start_date']  = tec_mod['expected_start_date']
        dir_tec_mod['expected_finish_date'] = tec_mod['expected_finish_date']
        dir_tec_mod['apply_date']           = tec_form_result
        dir_tec_mod['member_cname'        ] = cname #tec_model['member_cname'     ]
        dir_tec_mod['reason']               = tec_mod['reason']
        dir_tec_mod['inserted_at']          = tec_mod['inserted_at']
        result_list.append(dir_tec_mod)
        
    for pro_mod in pro_result:
        
        pro_form_result    = pro_form_model.get_new_project_apply_date(pro_mod['project_no'])
        pro_form_no_result = pro_form_model.get_new_project_form_no(pro_mod['project_no'])
        pro_spec_result    = pro_form_model.get_new_project_spec_describle(pro_mod['project_no'])
        
        dir_pro_mod = {}
        dir_pro_mod['uuid']                 = pro_mod['uuid']
        dir_pro_mod['project_no']           = pro_mod['project_no']
        dir_pro_mod['project_name']         = pro_mod['project_name']
        dir_pro_mod['project_type']         = "新開案"
        dir_pro_mod['bu']                   = pro_mod['bu']
        dir_pro_mod['form_no']              = pro_form_no_result
        dir_pro_mod['spec_describe']        = pro_spec_result
        dir_pro_mod['task']                 = pro_mod['task']
        dir_pro_mod['mile_stone']           = pro_mod['mile_stone']
        dir_pro_mod['status']               = pro_mod['status']
        dir_pro_mod['expected_start_date']  = pro_mod['expected_start_date']
        dir_pro_mod['expected_finish_date'] = pro_mod['expected_finish_date']
        dir_pro_mod['apply_date']           = pro_form_result
        dir_pro_mod['member_cname'        ] = cname #tec_model['member_cname'     ]
        dir_pro_mod['reason']               = pro_mod['reason']
        dir_pro_mod['inserted_at']          = pro_mod['inserted_at']
        result_list.append(dir_pro_mod)

    print(result_list)
  
    strJson = { 'result': 'ok', 'code':'', 'msg': '讀取專案資料成功', 'data': result_list }
    return Response(json.dumps(strJson), mimetype='application/json'), 200






# 部門全部列表(PM/RD 主管查詢)
@blue_project_list.route("/api/v0/db/data/project_list/all/", methods=['GET'])
def get_project_list_all():
    
    organize = request.args.get('organize')
    print(organize)
    #  先取得相關人員
    member_list = get_cname_by_organize(organize)
    print(member_list)
    
    result_list = []
    # 依照人員將資料找出
    
    for cname in member_list:
        
        # 取得新技術評估專案
        tec_task_model = new_technology_task(mongo.db)
        tec_task_result = tec_task_model.get_new_technology_forms_by_member(cname)
    
        # 取得新開案專案
        pro_task_model = new_project_task(mongo.db)
        pro_task_result = pro_task_model.get_new_project_task_by_member(cname)
        
        tec_form_model = new_technology_form(mongo.db)
        pro_form_model = new_project_form(mongo.db)
        
        for tec_mod in tec_task_result:
            
            tec_form_result    = tec_form_model.get_new_tech_project_apply_date(tec_mod['project_no'])
            tec_form_no_result = tec_form_model.get_new_tech_project_form_no(tec_mod['project_no'])
            tec_spec_result    = tec_form_model.get_new_tech_project_spec_describle(tec_mod['project_no'])
            
            dir_tec_mod = {}
            dir_tec_mod['uuid'                ] = tec_mod['uuid'                ]
            dir_tec_mod['project_no'          ] = tec_mod['project_no'          ]
            dir_tec_mod['project_name'        ] = tec_mod['project_name'        ]
            dir_tec_mod['project_type'        ] = "新技術評估"
            dir_tec_mod['bu'                  ] = tec_mod['bu'                  ]
            dir_tec_mod['form_no'             ] = tec_form_no_result
            dir_tec_mod['spec_describe'       ] = tec_spec_result
            dir_tec_mod['task'                ] = tec_mod['task'                ]
            dir_tec_mod['mile_stone'          ] = tec_mod['mile_stone'          ]
            dir_tec_mod['status'              ] = tec_mod['status'              ]
            dir_tec_mod['expected_start_date' ] = tec_mod['expected_start_date' ]
            dir_tec_mod['expected_finish_date'] = tec_mod['expected_finish_date']
            dir_tec_mod['member_cname'        ] = cname #tec_model['member_cname'     ]
            dir_tec_mod['apply_date'          ] = tec_form_result
            dir_tec_mod['inserted_at']          = tec_mod['inserted_at']
            result_list.append(dir_tec_mod)
        
        for pro_mod in pro_task_result:
            
            pro_form_result    = pro_form_model.get_new_project_apply_date(pro_mod['project_no'])
            pro_form_no_result = pro_form_model.get_new_project_form_no(pro_mod['project_no'])
            pro_spec_result    = pro_form_model.get_new_project_spec_describle(pro_mod['project_no'])
            
            dir_pro_mod = {}
            dir_pro_mod['uuid']                 = pro_mod['uuid']
            dir_pro_mod['project_no']           = pro_mod['project_no']
            dir_pro_mod['project_name']         = pro_mod['project_name']
            dir_pro_mod['project_type']         = "新開案"
            dir_pro_mod['bu']                   = pro_mod['bu']
            dir_pro_mod['form_no']              = pro_form_no_result
            dir_pro_mod['spec_describe']        = pro_spec_result
            dir_pro_mod['task']                 = pro_mod['task']
            dir_pro_mod['mile_stone']           = pro_mod['mile_stone']
            dir_pro_mod['status']               = pro_mod['status']
            dir_pro_mod['expected_start_date']  = pro_mod['expected_start_date']
            dir_pro_mod['expected_finish_date'] = pro_mod['expected_finish_date']
            dir_pro_mod['member_cname'        ] = cname #tec_model['member_cname'     ]
            dir_pro_mod['reason']               = pro_mod['reason']
            dir_pro_mod['apply_date']           = pro_form_result
            dir_pro_mod['inserted_at']          = pro_mod['inserted_at']
            result_list.append(dir_pro_mod)

    print("----------------------")
    print(result_list)
    
    
    strJson = { 'code': 0, 'msg': '讀取專案資料成功', 'count': len(result_list),'data': result_list }
    return Response(json.dumps(strJson), mimetype='application/json'), 200