import discord
import discord.member
import asyncio
import json

import frosch2010_Tabu_variables
import frosch2010_Tabu_settings
import frosch2010_Console_Utils as fCU
import frosch2010_Tabu_On_Start_Game as fTOSG
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_On_Reaction as fTOREA
import frosch2010_Tabu_load_settings as fTLS
import frosch2010_Tabu_manage_terms as fTMT
import frosch2010_Tabu_On_Ready as fTOR


#-----------------------------------------------------
#Variables
#-----------------------------------------------------

tabuSettings = frosch2010_Tabu_settings.tabu_settings()
tabuVars = frosch2010_Tabu_variables.tabu_variables()


#-----------------------------------------------------
#Create Discord-Client
#-----------------------------------------------------

intents = discord.Intents.default()
client = discord.Client(intents=intents)


#-----------------------------------------------------
#Load-Files (Settings, Tabu-Terms)
#-----------------------------------------------------

def load_files(file_path=None):

    global tabuSettings
    global tabuVars

    fTLS.load_settings(tabuSettings, file_path)
    fTMT.load_terms(tabuVars, file_path)


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

    if not msg.content.lower().startswith("!tabu"):

        #Add term automatically 
        if msg.channel.id == tabuSettings.tabu_channelID_add_terms:

            tabuVars.tabu_card_list.append(msg.content)
            tabuVars.tabu_card_pool.append(msg.content)

            fCU.log_In_Console("{} added a new card.".format(str(msg.author.name)), "AUTO-ADD", "inf")

        return


    args = msg.content.split(" ")

    if len(args) <= 1:

        await fDU.send_Message_To_Channel("<@{}> you must have mistyped?".format(msg.author.id), [msg.channel])
        return


    #-------------------------------------------------------------------------
    #Stop Bot - COMMAND
    if args[1].lower() == "shutdown" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        save_term_vars = tabuSettings.tabu_default_save_terms
        args = msg.content.split(" ")

        if len(args) >= 4:

            if args[2].lower() == "without" and args[3].lower() == "save":

                save_term_vars = False

            elif args[2].lower() == "with" and args[3].lower() == "save":

                save_term_vars = True


        fCU.log_In_Console("Shut down bot... [SAVE-Terms: YES]", "STOP-COM", "inf") if save_term_vars else fCU.log_In_Console("Shut down bot... [SAVE-Terms: NO]", "STOP-COM", "inf")
        await fDU.send_Message_To_Channel("Shut down bot... [SAVE-Terms: YES]", [msg.channel]) if save_term_vars else await fDU.send_Message_To_Channel("Shut down bot... [SAVE-Terms: NO]", [msg.channel])

        
        if save_term_vars:
            fTMT.save_terms(tabuVars)


        fCU.log_In_Console("Finished. See you soon...", "STOP-COM", "inf")

        await client.logout()


    #-----------------------------------------------------------------------
    #Join Tabu - COMMAND
    elif args[1].lower() == "join" and msg.channel.id == tabuSettings.tabu_channelID_join:

        if tabuVars.tabu_is_running:

            fCU.log_In_Console("{} tried to join tabu. Tabu already running.".format(msg.author.name), "JOIN-COM","war")

            await fDU.send_Message_To_Channel("<@{}> there is already a game running. Please wait until it is finished.".format(msg.author.id), [msg.channel])

        else:

            if msg.author in tabuVars.tabu_player_list_all:

                fCU.log_In_Console("{} tried to join tabu. {} already joined.".format(msg.author.name, msg.author.name), "JOIN-COM","war")

                await fDU.send_Message_To_Channel("<@{}> you have already joined the game! Wait until it starts...".format(msg.author.id), [msg.channel])

            else:

                tabuVars.tabu_player_list_all.append(msg.author)

                fCU.log_In_Console("{} joined tabu. [{} Players]".format(msg.author.name, str(len(tabuVars.tabu_player_list_all))), "JOIN-COM","inf") if len(tabuVars.tabu_player_list_all) > 1 else fCU.log_In_Console("{} joined tabu. [{} Player]".format(msg.author.name, str(len(tabuVars.tabu_player_list_all))), "JOIN-COM","inf")

                await fDU.send_Message_To_Channel("<@{}> you have joined the game. [{} Player(s)]".format(msg.author.id, str(len(tabuVars.tabu_player_list_all))), [msg.channel])

        return


    #------------------------------------------------------------------------------------------------------------------
    #Pause - COMMAND
    elif args[1].lower() == "pause" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_1):

        if tabuVars.tabu_is_running:

            if tabuVars.tabu_is_pause:

                await msg.delete()

                tabuVars.tabu_is_pause = True

                fCU.log_In_Console("Game paused by {}.".format(str(msg.author.name)), "PAUSE-COM", "inf")

                await fDU.send_Message_To_Channel("Taboo was paused by {} ...".format(str(msg.author.name)), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])

            else:
                
                fCU.log_In_Console("{} tried to pause a paused game.".format(str(msg.author.name)), "PAUSE-COM", "war")

                await fDU.send_Message_To_Channel("Taboo is already paused.", [msg.channel], 8)

        else:

            fCU.log_In_Console("{} tried to pause a game, but currently no game is running.".format(str(msg.author.name)), "PAUSE-COM", "war")

            await fDU.send_Message_To_Channel("<@{}> currently no game running.".format(msg.author.id), [msg.channel])


    #--------------------------------------------------------------------------------------------------------------------
    #Unpause - COMMAND
    elif args[1].lower() == "unpause" and (msg.channel.id == tabuSettings.tabu_channelID_team_1 or msg.channel.id == tabuSettings.tabu_channelID_team_1):

        if tabuVars.tabu_is_running:

            if not tabuVars.tabu_is_pause:

                await msg.delete()

                tabuVars.tabu_is_pause = False

                fCU.log_In_Console("Game unpaused by {}.".format(str(msg.author.name)), "PAUSE-COM", "inf")

                await fDU.send_Message_To_Channel("Taboo unpaused by {}...".format(str(msg.author.name)), [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])

            else:
                
                fCU.log_In_Console("{} tried to pause a paused game.".format(str(msg.author.name)), "PAUSE-COM", "war")

                await fDU.send_Message_To_Channel("Taboo is currently not paused.", [msg.channel], 8)

        else:

            fCU.log_In_Console("{} tried to pause a game, but currently no game is running.".format(str(msg.author.name)), "PAUSE-COM", "war")

            await fDU.send_Message_To_Channel("<@{}> currently no game running.".format(msg.author.id), [msg.channel])


    #------------------------------------------------------------------------
    #Start - COMMAND
    elif args[1].lower() == "start" and msg.channel.id == tabuSettings.tabu_channelID_join:

        if tabuVars.tabu_is_running:

            await msg.channel.send("<@{}> there is already a game running. Please wait until it is finished.".format(msg.author.id))

            fCU.log_In_Console("{} tried to start a game. Game already running.".format(msg.author.name), "START-COM", "war")

        else:

            if len(tabuVars.tabu_player_list_all) <= tabuSettings.tabu_min_players:

                await fTOSG.on_Start_Game(msg, tabuVars, tabuSettings, client)

            else:

                await msg.channel.send("<@{}> more players are needed for a start! At least {} players are needed for a start.".format(msg.author.id, str(tabuSettings.tabu_min_players)))

                fCU.log_In_Console("{} tried to start, but more players are needed for a start! At least {} players are needed for a start.".format(msg.author.name, str(tabuSettings.tabu_min_players)), "START-COM", "war")


    #-----------------------------------------------------------------------
    #Load cards - COMMAND
    elif args[1].lower() == "load" and msg.channel.id == tabuSettings.tabu_channelID_bot_admin:

        if len(args) > 2:
            
            #Argument 2 = term
            if args[2].lower() == "cards":

                await msg.channel.send("<@{}> looking for new terms...".format(msg.author.id))
                fCU.log_In_Console("{} started loading process for new terms...".format(msg.author.name), "LOAD-COM", "inf")


                limit = None

                if len(args) > 3:

                    limit = int(args[3])


                #Get messages
                channel = client.get_channel(tabuSettings.tabu_channelID_add_terms)
                messages = await channel.history(limit=limit).flatten()


                lst_Terms_already_loaded = []
                count_new_cards = 0


                #Load all old terms in list
                for term in tabuVars.tabu_card_list:

                    lst_Terms_already_loaded.append(term.split(":")[0])



                #Check if term exists
                for message in messages:

                    term_array = message.content.split(":")

                    if not term_array[0] in lst_Terms_already_loaded:

                        lst_Terms_already_loaded.append(term_array[0])

                        tabuVars.tabu_card_list.append(message.content)
                        tabuVars.tabu_card_pool.append(message.content)

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


                await msg.channel.send("<@{}> Term-Search completed. {} new term(s) found.".format(msg.author.id, str(count_new_cards)))
                fCU.log_In_Console("Loading process finished. {} terms(s) found.".format(str(count_new_cards)), "LOAD-COM", "inf")

            else:

                await fDU.send_Message_To_Channel("<@{}> you must have mistyped?".format(msg.author.id), [msg.channel])

        else:

            await fDU.send_Message_To_Channel("<@{}> you must have mistyped?".format(msg.author.id), [msg.channel])


@client.event
async def on_reaction_add(reaction, user):

    if user.bot:
        return

    if not tabuVars.tabu_is_running:
        return


    Bug (Doppelte Reaktionen) vermeiden
    if tabuVars.tabu_is_raeacting:
        return

    
    if tabuVars.tabu_current_time <=1 and tabuVars.tabu_is_switching == False:
        return

    
    tabuVars.tabu_is_raeacting = True

    await fTOREA.on_Reaction_Add(reaction, user, tabuVars, tabuSettings, client)

#---------------------------------------------------------------------------------

load_files()

try:
    client.run(tabuSettings.tabu_bot_token)
except Exception as error:
    fCU.log_In_Console("{}".format(error), "START", "err")