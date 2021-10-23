import os
import cv2
from pyrogram import Client
from pyrogram import filters
from pyrogram.types import Message
from PIL import Image
from config import bot, HNDLR, OWNER_ID


@Client.on_message(filters.user(OWNER_ID) & filters.command(['tiny'], prefixes=f"{HNDLR}"))
async def _(client, m: Message):
    reply = await m.get_reply_message()
    if not (reply and (reply.media)):
        await m.edit("`Please Reply To Sticker`")
        return
    xx = await m.edit("`Processing Tiny....`")
    ik = await bot.download_media(reply)
    im1 = Image.open("resources/blank_background.png")
    if ik.endswith(".tgs"):
        await m.client.download_media(reply, "kntl.tgs")
        os.system("lottie_convert.py kntl.tgs json.json")
        json = open("json.json", "r")
        jsn = json.read()
        json.close()
        jsn = jsn.replace("512", "2000")
        open("json.json", "w").write(jsn)
        os.system("lottie_convert.py json.json kntl.tgs")
        file = "kntl.tgs"
        os.remove("json.json")
    elif ik.endswith((".gif", ".mp4")):
        iik = cv2.VideoCapture(ik)
        dani, busy = iik.read()
        cv2.imwrite("i.png", busy)
        fil = "i.png"
        im = Image.open(fil)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove(fil)
        os.remove("k.png")
    else:
        im = Image.open(ik)
        z, d = im.size
        if z == d:
            xxx, yyy = 200, 200
        else:
            t = z + d
            a = z / t
            b = d / t
            aa = (a * 100) - 50
            bb = (b * 100) - 50
            xxx = 200 + 5 * aa
            yyy = 200 + 5 * bb
        k = im.resize((int(xxx), int(yyy)))
        k.save("k.png", format="PNG", optimize=True)
        im2 = Image.open("k.png")
        back_im = im1.copy()
        back_im.paste(im2, (150, 0))
        back_im.save("o.webp", "WEBP", quality=95)
        file = "o.webp"
        os.remove("k.png")
    await m.client.send_file(m.chat_id, file, reply_to=m.reply_to_msg_id)
    await xx.delete()
    os.remove(file)
    os.remove(ik)
