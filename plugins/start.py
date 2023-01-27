import os
from pyrogram.errors.exceptions.bad_request_400 import UserNotParticipant
import time
import asyncio
from configs import Config
from plugins.cb_data import doc,vid,aud
from pyrogram import Client, filters
from pyrogram.types import ( InlineKeyboardButton, InlineKeyboardMarkup,ForceReply)
import humanize
from plugins.batch import vid1,doc1,aud1
from helper.database import  insert ,find_one
from pyrogram.file_id import FileId
import datetime
#Part of Day --------------------
currentTime = datetime.datetime.now()

if currentTime.hour < 12:
	wish = "Good morning."
elif 12 <= currentTime.hour < 18:
	wish = 'Good afternoon.'
else:
	wish = 'Good evening.'

#-------------------------------

@Client.on_message(filters.private & filters.command(["start"]))
async def start(client,message):
	insert(int(message.chat.id))
	await message.reply_text(text =f"""
	Hello {wish} {message.from_user.first_name }
	__I am file renamer bot, Please sent any telegram 
	**Document Or Video** and enter new filename to rename it__
	""",reply_to_message_id = message.message_id ,  
	reply_markup=InlineKeyboardMarkup(
	 [[ InlineKeyboardButton("Support 🇮🇳" ,url="https://t.me/lntechnical") ], 
	[InlineKeyboardButton("Subscribe 🧐", url="https://youtube.com/c/LNtechnical") ]  ]))

@Client.on_message(filters.private & filters.command(["batch"]))
async def batch_handler(client,message):
    editable = await message.reply_text("`Processing...`", quote=True)
    txt = await client.send_message(from_channel, ".")
    last_msg_id = txt.message_id
    await txt.delete()
    start_time = datetime.datetime.now()
    txt1 = await editable.edit(text="Batch Shortening Started!")
    total = 0
    complete =0 
    empty = 0 
    failed = 0 
    failed_id = []
    try:
        
        for m in range(1,last_msg_id):
            msg = await client.get_messages(Config.FROM_CHANNEL,m)
            #print(msg)
            try:
                if msg.video:
                    #print(msg)
                    #print(msg.video.file_name)
                    fwd = await msg.forward(Config.LOG_CHANNEL)
                    mes = await fwd.reply("Renaming this file now...")
                    await vid1(client,msg,txt1,message)
                    complete+=1
                    await fwd.delete()
                    await mes.delete()
                    
                elif msg.document:
                    #print(msg)
                    #print(msg.document.file_name)
                    fwd = await msg.forward(Config.LOG_CHANNEL)
                    mes = await fwd.reply("Renaming this file now...")
                    await doc1(client,msg,txt1,message)
                    complete+=1
                    await fwd.delete()
                    await mes.delete()
                    
                elif msg.audio:
                    #print(msg)
                    #print(msg.audio.file_name)
                    fwd = await msg.forward(Config.LOG_CHANNEL)
                    mes = await fwd.reply("Renaming this file now...")
                    await aud1(client,msg,txt1,message)
                    complete+=1
                    await fwd.delete()
                    await mes.delete()
                
                else:
                    empty+=1 
                total+=1
            except Exception as e:
                #erre = await msg.forward(from_channel)
                await message.reply_text(f"this file id --- {msg.message_id} can't be rename due to errror ----- \n{e}")
                failed+=1 
                failed_id.append(msg.message_id)
                await fwd.delete()
                await mes.delete()
            if total % 10 == 0:
                msg = f"Batch renaming in Process !\n\nTotal: `{total}`\nSuccess: `{complete}`\nFailed: `{failed}`\nEmpty: `{empty}`\nFailed_id: `{failed_id}`"
                await txt1.edit((msg))
    
                    
    except Exception as e:
        await txt1.reply(f"batch Shortening failed due to ----- {e}",quote=True)
        print(e)
    finally:
        end_time = datetime.datetime.now()
        await asyncio.sleep(6)
        t = end_time - start_time
        time_taken = str(datetime.timedelta(seconds=t.seconds))
        msg = f"Batch Shortening Completed!\n\nTime Taken - `{time_taken}`\n\nTotal: `{total}`\nSuccess: `{complete}`\nFailed: `{failed}`\nEmpty: `{empty}`\nFailed_id: `{failed_id}`"
        await txt1.edit(msg)



@Client.on_message(filters.private &( filters.document | filters.audio | filters.video ))
async def send_doc(client,message):
       update_channel = Config.CHANNEL
       user_id = message.from_user.id
       if update_channel :
       	try:
       		await client.get_chat_member(update_channel, user_id)
       	except UserNotParticipant:
       		await message.reply_text("**__You are not subscribed my channel__** ",reply_to_message_id = message.message_id, reply_markup = InlineKeyboardMarkup([ [ InlineKeyboardButton("Support 🇮🇳" ,url=f"https://t.me/{update_channel}") ]   ]))
       		return
       date = message.date
       _used_date = find_one(user_id)
       used_date = _used_date["date"]      
       c_time = time.time()
       LIMIT = 240
       then = used_date+ LIMIT
       left = round(then - c_time)
       conversion = datetime.timedelta(seconds=left)
       ltime = str(conversion)
       if left > 0:
       	await app.send_chat_action(message.chat.id, "typing")
       	await message.reply_text(f"```Sorry Dude I am not only for YOU \n Flood control is active so please wait for {ltime}```",reply_to_message_id = message.message_id)
       else:
       	
       	media = await client.get_messages(message.chat.id,message.message_id)
       	file = media.document or media.video or media.audio 
       	dcid = FileId.decode(file.file_id).dc_id
       	filename = file.file_name
       	filesize = humanize.naturalsize(file.file_size)
       	fileid = file.file_id
       	await message.reply_text(f"""__What do you want me to do with this file?__\n**File Name** :- {filename}\n**File Size** :- {filesize}\n**Dc ID** :- {dcid} """,reply_to_message_id = message.message_id,reply_markup = InlineKeyboardMarkup([[ InlineKeyboardButton("📝 Rename",callback_data = "rename"),InlineKeyboardButton("✖️ Cancel",callback_data = "cancel")  ]]))
