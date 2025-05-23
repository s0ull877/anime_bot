import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

from aiogram import Bot
from aiogram.types import Message
from aiogram.utils import exceptions

import config
from database import database

from core.bot_admin.keyboard.allert_ikb import allert_ikb

bot = config.bot


async def allert_cmd(msg:Message):
    args = msg.text.split(' ')
    print(args)
        
    users_id = database.get_users('user_id')
    forward_message_id = msg.reply_to_message.message_id
    chat_id = msg.reply_to_message.chat.id
    
    if len(args) == 1:

        for user_id in users_id:
            
            try:
            
                await bot.copy_message(chat_id=user_id[0], from_chat_id=chat_id, message_id=forward_message_id)
            
            except exceptions.BotBlocked:
                pass
    else:

        for user_id in users_id:
            
            try:
            
                await bot.copy_message(chat_id=user_id[0], from_chat_id=chat_id, message_id=forward_message_id, \
                    reply_markup=allert_ikb(*args[1:]))
            
            except exceptions.BotBlocked:
                pass
        

async def help_cmd(message: Message):
    await message.answer("""
`/allert button_link button_text` \- команда отправляет рассылку ботом всем пользователям,
доп\. параметры\: 
button\_link \- добавляет кнопку с написаной ссылкой под отправленный пост
button\_text \- текст на кнопке, по умолчанию *Переходи по ссылке*\.
данная команда работает только на reply сообщения, выделенное сообщение отправится в рассылку
""", parse_mode='MarkdownV2')

