from telethon import TelegramClient
from telethon.tl.functions import channels
from telethon.tl.functions.channels import CreateChannelRequest, CheckUsernameRequest, UpdateUsernameRequest, EditAdminRequest
from telethon.tl.types import InputChannel, InputPeerChannel, ChatAdminRights
import pprint

import config


async def invite_client_bot(channel_id: int, client: TelegramClient) -> None:
        channel = await client.get_entity(channel_id)
        bot = await client.get_entity(config.client_bot_id)

        result = await client(EditAdminRequest(
            channel=channel,
            user_id=bot,
            admin_rights=ChatAdminRights(
                change_info=True,
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=True,
                anonymous=True,
                manage_call=True,
                other=True,
                manage_topics=True
            ),
            rank="Poster"
        ))


async def create_channel_public(channelName: str,channelDesc: str,desiredPublicUsername: str, client: TelegramClient,url: str) -> str:
    
    NewChannelName = channelName + ' все серии'
    
    createdPrivateChannel = await client(channels.CreateChannelRequest(NewChannelName,channelDesc,megagroup=False)) #сначала создание приватного канала для функции ниже

    newChannelID = createdPrivateChannel.__dict__["chats"][0].__dict__["id"]
    newChannelAccessHash = createdPrivateChannel.__dict__["chats"][0].__dict__["access_hash"]

    checkUsernameResult = await client(channels.CheckUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))

    if(checkUsernameResult==True):
        publicChannel = await client(channels.UpdateUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))
        channelPhoto = await client(channels.EditPhotoRequest(NewChannelName,photo=await client.upload_file(r'core/client/temp/image.jpg')))
        
        await invite_client_bot(newChannelID,client)
        await client.send_message(config.client_bot_id, message=f'/fill {desiredPublicUsername} {url}')
        
        return f'Канал создан - https://t.me/{desiredPublicUsername}\nНачинаю заполнение...'




