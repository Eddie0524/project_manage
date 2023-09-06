from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import MAIL_RECEIVER
import json
import time
import uuid
from apps.exts import mongo
import datetime
from apps.models.model_new_project_form import new_project_form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import random



blue_new_project_display = Blueprint('blue_new_project_display', __name__)



def init_new_project_display(app):
    app.register_blueprint(blueprint=blue_new_project_display)



@blue_new_project_display.route("/page/v0/new_project_display/", methods=['GET'])
def new_project_display_index():
    
    mode = "new_project_display"
    
    form_no    = request.args.get('form_no')
    project_no = request.args.get('project_no')

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    if account is None:
        #return redirect(url_for('blue_main.login_fun'))
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no ))
    else:
        
        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no = member_model.find_group_no_by_cname(cname)
        
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"

        new_project_form_model = new_project_form(mongo.db)
        param = { 'project_no' : project_no }
       
        new_project_model = new_project_form_model.get_new_project_form(param)
        print(new_project_model)

        return render_template(
            'new_project_display.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER = MAIL_RECEIVER,
            IS_LEADER=isleader,
            NEW_PROJECT_MODEL=new_project_model)