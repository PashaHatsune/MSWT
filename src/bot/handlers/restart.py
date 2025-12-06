import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject
from aiogram.exceptions import TelegramBadRequest
from ..container import Container
from ..services import UserService
from loguru import logger
restart = Router()

@restart.message(Command("restart"))
@inject
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
        except TelegramBadRequest:
            logger.error(f"Не удалось отправить сообщение {admin_id}")


    os.system("sh restart-daemon.sh")
