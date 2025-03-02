from aiogram.fsm.state import State, StatesGroup


class Trip(StatesGroup):
    name = State()
    description = State()
    locations = State()
    id = State()
