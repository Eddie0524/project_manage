from flask import Blueprint
from flask import Response
from flask import request
from flask import render_template
from flask import redirect
from flask import url_for
from apps.settings import DOMAIN_PATH
from apps.exts import mongo
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_member      import Member




blue_layout_feedback = Blueprint('blue_layout_feedback', __name__)



def init_layout_feedback(app):
    app.register_blueprint(blueprint=blue_layout_feedback)



@blue_layout_feedback.route("/page/v0/layout_feedback/", methods=['GET'])
def layout_feedback_index():
    
    project_no = request.args.get('project_no')
    mode = 'layout_feedback'
    
    # check cookie
    account  = request.cookies.get('account' )
    avatar   = request.cookies.get('avatar'  )
    member   = request.cookies.get('eName'   )
    cname    = request.cookies.get('cName'   )
    sex      = request.cookies.get('sex'     )
    cname    = request.cookies.get('cName'   )
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

        return render_template(
            'layout_feedback.html',
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            PHOTO=avatar,
            USER_CNAME=cname,
            GROUP_NO=group_no,
            IS_LEADER=isleader,
            ACCOUNT=account)