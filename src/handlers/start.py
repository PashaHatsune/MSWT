from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message

from dependency_injector.wiring import inject, Provide
from ..services import UserService
from ..container import Container


router = Router(name=__name__)

@inject
@router.message(Command(*["start", "help"]))
async def help_menu(
    message: Message,
    user_service: UserService = Provide[
        Container.user_service
    ]

) -> None:
    msg = f'''
AdminPanel by PashaHatsune.t.me — fork by A9FM
Version: {user_service.config.meta.version}
==========
1. RAM/CPU/ROM → /info
2. Bash Terminal → /sh (command)
3. Start Bots → /bots
4. Restart systemctl → /restart
5. Restart server (**WARNING**) → /stop
==========
'''
    await message.reply(
        text=msg
    )
