from aiogram.fsm.state import StatesGroup, State


class NewCouple(StatesGroup):
    waiting = State()
    joining = State()


class Couple(StatesGroup):
    select_category = State()
