
from pyrogram.errors import UserNotParticipant
import jdatetime
import re
from utils.cache import cache
import jdatetime
import datetime
from .logger import logger






async def join_checker(cli , msg , channels ):
   
    my_channels = channels

    not_join = []
        
    for i in my_channels : 
        try :  
            data = await cli.get_chat_member(int(i['chat_id']), msg.from_user.id )
        except UserNotParticipant :
            not_join.append(i['link'])
            continue
        except Exception as e  :
            print(e)
            continue
    return not_join




async def alert(client ,call , msg = None ):
    try :
        if msg is None : await call.answer('خطا لطفا دوباره تلاش کنید', show_alert=True)
        else : await call.answer(msg , show_alert = True)
    except Exception as e : logger.error(e)
    
   