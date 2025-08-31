from aiogram import Router, F
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext

from src.bot.keyboard.common import start_keyboard

router = Router()

@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    kb = start_keyboard()
    await message.answer("💖 Добро пожаловать в Heart 2 Heart!\n\n"
        "Каждый вопрос здесь - это маленький шаг навстречу пониманию, доверию и близости.\n\n"
        "Отвечайте вместе, открывайтесь друг другу и создавайте моменты, которые останутся в памяти. 🌹", reply_markup=kb)
