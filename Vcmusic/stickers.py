# Porter from Userge (https://github.com/UsergeTeam/Userge/
# Ported by KennedyProject (https://github.com/KennedyProject)
# For Vcmusic-Userbot 2021

import io
import os
import random

from PIL import Image
from pyrogram import emoji
from pyrogram import Client, filters, Message
from pyrogram.raw.functions.messages import GetStickerSet
from pyrogram.raw.types import InputStickerSetShortName
from pyrogram.errors import YouBlockedUser, StickersetInvalid

from config import bot, HNDLR, OWNER_ID, DOWN_PATH

@Client.on_message(filters.user(OWNER_ID) & filters.command(['kang'], prefixes=f"{HNDLR}"))
async def kang_(client, m: Message):
    """ kang a sticker """
    user = await client.get_me()
    replied = m.reply_to_message
    photo = None
    _emoji = None
    emoji_ = ""
    is_anim = False
    resize = False
    if replied and replied.media:
        if replied.photo:
            resize = True
        elif replied.document and "image" in replied.document.mime_type:
            resize = True
        elif replied.document and "tgsticker" in replied.document.mime_type:
            is_anim = True
        elif replied.sticker:
            if not replied.sticker.file_name:
                await m.edit("`Sticker has no Name!`")
                return
            emoji_ = replied.sticker.emoji
            is_anim = replied.sticker.is_animated
            if not replied.sticker.file_name.endswith('.tgs'):
                resize = True
        else:
            await m.edit("`Unsupported File!`")
            return
        await m.edit(f"`{random.choice(KANGING_STR)}`")
        photo = await bot.download_media(message=replied,
                                            file_name=DOWN_PATH)
    else:
        await m.err("`I can't kang that...`")
        return
    if photo:
        args = m.filtered_input_str.split(' ')
        pack = 1
        if len(args) == 2:
            _emoji, pack = args
        elif len(args) == 1:
            if args[0].isnumeric():
                pack = int(args[0])
            else:
                _emoji = args[0]

        if _emoji is not None:
            _saved = emoji_
            for k in _emoji:
                if k and k in (
                    getattr(emoji, a) for a in dir(emoji) if not a.startswith("_")
                ):
                    emoji_ += k
            if _saved and _saved != emoji_:
                emoji_ = emoji_[len(_saved):]
        if not emoji_:
            emoji_ = "🤔"

        u_name = user.username
        if u_name:
            u_name = "@" + u_name
        else:
            u_name = user.first_name or user.id
        packname = f"a{user.id}_by_userge_{pack}"
        custom_packnick = f"{u_name}'s kang pack"
        packnick = f"{custom_packnick} Vol.{pack}"
        cmd = '/newpack'
        if resize:
            photo = resize_photo(photo)
        if is_anim:
            packname += "_anim"
            packnick += " (Animated)"
            cmd = '/newanimated'
        exist = False
        try:
            exist = await m.bot.send(
                GetStickerSet(
                    stickerset=InputStickerSetShortName(
                        short_name=packname)))
        except StickersetInvalid:
            pass
        if exist is not False:
            async with bot.conversation('Stickers', limit=30) as conv:
                try:
                    await conv.send_message('/addsticker')
                except YouBlockedUser:
                    await m.edit('first **unblock** @Stickers')
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                msg = await conv.get_response(mark_read=True)
                limit = "50" if is_anim else "120"
                while limit in msg.text:
                    pack += 1
                    packname = f"a{user.id}_by_userge_{pack}"
                    packnick = f"{custom_packnick} Vol.{pack}"
                    if is_anim:
                        packname += "_anim"
                        packnick += " (Animated)"
                    await m.edit("`Switching to Pack " + str(pack) +
                                       " due to insufficient space`")
                    await conv.send_message(packname)
                    msg = await conv.get_response(mark_read=True)
                    if msg.text == "Invalid pack selected.":
                        await conv.send_message(cmd)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packnick)
                        await conv.get_response(mark_read=True)
                        await conv.send_document(photo)
                        await conv.get_response(mark_read=True)
                        await conv.send_message(emoji_)
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/publish")
                        if is_anim:
                            await conv.get_response(mark_read=True)
                            await conv.send_message(f"<{packnick}>", parse_mode=None)
                        await conv.get_response(mark_read=True)
                        await conv.send_message("/skip")
                        await conv.get_response(mark_read=True)
                        await conv.send_message(packname)
                        await conv.get_response(mark_read=True)
                        if '-d' in m.flags:
                            await m.delete()
                        else:
                            out = "__kanged__" if '-s' in m.flags else \
                                f"[kanged](t.me/addstickers/{packname})"
                            await m.edit(f"**Sticker** {out} __in a Different Pack__**!**")
                        return
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await m.edit("`Failed to add sticker, use` @Stickers "
                                 "`bot to add the sticker manually.`")
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message('/done')
                await conv.get_response(mark_read=True)
        else:
            await m.edit("`Brewing a new Pack...`")
            async with bot.conversation('Stickers') as conv:
                try:
                    await conv.send_message(cmd)
                except YouBlockedUser:
                    await m.edit('first **unblock** @Stickers')
                    return
                await conv.get_response(mark_read=True)
                await conv.send_message(packnick)
                await conv.get_response(mark_read=True)
                await conv.send_document(photo)
                rsp = await conv.get_response(mark_read=True)
                if "Sorry, the file type is invalid." in rsp.text:
                    await m.edit("`Failed to add sticker, use` @Stickers "
                                       "`bot to add the sticker manually.`")
                    return
                await conv.send_message(emoji_)
                await conv.get_response(mark_read=True)
                await conv.send_message("/publish")
                if is_anim:
                    await conv.get_response(mark_read=True)
                    await conv.send_message(f"<{packnick}>", parse_mode=None)
                await conv.get_response(mark_read=True)
                await conv.send_message("/skip")
                await conv.get_response(mark_read=True)
                await conv.send_message(packname)
                await conv.get_response(mark_read=True)
        if '-d' in m.flags:
            await m.delete()
        else:
            out = "__kanged__" if '-s' in m.flags else \
                f"[kanged](t.me/addstickers/{packname})"
            await m.edit(f"**Sticker** {out}**!**")
        if os.path.exists(str(photo)):
            os.remove(photo)

def resize_photo(photo: str) -> io.BytesIO:
    """ Resize the given photo to 512x512 """
    image = Image.open(photo)
    maxsize = 512
    scale = maxsize / max(image.width, image.height)
    new_size = (int(image.width*scale), int(image.height*scale))
    image = image.resize(new_size, Image.LANCZOS)
    resized_photo = io.BytesIO()
    resized_photo.name = "sticker.png"
    image.save(resized_photo, "PNG")
    os.remove(photo)
    return resized_photo


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
