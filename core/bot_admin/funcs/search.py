from aiogram.types import Message
from keyboard.anime_found_inkb import anime_found
from database import database

async def search_anime(msg: Message):
    req = len(msg.text)

    if req < 3:
        await msg.reply('Слишком короткий запрос!')
        return 
    response = database.search_anime_request(msg.text)
    l = len(response)
    if not l:
        await msg.answer(f'По запросу "<b>{msg.text}</b>" ничего не найдено.', parse_mode='HTML')
        return

    await msg.answer(f'<b>{l}</b> найдено по запросу "<b>{msg.text}</b>"', reply_markup=anime_found(response),parse_mode='HTML')