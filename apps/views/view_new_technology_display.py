from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.settings import SMTP_INFO
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import UPLOAD_FOLDER
from apps.settings import MAIL_RECEIVER
from flask import send_from_directory
from werkzeug.utils import secure_filename
import urllib.parse
import json
import time
import uuid
from apps.exts import mongo
from apps.models.model_new_technology_form import new_technology_form
from apps.models.model_new_technology_review import new_technology_review
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import random




blue_new_technology_display = Blueprint('blue_new_technology_display', __name__)


def init_new_technology_display(app):
    app.register_blueprint(blueprint=blue_new_technology_display)




@blue_new_technology_display.route("/page/v0/new_technology_display/", methods=['GET'])
def new_technology_display_index():
    
    mode = "new_technology_display"
    
    project_no = request.args.get('project_no')
    form_no    = request.args.get('form_no')

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    print("XXXXXXXXXXXX")
    print(project_no)

    if account is None:
        #return redirect(url_for('blue_main.login_fun'))
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, PROJECT_NO=project_no ))
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
        
        new_technology_form_model = new_technology_form(mongo.db)
        new_technology_form_review_model = new_technology_review(mongo.db)
        param = { 'project_no' :   project_no }
        new_technology_model = new_technology_form_model.get_new_technology_form(param)
        new_technology_review_model = new_technology_form_review_model.get_new_technology_review(param)
        #print(new_technology_review_model)
                
        return render_template(
            'new_technology_display.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            RECEIVER=MAIL_RECEIVER,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            PROJECT_NO=project_no,
            NEW_TECH_MODEL=new_technology_model,
            NEW_TECH_REVIEW_MODEL=new_technology_review_model)