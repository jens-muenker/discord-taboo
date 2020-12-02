from random import shuffle
from random import randrange
import asyncio
import copy

import frosch2010_Tabu_variables as fTV
import frosch2010_Console_Utils as fCU
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Class_Utils as fCLU
import frosch2010_Tabu_manage_timer as fMT

#-----------------------------------------------------

async def on_Start_Game(msg, tabuVars, tabuSettings, client):

    tabuVars.tabu_is_running = True


    fCU.log_In_Console("{} started game...".format(msg.author.name), "ON-START", "inf")
    await fDU.send_Message_To_Channel("{} has started the game...".format(msg.author.name), [msg.channel])


    #Check if Points-To-WIN should be changed
    args = msg.content.split(" ")

    if len(args) >= 3:

        try:

            tabuVars.tabu_points_to_win = int(args[2])

            fCU.log_In_Console("{} set points to win to: {}".format(msg.author.name, str(tabuVars.tabu_points_to_win)), "ON-START", "inf")

        except:
            
            fCU.log_In_Console("{} cant set points to win. Cant parse point-count from arguments.".format(msg.author.name), "ON-START", "err")


    #Delete messages in Team-Channels
    fCU.log_In_Console("Delete messages for team 1 and 2...", "ON-START", "inf")

    await fDU.delete_Messages_From_Channel([client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])


    #Delete messages in all private channels of players with the bot
    fCU.log_In_Console("Delete messages for all players...", "ON-START", "inf")

    channels = []

    for player in tabuVars.tabu_player_list_all:

        await player.create_dm()

        channels.append(client.get_channel(player.dm_channel.id))

    await fDU.delete_Messages_From_Channel(channels, 4)


    #Split player in teams
    fCU.log_In_Console("Shuffel playerlist and split them in teams...", "ON-START", "inf")

    shuffle(tabuVars.tabu_player_list_all)

    team_size = (len(tabuVars.tabu_player_list_all) / 2)

    tabuVars.tabu_player_list_team_1 = tabuVars.tabu_player_list_all[:int(team_size)]
    tabuVars.tabu_player_list_team_2 = tabuVars.tabu_player_list_all[int(team_size):]

    await fDU.send_Message_To_Channel(fTOF.str_Who_Which_Team(tabuVars), [msg.channel])


    #Define start team
    fCU.log_In_Console("Set start team...", "ON-START", "inf")

    tabuVars.tabu_guessing_team_num = randrange(0,1)


    #Set time per round + start timer
    fCU.log_In_Console("Starting timer...", "ON-START", "inf")

    tabuVars.tabu_current_time = copy.deepcopy(tabuSettings.tabu_round_lenght)
    fCLU.Timer(1, fMT.manage_timer, [tabuVars, tabuSettings, client])


    #Send timer messages to all
    fCU.log_In_Console("Sending countdown-messages...", "ON-START", "inf")

    await fTOF.send_Team_Countdowns(tabuVars, tabuSettings, client)
    await fTOF.send_Explainer_Countdown(tabuVars)


    fCU.log_In_Console("Started successfully...", "ON-START", "inf")

    await fTOF.send_New_Word_Card(tabuVars, tabuSettings, client)
