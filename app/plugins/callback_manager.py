from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f 
from utils import btn , txt

from utils.utils import alert




@Client.on_callback_query(f.user_not_join & f.updater , group=0)
async def call_user_not_join(bot ,call ):
    await alert(bot , call , msg=txt.place_join_channel)



@Client.on_callback_query(f.user_is_join & f.updater , group=0)
async def callback_manager(bot, call):
    

    status = call.data.split(':')

    if status[0] == 'setting' : 
        await setting_handler(bot , call )
    
    elif status[0] == 'joined' :
        await user_joined(bot , call )


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