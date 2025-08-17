from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from loguru import logger

from ..settings.main import config


class PermissionsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        # Работает только с сообщениями
        if not isinstance(event, Message):
            return await handler(event, data)

        # Если это не команда, пропускаем
        if not event.text or not event.text.startswith('/'):
            return await handler(event, data)

        user_id = event.from_user.id
        chat_id = event.chat.id
        bot = data.get("bot")

        # Проверяем владельца
        if user_id in config.owner:
            return await handler(event, data)

        # Если не владелец и это команда
        if bot:
            logger.warning(f"У {user_id} нет доступа. Пропускаю...")
            await bot.send_message(
                chat_id=chat_id,
                text="К сожалению, у вас нет доступа к боту."
            )
        return
