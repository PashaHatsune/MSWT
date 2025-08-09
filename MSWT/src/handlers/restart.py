import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import config

restart = Router()

@restart.message(Command("restart"))
async def restart_command(message: Message):
    for admin_id in config.owner:
        try:
            await message.bot.send_message(
                chat_id=admin_id,
                text=f"""{message.from_user.id} send command to server (restart with "restart_daemon.sh" script)"""
            )
        except Exception:
            pass

    os.system("sh restart_daemon.sh")
