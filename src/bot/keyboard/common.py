from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def start_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Создать пару", callback_data="create_couple")],
        [InlineKeyboardButton(text="Присоединиться", callback_data="join_couple")],
    ])
    return keyboard

def cancel_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Отмена", callback_data="cancel")]
    ])
    return keyboard
