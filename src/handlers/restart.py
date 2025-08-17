import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message


from dependency_injector.wiring import inject, Provide
from ..services import UserService
from ..container import Container


restart = Router()

@inject
@restart.message(Command("restart"))
async def restart_command(
    message: Message,
    user_service: UserService = Provide[
        Container.user_service
    ]
) -> None:
    for admin_id in user_service.config.telegram.owners:
        try:
            await message.bot.send_message(
                chat_id=admin_id,
                text=f"""🤔 | {message.from_user.id} send command to server (restart with "restart_daemon.sh" script)"""
            )
        except Exception:
            pass

    os.system("sh restart-daemon.sh")
