from aiogram.types import CallbackQuery

import config
from core.bot_admin.keyboard.under_seria import under_seria_ikb
from database import database

bot = config.bot

async def on_watch_anime_callback(callback: CallbackQuery) -> None:
    channel_link = callback.data.replace('watch_','')

    chan_id = database.get_chan_id(channel_link=channel_link)
    msg_id, _, _ = database.get_seria_data(table_name=channel_link, seria_num=1)

    if msg_id:

        await bot.copy_message(chat_id=callback.message.chat.id, from_chat_id=chan_id, \
            message_id=msg_id, reply_markup=under_seria_ikb(anime=channel_link,rowid=1))
        await callback.answer('🍿Приятного просмотра🍿')
        return

    await callback.answer('На данный момент это последняя серия')


async def new_seria_callback(callback:CallbackQuery) -> None:
    data_list = callback.data.split('/')
    channel_link = data_list[0]
    seria_num = int(data_list[1])

    chan_id = database.get_chan_id(channel_link=channel_link)
    msg_id, _, _ = database.get_seria_data(table_name=channel_link, seria_num=seria_num)
    

    if msg_id:

        await callback.message.delete()
        await bot.copy_message(chat_id=callback.message.chat.id, from_chat_id=chan_id, \
            message_id=msg_id, reply_markup=under_seria_ikb(anime=channel_link,rowid=seria_num))
        return

    await callback.answer('На данный момент это последняя серия')
    