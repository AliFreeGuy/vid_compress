from pyrogram import Client, filters
from utils import logger , cache , btn
from utils.connection import connection as con
import config
from utils import filters as f 
from pyrogram.types import (InlineQueryResultArticle, InputTextMessageContent,
                            InlineKeyboardMarkup, InlineKeyboardButton)
from utils.utils import random_code



@Client.on_inline_query()
async def answer(client, inline_query):
    plans = con.plans
    random_sub_code = random_code()
    results = []

    for plan in plans :
            if inline_query.query == plan['tag']:
                sub_data = {'user' : 'none' , 'plan' : plan["tag"]}
                cache.redis.hmset(f'sub:{random_sub_code}' , sub_data)
                des_text = f'🌟 برای فعال سازی اشتراک خودتون بر روی دکمه زیر بزنید '
                results.append(
                        InlineQueryResultArticle(
                            title=plan['name_fa'],
                            input_message_content=InputTextMessageContent(f"{plan['des_fa']}\n\n{des_text}"),
                            description=plan['des_fa'],
                            reply_markup=btn.admin_inline_query(sub_code=random_sub_code)))

    if inline_query.from_user.id == config.ADMIN :
        await inline_query.answer(results ,cache_time=1)
    

         