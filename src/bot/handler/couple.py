from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboard.common import start_keyboard, cancel_keyboard
from src.bot.keyboard.couple import leave_couple_keyboard
import src.bot.storage.couple as database

from src.bot.state import NewCouple, Couple
from src.bot.handler.common import start_message

from src.bot.config import bot

couple_router = Router()


@couple_router.callback_query(F.data == "create_couple")
async def create_couple(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    token = await database.user_in_couple(session, callback.from_user.id)

    if not token:
        await state.set_state(NewCouple.waiting)
        couple = await database.create_couple(
            session=session,
            telegram_id=callback.from_user.id
        )

        kb = cancel_keyboard()
        await callback.message.edit_text(
            f"✨ Ваша пара успешно создана!\n\n"
            f"Ваш секретный код для входа в команду:\n"
            f"`{couple.token}`\n\n"
            f"Передайте его партнёру и начните приключение вместе!",
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN,
        )
    else:
        kb = leave_couple_keyboard()
        await callback.message.edit_text(
            f"⚠️ У вас уже есть пара.\n\n"
            f"Ваш токен:\n"
            f"`{token}`\n\n"
            f"Чтобы создать новую, сначала выйдите из текущей.",
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN,
        )
    await callback.answer()

@couple_router.callback_query(F.data == "join_couple")
async def join_couple(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    token = await database.user_in_couple(session, callback.from_user.id)
    
    if token:
        kb = leave_couple_keyboard()
        await callback.message.edit_text(
            f"⚠️ У вас уже есть пара.\n\n"
            f"Ваш токен:\n"
            f"`{token}`\n",
        reply_markup=kb,
        parse_mode=ParseMode.MARKDOWN)
    else:
        kb = cancel_keyboard()
        await state.set_state(NewCouple.joining)
        await callback.message.edit_text(
            "Введите код, который сообщил вам партнёр",
            reply_markup=kb,
        )
    await callback.answer()


@couple_router.message(NewCouple.joining)
async def process_join_token(message: Message, state: FSMContext, session: AsyncSession):
    token = message.text.strip()
    kb = cancel_keyboard()

    try:
        couple, partner_telegram_id = await database.join_couple(
            session=session,
            telegram_id=message.from_user.id,
            token=token
        )

        await message.answer(
            f"🎉 Вы успешно присоединились к паре!\n\n"
            f"Ваш партнёр теперь с вами. Приключение начинается! ✨",
            reply_markup=kb,
            parse_mode=ParseMode.MARKDOWN,
        )

        await bot.send_message(
            chat_id=partner_telegram_id,
            text=f"🎉 Ваш партнёр присоединился!\n\nТеперь вы вместе. Приключение начинается! ✨",
            parse_mode=ParseMode.MARKDOWN,
        )

        await state.set_state(Couple.select_category)
        partner_state = FSMContext(storage=state.storage, key=("default", str(partner_telegram_id)))
        await partner_state.set_state(Couple.select_category)

    except ValueError as e:
        await message.answer(
            f"❌ Ошибка: {e}.\n\nПопробуйте ввести код снова или отмените действие.",
            reply_markup=kb,
        )


@couple_router.callback_query(F.data == "leave_couple")
async def leave_couple(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    await state.clear()
    try:
        await database.leave_couple(session, callback.from_user.id)
        await callback.message.answer("✅ Вы вышли из пары.")
    except ValueError:
        await callback.message.answer("❌ Вы не состоите в паре.")
    finally:
        kb = start_keyboard()
        await callback.message.answer(
            text=start_message,
            reply_markup=kb,
        )
        await callback.message.delete()
    await callback.answer()


@couple_router.callback_query(F.data == "back_to_start")
async def back_to_start(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    kb = start_keyboard()
    await callback.message.edit_text(
        text=start_message,
        reply_markup=kb,
    )

