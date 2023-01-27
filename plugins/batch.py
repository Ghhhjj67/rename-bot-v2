from helper.progress import progress_for_pyrogram
from pyrogram import Client, filters
from pyrogram.types import (  InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
from hachoir.metadata import extractMetadata
from hachoir.parser import createParser
from helper.database import find
import os
import re
from PIL import Image
from configs import Config
import time
async def doc1(bot,msg,txt,message):
    old_name = msg.document.file_name
    if Config.REMOVE_WORD:
        file_name0 = old_name.rsplit(".",1)[0]
        new_name0 = re.sub(Config.REMOVE_WORD,"",file_name0)
        new_name = Config.CH_USERNAME+new_name0+"."+old_name.rsplit(".",1)[1]
    else:
        new_name=old_name
    if msg.document.caption:
        if Config.REMOVE_CAPTION:
            new_caption = re.sub(Config.REMOVE_CAPTION,"",msg.document.caption)
        else:
            new_caption = msg.document.caption
    else:
        new_caption = new_name
    file_path = f"downloads/{new_name}"
    file = msg.document
    ms = await txt.edit("``` Trying To Download...```")
    c_time = time.time()
    try:
        path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
    except Exception as e:
        await ms.reply_text(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name,file_path)
    user_id = int(message.from_user.id)
    thumb = find(user_id)
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        c_time = time.time()
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_document(Config.TO_CHANNEL,document = file_path,thumb=ph_path,caption = f"**{new_caption}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
            os.remove(ph_path)
        except Exception as e:
            await ms.reply_text(e)
            os.remove(file_path)
            os.remove(ph_path)
    else:
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_document(Config.TO_CHANNEL,document = file_path,caption = f"**{new_caption}**",progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
        except Exception as e:
            await ms.reply_text(e)
            os.remove(file_path)
#@Client.on_callback_query(filters.regex("vid"))
async def vid1(bot,msg,txt,message):
    old_name = msg.video.file_name
    if Config.REMOVE_WORD:
        file_name0 = old_name.rsplit(".",1)[0]
        new_name0 = re.sub(Config.REMOVE_WORD,"",file_name0)
        new_name = Config.CH_USERNAME+new_name0+"."+old_name.rsplit(".",1)[1]
    else:
        new_name=old_name
    if msg.video.caption:
        if Config.REMOVE_CAPTION:
            new_caption = re.sub(Config.REMOVE_CAPTION,"",msg.video.caption)
        else:
            new_caption = msg.video.caption
    else:
        new_caption = new_name
    file_path = f"downloads/{new_name}"
    file = msg.video
    ms = await txt.edit("``` Trying To Download...```")
    c_time = time.time()
    try:
        path = await bot.download_media(message = file, progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
    except Exception as e:
        
        await ms.reply_text(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name,file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    user_id = int(message.from_user.id)
    thumbs = find(user_id)
    f_thumb_id0 = msg.video.thumbs[0] \
            if msg.video.thumbs \
            else None
    f_thumb_id =f_thumb_id0.file_id
    u_thumb_path = await bot.download_media(thumbs)
    if thumbs:
        if Config.DP_PASTE and f_thumb_id:
            await txt.edit("Fetching Thumbnail ...")
            fi_thumb_path = await bot.download_media(f_thumb_id)
            fi_thumb_path1 = await fix_thumbnail1(fi_thumb_path)
            im1 = Image.open(u_thumb_path)
            im2 = im1.resize((150,40),Image.ANTIALIAS)
            im2.save(u_thumb_path,"JPEG")
            im3 = Image.open(u_thumb_path)
            im4 = Image.open(fi_thumb_path1)
            Image.Image.paste(im4,im3,(170, 120))
            im4.save(fi_thumb_path1,"JPEG")
            #thumb_save = await bot.save_file(path=fi_thumb_path1)
        
        else:
            Image.open(u_thumb_path).convert("RGB").save(u_thumb_path)
            img = Image.open(u_thumb_path)
            img.resize((320, 320))
            img.save(u_thumb_path)
            #thumb_save =await bot.save_file(path=u_thumb_path)
        c_time = time.time()
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_video(Config.TO_CHANNEL,video = file_path,caption = f"**{new_caption}**",thumb=fi_thumb_path1 or u_thumb_path,duration =duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
            os.remove(fi_thumb_path or u_thumb_path)
        except Exception as e:
            await ms.reply(e)
            os.remove(file_path)
            os.remove(fi_thumb_path or u_thumb_path)
    else:
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_video(Config.TO_CHANNEL,video = file_path,caption = f"**{new_caption}**",duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
        except Exception as e:
            await ms.reply(e)
            os.remove(file_path)
#@Client.on_callback_query(filters.regex("aud"))
async def aud1(bot,msg,txt,message):
    old_name = msg.audio.file_name
    if Config.REMOVE_WORD:
        file_name0 = old_name.rsplit(".",1)[0]
        new_name0 = re.sub(Config.REMOVE_WORD,"",file_name0)
        new_name = Config.CH_USERNAME+new_name0+"."+old_name.rsplit(".",1)[1]
    else:
        new_name=old_name
    if msg.audio.caption:
        if Config.REMOVE_CAPTION:
            new_caption = re.sub(Config.REMOVE_CAPTION,"",msg.audio.caption)
        else:
            new_caption = msg.audio.caption
    else:
        new_caption = new_name
    file_path = f"downloads/{new_name}"
    file = msg.audio
    ms = await txt.edit("``` Trying To Download...```")
    c_time = time.time()
    try:
        path = await bot.download_media(message = file , progress=progress_for_pyrogram,progress_args=( "``` Trying To Download...```",  ms, c_time   ))
    except Exception as e:
        await ms.reply_text(e)
        return
    splitpath = path.split("/downloads/")
    dow_file_name = splitpath[1]
    old_file_name =f"downloads/{dow_file_name}"
    os.rename(old_file_name,file_path)
    duration = 0
    metadata = extractMetadata(createParser(file_path))
    if metadata.has("duration"):
        duration = metadata.get('duration').seconds
    user_id = int(message.from_user.id)
    
    thumb = find(user_id)
    if thumb:
        ph_path = await bot.download_media(thumb)
        Image.open(ph_path).convert("RGB").save(ph_path)
        img = Image.open(ph_path)
        img.resize((320, 320))
        img.save(ph_path, "JPEG")
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_audio(Config.TO_CHANNEL,audio = file_path,caption = f"**{new_caption}**",thumb=ph_path,duration =duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
            os.remove(ph_path)
        except Exception as e:
            await ms.reply(e)
            os.remove(file_path)
            os.remove(ph_path)
    else:
        await ms.edit("```Trying To Upload```")
        c_time = time.time()
        try:
            await bot.send_audio(Config.TO_CHANNEL,audio = file_path,caption = f"**{new_caption}**",duration = duration, progress=progress_for_pyrogram,progress_args=( "```Trying To Uploading```",  ms, c_time   ))
            #await ms.delete()
            os.remove(file_path)
        except Exception as e:
            await ms.reply(e)
            os.remove(file_path)
async def fix_thumbnail1(thumb_path: str, height1: int = 0):
    if not height1:
        metadata = extractMetadata(createParser(thumb_path))
        if metadata.has("height"):
            height1 = metadata.get("height")
        else:
            height1 = 0
    Image.open(thumb_path).convert("RGB").save(thumb_path)
    img = Image.open(thumb_path)
    width, height = img.size
    left = 6
    top = height / 10
    right = 1
    bottom = 3 * height / 4
    img1=img.crop((0, 0, width, height-35))
    img1.save(thumb_path, "JPEG")
    img_resi = Image.open(thumb_path)
    img_resi1=img_resi.resize((320,180),Image.ANTIALIAS)
    img_resi1.save(thumb_path,"JPEG")
    # img_edit=Image.open(thumb_path)
    # draw = ImageDraw.Draw(img_edit)
    # req = requests.get("https://github.com/yogeshmirro/font/blob/main/ShortBaby-Mg2w.ttf?raw=true")
    # myFont = ImageFont.truetype(BytesIO(req.content), 20)
    # draw.text((width/2, height-60), "@seaofallmovies",fill =(255, 0, 0),font=myFont)
    # img_edit.save(thumb_path,"JPEG")
    return thumb_path
