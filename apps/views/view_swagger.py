from flask import Blueprint
from flask_swagger_ui import get_swaggerui_blueprint
import json
from flask import jsonify
from apps.settings import DOMAIN_PATH
from apps.settings import SWAGGER_URL
from apps.settings import SWAGGER_JSON_URL


# 建立藍圖
blue_swagger = Blueprint('blue_swagger', __name__)
blue_swagger = get_swaggerui_blueprint(
    SWAGGER_URL,
    'http://{}{}'.format(DOMAIN_PATH, SWAGGER_JSON_URL),
    config={
        'operationsSorter': 'alpha',
        'showExtensions': True,
        'displayRequestDuration': True,  # 顯示請求時間
    }
)

def init_blue_swagger(app):

    app.register_blueprint(blueprint=blue_swagger, url_prefix=SWAGGER_URL)


# 開啟 Swagger UI 
@blue_swagger.route('/swagger/')
def swagger_docs():

    file_path = '../static/dev-rd-api.json'

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            #print(data)
        return jsonify(data)

    except FileNotFoundError:
        print('找不到指定的JSON文件:', file_path)
        return "找不到指定的JSON文件"

    except json.JSONDecodeError as e:
        print('無法解析JSON:', e)
        return "無法解析JSON"