import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils import exceptions

import config
from database import database

bot = config.bot


async def allert_cmd(msg:Message):
    users_id = database.get_users('user_id')
    forward_message_id = msg.reply_to_message.message_id
    chat_id = msg.reply_to_message.chat.id

    for user_id in users_id:
        
        try:
        
            await bot.copy_message(chat_id=user_id[0], from_chat_id=chat_id, message_id=forward_message_id)
        
        except exceptions.BotBlocked:
            pass
    

