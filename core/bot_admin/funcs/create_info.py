from aiogram import Bot
from aiogram.types import Message

from core.bot_admin.keyboard.create_info_ikb import start_create_ikb
from database import database
import config

bot = config.bot

async def start_create_info(text: str,channel_link:str):
    
    if text != "Successfull fill channel!":
        await bot.send_message(chat_id=config.tech_group_id,text=text)
        return

    anime = database.get_anime_name(channel_link=channel_link)

    await bot.send_message(chat_id=config.tech_group_id,text=f"Заполните информацию для аниме '{anime}'", reply_markup=start_create_ikb('Начать', f'info_{channel_link}'))

    

    

