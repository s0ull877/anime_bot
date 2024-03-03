from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Update
from config import client_bot_id
from database import database


class BotJoinMiddleware(BaseMiddleware):

    async def on_process_update(self, update: Update, data: dict):
        try:
            if update.my_chat_member.new_chat_member.user.id == client_bot_id and update.my_chat_member.new_chat_member.status == 'administrator':
                chan_id = update.my_chat_member.chat.id
                chan_name = update.my_chat_member.chat.title.replace(' все серии', '')
                chan_link = update.my_chat_member.chat.username
                database.insert_chan_info(chan_id,chan_name,chan_link)

            return            
        except Exception:
            pass