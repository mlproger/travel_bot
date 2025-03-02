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
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
    InlineKeyboardButton
)

router = Router()

class File(StatesGroup):
    i = State()


@router.callback_query(F.data == "get_files")
async def get_files(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    try:
        note = repo.get(id=callback.message.chat.id, id_trip=data["id"], flag=-3)[0]
        files = note["files"]
        names = note["files_names"]
        await state.set_state(File.i)
        msg = ""
        for i in range(len(names)):
            msg += f"{names[i]} | {i+1}\n"
        await callback.message.edit_text(
            text=msg
        )
        await callback.message.answer(
            "Напишите id файла, который вы хотите получить"
        )
    except TypeError:
        await callback.message.edit_text("Файлы еще не добавлены", reply_markup= await Button.choise_note_format_add2())

@router.message(File.i)
async def get_files_by_id(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        note = repo.get(id=message.from_user.id, id_trip=data["id"], flag=-3)[0]
        files = note["files"]
        names = note["files_names"]
        try:
            await message.answer_document(document=files[int(message.text) - 1])
        except:
            await message.answer_photo(photo=files[int(message.text) - 1])
        trip = TR.get(id = int(data["id"]), offset= 5*1, id_trip=-1)[0]
        routes = trip["locations"]
        routes = routes.split(',')
        points = []
        for i in range(len(routes)):
            if i % 3 == 0:
                _point = routes[i].replace('"', '').replace("{", "").replace("(", "").replace("\\","")
                points.append(_point)
        msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}: {'->'.join(map(str,points))}"
        await message.answer(
            text=msg,
            reply_markup = await Button.edit_trip()
        )
    except TypeError:
        await message.answer("Файлы еще не добавлены", reply_markup= await Button.choise_note_format_add2())
    except Exception as e:
        print(e)
        await message.answer("Введите числове значение из списка выше")

# @router.callback_query(F.data == "get_files")
# async def add_note(callback: CallbackQuery, state: FSMContext):
#     await callback.message.edit_text(
#         f"Что хотите посмотреть?",
#         reply_markup = await Button.choise_note_format_get()
#     )
