import os
import asyncio
import discord

import frosch2010_Console_Utils as fCU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Discord_Utils as fDU

async def on_Reaction_Add(reaction, user, tabuVars, tabuSettings, client):

    #Pause-Reaction
    if tabuVars.tabu_is_switching:

        if reaction.emoji == "⏸":

            if reaction.message.channel.id == tabuSettings.tabu_channelID_team_1 or reaction.message.channel.id == tabuSettings.tabu_channelID_team_2 or tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id == user.id or tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id == user.id:

                tabuVars.tabu_is_pause = True


                #Change reaction from pause to play
                for countdown in tabuVars.tabu_time_messages:

                    for r in countdown.reactions:
                        await countdown.clear_reaction(r)

                    await countdown.add_reaction("▶️")


                tabuVars.tabu_is_raeacting = False
                return

        
        elif reaction.emoji == "▶️":

            if reaction.message.channel.id == tabuSettings.tabu_channelID_team_1 or reaction.message.channel.id == tabuSettings.tabu_channelID_team_2 or tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id == user.id or tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id == user.id:

                tabuVars.tabu_is_pause = False


                #Change reaction from pause to play
                for countdown in tabuVars.tabu_time_messages:

                    for r in countdown.reactions:
                        await countdown.clear_reaction(r)

                    await countdown.add_reaction("⏸")


                tabuVars.tabu_is_raeacting = False
                return


    #Private chat
    elif reaction.message.channel.type == discord.channel.ChannelType.private:

        #Which team?
        if tabuVars.tabu_guessing_team_num == 0:

            #Player is still Explainer?
            if tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id != user.id:
                tabuVars.tabu_is_raeacting = False
                return

        else:

            #Player is still Explainer?
            if tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id != user.id:
                tabuVars.tabu_is_raeacting = False
                return


    #From team 1-channel
    elif reaction.message.channel.id == tabuSettings.tabu_channelID_team_1:
        if tabuVars.tabu_guessing_team_num == 0:
            tabuVars.tabu_is_raeacting = False
            return

    #From team 2-channel
    elif reaction.message.channel.id == tabuSettings.tabu_channelID_team_2:
        if tabuVars.tabu_guessing_team_num == 1:
            tabuVars.tabu_is_raeacting = False
            return


    #Skipped
    if reaction.emoji == "⏩":

        fCU.log_In_Console("Team skipped a card.", "REACTION-ADD", "inf")

        if tabuVars.tabu_current_time <= 1:
            tabuVars.tabu_is_raeacting = False
            return


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, client)

        tabuVars.tabu_is_raeacting = False

        if tabuVars.tabu_guessing_team_num == 0:

            fCU.log_In_Console("Team 1 get -3 points.", "REACTION-ADD", "inf")

            tabuVars.tabu_points_team_1 -= 3
            tabuVars.tabu_points_this_round -= 3

        else:

            fCU.log_In_Console("Team 2 get -3 points.", "REACTION-ADD", "inf")

            tabuVars.tabu_points_team_2 -= 3
            tabuVars.tabu_points_this_round -= 3


        fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")
        return
    
    #Correct
    elif reaction.emoji == "✅":

        if tabuVars.tabu_guessing_team_num == 0:

            fCU.log_In_Console("Team 1 get 10 points.", "REACTION-ADD", "inf")


            #Add points
            tabuVars.tabu_points_team_1 += 10
            tabuVars.tabu_points_this_round += 10


            #Did team win?
            if tabuVars.tabu_points_team_1 >= tabuVars.tabu_points_to_win:

                tabuVars.tabu_is_running = False

                fCU.log_In_Console("Team 1 won the game.", "REACTION-ADD", "inf")


                tabuVars.tabu_points_history_team_1.append(tabuVars.tabu_points_this_round)


                #Get current Explainer channel
                if tabuVars.tabu_guessing_team_num == 0:

                    explainer_channel = tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1]

                else:

                    explainer_channel = tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2]

                
                #Send win to all
                await fDU.send_Message_To_Channel("**Team 1 won!**", [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2), explainer_channel])
                #await fDU.send_Message_To_Channel("Punkte-Team 1: {}\nPunkte-Team 2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2), explainer_channel])


                await fTOF.create_and_send_win_graph(tabuVars, tabuSettings, client)


                await fTOF.delete_all_term_and_countdown_messages(tabuVars)


                #reset vars
                fTOF.reset_all_vars(tabuVars)

                return


            fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")

        else:

            fCU.log_In_Console("Team 2 get 10 points.", "REACTION-ADD", "inf")


            #Add points
            tabuVars.tabu_points_team_2 += 10
            tabuVars.tabu_points_this_round += 10


            #Did team win?
            if tabuVars.tabu_points_team_2 >= tabuVars.tabu_points_to_win:

                tabuVars.tabu_is_running = False


                fCU.log_In_Console("Team 2 won the game.", "REACTION-ADD", "inf")


                tabuVars.tabu_points_history_team_2.append(tabuVars.tabu_points_this_round)


                #Get current Explainer channel
                if tabuVars.tabu_guessing_team_num == 0:

                    explainer_channel = tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1]

                else:

                    explainer_channel = tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2]


                #Send win to all
                await fDU.send_Message_To_Channel("**Team 2 won!**", [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2), explainer_channel])
                #await fDU.send_Message_To_Channel("Punkte-Team 1: {}\nPunkte-Team 2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), [client.get_channel(723621829310152786), client.get_channel(723621890039611422), explainer_channel])


                await fTOF.create_and_send_win_graph(tabuVars, tabuSettings, client)


                await fTOF.delete_all_term_and_countdown_messages(tabuVars)


                #reset vars
                fTOF.reset_all_vars(tabuVars)

                return


            fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")


        for old_card in tabuVars.tabu_guessing_card_messages:
            try:
                await old_card.delete()
            except:
                pass


        tabuVars.tabu_guessing_card_messages.clear()


        if tabuVars.tabu_current_time <= 1:
            return


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, client)

    
    #False
    elif reaction.emoji == "❌":

        if tabuVars.tabu_guessing_team_num == 0:

            fCU.log_In_Console("Team 1 get -5 points.", "REACTION-ADD", "inf")

            tabuVars.tabu_points_team_1 -= 5
            tabuVars.tabu_points_this_round -= 5

        else:

            fCU.log_In_Console("Team 2 get -5 points.", "REACTION-ADD", "inf")

            tabuVars.tabu_points_team_2 -= 5
            tabuVars.tabu_points_this_round -= 5


        fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")


        for old_card in tabuVars.tabu_guessing_card_messages:
            try:
                await old_card.delete()
            except:
                pass

        tabuVars.tabu_guessing_card_messages.clear()

        if tabuVars.tabu_current_time <= 1:

            return

        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, client)