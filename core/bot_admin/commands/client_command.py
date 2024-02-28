from aiogram import Bot
from aiogram.types import Message

import config

bot = Bot(config.client_bot_token)

async def fill_channel(message: Message):
    id_is = message.text.split(' ')[-1]
    await message.reply(id_is)