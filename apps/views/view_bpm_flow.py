from flask import Blueprint
from flask import request
from flask import Response
from flask import render_template
from flask import redirect
from flask import url_for
from apps.exts import current_datetime
from werkzeug.utils import secure_filename
from apps.settings import DOMAIN_PATH
from apps.settings import ALLOWED_EXTENSIONS
from apps.settings import BPMN_FILE_FOLDER
from apps.settings import FILE_PATH
from flask import send_from_directory
import urllib.parse
from apps.exts import mongo
from apps.views.view_member        import get_cname_by_organize
from apps.views.view_member        import get_organize_by_cname
from apps.models.model_member      import Member
import json
import os
from apps.exts import logger
import xml.etree.ElementTree as ET
import xml.dom.minidom as minidom


blue_bpm_flow = Blueprint('blue_bpm_flow', __name__)


def init_bpm_flow(app):
    app.register_blueprint(blueprint=blue_bpm_flow)



@blue_bpm_flow.route("/page/v0/bpm_flow/", methods=['GET'])
def bpm_flow_index():

    project_no = request.args.get('project_no')
    mode = "bpm_flow"

    # check cookie
    account = request.cookies.get('account')
    avatar  = request.cookies.get('avatar' )
    member  = request.cookies.get('eName'  )
    sex     = request.cookies.get('sex'    )
    cname   = request.cookies.get('cName'  )

    #print(account)
    #print(cname)
    #print(avatar)
    #print(project_no)

    # MODE, FORM_NO
    if account is None:
        return redirect(url_for('blue_main.login_fun' ))
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
            'bpm_flow.html',
            MODE=mode,
            DOMAIN_PATH=DOMAIN_PATH,
            USER=member,
            USER_cname=cname,
            PHOTO=avatar,
            ACCOUNT=account,
            IS_LEADER=isleader,
            PROJECT_NO=project_no)



# client端按下[儲存按鈕] 上傳並儲存 bpmn xml 檔
@blue_bpm_flow.route('/api/v0/upload/bpmn/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        xml_name = request.args.get('file')
        xml_data = request.data.decode('utf-8')
        print(xml_data)
        file_path = os.path.join(BPMN_FILE_FOLDER, xml_name)
        print(file_path)
        save_xml(xml_data, file_path)
        strMsg = xml_name + ' 已成功儲存!'
        strJson = { 'result': 'ok', 'code':'', 'msg': strMsg , 'data': { }}
        return Response(json.dumps(strJson))



# 寫入 xml檔
def save_xml(xml_string, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(xml_string)



# 取得特定路徑下所有檔案列表
@blue_bpm_flow.route('/api/v0/bpmn/files/', methods=['GET'] )
def get_bpmn_file_list_from_folder():
    
    res = find_files_from_folder(BPMN_FILE_FOLDER)
    strJson = { 'result': 'ok', 'code':'', 'data': res }
    return Response(json.dumps(strJson))



# 依照資料夾路徑找出檔案名
def find_files_from_folder(folder_path):

    if os.path.exists(folder_path):
        file_list = []
        file_names = os.listdir(folder_path)
        for file_name in file_names:
            print(file_name)
            file_list.append(file_name)
        return file_list
    else:
        print("bpmn資料不存在")
        return []



# 分析XML 檔
@blue_bpm_flow.route('/api/v0/parser/xml/<file_name>/', methods=['GET'] )
def get_xml_content(file_name):
    print(file_name)
    file_path = os.path.join(BPMN_FILE_FOLDER, file_name)
    print(file_path)
    tree = ET.parse(file_path)
    #print(tree)
    root = tree.getroot()
    #print(root)
    
    #dirProcess = {}
    #processList = []
    
    
     # 部門群組陣列
    listDepartment = []
    
    # 第一層(main) 先定義需多少個群組
    for element_main in root:
        #print(element_main)
        tag_name_main = element_main.tag.split('}')[-1]
        #print(tag_name_main)
        
        # 先找出符合[ collaboration ] 名稱的tag, 為部門群組
        if tag_name_main == "collaboration":
            # 第二層(sub)
            for element_sub in element_main:
                tag_name_sub = element_sub.tag.split('}')[-1]
                #print(tag_name_sub)
                # 找出有幾個部門
                if( tag_name_sub == "participant"):
                    dirDepartment = {}
                    for tag_item in element_sub.attrib.items():
                        if tag_item[0] == 'id':
                            dirDepartment['id'] = tag_item[1]
                        if tag_item[0] == 'name':
                            dirDepartment['name'] = tag_item[1]
                        if tag_item[0] == 'processRef':
                            dirDepartment['processRef'] = tag_item[1]
                        dirDepartment['flow'] = []
                        dirDepartment['startEvent'] = {}
                        dirDepartment['task'] = []
                        dirDepartment['sequenceFlow'] = []
                        dirDepartment['endEvent'] = {}
                    listDepartment.append(dirDepartment)
        
            #print(listDepartment)
    #print(listDepartment)
    #print(len(listDepartment))


    # 第一層(main)
    for element_main in root:
        #print(element_main)
        tag_name_main = element_main.tag.split('}')[-1]
        #print(tag_name_main)
        
        # 先找出符合[ process ] 名稱的tag, process 為主要流程內容
        if tag_name_main == "process":
            #print(listDepartment)
            # 流程內容
            for attrib in element_main.attrib.items():
                #print(attrib)
            
                for depItem in listDepartment:
                    #print(depItem)
                    if attrib[0] == 'id':
                        if attrib[1] == depItem['processRef']:
                            
                            # 第二層(sub)
                            for element_sub in element_main:
                                #print(element_sub)
                                tag_name_sub = element_sub.tag.split('}')[-1]
                                #print(tag_name_sub)

                                # 找出起始點 startEvent
                                if( tag_name_sub == "startEvent"):
                                    dirStartEvent = {}
                                    for tag_item in element_sub.attrib.items():
                                        if tag_item[0] == 'id':
                                            dirStartEvent['id'] = tag_item[1]
                                        if tag_item[0] == 'name':
                                            dirStartEvent['name'] = tag_item[1]
                                    depItem['startEvent'] = dirStartEvent

                                # 找出結束點 endEvent
                                if( tag_name_sub == "endEvent"):
                                    dirEndEvent = {}
                                    for tag_item in element_sub.attrib.items():
                                        if tag_item[0] == 'id':
                                            dirEndEvent['id'] = tag_item[1]
                                        if tag_item[0] == 'name':
                                            dirEndEvent['name'] = tag_item[1]
                                    depItem['endEvent'] = dirEndEvent
                                    
                                # 找出有幾個任務 task
                                if( tag_name_sub == "task"):
                                    dirTask = {}
                                    for tag_item in element_sub.attrib.items():
                                        if tag_item[0] == 'id':
                                            dirTask['id'] = tag_item[1]
                                        if tag_item[0] == 'name':
                                            dirTask['name'] = tag_item[1]
                                    depItem['task'].append(dirTask)
                                    
                                # 找出有幾條連接線 sequenceFlow
                                if( tag_name_sub == "sequenceFlow"):
                                    dirSequenceFlow = {}
                                    for tag_item in element_sub.attrib.items():
                                        #print(tag_item)
                                        if tag_item[0] == 'id':
                                            dirSequenceFlow['id'] = tag_item[1]
                                        if tag_item[0] == 'sourceRef':
                                            dirSequenceFlow['sourceRef'] = tag_item[1]
                                        if tag_item[0] == 'targetRef':
                                            dirSequenceFlow['targetRef'] = tag_item[1]
                                    depItem['sequenceFlow'].append(dirSequenceFlow)


    #print(listDepartment)
    #print(len(listDepartment))
    
    # 建立動作順序
    #for processObj1 in listDepartment:
        #print(processObj1) 
    # 合併所有流程
    getAllProcessFlow(listDepartment)
    
        
        # for task_id, task_name in rearranged_tasks:
        #     print('---------------------------')
        #     print(f'Task ID: {task_id}, Task Name: {task_name}')
        # for task_id, task_name in rearranged_tasks:
        #     print(f'Task ID: {task_id}, Task Name: {task_name}')

    #     tempObj = {}
    #     processObj1['flow'].append(processObj1['startEvent']['name'])
    #     break
        
    # for processObj2 in listDepartment:
    #     # 透過來源ID 找到目標名稱與ID
    #     targetID, targetName  = getTargetObjName( processObj2, processObj2['task']['id'])
        
    #     print(targetID, targetName)
        
            # listStartEvent = []
            # listSequenceFlow = []
            # listTask = []
            
            # 第二層(sub)
            #for element_sub in element_main:
                #print(element_sub)
                #tag_name_sub = element_sub.tag.split('}')[-1]
                #print(tag_name_sub)
                
                # 找出起始點 startEvent
                # if( tag_name_sub == "startEvent"):
                #     dirStartEvent = {}
                #     for tag_item in element_sub.attrib.items():
                #         if tag_item[0] == 'id':
                #             dirStartEvent['id'] = tag_item[1]
                #         if tag_item[0] == 'name':
                #             dirStartEvent['name'] = tag_item[1]
                #         listStartEvent.append(dirStartEvent)
                
                # 找出有幾個任務 task
                # if( tag_name_sub == "task"):
                #     dirTask = {}
                #     for tag_item in element_sub.attrib.items():
                #         if tag_item[0] == 'id':
                #             dirTask['id'] = tag_item[1]
                #         if tag_item[0] == 'name':
                #             dirTask['name'] = tag_item[1]
                #     listTask.append(dirTask)


                # 找出有幾條連接線 sequenceFlow
                # if( tag_name_sub == "sequenceFlow"):
                #     dirSequenceFlow = {}
                #     for tag_item in element_sub.attrib.items():
                #         #print(tag_item)
                #         if tag_item[0] == 'id':
                #             dirSequenceFlow['id'] = tag_item[1]
                #         if tag_item[0] == 'sourceRef':
                #             dirSequenceFlow['sourceRef'] = tag_item[1]
                #         if tag_item[0] == 'targetRef':
                #             dirSequenceFlow['targetRef'] = tag_item[1]
                #     listSequenceFlow.append(dirSequenceFlow)
            
            
            # print(listStartEvent)
            # print(len(listStartEvent))
            
            # print(listSequenceFlow)
            # print(len(listSequenceFlow))
            
            # print(listTask)
            # print(len(listTask))


        
        # print('Element tag:',  child.tag )
        # print('Element text:', child.text)
        
        # for item in child.attrib.items():
        #     print(item)
        
        # for attr_name, attr_value in child.attrib.items():
        #     print(f'Attribute name: {attr_name}, Attribute value: {attr_value}')
            
        # for sub_child in child:
        #     print('Sub-element tag:', sub_child.tag)
        #     print('Sub-element text:', sub_child.text)
    
    strJson = { 'result': 'ok', 'code':'', 'data': listDepartment }
    return Response(json.dumps(strJson))
    


# 透過來源ID 找到目標名稱與ID
# def getTargetObjName( srcobj, sourceObjID):
#     targetObjID = ""
#     targetObjName = ""
#     for item1 in srcobj['sequenceFlow']:
#         print(item1)
#         if item1['sourceRef'] == sourceObjID:
#             targetObjID = item1['targetRef']
#             for item2 in srcobj['task']:
#                 if item2['id'] == targetObjID:
#                     targetObjName = item2['name']
#     return targetObjID, targetObjName


#
# 解析 JSON 數據
def getAllProcessFlow(dataList):
    
    merged_array = []
    for data in dataList:
        #print(data)
        merged_array += data['task']
        
    print(merged_array)
