from flask import Flask, render_template,request
from flask_cors import CORS
import json
import requests
import json

# 上傳檔案
import os
# from flaskapp import app
# from api import callapi,callxcreen,getimage
import urllib.request
from queue import Queue
import time
from werkzeug.utils import secure_filename
from flask import Flask, flash, request, redirect, url_for, render_template
import threading
import json
import pathlib

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])



app = Flask(__name__)
CORS(app)



@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

# 上傳檔案、辨識
@app.route('/uploadcustomfile', methods=['POST'])
def upload_image():
    # 取得目前檔案所在的資料夾 
    
    SRC_PATH =  pathlib.Path(__file__).parent.absolute() # SRC_PATH 值為 '/app'    
    UPLOAD_FOLDER = pathlib.WindowsPath('E:/GoodWork/express-mes/src/public/uploads')
    # SRC_PATH = 'E:\\GoodWork\express-mes\src'
    # UPLOAD_FOLDER = os.path.join(SRC_PATH,  'static', 'uploads') # UPLOAD_FOLDER 值為 '/app/static/uploads'
    # UPLOAD_FOLDER =  '@E:\\GoodWork\\express-mes\\src\\public\\uploads'
    print("TTTTTTTTTTT")
    print(SRC_PATH)
    print(UPLOAD_FOLDER)

    try:
        file = request.files['sendfile'] # 取得 AJAX 傳來的整張圖片
        file_names = []
        file_names.append(file.filename)
        if file.filename != '': # 如果取得到圖片的檔名
            # 驗證檔案型態
            isAllowedExtensions = allowed_file(file.filename)
            # 驗證成功
            if isAllowedExtensions:
                file.save(os.path.join(UPLOAD_FOLDER, file.filename)) # 圖片儲存路徑
                return {'states': "success",'msg':"上傳成功","data":file_names},200
            else:
                return {'states': "error",'msg':"不支援上傳此副檔名"},400
    except BaseException as e:
        return {'states': 'error','msg':"{}".format(e)},400


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8888, debug=True, threaded=True)
    #serve(app, host='0.0.0.0', port=8888, threads=4, _quiet=True)
    #serve(app, host='0.0.0.0', port=8888)