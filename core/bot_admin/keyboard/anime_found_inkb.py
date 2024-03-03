from aiogram.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup
from math import ceil
#response = [(channel_mame1,),(channel_mame2,),(channel_mame3,)]
def anime_found(data: list,page=0) -> InlineKeyboardMarkup:
    pages = ceil(len(data)/5)
    ikb = InlineKeyboardMarkup()
    try:
        for i in range(page*5,page*5+5):

            ikb.add(InlineKeyboardButton(text=data[i][0],callback_data=data[i][0]))
    
    except IndexError:
        if page != 0:
            ikb.add(InlineKeyboardButton(text='◀️',callback_data=f'page_previous/{page-1}'),
            InlineKeyboardButton(text=f'{page+1}/{pages}',callback_data=f'temp'),
            InlineKeyboardButton(text='❌',callback_data=f'temp'))
        return ikb
    
    if page == 0:
        ikb.add(InlineKeyboardButton(text='❌',callback_data=f'temp'),
        InlineKeyboardButton(text=f'{page+1}/{pages}',callback_data=f'temp'),
        InlineKeyboardButton(text='▶️',callback_data=f'page_next/{page+1}'))
        return ikb

    ikb.add(InlineKeyboardButton(text='◀️',callback_data=f'page_previous/{page-1}'),
    InlineKeyboardButton(text=f'{page+1}/{pages}',callback_data=f'temp'), 
    InlineKeyboardButton(text='▶️',callback_data=f'page_next/{page+1}'))

    return ikb



