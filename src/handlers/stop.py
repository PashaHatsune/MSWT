import os

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from config import config

stop = Router()

@stop.message(Command("stop"))
async def stop_command(message: Message) -> None:
    for admin_id in config.owner:
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"🔄 | <b>{message.from_user.id} restarting server...</b>"
        )

    os.system("sudo reboot")
