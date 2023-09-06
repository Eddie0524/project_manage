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
from apps.models.model_new_project_form import new_project_form_log
from apps.models.model_new_project_form import modify_new_project_form
from apps.models.model_new_technology_form import new_technology_form
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from apps.models.model_member import Member
import random



blue_new_project_edit = Blueprint('blue_new_project_edit', __name__)



def init_new_project_edit(app):
    app.register_blueprint(blueprint=blue_new_project_edit)



@blue_new_project_edit.route("/page/v0/new_project_edit/", methods=['GET'])
def new_project_edit_index():
    
   
    form_no    = request.args.get('form_no')
    project_no = request.args.get('project_no')
    mode = "new_project_edit"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(avatar)
    
    if account is None:
        return redirect(url_for('blue_main.login_fun'))
    else:
        if avatar == "":
            if sex == "male":
                avatar = "/assets/avatar/man2.png"
            else:
                avatar = "/assets/avatar/woman2.png"
        
      

        new_project_form_model = new_project_form(mongo.db)
        param = {
            'project_no' : project_no
        }
        new_project_model = new_project_form_model.get_new_project_form(param)       
  
    

        return render_template(
            'new_project_edit.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            RECEIVER = MAIL_RECEIVER,
            NEW_PROJECT_MODEL=new_project_model)




    


    
