import os
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from pytgcalls import idle as pyidle
from config import bot, call_py

bot.start()
print("The Userbot Started")
call_py.start()
print("Vcmusic Client Started")
pyidle()
idle()
