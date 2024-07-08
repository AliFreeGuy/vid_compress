from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f 
from utils import btn








@Client.on_callback_query(f.user_is_join & f.updater , group=0)
async def callback_manager(bot, call):

    status = call.data.split(':')

    if status[0] == 'setting' : 
        await setting_handler(bot , call )




async def setting_handler(bot , call ):

    status = call.data.split(':')[1]
    
    if status.startswith('lang'):
        user = con.update_lang(chat_id=call.from_user.id , full_name=call.from_user.first_name , lang=status.replace('lang_' , ''))
        setting = con.setting
        setting_text = setting.setting_text_fa if user.lang == 'fa' else setting.setting_text_en
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