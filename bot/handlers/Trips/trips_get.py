from aiogram import Router, F
from aiogram.utils.markdown import hbold
from aiogram.fsm.context import FSMContext
from aiogram.types.callback_query import CallbackQuery
from bot.Buttons.button import Button
from map.map import get_point_from_api, set_route
from .Repo import repo
from aiogram.fsm.state import State, StatesGroup
from aiogram.utils.markdown import hbold
from bot.handlers.Users.Repo import repo as UR
from aiogram.types import FSInputFile
from aiogram.types import (
    Message,
)

router = Router()

off = 0


def format_message(data):
    message = f"{hbold(str('НАЗВАНИЕ | ID'))}"
    message += "\n"
    for row in data:
        message += "๏" + " | ".join(row) + "\n"  # каждый элемент новой строки
    return message

@router.callback_query(F.data == "trip_1")
async def get_trips(callback: CallbackQuery, state: FSMContext):
    trips = repo.get(callback.message.chat.id, offset=0)
    if trips == 0:
        await callback.message.answer(
            text = "У вас нет ни запланнированых, ни совместных с друзьями путешествий(")
        await callback.message.answer(
            f"Что интерисует?",
            reply_markup = await Button.get_list_trips_fail()
        )
    else:
        routes = []
        for i in trips:
            routes.append([i["name"], str(i["id"])])
        msg = format_message(routes)
        await callback.message.edit_text(
            text=msg,
            reply_markup = await Button.count_trip()
        )

@router.callback_query(F.data == "trip+")
async def trip_next(callback: CallbackQuery, state: FSMContext):
    global off
    off += 1
    trips = repo.get(callback.message.chat.id, offset= 5*off)
    if trips == 0:
        off -= 1
        return
    routes = []
    for i in trips:
        routes.append([i["name"], str(i["id"])])
    msg = format_message(routes)
    await callback.message.edit_text(
        text=msg,
        reply_markup = await Button.count_trip()
    )

@router.callback_query(F.data == "trip-")
async def trip_prev(callback: CallbackQuery, state: FSMContext):
    global off
    off -= 1
    if off < 0: off = 0
    trips = repo.get(callback.message.chat.id, offset= 5*off)
    routes = []
    print(trips)
    for i in trips:
        routes.append([i["name"], str(i["id"])])
    msg = format_message(routes)
    await callback.message.edit_text(
        text=msg,
        reply_markup = await Button.count_trip()
    )


@router.callback_query(F.data == "back_get_trips")
async def back_trip(callback: CallbackQuery):
    await callback.message.edit_text(
        "С возвращением👋",
        reply_markup = await Button.trips()
    )

class ID(StatesGroup):
    id = State()

@router.callback_query(F.data == "get_trip_by_id")
async def get_trips(callback: CallbackQuery, state: FSMContext):
    await state.set_state(ID.id)
    await callback.message.answer(
        "Напишите id путешествия, по которму вы хотите получить больше информации"
    )



@router.message(ID.id)
async def get_trip_by_id(message: Message, state: FSMContext):
    await state.update_data(id = message.text)
    data = await state.get_data()
    print(data)
    try:
        trip = repo.get(id = message.from_user.id, offset= 5*off, id_trip=int(data["id"]))[0]
        print(trip, "1")
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
        # await state.clear()
    except TypeError as e:
        print(e)
        await message.answer(
            text="Маршрута с таким id не найдено",
        )
        trips = repo.get(message.from_user.id, offset= 5*off)
        routes = []
        print(trips)
        for i in trips:
            routes.append([i["name"], str(i["id"])])
        msg = format_message(routes)
        await state.clear()
        await message.answer(
            text=msg,
            reply_markup = await Button.count_trip()
        )
        
    

@router.callback_query(F.data == "delete_trip")
async def back_trip(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    _a = repo.delete(msg = f"DELETE FROM trips WHERE id = {data['id']}")
    trips = repo.get(id = callback.message.chat.id, offset= 5*off, id_trip=0)
    print(trips)
    routes = []
    print(trips)
    try:
        for i in trips:
            routes.append([i["name"], str(i["id"])])
        msg = format_message(routes)
        await callback.message.edit_text(
            text=msg,
            reply_markup = await Button.count_trip()
        )
    except:
        await callback.message.answer(
            text = "У вас нет ни запланнированых, ни совместных с друзьями путешествий(")
        await callback.message.answer(
            f"Что интерисует?",
            reply_markup = await Button.get_list_trips_fail()
        )



@router.callback_query(F.data == "make_route")
async def back_trip(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    print(data)
    await callback.message.edit_text(
        text="Прокладываем маршрут..."
    )
    trip = repo.get(id = callback.message.from_user.id, offset= 5*off, id_trip=int(data["id"]))[0]
    routes = trip["locations"]
    routes = routes.split(',')
    points = []
    for i in range(len(routes)):
        if i % 3 == 0:
            _point = routes[i].replace('"', '').replace("{", "").replace("(", "")
            points.append(_point)

    city = UR.get(callback.message.chat.id)[0]['city']
    point_dict = {}
    point_dict[city] = [await get_point_from_api(city)]
    for name in points:
        point_dict[name] = [await get_point_from_api(name)]
    print(point_dict)
    path = await set_route(point_dict)
    photo = FSInputFile(path)
    await callback.message.answer_photo(photo)
    await callback.message.answer(text=f"Полный маршрут {trip['name']}.", reply_markup= await Button.edit_trip())
    # await callback.message.edit_media(photo)