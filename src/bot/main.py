import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.methods import DeleteWebhook

from src.bot.config import settings
from src.bot.handler import common

from src.bot.middleware.database import DataBaseSession
from src.bot.storage.database import session_maker

bot = Bot(token=settings.bot_token)
dp = Dispatcher()

logging.basicConfig(
   level=logging.INFO,
   format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
   handlers=[
       logging.StreamHandler(),
   ]
)

logger = logging.getLogger(__name__)

async def main():
    logger.info("Bot started")
    dp.include_routers(common.router)
    dp.update.middleware(DataBaseSession(session_pool=session_maker))
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
