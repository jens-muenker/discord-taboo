import discord
import discord.member
import asyncio
import json

import frosch2010_Tabu_language
import frosch2010_Tabu_variables
import frosch2010_Tabu_settings
import frosch2010_Console_Utils as fCU
import frosch2010_Class_Utils as fCLU
import frosch2010_Tabu_On_Start_Game as fTOSG
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_On_Reaction as fTOREA
import frosch2010_Tabu_load_settings as fTLS
import frosch2010_Tabu_manage_terms as fTMT
import frosch2010_Tabu_load_language as fTLL
import frosch2010_Tabu_On_Ready as fTOR
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Tabu_edit_system_functions as fTESF
import frosch2010_Tabu_revenge_timer as fTRT


#-----------------------------------------------------
#Variables
#-----------------------------------------------------

tabuSettings = frosch2010_Tabu_settings.tabu_settings()
tabuVars = frosch2010_Tabu_variables.tabu_variables()
tabuLanguage = frosch2010_Tabu_language.tabu_language()


#-----------------------------------------------------
#Create Discord-Client
#-----------------------------------------------------

intents = discord.Intents.all()
client = discord.Client(intents=intents)


#-----------------------------------------------------
#Load-Files (Settings, Tabu-Terms)
#-----------------------------------------------------

def load_files(file_path=None):

    global tabuSettings
    global tabuVars
    global tabuLanguage

    fTLS.load_settings(tabuSettings, file_path)
    fTMT.load_terms(tabuVars, file_path)
    fTLL.load_language(tabuLanguage, file_path)


#-----------------------------------------------------
#Discord-Client-Events
#-----------------------------------------------------

@client.event
async def on_ready():

    await fTOR.on_ready(tabuSettings, client)


@client.event
async def on_message(msg):

    global tabuSettings
    global tabuVars

    if msg.author.bot:
        return


    #-----------------------------------------------------------
    #Edit - COMMAND
    if msg.channel.id == tabuSettings.tabu_channelID_add_terms:

        if msg.content.lower().startswith("!edit"):

            edit_array = str(msg.content).split(" ")

            if len(edit_array) < 2:
                await fDU.send_Message_To_Channel(tabuLanguage.tabu_false_edit_term_format.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel], tabuSettings.tabu_message_auto_delete)
                return

            edit_term = str(msg.content).replace(edit_array[0] + " ", "")

            if edit_term not in tabuVars.lst_Terms_already_loaded:
                await fDU.send_Message_To_Channel(tabuLanguage.tabu_edit_term_not_exist.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel], tabuSettings.tabu_message_auto_delete)
                fCU.log_In_Console("{} tried to edit a term, which does not exist.".format(str(msg.author.name)), "EDIT-COM", "inf")
                return


            if edit_term in tabuVars.tabu_edit_term_list:
                await fDU.send_Message_To_Channel(tabuLanguage.tabu_edit_term_has_an_editor.replace("[USER_ID]", "<@" + str(msg.author.id) + ">").replace("[EDITOR_ID]", "<@" + str(tabuVars.tabu_edit_term_list[edit_array[1]]) + ">"), [msg.channel], tabuSettings.tabu_message_auto_delete)
                fCU.log_In_Console("{} tried to edit a term that is already edited by someone else.".format(str(msg.author.name)), "EDIT-COM", "inf")
                return


            card_subject = edit_term
            card_subject_words = tabuVars.tabu_card_list[tabuVars.lst_Terms_already_loaded.index(edit_term)].split(":")[1]


            botMessage = await fTESF.send_edit_embed_msg(card_subject, card_subject_words, tabuLanguage, msg.channel)


            tabuVars.tabu_edit_term_list[card_subject] = msg.author.id
            tabuVars.tabu_edit_messages_list[msg.author.id] = [[botMessage], msg]           

            return

        else:

            #-------------------------------------------------------
            #Edit word from term
            if "=:=" in str(msg.content):

                if msg.author.id in tabuVars.tabu_edit_word_list:
                
                    term = str(tabuVars.tabu_edit_word_list[msg.author.id])
                    word_edit = str(msg.content).split("=:=")
                    index = tabuVars.lst_Terms_already_loaded.index(term)
                    userID = msg.author.id


                    tabuVars.tabu_card_list[index] = str(tabuVars.tabu_card_list[index]).replace(word_edit[0], word_edit[1])
                    tabuVars.lst_Terms_already_loaded[index] = tabuVars.tabu_card_list[index].split(":")[0]

                    
                    await msg.add_reaction("✅")


                    del tabuVars.tabu_edit_word_list[userID]
                    fTMT.save_terms(tabuVars)


                    card_subject_words = tabuVars.tabu_card_list[index].split(":")[1]

                    botMessage = await fTESF.send_edit_embed_msg(term, card_subject_words, tabuLanguage, msg.channel)


                    for msg in tabuVars.tabu_edit_messages_list[userID][0]:
                        try:
                            await msg.delete()
                        except:
                            fCU.log_In_Console("Failed to delete edit message.", "MAIN-MSG", "err")


                    tabuVars.tabu_edit_messages_list[userID][0] = [botMessage]

                else:
                    await msg.add_reaction("❌")

                return

            #-------------------------------------------------------
            #Remove word from term
            if msg.author.id in tabuVars.tabu_edit_delete_word_list:

                term = str(tabuVars.tabu_edit_delete_word_list[msg.author.id])
                index = tabuVars.lst_Terms_already_loaded.index(term)
                userID = msg.author.id

                if msg.content in tabuVars.tabu_card_list[index]:
                    await msg.add_reaction("🗑")
                    fCU.log_In_Console("{} removed a word from the term {}.".format(str(msg.author.name), str(term)), "MAIN-MSG", "inf")

                else:
                    await msg.add_reaction("❌")
                    fCU.log_In_Console("{} tried to remove a word from the term {}, which does not exist.".format(str(msg.author.name), str(term)), "MAIN-MSG", "inf")


                if tabuVars.tabu_card_list[index] in tabuVars.tabu_card_pool:
                    tabuVars.tabu_card_pool = str(tabuVars.tabu_card_list[index]).replace("," + msg.content, "").replace(msg.content, "")

                tabuVars.tabu_card_list[index] = str(tabuVars.tabu_card_list[index]).replace("," + msg.content, "").replace(msg.content, "")


                del tabuVars.tabu_edit_delete_word_list[userID]

                for msg in tabuVars.tabu_edit_messages_list[userID][0]:
                    try:
                        await msg.delete()
                    except:
                        fCU.log_In_Console("Failed to delete edit message.", "MAIN-MSG", "err")


                fTMT.save_terms(tabuVars)



                #Send new message for editing
                card_subject_words = tabuVars.tabu_card_list[index].split(":")[1]

                botMessage = await fTESF.send_edit_embed_msg(term, card_subject_words, tabuLanguage, msg.channel)

                tabuVars.tabu_edit_messages_list[userID][0] = [botMessage]

                return


            #-----------------------------------------------------------------------------------------------------------------------
            #Remove user if he previously wanted to edit a term
            await fTESF.remove_user_from_edit_list_if_possible(msg.author, tabuVars)


            #-----------------------------------------------------------------------------------------------------------------------
            #Check if the user has added a word to a term or added a new term

            term_array = str(msg.content).replace(": ", ":").replace(", ", ",").split(":")

            if len(term_array) < 2:
                await fDU.send_Message_To_Channel(tabuLanguage.tabu_false_term_format.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel], tabuSettings.tabu_message_auto_delete)
                return

            if not term_array[0] in tabuVars.lst_Terms_already_loaded:

                tabuVars.lst_Terms_already_loaded.append(term_array[0])

                tabuVars.tabu_card_list.append(str(msg.content).replace(": ", ":").replace(", ", ","))
                tabuVars.tabu_card_pool.append(str(msg.content).replace(": ", ":").replace(", ", ","))


                await msg.add_reaction("🆕")
                fCU.log_In_Console("{} added a new term.".format(str(msg.author.name)), "AUTO-ADD", "inf")

            else:

                index = [tabuVars.tabu_card_list.index(card) for card in tabuVars.tabu_card_list if card.startswith(term_array[0])][0]

                term_content = term_array[1].split(",")

                existing_term_content = tabuVars.tabu_card_list[index].split(":")[1]

                new_term = tabuVars.tabu_card_list[index][:]

                for word in term_content:

                    if not word in existing_term_content:

                        new_term += "," + word

                tabuVars.tabu_card_list[index] = new_term[:]


                await msg.add_reaction("➕")
                fCU.log_In_Console("{} add words to a term.".format(str(msg.author.name)), "AUTO-ADD", "inf")

            if tabuSettings.tabu_save_after_auto_add:

                fTMT.save_terms(tabuVars)

        return
    
    #-----------------------------------------------------------------------------------------------------------------------
    #Check messagesfor commands


    if not msg.content.lower().startswith("!tabu"):
        return


    args = msg.content.split(" ")

    if len(args) <= 1:

        await fDU.send_Message_To_Channel(tabuLanguage.tabu_wrong_arguments.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])
        return


    #--------------------------------------------------------------------------------------------
    #Shutdown Bot - COMMAND
    if args[1].lower() == "shutdown" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        save_term_vars = tabuSettings.tabu_default_save_terms
        args = msg.content.split(" ")

        if len(args) >= 4:

            if args[2].lower() == "without" and args[3].lower() == "save":

                save_term_vars = False

            elif args[2].lower() == "with" and args[3].lower() == "save":

                save_term_vars = True


        fCU.log_In_Console("Shut down bot... [SAVE-Terms: YES]", "SHUTDOWN-COM", "inf") if save_term_vars else fCU.log_In_Console("Shut down bot... [SAVE-Terms: NO]", "SHUTDOWN-COM", "inf")
        await fDU.send_Message_To_Channel(tabuLanguage.tabu_shutdown_bot + " [SAVE-Terms: YES]", [msg.channel]) if save_term_vars else await fDU.send_Message_To_Channel(tabuLanguage.tabu_shutdown_bot + " [SAVE-Terms: NO]", [msg.channel])

        
        if save_term_vars:
            fTMT.save_terms(tabuVars)


        fCU.log_In_Console("Finished. See you soon...", "SHUTDOWN-COM", "inf")

        await client.logout()


    #----------------------------------------------------------------------------------------------
    #TEMP - REVANCHE - COMMAND
    elif args[1].lower() == "revanche" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_2):

        tabuVars.tabu_revenge_question = True
        tabuVars.tabu_revenge_asking_player_msg = msg
        tabuVars.tabu_revenge_time = tabuSettings.tabu_revenge_time

        team_channels = [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)]

        for team in team_channels:

            botMessage = await team.send(tabuLanguage.tabu_revenge_asking.replace("[ASKING_USER_NAME]", tabuVars.tabu_revenge_asking_player_msg.author.name).replace("[REMAINING_TIME]", str(tabuVars.tabu_revenge_time)))

            await botMessage.add_reaction("✅")
            await botMessage.add_reaction("❌")

            tabuVars.tabu_revenge_msgs.append(botMessage)

        fCLU.Timer(1, fTRT.revenge_timer, [tabuVars, tabuSettings, tabuLanguage, client])

        return


    #-------------------------------------------------------------------------------------
    #Join Tabu - COMMAND
    elif args[1].lower() == "join" and msg.channel.id == tabuSettings.tabu_channelID_join:

        if tabuVars.tabu_is_running:

            fCU.log_In_Console("{} tried to join tabu. Tabu already running.".format(msg.author.name), "JOIN-COM","war")

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_already_running.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

        else:

            if msg.author in tabuVars.tabu_player_list_all:

                fCU.log_In_Console("{} tried to join tabu. {} already joined.".format(msg.author.name, msg.author.name), "JOIN-COM","war")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_user_already_joined.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

            else:

                tabuVars.tabu_player_list_all.append(msg.author)

                fCU.log_In_Console("{} joined tabu. [{} Players]".format(msg.author.name, str(len(tabuVars.tabu_player_list_all))), "JOIN-COM","inf") if len(tabuVars.tabu_player_list_all) > 1 else fCU.log_In_Console("{} joined tabu. [{} Player]".format(msg.author.name, str(len(tabuVars.tabu_player_list_all))), "JOIN-COM","inf")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_user_joined_game.replace("[USER_ID]", "<@" + str(msg.author.id) + ">").replace("[PLAYER_JOINED_COUNT]", str(len(tabuVars.tabu_player_list_all))), [msg.channel])

        return


    #--------------------------------------------------------------------------------------------------------------------------------------------------
    #Pause - COMMAND
    elif args[1].lower() == "pause" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_2):

        if tabuVars.tabu_is_running:

            if tabuVars.tabu_is_pause:

                await msg.delete()

                tabuVars.tabu_is_pause = True

                fCU.log_In_Console("Game paused by {}.".format(str(msg.author.name)), "PAUSE-COM", "inf")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_paused_by.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])

            else:
                
                fCU.log_In_Console("{} tried to pause a paused game.".format(str(msg.author.name)), "PAUSE-COM", "war")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_already_paused, [msg.channel], 8)

        else:

            fCU.log_In_Console("{} tried to pause a game, but currently no game is running.".format(str(msg.author.name)), "PAUSE-COM", "war")

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_no_game_running.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])


    #----------------------------------------------------------------------------------------------------------------------------------------------------
    #Unpause - COMMAND
    elif args[1].lower() == "unpause" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_2):

        if tabuVars.tabu_is_running:

            if not tabuVars.tabu_is_pause:

                await msg.delete()

                tabuVars.tabu_is_pause = False

                fCU.log_In_Console("Game unpaused by {}.".format(str(msg.author.name)), "PAUSE-COM", "inf")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_unpaused_by.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])

            else:
                
                fCU.log_In_Console("{} tried to pause a paused game.".format(str(msg.author.name)), "PAUSE-COM", "war")

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_is_not_paused, [msg.channel], 8)

        else:

            fCU.log_In_Console("{} tried to pause a game, but currently no game is running.".format(str(msg.author.name)), "PAUSE-COM", "war")

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_no_game_running.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])


    #--------------------------------------------------------------------------------------
    #Start - COMMAND
    elif args[1].lower() == "start" and msg.channel.id == tabuSettings.tabu_channelID_join:

        if tabuVars.tabu_is_running:

            await msg.channel.send(tabuLanguage.tabu_game_already_running.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"))

            fCU.log_In_Console("{} tried to start a game. Game already running.".format(msg.author.name), "START-COM", "war")

        else:

            if len(tabuVars.tabu_player_list_all) >= tabuSettings.tabu_min_players:

                await fTOSG.on_Start_Game(False, msg, tabuVars, tabuSettings, tabuLanguage, client)

            else:

                await msg.channel.send(tabuLanguage.tabu_more_players_needed.replace("[USER_ID]", "<@" + str(msg.author.id) + ">").replace("[MIN_PLAYER_COUNT]", str(tabuSettings.tabu_min_players)))

                fCU.log_In_Console("{} tried to start, but more players are needed for a start! At least {} players are needed for a start.".format(msg.author.name, str(tabuSettings.tabu_min_players)), "START-COM", "war")


    #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    #Stop-Game - COMMAND
    elif args[1].lower() == "stop" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_2 or msg.channel.id == tabuSettings.tabu_channelID_bot_admin):

        if tabuVars.tabu_is_running:

            if msg.author in tabuVars.tabu_player_list_all:

                fCU.log_In_Console("{} stopped taboo.".format(msg.author.name), "STOP-COM", "inf")

                tabuVars.tabu_is_running = False


                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_stopped_by.replace("[USER_NAME]", str(msg.author.name)), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])
                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_stopped_by.replace("[USER_NAME]", str(msg.author.name)), [msg.channel], 6)


                for term in tabuVars.tabu_guessing_card_messages:
                    try:
                        await term.delete()
                    except:
                        pass


                for countdown in tabuVars.tabu_time_messages:
                    try:
                        await countdown.delete()
                    except:
                        pass


                fTOF.reset_all_vars(tabuVars)

            else:

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_game_cant_stopped.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel], 4)

                fCU.log_In_Console("{} tried to stop taboo. But he does not play along!".format(msg.author.name), "STOP-COM", "war")

        else:

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_no_game_running.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])


    #------------------------------------------------------------------------------------------
    #Tabu-Save - COMMAND
    elif args[1].lower() == "save" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        await fDU.send_Message_To_Channel(tabuLanguage.tabu_save.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

        fCU.log_In_Console("{} saved")

        fTMT.save_terms(tabuVars)


    #------------------------------------------------------------------------------------------
    #Kick-Player - COMMAND
    elif args[1].lower() == "kick" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        if len(args) > 2:

            if len(msg.mentions) > 0:

                kick_user = await client.fetch_user(msg.mentions[0].id)

                if kick_user in tabuVars.tabu_player_list_all:

                    if (tabuVars.tabu_guessing_team_num == 0 and kick_user == tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1]) or (tabuVars.tabu_guessing_team_num == 1 and tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2]):

                        await fDU.send_Message_To_Channel(tabuLanguage.tabu_cant_kick_current_explainer.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

                    else:

                        tabuVars.tabu_player_list_all.remove(kick_user)

                        if kick_user in tabuVars.tabu_player_list_team_1:

                            tabuVars.tabu_player_list_team_1.remove(kick_user)

                        else:

                            tabuVars.tabu_player_list_team_2.remove(kick_user)


                        await fDU.send_Message_To_Channel(tabuLanguage.tabu_user_kicked, [msg.channel])

                        fCU.log_In_Console("{} kicked player {}".format(str(msg.author.name), str(kick_user.name)))

                else:

                    await fDU.send_Message_To_Channel(tabuLanguage.tabu_kick_user_isnt_player.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

            else:

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_no_kick_user.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

        else:

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_wrong_arguments.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])


    #------------------------------------------------------------------------------------------
    #Load cards - COMMAND
    elif args[1].lower() == "load" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        if len(args) > 2:
            
            #Argument 2 = cards
            if args[2].lower() == "cards":

                await msg.channel.send(tabuLanguage.tabu_search_for_new_terms.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"))
                fCU.log_In_Console("{} started loading process for new cards...".format(msg.author.name), "LOAD-COM", "inf")


                limit = None

                if len(args) > 3:

                    limit = int(args[3])


                #Nachrichten abrufen
                channel = client.get_channel(tabuSettings.tabu_channelID_add_terms)
                messages = await channel.history(limit=limit).flatten()


                lst_Terms_already_loaded = []
                count_new_cards = 0


                #Alte Karten in vorhanden laden
                for term in tabuVars.tabu_card_list:

                    lst_Terms_already_loaded.append(term.split(":")[0])



                #Ueberpruefen, ob Card schon vorhanden
                for message in messages:

                    term_array = str(message.content).replace(": ", ":").replace(", ", ",").split(":")

                    if not term_array[0] in lst_Terms_already_loaded:

                        lst_Terms_already_loaded.append(term_array[0])

                        tabuVars.tabu_card_list.append(str(message.content).replace(": ", ":").replace(", ", ","))
                        tabuVars.tabu_card_pool.append(str(message.content).replace(": ", ":").replace(", ", ","))

                        count_new_cards += 1

                    else:

                        index = [tabuVars.tabu_card_list.index(card) for card in tabuVars.tabu_card_list if card.startswith(term_array[0])][0]

                        term_content = term_array[1].split(",")

                        existing_term_content = tabuVars.tabu_card_list[index].split(":")[1]

                        new_term = tabuVars.tabu_card_list[index][:]

                        for word in term_content:

                            if not word in existing_term_content:

                                new_term += "," + word

                        tabuVars.tabu_card_list[index] = new_term


                await msg.channel.send(tabuLanguage.tabu_search_for_new_terms_finished.replace("[USER_ID]", "<@" + str(msg.author.id) + ">").replace("[COUNT_NEW_TERMS]", str(count_new_cards)))
                fCU.log_In_Console("Loading process finished. {} card(s) found.".format(str(count_new_cards)), "LOAD-COM", "inf")

            else:

                await fDU.send_Message_To_Channel(tabuLanguage.tabu_wrong_arguments.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])

        else:

            await fDU.send_Message_To_Channel(tabuLanguage.tabu_wrong_arguments.replace("[USER_ID]", "<@" + str(msg.author.id) + ">"), [msg.channel])


@client.event
async def on_reaction_add(reaction, user):

    if user.bot:
        return

    await fTOREA.on_Reaction_Add(reaction, user, tabuVars, tabuSettings, tabuLanguage, client)

#---------------------------------------------------------------------------------

load_files()

try:
    client.run(tabuSettings.tabu_bot_token)
except Exception as error:
    fCU.log_In_Console("{}".format(error), "START", "err")