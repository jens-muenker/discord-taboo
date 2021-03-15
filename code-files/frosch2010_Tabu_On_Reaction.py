import os
import asyncio
import discord

import frosch2010_Console_Utils as fCU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_manage_terms as fTMT
import frosch2010_Tabu_edit_system_functions as fTESF
import frosch2010_Tabu_On_Start_Game as fTOSG
import frosch2010_Tabu_win_manager as fTWM

async def on_Reaction_Add(reaction, user, tabuVars, tabuSettings, tabuLanguage, client):

    #Edit Reaction?
    if reaction.message.channel.id == tabuSettings.tabu_channelID_add_terms:
        users = await reaction.users().flatten()

        for user in users:
            if user.id in tabuVars.tabu_edit_messages_list:
            
                #------------------------------------------------------------------------------
                #Card-Delete-Message reaction
                if user.id in tabuVars.tabu_edit_delete_card_list:
                    if tabuVars.tabu_edit_delete_card_list[user.id].id == reaction.message.id:

                        #--------------------------
                        #Delete term
                        if reaction.emoji == "✅":

                            term = str(tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", ""))
                            index = tabuVars.lst_Terms_already_loaded.index(term)


                            #Delete term from all lists
                            del tabuVars.lst_Terms_already_loaded[index]

                            if tabuVars.tabu_card_list[index] in tabuVars.tabu_card_pool:
                                tabuVars.tabu_card_pool.remove(tabuVars.tabu_card_list[index])

                            del tabuVars.tabu_card_list[index]


                            #-------------------------------------------------------
                            #Delete all edit-messages

                            del tabuVars.tabu_edit_term_list[tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", "")]

                            await fTESF.delete_edit_msgs(reaction.message, tabuVars.tabu_edit_messages_list[user.id][0])


                            del tabuVars.tabu_edit_messages_list[user.id]
                            del tabuVars.tabu_edit_delete_card_list[user.id]

                            fTMT.save_terms(tabuVars)

                            fCU.log_In_Console("{} deleted the term {}.".format(str(user.name), str(term)), "REACT-EDIT-DEL-Y", "inf")

                            return


                        #----------------------------
                        #Do not delete term
                        elif reaction.emoji == "❌":

                            term = str(tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", ""))
                            index = tabuVars.lst_Terms_already_loaded.index(term)

                            card_subject_words = tabuVars.tabu_card_list[index].split(":")[1]


                            botMessage = await fTESF.send_edit_embed_msg(term, card_subject_words, tabuLanguage, reaction.message.channel)

                            #-------------------------------------------------------
                            #Delete all edit-messages

                            await fTESF.delete_edit_msgs(reaction.message, tabuVars.tabu_edit_messages_list[user.id][0])
                            del tabuVars.tabu_edit_delete_card_list[user.id]

                            tabuVars.tabu_edit_messages_list[user.id][0] = [botMessage]

                    else:
                        fCU.log_In_Console("{} added a reaction on an delete term message, but he is not the current editor.".format(str(user.name)), "REACT-EDIT-DEL", "war")

                    return


                #------------------------------------------------------------------------------
                #Card-Edit-Message reaction
                elif tabuVars.tabu_edit_messages_list[user.id][0][0].id == reaction.message.id:

                    #--------------------------
                    #Edit word from term
                    if reaction.emoji == "✏️":

                        botMessage = await reaction.message.channel.send(tabuLanguage.tabu_edit_word)

                        tabuVars.tabu_edit_messages_list[user.id][0].append(botMessage)
                        tabuVars.tabu_edit_word_list[user.id] = tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", "")

                        return


                    #----------------------------
                    #Remove word from term
                    elif reaction.emoji == "✂️":

                        botMessage = await reaction.message.channel.send(tabuLanguage.tabu_edit_delete_word)

                        tabuVars.tabu_edit_messages_list[user.id][0].append(botMessage)
                        tabuVars.tabu_edit_delete_word_list[user.id] = tabuVars.tabu_edit_messages_list[user.id][1].content.replace(tabuVars.tabu_edit_messages_list[user.id][1].content.split(" ")[0] + " ", "")

                        return


                    #----------------------------
                    #Remove card
                    elif reaction.emoji == "🗑":

                        botMessage = await reaction.message.channel.send(tabuLanguage.tabu_edit_sure_delete_card)

                        await botMessage.add_reaction("✅")
                        await botMessage.add_reaction("❌")

                        tabuVars.tabu_edit_delete_card_list[user.id] = botMessage

                        return


                    #----------------------------
                    #Edit finish
                    elif reaction.emoji == "✅":
                        await fTESF.remove_user_from_edit_list_if_possible(user, tabuVars)


                else:
                    fCU.log_In_Console("{} added a reaction on an edit term message, but he is not the current editor.".format(str(user.name)), "REACT-EDIT", "war")


        return


    #Revanche?
    if reaction.message.channel.id == tabuSettings.tabu_channelID_team_1 or tabuSettings.tabu_channelID_team_2:
        if tabuVars.tabu_revenge_question:

            users = await reaction.users().flatten()

            for user in users:
                if user in tabuVars.tabu_player_list_last_game:
                    if user not in tabuVars.tabu_revenge_player_yes:
                        if reaction.emoji == "✅":


                            tabuVars.tabu_revenge_player_yes.append(user)

                            if len(tabuVars.tabu_revenge_player_yes) == len(tabuVars.tabu_player_list_last_game):

                                fCU.log_In_Console("An revenge starting in a few seconds...", "REACT REV", "inf")

                                tabuVars.tabu_revenge_question = False
                                tabuVars.tabu_player_list_all = tabuVars.tabu_player_list_last_game[:]
                                tabuVars.tabu_player_list_last_game = []


                                botMessage = await fDU.send_Message_To_Channel(tabuLanguage.tabu_revenge_starting, [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])
                                await fTOSG.on_Start_Game(True, tabuVars.tabu_revenge_asking_player_msg, tabuVars, tabuSettings, tabuLanguage, client)

                                
                                tabuVars.tabu_revenge_msgs.append(botMessage)
                                for old_card in tabuVars.tabu_revenge_msgs:
                                    try:
                                        await old_card.delete()
                                    except:
                                        pass


                                tabuVars.tabu_revenge_msgs = []
                                tabuVars.tabu_revenge_player_yes = []
                                tabuVars.tabu_revenge_asking_player_msg = None

                                return

                            
                        elif reaction.emoji == "❌":

                            fCU.log_In_Console("An revenge is canceled.", "REACT REV", "inf")

                            tabuVars.tabu_revenge_player_yes = []
                            tabuVars.tabu_revenge_question = False

                            botMessage = await fDU.send_Message_To_Channel(tabuLanguage.tabu_revenge_canceled, [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])

                            fCU.log_In_Console("Deleting all question-messages...", "REACT REV", "inf")

                            tabuVars.tabu_revenge_msgs.append(botMessage)
                            for old_card in tabuVars.tabu_revenge_msgs:
                                try:
                                    await old_card.delete()
                                except:
                                    pass

                            return


    #---------------------------------------------------------------------------
    #IN-Game reactions

    if not tabuVars.tabu_is_running:
        return


    #Bug (Doppelte Reaktionen) vermeiden
    if tabuVars.tabu_is_raeacting:
        return

    
    #Bug vermeiden
    if tabuVars.tabu_current_time <=1 and tabuVars.tabu_is_switching == False:
        return

    
    tabuVars.tabu_is_raeacting = True


    #Pause-Reaction
    if tabuVars.tabu_is_switching:

        if reaction.emoji == "⏸":

            if reaction.message.channel.id == tabuSettings.tabu_channelID_team_1 or reaction.message.channel.id == tabuSettings.tabu_channelID_team_2 or tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id == user.id or tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id == user.id:

                tabuVars.tabu_is_pause = True


                #Reaction von Pause auf Play aendern
                for countdown in tabuVars.tabu_time_messages:

                    if countdown.channel.type == discord.channel.ChannelType.private:

                        continue


                    msg_countdown = await countdown.channel.fetch_message(countdown.id)


                    for r in msg_countdown.reactions:
                        await msg_countdown.clear_reaction(r)

                    await countdown.add_reaction("▶️")


                tabuVars.tabu_is_raeacting = False
                return

        
        elif reaction.emoji == "▶️":

            if reaction.message.channel.id == tabuSettings.tabu_channelID_team_1 or reaction.message.channel.id == tabuSettings.tabu_channelID_team_2 or tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id == user.id or tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id == user.id:

                tabuVars.tabu_is_pause = False


                #Reaction von Play auf Pause aendern
                for countdown in tabuVars.tabu_time_messages:

                    if countdown.channel.type == discord.channel.ChannelType.private:
                        
                        continue


                    msg_countdown = await countdown.channel.fetch_message(countdown.id)


                    for r in msg_countdown.reactions:
                        await msg_countdown.clear_reaction(r)

                    await countdown.add_reaction("⏸")


                tabuVars.tabu_is_raeacting = False
                return


    #Privat Chat
    elif reaction.message.channel.type == discord.channel.ChannelType.private:

        #Abfragen welches Team gerade dran ist
        if tabuVars.tabu_guessing_team_num == 0:

            #Abfragen ob der Spieler noch Explainer ist
            if tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].id != user.id:
                tabuVars.tabu_is_raeacting = False
                return

        else:

            #Abfragen ob der Spieler noch Explainer ist
            if tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].id != user.id:
                tabuVars.tabu_is_raeacting = False
                return


    #Aus Team 1
    elif reaction.message.channel.id == tabuSettings.tabu_channelID_team_1:
        if tabuVars.tabu_guessing_team_num == 0:
            tabuVars.tabu_is_raeacting = False
            return

    #Aus Team 2
    elif reaction.message.channel.id == tabuSettings.tabu_channelID_team_2:
        if tabuVars.tabu_guessing_team_num == 1:
            tabuVars.tabu_is_raeacting = False
            return


    #Skipped
    if reaction.emoji == "⏩":

        fCU.log_In_Console("Team skipped a card.", "REACTION-ADD", "inf")

        #Bug vermeiden
        if tabuVars.tabu_current_time <= 1:
            tabuVars.tabu_is_raeacting = False
            return


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client)

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
    
    #Richtig
    elif reaction.emoji == "✅":

        if tabuVars.tabu_guessing_team_num == 0:

            fCU.log_In_Console("Team 1 get 10 points.", "REACTION-ADD", "inf")


            #Punkte hinzufuegen
            tabuVars.tabu_points_team_1 += 10
            tabuVars.tabu_points_this_round += 10


            #Hat Team gewonnen?
            if tabuVars.tabu_points_team_1 >= tabuVars.tabu_points_to_win:

                if tabuSettings.tabu_same_chance and tabuVars.tabu_start_team_num == tabuVars.tabu_guessing_team_num:
                    tabuVars.tabu_is_chance = True

                    if tabuVars.tabu_guessing_team_num == 0:
                        tabuVars.tabu_chance_team = 2
                    else:
                        tabuVars.tabu_chance_team = 1

                    
                else:

                    if tabuVars.tabu_was_chance == False:
                        await fTWM.team_1_won(tabuVars, tabuLanguage, tabuSettings, client)
                        return               


            fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")

        else:

            fCU.log_In_Console("Team 2 get 10 points.", "REACTION-ADD", "inf")


            #Punkte hinzufuegen
            tabuVars.tabu_points_team_2 += 10
            tabuVars.tabu_points_this_round += 10


            #Hat Team gewonnen?
            if tabuVars.tabu_points_team_2 >= tabuVars.tabu_points_to_win:

                if tabuSettings.tabu_same_chance and tabuVars.tabu_start_team_num == tabuVars.tabu_guessing_team_num:
                    tabuVars.tabu_is_chance = True

                    if tabuVars.tabu_guessing_team_num == 0:
                        tabuVars.tabu_chance_team = 2
                    else:
                        tabuVars.tabu_chance_team = 1
                    

                else:
                    
                    if tabuVars.tabu_was_chance == False:
                        await fTWM.team_2_won(tabuVars, tabuLanguage, tabuSettings, client)
                        return


            fCU.log_In_Console("[Points] Team-1: {} | Team-2: {}".format(str(tabuVars.tabu_points_team_1), str(tabuVars.tabu_points_team_2)), "REACTION-ADD", "inf")


        for old_card in tabuVars.tabu_guessing_card_messages:
            try:
                await old_card.delete()
            except:
                pass


        tabuVars.tabu_guessing_card_messages.clear()


        #Bug vermeiden
        if tabuVars.tabu_current_time <= 1:
            return


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client)

    
    #Falsche Antwort
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

        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client)