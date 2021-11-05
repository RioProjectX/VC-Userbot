import os
from pyrogram import Client, idle
from pytgcalls import PyTgCalls
from pytgcalls import idle as pyidle
from config import bot, call_py

print("The Userbot Started")
bot.start()

print("VC Music Client Started")
call_py.start()

pyidle()
idle()
