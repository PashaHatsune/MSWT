import os
import random
import subprocess
from time import perf_counter

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router(name=__name__)

@router.message(Command("sh"))
async def sh_command(
    message: Message
) -> None:
    if message.reply_to_message:
        cmd_text = message.reply_to_message.text
    else:
        parts = message.text.split(maxsplit=1)
        if len(parts) < 2:
            await message.reply(
                text="<b>🤷‍♀️ | Specify the command in message text or in reply</b>"
            )
            return
        cmd_text = parts[1]

    status_msg = await message.reply(
        text="🏃‍♀️ | <b>Running...</b>"
    )

    cmd_obj = subprocess.Popen(
        cmd_text,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    text = f"$ <code>{cmd_text}</code>\n\n"
    try:
        start_time = perf_counter()
        stdout, stderr = cmd_obj.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        text += "<b>🤔 | Timeout expired (60 seconds)</b>"
        stdout = stderr = ""
    else:
        stop_time = perf_counter()
        if stdout:
            text += f"<b>✅ | Output:</b>\n<code>{stdout}</code>\n"
        if stderr:
            text += f"<b>❌ | Error:</b>\n<code>{stderr}</code>\n"

        elapsed_ms = round((stop_time - start_time) * 1000, 3)
        text += f"<b>🔼 | Completed in {elapsed_ms} milliseconds with code {cmd_obj.returncode}</b>"

    try:
        await status_msg.edit_text(text)
    except Exception:
        output = f"{stdout}\n\n{stderr}"
        filename = f"result_{random.randint(1, 9999)}.txt"

        with open(filename, "w") as file:
            file.write(output)

        await message.reply_document(
            document=open(filename, "rb"),
            caption=f"<code>{cmd_text}</code>"
        )

        os.remove(filename)

    cmd_obj.kill()