import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from src.bot.config import settings, bot, logger
from src.bot.handler import common, couple

from src.bot.middleware.database import DataBaseSession
from src.storage.database import session_maker

dp = Dispatcher()

async def main():
    logger.info("Bot started")
    dp.include_routers(common.router, couple.couple_router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
