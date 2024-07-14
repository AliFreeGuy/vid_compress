from pyrogram import Client




api_id = 26801362
api_hash = 'ed9c1202ed0cf85a66f8d5b6b392fd1e'
bot_token = ''
proxy = {"scheme": "socks5","hostname": "127.0.0.1","port": 1080,}


bot = Client('fff' , api_id = api_id , api_hash=api_hash , proxy=proxy )




with bot :
    session_string = bot.export_session_string()
    print(session_string)