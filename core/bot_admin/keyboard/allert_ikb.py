from aiogram.types import CallbackQuery,InlineKeyboardButton,InlineKeyboardMarkup

def allert_ikb(link:str, text='Переходи по ссылке') -> InlineKeyboardMarkup:
    ikb = InlineKeyboardMarkup()

    ikb.add(InlineKeyboardButton(text=text, url=link))

    return ikb