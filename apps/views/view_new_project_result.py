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
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_new_project_form import new_project_form
from apps.models.model_member import Member
from apps.views.view_member   import get_cname_by_organize
from apps.views.view_member   import get_organize_by_cname


blue_new_project_result = Blueprint('blue_new_project_result', __name__)


def init_new_project_result(app):
    app.register_blueprint(blueprint=blue_new_project_result)



@blue_new_project_result.route("/page/v0/new_project_result/", methods=['GET'])
def new_project_result_index():

    project_no = request.args.get('project_no')
    form_no    = request.args.get('form_no')
    
    mode = 'new_project_result'

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(cname)
    #print(avatar)
    #print(form_no)

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO=form_no ))
    else:
        
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)
        
        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)
       
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
                
        return render_template(
            'new_project_result.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            FORM_NO=form_no,
            IS_LEADER=isleader,
            NEW_PROJECT_MODEL=new_project_model)