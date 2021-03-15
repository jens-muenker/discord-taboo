import os
import asyncio
import discord

import frosch2010_Console_Utils as fCU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_manage_terms as fTMT


async def team_1_won(tabuVars, tabuLanguage, tabuSettings, client):

    tabuVars.tabu_is_running = False

    fCU.log_In_Console("Team 1 won the game.", "WIN-MAN", "inf")


    #Get current Explainer channel
    if tabuVars.tabu_guessing_team_num == 0:

        explainer_channel = tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1]

    else:

        explainer_channel = tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2]


    for player in tabuVars.tabu_player_list_all:
        tabuVars.tabu_player_list_last_game.append(player)

    await fDU.send_Message_To_Channel(tabuLanguage.tabu_team_1_won, [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2), explainer_channel])
    await fTOF.create_and_send_win_graph(tabuVars, tabuSettings, tabuLanguage, client)
    await fTOF.delete_all_term_and_countdown_messages(tabuVars)


    fTOF.reset_all_vars(tabuVars)

    if tabuSettings.tabu_save_after_game:
        fTMT.save_terms(tabuVars)


async def team_2_won(tabuVars, tabuLanguage, tabuSettings, client):

    tabuVars.tabu_is_running = False


    fCU.log_In_Console("Team 2 won the game.", "WIN-MAN", "inf")


    #Get current Explainer channel
    if tabuVars.tabu_guessing_team_num == 0:

        explainer_channel = tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1]

    else:

        explainer_channel = tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2]


    await fDU.send_Message_To_Channel(tabuLanguage.tabu_team_2_won, [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2), explainer_channel])
    await fTOF.create_and_send_win_graph(tabuVars, tabuSettings, tabuLanguage, client)
    await fTOF.delete_all_term_and_countdown_messages(tabuVars)


    fTOF.reset_all_vars(tabuVars)

    if tabuSettings.tabu_save_after_game:
        fTMT.save_terms(tabuVars)