
import os
import sys
from pathlib import Path

import asyncio

from loguru import logger
from aiogram import Bot, Dispatcher
from config import config

from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode

from src.handlers import load_routers
from src.middlewire.middlewire import PermissionsMiddleware

from src.handlers.bots import bots

async def main():
    bot = Bot(
        config.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dp = Dispatcher()

    for router in load_routers():
        dp.include_router(router)
    dp.update.middleware(PermissionsMiddleware())

    for i in config.owner:
        @dp.startup()
        async def on():
            logger.info("🔼 | Бот был поднят")

            await bot.send_message(
                chat_id=i,
                text="Хэллоу Эвэрiнiан :)"
            )
            await bots(bot)

        @dp.shutdown()
        async def off():
            logger.info("🔽 | Бот был выключен")
            await bot.send_message(
                chat_id=i,
                text="Бай-бай :)"
            )


    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())