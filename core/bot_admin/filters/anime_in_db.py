from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.callback_query import CallbackQuery
import config
from database import database

class InDB(BoundFilter):
    key = "in_db"

    def __init__(self, in_db):
        self.in_db = in_db

    async def check(self, callback: CallbackQuery) -> bool:
        answer = database.get_link(callback.data)
        return answer