# Porter from Userge (https://github.com/UsergeTeam/Userge/
# Ported by KennedyProject (https://github.com/KennedyProject)
# For Vcmusic-Userbot 2021

import io
import os
import random
import datetime
import config
import asyncio
from time import sleep
from PIL import Image
from pyrogram import emoji
from pyrogram.types import Message
from pyrogram import Client, filters
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.errors import YouBlockedUser, StickersetInvalid

from config import bot, HNDLR, OWNER_ID

@Client.on_message(filters.user(OWNER_ID) & filters.command(['kang'], prefixes=f"{HNDLR}"))
async def packinfo(client, message: Message):
    engine = message.Engine
    pablo = await message.edit(f"`{random.choice(KANGING_STR)}`"))
    if not message.reply_to_message:
        await pablo.edit(engine.get_string("`Reply to sticker to kang it`").format("Sticker"))
        return
    Hell = get_text(message)
    name = ""
    pack = 1
    nm = message.from_user.username
    if nm:
        nam = message.from_user.username
        name = nam[1:]
    else:
        name = message.from_user.first_name
    packname = f"@{nm} Kang Pack {pack}"
    packshortname = f"{message.from_user.id}_{pack}"
    non = [None, "None"]
    emoji = "😁"
    try:
        Hell = Hell.strip()
        if Hell.isalpha():
            emoji = "😁"
        elif not Hell.isnumeric():
            emoji = Hell
    except:
        emoji = "😁"
    exist = None
    is_anim = False
    if message.reply_to_message.sticker:
        if not Hell:
            emoji = message.reply_to_message.sticker.emoji or "😁"
        is_anim = message.reply_to_message.sticker.is_animated
        if is_anim:
            packshortname += "_animated"
            packname += " Animated"
        if message.reply_to_message.sticker.mime_type == "application/x-tgsticker":
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
        else:
            cool = await convert_to_image(message, client)
            if not cool:
                await pablo.edit(engine.get_string("`Unsuported file`").format("Media"))
                return
            file_name = resize_image(cool)
    elif message.reply_to_message.document:
        if message.reply_to_message.document.mime_type == "application/x-tgsticker":
            is_anim = True
            packshortname += "_animated"
            packname += " Animated"
            file_name = await message.reply_to_message.download("AnimatedSticker.tgs")
    else:
        cool = await convert_to_image(message, client)
        if not cool:
            await pablo.edit(engine.get_string("`Unsupported file`").format("Media"))
            return
        file_name = resize_image(cool)
    try:
        exist = await client.send(
            GetStickerSet(stickerset=InputStickerSetShortName(short_name=packshortname))
        )
    except StickersetInvalid:
        pass
    if exist:
        try:
            await client.send_message("stickers", "/addsticker")
        except YouBlockedUser:
            await pablo.edit("`Please Unblock @Stickers`")
            await client.unblock_user("stickers")
        await client.send_message("stickers", packshortname)
        await asyncio.sleep(0.2)
        limit = "50" if is_anim else "120"
        messi = (await client.get_history("stickers", 1))[0]
        while limit in messi.text:
            pack += 1
            prev_pack = int(pack) - 1
            await pablo.edit(engine.get_string("Kang_Full").format(prev_pack, pack))
            packname = f"@{nm} Kang Pack {pack}"
            packshortname = f"{message.from_user.id}_{pack}"
            if is_anim:
                packshortname += "_animated"
                packname += " Animated"
            await client.send_message("stickers", packshortname)
            await asyncio.sleep(0.2)
            messi = (await client.get_history("stickers", 1))[0]
            if messi.text == "Invalid pack selected.":
                if is_anim:
                    await client.send_message("stickers", "/newanimated")
                else:
                    await client.send_message("stickers", "/newpack")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packname)
                await asyncio.sleep(0.2)
                await client.send_document("stickers", file_name)
                await asyncio.sleep(1)
                await client.send_message("stickers", emoji)
                await asyncio.sleep(0.5)
                await client.send_message("stickers", "/publish")
                if is_anim:
                    await client.send_message("stickers", f"<{packname}>")
                await client.send_message("stickers", "/skip")
                await asyncio.sleep(0.5)
                await client.send_message("stickers", packshortname)
                await pablo.edit(engine.get_string("Added_Sticker").format(emoji, packshortname))
                return
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/done")
        await pablo.edit(engine.get_string("Added_Sticker").format(emoji, packshortname))
    else:
        if is_anim:
            await client.send_message("stickers", "/newanimated")
        else:
            await client.send_message("stickers", "/newpack")
        await client.send_message("stickers", packname)
        await asyncio.sleep(0.2)
        await client.send_document("stickers", file_name)
        await asyncio.sleep(1)
        await client.send_message("stickers", emoji)
        await asyncio.sleep(0.5)
        await client.send_message("stickers", "/publish")
        await asyncio.sleep(0.5)
        if is_anim:
            await client.send_message("stickers", f"<{packname}>")
        await client.send_message("stickers", "/skip")
        await asyncio.sleep(0.5)
        await client.send_message("stickers", packshortname)
        await pablo.edit(engine.get_string("Added_Sticker").format(emoji, packshortname))
        if os.path.exists(file_name):
            os.remove(file_name)


def resize_image(image):
    im = Image.open(image)
    if (im.width and im.height) < 512:
        size1 = im.width
        size2 = im.height
        if im.width > im.height:
            scale = 512 / size1
            size1new = 512
            size2new = size2 * scale
        else:
            scale = 512 / size2
            size1new = size1 * scale
            size2new = 512
        size1new = math.floor(size1new)
        size2new = math.floor(size2new)
        sizenew = (size1new, size2new)
        im = im.resize(sizenew)
    else:
        maxsize = (512, 512)
        im.thumbnail(maxsize)
    file_name = "Sticker.png"
    im.save(file_name, "PNG")
    if os.path.exists(image):
        os.remove(image)
    return file_name


KANGING_STR = (
    "Using Witchery to kang this sticker...",
    "Plagiarising hehe...",
    "Inviting this sticker over to my pack...",
    "Kanging this sticker...",
    "Hey that's a nice sticker!\nMind if I kang?!..",
    "hehe me stel ur stikér\nhehe.",
    "Ay look over there (☉｡☉)!→\nWhile I kang this...",
    "Roses are red violets are blue, kanging this sticker so my pacc looks cool",
    "Imprisoning this sticker...",
    "Mr.Steal Your Sticker is stealing this sticker... ")
