from aiogram import Bot
from aiogram.types import Message

import config
from database import database

bot = Bot(config.client_bot_token)

async def fill_channel(message: Message):
    id_is = message.text.split(' ')[1]
    url = message.text.split(' ')[-1]
    database.create_tables(id_is)

