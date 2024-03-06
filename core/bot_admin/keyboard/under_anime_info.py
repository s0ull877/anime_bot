from aiogram.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup



def under_anime_info(data: str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()

    ikb.add(InlineKeyboardButton(text='🎬Начать просмотр', callback_data=f'watch_{data}'))
    ikb.add(InlineKeyboardButton(text='📃Обзор', callback_data=f'desc_{data}'))
    ikb.add(InlineKeyboardButton(text='❌', callback_data=f'delete'))


    return ikb


def under_anime_desc(data:str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()

    ikb.add(InlineKeyboardButton(text='🎬Начать просмотр', callback_data=f'watch_{data}'))
    ikb.add(InlineKeyboardButton(text='🌅Постер', callback_data=f'poster_{data}'))
    ikb.add(InlineKeyboardButton(text='❌', callback_data=f'delete'))


    return ikb


