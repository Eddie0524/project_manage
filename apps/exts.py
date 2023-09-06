from flask_cors import CORS
from flask_pymongo import PyMongo
import time
import logging
from logging.handlers import TimedRotatingFileHandler
import os
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger



logger = logging.getLogger("app_logger")
logger.setLevel(logging.DEBUG)

mongo = PyMongo()

current_datetime = time.strftime("%Y-%m-%d %H:%M:%S")

def save_log_task():
    print("Running scheduled save_log_task...")
    for handler in logger.handlers:
        handler.close()
        logger.removeHandler(handler)
    
    log_file = "{}\\{}\\{}.log".format(os.path.dirname(__file__),'log', time.strftime('%Y-%m-%d') )
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    



def init_exts(app):

    CORS(app, resources={r"/*": {"origins": "*"}})
    mongo.init_app(app)

    scheduler = BackgroundScheduler()
    scheduler.add_job(save_log_task, CronTrigger(hour='0', minute='0', second='0')) #每日開始
    scheduler.start()
    
    log_file1 = "{}\\{}\\{}.log".format(os.path.dirname(__file__),'log', time.strftime('%Y-%m-%d') )
    #print(log_file1)
    formatter1 = logging.Formatter('%(asctime)s - %(levelname)s - %(funcName)s - %(message)s')
    
    file_handler1 = logging.FileHandler(log_file1)
    file_handler1.setLevel(logging.DEBUG)
    file_handler1.setFormatter(formatter1)
    logger.addHandler(file_handler1)

