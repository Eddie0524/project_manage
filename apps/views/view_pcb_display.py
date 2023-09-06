from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import SERVER_IP
from apps.settings import FILE_PATH
import json
import time
import os
from werkzeug.utils import secure_filename
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import UPLOAD_FOLDER
from apps.settings import MAIL_RECEIVER
from flask import send_from_directory
import urllib.parse
import uuid
import datetime
from apps.exts import mongo
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_layout_form import layout_form
from apps.models.model_pcb_form import pcb_form
from apps.models.model_member   import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname
import random




blue_pcb_display = Blueprint('blue_pcb_display', __name__)



def init_pcb_display(app):
    app.register_blueprint(blueprint=blue_pcb_display)




@blue_pcb_display.route("/page/v0/pcb_display/", methods=['GET'])
def pcb_display_index():
    
    mode = "pcb_display"
    
    form_no    = request.args.get('form_no')
    project_no = request.args.get('project_no')

    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
    #group_no = request.cookies.get('group_no')
    #department = request.cookies.get('department')


    if account is None:
        #return redirect(url_for('blue_main.login_fun'))
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no ))
    else:

        # 判斷是否為主管
        member_model = Member(mongo.db)
        isleader = member_model.check_leader_by_cname(cname)
        # 取得部門區分
        group_no   = member_model.find_group_no_by_cname(cname)
        department = member_model.find_department_by_cname(cname)

        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
        
        pcb_form_model = pcb_form(mongo.db)
        param = {
            'project_no'    : project_no,
            'form_no'       : form_no
        }
       
        pcb_model = pcb_form_model.get_pcb_form(param)
        print(pcb_model)
        print(department)

        return render_template(
            'pcb_display.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            ACCOUNT=account,
            GROUP_NO=group_no,
            DEPARTMENT=department,
            RECEIVER=MAIL_RECEIVER,
            IS_LEADER=isleader,
            PCB_MODEL=pcb_model
        )