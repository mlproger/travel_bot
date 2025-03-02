import os
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import CommandStart
from aiogram.enums import ParseMode
import logging
import sys
import asyncio
from dotenv import load_dotenv
import requests
from bot.handlers.Users.user_register_handler import router as user_registration_hendler
from bot.handlers.Users.user_update import router as user_update_hendler
from bot.handlers.Trips.trips_register import router as trip_registration_hendler
from bot.Buttons.handlers.handler import router as other_router
from bot.handlers.Trips.trips_get import router as trips_get_router
from bot.handlers.Notes.note_register import router as notes_add_router
from bot.handlers.Notes.note_get import router as notes_get_router
from bot.handlers.Notes.file_register import router as file_register
from bot.handlers.Notes.file_get import router as file_get
from selenium import webdriver



TOKEN = 'token'



dp = Dispatcher()



async def main() -> None:
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    dp.include_routers(user_update_hendler, user_registration_hendler, trip_registration_hendler, other_router, trips_get_router, notes_add_router,notes_get_router,file_register, file_get)
    await dp.start_polling(bot)



if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
    

    



