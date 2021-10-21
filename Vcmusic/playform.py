import os
import asyncio
from pyrogram import Client
from Vcmusic.queues import QUEUE, add_to_queue
from config import bot, call_py, HNDLR, contact_filter
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import StreamType
from pytgcalls.types.input_stream import AudioPiped

@Client.on_message(filters.command(['playfrom'], prefixes=f"{HNDLR}"))
async def playfrom(client, m: Message):
   chat_id = m.chat.id
   if len(m.command) < 2:
      await m.reply("**USAGE:** \n\n`/playfrom [chat_id/username]` \n`/playfrom [chat_id/username] ; [no. of songs]`")
   else:
      args = m.text.split(maxsplit=1)[1]
      if ";" in args:
         chat = args.split(";")[0]
         limit = int(args.split(";")[1])
      else:
         chat = args
         limit = 10
      hmm = await m.reply(f"Searching the last **{limit}** Songs from `{chat}`")
      try:
         async for x in bot.search_messages(chat, limit=limit, filter="audio"):
               location = await x.download()
               if x.audio.title:
                  songname = x.audio.title[:30] + "..."
               else:
                  songname = x.audio.file_name[:30] + "..."
               link = x.link
               if chat_id in QUEUE:
                  add_to_queue(chat_id, songname, location, link, "Audio", 0)
               else:
                  await call_py.join_group_call(
                     chat_id,
                     AudioPiped(
                        location
                     ),
                     stream_type=StreamType().pulse_stream,
                  )
                  add_to_queue(chat_id, songname, location, link, "Audio", 0)
                  await m.reply(f"**Started Playing Songs from {chat} ▶** \n**🏷️ Name** : [{songname}]({link}) \n**☁️ Chat ID** : `{chat_id}`", disable_web_page_preview=True)
         await hmm.delete()
         await m.reply(f"Added **{limit}** SONGS to Queue")
      except Exception as e:
         await hmm.edit(f"**ERROR** \n`{e}`")
