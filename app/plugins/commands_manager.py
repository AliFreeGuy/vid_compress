from pyrogram import Client, filters
from utils import logger
from utils import cache
from utils.connection import connection as con
from utils import filters as f  
from utils import btn ,txt
import config
from utils.utils import jdate , m_to_g



@Client.on_message(filters.private &f.user_is_join & f.updater , group=1)
async def command_manager(bot, msg):
    if msg.text  :


        if msg.text in ['/help' , '🆘 help' , '🆘 راهنما']  : 
            await help_handler(bot , msg )
        
        elif msg.text in ['/support' ,'🧑‍✈️ support' , '🧑‍✈️ پشتیبانی' ] : 
            await support_handler(bot , msg )

        elif msg.text == '/start' : 
            await start_handler(bot , msg )

        elif msg.text in ['/setting' , '⚙️ setting' , '⚙️ تنظیمات'] : 
            await setting_handler(bot , msg )
        
        elif msg.text in ['/plans' , '🎖 plans' , '🎖 اشتراک'] : 
            await plans_handler(bot , msg )

        elif msg.text in ['/profile' , '🎫 profile' ,'🎫 پروفایل' ] : 
            await profile_handler(bot ,msg )
        
        elif msg.text.startswith('/start sub_'):
            await activate_sub_handler(bot , msg )
        
        elif msg.text == 'پنل' : 
            await admin_panel_handler(bot , msg )





async def admin_panel_handler(bot  ,msg ):
    
    if msg.from_user.id == config.ADMIN :
        await bot.send_message(msg.from_user.id , text =txt.admin_panel , reply_markup = btn.admin_panel_btn() )



async def activate_sub_handler(bot , msg ):
    sub_code = msg.text.replace('/start sub_' , '')
    sub_key = f'sub:{sub_code}'
    sub_data = cache.redis.hgetall(sub_key)
    user = con.get_user(msg.from_user.id)
    
    if sub_data :
        if sub_data['user'] == 'none' : 
            con.add_sub(chat_id = msg.from_user.id , plan_tag=sub_data['plan'])
            cache.redis.hset(sub_key ,'user'  ,  str(msg.from_user.id))
            await bot.send_message(msg.from_user.id , '🥳')
            await bot.send_message(msg.from_user.id  ,txt.user_sub_activated(user.lang))
        else :await bot.send_message(msg.from_user.id , txt.sub_not_active(user_lang=user.lang))
    else :await bot.send_message(msg.from_user.id , txt.sub_not_found(user.lang) )



async def profile_handler(bot , msg ):
    user = con.get_user(msg.from_user.id )
    plans = con.plans
    
    if user.lang == 'fa':
        text = []
        if user.sub.expiry != None  :
            text.append(f'آیدی اختصاصی : `{str(user.chat_id)}`')
            for plan in plans :
                if plan['id'] == user.sub.plan :
                    text.append(f'اشتراک فعال : `{plan["name_fa"]}`')
                    break
            text.append(f'حجم قابل استفاده : `{str(m_to_g(user.sub.volume))} گیگ`')
            text.append(f'تاریخ پایان اشتراک : `{str(jdate(user.sub.expiry)["date"])}`')
            text.append('\nبرای ارتقا اشتراک بر روی /plans بزنید')
            await bot.send_message(chat_id = msg.from_user.id , text = "\n".join(text))
        else :
            text =  f'''آیدی اختصاصی : `{str(user.chat_id)}`\nاشتراک فعال : `خالی`\nبرای فعال سازی اشتراک بر روی /plans بزنید\n\n@infoVidCompressBot'''
            await bot.send_message(chat_id = msg.from_user.id , text = text )

    elif user.lang == 'en':
        text = []
        if user.sub.expiry != None  :
            text.append(f'chat id : `{str(user.chat_id)}`')
            for plan in plans :
                if plan['id'] == user.sub.plan :
                    text.append(f'active subscription : `{plan["name_fa"]}`')
                    break
            text.append(f'usable volume : `{str(m_to_g(user.sub.volume))} GB`')
            text.append(f'subscription end date : `{str(user.sub.expiry[:10])}`')
            text.append('\nclick on /plans to upgrade your subscription')
            await bot.send_message(chat_id = msg.from_user.id , text = "\n".join(text))
        else :
            text =  f'''chat id : {str(msg.from_user.id)}\nactive subscription : nothing\nclick on /plans to upgrade your subscription\n\n@infoVidCompressBot'''
            await bot.send_message(chat_id = msg.from_user.id , text = text )











async def plans_handler(bot , msg ):
    try : 
        plans = con.plans
        if plans :
            user = con.get_user(chat_id  = msg.from_user.id )
            setting = con.setting
            plans_text = []
            for plan in plans : 
                if user.lang == 'fa' : plans_text.append(plan['des_fa'])
                else :plans_text.append(plan['des_en'])
            await bot.send_message(
                    chat_id = msg.from_user.id ,
                    text = '\n\n〰️〰️〰️〰️〰〰️〰️〰️〰️〰〰️\n\n'.join(plans_text),
                    reply_markup = btn.admin_chat_id(user_lang = user.lang , chat_id = setting.admin_chat_id))
        await bot.send_message(msg.from_user.id , 'پلنی وجود ندارد !')
        
    except Exception as e :
        logger.error(e)
    


async def setting_handler(bot , msg ):
    setting = con.setting
    user = con.get_user(msg.from_user.id )
    setting_text = setting.setting_text_fa if user.lang == 'fa' else setting.setting_text_en
    await bot.send_message(msg.from_user.id , text = setting_text , reply_markup = btn.setting_btn(user_lang=user.lang , user_quality=user.quality))


async def start_handler(bot ,msg ):

    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    start_text = setting.start_text_fa if user.lang == 'fa' else setting.start_text_en
    placeholder_text = setting.placeholder_text_fa if user.lang == 'fa' else setting.placeholder_text_en
    await bot.send_message(msg.from_user.id, text=start_text ,reply_markup = btn.user_panel_menu(user_lang=user.lang  , placeholder=placeholder_text))


async def support_handler(bot , msg ):
    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    support_text = setting.sup_text_fa if user.lang == 'fa' else setting.sup_text_en
    placeholder_text = setting.placeholder_text_fa if user.lang == 'fa' else setting.placeholder_text_en
    await bot.send_message(msg.from_user.id, text=support_text , reply_markup = btn.user_panel_menu(user.lang , placeholder_text)) 

    
async def help_handler(bot ,msg):
    setting  = con.setting
    user = con.get_user(msg.from_user.id)
    help_text = setting.help_text_fa if user.lang == 'fa' else setting.help_text_en
    placeholder_text = setting.placeholder_text_fa if user.lang == 'fa' else setting.placeholder_text_en
    await bot.send_message(msg.from_user.id, text=help_text , reply_markup = btn.user_panel_menu(user_lang=user.lang , placeholder=placeholder_text))

    