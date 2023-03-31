from aiogram.fsm.state import StatesGroup, State


class MainState(StatesGroup):
    start = State()
    valid_email = State()
