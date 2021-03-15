import discord
import asyncio
import copy

import frosch2010_Console_Utils as fCU
import frosch2010_Class_Utils as fCLU
import frosch2010_Tabu_other_funtions as fTOF
import frosch2010_Tabu_win_manager as fTWM


async def manage_timer(tabuVars, tabuSettings, tabuLanguage, client):

    #Beende Timer falls running=false (Spiel unterbrochen/beendet?)
    if not tabuVars.tabu_is_running:

        fCU.log_In_Console("Game is no longer running! Timer ended...", "MAN-TIMER","war")

        return

    
    #Print Countdown to all
    for countdown in tabuVars.tabu_time_messages:
        if tabuVars.tabu_is_running:
            if tabuVars.tabu_is_chance or tabuVars.tabu_was_chance:
                await countdown.edit(content=tabuLanguage.tabu_time_left.replace("[TIME_LEFT]", str(tabuVars.tabu_current_time)).replace("[POINTS_TEAM_1]", str(tabuVars.tabu_points_team_1)).replace("[POINTS_TEAM_2]", str(tabuVars.tabu_points_team_2)) + "\n\n" + tabuVars.tabu_chance_team.replace("[TEAM_NUM]", "2"))
            else:
                await countdown.edit(content=tabuLanguage.tabu_time_left.replace("[TIME_LEFT]", str(tabuVars.tabu_current_time)).replace("[POINTS_TEAM_1]", str(tabuVars.tabu_points_team_1)).replace("[POINTS_TEAM_2]", str(tabuVars.tabu_points_team_2)))


    #Ist die Zeit fuers Team abgelaufen?
    if tabuVars.tabu_current_time == 0:

        fCU.log_In_Console("Time is up!", "MAN-TIMER", "inf")
        tabuVars.tabu_current_time = copy.deepcopy(tabuSettings.tabu_round_lenght)

        tabuVars.tabu_is_switching = True


        #Loesche alle Guess-Cards vom "alten" Team
        fCU.log_In_Console("Deleting all old cards...", "MAN-TIMER", "inf")

        for old_card in tabuVars.tabu_guessing_card_messages:

            await old_card.delete()

        tabuVars.tabu_guessing_card_messages.clear()

        if tabuVars.tabu_guessing_team_num == 0:

            await tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].send(tabuLanguage.tabu_time_is_up, delete_after=4)

        else:

            await tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].send(tabuLanguage.tabu_time_is_up, delete_after=4)


        if tabuVars.tabu_is_chance and tabuVars.tabu_was_chance:

            if tabuVars.tabu_guessing_team_num == 0:
                tabuVars.tabu_points_history_team_1.append(tabuVars.tabu_points_this_round)
            else:
                tabuVars.tabu_points_history_team_2.append(tabuVars.tabu_points_this_round)


            if tabuVars.tabu_points_team_1 > tabuVars.tabu_points_team_2:
                await fTWM.team_1_won(tabuVars, tabuLanguage, tabuSettings, client)

            else:
                await fTWM.team_2_won(tabuVars, tabuLanguage, tabuSettings, client)

            return


        elif tabuVars.tabu_is_chance:
            tabuVars.tabu_was_chance = True


        #Teamwechsel
        fTOF.change_guessing_team(tabuVars)


        #Neuen Countdown an neuen Explainer senden
        await tabuVars.tabu_time_messages[2].delete()

        tabuVars.tabu_time_messages = tabuVars.tabu_time_messages[:2]

        await fTOF.send_Explainer_Countdown(tabuVars, tabuLanguage)


        #Allen Countdowns Pause-Reactions hinzufuegen
        for countdown in tabuVars.tabu_time_messages:

            if countdown.channel.type == discord.channel.ChannelType.private:

                continue

            await countdown.add_reaction("⏸")


        #Warte 10 Sec. bis es weiter geht
        waiting_time = copy.deepcopy(tabuSettings.tabu_switching_lenght) + 1

        while waiting_time > 0:

            if not tabuVars.tabu_is_pause:

                waiting_time -= 1


                for countdown in tabuVars.tabu_time_messages:

                    if waiting_time == 0:

                        await countdown.edit(content=tabuLanguage.tabu_it_will_start_soon)

                    else:

                        await countdown.edit(content=tabuLanguage.tabu_it_will_start_in.replace("[STARTING_IN]", str(waiting_time)))
            else:

                waiting_time = copy.deepcopy(tabuSettings.tabu_switching_lenght) + 1

                for countdown in tabuVars.tabu_time_messages:

                    await countdown.edit(content=tabuLanguage.tabu_game_paused)



            await asyncio.sleep(1)


        #Pause-Reations entfernen
        for countdown in tabuVars.tabu_time_messages:

            if countdown.channel.type == discord.channel.ChannelType.private:

                continue


            msg_countdown = await countdown.channel.fetch_message(countdown.id)


            for r in msg_countdown.reactions:
                await msg_countdown.clear_reaction(r)


        tabuVars.tabu_is_switching = False


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client)

        fCLU.Timer(1, manage_timer, [tabuVars, tabuSettings, tabuLanguage, client])

    else:

        tabuVars.tabu_current_time -= 1

        fCLU.Timer(1, manage_timer, [tabuVars, tabuSettings, tabuLanguage, client])