from aiogram.types import Message

from core.bot_admin.keyboard.under_anime_info import under_anime_info,under_anime_desc

from database import database
import config


bot = config.bot


async def start_cmd(message:Message):
    text = """Привет, я бот для просмотра аниме!
Ты можешь просто написать название аниме и начать просмотр.)
Используй команду /random, если не знаешь что посмотреть"""
    msg = await message.answer(text=text)
    database.add_or_update_user(message.chat.id,message.from_user.username, message.from_user.first_name)


async def random_cmd(message: Message) -> None:
    chan_link = database.get_random_link()
    chan_link, msg_id, desc = database.get_infodata(chan_link)
    await message.delete()
    await bot.copy_message(chat_id=message.chat.id, from_chat_id=config.tech_group_id, \
        message_id=msg_id, reply_markup=under_anime_info(chan_link))