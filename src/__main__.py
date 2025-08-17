import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums.parse_mode import ParseMode
from loguru import logger

from .container import Container
from .handlers import load_routers, start_background_tasks
from .handlers.bots import bots
from .middlewire.middlewire import PermissionsMiddleware
from .settings import config

logger.add(
    "logs.log",
    rotation="10 MB",
    enqueue=True,
    backtrace=True,
    diagnose=True
)

async def main():
    bot = Bot(
        token=config.telegram.token.get_secret_value(),
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )

    dp = Dispatcher()
    
    dp.message.middleware(PermissionsMiddleware())

    for router in load_routers():
        dp.include_router(router)

    for owner_id in config.telegram.owners:

        @dp.startup()
        async def on_startup(owner_id=owner_id):
            logger.info("🔼 | Bot is start")
            await bot.send_message(
                chat_id=owner_id,
                text="🔼 | <b>Bot is start</b>"
            )
            await bots(bot)

        @dp.shutdown()
        async def on_shutdown(owner_id=owner_id):
            logger.info("🔽 | The bot is disabled")
            await bot.send_message(
                chat_id=owner_id,
                text="🔽 | <b>The bot is disabled</b>"
            )


    container = Container(bot=bot)
    container.wire(
        modules=[__name__], packages=[
            '.handlers',
            '.handlers.tasks'
            ]
    )
    asyncio.create_task(start_background_tasks(bot))

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
