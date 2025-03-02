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

@router.callback_query(F.data == "choise_get")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Что хотите посмотреть?",
        reply_markup = await Button.choise_note_format_get()
    )


@router.callback_query(F.data == "get_text")
async def add_note(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    trip = TR.get(id = int(data["id"]), offset= 5*1, id_trip=-1)[0]
    routes = trip["locations"]
    routes = routes.split(',')
    points = []
    for i in range(len(routes)):
        if i % 3 == 0:
            _point = routes[i].replace('"', '').replace("{", "").replace("(", "").replace("\\","")
            points.append(_point)
    try:
        note = repo.get(id=callback.message.chat.id, id_trip=data["id"], flag=-3)[0]
        await callback.message.answer(
            text = note["note_text"],
        )
        msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {'->'.join(map(str,points))}"
        await callback.message.edit_text(
            text=msg,
            reply_markup = await Button.edit_trip()
        )

    except:
        await callback.message.edit_text(
            text = "Заметок еще нет",
            reply_markup= await Button.choise_note_format_add1()
        )



@router.callback_query(F.data == "back_get_text")
async def back_text_get(callback: CallbackQuery, state: FSMContext):
    # data = await state.get_data()
    # trip = TR.get(id = int(data["id"]), offset= 5*1, id_trip=-1)[0]
    # msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {trip['locations']}"
    await callback.message.edit_text(
        text="Что хотите сделать",
        reply_markup = await Button.choise_action_note()
    )


