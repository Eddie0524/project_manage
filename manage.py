from apps import create_app
#from waitress import serve

##########################################################
# conda create -n flask-sunix python=3.7
# conda activate flask-sunix
# pip install -r requirements.txt
# python manage.py
##########################################################

app = create_app()

if __name__ == '__main__':
    #app.run()
    app.run(host='0.0.0.0', port=8888, debug=True, threaded=True)
    #serve(app, host='0.0.0.0', port=8888, threads=4, _quiet=True)
    #serve(app, host='0.0.0.0', port=8888)