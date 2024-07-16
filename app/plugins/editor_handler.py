from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f  
from utils import btn ,txt 
from utils.utils import jdate , m_to_g , alert , b_to_mb , file_checker
import config
from utils.tasks import editor
import random
 

@Client.on_message(filters.private &f.user_is_join &filters.video , group=2)
async def video_editor_handler(bot, msg):
    if msg.from_user.id == msg.chat.id :
        user = con.get_user(chat_id=msg.from_user.id )
        setting = con.setting

        if user.sub.expiry != None :
            await editor_manager(bot , msg )

        else :
            user_not_sub_text = setting.user_not_sub_fa if user.lang == 'fa' else setting.user_not_sub_en
            await msg.reply_text(user_not_sub_text, quote=True)



async def editor_manager(bot ,msg ):

    data = {}
    user = con.get_user(chat_id=msg.from_user.id )
    setting= con.setting
    video_size  = b_to_mb(msg.video.file_size)
    
    if user.sub.volume  > video_size : 

        backup_vid = await msg.copy(config.BACKUP)
        data['backup_msg_id']  =backup_vid.id
        data['chat_id'] = msg.from_user.id 
        data['bot_msg_id'] = msg.id
        data['file_size'] = b_to_mb(msg.video.file_size)
        data['user_lang'] = user.lang
        data['unique_id']  = msg.video.file_unique_id
        update_sub = con.update_sub(chat_id=msg.from_user.id , volume=float(f'-{b_to_mb(msg.video.file_size)}'))
        
        

       
        if update_sub : 

            file_checker_data = file_checker(unique_id = msg.video.file_unique_id , quality = update_sub.quality)
            if file_checker_data :
                await bot.send_video(msg.from_user.id , video = file_checker_data['file_id'])

            elif not file_checker_data and  update_sub.quality != '' :
                data['quality'] = update_sub.quality
                random_code = str(random.randint(9999 , 999999))
                data['id']  = random_code
                vid_data_key = f'vid_data:{random_code}'
                data['task_id'] = 'none'
                task = editor.delay(data)
                data['task_id'] = task.id
                cache.redis.hmset(vid_data_key , data)
                vid_editor_text = setting.vid_editor_text_fa if user.lang == 'fa' else setting.vid_editor_text_en
                await msg.reply_text(vid_editor_text, quote=True , reply_markup  =btn.vid_editor_btn(vid_data =vid_data_key , user_lang=user.lang))
                print(data)

            else :
                data['quality'] = 'none' 
                data['task_id'] = 'none'
                random_code = str(random.randint(9999 , 999999))
                data['id']  = random_code
                vid_data_key = f'vid_data:{random_code}'
                cache.redis.hmset(vid_data_key , data)
                vid_editor_text = setting.vid_editor_text_fa if user.lang == 'fa' else setting.vid_editor_text_en
                await msg.reply_text(vid_editor_text, quote=True , reply_markup  =btn.vid_editor_quality(vid_key =vid_data_key , user_lang=user.lang))
                print(data)


    
        else :
            user_not_sub_text = setting.user_not_sub_fa if user.lang == 'fa' else setting.user_not_sub_en
            await msg.reply_text(user_not_sub_text, quote=True)

    else :
        user_not_sub_text = setting.user_not_sub_fa if user.lang == 'fa' else setting.user_not_sub_en
        await msg.reply_text(user_not_sub_text, quote=True)