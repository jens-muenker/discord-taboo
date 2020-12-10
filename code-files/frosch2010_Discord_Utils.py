import discord

async def send_Message_To_Channel(msg, channels, delete_after_time=None):

    for channel in channels:

        await channel.send(msg, delete_after= delete_after_time) if delete_after_time else await channel.send(msg)

async def get_Messages_From_Channel(channel, limit=None):

    return await channel.history(limit=None).flatten()

async def delete_Messages_From_Channel(channels, delete_limit=None):

    for channel in channels:

        messages = await channel.history(limit=delete_limit).flatten()

        for msg in messages:

            try:
                await msg.delete()
            except:
                pass