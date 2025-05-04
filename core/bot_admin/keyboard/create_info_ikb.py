from aiogram.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup


def start_create_ikb(text: str,data:str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=text,callback_data=f'{data}')]
    ])
    return ikb


def end_create_ikb(data:str) -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='Все верно',callback_data=f'send_{data}')],
        [InlineKeyboardButton(text='❌',callback_data=f'{data}')]
    ])
    return ikb


temp_ikb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='✅',callback_data=f'temp')]
    ])