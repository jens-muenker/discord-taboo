import discord

import frosch2010_Console_Utils as fCU

async def on_ready(tabuSettings, client):

    if check_bot_permissions(tabuSettings, client):

        fCU.log_In_Console("Logged in as user {}".format(client.user.name), "ON-READY", "inf")

    else:

        fCU.log_In_Console("The bot does not have all necessary permissions!", "ON-READY", "err")
        fCU.log_In_Console("Shutdown bot...", "ON-READY", "inf")

        await client.logout()


def check_bot_permissions(tabuSettings, client):

    is_all_ready = True


    #Check Channel Join exists
    if discord.utils.get(client.get_guild(347451773289758730).text_channels, id=tabuSettings.tabu_channelID_join) is None:

        is_all_ready = False

        fCU.log_In_Console("'channelID_join' doesnt exist your server!", "CHECK-PERMISSIONS", "err")

    else:

        channel_join = client.get_channel(tabuSettings.tabu_channelID_join)


        #Check Permissions
        if not channel_join.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).view_channel:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read in the channel 'channelID_join'!", "CHECK-PERMISSIONS", "err")

        if not channel_join.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).send_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send messages in the channel 'channelID_join'!", "CHECK-PERMISSIONS", "err")



    #Check Channel Team-1 exists
    if discord.utils.get(client.get_guild(347451773289758730).text_channels, id=tabuSettings.tabu_channelID_team_1) is None:

        is_all_ready = False

        fCU.log_In_Console("'tabu_channelID_team_1' doesnt exist your server!", "CHECK-PERMISSIONS", "err")

    else:

        channel_team_1 = client.get_channel(tabuSettings.tabu_channelID_team_1)


        #Check Permissions
        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).view_channel:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).send_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send messages in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).manage_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to manage messages in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).read_message_history:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read old messages in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).add_reactions:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to add reactions in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_1.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).attach_files:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send files in the channel 'tabu_channelID_team_1'!", "CHECK-PERMISSIONS", "err")



    #Check Channel Team-2 exists
    if discord.utils.get(client.get_guild(347451773289758730).text_channels, id=tabuSettings.tabu_channelID_team_2) is None:

        is_all_ready = False

        fCU.log_In_Console("'tabu_channelID_team_2' doesnt exist your server!", "CHECK-PERMISSIONS", "err")

    else:

        channel_team_2 = client.get_channel(tabuSettings.tabu_channelID_team_2)


        #Check Permissions
        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).view_channel:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).send_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send messages in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).manage_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to manage messages in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).read_message_history:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read old messages in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).add_reactions:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to add reactions in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")

        if not channel_team_2.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).attach_files:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send files in the channel 'tabu_channelID_team_2'!", "CHECK-PERMISSIONS", "err")



    #Check Channel Add-Terms exists
    if discord.utils.get(client.get_guild(347451773289758730).text_channels, id=tabuSettings.tabu_channelID_add_terms) is None:

        is_all_ready = False

        fCU.log_In_Console("'tabu_channelID_add_terms' doesnt exist your server!", "CHECK-PERMISSIONS", "err")

    else:

        channel_add_terms = client.get_channel(tabuSettings.tabu_channelID_add_terms)

        #Check Permissions
        if not channel_add_terms.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).view_channel:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read in the channel 'tabu_channelID_add_terms'!", "CHECK-PERMISSIONS", "err")



    #Check Channel Bot-Admin exists
    if discord.utils.get(client.get_guild(347451773289758730).text_channels, id=tabuSettings.tabu_channelID_bot_admin) is None:

        is_all_ready = False

        fCU.log_In_Console("'tabu_channelID_bot_admin' doesnt exist your server!", "CHECK-PERMISSIONS", "err")

    else:

        channel_bot_admin = client.get_channel(tabuSettings.tabu_channelID_bot_admin)


        #Check Permissions
        if not channel_bot_admin.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).view_channel:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to read in the channel 'tabu_channelID_bot_admin'!", "CHECK-PERMISSIONS", "err")

        if not channel_bot_admin.permissions_for(client.get_guild(347451773289758730).get_member(client.user.id)).send_messages:

            is_all_ready = False
            fCU.log_In_Console("Bot has not permssions to send messages in the channel 'tabu_channelID_bot_admin'!", "CHECK-PERMISSIONS", "err")


    return is_all_ready
    