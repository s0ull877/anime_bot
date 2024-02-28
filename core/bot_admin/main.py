import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import logging
from aiogram import Bot,Dispatcher,executor,types

import config

from core.bot_admin.filters.is_client import IsClient

from core.bot_admin.commands.client_command import fill_channel

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = Bot(config.client_bot_token)
dp = Dispatcher(bot)




@dp.message_handler(IsClient(True) , commands=['start', 'help'])
async def send_welcome(message: types.Message):

    await message.reply("Hi!\nI'm s0 Bot!\nPowered by aiogram.")




dp.register_message_handler(fill_channel, IsClient(True), commands=['fill'])

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)