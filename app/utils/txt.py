

place_join_channel = f'لطفا ابتدا عضو کانال شوید !'

def sub_not_found(user_lang ):

    if user_lang == 'fa' : 
        return 'همچین کد اشتراکی نداریم :('
    else :
        return 'No subscription found with this code :('
    

 
def user_sub_activated(user_lang):
    if user_lang == 'fa' : 
        return '🥳 اشتراک شما با موفقیت فعال شد !'
    else :
        return '🥳 Your subscription has been successfully activated'

def sub_not_active(user_lang ):
    if user_lang == 'fa' :
        return 'این کد اشتراک قبلا استفاده شده :('
    else :
        return 'This subscription has already been used :('