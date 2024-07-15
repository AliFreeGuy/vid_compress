from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f 
from utils import btn , txt
from utils.utils import alert
from celery.result import AsyncResult
from utils.tasks import app 
from flower.utils.broker import Broker
from utils.tasks import editor


@Client.on_callback_query(f.user_not_join & f.updater , group=0)
async def call_user_not_join(bot ,call ):
    await alert(bot , call , msg=txt.place_join_channel)



@Client.on_callback_query(f.user_is_join & f.updater , group=0)
async def callback_manager(bot, call):
    
    logger.info(f'{call.from_user.first_name} - {call.from_user.id} - {call.data}')

    status = call.data.split(':')

    if status[0] == 'setting' : 
        await setting_handler(bot , call )
    
    elif status[0] == 'joined' :
        await user_joined(bot , call )

    elif status[0] == 'status-editor' :
        await status_editor(bot , call )
    
    elif status[0] == 'cancel-editor' : 
        await cancel_editor(bot , call )
    
    elif status[0].startswith('editor_q'):
        await set_editor_quality(bot ,call  )






async def set_editor_quality(bot , call ):
    user = con.get_user(call.from_user.id )
    setting = con.setting
    vid_key = f'vid_data:{call.data.split(":")[2]}'
    vid_data = cache.redis.hgetall(vid_key)
    if vid_data :
        cache.redis.hset(vid_key , 'quality'  , call.data.split(':')[0].replace('editor_' , ''))
        data = cache.redis.hgetall(vid_key)
        
        data['quality'] = call.data.split(':')[0].replace('editor_' , '')
        data = cache.redis.hgetall(vid_key)
        data['task_id'] = 'none'

        cache.redis.hset(vid_key , 'user_lang'  , user.lang)

        task = editor.delay(data)
        data['task_id'] = task.id
        data['user_lang'] = user.lang

        
        try :
                vid_editor_text = setting.vid_editor_text_fa if user.lang == 'fa' else setting.vid_editor_text_en
                await bot.edit_message_text(chat_id = call.from_user.id ,
                                            text = vid_editor_text ,
                                            message_id  = call.message.id,
                                            reply_markup = btn.vid_editor_btn(vid_data =vid_key , user_lang=user.lang))
        except Exception as e :
            logger.warning(e)
        



async def status_editor(bot , call ):

    user = con.get_user(call.from_user.id)
    vid_data = cache.redis.hgetall(call.data.replace('status-editor:' , ''))
    task_id = vid_data['task_id']
    
    broker = Broker(
        app.connection(connect_timeout=1.0).as_uri(include_password=True),
        broker_options=app.conf.broker_transport_options,
        broker_use_ssl=app.conf.broker_use_ssl,
    )
    async def queue_length():
        queues = await broker.queues(["celery"])
        print(queues)
        return queues[0].get("messages")
    

    await alert(bot , call , msg =txt.task_status(user_lang=user.lang , task_count=await queue_length()))
    
    

    
  




async def cancel_editor(bot , call ):
    try :
        vid_data = cache.redis.hgetall(call.data.replace('cancel-editor:' , ''))
        task_id = vid_data['task_id']
        task = AsyncResult(task_id)
        task.revoke(terminate=True)
        await alert(bot  ,call , msg= 'عملیات با موفقیت کنسل شد')
        await bot.delete_messages(call.from_user.id , call.message.id)
    except Exception as e :
        logger.error(e)







async def user_joined(bot , call ):
    await bot.delete_messages(
    chat_id=call.from_user.id,
    message_ids=call.message.id
)   
    setting  = con.setting
    user = con.get_user(call.from_user.id)
    start_text = setting.start_text_fa if user.lang == 'fa' else setting.start_text_en
    placeholder_text = setting.placeholder_text_fa if user.lang == 'fa' else setting.placeholder_text_en
    await bot.send_message(call.from_user.id, text=start_text  , reply_markup = placeholder_text)





async def setting_handler(bot , call ):

    status = call.data.split(':')[1]
    
    if status.startswith('lang'):
        user = con.update_lang(chat_id=call.from_user.id , full_name=call.from_user.first_name , lang=status.replace('lang_' , ''))
        setting = con.setting
        setting_text = setting.setting_text_fa if user.lang == 'fa' else setting.setting_text_en
        placeholder_text = setting.placeholder_text_fa if user.lang == 'fa' else setting.placeholder_text_en
        chagne_btn_lang = await bot.send_message(call.from_user.id , text =txt.changed_lang(user.lang) , reply_markup = btn.user_panel_menu(user_lang=user.lang , placeholder=placeholder_text))
        
        try :
            await bot.edit_message_text(chat_id = call.from_user.id ,
                                        text = setting_text ,
                                        message_id  = call.message.id,
                                        reply_markup = btn.setting_btn(user_lang=user.lang , user_quality=user.quality))
        except Exception as e :
            logger.warning(e)



    elif status.startswith('quality_'):
        user  = con.get_user(call.from_user.id )
        if user.quality == status.replace('quality_' ,''):
            user = con.update_quality(chat_id=call.from_user.id  , full_name=call.from_user.first_name , quality='' )
        else : 
            user = con.update_quality(chat_id=call.from_user.id , full_name=call.from_user.first_name , quality=status.replace('quality_' , ''))
        setting = con.setting
        setting_text = setting.setting_text_fa if user.lang == 'fa' else setting.setting_text_en
        try :
            await bot.edit_message_text(chat_id = call.from_user.id ,
                                        text = setting_text ,
                                        message_id  = call.message.id,
                                        reply_markup = btn.setting_btn(user_lang=user.lang , user_quality=user.quality))

        except Exception as e :
            logger.warning(e)