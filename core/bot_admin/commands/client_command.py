import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

from aiogram import Bot
from aiogram.types import Message

import config
from database import database
from core.bot_admin.funcs.fill_channel import fill_channel

bot = Bot(config.client_bot_token)

async def fill_channel_cmd(message: Message):
    channel_link = message.text.split(' ')[1]
    chan_id = database.get_chan_id(channel_link)
    url = message.text.split(' ')[-1]
    database.create_tables(channel_link)

    text = await fill_channel(url=url,chan_id=chan_id, chan_name=channel_link, bot=bot)
    await message.reply(text=text)

