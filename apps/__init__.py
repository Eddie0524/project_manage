from flask import Flask
from apps.exts import init_exts
from apps.views.view_main   import init_blue_main
from apps.views.view_member import init_blue_member

from apps.views.view_new_technology_form     import init_new_technology_form
from apps.views.view_new_technology_task     import init_new_technology_task
from apps.views.view_new_technology_feedback import init_new_technology_feedback
from apps.views.view_new_technology_review   import init_new_technology_review
from apps.views.view_new_technology_result   import init_new_technology_result
from apps.views.view_new_technology_display  import init_new_technology_display

from apps.views.view_new_project_form      import init_new_project_form
from apps.views.view_new_project_approve   import init_new_project_approve
from apps.views.view_new_project_task      import init_new_project_task
from apps.views.view_new_project_feedback  import init_new_project_feedback
from apps.views.view_new_project_review    import init_new_project_review
from apps.views.view_new_project_result    import init_new_project_result
from apps.views.view_new_project_display   import init_new_project_display

from apps.views.view_layout_form     import init_layout_form
from apps.views.view_layout_task     import init_layout_task
from apps.views.view_layout_feedback import init_layout_feedback
from apps.views.view_layout_result   import init_layout_result
from apps.views.view_layout_display  import init_layout_display

from apps.views.view_pcb_form     import init_pcb_form
from apps.views.view_pcb_task     import init_pcb_task
from apps.views.view_pcb_feedback import init_pcb_feedback
from apps.views.view_pcb_result   import init_pcb_result
from apps.views.view_pcb_display  import init_pcb_display

from apps.views.view_task_milestone import init_blue_task_milestone
from apps.views.view_status         import init_blue_status
from apps.views.view_milestone      import init_blue_milestone
from apps.views.view_task           import init_blue_task
from apps.views.view_feedback_rule  import init_blue_feedback_rule
from apps.views.view_email          import init_blue_email
from apps.views.view_attach         import init_blue_attach

from apps.views.view_end_project_reason import init_blue_end_project_reason
from apps.views.view_project_status     import init_blue_project_status
from apps.views.view_form_sn            import init_blue_form_sn
from apps.views.view_all_kinds_reason   import init_blue_all_kinds_reason
from apps.settings import UPLOAD_FOLDER

from apps.views.view_swagger import init_blue_swagger
from apps.views.view_flow_dashboard import init_blue_flow_dashboard

from apps.settings import MONGODB_PATH
from apps.views.view_bpm_flow import init_bpm_flow
from apps.views.view_project_list import init_blue_project_list
from apps.views.view_form_list import init_blue_form_list
from apps.views.view_form_flow import init_form_flow
from apps.views.view_flow_step import init_blue_flow_step
from apps.views.view_internal_project_task import init_internal_project_task
from apps.views.view_new_project_edit import init_new_project_edit

from apps.views.view_new_technology_edit import init_new_technology_edit
from apps.views.view_layout_edit import init_layout_edit
from apps.views.view_pcb_edit import init_pcb_edit
from apps.views.view_internal_project_form import init_internal_project_form
from apps.views.view_internal_project_display import init_internal_project_display
from apps.views.view_internal_project_approve import init_internal_project_approve




def create_app():
    
    app = Flask(__name__)
    app.config['MONGO_URI'] = MONGODB_PATH
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 4096 * 1024 * 1024  # 64MB

  
    init_blue_main(app)
    init_blue_member(app)
    
    init_new_technology_form(app)
    init_new_technology_task(app)
    init_new_technology_review(app)
    init_new_technology_feedback(app)
    init_new_technology_result(app)
    init_new_technology_display(app)
    
    init_new_project_form(app)
    init_new_project_approve(app)
    init_new_project_task(app)
    init_new_project_feedback(app)
    init_new_project_review(app)
    init_new_project_result(app)
    init_new_project_display(app)
    
    init_layout_form(app)
    init_layout_task(app)
    init_layout_feedback(app)
    init_layout_result(app)
    init_layout_display(app)
    
    init_pcb_form(app)
    init_pcb_task(app)
    init_pcb_feedback(app)
    init_pcb_result(app)
    init_pcb_display(app)

    init_exts(app)
    init_blue_flow_step(app)

    #專案進度Task及里程碑
    init_blue_task_milestone(app)
    init_blue_status(app)
    init_blue_milestone(app)
    init_blue_task(app)
    init_blue_feedback_rule(app)
    init_blue_email(app)
    init_blue_attach(app)

    #專案中止原因
    init_blue_end_project_reason(app)
    init_blue_all_kinds_reason(app) # 各種原因編輯

    #專案狀態
    init_blue_project_status(app)
    init_blue_project_list(app)
    init_blue_form_list(app)

    #表單流水號sn
    init_blue_form_sn(app)

    #SwaggerUI
    init_blue_swagger(app)

    #flow dashboard
    init_blue_flow_dashboard(app)

    init_bpm_flow(app)

    init_form_flow(app)

    init_internal_project_task(app)
    init_internal_project_display(app)

    init_new_project_edit(app)
    init_new_technology_edit(app)
    init_layout_edit(app)
    init_pcb_edit(app)
    init_internal_project_form(app)
    init_internal_project_approve(app)
    return app