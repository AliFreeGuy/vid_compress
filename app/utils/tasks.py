
from celery import Celery
from celery.schedules import crontab
import redis
from os.path import abspath, dirname
import sys
import requests
from pyrogram import Client
import time
import os

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)

import config
from utils import cache
from config import REDIS_DB, REDIS_HOST, REDIS_PORT

r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)
app = Celery('tasks', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')
app.conf.timezone = 'UTC'

app.conf.update(
    task_serializer='json',
    result_serializer='json',
    accept_content=['json',],
    worker_concurrency=1,
    worker_prefetch_multiplier=1,
)





@app.task(name='tasks.editor', bind=True, default_retry_delay=1)
def editor(self , data ):
    
    if config.DEBUG == 'True':bot = Client('editor' , api_hash=config.API_HASH , api_id=config.API_ID , session_string=config.SESSION_STRING , proxy = config.PROXY)
    else :bot = Client('editor' , api_hash=config.API_HASH , api_id=config.API_ID , session_string=config.SESSION_STRING )
    


    with bot :
        bot.send_message(config.ADMIN , 'hi user ')
























#celery -A tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




























