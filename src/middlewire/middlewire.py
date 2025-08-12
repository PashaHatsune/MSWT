from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.enums.chat_type import ChatType
from aiogram.types import TelegramObject
from loguru import logger

from ...config import config


class PermissionsMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ) -> Any:
        user = data.get("event_from_user")
        bot = data.get("bot")

        user_id = user.id if user else None
        chat = data.get("event_chat")

        # Проверяем, что чат личный (private)
        if chat is None or chat.type != ChatType.PRIVATE:
            return await handler(event, data)

        if user_id in config.owner:
            return await handler(event, data)
        else:
            if bot and user_id:
                logger.warning(f"У {user_id} нет доступа. Пропускаю...")
                await bot.send_message(
                    chat_id=user_id,
                    text="К сожалению, у вас нет доступа к боту."
                )
            return
