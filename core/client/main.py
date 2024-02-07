import os
import sys
sys.path.insert(0,os.path.join(os.getcwd()))

import config
from telethon import TelegramClient
from telethon.sync import events

from core.client.parser import parse_params,valid_url_for_chan
from core.client.create_chan import create_channel_private
import logging

logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s',
                    level=logging.WARNING)

client = TelegramClient('anon', config.api_id, config.api_hash, system_version="Aspire 5750G-2454G50Mnkk")

with client:
    temp_dict = {}

    @client.on(events.NewMessage(chats=config.ADMIN_ID,pattern=r"/create_chan"))
    async def cmd_create_chan(msg):

        resp = valid_url_for_chan(msg.text)

        if resp not in msg.text:
            _ = await msg.reply(resp)
        else:

            name, tg_me = parse_params(resp)
            suc_chan = await create_channel_private(name,config.desc_channel,tg_me,client)
            _ = await msg.reply(suc_chan)


    client.run_until_disconnected()