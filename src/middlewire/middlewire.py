from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject
from dependency_injector.wiring import Provide, inject
from loguru import logger

from ..container import Container
from ..services import UserService


class PermissionsMiddleware(BaseMiddleware):
    @inject
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
        user_service: UserService = Provide[
        Container.user_service
    ]
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
        if user_id in user_service.config.telegram.owners:
            return await handler(event, data)

        # Если не владелец и это команда
        if bot:
            logger.warning(f"У {user_id} нет доступа. Пропускаю...")
            await bot.send_message(
                chat_id=chat_id,
                text="К сожалению, у вас нет доступа к боту."
            )
        return
