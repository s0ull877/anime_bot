import sys
import os
sys.path.insert(0,os.path.join(os.getcwd()))

import config
from telethon import TelegramClient

from core.client.create_chan import create_channel_private
from core.client.parser import parse_params


client = TelegramClient('anon', config.api_id, config.api_hash, system_version="Aspire 5750G-2454G50Mnkk")

# with client:
#     client.loop.run_until_complete(create_channel_private())