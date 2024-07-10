from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f  
from utils import btn ,txt 
from utils.utils import jdate , m_to_g , alert







@Client.on_message(filters.private &f.user_is_join &filters.video , group=2)
async def video_editor_handler(bot, msg):

    user = con.get_user(chat_id=msg.from_user.id )
    setting = con.setting

    if user.sub.expiry != None :
        await editor_manager(bot , msg )

    else :
        user_not_sub_text = setting.user_not_sub_fa if user.lang == 'fa' else setting.user_not_sub_en
        await msg.reply_text(user_not_sub_text, quote=True)



async def editor_manager(bot ,msg ):
    print('hi user mother fucker')
    print(msg)