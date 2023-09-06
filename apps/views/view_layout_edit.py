from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import MAIL_RECEIVER
from apps.models.model_layout_form import layout_form
from apps.exts import mongo
import uuid
import datetime
import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_layout_result import layout_result
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import random
import time

blue_layout_edit = Blueprint('blue_layout_edit', __name__)



def init_layout_edit(app):
    app.register_blueprint(blueprint=blue_layout_edit)



@blue_layout_edit.route("/page/v0/layout_edit/", methods=['GET'])
def layout_edit_index():
    
    button_status = request.args.get('status')
    project_no    = request.args.get('project_no')
    form_no       = request.args.get('form_no')
    
    mode = 'layout_edit'
    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    cname   = request.cookies.get('cName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName')
    #group_no = request.cookies.get('group_no')
    
    #print(account)
    #print(avatar)
    
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO=project_no))

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
        
        layout_form_model = layout_form(mongo.db)
        param = {
            'project_no'    : project_no,
            'form_no'       :form_no
        }
       
        layout_form_model = layout_form_model.get_layout_form(param)

        return render_template(
            'layout_edit.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            GROUP_NO=group_no,
            ACCOUNT=account,
            RECEIVER=MAIL_RECEIVER,
            BUTTON_STATUS=button_status,
            IS_LEADER=isleader,
            LAYOUT_FORM_MODEL=layout_form_model)









