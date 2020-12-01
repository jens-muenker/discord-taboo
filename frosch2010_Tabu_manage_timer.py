import discord
import asyncio
import copy

import frosch2010_Console_Utils as fCU
import frosch2010_Class_Utils as fCLU
import frosch2010_Tabu_other_funtions as fTOF

async def manage_timer(tabuVars, tabuSettings, client):

    #Exit timer if running=false (game interrupted/exited?)
    if not tabuVars.tabu_is_running:

        fCU.log_In_Console("Game is no longer running! Timer ended...", "MAN-TIMER","war")

        return

    
    #Print countdown to all
    for countdown in tabuVars.tabu_time_messages:

        if tabuVars.tabu_is_running:

            await countdown.edit(content="Time Remaining: {}".format(str(tabuVars.tabu_current_time)))


    #Is the time for the team over?
    if tabuVars.tabu_current_time == 0:

        fCU.log_In_Console("Time is up!", "MAN-TIMER", "inf")
        tabuVars.tabu_current_time = copy.deepcopy(tabuSettings.tabu_round_lenght)

        tabuVars.tabu_is_switching = True


        #Delete all Guess-Terms from the "old" team
        fCU.log_In_Console("Deleting all old cards...", "MAN-TIMER", "inf")

        for old_card in tabuVars.tabu_guessing_card_messages:

            await old_card.delete()

        tabuVars.tabu_guessing_card_messages.clear()

        if tabuVars.tabu_guessing_team_num == 0:

            await tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].send("Time is up!", delete_after=4)

        else:

            await tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].send("Time is up!", delete_after=4)


        #Team change
        fTOF.change_guessing_team(tabuVars)


        #Send new countdown to new explainer
        await tabuVars.tabu_time_messages[2].delete()

        tabuVars.tabu_time_messages = tabuVars.tabu_time_messages[:2]

        await fTOF.send_Explainer_Countdown(tabuVars)


        #Add pause reactions to all countdowns
        for countdown in tabuVars.tabu_time_messages:

            await countdown.add_reaction("⏸")


        #Wait for team change
        waiting_time = copy.deepcopy(tabuSettings.tabu_switching_lenght) + 1

        while waiting_time > 0:

            if not tabuVars.tabu_is_pause:

                waiting_time -= 1


                for countdown in tabuVars.tabu_time_messages:

                    if waiting_time == 0:

                        await countdown.edit(content="It will start soon...")

                    else:

                        await countdown.edit(content="Soon it starts in: {}".format(str(waiting_time)))
            else:

                waiting_time = copy.deepcopy(tabuSettings.tabu_switching_lenght) + 1

                for countdown in tabuVars.tabu_time_messages:

                    await countdown.edit(content="Continuation paused...")


            await asyncio.sleep(1)


        #Remove pause-reactions
        for countdown in tabuVars.tabu_time_messages:

            for r in countdown.reactions:
                await countdown.clear_reaction(r)


        tabuVars.tabu_is_switching = False


        await fTOF.send_New_Word_Card(tabuVars, tabuSettings, client)

        fCLU.Timer(1, manage_timer, [tabuVars, tabuSettings, client])

    else:

        tabuVars.tabu_current_time -= 1

        fCLU.Timer(1, manage_timer, [tabuVars, tabuSettings, client])