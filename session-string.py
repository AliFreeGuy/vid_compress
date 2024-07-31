from pyrogram import Client
from os import environ as env



BOT_TOKEN='6768039069:AAFduOnBvLH5RA_MFfairM39dVzglQK0Pns'
API_ID='26801362'
API_HASH='ed9c1202ed0cf85a66f8d5b6b392fd1e'
WORK_DIR='/tmp'
BOT_DEBUG='False'

bot = Client('test' , api_id=API_ID , api_hash=API_HASH , bot_token = BOT_TOKEN )

with bot :
    data = bot.export_session_string()
    print(data)
