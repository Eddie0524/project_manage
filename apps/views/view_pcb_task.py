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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
from apps.views.view_member     import get_cname_by_organize
from apps.views.view_member     import get_organize_by_cname




blue_pcb_task = Blueprint('blue_pcb_task', __name__)


def init_pcb_task(app):
    app.register_blueprint(blueprint=blue_pcb_task)



@blue_pcb_task.route("/page/v0/pcb_task/", methods=['GET'])
def pcb_task_index():

    #leader = request.args.get('leader')
    form_no = request.args.get('form_no')
    
    mode = 'pcb_task'

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    # print(account)
    # print(cname)
    # print(avatar)
    # print(form_no)

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO=form_no ))
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
                
        return render_template(
            'pcb_task.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_cname=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            FORM_NO=form_no)