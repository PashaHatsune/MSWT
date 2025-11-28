from aiogram import Router
from aiogram.filters.command import Command
from aiogram.types import Message
from dependency_injector.wiring import Provide, inject

from ..container import Container
from ..services import UserService

router = Router(name=__name__)

@router.message(Command(*["start", "help"]))
@inject
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
4. Start sh module → /startsh (file.sh)
5. Stop sh module → /stopsh (file.sh)
6. Show sh logs → /logs (file.sh)
7. Restart systemctl → /restart
8. Restart server (**WARNING**) → /stop
==========
'''
    await message.reply(
        text=msg
    )
