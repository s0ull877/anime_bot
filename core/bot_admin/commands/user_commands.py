from aiogram.types import Message

from database import database


async def start_cmd(message:Message):
    text = """Привет, я бот для просмотра аниме!
Ты можешь просто написать название аниме и начать просмотр.)
Используй команду /random, если не знаешь что посмотреть"""
    msg = await message.answer(text=text)
    database.add_or_update_user(message.chat.id,message.from_user.username, message.from_user.first_name)