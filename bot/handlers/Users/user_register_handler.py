from typing import Any, Dict
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import Router, types, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.handlers.callback_query import CallbackQuery
from bot.Buttons.button import Button
from .Repo import repo
from .Repo.user_repo import UserRepository
from .user_state import User
from aiogram.types import (
    KeyboardButton,
    InlineKeyboardButton,
    Message,
    ReplyKeyboardMarkup,
    InlineKeyboardMarkup,
    ReplyKeyboardRemove,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder



router = Router()



@router.message(CommandStart())
@router.message(Command("main"))
async def greeting(message: types.Message) -> None:
    print(message.from_user.username)
    _check = repo.get(message.from_user.id)
    if _check == 0:
        print(message.from_user.full_name)
        await message.answer(
            f"Привет, {hbold(message.from_user.full_name)}!\nДобро пожаловать в Travel Bot\nДля начала нам нужно познакомиться, расскажи о себе)",
            reply_markup = ReplyKeyboardRemove(
                keyboard=[
                    [
                        KeyboardButton(text="Зарегистрироваться"),
                        KeyboardButton(text="Не хочу регистрироваться...")
                    ]
                ],
                resize_keyboard = True
            ),
        )
    else:
        print(message.from_user.full_name)
        print(message.from_user.username)
        await message.answer(
            "С возвращением👋",
            reply_markup = Button.main
            # reply_markup = ff()
        )


@router.callback_query(F.data == "profile")
@router.message(Command("me"))
async def get_me(callback: CallbackQuery):
    me = repo.get(callback.message.chat.id)[0]
    if me != 0:
        await callback.message.edit_text(
            f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
            reply_markup = Button.profile
        )
    else: 
        await callback.message.edit_text(
            f"Привет, {hbold(callback.message.from_user.full_name)}!\nДобро пожаловать в Travel Bot\nДля начала нам нужно познакомиться, расскажи о себе)",
            reply_markup = ReplyKeyboardRemove(
                keyboard=[
                    [
                        KeyboardButton(text="Зарегистрироваться"),
                        KeyboardButton(text="Не хочу регистрироваться...")
                    ]
                ],
                resize_keyboard = True
            ),
        )



@router.message(F.text.casefold() == "зарегистрироваться")
async def register_user(message: types.Message, state: FSMContext) -> None:
    await state.set_state(User.age)
    await message.answer("Для начала введи свой возраст", reply_markup=ReplyKeyboardRemove(),)

@router.message(User.age)
async def set_user_age(message: types.Message, state: FSMContext) -> None:
    age = message.text
    if age.isdigit():
        await state.update_data(age=message.text)
        await state.set_state(User.city)
        await message.answer("Запомнил, теперь введи свой город 🏙️")
    else:
        await message.answer("Неее, так не пойдет. Возраст состоит только из цифр. Давай еще раз, введи свой возраст")



@router.message(User.city)
async def set_user_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(city=message.text)
    await state.set_state(User.country)
    await message.answer("Теперь введи страну проживания 🌍")


@router.message(User.country)
async def set_user_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(country=message.text)
    await state.set_state(User.bio)
    await message.answer("Кратко расскажи о себе")


@router.message(User.bio)
async def set_user_age(message: types.Message, state: FSMContext) -> None:
    await state.update_data(bio=message.text)
    data = await state.get_data()
    await finish_registration(message=message, data=data)
    await state.clear()

    

async def finish_registration(message: Message, data: Dict[str, Any]):
    print(data)
    print(message.from_user.id)
    data["name"] = message.from_user.full_name
    data["tg_id"] = str(message.from_user.id)
    repo.add(data)
    await message.answer(
        text=f"Регистрация заверешена, приятно познакомиться 🙂",
        reply_markup = Button.main
    )



@router.message(F.text.casefold() == "не хочу регистрироваться...")
async def register_user(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer("Приходите, когда созреете для путушествий)", reply_markup=ReplyKeyboardRemove(),)


