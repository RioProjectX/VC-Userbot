import os
import asyncio
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from config import bot, HNDLR, contact_filter

@Client.on_message(contact_filter & filters.command(['p'], prefixes=f"{HNDLR}"))
async def asa(client, m: Message):
   await m.edit("`Assalamualaikum wr.rb`")

@Client.on_message(contact_filter & filters.command(['l'], prefixes=f"{HNDLR}"))
async def wasa(client, m: Message):
   await m.edit("`Waalaikumussalam wr.rb`")

