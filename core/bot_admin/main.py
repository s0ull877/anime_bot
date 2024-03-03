import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import logging
from aiogram import Bot,Dispatcher,executor,types

import config

from core.bot_admin.filters.is_client import IsClient

from core.bot_admin.commands.client_command import fill_channel_cmd
from core.bot_admin.commands.user_commands import start_cmd

from core.bot_admin.middleware.channel_join import BotJoinMiddleware

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = Bot(config.client_bot_token)
dp = Dispatcher(bot)


dp.register_message_handler(start_cmd, commands=['start', 'help'])
dp.register_message_handler(fill_channel_cmd, IsClient(True), commands=['fill'])



if __name__ == '__main__':
    dp.middleware.setup(BotJoinMiddleware())
    executor.start_polling(dp, skip_updates=True)