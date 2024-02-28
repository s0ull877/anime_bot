from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message
import config

class IsClient(BoundFilter):
    key = "is_client"

    def __init__(self, client):
        self.admin = client

    async def check(self, msg: Message):
        return msg.chat.id == config.CLIENT_ID