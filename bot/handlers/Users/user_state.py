from aiogram.fsm.state import State, StatesGroup


class User(StatesGroup):
    age = State()
    city = State()
    country = State()
    bio = State()

    update_age = State()
    update_city = State()
    update_country = State()
    update_bio = State()
