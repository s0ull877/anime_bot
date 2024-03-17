from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message
import config

class IsAdmin(BoundFilter):
    key = "is_admin"

    def __init__(self, admin=None):
        self.admin = admin

    async def check(self, msg: Message) -> bool:
        return msg.from_user.id in config.ADMIN_ID