from aiogram import Router
from aiogram import Router, types, F

from bot.Buttons.button import Button
from .Repo import repo
from .user_state import User
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from aiogram.types import (
    KeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
)

router = Router()
btn = [ KeyboardButton(text="🔞 Возраст"),KeyboardButton(text="🏙️ Город"),KeyboardButton(text="🌍 Страна"),KeyboardButton(text="❓ О себе"),KeyboardButton(text="⬅️ Назад")]

@router.callback_query(F.data == "edit")
async def patch_me(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        "Выбери поле, которое хочешь отредактировать",
        reply_markup = await Button.edit_prifile()
    )


@router.callback_query(F.data == "edit_profile_0")
async def update_age(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User.update_age)
    await callback.message.edit_text("Ну-ка, сколько там тебе стукнуло?)")
    
    

@router.message(User.update_age)
async def update_name(message: types.Message, state: FSMContext):
    await state.clear()
    repo.update(field="age", value = message.text, id=message.from_user.id)
    me = repo.get(message.from_user.id)[0]
    await message.answer(
        f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
            reply_markup = await Button.edit_prifile()
        )


@router.callback_query(F.data == "edit_profile_1")
async def update_city(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User.update_city)
    await callback.message.edit_text("Ого, кто-то переезжает))) Куда ставить метку?")
    
    
@router.message(User.update_city)
async def set_city(message: types.Message, state: FSMContext):
    await state.update_data(city = message.text)
    await state.clear()
    repo.update(field="city", value = message.text, id=message.from_user.id)
    me = repo.get(message.from_user.id)[0]
    await message.answer(
        f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
            reply_markup = await Button.edit_prifile()
        )


@router.callback_query(F.data == "edit_profile_2")
async def update_county(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User.update_country)
    await callback.message.edit_text("Заграницу??? А куда дислоцируемся?")
    
    
@router.message(User.update_country)
async def set_county(message: types.Message, state: FSMContext):
    await state.update_data(country = message.text)
    await state.clear()
    repo.update(field="country", value = message.text, id=message.from_user.id)
    me = repo.get(message.from_user.id)[0]
    await message.answer(
        f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
            reply_markup = await Button.edit_prifile()
        )


@router.callback_query(F.data == "edit_profile_3")
async def update_bio(callback: CallbackQuery, state: FSMContext):
    await state.set_state(User.update_bio)
    await callback.message.edit_text("Новая страница в жизни? Ну рассказывай, я слушаю")
    
    
@router.message(User.update_bio)
async def sit_bio(message: types.Message, state: FSMContext):
    await state.update_data(bio = message.text)
    await state.clear()
    repo.update(field="bio", value = message.text, id=message.from_user.id)
    me = repo.get(message.from_user.id)[0]
    await message.answer(
        f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
            reply_markup = await Button.edit_prifile()
        )

@router.callback_query(F.data == "edit_profile_4")
async def cancel(callback: CallbackQuery):
    me = repo.get(callback.message.chat.id)[0]
    await callback.message.edit_text(
        f"✅ Имя: {me['name']}\n🔞 Возраст: {me['age']}\n🏙️ Город: {me['city']}\n🌍 Страна: {me['country']}\n❓ О себе: {me['bio']}",
        reply_markup= Button.profile)

# @router.message(F.text.casefold() == "⬅️ назад")
# async def patch_me(message: types.Message):
#     await message.answer(
#         "...",
#         reply_markup = ReplyKeyboardRemove(
#             keyboard=[
#                 [
#                     KeyboardButton(text="Мой профиль 👤"),
#                     KeyboardButton(text="В путешествие 🌍")
#                 ]
#             ],
#             resize_keyboard = True
#         ),
#     )