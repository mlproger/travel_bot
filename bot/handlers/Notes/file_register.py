import io
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
    FSInputFile,
    
)

class File(StatesGroup):
    file_id = State()
    file_name = State()

router = Router()

@router.callback_query(F.data == "add_files")
async def add_note(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text(
        f"Пришлите файл, который я запомню",
    )
    await state.set_state(File.file_id)

@router.message(File.file_id)
async def get_file(message: Message, state: FSMContext):
    data = await state.get_data()
    await state.set_state(File.file_name)
    if message.content_type == 'photo':
        file = io.BytesIO()
        paths = rf"Files/{message.photo[-1].file_id}"
        await message.bot.download(message.photo[-1].file_id, destination=f"Files/{message.photo[-1].file_id}.png")
        with open(f"Files/{message.photo[-1].file_id}_{message.photo[-1].file_id}", 'w') as f:
            pass
        await message.bot.download(message.photo[-1].file_id, destination=f"Files/{message.photo[-1].file_id}.png")
        f = f"INSERT INTO notes (id_trip, unique_id_trip, files) VALUES ({data['id']},{data['id']}, ARRAY['{message.photo[-1].file_id}']) ON CONFLICT(unique_id_trip) DO UPDATE SET files = array_append(notes.files, '{message.photo[-1].file_id}')"
        repo.add_by_msg(msg=f)
        await message.answer(text="Впишите название для фото")
    else:
        with open(f"Files/{message.document.file_id}_{message.document.file_name}", 'w') as f:
            pass
        await message.bot.download(message.document.file_id, destination=f"Files/{message.document.file_id}_{message.document.file_name}")
        f = f"INSERT INTO notes (id_trip, unique_id_trip, files) VALUES ({data['id']},{data['id']}, ARRAY['{message.document.file_id}']) ON CONFLICT(unique_id_trip) DO UPDATE SET files = array_append(notes.files, '{message.document.file_id}')"
        repo.add_by_msg(msg=f)
        await message.answer(text="Впишите название для документа")

@router.message(File.file_name)
async def set_file_name(message: Message, state: FSMContext):
    data = await state.get_data()
    name = message.text
    f = f"UPDATE notes SET files_names = array_append(files_names, '{name}') WHERE id_trip = {data['id']}"
    repo.add_by_msg(msg=f)
    trip = TR.get(id = int(data["id"]), offset= 5*1, id_trip=-1)[0]
    routes = trip["locations"]
    routes = routes.split(',')
    points = []
    for i in range(len(routes)):
        if i % 3 == 0:
            _point = routes[i].replace('"', '').replace("{", "").replace("(", "")
            points.append(_point)
    await message.answer("Файл успешно добавлен")
    msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {'->'.join(map(str,points))}"
    await message.answer(
            text=msg,
            reply_markup = await Button.edit_trip()
        )
