from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.message.common import start_message
from src.bot.keyboard.common import start_keyboard

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    kb = start_keyboard()
    await message.answer(start_message, reply_markup=kb)
