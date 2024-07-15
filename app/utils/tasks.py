from celery import Celery
from celery.schedules import crontab
import redis
from os.path import abspath, dirname
import sys
from ffmpeg_progress_yield import FfmpegProgress
from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)
from datetime import datetime
import requests
from pyrogram import Client
import time
import os
from pathlib import Path
import random

parent_dir = dirname(dirname(abspath(__file__)))
sys.path.insert(0, parent_dir)

import config
from utils import cache , logger
from utils.connection import connection as con
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


def progressbar(current, total , task_id=None ):
    percentage = current * 100 // total
    progress_bar = ""
    for i in range(20):
        if percentage >= (i + 1) * 5:progress_bar += "█"
        elif percentage >= i * 5 + 2:progress_bar += "▒"
        else:progress_bar += "░"
        date = datetime.now()
    progress_data = {'progress' : progress_bar ,'percentage' : percentage , 'text' :f"{progress_bar} {percentage} ",'date' : str(date) }
    if not r.exists(task_id):
        r.hmset(task_id, progress_data)
        progress_data['is_update'] = 'True'
    elif r.exists(task_id ):
        if int(float(r.hgetall(task_id)['percentage'])) != percentage :
            p = r.hgetall(task_id)
            last_pdate = datetime.strptime(p['date'], '%Y-%m-%d %H:%M:%S.%f')
            time_difference = date - last_pdate
            seconds_difference = time_difference.total_seconds()
            if int(seconds_difference) >= config.EDITOR_TTL :
                progress_data['is_update'] = 'True'
                r.hmset(task_id, progress_data)
            else :
                progress_data['is_update'] = 'Fasle'
        else :
            r.hmset(task_id, progress_data)
            progress_data['is_update'] = 'False'
    return progress_data



def cancel_markup(user_lang , callback_data):
     text = '❌ Cancel' if user_lang == 'en' else '❌ کنسل'
     return InlineKeyboardMarkup([[
                          InlineKeyboardButton(text = text, callback_data=callback_data),
                          ],]) 




@app.task(name='tasks.editor', bind=True, default_retry_delay=1)
def editor(self , data ):
    
    videos_folder = Path.cwd() / 'videos'
    videos_folder.mkdir(exist_ok=True)
    file_path = videos_folder / str(self.request.id)
    file_path.mkdir(exist_ok=True)

    video_name = f'{file_path}/{random.randint(999 , 999999)}.mp4'
    thumb_name = f'{file_path}/{random.randint(999 , 999999)}.jpeg'
    setting = con.setting

    


    if config.DEBUG == 'True':bot = Client('editor' , api_hash=config.API_HASH , api_id=config.API_ID , session_string=config.SESSION_STRING , proxy = config.PROXY)
    else :bot = Client('editor' , api_hash=config.API_HASH , api_id=config.API_ID , session_string=config.SESSION_STRING )
    

    with bot : 
        cache.redis.hset(f'vid_data:{data["id"]}' , 'file_path'  , str(file_path))
        message = bot.get_messages(config.BACKUP, int(data['backup_msg_id']))
        def progress(current, total):
                    pdata = int(float(f"{current * 100 / total:.1f}"))
                    progress = progressbar(pdata , 400 , str(self.request.id) )
                    if progress['is_update'] == 'True' :
                        pbar = progress['text']
                        vid_editor_text = setting.vid_editor_text_fa if data['user_lang'] == 'fa' else setting.vid_editor_text_en
                        text = f'{vid_editor_text}\n\n📥{str(pbar)}'
                        msg_id = int(data['bot_msg_id'])+1
                        try :
                            bot.edit_message_text(chat_id=int(data['chat_id']) ,text = text ,message_id = msg_id ,
                        reply_markup=cancel_markup(user_lang=data["user_lang"] , callback_data=f'cancel-editor:vid_data:{str(data["id"])}'))
                        except Exception as e :logger.warning(e)
        bot.download_media(message, progress=progress , file_name=video_name)











    
    with bot :

            cmd = ["ffmpeg", "-i", video_name,]
            cmd.extend(["-filter_complex", f"drawtext=text='{setting.watermark_text}':fontsize=30:fontcolor=yellow:x=(main_w-text_w-10):y=(main_h-text_h-10)"])
            cmd.extend([
                "-r", "15",
                "-b:v", f"500k",
                "-b:a", "64k",
                f'{file_path}/output.mp4'])

            ff = FfmpegProgress(cmd)
            for progress in ff.run_command_with_progress():
                pdata = int(str(progress).split('.')[0])
                pbar = progressbar(pdata *2 +100 , 400 , str(self.request.id))
                pbar_text= pbar['text']
                if pbar['is_update'] == 'True':
                    vid_editor_text = setting.vid_editor_text_fa if data['user_lang'] == 'fa' else setting.vid_editor_text_en
                    text = f'{vid_editor_text}\n\n📥{str(pbar_text)}'
                    msg_id = int(data['bot_msg_id'])+1
                    try :
                        bot.edit_message_text(chat_id=int(data['chat_id']) ,text = text ,message_id = msg_id ,
                        reply_markup=cancel_markup(user_lang=data["user_lang"] , callback_data=f'cancel-editor:vid_data:{str(data["id"])}'))
                    except Exception as e :
                         logger.warning(e)









    with bot :
        def progress(current, total):
            pdata = int(float(f"{current * 100 / total:.1f}"))
            progress = progressbar(pdata +300 , 402 , str(self.request.id) )
            if progress['is_update'] == 'True' :
                pbar = progress['text']
                vid_editor_text = setting.vid_editor_text_fa if data['user_lang'] == 'fa' else setting.vid_editor_text_en
                text = f'{vid_editor_text}\n\n📥{str(pbar)}'
                msg_id = int(data['bot_msg_id'])+1
                try :
                    bot.edit_message_text(chat_id=int(data['chat_id']) ,text = text ,message_id = msg_id ,
                    reply_markup=cancel_markup(user_lang=data["user_lang"] , callback_data=f'cancel-editor:vid_data:{str(data["id"])}'))
                except Exception as e :logger.warning(e)
        bot.send_video(int(data['chat_id'])  , video=f'{file_path}/output.mp4', progress=progress ) 
        bot.delete_messages(int(data["chat_id"]), int(data['bot_msg_id'])+1)



   


















#celery -A tasks worker --beat -Q downloader_queue --concurrency=1 -n downloader_worker@%h
#celery -A tasks worker -Q uploader_queue --concurrency=1 -n uploader_worker@%h




























