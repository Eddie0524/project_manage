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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname
from apps.models.model_pcb_result import pcb_result
from apps.models.model_pcb_form import pcb_form



blue_pcb_edit = Blueprint('blue_pcb_edit', __name__)



def init_pcb_edit(app):
    app.register_blueprint(blueprint=blue_pcb_edit)



@blue_pcb_edit.route("/page/v0/pcb_edit/", methods=['GET'])
def pcb_result_index():

    form_no = request.args.get('form_no')
    button_status = request.args.get('status')
    project_no = request.args.get('project_no')
    mode = "pcb_edit"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(cname)
    #print(avatar)
    #print(form_code)
    

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no))
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

        pcb_form_model = pcb_form(mongo.db)
        param = {
            'project_no' : project_no,
            'form_no'    : form_no
        }
       
        pcb_form_model = pcb_form_model.get_pcb_form(param)
        print(pcb_form_model)
            
        return render_template(
            'pcb_edit.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER=MAIL_RECEIVER,
            GROUP_NO=group_no,
            BUTTON_STATUS=button_status,
            IS_LEADER=isleader,
            PCB_FORM_MODEL=pcb_form_model)
    

