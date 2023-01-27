import os 


class Config(object):
    API_ID = int(os.environ.get("API_ID","18860540"))
    API_HASH = os.environ.get("API_HASH","22dd2ad1706199438ab3474e85c9afab")
    ADMIN = int(os.environ.get("ADMIN","5253824227"))
    CH_USERNAME = os.environ.get("CH_USERNAME","@seaofallmovies")
    DB_NAME = os.environ.get("DB_NAME","renamebot2")
    DB_URL = os.environ.get("DB_URL","mongodb+srv://abc:abc@cluster01.98xu6iz.mongodb.net/?retryWrites=true&w=majority")
    DP_PASTE = os.environ.get("DP_PASTE",True)
    FROM_CHANNEL = int(os.environ.get("FROM_CHANNEL","-1001785312895"))
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL","-1001718574234"))
    REMOVE_WORD = os.environ.get("REMOVE_WORD","💥|Join Us Oɴ Tᴇʟᴇɢʀᴀᴍ|❤️|SIDHUU5911|BuLMoviee|Join Us On Telegram||JESSEVERSE|Jesseverse|_Join_Us_On_Telegram_|Theprofffesorr|Latest_Movies_Reborn|@|Latest_Movies_1stOnNet|Hindi_Fhd_Movies|Backup channel|File Uploaded Here|https|http|:|//|t.me|Quality_HD|Hindi_FHd_Movies|Latest_Movies_FreeOnNet|Uploaded by|🔰|Uᴘʟᴏᴀᴅᴇᴅ Bʏ|JOIN|SUPPORT|♻️ F-Press")
    TOKEN = os.environ.get("TOKEN","5598160444:AAEpXtNmrHzquJTAZB3KRYFkj3K_-p15eXo")
    TO_CHANNEL = int(os.environ.get("TO_CHANNEL","-1001541703053"))
    REMOVE_CAPTION = osos.environ.get("REMOVE_CAPTION","")
