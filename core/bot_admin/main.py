import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import logging
from aiogram import Bot,Dispatcher,executor,types
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import config

from core.bot_admin.filters.is_client import IsClient
from core.bot_admin.filters.is_private_chat import IsPrivate
from core.bot_admin.filters.anime_in_db import InDB



from core.bot_admin.commands.client_command import fill_channel_cmd
from core.bot_admin.commands.user_commands import start_cmd

from core.bot_admin.middleware.channel_join import BotJoinMiddleware

from core.bot_admin.funcs.search import search_anime
from core.bot_admin.funcs.create_info import start_create_info

from core.bot_admin.callbacks.show_pages import show_next_page,show_previous_page,temp_handler
from core.bot_admin.callbacks.create_info_callbacks import on_anime_callback,on_releas_callback,on_studio_callback,on_genres_callback,on_photo_callback
from core.bot_admin.callbacks.create_info_callbacks import on_releas_message,on_studio_message,on_genres_message,on_photo_message,on_send_data_callback
from core.bot_admin.callbacks.show_anime import on_anime_button_callback,on_desc_anime_callback,on_poster_anime_callback,delete_callback
from core.bot_admin.callbacks.anime_player import on_watch_anime_callback, new_seria_callback

from core.bot_admin.FSM.add_info_states import Form



logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

bot = config.bot
dp = Dispatcher(bot,storage=MemoryStorage())


dp.register_message_handler(start_cmd, IsPrivate(True), commands=['start', 'help'])
dp.register_message_handler(fill_channel_cmd, IsClient(True), commands=['fill'])
dp.register_message_handler(on_releas_message,state=Form.releas)
dp.register_message_handler(on_studio_message,state=Form.studio)
dp.register_message_handler(on_genres_message,state=Form.genres)
dp.register_message_handler(on_photo_message,state=Form.photo,content_types=types.ContentType.PHOTO)
dp.register_message_handler(start_create_info,IsClient(True))
dp.register_message_handler(search_anime,IsPrivate(True))


dp.register_callback_query_handler(show_next_page,lambda callback: callback.data.startswith('page_next'))
dp.register_callback_query_handler(show_previous_page,lambda callback: callback.data.startswith('page_previous'))
dp.register_callback_query_handler(temp_handler,lambda callback: callback.data.startswith('temp'))
dp.register_callback_query_handler(on_send_data_callback,lambda callback: callback.data.startswith('send_info'))

dp.register_callback_query_handler(on_releas_callback,lambda callback: callback.data.startswith('info'),state=Form.releas)
dp.register_callback_query_handler(on_studio_callback,lambda callback: callback.data.startswith('info'),state=Form.studio)
dp.register_callback_query_handler(on_genres_callback,lambda callback: callback.data.startswith('info'),state=Form.genres)
dp.register_callback_query_handler(on_photo_callback,lambda callback: callback.data.startswith('info'),state=Form.photo)
dp.register_callback_query_handler(on_anime_callback,lambda callback: callback.data.startswith('info'))

dp.register_callback_query_handler(delete_callback,lambda callback: callback.data.startswith('delete'))
dp.register_callback_query_handler(on_anime_button_callback,InDB(True))
dp.register_callback_query_handler(on_desc_anime_callback,lambda callback: callback.data.startswith('desc'))
dp.register_callback_query_handler(on_poster_anime_callback,lambda callback: callback.data.startswith('poster'))

dp.register_callback_query_handler(on_watch_anime_callback,lambda callback: callback.data.startswith('watch'))
dp.register_callback_query_handler(new_seria_callback,lambda callback: callback.data.startswith('s0_anime'))





@dp.callback_query_handler()
async def test(callback: types.CallbackQuery):
    print(callback)

if __name__ == '__main__':
    dp.middleware.setup(BotJoinMiddleware())


    executor.start_polling(dp, skip_updates=True)