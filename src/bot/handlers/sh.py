import os
import random
import subprocess
from time import perf_counter

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import FSInputFile, Message

router = Router(name=__name__)


@router.message(Command("sh"))
async def sh_command(message: Message) -> None:
    cmd_text = (message.reply_to_message.text if message.reply_to_message
                else (message.text.split(maxsplit=1)[1] if len(message.text.split(maxsplit=1)) > 1 else None))
    if not cmd_text:
        await message.reply("<b>🤷‍♀️ | Specify command text, reply, or file path</b>")
        return

    file_path = os.path.expanduser(cmd_text)
    # Если это существующий файл — отправляем его
    if os.path.isfile(file_path):
        await message.reply_document(
            FSInputFile(
                path=file_path
            )
        )
        return

    status_msg = await message.reply("🏃‍♀️ | <b>Running...</b>")

    proc = subprocess.Popen(
        cmd_text,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    start_time = perf_counter()
    try:
        stdout, stderr = proc.communicate(timeout=60)
    except subprocess.TimeoutExpired:
        stdout = stderr = ""
        text = "<b>🤔 | Timeout expired (60 seconds)</b>"
    else:
        elapsed_ms = round((perf_counter() - start_time) * 1000, 3)
        text = f"$ <code>{cmd_text}</code>\n\n"
        if stdout: text += f"<b>✅ | Output:</b>\n<code>{stdout}</code>\n"
        if stderr: text += f"<b>❌ | Error:</b>\n<code>{stderr}</code>\n"
        text += f"<b>🔼 | Completed in {elapsed_ms} ms with code {proc.returncode}</b>"

    try:
        await status_msg.edit_text(text)
    except Exception:
        filename = f"result_{random.randint(1,9999)}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(f"{stdout}\n{stderr}")
        await message.reply_document(
            FSInputFile(
                path=filename,
                filename='log.txt'
            ),
            caption=f"<code>{cmd_text}</code>"
        )
        os.remove(filename)

    proc.kill()
