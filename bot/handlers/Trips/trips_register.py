from typing import Any, Dict
from aiogram import Router, types, F
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types.callback_query import CallbackQuery
from bot.Buttons.button import Button
from bot.handlers.Users.Repo import repo as UR
from map.map import get_point_from_api, set_route
from .Repo import repo
import logging
from aiogram.types import WebAppInfo
from .trips_state import Trip
from aiogram.types import (
    Message,
    ReplyKeyboardRemove,
)



router = Router()
locations = []



@router.message(F.text.casefold() == "❌ отменить создание путешествия")
async def cancel_add_trip(message: Message, state: FSMContext):
    await message.answer(
        "Отменил",
        reply_markup = ReplyKeyboardRemove()
    )
    await state.clear()
    await message.answer(
        text="Что интересует?",
        reply_markup = await Button.trips()
    )


@router.callback_query(F.data == "trip")
async def register_trip1(callback: CallbackQuery):
    await callback.message.edit_text(
        f"Что интерисует?",
        reply_markup = await Button.trips()
    )



@router.callback_query(F.data == "trip_0")
async def register_trip(callback: CallbackQuery, state: FSMContext):
    await state.set_state(Trip.name)
    await callback.message.edit_text("Настраиваем путешествие....")
    await callback.message.answer("Приступим! Впишите название для вашего путешествия. Как начсчет 'крестовый поход'?", reply_markup = Button.cancel_trip)



@router.message(Trip.name)
async def set_trip_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(Trip.description)
    data = await state.get_data()
    await message.answer(f"Для чего нам {data['name']}? Предлагаю добавить описание")

@router.message(Trip.description)
async def set_trip_description(message: types.Message, state: FSMContext):
    await state.update_data(description=message.text)
    await state.set_state(Trip.locations)
    await message.answer(f"Давай чуть подробнее распланируем путешествие. Куда и когда пойдем?\nДля этого впиши сюда локации в следущем формате:\nнаселенный пункт;дата прибытия;дата отбытия\nПо завершении добавления локаций нажми кнопку\nДату необходимо указать в формате дд.мм.гггг", reply_markup = Button.cancel_trip_location)



@router.message(F.text.casefold() == "✅ закончить добавление локаций")
async def stop(message: types.Message, state: FSMContext):
    global locations
    data = await state.get_data()
    print(data, "DATA")
    await state.set_state(Trip.id)
    await message.answer(
        text="Путешествие успешго добавлено!",
        reply_markup=ReplyKeyboardRemove()
    )
    await finish_add_trip(message=message, data=data, points=locations,state=state)

    locations = []


@router.message(Trip.locations)
async def set_trip_location(message: types.Message, state: FSMContext):
    point = message.text.replace(";", ",")
    if len(point.split(',')) != 3:
        await message.answer(
            text = "Введи данные в следущем формате 'населенный пункт;дата прибытия;дата отбытия'"
        )
    else:
        # check = await get_point_from_api(point.split(',')[0])
        # logging.info(check)
        # locations.append(point) 
        try:
            check = await get_point_from_api(point.split(',')[0])
            # logging.info(check)
            locations.append(point) 
        except Exception as e:
            logging.error(e)
            await message.answer(
                text = "Хммм, я не могу найти такого места, попробуй еще раз"
            )



async def finish_add_trip(message: Message, data: Dict[str, Any], points, state: FSMContext):
    arr = []
    names = []
    for i in points:
        arr.append(f"{*i.split(','),}")
        names.append(i.split(',')[0])
    s = ""
    for i in range(len(arr)):
        if i != len(arr)-1:
            s += arr[i] + "::location" + ","
        else:
            s += arr[i] + "::location"
    f = f"""
        INSERT INTO trips (Name, description, locations, entity_id) VALUES (
        '{data["name"]}',
        '{data["description"]}',
        ARRAY[
            {s}
        ],
        '{message.from_user.id}'
        )
        """
    print(f)
    _a = repo.add_by_msg(msg=f)
    if _a == "Error":
        await message.answer("Имя для путешествия должно быть уникальным, пересоздайте", reply_markup = await Button.trips())
    else:
        print(data["name"])
        trip = repo.get(id=message.from_user.id, id_trip=-2, name= data["name"])[0]
        await state.update_data(id = trip["id"])
        routes = trip["locations"]
        routes = routes.split(',')
        locations = []
        for i in range(len(routes)):
            if i % 3 == 0:
                _point = routes[i].replace('"', '').replace("{", "").replace("(", "").replace("\\", "")
                locations.append(_point)
        msg = f"{hbold('Название')}: {trip['name']}\n{hbold('Описание')}: {trip['description']}\n{hbold('Маршрут')}:{'->'.join(map(str,locations))}"
        await message.answer(
            text = msg,
            reply_markup = await Button.edit_trip()
        )

        # city = UR.get(message.from_user.id)[0]['city']
        # point_dict = {}
        # point_dict[city] = [await get_point_from_api(city)]
        # for name in names:
        #     point_dict[name] = [await get_point_from_api(name)]
        # print(point_dict)
        # path = await set_route(point_dict)
        # photo = FSInputFile(path)
        # await message.answer_photo(photo, caption=f"Полный маршрут {data['name']}. Для более подробного ознакомления парейдите к простомтору списка ваших путешествий", reply_markup=ReplyKeyboardRemove())  
        # await state.clear()


@router.callback_query(F.data == "trip_2")
async def back_trip(callback: CallbackQuery):
    await callback.message.edit_text(
        "С возвращением👋",
        reply_markup = Button.main
    )


