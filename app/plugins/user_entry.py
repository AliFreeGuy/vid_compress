from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f 
from utils import btn








@Client.on_message(filters.private & f.user_not_join & f.updater, group=0)
async def user_not_join(bot, msg):
    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    join_text = setting.join_text_fa if user.lang == 'fa' else setting.join_text_en
    await bot.send_message(msg.from_user.id, text=join_text, reply_markup = btn.join_channel(lang=user.lang , url=setting.channel_url))