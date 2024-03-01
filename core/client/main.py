import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import config
from telethon import TelegramClient
from telethon.sync import events
from telethon.tl.functions.channels import InviteToChannelRequest,EditAdminRequest
from telethon.tl.types import PeerUser, PeerChat, PeerChannel,ChatAdminRights

from core.client.functions.parser import parse_params,valid_url_for_chan
from core.client.commands.create_chan import create_channel_public
from database import database
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient('anon', config.api_id, config.api_hash, system_version="Aspire 5750G-2454G50Mnkk")

with client:

    @client.on(events.NewMessage(chats=config.ADMIN_ID,pattern=r"/create_chan"))
    async def cmd_create_chan(msg):

        resp = valid_url_for_chan(msg.text)

        if resp not in msg.text:
            _ = await msg.reply(resp)
        else:

            name, tg_me = parse_params(resp)
            answer = database.get_answer(tg_me)
            if answer:
                await msg.reply('Такой канал уже создан')
            else:
                suc_chan = await create_channel_public(name,config.desc_channel,tg_me,client,resp)
                _ = await msg.reply(suc_chan)
            


    client.run_until_disconnected()