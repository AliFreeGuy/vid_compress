from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con


@Client.on_message(filters.command('start'))
async def say_hello(bot, msg):
    data = con.setting
    print(data)
    await bot.send_message(msg.from_user.id , f'hi user')