import os
import sys
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, OWNER_ID
from time import time
from time import sleep
from datetime import datetime

# System Uptime
START_TIME = datetime.utcnow()
TIME_DURATION_UNITS = (
    ('Week', 60 * 60 * 24 * 7),
    ('Day', 60 * 60 * 24),
    ('Hour', 60 * 60),
    ('Min', 60),
    ('Sec', 1)
)
async def _human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in TIME_DURATION_UNITS:
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{} {}{}'
                         .format(amount, unit, "" if amount == 1 else "s"))
    return ', '.join(parts)


@Client.on_message(filters.user(OWNER_ID) & filters.command(['ping'], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
   start = time()
   current_time = datetime.utcnow()
   m_reply = await m.edit("`Pinging...`")
   delta_ping = time() - start
   await m_reply.edit("**0% ▒▒▒▒▒▒▒▒▒▒**")
   await m_reply.edit("**20% ██▒▒▒▒▒▒▒▒**")
   await m_reply.edit("**40% ████▒▒▒▒▒▒**")
   await m_reply.edit("**60% ██████▒▒▒▒**")
   await m_reply.edit("**80% ████████▒▒**")
   await m_reply.edit("**100% ██████████**")
   await asyncio.sleep(1)
   end = datetime.now()
   uptime_sec = (current_time - START_TIME).total_seconds()
   uptime = await _human_time_duration(int(uptime_sec))
   await m_reply.edit(f"🏓 `Pong!!`\n**Speed -** `{delta_ping * 1000:.3f} ms` \n**Uptime** - `{uptime}`")

@Client.on_message(filters.user(OWNER_ID) & filters.command(['pink'], prefixes=f"{HNDLR}"))
async def pong(client, m: Message):
   start = time()
   current_time = datetime.utcnow()
   pong = await m.edit("`KONTOL...`")
   delta_ping = time() - start
   await pong.edit("8✊===D")
   await pong.edit("8=✊==D")
   await pong.edit("8==✊=D")
   await pong.edit("8===✊D")
   await pong.edit("8==✊=D")
   await pong.edit("8=✊==D")
   await pong.edit("8✊===D")
   await pong.edit("8=✊==D")
   await pong.edit("8==✊=D")
   await pong.edit("8===✊D")
   await pong.edit("8==✊=D")
   await pong.edit("8=✊==D")
   await pong.edit("8✊===D")
   await pong.edit("8=✊==D")
   await pong.edit("8==✊=D")
   await pong.edit("8===✊D")
   await pong.edit("8===✊D💦")
   await pong.edit("8====D💦💦")
   await pong.edit("**CROOTTTT PINGGGG!**")
   end = datetime.now()
   uptime_sec = (current_time - START_TIME).total_seconds()
   uptime = await _human_time_duration(int(uptime_sec))
   await pong.edit(
       f"**KONTOL!! **\n✨ **NGENTOT** : {delta_ping * 1000:.3f} ms\n**⏱️ Bot Uptime** : {uptime}")

@Client.on_message(filters.user(OWNER_ID) & filters.command(['help'], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
   HELP = f"**💡 Help menu** \n\n📚 __All Commands__ : \n• `{HNDLR}play` \n• `{HNDLR}vplay` \n• `{HNDLR}stream` (For Radio links) \n• `{HNDLR}vstream` (For .m3u8 / live links) \n• `{HNDLR}playfrom [channel] ; [n]` - Plays last n songs from channel \n• `{HNDLR}playlist` / `{HNDLR}queue` \n• `{HNDLR}repo \n• `{HNDLR}ping` \n• `{HNDLR}skip` \n• `{HNDLR}pause` and `{HNDLR}resume` \n• `{HNDLR}stop` / `{HNDLR}end` \n• `{HNDLR}help`\n\n📝 Notes: Your contacts is sudo users, can control your userbot musicplayer"
   await m.edit(HELP)

@Client.on_message(filters.user(OWNER_ID) & filters.command(['repo'], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
   KONTOL = f"⚙️ **Source code**\n• **😼 Github :** [Vcmusic-Userbot](https://github.com/KennedyProject/Vcmusic-Userbot)\n• 🗂️ **GPL - 3.0 License**"
   await m.edit(KONTOL, disable_web_page_preview=True)
