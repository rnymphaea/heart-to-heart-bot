from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def leave_couple_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Покинуть пару", callback_data="leave_couple")],
        [InlineKeyboardButton(text="Назад", callback_data="back_to_start")]
    ])
    return keyboard
