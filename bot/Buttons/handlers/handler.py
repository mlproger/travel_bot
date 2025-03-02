from aiogram.types.callback_query import CallbackQuery
from aiogram import Router, F
from ..button import Button
router = Router()


@router.callback_query(F.data == "main_page")
async def cancel(callback: CallbackQuery):
    await callback.message.edit_text(
        f"С чего начнем?",
        reply_markup= Button.main)