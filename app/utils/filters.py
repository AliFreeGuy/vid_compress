from pyrogram import filters
from utils.utils import join_checker
from utils.connection import connection as con 
from utils.logger import logger
import config
from datetime import datetime
import pytz



async def user_is_admin(_ , cli , msg ):
    admins = [config.ADMIN]
    if msg.from_user.id in admins : 
         return True
    return False


async def updater(_ , cli , msg ):
    try :
        user =  con.user(chat_id=msg.from_user.id , full_name=msg.from_user.first_name )
        if user and user.sub.expiry == None :
                con.add_sub(chat_id=msg.from_user.id , plan_tag='free')

        expiry_date_str = user.sub.expiry
        expiry_date = datetime.fromisoformat(expiry_date_str.replace('Z', '+00:00'))
        current_date = datetime.now(pytz.utc)
        if current_date > expiry_date:
            con.add_sub(chat_id=msg.from_user.id , plan_tag='free')
            
    except Exception as e :
         logger.error(e)
         
    return True

async def user_is_join(_ , cli , msg ):
        if con and con.setting.channel_url and con.setting.channel_chat_id :
            channels = [{'chat_id' : con.setting.channel_chat_id , 'link'  : con.setting.channel_url} ]
            is_join = await join_checker(cli , msg , channels)
            if not is_join : return True
            else :return False
        return True



async def user_not_join(_ , cli , msg ):
        if con and con.setting.channel_url and con.setting.channel_chat_id :
            channels = [{'chat_id' : con.setting.channel_chat_id , 'link'  : con.setting.channel_url} ]
            is_join = await join_checker(cli , msg , channels)
            if not is_join : return False
            else :return True
        return False


updater = filters.create(updater)
user_not_join=filters.create(user_not_join)
user_is_join = filters.create(user_is_join)
is_admin  =filters.create(user_is_admin)
