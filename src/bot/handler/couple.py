from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.filters import StateFilter
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboard.common import cancel_keyboard
import src.bot.storage.couple as database


couple_router = Router()

@couple_router.callback_query(F.data == "create_couple")
async def create_couple(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    kb = cancel_keyboard()
    couple = await database.create_couple(
        session=session,
        telegram_id=callback.from_user.id
    )

    await callback.message.answer(
        f"✨ Ваша пара успешно создана!\n\n"
        f"Ваш секретный код для входа в команду:\n"
        f"`{couple.token}`\n\n"
        f"Передайте его партнёру и начните приключение вместе!",
        reply_markup=kb,
        parse_mode=ParseMode.MARKDOWN,
    )
