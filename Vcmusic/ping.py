import os
import sys
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, call_py, HNDLR, contact_filter
from time import time
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


@Client.on_message(contact_filter & filters.command(['ping'], prefixes=f"{HNDLR}"))
async def ping(client, m: Message):
   start = time()
   current_time = datetime.utcnow()
   m_reply = await m.reply_text("`Ping...`")
   delta_ping = time() - start
   uptime_sec = (current_time - START_TIME).total_seconds()
   uptime = await _human_time_duration(int(uptime_sec))
   await m_reply.edit(f"🏓 `Pong!!`\n**Speed -** `{delta_ping * 1000:.3f} ms` \n**Uptime** - `{uptime}`")

@Client.on_message(contact_filter & filters.command(['help'], prefixes=f"{HNDLR}"))
async def help(client, m: Message):
   HELP = f"**💡 Help menu** \n\n__👥 All Users command__ (Anyone can Use): \n• `{HNDLR}play` \n• `{HNDLR}vplay` \n• `{HNDLR}stream` (For Radio links) \n• `{HNDLR}vstream` (For .m3u8 / live links) \n• `{HNDLR}playfrom [channel] ; [n]` - Plays last n songs from channel \n• `{HNDLR}playlist` / `{HNDLR}queue` \n• `{HNDLR}repo \n\n__👮 Sudo users command__ (Can only be accessed by You and Your Contacts): \n• `{HNDLR}ping` \n• `{HNDLR}skip` \n• `{HNDLR}pause` and `{HNDLR}resume` \n• `{HNDLR}stop` / `{HNDLR}end` \n• `{HNDLR}help`"
   await m.reply(HELP)

@Client.on_message(filters.command(['repo'], prefixes=f"{HNDLR}"))
async def repo(client, m: Message):
   KONTOL = f"⚙️ **Source code**\n• **😼 Github :** [Vcmusic-Userbot](https://github.com/KennedyProject/Vcmusic-Userbot)\n• 🗂️ **General Public License 3.0**"
   await m.reply(KONTOL, disable_web_page_preview=True)
