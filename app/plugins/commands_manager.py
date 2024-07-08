from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f 
from utils import btn








@Client.on_message(filters.private &f.user_is_join & f.updater , group=1)
async def command_manager(bot, msg):
    if msg.text  :


        if msg.text == '/help' : 
            await help_handler(bot , msg )
        
        elif msg.text == '/support' : 
            await support_handler(bot , msg )

        elif msg.text == '/start' : 
            await start_handler(bot , msg )

        elif msg.text == '/setting' : 
            await setting_handler(bot , msg )





async def setting_handler(bot , msg ):
    setting = con.setting
    user = con.get_user(msg.from_user.id )
    setting_text = setting.setting_text_fa if user.lang == 'fa' else setting.setting_text_en
    await bot.send_message(msg.from_user.id , text = setting_text , reply_markup = btn.setting_btn(user_lang=user.lang , user_quality=user.quality))


async def start_handler(bot ,msg ):

    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    start_text = setting.start_text_fa if user.lang == 'fa' else setting.start_text_en
    await bot.send_message(msg.from_user.id, text=start_text)


async def support_handler(bot , msg ):
    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    support_text = setting.sup_text_fa if user.lang == 'fa' else setting.sup_text_en
    await bot.send_message(msg.from_user.id, text=support_text)

    
async def help_handler(bot ,msg):
    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    help_text = setting.help_text_fa if user.lang == 'fa' else setting.help_text_en
    await bot.send_message(msg.from_user.id, text=help_text)

    