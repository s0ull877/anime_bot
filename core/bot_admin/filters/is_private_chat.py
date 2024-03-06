from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message


class IsPrivate(BoundFilter):
    key = "is_private"

    def __init__(self, answer):
        self.answer = answer

    async def check(self, msg: Message) -> bool:
        return msg.chat.type == "private" and self.answer