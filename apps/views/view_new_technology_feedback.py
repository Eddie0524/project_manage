from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.exts import mongo
from apps.models.model_new_technology_task import new_technology_task
import json
import time
from werkzeug.utils import secure_filename
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import UPLOAD_FOLDER
from flask import send_from_directory
import urllib.parse
import os
from apps.settings import MAIL_RECEIVER
from apps.models.model_member      import Member
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname



blue_new_technology_feedback = Blueprint('blue_new_technology_feedback', __name__)


def init_new_technology_feedback(app):
    app.register_blueprint(blueprint=blue_new_technology_feedback)



@blue_new_technology_feedback.route("/page/v0/new_technology_feedback/", methods=['GET'])
def new_technology_feedback_index():
    
    # project_no = request.args.get('project_no')
    mode = "new_technology_feedback"
    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    cname   = request.cookies.get('cName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName')
    #group_no = request.cookies.get('group_no')
    
    # print(account)
    # print(avatar)
    
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode))

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
            'new_technology_feedback.html',
            DOMAIN_PATH=DOMAIN_PATH,
            MODE=mode,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            GROUP_NO=group_no,
            ACCOUNT=account,
            IS_LEADER=isleader,
            RECEIVER=MAIL_RECEIVER)


# 取得跟某人有關的所有評估案列表
@blue_new_technology_feedback.route("/api/v0/db/new_technology_forms/by/member/", methods=['GET'])
def get_new_technology_forms_by_member():
    
    member_cname = request.args.get('user')
    print(member_cname)
    task_model = new_technology_task(mongo.db)
    result = task_model.get_new_technology_forms_by_member(member_cname)
    strJson = { 'code': 0, 'msg':'', 'count': len(result), 'data': result }
    return Response(json.dumps(strJson), mimetype='application/json'), 200






def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS



def convert_bytes_to_mb(bytes):
    mb = bytes / (1024 * 1024)  # 1 MB = 1024 * 1024 bytes
    return mb



@blue_new_technology_feedback.route('/upload/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        project_no = request.args.get('project_no')
        file = request.files['file']
  
        #建立專案名稱資料夾
        folderpath = os.path.join(UPLOAD_FOLDER, project_no + "\\")
        if not os.path.exists(folderpath):
            os.makedirs(folderpath)

        if file and allowed_file(file.filename):
            filename = secure_filename(urllib.parse.quote(file.filename.encode('utf-8')))
            print(filename)
            #print(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
            # 儲存檔案
            #file.save(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
            file.save(os.path.join(folderpath + "\\" + file.filename))
            #file_size_bytes = os.path.getsize(os.path.join(UPLOAD_FOLDER, "form_no" + "\\" + file.filename))
            file_size_bytes = os.path.getsize(os.path.join(folderpath + "\\" + file.filename))
            print(file_size_bytes)
            file_size_mb = convert_bytes_to_mb(file_size_bytes)
            print(file_size_mb)
            strMsg = '[ {} ], 檔案大小 : {}  MB 上傳成功'.format(file.filename, round(file_size_mb, 2))
            strJson = { 'result': 'ok', 'code':'', 'data': { 'msg': strMsg  }}

    return Response(json.dumps(strJson))


