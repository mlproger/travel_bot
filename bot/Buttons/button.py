from aiogram.types import (
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    ReplyKeyboardRemove,
    KeyboardButton,
)
from aiogram.utils.keyboard import InlineKeyboardBuilder


class Button:



    main = InlineKeyboardBuilder(
        markup = [
            [
                InlineKeyboardButton(text="Мой профиль 👤", callback_data = "profile"),
                InlineKeyboardButton(text="В путешествие 🌍", callback_data = "trip")
            ]
        ]
    ).adjust(1).as_markup()

    async def trips():
        keyes = InlineKeyboardBuilder()
        texts = [
            "Запланировать путешествие 📊",
            "Просмотреть список путешевствий 📒",
            "⬅️ Назад",
        ]
        for i in range(len(texts)):
            keyes.add(InlineKeyboardButton(text=texts[i], callback_data=f"trip_{i}"))
        return keyes.adjust(1).as_markup()



    profile = InlineKeyboardMarkup(
    inline_keyboard = [
            [
                InlineKeyboardButton(text="Редактировать ✏️", callback_data = "edit"),
                InlineKeyboardButton(text="На главную", callback_data = "main_page"),
            ]
        ]
    )
    
    async def edit_prifile():
        keyes = InlineKeyboardBuilder()
        texts = [
            "🔞 Возраст",
            "🏙️ Город",
            "🌍 Страна",
            "❓ О себе",
            "❌ Отмена"
        ]
        for i in range(len(texts)):
            keyes.add(InlineKeyboardButton(text=texts[i], callback_data=f"edit_profile_{i}"))
        return keyes.adjust(2).as_markup()
    

    cancel_trip = ReplyKeyboardRemove(
    keyboard = [
            [
                KeyboardButton(text="❌ Отменить создание путешествия"),
            ]
        ],
        resize_keyboard=True
    )

    cancel_trip_location = ReplyKeyboardRemove(
    keyboard = [
            [
                KeyboardButton(text="❌ Отменить создание путешествия"),
                KeyboardButton(text="✅ Закончить добавление локаций"),
            ]
        ],
        resize_keyboard=True
    )

    async def get_list_trips_fail():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Запланировать путешествие 📊", callback_data="trip_0"))
        keyes.add(InlineKeyboardButton(text="На главную", callback_data="main_page"))

        return keyes.adjust(1).as_markup()
    
    async def count_trip():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="<<<", callback_data = "trip-"))
        keyes.add(InlineKeyboardButton(text=">>>", callback_data = "trip+"))
        keyes.add(InlineKeyboardButton(text="Подробнее по id", callback_data = "get_trip_by_id"))
        keyes.add(InlineKeyboardButton(text="⬅️ Назад", callback_data = "back_get_trips"))

        return keyes.adjust(2).as_markup()
    
    async def edit_trip():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Редактировать ✏️", callback_data = "edit_trip"))
        keyes.add(InlineKeyboardButton(text="Удалить ❌", callback_data = "delete_trip"))
        keyes.add(InlineKeyboardButton(text="Файлы/заметки 📂", callback_data="add_notes"))
        keyes.add(InlineKeyboardButton(text="Проложить маршрут 🗺️", callback_data="make_route"))
        keyes.add(InlineKeyboardButton(text="К списку путешествий", callback_data="trip_1"))

        return keyes.adjust(1).as_markup()
    
    async def choise_action_note():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Добавить", callback_data="choise_add")),
        keyes.add(InlineKeyboardButton(text="Посмотреть", callback_data="choise_get")),
        keyes.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_trip"))

        return keyes.adjust(2).as_markup()
 
    
    choise_note_format = InlineKeyboardMarkup(
        inline_keyboard = [
            [
                InlineKeyboardButton(text="Файлы 📂", callback_data="add_files"),
                InlineKeyboardButton(text="Текстовая замтека 📝", callback_data="add_text")
            ]
        ]
    )
    
    async def choise_note_format_get(): 
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Файлы 📂", callback_data="get_files"))
        keyes.add(InlineKeyboardButton(text="Текстовая замтека 📝", callback_data="get_text"))
        keyes.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_get_text"))

        return keyes.adjust(2).as_markup()
    

    async def choise_note_format_add1():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Создать текстовую замтеку 📝", callback_data="add_text"))
        keyes.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_get_text"))

        return keyes.adjust(1).as_markup()
    
    async def choise_note_format_add2():
        keyes = InlineKeyboardBuilder()
        keyes.add(InlineKeyboardButton(text="Добавить файлы 📂", callback_data="add_files"))
        keyes.add(InlineKeyboardButton(text="⬅️ Назад", callback_data="back_get_text"))

        return keyes.adjust(1).as_markup()

