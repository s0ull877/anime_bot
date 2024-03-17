from aiogram.dispatcher.filters import BoundFilter
from aiogram.types.message import Message
import config

class IsReply(BoundFilter):
    key = "is_reply"

    def __init__(self, ans=True):
        self.ans = ans

    async def check(self, msg: Message) -> bool:
        return dict(msg).get('reply_to_message')