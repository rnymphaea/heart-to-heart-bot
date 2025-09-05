from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

def leave_couple_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🚪 Покинуть пару", callback_data="leave_couple")],
        [InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_start")]
    ])
    return keyboard


def select_option_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📂 Категории", callback_data="select_category")],
        [InlineKeyboardButton(text="🎲 Случайный вопрос", callback_data="random_question")],
        [InlineKeyboardButton(text="✍️ Задать свой вопрос", callback_data="own_question")]
    ])
    return keyboard


def next_question_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="➡️ Следующий вопрос", callback_data="next_question")]
    ])
    return keyboard


def category_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💡 Разговорные", callback_data="category_talk"),
            InlineKeyboardButton(text="😂 Весёлые", callback_data="category_fun"),
        ],
        [
            InlineKeyboardButton(text="❤️ Отношения", callback_data="category_relationship"),
            InlineKeyboardButton(text="🎯 Цели", callback_data="category_goals"),
        ],
        [
            InlineKeyboardButton(text="💭 Размышления", callback_data="category_reflection"),
            InlineKeyboardButton(text="🔞 18+", callback_data="category_adult"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_menu")
        ]
    ])
    return keyboard
