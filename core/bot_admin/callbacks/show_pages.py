from aiogram.types import CallbackQuery

from database import database

from core.bot_admin.keyboard.anime_found_inkb import anime_found


async def show_next_page(callback: CallbackQuery):

    pattern = callback.message.text.split('"')[1]

    response = database.search_anime_request(pattern)

    page = int(callback.data.split('/')[-1])

    await callback.message.edit_reply_markup(anime_found(data=response, page=page))


async def show_previous_page(callback: CallbackQuery):

    pattern = callback.message.text.split('"')[1]
    response = database.search_anime_request(pattern)

    page = int(callback.data.split('/')[-1])

    await callback.message.edit_reply_markup(anime_found(data=response, page=page))


async def temp_handler(callback:CallbackQuery):
    pass