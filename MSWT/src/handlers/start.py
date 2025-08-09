from aiogram import Router
from aiogram.types import Message
from aiogram.filters.command import Command

from config import config

start = Router()

@start.message(Command(*["start", "help"]))
async def help_menu(message: Message) -> None:
    msg = f'''
AdminPanel by PashaHatsune.t.me — fork by A9FM
Version: {config.version}
==========
1. RAM/CPU/ROM → /info
2. Bash Terminal → /sh (command)
3. Start Bots → /bots
4. Restart systemctl → /restart
5. Restart server (**WARNING**) → /stop
==========
'''
    await message.reply(
        chat_id=message.chat.id,
        text=msg
    )
