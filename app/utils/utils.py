
from pyrogram.errors import UserNotParticipant
import jdatetime
import re
from utils.cache import cache
import jdatetime
import datetime
from .logger import logger
import jdatetime
import uuid




def b_to_mb(data):
    file_size_in_megabytes = data / (1024 * 1024)
    file_size = (f"{file_size_in_megabytes:.2f}")
    return float(file_size)



def random_code():
    return uuid.uuid4()

def m_to_g(data):
    try :
        number = data
        result = number / 1000
        formatted_result = "{:.1f}".format(result)
        return formatted_result
    except Exception as e : print('m to g utils  ' , str(e))

def jdate(date_miladi):
    try :
        try :date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%S.%fZ")
        except : date_time = jdatetime.datetime.strptime(date_miladi, "%Y-%m-%dT%H:%M:%SZ")
        date_shamsi = jdatetime.datetime.fromgregorian(datetime=date_time).replace(hour=0, minute=0, second=0, microsecond=0)
        current_date_shamsi = jdatetime.datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        remaining_days = (date_shamsi - current_date_shamsi).days
        date = date_shamsi.strftime('%Y-%m-%d').split('-')
        date = f'{date[2]}-{date[1]}-{date[0]}'
        print(date)
        result = {
            'date': date,
            'day': remaining_days
        }
        return result
    except Exception as e : print('jdate utils ' , str(e))






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
    
   