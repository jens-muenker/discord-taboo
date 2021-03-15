import discord
import asyncio
import copy

import frosch2010_Console_Utils as fCU
import frosch2010_Class_Utils as fCLU
import frosch2010_Discord_Utils as fDU
import frosch2010_Tabu_other_funtions as fTOF

async def revenge_timer(tabuVars, tabuSettings, tabuLanguage, client):


    if not tabuVars.tabu_revenge_question:

        fCU.log_In_Console("Revenge question time ended...", "REV-TIMER","inf")
        return

    #Print Countdown to all
    for countdown in tabuVars.tabu_revenge_msgs:
        if tabuVars.tabu_revenge_question:
            try:
                await countdown.edit(content=tabuLanguage.tabu_revenge_asking.replace("[ASKING_USER_NAME]", tabuVars.tabuVars.tabu_revenge_asking_player_msg.author.name).replace("[REMAINING_TIME]", str(tabuVars.tabu_revenge_time)))
            except:
                pass


    #Ist die Zeit fuers Team abgelaufen?
    if tabuVars.tabu_revenge_time == 0:

        fCU.log_In_Console("Time is up!", "REV-TIMER", "inf")
        tabuVars.tabu_revenge_time = copy.deepcopy(tabuSettings.tabu_revenge_time)

        tabuVars.tabu_revenge_question = False


        botMessage = await fDU.send_Message_To_Channel(tabuLanguage.tabu_revenge_canceled, [client.get_channel(tabuSettings.tabu_channelID_team_1), client.get_channel(tabuSettings.tabu_channelID_team_2)])


        fCU.log_In_Console("Deleting all revenge questions...", "REV-TIMER", "inf")

        tabuVars.tabu_revenge_msgs.append(botMessage)
        for old_card in tabuVars.tabu_revenge_msgs:
            try:
                await old_card.delete()
            except:
                pass

        tabuVars.tabu_revenge_msgs = []
        tabuVars.tabu_revenge_player_yes = []
        tabuVars.tabu_revenge_asking_player_name = ""
        tabuVars.tabu_revenge_asking_player_msg = None

    else:

        tabuVars.tabu_revenge_time -= 1

        fCLU.Timer(1, revenge_timer, [tabuVars, tabuSettings, tabuLanguage, client])