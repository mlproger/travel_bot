from typing import Any, Dict
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.types import FSInputFile
from aiogram.types.callback_query import CallbackQuery
from bot.Buttons.button import Button
from bot.handlers.Users.Repo import repo as UR
from map.map import get_point_from_api, set_route
from .Repo import repo
from aiogram.fsm.state import State, StatesGroup
from bot.handlers.Trips.Repo import repo as TR

from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)


router = Router()
class Note(StatesGroup):
    text_note = State()



@router.callback_query(F.data == "add_notes")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Что хотите сделать?",
        reply_markup = await Button.choise_action_note()
    )

@router.callback_query(F.data == "back_to_trip")
async def add_note(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    trip = TR.get(id = callback.message.chat.id, id_trip=int(data["id"]))[0]
    routes = trip["locations"]
    routes = routes.split(',')
    points = []
    for i in range(len(routes)):
        if i % 3 == 0:
            _point = routes[i].replace('"', '').replace("{", "").replace("(", "")
            points.append(_point)

    msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {'->'.join(map(str,points))}"
    await callback.message.edit_text(
        text=msg,
        reply_markup = await Button.edit_trip()
    )


@router.callback_query(F.data == "choise_add")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Note.text_note)
    await callback.message.edit_text(
        f"Что хотите создать",
        reply_markup =  Button.choise_note_format
    )

@router.callback_query(F.data == "add_text")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Note.text_note)
    await callback.message.edit_text(
        f"Введите текст заметки, а ее запишу)",
    )

@router.message(Note.text_note)
async def add_text_note(message: Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    f = f"INSERT INTO notes (note_text, id_trip, unique_id_trip) VALUES ('{message.text}', {data['id']}, {data['id']}) ON CONFLICT (unique_id_trip) DO UPDATE SET note_text = '{message.text}'"
    repo.add_by_msg(msg=f)
    trip = TR.get(id = int(data["id"]), offset= 5*1, id_trip=-1)[0]
    routes = trip["locations"]
    routes = routes.split(',')
    points = []
    for i in range(len(routes)):
        if i % 3 == 0:
            _point = routes[i].replace('"', '').replace("{", "").replace("(", "")
            points.append(_point)
    await message.answer("Замтека успешно добавлена")
    msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {'->'.join(map(str,points))}"
    await message.answer(
            text=msg,
            reply_markup = await Button.edit_trip()
        )