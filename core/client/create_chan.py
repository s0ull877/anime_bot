from telethon.tl.functions import channels


async def create_channel_private(channelName: str,channelDesc: str,desiredPublicUsername: str):
    # channelName = 'Test_photo'
    # channelDesc = 'dskhajdhasj'
    # desiredPublicUsername = "skajsdksaja" #юзенейм канала 
    

    createdPrivateChannel = await client(channels.CreateChannelRequest(channelName,channelDesc,megagroup=False)) #сначала создание приватного канала для функции ниже

    newChannelID = createdPrivateChannel.__dict__["chats"][0].__dict__["id"]
    newChannelAccessHash = createdPrivateChannel.__dict__["chats"][0].__dict__["access_hash"]

    checkUsernameResult = await client(channels.CheckUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))

    if(checkUsernameResult==True):
        publicChannel = await client(channels.UpdateUsernameRequest(InputPeerChannel(channel_id=newChannelID, access_hash=newChannelAccessHash), desiredPublicUsername))    
        channelPhoto = await client(channels.EditPhotoRequest(channelName,photo=await client.upload_file(r'core/client/temp/image.jpg')))