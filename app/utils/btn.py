from pyrogram.types import (ReplyKeyboardMarkup, InlineKeyboardMarkup,InlineKeyboardButton , KeyboardButton)




def join_channel(lang , url ):
    buttons = []
    if lang == 'en'  : 
        buttons.append([InlineKeyboardButton(text='Join Channel',url=url)])
        buttons.append([InlineKeyboardButton(text='I became a member',callback_data='joined')])
    elif lang == 'fa' : 
        buttons.append([InlineKeyboardButton(text='عضویت در کانال',url=url)])
        buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='joined')])
    return InlineKeyboardMarkup(buttons)



def setting_btn(user_lang , user_quality):
    buttons = []


    fa_text = f'✔️ 🇮🇷 فارسی' if user_lang == 'fa' else '🇮🇷 فارسی'
    en_text = f'✔️ 🇺🇸 English' if user_lang == 'en' else '🇺🇸 English'
    lang_btn = [
            InlineKeyboardButton(text=fa_text,callback_data=f'setting:lang_fa'),
            InlineKeyboardButton(text=en_text,callback_data=f'setting:lang_en'),
            ] 
    buttons.append(lang_btn)


    if user_lang == 'fa' : 
        q1= f'✔️ کیفیت خوب' if user_quality == 'q1' else 'کیفیت خوب'
        q2= f'✔️ کیفیت متوسط' if user_quality == 'q2' else 'کیفیت متوسط'
        q3= f'✔️ کیفیت کم' if user_quality == 'q3' else 'کیفیت کم'
        quality_btn = [
            InlineKeyboardButton(text=q1,callback_data=f'setting:quality_q1'),
            InlineKeyboardButton(text=q2,callback_data=f'setting:quality_q2'),
            InlineKeyboardButton(text=q3,callback_data=f'setting:quality_q3'),
            ] 
        buttons.append(quality_btn)
    

    elif user_lang == 'en' : 
        q1= f'✔️ good quality' if user_quality == 'q1' else 'good quality'
        q2= f'✔️ mid quality' if user_quality == 'q2' else 'mid quality'
        q3= f'✔️ low quality' if user_quality == 'q3' else 'low quality'
        quality_btn = [
            InlineKeyboardButton(text=q1,callback_data=f'setting:quality_q1'),
            InlineKeyboardButton(text=q2,callback_data=f'setting:quality_q2'),
            InlineKeyboardButton(text=q3,callback_data=f'setting:quality_q3'),
            ] 
        buttons.append(quality_btn)
    
    return InlineKeyboardMarkup(buttons)


    
# def join_channels_url(channels):
#     persian_numbers = ['اول', 'دوم', 'سوم', 'چهارم', 'پنجم']  
#     buttons = []
#     for idx, channel in enumerate(channels):
#         text = f"کانال {persian_numbers[idx]}"
#         buttons.append([InlineKeyboardButton(text=text, url=channel)])
#     buttons.append([InlineKeyboardButton(text='عضو شدم',callback_data='join:joined')])
#     return InlineKeyboardMarkup(buttons)




# def cancel_task(data ):
#     buttons = []
#     buttons.append([InlineKeyboardButton(text='لغو عملیات',callback_data=data)])
#     return InlineKeyboardMarkup(buttons)
    
# def plans_btn(plans , support_id=None ):
#     buttoons = []
#     for plan in plans :
#         plan_tag = plan['tag']
#         buttoons.append(InlineKeyboardButton(text=plan['name'], callback_data=f'plans:{plan_tag}'))
#     chunked_buttons = [buttoons[i:i + 3] for i in range(0, len(buttoons), 3)]
#     if  support_id : 
#         chunked_buttons.append([InlineKeyboardButton(text='خرید اشتراک' , url=f'https://t.me/{support_id}')])
#     return InlineKeyboardMarkup(chunked_buttons)

    
# def get_file(call_data):
#     buttons = [[InlineKeyboardButton(text='دریافت فایل',callback_data=call_data)]]
#     return InlineKeyboardMarkup(buttons)



































































































