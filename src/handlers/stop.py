import os

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from ..container import Container
from ..services import UserService

router = Router(name=__name__)

@inject
@router.message(Command("stop"))
async def stop_command(
    message: Message,
    user_service: UserService = Provide[
        Container.user_service
    ]
) -> None:
    for admin_id in user_service.config.telegram.owners:
        await message.bot.send_message(
            chat_id=admin_id,
            text=f"🔄 | <b>{message.from_user.id} restarting server...</b>"
        )

    os.system("sudo reboot")
