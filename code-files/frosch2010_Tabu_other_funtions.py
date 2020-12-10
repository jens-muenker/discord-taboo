import discord
from random import shuffle
from random import randrange
import os
import matplotlib.pyplot as plt, numpy as np

import frosch2010_Tabu_variables as fTV
import frosch2010_Console_Utils as fCU


async def print_Who_Which_Team(tabuVars, channel):

    team1 = ""

    for player in tabuVars.tabu_player_list_team_1:

        team1 += player.name + ", "

    team1 = team1[:int(len(team1) - 2)]


    team2 = ""

    for player in tabuVars.tabu_player_list_team_2:

        team2 += player.name + ", "

    team2 = team2[:int(len(team2) - 2)]


    embed = discord.Embed(title="Team 1", description=team1, color=0x22a7f0)
    await channel.send(embed=embed)

    embed1 = discord.Embed(title="Team 2", description=team2, color=0xC0392B)
    await channel.send(embed=embed1)


async def send_Card_To_Team(card, tabuVars, tabuSettings, tabuLanguage, client):
    
    card_subject = card.split(":")
    card_subject_words = card.split(":")[1].replace(",", "\n")


    if tabuVars.tabu_guessing_team_num == 0:

        channel = client.get_channel(tabuSettings.tabu_channelID_team_2)

    else:

        channel = client.get_channel(tabuSettings.tabu_channelID_team_1)


    embed = discord.Embed(title=tabuLanguage.tabu_card_term_prefix + card_subject[0], description=tabuLanguage.tabu_card_term_suffix, color=0x22a7f0)
    embed.add_field(name="###############################", value=card_subject_words, inline=True)

    botMessage = await channel.send(embed=embed)

    await botMessage.add_reaction("✅")
    await botMessage.add_reaction("❌")

    tabuVars.tabu_guessing_card_messages.append(botMessage)


async def send_Card_To_Player(card, player, tabuVars, tabuLanguage):
    
    card_subject = card.split(":")
    card_subject_words = card.split(":")[1].replace(",", "\n")

    embed = discord.Embed(title=tabuLanguage.tabu_card_term_prefix + card_subject[0], description=tabuLanguage.tabu_card_term_suffix, color=0x22a7f0)
    embed.add_field(name="###############################", value=card_subject_words, inline=True)

    botMessage = await player.send(embed=embed)

    await botMessage.add_reaction("⏩")
    await botMessage.add_reaction("✅")
    await botMessage.add_reaction("❌")

    tabuVars.tabu_guessing_card_messages.append(botMessage)


async def send_Team_Countdowns(tabuVars, tabuSettings, tabuLanguage, client):

    #Team 1
    channel_team_1 = client.get_channel(tabuSettings.tabu_channelID_team_1)

    team_1_countdown = await channel_team_1.send(tabuLanguage.tabu_time_left.replace("[TIME_LEFT]", str(tabuVars.tabu_current_time)))

    tabuVars.tabu_time_messages.append(team_1_countdown)

    #Team 2
    channel_team_2 = client.get_channel(tabuSettings.tabu_channelID_team_2)

    team_2_countdown = await channel_team_2.send(tabuLanguage.tabu_time_left.replace("[TIME_LEFT]", str(tabuVars.tabu_current_time)))

    tabuVars.tabu_time_messages.append(team_2_countdown)


async def send_Explainer_Countdown(tabuVars, tabuLanguage):

    if tabuVars.tabu_guessing_team_num == 0:

        player_countdown = await tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1].send(tabuLanguage.tabu_it_will_start_soon)

        tabuVars.tabu_time_messages.append(player_countdown)

    else:

        player_countdown = await tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2].send(tabuLanguage.tabu_it_will_start_soon)

        tabuVars.tabu_time_messages.append(player_countdown)


async def create_and_send_win_graph(tabuVars, tabuSettings, tabuLanguage, client):

    #X-Achse fuer Grafik erstellen
    x_axis_team_1 = []
    x_axis_team_2 = []

    for index in range(len(tabuVars.tabu_points_history_team_1)):
        x_axis_team_1.append(index)

    for index in range(len(tabuVars.tabu_points_history_team_2)):
        x_axis_team_2.append(index)

    #Grafik erstellen
    with plt.style.context('fivethirtyeight'):

        fig = plt.figure()
        plt.plot(x_axis_team_1, tabuVars.tabu_points_history_team_1, label = "Team 1")
        plt.plot(x_axis_team_2, tabuVars.tabu_points_history_team_2, label = "Team 2")


        #X-Achsenbeschriftung festlegen
        if len(x_axis_team_1) >= len(x_axis_team_2):

            plt.xticks(range(len(x_axis_team_1)), x_axis_team_1)

        else:

            plt.xticks(range(len(x_axis_team_2)), x_axis_team_2)


        plt.title("\nTeam 1: {} {} | Team 2: {} {}\n".format(str(tabuVars.tabu_points_team_1), str(tabuLanguage.tabu_graph_points), str(tabuVars.tabu_points_team_2), str(tabuLanguage.tabu_graph_points)), fontsize=16)
        plt.ylabel(tabuLanguage.tabu_graph_points_per_round, fontsize=10)
        plt.xlabel(tabuLanguage.tabu_graph_round, fontsize=10)

        plt.legend(bbox_to_anchor=(1.05, 1), loc='lower left', borderaxespad=0.)

        plt.grid(True)

        plt.savefig("Stats.png", bbox_inches = "tight", dip = 300)


    #An Team-Channels versenden
    channel = client.get_channel(tabuSettings.tabu_channelID_team_1)
    await channel.send(file=discord.File("Stats.png"))

    channel = client.get_channel(tabuSettings.tabu_channelID_team_2)
    await channel.send(file=discord.File("Stats.png"))

    os.remove("Stats.png")


async def send_New_Word_Card(tabuVars, tabuSettings, tabuLanguage, client):

    fCU.log_In_Console("Checking if old card-messages exists...", "NEW-CARD", "inf")


    #Alte Karte loeschen, wenn vorhanden
    if len(tabuVars.tabu_guessing_card_messages) > 0:

        fCU.log_In_Console("Delete old card-messages...", "NEW-CARD", "inf")


        for old_card in tabuVars.tabu_guessing_card_messages:

            try:
            
                await old_card.delete()

            except:

                fCU.log_In_Console("Failed to delete old card.", "NEW-CARD", "err")

        tabuVars.tabu_guessing_card_messages.clear()


    #Gibt es noch Karten im Deck?
    if len(tabuVars.tabu_card_pool) == 1:

        fCU.log_In_Console("No cards in pool.", "NEW-CARD", "err")

        tabuVars.tabu_card_pool = tabuVars.tabu_card_list.copy()


    #Karte aus Liste auswaehlen & anschliessend aus Liste loeschen
    fCU.log_In_Console("GET new card...", "NEW-CARD", "inf")

    shuffle(tabuVars.tabu_card_pool)


    card_id = randrange(0, (len(tabuVars.tabu_card_pool) - 1))

    card = tabuVars.tabu_card_pool[card_id]

    del tabuVars.tabu_card_pool[card_id]


    #Verbotene Begriffe kuerzen, wenn mehr als 5

    card_array = card.split(":")
    card_words = card_array[1].split(",")

    if len(card_words) > 5:

        shuffle(card_words)

        card = card_array[0] + ":"

        for i in range(0, 5):

            if i == 0:

                card += card_words[i]

            else:

                card += "," + card_words[i]


    tabuVars.tabu_is_raeacting = False


    #Begriff zum Gegner-Team & Erklaerer senden
    fCU.log_In_Console("Send card to team and explainer...", "NEW-CARD", "inf")

    if tabuVars.tabu_guessing_team_num == 0:

        await send_Card_To_Team(card, tabuVars, tabuSettings, tabuLanguage, client)

        await send_Card_To_Player(card, tabuVars.tabu_player_list_team_1[tabuVars.tabu_explainer_team_1], tabuVars, tabuLanguage)

    else:

        await send_Card_To_Team(card, tabuVars, tabuSettings, tabuLanguage, client)

        await send_Card_To_Player(card, tabuVars.tabu_player_list_team_2[tabuVars.tabu_explainer_team_2], tabuVars, tabuLanguage)


def change_guessing_team(tabuVars):

    fCU.log_In_Console("Change guessing team...", "CHANGE-TEAM", "inf")

    if tabuVars.tabu_guessing_team_num == 0:

        tabuVars.tabu_points_history_team_1.append(tabuVars.tabu_points_this_round)

        tabuVars.tabu_points_this_round = 0

        if tabuVars.tabu_explainer_team_1 == (len(tabuVars.tabu_player_list_team_1) - 1):

            tabuVars.tabu_explainer_team_1 = 0

        else:

            tabuVars.tabu_explainer_team_1 += 1

        tabuVars.tabu_guessing_team_num = 1

        fCU.log_In_Console("Now team 2 turn", "CHANGE-TEAM", "inf")

    else:

        tabuVars.tabu_points_history_team_2.append(tabuVars.tabu_points_this_round)

        tabuVars.tabu_points_this_round = 0

        if tabuVars.tabu_explainer_team_2 == (len(tabuVars.tabu_player_list_team_2) - 1):

            tabuVars.tabu_explainer_team_2 = 0

        else:

            tabuVars.tabu_explainer_team_2 += 1

        tabuVars.tabu_guessing_team_num = 0

        fCU.log_In_Console("Now team 1 turn", "CHANGE-TEAM", "inf")


async def delete_all_term_and_countdown_messages(tabuVars):

    #Alle alten Term-Messages loeschen
    for old_card in tabuVars.tabu_guessing_card_messages:
        try:
            await old_card.delete()
        except:
            pass


    #Alle alten Countdown-Messages loeschen
    for old_countdown in tabuVars.tabu_time_messages:
        try:
            await old_countdown.delete()
        except:
            pass


def reset_all_vars(tabuVars):

    tabuVars.tabu_player_list_all = []
    tabuVars.tabu_player_list_team_1 = []
    tabuVars.tabu_player_list_team_2 = []

    tabuVars.tabu_points_team_1 = 0
    tabuVars.tabu_points_team_2 = 0

    tabuVars.tabu_points_history_team_1 = [0]
    tabuVars.tabu_points_history_team_2 = [0]
    tabuVars.tabu_points_this_round = 0

    tabuVars.tabu_guessing_team_num = 0
    tabuVars.tabu_explainer_team_1 = 0
    tabuVars.tabu_explainer_team_2 = 0

    tabuVars.tabu_guessing_card_messages = []
    tabuVars.tabu_time_messages = []

    tabu_is_running = False
    tabu_is_pause = False
    tabu_is_switching = False
    tabu_is_raeacting = False

    tabu_points_to_win = 60