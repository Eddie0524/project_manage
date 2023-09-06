from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
import json
import time
import uuid
from apps.exts import mongo
import datetime
from apps.models.model_member      import Member
from apps.models.model_new_project_form import new_project_form
from apps.models.model_new_project_task import new_project_task
from apps.models.model_internal_project_form import internal_project_form




blue_internal_project_display = Blueprint('blue_internal_project_display', __name__)



def init_internal_project_display(app):
    app.register_blueprint(blueprint=blue_internal_project_display)



@blue_internal_project_display.route("/page/v0/internal_project_display/", methods=['GET'])
def internal_project_display_index():
    
    mode = "internal_project_display"

    form_no    = request.args.get('form_no')
    project_no = request.args.get('project_no')

    # check cookie
    account    = request.cookies.get('account' )
    avatar     = request.cookies.get('avatar'  )
    member     = request.cookies.get('eName'   )
    sex        = request.cookies.get('sex'     )
    cname      = request.cookies.get('cName'   )
    group_no   = request.cookies.get('group_no')
    department = request.cookies.get('department')
    #print(group_no)

    if account is None:
        #return redirect(url_for('blue_main.login_fun'))
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no, FORM_NO=form_no ))
    else:
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
                
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)

        # internal_project_model = new_project_form(mongo.db)
        internal_project_model = internal_project_form(mongo.db)
        param1 = {
            'project_no' : project_no,
            'form_no': form_no
        }
        #internal_model = internal_project_model.get_new_project_form(param1)
        internal_model=internal_project_model.get_internal_project_form(param1)

        print(internal_model)
        print(department)
        
        param2 = {
            'project_no' : project_no,
        }
        new_project_task_model = new_project_task(mongo.db)
        task_model = new_project_task_model.get_new_project_task(param2)
        

        return render_template(
            'internal_project_display.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            DEPARTMENT=department,
            PROJECT_NO=project_no,
            IS_LEADER=isleader,
            TASK_MODEL=task_model,
            INTERNAL_MODEL=internal_model)