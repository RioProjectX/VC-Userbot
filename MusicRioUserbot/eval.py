import os
import sys
import re
import traceback
import subprocess
from io import StringIO
from pyrogram import Client, filters
from pyrogram.types import Message
from config import HNDLR, bot as USER

async def aexec(code, client, m: Message):
    exec(
        "async def __aexec(client, m: Message): "
        + "".join(f"\n {a}" for a in code.split("\n"))
    )
    return await locals()["__aexec"](client, m)

@Client.on_message(filters.command(["eval"], prefixes=f"{HNDLR}"))
async def executor(client, m: Message):
    if len(m.command) < 2:
        return await m.edit(text="`please give me some command to execute.`")
    try:
        cmd = m.text.split(" ", maxsplit=1)[1]
    except IndexError:
        return await m.delete()
    old_stderr = sys.stderr
    old_stdout = sys.stdout
    redirected_output = sys.stdout = StringIO()
    redirected_error = sys.stderr = StringIO()
    stdout, stderr, exc = None, None, None
    try:
        await aexec(cmd, client, m)
    except Exception:
        exc = traceback.format_exc()
    stdout = redirected_output.getvalue()
    stderr = redirected_error.getvalue()
    sys.stdout = old_stdout
    sys.stderr = old_stderr
    evaluation = ""
    if exc:
        evaluation = exc
    elif stderr:
        evaluation = stderr
    elif stdout:
        evaluation = stdout
    else:
        evaluation = "Success"
    final_output = f"**OUTPUT**:\n\n```{evaluation.strip()}```"
    if len(final_output) > 4096:
        filename = "output.txt"
        with open(filename, "w+", encoding="utf8") as out_file:
            out_file.write(str(evaluation.strip()))
        await m.reply_document(
            document=filename,
            caption=f"**INPUT:**\n`{cmd[0:980]}`\n\n**OUTPUT:**\n`Attached Document`",
            quote=False,
        )
        await m.delete()
        os.remove(filename)
    else:
        await m.edit(text=final_output)


@Client.on_message(filters.command(["sh"], prefixes=f"{HNDLR}"))
async def shellrunner(client, m: Message):
    if len(m.command) < 2:
        return await m.edit(text="`Give a command to running`")
    text = m.text.split(None, 1)[1]
    if "\n" in text:
        code = text.split("\n")
        output = ""
        for x in code:
            shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", x)
            try:
                process = subprocess.Popen(
                    shell,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                )
            except Exception as err:
                print(err)
                await m.edit(m, text=f"**ERROR:**\n```{err}```")
            output += f"**{code}**\n"
            output += process.stdout.read()[:-1].decode("utf-8")
            output += "\n"
    else:
        shell = re.split(""" (?=(?:[^'"]|'[^']*'|"[^"]*")*$)""", text)
        for a in range(len(shell)):
            shell[a] = shell[a].replace('"', "")
        try:
            process = subprocess.Popen(
                shell,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
        except Exception as err:
            print(err)
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errors = traceback.format_exception(
                etype=exc_type,
                value=exc_obj,
                tb=exc_tb,
            )
            return await m.edit(
                text=f"**ERROR:**\n\n```{''.join(errors)}```"
            )
        output = process.stdout.read()[:-1].decode("utf-8")
    if str(output) == "\n":
        output = None
    if output:
        if len(output) > 4096:
            with open("output.txt", "w+") as file:
                file.write(output)
            await app.send_document(
                m.chat.id,
                "output.txt",
                reply_to_message_id=m.message_id,
                caption="`Output`",
            )
            return os.remove("output.txt")
        await m.edit(text=f"**OUTPUT:**\n\n```{output}```")
    else:
        await m.edit(text="**OUTPUT: **\n`No output`")
