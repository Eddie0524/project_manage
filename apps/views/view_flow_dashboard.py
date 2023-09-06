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




blue_flow_dashboard = Blueprint('blue_flow_dashboard', __name__)



def init_blue_flow_dashboard(app):
    app.register_blueprint(blueprint=blue_flow_dashboard)


@blue_flow_dashboard.route("/page/v0/flow_dashboard/", methods=['GET'])
def flow_dashboard_index():

    #form_no = request.args.get('form_no')
    mode = "flow_dashboard"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.assign_login_fun', MODE=mode, FORM_NO='' ))
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
            'flow_dashboard.html',
            DOMAIN_PATH=DOMAIN_PATH,
            MODE=mode,
            USER=member,
            USER_CNAME=cname,
            PHOTO=avatar,
            IS_LEADER=isleader,
            ACCOUNT=account)