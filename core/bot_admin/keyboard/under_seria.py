from aiogram.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup

import database
import config

def under_seria_ikb(anime: str, rowid: int) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()
    if rowid == 1:
        ikb.add(InlineKeyboardButton(text='⏭Вперед', callback_data=f'{anime}/{rowid+1}'))
        return ikb

    ikb.add(InlineKeyboardButton(text='Назад⏮', callback_data=f'{anime}/{rowid-1}'),
            InlineKeyboardButton(text='⏭Вперед', callback_data=f'{anime}/{rowid+1}'))
    
    return ikb