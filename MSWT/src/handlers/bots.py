# src/handlers/bots.py
import os
import re
import subprocess
from typing import Optional
from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.filters.command import Command

bots_roter = Router()

from config import config

@bots_roter.message(Command('bots'))
async def bots(bot: Bot, message: Optional[Message] = None) -> None:
    text = ""

    for filename in os.listdir("."):
        if re.search(r"-start\.sh$", filename):
            try:
                process = subprocess.Popen(
                    f"sh {filename}",
                    stdout=subprocess.PIPE,
                    shell=True
                )
                process.daemon = True
                text += f"✅ File autostart {filename} started!\n"
            except Exception:
                text += f"❌ File autostart {filename} not started!\n"

        elif re.search(r"-start\.bat$", filename):
            try:
                process = subprocess.Popen(
                    filename,
                    stdout=subprocess.PIPE,
                    shell=True
                )
                process.daemon = True
                text += f"✅ File autostart {filename} started!\n"
            except Exception:
                text += f"❌ File autostart {filename} not started!\n"

    if not text:
        text = "File autostart not found..."

    if message:
        try:
            usernames = message.from_user.mention_html()
        except Exception:
            usernames = "ROOT"
    else:
        usernames = "ROOT"

    final_text = f"{usernames} trying to run autostart tasks\n{text}"

    for admin_id in config.owner:
        try:
            await bot.send_message(admin_id, final_text)
        except Exception:
            pass

