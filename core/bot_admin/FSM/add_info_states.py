from aiogram.dispatcher.filters.state import State, StatesGroup

class Form(StatesGroup):
    releas = State()
    studio = State()
    genres = State()
    photo = State()
