



def sub_not_found(user_lang ):

    if user_lang == 'fa' : 
        return 'همچین کد اشتراکی نداریم :('
    else :
        return 'No subscription found with this code :('
    

def sub_not_active(user_lang ):
    if user_lang == 'fa' :
        return 'این کد اشتراک قبلا استفاده شده :('
    else :
        return 'This subscription has already been used :('