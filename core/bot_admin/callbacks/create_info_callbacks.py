import os

from aiogram import Bot
from aiogram.types import CallbackQuery, Message, InputFile
from aiogram.dispatcher import FSMContext

import config
from core.bot_admin.FSM.add_info_states import Form
from core.bot_admin.funcs.parser import get_desc
from core.bot_admin.keyboard.create_info_ikb import start_create_ikb,end_create_ikb,temp_ikb
from database import database

bot = Bot(config.client_bot_token)


async def on_s0_anime_callback(callback: CallbackQuery):
    await callback.message.delete()

    await callback.message.answer('Напиши год выпуска данного аниме и нажми на кнопку.',reply_markup=start_create_ikb('Готово',callback.data))
    
    await Form.releas.set()

# state = releas
async def on_releas_message(message: Message, state:FSMContext):
    async with state.proxy() as data:
        data['releas'] = message.text  
    

# state = releas
async def on_releas_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            temp = data['releas']  

        await callback.message.delete()

        await callback.message.answer('Теперь напиши от какой студии данное аниме.',reply_markup=start_create_ikb('Готово',callback.data))
        
        await Form.next()
    except KeyError:
        await callback.answer('Сначала отправьте год выпуска.')

# state = studio
async def on_studio_message(message: Message, state:FSMContext):
    async with state.proxy() as data:
        data['studio'] = message.text  
    

# state = studio
async def on_studio_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            temp = data['studio']  


        await callback.message.delete()
        
        await callback.message.answer('Теперь напиши жанры данного аниме, по 1 в каждом сообщении',reply_markup=start_create_ikb('Готово',callback.data))
        
        async with state.proxy() as data:
            data['genres'] = [] 

        await Form.next()
    except KeyError:
        await callback.answer('Сначала отправьте от какой студии данное аниме.')


# state = genres
async def on_genres_message(message: Message, state:FSMContext):
    async with state.proxy() as data:
        data['genres'].append(message.text)
    

# state = genres
async def on_genres_callback(callback: CallbackQuery, state: FSMContext):
    try:
        async with state.proxy() as data:
            temp = data['genres'][0]

        await callback.message.delete()

        await callback.message.answer('Теперь отправь фото-постер к этому аниме',reply_markup=start_create_ikb('Готово',callback.data))

        await Form.next()
    except IndexError:
        await callback.answer('Сначала отправьте жанр аниме.')



# state = photo
async def on_photo_message(message: Message, state:FSMContext):
    await message.answer("Подождите пару секунд и нажмите 'Готово'")
    photo_id = message.photo[-1].file_id

    f_info = await bot.get_file(photo_id)
    f = await bot.download_file(file_path=f_info.file_path)

    with open(r'core\bot_admin\temp\info.jpg', 'wb') as ph:
        ph.write(f.getvalue())

        
    
# state = photo
async def on_photo_callback(callback: CallbackQuery, state: FSMContext):

    genres = ''
    async with state.proxy() as data:
        releas = data['releas']
        studio = data['studio']
        genres_list = data['genres']
    await state.finish()

    for genre in genres_list:
        genres += f'#{genre} '
    
    chan_link = callback.data.replace('info_','')
    anime = database.get_anime_name(chan_link)
    data = database.get_counts(table_name=chan_link)
    series_count = data[0]
    season_count = data[-1]

    await callback.message.delete()
    await callback.message.answer(f"Вот так выглядит постер к аниме '{anime}'")

    text=f"""<b>{anime}</b>\n
<b>Год выпуска:</b> <i>{releas}</i>\n
<b>От студии: {studio}</b>\n
<b>Серий: {series_count}</b>\n
<b>Сезонов: {season_count}</b>\n
<b>{genres}</b>\n
💬Удобный просмотр в @s0_client_adminBot
"""

    photo = InputFile('core/bot_admin/temp/info.jpg')
    
    poster_msg = await bot.send_photo(chat_id=config.tech_group_id, photo=photo, caption=text, parse_mode='HTML', reply_markup=end_create_ikb(callback.data))


async def on_send_data_callback(callback: CallbackQuery):
    await callback.message.edit_reply_markup(temp_ikb)
    msg_id = callback.message.message_id
    
    message = await bot.copy_message(chat_id=config.s0_anime_info,from_chat_id=config.tech_group_id,message_id=msg_id)

    channel_link = callback.data.replace('send_info_','')
    url = database.get_url(channel_link=channel_link)
    desc = get_desc(url=url)
    
    database.insert_data_info(channel_link=channel_link,msg_id=msg_id,description=desc)
