from aiogram import Bot
from aiogram.types import CallbackQuery

from core.bot_admin.keyboard.under_anime_info import under_anime_info,under_anime_desc

from database import database
import config

bot = config.bot


async def on_anime_button_callback(callback: CallbackQuery) -> None:
    await callback.answer('')
    chan_link = database.get_link(callback.data)
    chan_link, msg_id, desc = database.get_infodata(chan_link)
    await bot.copy_message(chat_id=callback.message.chat.id, from_chat_id=config.tech_group_id, \
        message_id=msg_id, reply_markup=under_anime_info(chan_link))


async def on_desc_anime_callback(callback:CallbackQuery) -> None:
    chan_link = callback.data.replace('desc_','') 
    chan_link, msg_id, desc = database.get_infodata(chan_link)
    await callback.message.delete()
    await callback.message.answer(text=desc,reply_markup=under_anime_desc(chan_link))

async def on_poster_anime_callback(callback: CallbackQuery) -> None:
    chan_link = callback.data.replace('poster_','') 
    chan_link, msg_id, desc = database.get_infodata(chan_link)
    await callback.message.delete()
    await bot.copy_message(chat_id=callback.message.chat.id, from_chat_id=config.tech_group_id, \
        message_id=msg_id, reply_markup=under_anime_info(chan_link))


async def delete_callback(callback:CallbackQuery) -> None:
    await callback.message.delete()