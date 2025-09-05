from aiogram import Router, F
from aiogram.types import CallbackQuery, Message, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter
from aiogram.enums.parse_mode import ParseMode

from sqlalchemy.ext.asyncio import AsyncSession

from src.bot.keyboard.common import start_keyboard, cancel_keyboard
from src.bot.keyboard.couple import leave_couple_keyboard, select_option_keyboard, next_question_keyboard, category_keyboard
import src.bot.storage.couple as database

from src.bot.state import NewCouple, Couple

from src.bot.message.common import start_message
from src.bot.message.couple import select_option_message, own_question_message, next_question_message, select_category_message

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

    try:
        couple, partner_telegram_id = await database.join_couple(
            session=session,
            telegram_id=message.from_user.id,
            token=token
        )

        await message.answer(
            f"🎉 Вы успешно присоединились к паре!\n\n"
            f"Теперь вы вместе. Приключение начинается! ✨",
            parse_mode=ParseMode.MARKDOWN,
        )

        await bot.send_message(
            chat_id=partner_telegram_id,
            text=f"🎉 Ваш партнёр присоединился!\n\nТеперь вы вместе. Приключение начинается! ✨",
            parse_mode=ParseMode.MARKDOWN,
        )
        
        kb = select_option_keyboard()
        await message.answer(text=select_option_message, reply_markup=kb)
        await bot.send_message(chat_id=partner_telegram_id, text=select_option_message, reply_markup=kb)

        await state.set_state(Couple.select_option)
        partner_state = FSMContext(storage=state.storage, key=("default", str(partner_telegram_id)))
        await partner_state.set_state(Couple.select_option)

    except ValueError as e:
        kb = cancel_keyboard()

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


@couple_router.callback_query(F.data == "own_question")
async def own_question(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Couple.own_question)
    kb = cancel_keyboard()
    await callback.message.edit_text(
        text=own_question_message,
        reply_markup=kb
    )


@couple_router.message(Couple.own_question)
async def process_own_question(message: Message, state: FSMContext, session: AsyncSession):
    user_question = message.text.strip()
    kb = next_question_keyboard()
    try:
        partner_telegram_id = await database.get_partner_telegram_id(
            session=session,
            telegram_id=message.from_user.id
        )

        await message.bot.send_message(
            chat_id=partner_telegram_id,
            text=f"❓ Ваш партнёр задал вам вопрос:\n\n{user_question}",
            reply_markup=kb
        )

        await message.answer(
            "✅ Ваш вопрос отправлен партнёру! Ожидайте его ответа ✨",
            reply_markup=kb
        )

        await state.set_state(Couple.answer)

        partner_state = FSMContext(storage=state.storage, key=("default", str(partner_telegram_id)))
        await partner_state.set_state(Couple.answer)


    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")

    except Exception as e:
        await message.answer(f"⚠️ Что-то пошло не так. Попробуйте ещё раз позже.")


@couple_router.message(Couple.answer)
async def process_answer(message: Message, state: FSMContext, session: AsyncSession):
    answer = message.text.strip()
    try:
        partner_telegram_id = await database.get_partner_telegram_id(
            session=session,
            telegram_id=message.from_user.id
        )

        await message.bot.send_message(
            chat_id=partner_telegram_id,
            text=answer,
        )
    except ValueError as e:
        await message.answer(f"❌ Ошибка: {e}")


@couple_router.callback_query(F.data == "next_question")
async def next_question(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    kb = select_option_keyboard()
    try:
        partner_telegram_id = await database.get_partner_telegram_id(
            session=session,
            telegram_id=callback.from_user.id
        )

        await callback.bot.send_message(
            chat_id=partner_telegram_id,
            text=next_question_message,
            reply_markup=kb
        )

        await callback.message.answer(
            text=next_question_message,
            reply_markup=kb
        )

        await state.set_state(Couple.select_option)

        partner_state = FSMContext(storage=state.storage, key=("default", str(partner_telegram_id)))
        await partner_state.set_state(Couple.select_option)

        await callback.answer()
    except ValueError as e:
        await callback.message.answer(f"❌ Ошибка: {e}")

    except Exception as e:
        await callback.message.answer(f"⚠️ Что-то пошло не так. Попробуйте ещё раз позже.")


@couple_router.callback_query(F.data == "select_category")
async def select_category(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Couple.select_category)

    kb = category_keyboard()
    await callback.message.edit_text(text=select_category_message, reply_markup=kb)


@couple_router.callback_query(
    F.data.in_(["category_talk", "category_fun", "category_relationship", "category_goals", "category_reflection", "category_adult"])
)
async def process_select_category(callback: CallbackQuery, state: FSMContext, session: AsyncSession):
    category = callback.data
    await callback.message.answer(text=f"Вы выбрали категорию: {category}")
