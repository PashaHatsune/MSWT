
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from .config import config
from .src.handlers import load_routers, start_background_tasks
from .src.handlers.bots import bots
from .src.middlewire.middlewire import PermissionsMiddleware

logger.add(
    "logs.log",
    rotation="10 MB", 
    enqueue=True,
    backtrace=True,
    diagnose=True
)

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
            logger.info("🔼 | Bot is start")

            await bot.send_message(
                chat_id=i,
                text="🔼 | <b>Bot is start</b>"
            )
            await bots(bot)

        @dp.shutdown()
        async def off():
            logger.info("🔽 | The bot is disabled")
            await bot.send_message(
                chat_id=i,
                text="🔽 | <b>The bot is disabled</b>"
            )


    asyncio.create_task(start_background_tasks(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


